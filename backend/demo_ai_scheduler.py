#!/usr/bin/env python3
"""
AI Scheduler Demonstration Script
===================================
This script demonstrates the Google Gemini AI-powered remedial class scheduling system.
It shows how students with marks < 10 are automatically scheduled with appropriate teachers.
"""

import asyncio
import httpx
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
import json

console = Console()

BASE_URL = "http://localhost:8000"


async def clear_database():
    """Clear existing timetables from database."""
    console.print("\n[bold yellow]🗑️  Clearing existing timetables...[/bold yellow]")

    async with httpx.AsyncClient(timeout=30.0) as client:
        # Get all timetables and delete them
        response = await client.get(f"{BASE_URL}/timetables")
        if response.status_code == 200:
            timetables = response.json()
            for tt in timetables:
                await client.delete(f"{BASE_URL}/timetables/{tt['id']}")

    console.print("[green]✓ Timetables cleared successfully[/green]")


async def create_sample_data():
    """Display existing students and teachers."""
    console.print("\n[bold cyan]👥 Loading Existing Data...[/bold cyan]")

    async with httpx.AsyncClient(timeout=30.0) as client:
        # Get existing students
        students_response = await client.get(f"{BASE_URL}/students")
        created_students = students_response.json() if students_response.status_code == 200 else []

        # Get existing teachers
        teachers_response = await client.get(f"{BASE_URL}/teachers")
        created_teachers = teachers_response.json() if teachers_response.status_code == 200 else []

    # Skip if no data exists
    if not created_students and not created_teachers:
        console.print("[yellow]No existing data found. Please add students and teachers first.[/yellow]")
        return [], []

    # Display students table with subject-wise marks
    students_table = Table(title="📚 Students Created", show_header=True, header_style="bold magenta")
    students_table.add_column("ID", style="dim", width=6)
    students_table.add_column("Name", style="cyan", width=20)
    students_table.add_column("Email", style="blue", width=25)
    students_table.add_column("Subject Marks", justify="left", width=50)

    for student in created_students:
        # Display subject marks
        subject_marks = student.get('subject_marks', [])
        if subject_marks:
            marks_display = []
            for sm in subject_marks:
                marks_style = "[red]" if sm['marks'] < 10 else "[green]"
                marks_display.append(f"{sm['subject_name']}: {marks_style}{sm['marks']}/30[/{marks_style.strip('[')}]")
            marks_str = ", ".join(marks_display)
        else:
            marks_str = "[dim]No subject marks[/dim]"

        students_table.add_row(
            str(student['id']),
            student['name'],
            student['email'],
            marks_str
        )

    console.print(students_table)

    # Display teachers table
    teachers_table = Table(title="👨‍🏫 Teachers Created", show_header=True, header_style="bold green")
    teachers_table.add_column("ID", style="dim", width=6)
    teachers_table.add_column("Name", style="cyan")
    teachers_table.add_column("Subject", style="yellow")
    teachers_table.add_column("Availability", style="blue")

    for teacher in created_teachers:
        teachers_table.add_row(
            str(teacher['id']),
            teacher['name'],
            teacher['subject'] or "N/A",
            teacher['availability'] or "N/A"
        )

    console.print(teachers_table)

    return created_students, created_teachers


async def run_ai_scheduling():
    """Run the AI-powered scheduling."""
    console.print("\n" + "="*80)
    console.print(Panel.fit(
        "[bold white on blue] 🤖 RUNNING GOOGLE GEMINI 2.0 FLASH AI SCHEDULER [/bold white on blue]",
        border_style="blue"
    ))
    console.print("="*80 + "\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]AI is analyzing students and generating optimal schedule...", total=None)

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(f"{BASE_URL}/timetables/auto")

        progress.stop()

    if response.status_code == 200:
        schedules = response.json()

        console.print(f"\n[bold green]✓ AI Scheduling Complete![/bold green]")
        console.print(f"[dim]Generated {len(schedules)} remedial class sessions[/dim]\n")

        # Display schedule table
        schedule_table = Table(
            title="📅 AI-Generated Remedial Class Schedule",
            show_header=True,
            header_style="bold cyan",
            border_style="green"
        )
        schedule_table.add_column("Session", style="dim", width=8)
        schedule_table.add_column("Student ID", justify="center")
        schedule_table.add_column("Teacher ID", justify="center")
        schedule_table.add_column("Start Time", style="yellow")
        schedule_table.add_column("End Time", style="yellow")
        schedule_table.add_column("Location", style="magenta")
        schedule_table.add_column("Notes", style="blue")

        for idx, schedule in enumerate(schedules, 1):
            schedule_table.add_row(
                f"#{idx}",
                str(schedule['student_id']),
                str(schedule['teacher_id']),
                schedule['slot_start'],
                schedule['slot_end'],
                schedule['location'],
                schedule['notes']
            )

        console.print(schedule_table)

        # Get student and teacher details
        async with httpx.AsyncClient() as client:
            students_response = await client.get(f"{BASE_URL}/students")
            teachers_response = await client.get(f"{BASE_URL}/teachers")

            students = {s['id']: s for s in students_response.json()}
            teachers = {t['id']: t for t in teachers_response.json()}

        # Display detailed schedule
        console.print("\n[bold cyan]📋 Detailed Schedule Breakdown:[/bold cyan]\n")

        for idx, schedule in enumerate(schedules, 1):
            student = students.get(schedule['student_id'], {})
            teacher = teachers.get(schedule['teacher_id'], {})

            # Extract subject from notes (format: "Subject remedial session")
            subject = schedule['notes'].split(' remedial')[0] if 'remedial' in schedule['notes'] else 'N/A'

            # Find the student's marks in this subject
            student_subject_marks = student.get('subject_marks', [])
            subject_mark = next((sm for sm in student_subject_marks if sm['subject_name'] == subject), None)
            marks_display = f"{subject_mark['marks']}/30" if subject_mark else "N/A"

            panel_content = f"""
[bold]Student:[/bold] {student.get('name', 'Unknown')}
[bold]Subject:[/bold] {subject} (Student's marks: [red]{marks_display}[/red])
[bold]Teacher:[/bold] {teacher.get('name', 'Unknown')} ([yellow]{teacher.get('subject', 'N/A')}[/yellow])
[bold]Time:[/bold] {schedule['slot_start']} → {schedule['slot_end']}
[bold]Location:[/bold] {schedule['location']}
[bold]Notes:[/bold] {schedule['notes']}
            """

            console.print(Panel(
                panel_content.strip(),
                title=f"[bold]Session #{idx}[/bold]",
                border_style="green",
                expand=False
            ))

        return schedules
    else:
        console.print(f"[bold red]✗ Scheduling failed with status {response.status_code}[/bold red]")
        console.print(f"[red]{response.text}[/red]")
        return None


async def main():
    """Main demonstration function."""
    console.print("\n" + "="*80)
    console.print(Panel.fit(
        "[bold white on green] AI-POWERED REMEDIAL CLASS TIMETABLE GENERATOR [/bold white on green]\n"
        "[dim]Powered by Google Gemini 2.0 Flash[/dim]",
        border_style="green"
    ))
    console.print("="*80)

    try:
        # Step 1: Clear timetables
        await clear_database()

        # Step 2: Load existing data
        students, teachers = await create_sample_data()

        if not students:
            console.print("\n[red]Cannot run demonstration without data![/red]")
            return

        # Step 3: Run AI scheduling
        schedules = await run_ai_scheduling()

        if schedules:
            # Count subjects where students have marks < 10
            failing_subject_count = 0
            for s in students:
                for sm in s.get('subject_marks', []):
                    if sm['marks'] < 10:
                        failing_subject_count += 1

            console.print("\n" + "="*80)
            console.print(Panel.fit(
                f"[bold green]✓ DEMONSTRATION COMPLETE[/bold green]\n\n"
                f"[white]Failing subject instances (marks < 10):[/white] [red]{failing_subject_count}[/red]\n"
                f"[white]Remedial sessions scheduled:[/white] [green]{len(schedules)}[/green]\n"
                f"[white]AI Model:[/white] [cyan]Google Gemini 2.0 Flash[/cyan]",
                border_style="green"
            ))
            console.print("="*80 + "\n")

            console.print("[bold cyan]🎯 Key Features Demonstrated:[/bold cyan]")
            console.print("  ✓ Subject-wise marks tracking (out of 30)")
            console.print("  ✓ Automatic filtering of students failing specific subjects (marks < 10/30)")
            console.print("  ✓ AI-powered conflict-free scheduling")
            console.print("  ✓ Intelligent teacher-subject matching")
            console.print("  ✓ Availability consideration")
            console.print("  ✓ Optimal time slot allocation\n")

    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")


if __name__ == "__main__":
    asyncio.run(main())

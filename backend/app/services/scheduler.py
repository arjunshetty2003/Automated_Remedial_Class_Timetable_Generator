from __future__ import annotations

import json
from collections.abc import Sequence
from datetime import datetime, timedelta
from typing import Any
import httpx

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from app import schemas
from app.core.config import get_settings
from app.models.student import Student


class SchedulerService:
    """Coordinates AI-assisted timetable generation."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def _expand_class_timetables(
        self,
        timetables: list[schemas.TimetableRead]
    ) -> list[dict[str, Any]]:
        """
        Expand class-level timetables into individual student schedules.

        For class-level timetables (where class_id is set), we need to create
        individual schedule entries for each student in that class to check conflicts.
        """
        expanded_schedules = []

        for tt in timetables:
            if tt.class_id:
                # This is a class-level timetable - expand to all students in the class
                stmt = select(Student).where(Student.class_id == tt.class_id)
                result = await self._session.execute(stmt)
                students_in_class = result.scalars().all()

                for student in students_in_class:
                    expanded_schedules.append({
                        "student_id": student.id,
                        "teacher_id": tt.teacher_id,
                        "slot_start": tt.slot_start.isoformat(),
                        "slot_end": tt.slot_end.isoformat(),
                        "type": "regular",
                        "subject": tt.subject,
                    })
            elif tt.student_id:
                # Individual timetable - add as is
                expanded_schedules.append({
                    "student_id": tt.student_id,
                    "teacher_id": tt.teacher_id,
                    "slot_start": tt.slot_start.isoformat(),
                    "slot_end": tt.slot_end.isoformat(),
                    "type": "regular",
                })

        return expanded_schedules

    async def generate_timetable(
        self,
        students: Sequence[schemas.StudentRead],
        teachers: Sequence[schemas.TeacherRead],
        existing_timetables: list[schemas.TimetableRead] | None = None,
    ) -> list[schemas.TimetableRead]:
        """
        Generate conflict-free timetable using AI.

        Process:
        1. Find students with subject marks < 10 (out of 30)
        2. Match students to teachers by failing subject
        3. Check existing regular timetables to avoid conflicts
        4. Use AI to analyze availabilities and find optimal time slots
        5. Return scheduled timetable entries
        """

        # Build list of student-subject pairs that need remedial classes
        remedial_needs = []
        for student in students:
            for subject_mark in student.subject_marks:
                if subject_mark.marks < 10:  # Failing threshold: < 10 out of 30
                    remedial_needs.append({
                        "student": student,
                        "subject": subject_mark.subject_name,
                        "marks": subject_mark.marks
                    })

        if not remedial_needs:
            return []

        if not teachers:
            return []

        # Expand class-level timetables into individual student schedules for conflict checking
        expanded_schedules = await self._expand_class_timetables(existing_timetables or [])

        # Prepare data for AI including existing schedules
        schedule_request = await self._prepare_schedule_request_subject_based(
            remedial_needs, teachers, expanded_schedules
        )

        # Get AI-generated schedule
        ai_schedule = await self._call_ai_scheduler(schedule_request)

        # Convert AI response to TimetableRead objects
        timetable_entries = self._parse_ai_response(ai_schedule, students, teachers)

        return timetable_entries

    async def _prepare_schedule_request_subject_based(
        self,
        remedial_needs: list[dict[str, Any]],
        teachers: Sequence[schemas.TeacherRead],
        expanded_schedules: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Prepare the scheduling request data for AI with subject-specific information."""

        return {
            "remedial_needs": [
                {
                    "student_id": need["student"].id,
                    "student_name": need["student"].name,
                    "subject": need["subject"],
                    "marks": need["marks"],
                    "availability": need["student"].availability or "Not specified",
                }
                for need in remedial_needs
            ],
            "teachers": [
                {
                    "id": t.id,
                    "name": t.name,
                    "subject": t.subject or "General",
                    "availability": t.availability or "Not specified",
                }
                for t in teachers
            ],
            "existing_schedules": expanded_schedules,  # Already expanded from class-level
        }

    def _prepare_schedule_request(
        self,
        students: Sequence[schemas.StudentRead],
        teachers: Sequence[schemas.TeacherRead],
    ) -> dict[str, Any]:
        """Prepare the scheduling request data for AI (legacy method)."""

        return {
            "students": [
                {
                    "id": s.id,
                    "name": s.name,
                    "marks": s.marks,
                    "availability": s.availability or "Not specified",
                }
                for s in students
            ],
            "teachers": [
                {
                    "id": t.id,
                    "name": t.name,
                    "subject": t.subject or "General",
                    "availability": t.availability or "Not specified",
                }
                for t in teachers
            ],
        }

    async def _call_ai_scheduler(self, schedule_request: dict[str, Any]) -> str:
        """Call AI model to generate the schedule."""

        settings = get_settings()

        # Create the prompt
        system_prompt = """You are an intelligent scheduling assistant for a remedial class timetable system.

Your task is to create a conflict-free schedule that matches students with teachers based on the specific subjects they are failing.

Note: Marks are out of 30. Students with marks < 10 need remedial classes.

Guidelines:
1. CRITICAL: Match students with teachers who teach the subject they are failing
2. Each remedial need is for a specific subject - student must get help in THAT subject only
3. Avoid scheduling conflicts - no student or teacher should have overlapping sessions
4. Consider the availability constraints provided
5. Schedule sessions during reasonable hours (9 AM - 6 PM on weekdays)
6. Each session should be 1 hour long
7. Distribute the load evenly across teachers
8. Include the subject name in the notes

Return your response as a JSON array with this structure:
[
  {
    "student_id": 1,
    "teacher_id": 1,
    "slot_start": "2024-01-15T10:00:00",
    "slot_end": "2024-01-15T11:00:00",
    "location": "Room 101",
    "notes": "Mathematics remedial session"
  }
]

Important: Only return the JSON array, no additional text."""

        # Check if we have subject-based data or legacy data
        if 'remedial_needs' in schedule_request:
            existing_schedules_info = ""
            if schedule_request.get('existing_schedules'):
                existing_schedules_info = f"""

IMPORTANT: The following regular class schedules already exist. DO NOT schedule remedial classes that conflict with these times:
{json.dumps(schedule_request['existing_schedules'], indent=2)}

You MUST ensure that:
1. No student is scheduled for remedial class during their regular class time
2. No teacher is scheduled for remedial class during their regular teaching time"""

            user_prompt = f"""Please schedule remedial classes for students failing specific subjects:

Students and their failing subjects (marks < 10 out of 30):
{json.dumps(schedule_request['remedial_needs'], indent=2)}

Available teachers:
{json.dumps(schedule_request['teachers'], indent=2)}{existing_schedules_info}

Generate a conflict-free schedule starting from next Monday. Match each student with a teacher who teaches their failing subject."""
        else:
            # Legacy format
            user_prompt = f"""Please schedule remedial classes for the following students and teachers:

Students needing remedial classes:
{json.dumps(schedule_request['students'], indent=2)}

Available teachers:
{json.dumps(schedule_request['teachers'], indent=2)}

Generate a conflict-free schedule starting from next Monday."""

        # Try OpenAI first, fall back to Gemini
        try:
            if settings.openai_api_key:
                llm = ChatOpenAI(
                    model="gpt-4",
                    temperature=0.3,
                    api_key=settings.openai_api_key,
                )
                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=user_prompt),
                ]
                response = await llm.ainvoke(messages)
                return response.content
            elif settings.google_api_key:
                # Use Gemini REST API directly (v1 API)
                full_prompt = f"{system_prompt}\n\n{user_prompt}"
                url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={settings.google_api_key}"

                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        url,
                        json={
                            "contents": [{
                                "parts": [{"text": full_prompt}]
                            }]
                        },
                        timeout=60.0
                    )
                    response.raise_for_status()
                    result = response.json()
                    return result["candidates"][0]["content"]["parts"][0]["text"]
            else:
                # Return a simple scheduling algorithm if no AI keys are configured
                return self._fallback_schedule(schedule_request)

        except Exception as e:
            # Fallback to simple scheduling if AI fails
            print(f"AI scheduling failed: {e}, using fallback method")
            return self._fallback_schedule(schedule_request)

    def _fallback_schedule(self, schedule_request: dict[str, Any]) -> str:
        """Simple fallback scheduling algorithm without AI."""

        teachers = schedule_request["teachers"]

        if not teachers:
            return "[]"

        # Handle both subject-based and legacy formats
        if 'remedial_needs' in schedule_request:
            # Subject-based format
            remedial_items = schedule_request['remedial_needs']
        else:
            # Legacy format - convert to remedial_needs format
            remedial_items = [
                {
                    "student_id": s["id"],
                    "student_name": s.get("name", "Unknown"),
                    "subject": "General",
                    "marks": s.get("marks", 0)
                }
                for s in schedule_request.get("students", [])
            ]

        if not remedial_items:
            return "[]"

        schedule = []
        # Start from next Monday at 9 AM
        from datetime import datetime, timedelta
        today = datetime.now()
        days_ahead = 0 - today.weekday()  # Monday is 0
        if days_ahead <= 0:
            days_ahead += 7
        next_monday = today + timedelta(days=days_ahead)
        next_monday = next_monday.replace(hour=9, minute=0, second=0, microsecond=0)

        current_time = next_monday
        teacher_idx = 0

        for remedial_item in remedial_items:
            # Try to match student with teacher by subject
            subject = remedial_item.get("subject", "General")
            matched_teacher = None

            for teacher in teachers:
                if teacher.get("subject", "").lower() == subject.lower():
                    matched_teacher = teacher
                    break

            # If no match, use round-robin
            if not matched_teacher:
                matched_teacher = teachers[teacher_idx % len(teachers)]
                teacher_idx += 1

            slot_start = current_time
            slot_end = current_time + timedelta(hours=1)

            schedule.append({
                "student_id": remedial_item["student_id"],
                "teacher_id": matched_teacher["id"],
                "slot_start": slot_start.isoformat(),
                "slot_end": slot_end.isoformat(),
                "location": f"Room {100 + (teacher_idx % 10)}",
                "notes": f"{subject} remedial session (marks: {remedial_item.get('marks', 'N/A')}/30)"
            })

            # Move to next hour
            current_time += timedelta(hours=1)

            # If past 6 PM, move to next day at 9 AM
            if current_time.hour >= 18:
                current_time = (current_time + timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)

        return json.dumps(schedule, indent=2)

    def _parse_ai_response(
        self,
        ai_response: str,
        students: Sequence[schemas.StudentRead],
        teachers: Sequence[schemas.TeacherRead],
    ) -> list[schemas.TimetableRead]:
        """Parse AI response and convert to TimetableRead objects."""

        try:
            # Extract JSON from the response (AI might add extra text)
            response_text = ai_response.strip()

            # Find JSON array in the response
            start_idx = response_text.find("[")
            end_idx = response_text.rfind("]") + 1

            if start_idx == -1 or end_idx == 0:
                print("No JSON array found in AI response")
                return []

            json_str = response_text[start_idx:end_idx]
            schedule_data = json.loads(json_str)

            # Convert to TimetableRead objects
            timetable_entries = []

            for entry in schedule_data:
                try:
                    timetable_entry = schemas.TimetableRead(
                        id=0,  # Will be assigned by database
                        student_id=entry["student_id"],
                        teacher_id=entry["teacher_id"],
                        slot_start=datetime.fromisoformat(entry["slot_start"].replace("Z", "+00:00")),
                        slot_end=datetime.fromisoformat(entry["slot_end"].replace("Z", "+00:00")),
                        location=entry.get("location", "TBD"),
                        notes=entry.get("notes", ""),
                    )
                    timetable_entries.append(timetable_entry)
                except (KeyError, ValueError) as e:
                    print(f"Skipping invalid entry: {e}")
                    continue

            return timetable_entries

        except json.JSONDecodeError as e:
            print(f"Failed to parse AI response as JSON: {e}")
            return []
        except Exception as e:
            print(f"Error parsing AI response: {e}")
            return []

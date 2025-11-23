#!/usr/bin/env python3
"""
Script to populate sample regular timetables for students and teachers.
This creates a regular class schedule that remedial classes must work around.
"""
import asyncio
import httpx
from datetime import datetime, timedelta


BASE_URL = "http://localhost:8000"


# Define regular class schedule (weekdays, specific times)
# Format: {day_of_week: [(subject, teacher_id, time_slot, location)]}
REGULAR_SCHEDULE = {
    "Monday": [
        ("Mathematics", 1, "09:00-10:00", "Room A1"),
        ("Physics", 2, "10:00-11:00", "Lab 1"),
        ("Chemistry", 5, "11:00-12:00", "Lab 2"),
        ("Computer Science", 6, "14:00-15:00", "Computer Lab"),
    ],
    "Tuesday": [
        ("Mathematics", 3, "09:00-10:00", "Room A2"),
        ("Physics", 4, "10:00-11:00", "Lab 1"),
        ("Chemistry", 5, "13:00-14:00", "Lab 2"),
        ("Computer Science", 6, "14:00-15:00", "Computer Lab"),
    ],
    "Wednesday": [
        ("Mathematics", 1, "09:00-10:00", "Room A1"),
        ("Physics", 2, "11:00-12:00", "Lab 1"),
        ("Chemistry", 5, "13:00-14:00", "Lab 2"),
        ("Computer Science", 6, "15:00-16:00", "Computer Lab"),
    ],
    "Thursday": [
        ("Mathematics", 3, "10:00-11:00", "Room A2"),
        ("Physics", 4, "11:00-12:00", "Lab 1"),
        ("Chemistry", 5, "14:00-15:00", "Lab 2"),
    ],
    "Friday": [
        ("Mathematics", 1, "09:00-10:00", "Room A1"),
        ("Physics", 4, "10:00-11:00", "Lab 1"),
        ("Chemistry", 5, "11:00-12:00", "Lab 2"),
    ],
}


# Students attending each class
STUDENTS_PER_CLASS = {
    "Mathematics": [1, 2, 4, 6, 9],  # Student IDs
    "Physics": [1, 2, 6, 9],
    "Chemistry": [1, 2, 5, 9],
    "Computer Science": [5, 9],
}


async def get_next_weekday(weekday_name: str) -> datetime:
    """Get the next occurrence of a specific weekday."""
    weekdays = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
    }

    today = datetime.now()
    target_weekday = weekdays[weekday_name]
    days_ahead = target_weekday - today.weekday()

    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7

    return today + timedelta(days=days_ahead)


async def populate_regular_timetables():
    """Create regular class timetables for all students and teachers."""

    print("\n" + "="*80)
    print("POPULATING REGULAR CLASS TIMETABLES")
    print("="*80 + "\n")

    total_created = 0

    async with httpx.AsyncClient(timeout=30.0) as client:
        for day_name, classes in REGULAR_SCHEDULE.items():
            day_date = await get_next_weekday(day_name)
            print(f"\n📅 {day_name} ({day_date.strftime('%Y-%m-%d')})")
            print("-" * 60)

            for subject, teacher_id, time_slot, location in classes:
                start_time_str, end_time_str = time_slot.split("-")
                start_hour, start_min = map(int, start_time_str.split(":"))
                end_hour, end_min = map(int, end_time_str.split(":"))

                slot_start = day_date.replace(hour=start_hour, minute=start_min, second=0, microsecond=0)
                slot_end = day_date.replace(hour=end_hour, minute=end_min, second=0, microsecond=0)

                students_in_class = STUDENTS_PER_CLASS.get(subject, [])

                print(f"\n  {subject} ({time_slot}) - Teacher ID {teacher_id} - {location}")

                for student_id in students_in_class:
                    payload = {
                        "student_id": student_id,
                        "teacher_id": teacher_id,
                        "timetable_type": "regular",
                        "slot_start": slot_start.isoformat(),
                        "slot_end": slot_end.isoformat(),
                        "location": location,
                        "notes": f"Regular {subject} class"
                    }

                    try:
                        response = await client.post(
                            f"{BASE_URL}/timetables",
                            json=payload
                        )

                        if response.status_code == 201:
                            print(f"    ✓ Student {student_id} enrolled")
                            total_created += 1
                        else:
                            print(f"    ❌ Failed for Student {student_id}: {response.text}")

                    except Exception as e:
                        print(f"    ❌ Error for Student {student_id}: {e}")

    print("\n" + "="*80)
    print(f"✓ Created {total_created} regular class timetable entries")
    print("="*80 + "\n")

    # Display summary
    print("\n📊 SUMMARY:")
    print("-" * 60)

    async with httpx.AsyncClient(timeout=30.0) as client:
        # Get regular timetables
        response = await client.get(f"{BASE_URL}/timetables?timetable_type=regular")
        if response.status_code == 200:
            regular_timetables = response.json()
            print(f"Total regular classes in database: {len(regular_timetables)}")

            # Group by day
            by_day = {}
            for tt in regular_timetables:
                day = datetime.fromisoformat(tt['slot_start'].replace('Z', '+00:00')).strftime('%A')
                by_day[day] = by_day.get(day, 0) + 1

            print("\nClasses per day:")
            for day, count in sorted(by_day.items()):
                print(f"  {day}: {count} classes")


if __name__ == "__main__":
    asyncio.run(populate_regular_timetables())

#!/usr/bin/env python3
"""
Script to populate class-level regular timetables.
This creates regular class schedules for entire classes (not individual students).
Remedial classes must work around these schedules.

Run this AFTER:
1. populate_classes.py
2. Creating teachers
3. Assigning students to classes
"""
import asyncio
import httpx
from datetime import datetime, timedelta


BASE_URL = "http://localhost:8000"


# Define regular class schedule - CLASS-LEVEL
# Format: {day_of_week: [(class_id, subject, teacher_id, time_slot, location)]}
REGULAR_SCHEDULE = {
    "Monday": [
        (1, "Mathematics", 1, "09:00-10:00", "Room A1"),
        (1, "Physics", 2, "10:00-11:00", "Lab 1"),
        (1, "Chemistry", 5, "11:00-12:00", "Lab 2"),
        (1, "Computer Science", 6, "14:00-15:00", "Computer Lab"),
        (2, "Mathematics", 3, "09:00-10:00", "Room A2"),
        (2, "Physics", 4, "10:00-11:00", "Lab 1"),
    ],
    "Tuesday": [
        (1, "Mathematics", 3, "09:00-10:00", "Room A2"),
        (1, "Physics", 4, "10:00-11:00", "Lab 1"),
        (1, "Chemistry", 5, "13:00-14:00", "Lab 2"),
        (2, "Computer Science", 6, "14:00-15:00", "Computer Lab"),
        (2, "Mathematics", 1, "09:00-10:00", "Room A1"),
    ],
    "Wednesday": [
        (1, "Mathematics", 1, "09:00-10:00", "Room A1"),
        (1, "Physics", 2, "11:00-12:00", "Lab 1"),
        (1, "Chemistry", 5, "13:00-14:00", "Lab 2"),
        (2, "Computer Science", 6, "15:00-16:00", "Computer Lab"),
        (2, "Physics", 2, "10:00-11:00", "Lab 1"),
    ],
    "Thursday": [
        (1, "Mathematics", 3, "10:00-11:00", "Room A2"),
        (1, "Physics", 4, "11:00-12:00", "Lab 1"),
        (1, "Chemistry", 5, "14:00-15:00", "Lab 2"),
        (2, "Mathematics", 3, "09:00-10:00", "Room A2"),
        (2, "Chemistry", 5, "13:00-14:00", "Lab 2"),
    ],
    "Friday": [
        (1, "Mathematics", 1, "09:00-10:00", "Room A1"),
        (1, "Physics", 4, "10:00-11:00", "Lab 1"),
        (1, "Chemistry", 5, "11:00-12:00", "Lab 2"),
        (2, "Computer Science", 6, "14:00-15:00", "Computer Lab"),
        (2, "Physics", 4, "10:00-11:00", "Lab 1"),
    ],
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
    """Create class-level regular timetables."""

    print("\n" + "="*80)
    print("POPULATING CLASS-LEVEL REGULAR TIMETABLES")
    print("="*80 + "\n")

    total_created = 0

    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        # First, verify classes exist
        try:
            response = await client.get(f"{BASE_URL}/classes/")
            if response.status_code == 200:
                classes = response.json()
                if not classes:
                    print("❌ No classes found! Please run populate_classes.py first.")
                    return
                print(f"✓ Found {len(classes)} classes in database\n")
            else:
                print("❌ Failed to fetch classes. Is the server running?")
                return
        except Exception as e:
            print(f"❌ Error connecting to server: {e}")
            return

        for day_name, class_sessions in REGULAR_SCHEDULE.items():
            day_date = await get_next_weekday(day_name)
            print(f"\n📅 {day_name} ({day_date.strftime('%Y-%m-%d')})")
            print("-" * 60)

            for class_id, subject, teacher_id, time_slot, location in class_sessions:
                start_time_str, end_time_str = time_slot.split("-")
                start_hour, start_min = map(int, start_time_str.split(":"))
                end_hour, end_min = map(int, end_time_str.split(":"))

                slot_start = day_date.replace(hour=start_hour, minute=start_min, second=0, microsecond=0)
                slot_end = day_date.replace(hour=end_hour, minute=end_min, second=0, microsecond=0)

                payload = {
                    "class_id": class_id,  # CLASS-LEVEL (not student_id)
                    "student_id": None,    # No individual student
                    "teacher_id": teacher_id,
                    "timetable_type": "regular",
                    "slot_start": slot_start.isoformat(),
                    "slot_end": slot_end.isoformat(),
                    "location": location,
                    "subject": subject,
                    "notes": f"Regular {subject} class for entire class"
                }

                try:
                    response = await client.post(
                        f"{BASE_URL}/timetables",
                        json=payload
                    )

                    if response.status_code == 201:
                        print(f"  ✓ Class {class_id} - {subject} ({time_slot}) - Teacher {teacher_id} - {location}")
                        total_created += 1
                    else:
                        print(f"  ❌ Failed for Class {class_id} - {subject}: {response.text}")

                except Exception as e:
                    print(f"  ❌ Error for Class {class_id} - {subject}: {e}")

    print("\n" + "="*80)
    print(f"✓ Created {total_created} class-level regular timetable entries")
    print("="*80 + "\n")

    # Display summary
    print("\n📊 SUMMARY:")
    print("-" * 60)

    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
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

            # Group by class
            by_class = {}
            for tt in regular_timetables:
                class_id = tt.get('class_id')
                if class_id:
                    by_class[class_id] = by_class.get(class_id, 0) + 1

            print("\nClasses per class:")
            for class_id, count in sorted(by_class.items()):
                print(f"  Class {class_id}: {count} sessions")


if __name__ == "__main__":
    asyncio.run(populate_regular_timetables())

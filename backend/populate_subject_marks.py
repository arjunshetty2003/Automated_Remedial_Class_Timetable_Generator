#!/usr/bin/env python3
"""
Script to populate subject-wise marks for existing students.
This adds sample subject marks to demonstrate the subject-based remedial scheduling.
Marks are out of 30 (passing threshold is 10/30).
"""
import asyncio
import httpx


BASE_URL = "http://localhost:8000"

# Subject-wise marks for each student
# Format: {student_id: {subject: marks}}
# Marks are out of 30
SUBJECT_MARKS_DATA = {
    1: {  # Rahul Kumar
        "Mathematics": 8,
        "Physics": 12,
        "Chemistry": 9,
        "Computer Science": 15
    },
    2: {  # Priya Sharma
        "Mathematics": 14,
        "Physics": 6,
        "Chemistry": 7,
        "Computer Science": 11
    },
    4: {  # Aarav Sharma
        "Mathematics": 7,
        "Physics": 15,
        "Chemistry": 18,
        "Computer Science": 12
    },
    5: {  # Diya Patel
        "Mathematics": 16,
        "Physics": 11,
        "Chemistry": 5,
        "Computer Science": 9
    },
    6: {  # Rohan Kumar
        "Mathematics": 9,
        "Physics": 8,
        "Chemistry": 14,
        "Computer Science": 16
    },
    8: {  # Arjun Reddy
        "Mathematics": 22,
        "Physics": 19,
        "Chemistry": 25,
        "Computer Science": 21
    },
    9: {  # Ananya Gupta
        "Mathematics": 11,
        "Physics": 6,
        "Chemistry": 8,
        "Computer Science": 5
    },
    3: {  # Amit Singh
        "Mathematics": 15,
        "Physics": 14,
        "Chemistry": 16,
        "Computer Science": 13
    }
}


async def populate_subject_marks():
    """Populate subject marks for all students."""
    print("🎯 Populating Subject-Wise Marks for Students...")
    print("=" * 60)

    async with httpx.AsyncClient(timeout=30.0) as client:
        total_created = 0

        for student_id, subjects in SUBJECT_MARKS_DATA.items():
            print(f"\n📚 Student ID {student_id}:")

            for subject, marks in subjects.items():
                payload = {
                    "student_id": student_id,
                    "subject_name": subject,
                    "marks": marks
                }

                try:
                    response = await client.post(
                        f"{BASE_URL}/subject-marks",
                        json=payload
                    )

                    if response.status_code in [200, 201]:
                        status = "⚠️ NEEDS REMEDIAL" if marks < 10 else "✓ OK"
                        print(f"  {subject:20} {marks:3}/30  {status}")
                        total_created += 1
                    else:
                        print(f"  ❌ Failed to add {subject}: {response.text}")

                except Exception as e:
                    print(f"  ❌ Error adding {subject}: {e}")

    print("\n" + "=" * 60)
    print(f"✅ Successfully created {total_created} subject mark records!")
    print("\n📊 Summary:")
    print(f"   - Total students: {len(SUBJECT_MARKS_DATA)}")
    print(f"   - Subjects per student: 4 (Math, Physics, Chemistry, CS)")
    print(f"   - Total records: {total_created}")


async def show_failing_subjects():
    """Show which students are failing which subjects."""
    print("\n" + "=" * 60)
    print("🚨 Students Needing Remedial Classes by Subject:")
    print("=" * 60)

    subjects = ["Mathematics", "Physics", "Chemistry", "Computer Science"]

    async with httpx.AsyncClient(timeout=30.0) as client:
        for subject in subjects:
            print(f"\n📖 {subject}:")

            try:
                response = await client.get(
                    f"{BASE_URL}/subject-marks",
                    params={"student_id": None}
                )

                if response.status_code == 200:
                    marks = response.json()
                    failing = [
                        m for m in marks
                        if m["subject_name"] == subject and m["marks"] < 10
                    ]

                    if failing:
                        for mark in failing:
                            print(f"   - Student ID {mark['student_id']}: {mark['marks']}/30")
                    else:
                        print("   ✓ No students failing")

            except Exception as e:
                print(f"   ❌ Error: {e}")


async def main():
    """Main function."""
    print("\n" + "=" * 60)
    print(" SUBJECT-WISE MARKS POPULATION SCRIPT")
    print("=" * 60)

    try:
        await populate_subject_marks()
        await show_failing_subjects()

        print("\n" + "=" * 60)
        print("✨ Done! You can now use subject-based AI scheduling.")
        print("=" * 60)
        print("\n💡 Next steps:")
        print("   1. View subject marks: GET /subject-marks")
        print("   2. Run AI scheduler: POST /timetables/auto")
        print("   3. View students failing a subject: GET /subject-marks/students-failing/{subject}")
        print()

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

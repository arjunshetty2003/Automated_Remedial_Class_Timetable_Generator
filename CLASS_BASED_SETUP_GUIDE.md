# Class-Based Remedial Timetable System - Setup Guide

## 🎯 Overview

This system now supports **class-based organization** where:
- Students are organized into classes (e.g., "10A", "12 Science B")
- Regular timetables are created at the **class level** (entire class attends together)
- Remedial timetables are created for **individual students** who are failing
- The AI scheduler automatically avoids conflicts between regular and remedial classes

---

## 📋 Prerequisites

1. ✅ Supabase database configured in `.env`
2. ✅ Backend virtual environment activated
3. ✅ All dependencies installed (`pip install -r requirements.txt` or `uv sync`)

---

## 🚀 Complete Setup Steps

### Step 1: Run Database Migration

```bash
cd backend
source .venv/bin/activate
alembic upgrade head
```

This creates:
- `classes` table
- Adds `class_id` to `students` table
- Updates `timetable` table to support both class-level and individual schedules

### Step 2: Create Classes

```bash
python populate_classes.py
```

**Creates 5 classes:**
- 10A (Grade 10, Section A)
- 10B (Grade 10, Section B)
- 11 Science
- 12 Science A
- 12 Science B

### Step 3: Create Teachers

If teachers don't exist yet, create them via API or a script:

```bash
# Example: Using curl
curl -X POST http://localhost:8000/teachers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. Rajesh Gupta",
    "email": "rajesh@school.edu",
    "subject": "Mathematics",
    "availability": "Mon-Fri 9AM-5PM"
  }'
```

Or use your existing teacher population script.

### Step 4: Create Students

Create students and assign them to classes:

```bash
# If you already have students, assign them to classes
python assign_students_to_classes.py

# Or create new students via API with class_id
curl -X POST http://localhost:8000/students \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Rahul Kumar",
    "email": "rahul@student.edu",
    "marks": 15,
    "class_id": 1,
    "availability": "Evenings preferred"
  }'
```

### Step 5: Add Subject Marks

```bash
python populate_subject_marks.py
```

This adds subject-wise marks for each student. Students with marks < 10 will need remedial classes.

### Step 6: Create Class-Level Regular Timetables

```bash
python populate_regular_timetables_class_based.py
```

**This creates regular class schedules** where entire classes attend lectures together. Example:
- Class 10A has Mathematics on Monday 9-10 AM
- All students in Class 10A attend this lecture
- The AI will avoid scheduling remedial classes during this time for any student in Class 10A

### Step 7: Generate Remedial Timetables

Now run the AI scheduler to generate conflict-free remedial schedules:

```bash
# Option 1: Visual demo script
python demo_ai_scheduler.py

# Option 2: Direct API call
curl -X POST http://localhost:8000/timetables/auto
```

**The AI will:**
1. Find all students with subject marks < 10
2. Match them with teachers who teach that subject
3. Check all regular class schedules (class-level)
4. Generate remedial schedules that avoid conflicts

---

## 📊 How It Works

### Class-Level Timetables (Regular Classes)

```json
{
  "class_id": 1,
  "student_id": null,
  "teacher_id": 5,
  "timetable_type": "regular",
  "slot_start": "2024-01-15T09:00:00",
  "slot_end": "2024-01-15T10:00:00",
  "location": "Room A1",
  "subject": "Mathematics",
  "notes": "Regular Mathematics class for entire class"
}
```

### Individual Timetables (Remedial Classes)

```json
{
  "class_id": null,
  "student_id": 3,
  "teacher_id": 5,
  "timetable_type": "remedial",
  "slot_start": "2024-01-15T15:00:00",
  "slot_end": "2024-01-15T16:00:00",
  "location": "Room B2",
  "subject": "Mathematics",
  "notes": "Mathematics remedial session"
}
```

### Conflict Detection

When generating remedial schedules, the system:

1. **Expands class-level timetables**: Converts class-level schedules to individual student schedules
   - If Class 10A has Math at 9 AM, and Student #3 is in Class 10A
   - System creates a virtual entry: Student #3 has Math at 9 AM

2. **Checks conflicts**: Ensures no remedial class conflicts with:
   - Student's regular class schedule (via their class_id)
   - Teacher's regular teaching schedule

3. **Generates schedule**: AI finds time slots that work for both student and teacher

---

## 🔍 Verification Commands

### Check Classes
```bash
curl http://localhost:8000/classes
```

### Check Students in a Class
```bash
curl http://localhost:8000/classes/1/students
```

### Check Regular Timetables
```bash
curl "http://localhost:8000/timetables?timetable_type=regular"
```

### Check Remedial Timetables
```bash
curl "http://localhost:8000/timetables?timetable_type=remedial"
```

### Check All Timetables for a Student
```bash
# Get student's class_id first
curl http://localhost:8000/students/3

# Then check:
# 1. Class-level timetables for their class
# 2. Individual remedial timetables
```

---

## 📝 API Endpoints Reference

### Classes
- `POST /classes` - Create a new class
- `GET /classes` - List all classes with student count
- `GET /classes/{id}` - Get specific class
- `GET /classes/{id}/students` - Get students in a class
- `PUT /classes/{id}` - Update class
- `DELETE /classes/{id}` - Delete class

### Students
- `POST /students` - Create student (include `class_id`)
- `GET /students` - List all students
- `PUT /students/{id}` - Update student (can change `class_id`)

### Timetables
- `POST /timetables` - Create timetable entry
  - For class-level: set `class_id`, leave `student_id` null
  - For individual: set `student_id`, leave `class_id` null
- `GET /timetables` - List all timetables
- `GET /timetables?timetable_type=regular` - Filter by type
- `POST /timetables/auto` - Generate AI remedial schedule

---

## 🎨 Example Workflow

### 1. Start the Server
```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload
```

### 2. Run Setup Scripts in Order
```bash
# Database schema
alembic upgrade head

# Create organizational structure
python populate_classes.py

# Create teachers (if needed)
# ... via API or script ...

# Create students and assign to classes
python assign_students_to_classes.py  # If students exist
# OR create new students with class_id via API

# Add subject marks
python populate_subject_marks.py

# Create regular class schedules (class-level)
python populate_regular_timetables_class_based.py

# Generate remedial schedules (AI)
python demo_ai_scheduler.py
```

### 3. View Results
```bash
# See the visual demo output, or query via API
curl "http://localhost:8000/timetables?timetable_type=remedial"
```

---

## 🔄 Migration from Old System

If you already have individual student timetables from the old system:

1. **Run migration**: `alembic upgrade head`
2. **Create classes**: `python populate_classes.py`
3. **Assign students to classes**: `python assign_students_to_classes.py`
4. **Clear old regular timetables**: They're individual-based, not class-based
5. **Create new class-level timetables**: `python populate_regular_timetables_class_based.py`
6. **Keep remedial timetables**: They remain individual-based (no change needed)

---

## 💡 Tips

1. **Class Size**: Distribute students evenly across classes for balanced scheduling
2. **Teacher Load**: Monitor how many regular classes vs remedial sessions each teacher has
3. **Room Allocation**: Consider room availability when setting locations
4. **Time Slots**: Regular classes typically 9 AM - 3 PM, remedial classes can be before/after
5. **Conflict Resolution**: If AI can't find slots, consider:
   - Adjusting teacher availability
   - Adding more teachers
   - Spreading remedial sessions across more days

---

## 🐛 Troubleshooting

### "No classes found"
→ Run `python populate_classes.py`

### "Students not assigned to classes"
→ Run `python assign_students_to_classes.py`

### "No regular timetables"
→ Run `python populate_regular_timetables_class_based.py`

### "Remedial scheduling conflicts"
→ Check if:
- Regular timetables are properly created (class-level)
- Students are assigned to correct classes
- Teacher availability is set

---

## 📚 File Reference

### New Scripts
- `populate_classes.py` - Creates classes
- `assign_students_to_classes.py` - Assigns existing students to classes
- `populate_regular_timetables_class_based.py` - Creates class-level regular schedules

### Updated Files
- `app/models/class_model.py` - Class model (NEW)
- `app/models/student.py` - Added `class_id` field
- `app/models/timetable.py` - Added `class_id` and `subject` fields
- `app/services/scheduler.py` - Expands class timetables for conflict checking
- `app/schemas/class_schema.py` - Class API schemas (NEW)
- `app/api/routes/classes.py` - Class API endpoints (NEW)

### Migration
- `alembic/versions/20251123_195713_add_class_organization_structure.py` - Database migration

---

## ✅ Success Criteria

After completing setup, you should have:

- [x] Classes created and visible via API
- [x] Students assigned to classes
- [x] Teachers created with subjects
- [x] Subject marks populated (some < 10)
- [x] Class-level regular timetables created
- [x] AI-generated remedial timetables with no conflicts

---

**🎉 Your class-based remedial timetable system is now ready!**

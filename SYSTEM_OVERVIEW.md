# AI-Powered Remedial Class Timetable Generator

## 🎯 System Overview

This is an intelligent scheduling system that automatically generates **remedial class timetables** for students failing in specific subjects, while **avoiding conflicts** with their regular class schedules.

---

## ✨ Key Features

### 1. **Subject-Wise Performance Tracking**
- Marks tracked individually for each subject (out of 30)
- Subjects: Mathematics, Physics, Chemistry, Computer Science
- **Failing threshold**: < 10/30

### 2. **Dual Timetable System**

#### **Regular Timetables**
- Normal class schedules for all students
- Fixed weekly schedule (Monday-Friday)
- Typical timings: 9AM - 6PM

#### **Remedial Timetables**
- AI-generated schedules for failing students
- **Automatically avoids conflicts** with:
  - Student's regular classes
  - Teacher's regular teaching hours
- Subject-specific teacher matching

### 3. **Intelligent AI Scheduler** (Google Gemini 2.0 Flash)
- Identifies students failing subjects (marks < 10/30)
- Matches students with teachers who teach that specific subject
- Checks existing regular schedules
- Generates conflict-free remedial class schedule
- Considers teacher/student availability

---

## 📊 Database Schema

### **Students**
- Basic info: name, email, marks (overall)
- Availability preferences
- Relationship: `subject_marks` (one-to-many)

### **Subject Marks**
- `student_id` (FK)
- `subject_name` (Mathematics, Physics, Chemistry, CS)
- `marks` (out of 30)

### **Teachers**
- Basic info: name, email, subject
- Availability preferences

### **Timetables**
- `student_id` (FK)
- `teacher_id` (FK)
- **`timetable_type`** - **NEW!** (`regular` or `remedial`)
- `slot_start`, `slot_end`
- `location`, `notes`

---

## 🔄 How It Works

### **Step 1: Regular Schedule Setup**
```bash
python populate_regular_timetables.py
```
Creates weekly regular class schedules for all students.

### **Step 2: Subject Marks Entry**
```bash
python populate_subject_marks.py
```
Adds subject-wise marks for students.

### **Step 3: AI Remedial Scheduling**
```bash
curl -X POST http://localhost:8000/timetables/auto
```
or run the demo:
```bash
python demo_ai_scheduler.py
```

**The AI will**:
1. Find all subject-mark combinations where marks < 10/30
2. Identify which teachers teach those subjects
3. Retrieve all existing regular class schedules
4. Generate remedial schedule avoiding conflicts
5. Return conflict-free timetable entries marked as `remedial`

---

## 🌐 API Endpoints

### **Timetables**
- `GET /timetables` - List all timetables
- `GET /timetables?timetable_type=regular` - Filter by type
- `GET /timetables?timetable_type=remedial` - Get only remedial classes
- `POST /timetables` - Create manual timetable entry
- `POST /timetables/auto` - **AI-generated remedial schedule**
- `DELETE /timetables/{id}` - Delete timetable entry

### **Students**
- `GET /students` - List all students (includes subject_marks)
- `POST /students` - Create student
- `PUT /students/{id}` - Update student

### **Subject Marks**
- `GET /subject-marks` - List all marks
- `GET /subject-marks?student_id={id}` - Filter by student
- `GET /subject-marks/students-failing/{subject}` - Get failing students
- `POST /subject-marks` - Add subject mark

### **Teachers**
- `GET /teachers` - List all teachers
- `POST /teachers` - Create teacher

---

## 🎨 Example Regular Schedule

**Monday**:
- 09:00-10:00: Mathematics (Teacher: Dr. Rajesh Gupta, Room A1)
- 10:00-11:00: Physics (Teacher: Prof. Meera Patel, Lab 1)
- 11:00-12:00: Chemistry (Teacher: Dr. Vikram Desai, Lab 2)
- 14:00-15:00: Computer Science (Teacher: Prof. Anjali Nair, Computer Lab)

**The AI ensures remedial classes don't conflict with these times!**

---

## 📈 Example Remedial Scenario

**Student: Ananya Gupta**
- Mathematics: 11/30 ✅ (passing)
- Physics: 6/30 ❌ (needs remedial)
- Chemistry: 8/30 ❌ (needs remedial)
- Computer Science: 5/30 ❌ (needs remedial)

**AI Action**:
- ✅ Schedules Physics remedial with Prof. Meera (Physics teacher)
- ✅ Schedules Chemistry remedial with Dr. Vikram (Chemistry teacher)
- ✅ Schedules CS remedial with Prof. Anjali (CS teacher)
- ✅ **Avoids** her regular class times (Mon-Fri 9AM-3PM)
- ✅ **Avoids** teachers' regular teaching hours

---

## 💻 Technology Stack

- **Backend**: FastAPI (Python 3.14)
- **Database**: PostgreSQL/Supabase
- **ORM**: SQLAlchemy 2.0
- **AI**: Google Gemini 2.0 Flash
- **API Validation**: Pydantic v2

---

## 🚀 Running the System

### **1. Start the Server**
```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload
```

### **2. Populate Data** (one-time setup)
```bash
# Add regular class schedules
python populate_regular_timetables.py

# Add subject marks
python populate_subject_marks.py
```

### **3. Generate Remedial Schedule**
```bash
# Option 1: Demo script (visual)
python demo_ai_scheduler.py

# Option 2: Direct API call
curl -X POST http://localhost:8000/timetables/auto
```

### **4. View Schedules**
```bash
# All timetables
curl http://localhost:8000/timetables

# Only regular classes
curl "http://localhost:8000/timetables?timetable_type=regular"

# Only remedial classes
curl "http://localhost:8000/timetables?timetable_type=remedial"
```

---

## 📝 Key Files

- `app/models/timetable.py` - Timetable model with type enum
- `app/schemas/timetable.py` - API schemas
- `app/services/scheduler.py` - AI scheduling logic with conflict avoidance
- `app/api/routes/timetables.py` - Timetable endpoints
- `populate_regular_timetables.py` - Creates regular schedules
- `populate_subject_marks.py` - Adds student marks
- `demo_ai_scheduler.py` - Visual demonstration

---

## 🎯 What Makes This Special

1. **Conflict-Free Scheduling**: AI respects existing regular class times
2. **Subject-Specific Matching**: Students get help from teachers who teach their failing subject
3. **Dual Timetable System**: Separate tracking of regular vs remedial classes
4. **Intelligent Filtering**: API can filter timetables by type
5. **Real-Time Conflict Detection**: Checks all existing schedules before scheduling

---

## 📊 Sample Data

- **8 Students** with varying performance
- **6 Teachers** (2 Math, 2 Physics, 1 Chemistry, 1 CS)
- **70+ Regular class entries** (full weekly schedule)
- **12 Remedial sessions** (AI-generated, conflict-free)

---

## 🔮 Future Enhancements

- Frontend UI for viewing both schedules side-by-side
- Calendar view showing regular + remedial classes
- Teacher workload balancing
- Student performance tracking over time
- Automatic rescheduling if conflicts arise

---

*Generated by AI-Powered Remedial Class Timetable Generator*
*Powered by Google Gemini 2.0 Flash* 🤖

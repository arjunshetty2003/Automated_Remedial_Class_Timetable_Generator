export interface SubjectMarkInfo {
  id: number;
  subject_name: string;
  marks: number;
}

export interface Student {
  id: number;
  name: string;
  email: string;
  marks: number;
  availability?: string;
  class_id?: number;
  created_at: string;
  subject_marks?: SubjectMarkInfo[];
}

export interface Teacher {
  id: number;
  name: string;
  email: string;
  subject?: string;
  availability?: string;
  created_at: string;
}

export interface SubjectMark {
  id: number;
  student_id: number;
  subject_name: string;
  marks: number;
  created_at: string;
}

export enum TimetableType {
  REGULAR = "regular",
  REMEDIAL = "remedial"
}

export interface Timetable {
  id: number;
  student_id: number;
  teacher_id: number;
  timetable_type: TimetableType;
  slot_start: string;
  slot_end: string;
  location?: string;
  notes?: string;
  student?: Student;
  teacher?: Teacher;
}

export interface CreateStudentRequest {
  name: string;
  email: string;
  marks: number;
  availability?: string;
  class_id?: number;
}

export interface CreateTeacherRequest {
  name: string;
  email: string;
  subject?: string;
  availability?: string;
}

export interface CreateSubjectMarkRequest {
  student_id: number;
  subject_name: string;
  marks: number;
}

export interface CreateTimetableRequest {
  student_id: number;
  teacher_id: number;
  timetable_type: TimetableType;
  slot_start: string;
  slot_end: string;
  location?: string;
  notes?: string;
}

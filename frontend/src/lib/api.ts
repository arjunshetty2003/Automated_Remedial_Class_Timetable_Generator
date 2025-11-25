import {
  Student,
  Teacher,
  SubjectMark,
  Timetable,
  CreateStudentRequest,
  CreateTeacherRequest,
  CreateSubjectMarkRequest,
  CreateTimetableRequest,
} from "@/types/api";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function fetchAPI<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`API Error: ${response.status} - ${errorText}`);
  }

  return response.json();
}

export const studentsAPI = {
  getAll: () => fetchAPI<Student[]>("/students"),
  getById: (id: number) => fetchAPI<Student>(`/students/${id}`),
  create: (data: CreateStudentRequest) =>
    fetchAPI<Student>("/students", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  update: (id: number, data: Partial<CreateStudentRequest>) =>
    fetchAPI<Student>(`/students/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),
  delete: (id: number) =>
    fetchAPI<void>(`/students/${id}`, { method: "DELETE" }),
};

export const teachersAPI = {
  getAll: () => fetchAPI<Teacher[]>("/teachers"),
  getById: (id: number) => fetchAPI<Teacher>(`/teachers/${id}`),
  create: (data: CreateTeacherRequest) =>
    fetchAPI<Teacher>("/teachers", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  update: (id: number, data: Partial<CreateTeacherRequest>) =>
    fetchAPI<Teacher>(`/teachers/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),
  delete: (id: number) =>
    fetchAPI<void>(`/teachers/${id}`, { method: "DELETE" }),
};

export const subjectMarksAPI = {
  getAll: () => fetchAPI<SubjectMark[]>("/subject-marks"),
  getById: (id: number) => fetchAPI<SubjectMark>(`/subject-marks/${id}`),
  create: (data: CreateSubjectMarkRequest) =>
    fetchAPI<SubjectMark>("/subject-marks", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  update: (id: number, data: Partial<CreateSubjectMarkRequest>) =>
    fetchAPI<SubjectMark>(`/subject-marks/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),
  delete: (id: number) =>
    fetchAPI<void>(`/subject-marks/${id}`, { method: "DELETE" }),
};

export const timetablesAPI = {
  getAll: (type?: string) => {
    const query = type ? `?timetable_type=${type}` : "";
    return fetchAPI<Timetable[]>(`/timetables${query}`);
  },
  getById: (id: number) => fetchAPI<Timetable>(`/timetables/${id}`),
  create: (data: CreateTimetableRequest) =>
    fetchAPI<Timetable>("/timetables", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  delete: (id: number) =>
    fetchAPI<void>(`/timetables/${id}`, { method: "DELETE" }),
  generateRemedial: () => fetchAPI<Timetable[]>("/timetables/auto", {
    method: "POST",
  }),
};

"use client";

import { useEffect, useState } from "react";
import { subjectMarksAPI, studentsAPI } from "@/lib/api";
import type { SubjectMark, Student, CreateSubjectMarkRequest } from "@/types/api";

export default function MarksPage() {
  const [marks, setMarks] = useState<SubjectMark[]>([]);
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState<CreateSubjectMarkRequest>({
    student_id: 0,
    subject: "",
    marks: 0,
    max_marks: 30,
  });
  const [error, setError] = useState<string | null>(null);

  const subjects = [
    "Mathematics",
    "Physics",
    "Chemistry",
    "Computer Science",
    "English",
    "Biology",
  ];

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    try {
      setLoading(true);
      const [marksData, studentsData] = await Promise.all([
        subjectMarksAPI.getAll(),
        studentsAPI.getAll(),
      ]);
      setMarks(marksData);
      setStudents(studentsData);
      setError(null);
    } catch (err) {
      setError("Failed to load data");
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    try {
      await subjectMarksAPI.create(formData);
      setFormData({ student_id: 0, subject: "", marks: 0, max_marks: 30 });
      setShowForm(false);
      loadData();
    } catch (err) {
      setError("Failed to create mark entry");
      console.error(err);
    }
  }

  async function handleDelete(id: number) {
    if (!confirm("Are you sure you want to delete this mark entry?")) return;

    try {
      await subjectMarksAPI.delete(id);
      loadData();
    } catch (err) {
      setError("Failed to delete mark entry");
      console.error(err);
    }
  }

  function getStudentName(studentId: number): string {
    const student = students.find((s) => s.id === studentId);
    return student?.name || `Student ${studentId}`;
  }

  function getMarkStatus(marks: number, maxMarks: number): string {
    const percentage = (marks / maxMarks) * 100;
    if (percentage < 33) return "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200";
    if (percentage < 60) return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200";
    return "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200";
  }

  const failingMarks = marks.filter((m) => m.marks < 10);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-zinc-900 dark:text-white">
            Subject Marks
          </h1>
          <p className="mt-2 text-zinc-600 dark:text-zinc-400">
            Track student performance across subjects (Max: 30 marks)
          </p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-purple-500 hover:bg-purple-600 text-white font-medium py-2 px-4 rounded-lg transition-colors"
        >
          {showForm ? "Cancel" : "Add Mark"}
        </button>
      </div>

      {error && (
        <div className="mb-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {failingMarks.length > 0 && (
        <div className="mb-6 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
          <h3 className="text-red-900 dark:text-red-200 font-semibold mb-2">
            Students Needing Remedial Classes
          </h3>
          <p className="text-red-700 dark:text-red-400 text-sm">
            {failingMarks.length} student(s) have marks below 10/30 and need remedial classes.
          </p>
        </div>
      )}

      {showForm && (
        <div className="mb-8 bg-white dark:bg-zinc-900 shadow rounded-lg p-6">
          <h2 className="text-xl font-semibold text-zinc-900 dark:text-white mb-4">
            Add Subject Mark
          </h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2">
                  Student *
                </label>
                <select
                  required
                  value={formData.student_id}
                  onChange={(e) => setFormData({ ...formData, student_id: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border border-zinc-300 dark:border-zinc-600 rounded-md bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                >
                  <option value={0}>Select a student</option>
                  {students.map((student) => (
                    <option key={student.id} value={student.id}>
                      {student.name} ({student.enrollment_number})
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2">
                  Subject *
                </label>
                <select
                  required
                  value={formData.subject}
                  onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
                  className="w-full px-3 py-2 border border-zinc-300 dark:border-zinc-600 rounded-md bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                >
                  <option value="">Select a subject</option>
                  {subjects.map((subject) => (
                    <option key={subject} value={subject}>
                      {subject}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2">
                  Marks Obtained *
                </label>
                <input
                  type="number"
                  required
                  min={0}
                  max={30}
                  value={formData.marks}
                  onChange={(e) => setFormData({ ...formData, marks: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border border-zinc-300 dark:border-zinc-600 rounded-md bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2">
                  Maximum Marks
                </label>
                <input
                  type="number"
                  value={formData.max_marks}
                  onChange={(e) => setFormData({ ...formData, max_marks: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border border-zinc-300 dark:border-zinc-600 rounded-md bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                  disabled
                />
              </div>
            </div>
            <div className="flex justify-end">
              <button
                type="submit"
                className="bg-purple-500 hover:bg-purple-600 text-white font-medium py-2 px-6 rounded-lg transition-colors"
              >
                Add Mark
              </button>
            </div>
          </form>
        </div>
      )}

      {loading ? (
        <div className="text-center py-12">
          <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-purple-500 border-r-transparent"></div>
          <p className="mt-4 text-zinc-600 dark:text-zinc-400">Loading marks...</p>
        </div>
      ) : marks.length === 0 ? (
        <div className="text-center py-12 bg-white dark:bg-zinc-900 rounded-lg">
          <p className="text-zinc-600 dark:text-zinc-400">No marks found. Add subject marks to track student performance.</p>
        </div>
      ) : (
        <div className="bg-white dark:bg-zinc-900 shadow rounded-lg overflow-hidden">
          <table className="min-w-full divide-y divide-zinc-200 dark:divide-zinc-700">
            <thead className="bg-zinc-50 dark:bg-zinc-800">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                  Student
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                  Subject
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                  Marks
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                  Percentage
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-zinc-900 divide-y divide-zinc-200 dark:divide-zinc-700">
              {marks.map((mark) => {
                const percentage = ((mark.marks / mark.max_marks) * 100).toFixed(1);
                return (
                  <tr key={mark.id} className="hover:bg-zinc-50 dark:hover:bg-zinc-800">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-zinc-900 dark:text-white">
                      {getStudentName(mark.student_id)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-zinc-900 dark:text-white">
                      {mark.subject}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-zinc-900 dark:text-white">
                      {mark.marks} / {mark.max_marks}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-zinc-600 dark:text-zinc-400">
                      {percentage}%
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <span className={`px-2 py-1 text-xs font-semibold rounded-full ${getMarkStatus(mark.marks, mark.max_marks)}`}>
                        {mark.marks < 10 ? "Needs Remedial" : parseFloat(percentage) >= 60 ? "Good" : "Average"}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <button
                        onClick={() => handleDelete(mark.id)}
                        className="text-red-600 hover:text-red-900 dark:text-red-400 dark:hover:text-red-300"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

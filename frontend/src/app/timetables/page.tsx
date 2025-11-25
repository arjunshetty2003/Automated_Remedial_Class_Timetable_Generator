"use client";

import { useEffect, useState } from "react";
import { timetablesAPI, studentsAPI, teachersAPI } from "@/lib/api";
import type { Timetable, Student, Teacher } from "@/types/api";

export default function TimetablesPage() {
  const [timetables, setTimetables] = useState<Timetable[]>([]);
  const [students, setStudents] = useState<Student[]>([]);
  const [teachers, setTeachers] = useState<Teacher[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<"all" | "regular" | "remedial">("all");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadData();
  }, [filter]);

  async function loadData() {
    try {
      setLoading(true);
      const filterParam = filter === "all" ? undefined : filter;
      const [timetablesData, studentsData, teachersData] = await Promise.all([
        timetablesAPI.getAll(filterParam),
        studentsAPI.getAll(),
        teachersAPI.getAll(),
      ]);
      setTimetables(timetablesData);
      setStudents(studentsData);
      setTeachers(teachersData);
      setError(null);
    } catch (err) {
      setError("Failed to load timetables");
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  async function handleDelete(id: number) {
    if (!confirm("Are you sure you want to delete this timetable entry?")) return;

    try {
      await timetablesAPI.delete(id);
      loadData();
    } catch (err) {
      setError("Failed to delete timetable entry");
      console.error(err);
    }
  }

  function getStudentName(studentId: number): string {
    const student = students.find((s) => s.id === studentId);
    return student?.name || `Student ${studentId}`;
  }

  function getTeacherName(teacherId: number): string {
    const teacher = teachers.find((t) => t.id === teacherId);
    return teacher?.name || `Teacher ${teacherId}`;
  }

  function getTeacherSubject(teacherId: number): string {
    const teacher = teachers.find((t) => t.id === teacherId);
    return teacher?.subject || "Unknown";
  }

  function formatDateTime(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleString("en-US", {
      weekday: "short",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  }

  function getDayOfWeek(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", { weekday: "long" });
  }

  const regularCount = timetables.filter((t) => t.timetable_type === "regular").length;
  const remedialCount = timetables.filter((t) => t.timetable_type === "remedial").length;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-zinc-900 dark:text-white">
          Timetables
        </h1>
        <p className="mt-2 text-zinc-600 dark:text-zinc-400">
          View regular and remedial class schedules
        </p>
      </div>

      {error && (
        <div className="mb-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded">
          {error}
        </div>
      )}

      <div className="mb-6 flex gap-4 items-center">
        <div className="flex gap-2">
          <button
            onClick={() => setFilter("all")}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              filter === "all"
                ? "bg-blue-500 text-white"
                : "bg-zinc-200 dark:bg-zinc-700 text-zinc-900 dark:text-white hover:bg-zinc-300 dark:hover:bg-zinc-600"
            }`}
          >
            All ({timetables.length})
          </button>
          <button
            onClick={() => setFilter("regular")}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              filter === "regular"
                ? "bg-purple-500 text-white"
                : "bg-zinc-200 dark:bg-zinc-700 text-zinc-900 dark:text-white hover:bg-zinc-300 dark:hover:bg-zinc-600"
            }`}
          >
            Regular ({regularCount})
          </button>
          <button
            onClick={() => setFilter("remedial")}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              filter === "remedial"
                ? "bg-orange-500 text-white"
                : "bg-zinc-200 dark:bg-zinc-700 text-zinc-900 dark:text-white hover:bg-zinc-300 dark:hover:bg-zinc-600"
            }`}
          >
            Remedial ({remedialCount})
          </button>
        </div>
      </div>

      {loading ? (
        <div className="text-center py-12">
          <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-blue-500 border-r-transparent"></div>
          <p className="mt-4 text-zinc-600 dark:text-zinc-400">Loading timetables...</p>
        </div>
      ) : timetables.length === 0 ? (
        <div className="text-center py-12 bg-white dark:bg-zinc-900 rounded-lg">
          <p className="text-zinc-600 dark:text-zinc-400">
            No timetable entries found. {filter !== "all" && `Try selecting a different filter.`}
          </p>
        </div>
      ) : (
        <div className="bg-white dark:bg-zinc-900 shadow rounded-lg overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-zinc-200 dark:divide-zinc-700">
              <thead className="bg-zinc-50 dark:bg-zinc-800">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                    Type
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                    Student
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                    Teacher
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                    Subject
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                    Day
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                    Time Slot
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                    Location
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white dark:bg-zinc-900 divide-y divide-zinc-200 dark:divide-zinc-700">
                {timetables.map((timetable) => (
                  <tr key={timetable.id} className="hover:bg-zinc-50 dark:hover:bg-zinc-800">
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <span
                        className={`px-2 py-1 text-xs font-semibold rounded-full ${
                          timetable.timetable_type === "regular"
                            ? "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200"
                            : "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200"
                        }`}
                      >
                        {timetable.timetable_type}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-zinc-900 dark:text-white">
                      {getStudentName(timetable.student_id)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-zinc-900 dark:text-white">
                      {getTeacherName(timetable.teacher_id)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-zinc-600 dark:text-zinc-400">
                      {getTeacherSubject(timetable.teacher_id)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-zinc-600 dark:text-zinc-400">
                      {getDayOfWeek(timetable.slot_start)}
                    </td>
                    <td className="px-6 py-4 text-sm text-zinc-600 dark:text-zinc-400">
                      <div className="flex flex-col">
                        <span className="text-xs text-zinc-500 dark:text-zinc-500">Start:</span>
                        <span>{formatDateTime(timetable.slot_start)}</span>
                        <span className="text-xs text-zinc-500 dark:text-zinc-500 mt-1">End:</span>
                        <span>{formatDateTime(timetable.slot_end)}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-zinc-600 dark:text-zinc-400">
                      {timetable.location || "-"}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <button
                        onClick={() => handleDelete(timetable.id)}
                        className="text-red-600 hover:text-red-900 dark:text-red-400 dark:hover:text-red-300"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

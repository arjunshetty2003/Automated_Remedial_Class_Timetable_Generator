"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { studentsAPI, teachersAPI, subjectMarksAPI, timetablesAPI } from "@/lib/api";

export default function Home() {
  const [stats, setStats] = useState({
    students: 0,
    teachers: 0,
    regularClasses: 0,
    remedialClasses: 0,
    failingMarks: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadStats() {
      try {
        const [students, teachers, marks, regularTT, remedialTT] = await Promise.all([
          studentsAPI.getAll(),
          teachersAPI.getAll(),
          subjectMarksAPI.getAll(),
          timetablesAPI.getAll("regular"),
          timetablesAPI.getAll("remedial"),
        ]);

        const failingCount = marks.filter((m) => m.marks < 10).length;

        setStats({
          students: students.length,
          teachers: teachers.length,
          regularClasses: regularTT.length,
          remedialClasses: remedialTT.length,
          failingMarks: failingCount,
        });
      } catch (error) {
        console.error("Failed to load stats:", error);
      } finally {
        setLoading(false);
      }
    }

    loadStats();
  }, []);

  const cards = [
    {
      title: "Students",
      value: stats.students,
      href: "/students",
      color: "bg-blue-500",
    },
    {
      title: "Teachers",
      value: stats.teachers,
      href: "/teachers",
      color: "bg-green-500",
    },
    {
      title: "Regular Classes",
      value: stats.regularClasses,
      href: "/timetables",
      color: "bg-purple-500",
    },
    {
      title: "Remedial Classes",
      value: stats.remedialClasses,
      href: "/timetables",
      color: "bg-orange-500",
    },
    {
      title: "Students Needing Help",
      value: stats.failingMarks,
      href: "/marks",
      color: "bg-red-500",
    },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-zinc-900 dark:text-white">
          Dashboard
        </h1>
        <p className="mt-2 text-zinc-600 dark:text-zinc-400">
          AI-powered automated remedial class timetable generator
        </p>
      </div>

      {loading ? (
        <div className="text-center py-12">
          <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-blue-500 border-r-transparent"></div>
          <p className="mt-4 text-zinc-600 dark:text-zinc-400">Loading statistics...</p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 mb-8">
            {cards.map((card) => (
              <Link
                key={card.title}
                href={card.href}
                className="bg-white dark:bg-zinc-900 overflow-hidden shadow rounded-lg hover:shadow-lg transition-shadow"
              >
                <div className="p-5">
                  <div className="flex items-center">
                    <div className="shrink-0">
                      <div className={`${card.color} rounded-md p-3`}>
                        <div className="h-6 w-6 text-white font-bold flex items-center justify-center">
                          {card.value}
                        </div>
                      </div>
                    </div>
                    <div className="ml-5 w-0 flex-1">
                      <dl>
                        <dt className="text-sm font-medium text-zinc-500 dark:text-zinc-400 truncate">
                          {card.title}
                        </dt>
                        <dd className="text-3xl font-semibold text-zinc-900 dark:text-white">
                          {card.value}
                        </dd>
                      </dl>
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-white dark:bg-zinc-900 shadow rounded-lg p-6">
              <h2 className="text-lg font-semibold text-zinc-900 dark:text-white mb-4">
                Quick Actions
              </h2>
              <div className="space-y-3">
                <Link
                  href="/remedial"
                  className="block w-full bg-blue-500 hover:bg-blue-600 text-white font-medium py-3 px-4 rounded-lg text-center transition-colors"
                >
                  Generate AI Remedial Timetable
                </Link>
                <Link
                  href="/students"
                  className="block w-full bg-zinc-200 hover:bg-zinc-300 dark:bg-zinc-700 dark:hover:bg-zinc-600 text-zinc-900 dark:text-white font-medium py-3 px-4 rounded-lg text-center transition-colors"
                >
                  Manage Students
                </Link>
                <Link
                  href="/teachers"
                  className="block w-full bg-zinc-200 hover:bg-zinc-300 dark:bg-zinc-700 dark:hover:bg-zinc-600 text-zinc-900 dark:text-white font-medium py-3 px-4 rounded-lg text-center transition-colors"
                >
                  Manage Teachers
                </Link>
              </div>
            </div>

            <div className="bg-white dark:bg-zinc-900 shadow rounded-lg p-6">
              <h2 className="text-lg font-semibold text-zinc-900 dark:text-white mb-4">
                System Overview
              </h2>
              <div className="space-y-3 text-sm text-zinc-600 dark:text-zinc-400">
                <div className="flex justify-between">
                  <span>Total Students:</span>
                  <span className="font-semibold text-zinc-900 dark:text-white">
                    {stats.students}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span>Total Teachers:</span>
                  <span className="font-semibold text-zinc-900 dark:text-white">
                    {stats.teachers}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span>Regular Timetable Slots:</span>
                  <span className="font-semibold text-zinc-900 dark:text-white">
                    {stats.regularClasses}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span>Remedial Timetable Slots:</span>
                  <span className="font-semibold text-zinc-900 dark:text-white">
                    {stats.remedialClasses}
                  </span>
                </div>
                <div className="flex justify-between pt-3 border-t border-zinc-200 dark:border-zinc-700">
                  <span>Students Needing Remedial:</span>
                  <span className="font-semibold text-red-600 dark:text-red-400">
                    {stats.failingMarks}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { timetablesAPI } from "@/lib/api";
import type { Timetable } from "@/types/api";

export default function RemedialPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [generatedTimetables, setGeneratedTimetables] = useState<Timetable[]>([]);

  async function handleGenerate() {
    if (!confirm("Generate AI-powered remedial timetable? This will analyze student marks and create optimal schedules avoiding conflicts with regular classes.")) {
      return;
    }

    try {
      setLoading(true);
      setError(null);
      setSuccess(false);

      const result = await timetablesAPI.generateRemedial();
      setGeneratedTimetables(result);
      setSuccess(true);

      setTimeout(() => {
        router.push("/timetables");
      }, 3000);
    } catch (err: any) {
      setError(err.message || "Failed to generate remedial timetable");
      console.error(err);
    } finally {
      setLoading(false);
    }
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

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-zinc-900 dark:text-white">
          AI Remedial Timetable Generator
        </h1>
        <p className="mt-2 text-zinc-600 dark:text-zinc-400">
          Generate intelligent remedial class schedules using Google Gemini AI
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white dark:bg-zinc-900 shadow rounded-lg p-6">
          <h2 className="text-xl font-semibold text-zinc-900 dark:text-white mb-4">
            How It Works
          </h2>
          <div className="space-y-4 text-zinc-600 dark:text-zinc-400">
            <div className="flex items-start">
              <div className="shrink-0 bg-blue-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold mr-3">
                1
              </div>
              <div>
                <h3 className="font-semibold text-zinc-900 dark:text-white mb-1">
                  Analyze Student Performance
                </h3>
                <p className="text-sm">
                  System identifies students with marks below 10/30 who need remedial classes.
                </p>
              </div>
            </div>

            <div className="flex items-start">
              <div className="shrink-0 bg-blue-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold mr-3">
                2
              </div>
              <div>
                <h3 className="font-semibold text-zinc-900 dark:text-white mb-1">
                  Match Students with Teachers
                </h3>
                <p className="text-sm">
                  Automatically pairs students with subject-specific teachers based on failing subjects.
                </p>
              </div>
            </div>

            <div className="flex items-start">
              <div className="shrink-0 bg-blue-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold mr-3">
                3
              </div>
              <div>
                <h3 className="font-semibold text-zinc-900 dark:text-white mb-1">
                  Check Existing Schedules
                </h3>
                <p className="text-sm">
                  Reviews all regular timetables to avoid conflicts with existing classes for both students and teachers.
                </p>
              </div>
            </div>

            <div className="flex items-start">
              <div className="shrink-0 bg-blue-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold mr-3">
                4
              </div>
              <div>
                <h3 className="font-semibold text-zinc-900 dark:text-white mb-1">
                  AI-Powered Scheduling
                </h3>
                <p className="text-sm">
                  Google Gemini 2.0 Flash analyzes all constraints and generates optimal time slots for remedial classes.
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-br from-blue-500 to-purple-600 shadow rounded-lg p-6 text-white">
          <h2 className="text-xl font-semibold mb-4">
            AI Features
          </h2>
          <div className="space-y-3 mb-6">
            <div className="flex items-center">
              <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              Subject-wise performance tracking
            </div>
            <div className="flex items-center">
              <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              Automatic conflict detection
            </div>
            <div className="flex items-center">
              <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              Individual student schedules
            </div>
            <div className="flex items-center">
              <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              Optimal time slot allocation
            </div>
            <div className="flex items-center">
              <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              Google Gemini 2.0 Flash powered
            </div>
          </div>

          <button
            onClick={handleGenerate}
            disabled={loading}
            className="w-full bg-white text-blue-600 font-bold py-3 px-6 rounded-lg hover:bg-zinc-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <div className="flex items-center justify-center">
                <div className="inline-block h-5 w-5 animate-spin rounded-full border-4 border-solid border-blue-600 border-r-transparent mr-2"></div>
                Generating with AI...
              </div>
            ) : (
              "Generate Remedial Timetable"
            )}
          </button>
        </div>
      </div>

      {error && (
        <div className="mt-6 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded">
          <strong className="font-bold">Error: </strong>
          <span>{error}</span>
        </div>
      )}

      {success && generatedTimetables.length > 0 && (
        <div className="mt-6 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-6">
          <div className="flex items-center mb-4">
            <svg className="w-6 h-6 text-green-600 dark:text-green-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            <h3 className="text-lg font-semibold text-green-900 dark:text-green-200">
              Successfully generated {generatedTimetables.length} remedial class(es)!
            </h3>
          </div>
          <p className="text-green-700 dark:text-green-400 mb-4">
            Redirecting to timetables page in 3 seconds...
          </p>
          <div className="bg-white dark:bg-zinc-900 rounded-lg overflow-hidden">
            <table className="min-w-full divide-y divide-zinc-200 dark:divide-zinc-700">
              <thead className="bg-zinc-50 dark:bg-zinc-800">
                <tr>
                  <th className="px-4 py-2 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400">Student ID</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400">Teacher ID</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400">Start Time</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400">End Time</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400">Location</th>
                </tr>
              </thead>
              <tbody className="bg-white dark:bg-zinc-900 divide-y divide-zinc-200 dark:divide-zinc-700">
                {generatedTimetables.map((tt, idx) => (
                  <tr key={idx}>
                    <td className="px-4 py-2 text-sm text-zinc-900 dark:text-white">{tt.student_id}</td>
                    <td className="px-4 py-2 text-sm text-zinc-900 dark:text-white">{tt.teacher_id}</td>
                    <td className="px-4 py-2 text-sm text-zinc-600 dark:text-zinc-400">{formatDateTime(tt.slot_start)}</td>
                    <td className="px-4 py-2 text-sm text-zinc-600 dark:text-zinc-400">{formatDateTime(tt.slot_end)}</td>
                    <td className="px-4 py-2 text-sm text-zinc-600 dark:text-zinc-400">{tt.location || "-"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      <div className="mt-8 bg-zinc-100 dark:bg-zinc-800 rounded-lg p-6">
        <h2 className="text-lg font-semibold text-zinc-900 dark:text-white mb-3">
          Prerequisites
        </h2>
        <ul className="space-y-2 text-sm text-zinc-600 dark:text-zinc-400">
          <li className="flex items-start">
            <span className="mr-2">•</span>
            <span>Students must be added to the system</span>
          </li>
          <li className="flex items-start">
            <span className="mr-2">•</span>
            <span>Teachers must be registered with their subjects</span>
          </li>
          <li className="flex items-start">
            <span className="mr-2">•</span>
            <span>Subject marks must be recorded (students with marks below 10/30 will get remedial classes)</span>
          </li>
          <li className="flex items-start">
            <span className="mr-2">•</span>
            <span>Regular timetable should be populated to avoid scheduling conflicts</span>
          </li>
        </ul>
      </div>
    </div>
  );
}

# Remedial Timetable Generator - Frontend

Modern Next.js frontend application for the AI-powered Automated Remedial Class Timetable Generator.

## Features

- **Dashboard** - Real-time statistics and quick actions
- **Student Management** - Add, view, and manage student records
- **Teacher Management** - Manage teachers and their subject assignments
- **Subject Marks Tracking** - Track student performance across subjects (out of 30 marks)
- **Timetable Viewer** - View and filter regular vs remedial class schedules
- **AI Remedial Generator** - Generate intelligent remedial schedules using Google Gemini AI

## Tech Stack

- **Next.js 16** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS 4** - Utility-first styling
- **React 19** - Latest React features

## Getting Started

### Prerequisites

- Node.js 18+ installed
- Backend server running on `http://localhost:8000`

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The application will be available at `http://localhost:3000`

### Environment Variables

The `.env.local` file is already configured:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router pages
│   │   ├── layout.tsx         # Root layout with navigation
│   │   ├── page.tsx           # Dashboard home page
│   │   ├── students/          # Student management
│   │   ├── teachers/          # Teacher management
│   │   ├── marks/             # Subject marks tracking
│   │   ├── timetables/        # Timetable viewer
│   │   └── remedial/          # AI remedial generator
│   ├── components/            # Reusable components
│   │   └── Navigation.tsx     # Main navigation bar
│   ├── lib/                   # Utility functions
│   │   └── api.ts            # API client functions
│   └── types/                 # TypeScript types
│       └── api.ts            # API type definitions
├── public/                    # Static assets
└── package.json
```

## Pages Overview

### Dashboard (/)

Displays real-time statistics:
- Total students and teachers
- Regular vs remedial class counts
- Students needing remedial help
- Quick action buttons

### Students (/students)

- View all students in a data table
- Add new students with form validation
- Delete student records
- Displays subject-wise marks

### Teachers (/teachers)

- View all teachers organized by subject
- Add new teachers with subject assignment
- Delete teacher records
- Subject dropdown with predefined options

### Subject Marks (/marks)

- Track student performance across subjects
- Marks are out of 30 total
- Color-coded status (red < 33%, yellow < 60%, green >= 60%)
- Highlights students needing remedial (< 10/30)
- Add, view, and delete mark entries

### Timetables (/timetables)

- View all timetable entries
- Filter by type: All / Regular / Remedial
- Displays student, teacher, subject, day, and time
- Shows location information
- Delete timetable entries

### AI Remedial Generator (/remedial)

Intelligent remedial schedule generation:

1. **Analyzes** students with marks < 10/30
2. **Matches** students with subject-specific teachers
3. **Checks** existing regular schedules for conflicts
4. **Generates** optimal time slots using Google Gemini AI
5. **Creates** remedial timetable entries

## Development

```bash
# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linting
npm run lint
```

## License

Part of the Automated Remedial Class Timetable Generator system.

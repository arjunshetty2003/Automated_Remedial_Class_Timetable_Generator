# Remedial Scheduler MCP Server

A Model Context Protocol (MCP) server that provides tools for managing the Remedial Class Scheduler database in Supabase.

## Features

- **Database Schema Management**: Create tables for students, teachers, and timetables
- **CRUD Operations**: List and create students, teachers, and timetable entries
- **SQL Execution**: Execute raw SQL queries for advanced operations
- **Supabase Integration**: Direct connection to your Supabase PostgreSQL database

## Setup

### 1. Install Dependencies

```bash
cd mcp-server
npm install
```

### 2. Configure Supabase Credentials

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Then get your Supabase credentials:

1. Go to your Supabase Dashboard
2. Navigate to **Project Settings** → **API**
3. Copy the following values to your `.env` file:
   - **Project URL** → `SUPABASE_URL`
   - **anon public key** → `SUPABASE_ANON_KEY`
   - **service_role key** (optional, for admin operations) → `SUPABASE_SERVICE_ROLE_KEY`

**Example `.env` file:**
```env
SUPABASE_URL=https://lxizswzgdzjzsonekqdx.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 3. Configure MCP in Claude Code

Update your `.mcp.json` file in the project root:

```json
{
  "mcpServers": {
    "remedial-scheduler": {
      "command": "node",
      "args": ["mcp-server/index.js"],
      "env": {
        "SUPABASE_URL": "https://lxizswzgdzjzsonekqdx.supabase.co",
        "SUPABASE_ANON_KEY": "your-anon-key-here"
      }
    }
  }
}
```

Or use the CLI:

```bash
claude mcp add --scope project remedial-scheduler node mcp-server/index.js
```

### 4. Restart Claude Code

After configuring the MCP server, restart Claude Code (or reload the window in VS Code) to load the new server.

## Available Tools

### `create_tables`
Creates the database schema (students, teachers, timetables tables)

### `list_students`
Lists all students from the database
- **Parameters**: `limit` (optional, default: 100)

### `create_student`
Creates a new student record
- **Parameters**: `name`, `email`, `marks`, `availability` (optional)

### `list_teachers`
Lists all teachers from the database
- **Parameters**: `limit` (optional, default: 100)

### `create_teacher`
Creates a new teacher record
- **Parameters**: `name`, `email`, `subject` (optional), `availability` (optional)

### `list_timetables`
Lists all timetable entries with student and teacher details
- **Parameters**: `limit` (optional, default: 100)

### `create_timetable`
Creates a new timetable entry
- **Parameters**: `student_id`, `teacher_id`, `slot_start`, `slot_end`, `location` (optional), `notes` (optional)

### `execute_sql`
Executes a raw SQL query (use with caution)
- **Parameters**: `query` (SQL string)

## Usage Example

Once configured, you can use these tools through Claude Code:

1. Create the database schema:
   ```
   "Use the create_tables tool to set up the database"
   ```

2. Add some students:
   ```
   "Use create_student to add a student named John with email john@example.com and marks 8"
   ```

3. List all students:
   ```
   "Use list_students to show me all students"
   ```

## Troubleshooting

- **Authentication errors**: Make sure your Supabase keys are correct and have the necessary permissions
- **Table already exists**: You can safely ignore these errors when running `create_tables` multiple times
- **Connection issues**: Verify your `SUPABASE_URL` is correct and your Supabase project is active

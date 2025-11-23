#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { createClient } from "@supabase/supabase-js";

// Load environment variables
const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_ANON_KEY;

if (!SUPABASE_URL || !SUPABASE_KEY) {
  console.error("Error: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY (or SUPABASE_ANON_KEY) must be set");
  process.exit(1);
}

// Initialize Supabase client
const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

// Create MCP server
const server = new Server(
  {
    name: "remedial-scheduler-mcp",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "create_tables",
        description: "Create the database schema (students, teachers, timetables tables)",
        inputSchema: {
          type: "object",
          properties: {},
        },
      },
      {
        name: "list_students",
        description: "List all students from the database",
        inputSchema: {
          type: "object",
          properties: {
            limit: {
              type: "number",
              description: "Maximum number of students to return (default: 100)",
            },
          },
        },
      },
      {
        name: "create_student",
        description: "Create a new student record",
        inputSchema: {
          type: "object",
          properties: {
            name: {
              type: "string",
              description: "Student name",
            },
            email: {
              type: "string",
              description: "Student email",
            },
            marks: {
              type: "number",
              description: "Student marks (0-100)",
            },
            availability: {
              type: "string",
              description: "Student availability (JSON string or text)",
            },
          },
          required: ["name", "email", "marks"],
        },
      },
      {
        name: "list_teachers",
        description: "List all teachers from the database",
        inputSchema: {
          type: "object",
          properties: {
            limit: {
              type: "number",
              description: "Maximum number of teachers to return (default: 100)",
            },
          },
        },
      },
      {
        name: "create_teacher",
        description: "Create a new teacher record",
        inputSchema: {
          type: "object",
          properties: {
            name: {
              type: "string",
              description: "Teacher name",
            },
            email: {
              type: "string",
              description: "Teacher email",
            },
            subject: {
              type: "string",
              description: "Subject taught by teacher",
            },
            availability: {
              type: "string",
              description: "Teacher availability (JSON string or text)",
            },
          },
          required: ["name", "email"],
        },
      },
      {
        name: "list_timetables",
        description: "List all timetable entries",
        inputSchema: {
          type: "object",
          properties: {
            limit: {
              type: "number",
              description: "Maximum number of entries to return (default: 100)",
            },
          },
        },
      },
      {
        name: "create_timetable",
        description: "Create a new timetable entry",
        inputSchema: {
          type: "object",
          properties: {
            student_id: {
              type: "number",
              description: "Student ID",
            },
            teacher_id: {
              type: "number",
              description: "Teacher ID",
            },
            slot_start: {
              type: "string",
              description: "Start time (ISO 8601 format)",
            },
            slot_end: {
              type: "string",
              description: "End time (ISO 8601 format)",
            },
            location: {
              type: "string",
              description: "Location of the class",
            },
            notes: {
              type: "string",
              description: "Additional notes",
            },
          },
          required: ["student_id", "teacher_id", "slot_start", "slot_end"],
        },
      },
      {
        name: "execute_sql",
        description: "Execute a raw SQL query (use with caution)",
        inputSchema: {
          type: "object",
          properties: {
            query: {
              type: "string",
              description: "SQL query to execute",
            },
          },
          required: ["query"],
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case "create_tables": {
        // Create students table
        await supabase.rpc("exec_sql", {
          sql: `
            CREATE TABLE IF NOT EXISTS students (
              id SERIAL PRIMARY KEY,
              name VARCHAR(255) NOT NULL,
              email VARCHAR(255) UNIQUE NOT NULL,
              marks INTEGER CHECK (marks >= 0 AND marks <= 100),
              availability TEXT,
              created_at TIMESTAMPTZ DEFAULT NOW()
            );
          `,
        });

        // Create teachers table
        await supabase.rpc("exec_sql", {
          sql: `
            CREATE TABLE IF NOT EXISTS teachers (
              id SERIAL PRIMARY KEY,
              name VARCHAR(255) NOT NULL,
              email VARCHAR(255) UNIQUE NOT NULL,
              subject VARCHAR(128),
              availability TEXT,
              created_at TIMESTAMPTZ DEFAULT NOW()
            );
          `,
        });

        // Create timetables table
        await supabase.rpc("exec_sql", {
          sql: `
            CREATE TABLE IF NOT EXISTS timetables (
              id SERIAL PRIMARY KEY,
              student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
              teacher_id INTEGER REFERENCES teachers(id) ON DELETE CASCADE,
              slot_start TIMESTAMPTZ NOT NULL,
              slot_end TIMESTAMPTZ NOT NULL,
              location VARCHAR(255),
              notes TEXT
            );
          `,
        });

        return {
          content: [
            {
              type: "text",
              text: "Database tables created successfully (students, teachers, timetables)",
            },
          ],
        };
      }

      case "list_students": {
        const limit = args.limit || 100;
        const { data, error } = await supabase
          .from("students")
          .select("*")
          .order("created_at", { ascending: false })
          .limit(limit);

        if (error) throw error;

        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(data, null, 2),
            },
          ],
        };
      }

      case "create_student": {
        const { data, error } = await supabase
          .from("students")
          .insert([
            {
              name: args.name,
              email: args.email,
              marks: args.marks,
              availability: args.availability || null,
            },
          ])
          .select();

        if (error) throw error;

        return {
          content: [
            {
              type: "text",
              text: `Student created successfully: ${JSON.stringify(data[0], null, 2)}`,
            },
          ],
        };
      }

      case "list_teachers": {
        const limit = args.limit || 100;
        const { data, error } = await supabase
          .from("teachers")
          .select("*")
          .order("created_at", { ascending: false })
          .limit(limit);

        if (error) throw error;

        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(data, null, 2),
            },
          ],
        };
      }

      case "create_teacher": {
        const { data, error } = await supabase
          .from("teachers")
          .insert([
            {
              name: args.name,
              email: args.email,
              subject: args.subject || null,
              availability: args.availability || null,
            },
          ])
          .select();

        if (error) throw error;

        return {
          content: [
            {
              type: "text",
              text: `Teacher created successfully: ${JSON.stringify(data[0], null, 2)}`,
            },
          ],
        };
      }

      case "list_timetables": {
        const limit = args.limit || 100;
        const { data, error } = await supabase
          .from("timetables")
          .select("*, students(name, email), teachers(name, email)")
          .order("slot_start", { ascending: true })
          .limit(limit);

        if (error) throw error;

        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(data, null, 2),
            },
          ],
        };
      }

      case "create_timetable": {
        const { data, error } = await supabase
          .from("timetables")
          .insert([
            {
              student_id: args.student_id,
              teacher_id: args.teacher_id,
              slot_start: args.slot_start,
              slot_end: args.slot_end,
              location: args.location || null,
              notes: args.notes || null,
            },
          ])
          .select();

        if (error) throw error;

        return {
          content: [
            {
              type: "text",
              text: `Timetable entry created successfully: ${JSON.stringify(data[0], null, 2)}`,
            },
          ],
        };
      }

      case "execute_sql": {
        const { data, error } = await supabase.rpc("exec_sql", {
          sql: args.query,
        });

        if (error) throw error;

        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(data, null, 2),
            },
          ],
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    return {
      content: [
        {
          type: "text",
          text: `Error: ${error.message}`,
        },
      ],
      isError: true,
    };
  }
});

// Start the server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Remedial Scheduler MCP Server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});

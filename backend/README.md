# Remedial Scheduler Backend

FastAPI service powering the AI-Based Remedial Class Scheduler. It exposes CRUD APIs for students, teachers, and timetables and will integrate with LangChain to orchestrate AI-assisted scheduling.

## Getting Started

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .[dev]
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000 with docs at http://localhost:8000/docs.

## Supabase Database Setup

This project uses Supabase as the PostgreSQL database host.

### 1. Create a Supabase Project

1. Go to [supabase.com](https://supabase.com) and create a new project
2. Wait for the database to be provisioned
3. Note down your database password (you'll need this for the connection string)

### 2. Get Your Database Connection String

1. In Supabase Dashboard, go to **Project Settings** → **Database**
2. Under **Connection String**, select **Session mode** (recommended for connection pooling)
3. Copy the connection string - it will look like:
   ```
   postgresql://postgres.[PROJECT_REF]:[YOUR-PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
   ```
4. For SQLAlchemy with asyncpg, modify it to:
   ```
   postgresql+asyncpg://postgres.[PROJECT_REF]:[YOUR-PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
   ```

### 3. Configure Environment Variables

Copy `.env.example` to `.env` and update with your Supabase credentials:

```bash
cp .env.example .env
```

| Variable | Description |
| --- | --- |
| `DATABASE_URL` | Supabase PostgreSQL connection string (Session mode recommended). Replace `[PROJECT_REF]`, `[PASSWORD]`, and `[REGION]` with your actual values. |
| `OPENAI_API_KEY` | OpenAI API key for schedule generation. |
| `GOOGLE_API_KEY` | Google Generative AI key (Gemini). |

**Example `.env` file:**
```env
DATABASE_URL=postgresql+asyncpg://postgres.xxxxx:your-password@aws-0-us-west-1.pooler.supabase.com:6543/postgres
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...
ENVIRONMENT=development
```

### 4. Run Database Migrations

After configuring your connection string, you'll need to create the database tables:

```bash
# Initialize Alembic (if not already done)
alembic init alembic

# Generate migration from models
alembic revision --autogenerate -m "Initial tables"

# Apply migrations to Supabase
alembic upgrade head
```

## Running Tests

```bash
pytest
```

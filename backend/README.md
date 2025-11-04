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

## Environment Variables

Copy `.env.example` to `.env` and adjust as needed.

```bash
cp .env.example .env
```

| Variable | Description |
| --- | --- |
| `DATABASE_URL` | SQLAlchemy async URL for the MySQL database. |
| `OPENAI_API_KEY` | OpenAI API key for schedule generation. |
| `GOOGLE_API_KEY` | Google Generative AI key (Gemini). |

## Running Tests

```bash
pytest
```

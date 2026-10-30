# JobTracker - AI-Powered Job Application Tracker + Resume Analyzer

Full-stack app to track job applications on a Kanban board, see funnel analytics,
and score your resume against any job description (TF-IDF + cosine similarity).

## Features
- JWT auth (register / login / refresh), roles: User and Admin
- Application tracking with Kanban drag-and-drop, search, filters
- **Status history**: every change is timestamped, which powers the funnel (Applied -> Interview -> Offer %)
- **Resume Analyzer**: upload PDF -> text extraction (pdfplumber) -> match score + matched / missing keywords
- Dashboard charts (applications per week, status split)
- Interview email reminders (Celery + Redis, runs hourly via Celery beat)
- Swagger API docs at `/api/docs/`, rate limiting on analyzer and auth endpoints
- Dockerized, pytest suite, GitHub Actions CI

## Tech Stack
Django 5 + Django REST Framework - React 18 + Vite + Tailwind + Recharts - PostgreSQL - Celery + Redis -
scikit-learn + pdfplumber - Docker - GitHub Actions

## Architecture
```
React (Vite)  --/api-->  Django REST  --> PostgreSQL
                              |
                              +--> Celery worker/beat --> Redis --> email reminders
```

## Run locally (without Docker)
**Backend**
```bash
cd backend
python -m venv venv && source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser                    # optional, for /admin
python manage.py runserver                          # http://localhost:8000
pytest                                              # run tests
```
Uses SQLite by default. Set `POSTGRES_DB`, `POSTGRES_HOST`, ... env vars to use PostgreSQL.

**Frontend**
```bash
cd frontend
npm install
npm run dev                                         # http://localhost:5173 (proxies /api to :8000)
```

**Celery (optional, needs Redis running)**
```bash
cd backend
celery -A config worker -l info
celery -A config beat -l info
```

## Run everything with Docker
```bash
cp .env.example .env
docker compose up --build
```
App: http://localhost:8080 - API docs: http://localhost:8000/api/docs/

## API overview
| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/auth/register/` | Create account |
| POST | `/api/auth/login/` | Get JWT access + refresh |
| POST | `/api/auth/refresh/` | New access token |
| GET/PATCH | `/api/auth/me/` | Current user |
| GET/POST | `/api/applications/?status=&search=&ordering=` | List / create |
| GET/PATCH/DELETE | `/api/applications/{id}/` | Detail |
| GET | `/api/applications/{id}/history/` | Status timeline |
| POST | `/api/resumes/analyze/` | PDF + job description -> score |
| GET | `/api/resumes/` | Past analyses |
| GET | `/api/analytics/summary/` | Dashboard numbers |
| GET | `/api/analytics/admin-stats/` | Platform stats (admin only) |

## How the match score works
`score = 40% cosine similarity (TF-IDF, unigrams+bigrams) + 60% keyword coverage`
where keyword coverage = share of the job description's top-20 TF-IDF keywords found in the resume.
See `backend/apps/resumes/matcher.py`.

## Deploy
- **Render / Railway**: backend as Web Service (root `backend`, start: `gunicorn config.wsgi`), add PostgreSQL + Redis,
  set env vars from `.env.example`; frontend as Static Site (`npm run build`, publish `dist`, set `VITE_API_URL` to the backend URL + `/api`).
- Set `CORS_ALLOWED_ORIGINS` to your frontend URL.

## Resume bullet (edit the numbers to your real ones)
> Built a full-stack job tracker using Django REST, React, PostgreSQL and Celery; implemented TF-IDF resume-to-JD matching
> with missing-keyword detection; added status-history funnel analytics, JWT auth, Dockerized deployment and GitHub Actions CI with pytest.

## Ideas to extend
Gmail/Outlook calendar sync - LinkedIn job-URL scraping - sentence-transformer embeddings for smarter matching - team/mentor sharing.

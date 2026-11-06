# RehabConnect — Digital Rehabilitation Platform (Portfolio Prototype)

**Full-stack digital health demo** aligned to a Lead Full Stack Software Engineer role focused on digital rehabilitation, remote monitoring, APIs and patient-centred design.

> **Safety and privacy:** Educational prototype with **fictional patients and synthetic check-ins only**. Not a medical device, not clinically validated, not intended for healthcare decisions. The clinician/patient view toggle is **not authentication or authorization**. Do not upload real patient information or deploy it publicly with sensitive data.

## Features
- **Clinician view:** browse fictional patients, review progress, add demonstration exercise plans.
- **Patient view:** view a plan, record exercise completion and pain scores (0–10).
- **Analytics:** check-in counts, completion rates, pain score trend chart.
- **API:** FastAPI REST endpoints with Pydantic validation and OpenAPI docs.
- **Persistence:** SQLAlchemy + local SQLite database, seeded fictional data.
- **Quality:** pytest API tests and GitHub Actions CI for backend and frontend.
- **Containerization:** Dockerfile for backend API.

## Stack
React 18, TypeScript, Vite, Recharts, FastAPI, SQLAlchemy, SQLite, pytest, Docker, GitHub Actions.

## Quick start — GitHub Codespaces / VS Code

Open **two terminals** at the repository root.

**Terminal 1: backend**

```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Terminal 2: frontend**

```bash
cd frontend
npm install
npm run dev
```

In Codespaces, open the **Ports** tab and forward **5173** (frontend) and **8000** (API). Open the forwarded URL for **5173** to use the app. Vite proxies `/api` requests to port 8000. If using Codespaces, port 8000 need not be public.

Local URLs: dashboard http://localhost:5173 and API docs http://localhost:8000/docs.

**Important:** The frontend is a development server; the Dockerfile packages only the backend API, not the full React application.

## Run tests

```bash
cd backend
python -m pytest -q
```

```bash
cd frontend
npm install
npm run build
```

## Example API endpoints
| Method | Path | Purpose |
|---|---|---|
| GET | `/api/health` | Health check |
| GET | `/api/patients` | Fictional patient list |
| GET | `/api/patients/{id}/plans` | Plans |
| POST | `/api/plans` | Add demo plan |
| GET | `/api/patients/{id}/checkins` | Check-ins |
| POST | `/api/checkins` | Add patient report |
| GET | `/api/patients/{id}/summary` | Summary and trend data |

## Portfolio relevance
Shows full-stack implementation, API design, database modeling, validation, automated tests, CI, dashboard design, documentation and healthcare-domain product thinking. See [architecture and production gaps](docs/ARCHITECTURE.md).

## Future engineering milestones
1. Authentication and server-side RBAC with patient/clinician access isolation.
2. PostgreSQL migration, schema migrations and secure audit events.
3. Accessibility testing, mobile usability and robust error handling.
4. FHIR integration sandbox and documented clinical interoperability requirements.
5. Cloud deployment with monitoring and threat modeling, after security hardening.

## License
MIT — see `LICENSE`.

# Architecture and decisions

```text
React + TypeScript + Recharts (localhost:5173)
             |
        Vite /api proxy
             |
FastAPI REST API (localhost:8000)
             |
        SQLAlchemy ORM
             |
       SQLite database
```

## Scope
- Fictional patients and exercise plans seeded on first startup.
- Two *interface modes* for demonstration, **not authenticated roles**.
- REST endpoints documented at `/docs`.
- Validation on incoming data using Pydantic.
- SQLite chosen for reproducible local demo; not a production healthcare datastore.

## Gaps before any real deployment
- Authenticated identity, role-based authorization and tenant isolation.
- Data protection impact assessment, lawful basis, consent where applicable, retention policy.
- Threat modeling, encryption, secrets, audit logging, access reviews, backups and recovery.
- Accessibility testing, usability testing with representative patients and clinicians.
- Clinical safety case and assessment of applicable UK regulatory requirements.
- Interoperability testing (e.g. FHIR) and secure integration with clinical systems.
- Monitoring, rate limits, deployment hardening and operational ownership.

## User stories
- As a clinician, I want to view fictional patient plans and reported outcomes.
- As a patient, I want to record exercise completion and a symptom score.
- As a reviewer, I want to inspect API docs and automated tests.

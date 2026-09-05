# Stage 01 — Foundation & Architecture

## 1. Status

**COMPLETED** (implementation + tests). Documentation learning system expanded afterward.

Verified: **11 pytest tests passed**; `/health` and `/ready` worked against local PostgreSQL. Docker Compose files exist; full Compose run requires Docker Desktop (not installed on the verification machine).

## 2. What are we building?

The **platform foundation** for Enterprise AI Modernization Architect:

- repository layout (modular monolith)
- typed configuration
- FastAPI application
- PostgreSQL connectivity
- health/readiness probes
- structured logging with request/trace IDs
- Docker packaging files
- initial documentation / interview study guides

We are **not** building inventory import, RAG, or agents in this stage.

## 3. Why are we building it?

Enterprise AI projects fail when people jump straight to “call an LLM.”  

Stage 1 proves we can run a real service: configure it safely, connect to a database, observe requests, and test it. Every later stage plugs into this foundation.

## 4. What problem does it solve?

Without Stage 1 you get:

- secrets hard-coded in notebooks
- no health signals for operators
- no shared project structure
- AI demos that cannot become systems

Stage 1 solves “we don’t have a credible engineering base yet.”

## 5. Concepts I need to understand first

### Modular monolith

**Simple:** One app, organized into folders/modules with clear jobs.  
**Why here:** Avoid microservice complexity before we need it.

### Liveness vs readiness

**Simple:** Liveness = process is alive. Readiness = dependencies are usable.  
**Why here:** `/health` vs `/ready`.

### Environment configuration

**Simple:** Settings come from environment variables, not hard-coded secrets.  
**Why here:** `AIMA_*` via Pydantic Settings.

### Structured logging

**Simple:** Logs as fields (JSON) you can search, not only English sentences.  
**Why here:** Correlate requests now; agent/tool metrics later.

### System of record

**Simple:** Official database of truth.  
**Why here:** PostgreSQL path is established before AI.

## 6. Technologies used

### Python 3.12+

- **What:** Language for backend/AI/data work.
- **Why:** Ecosystem fit for FastAPI, data, and AI libraries.
- **How:** Python package `aima` (technical identifier; branding is Enterprise AI Modernization Architect) via `pyproject.toml`.

### FastAPI

- **What:** API framework.
- **Why:** Typed contracts + OpenAPI.
- **How:** `app/main.py` factory; health routes.

### Pydantic Settings

- **What:** Typed config loader.
- **Why:** Validate config at startup.
- **How:** `app/config/settings.py` with `AIMA_` prefix.

### SQLAlchemy + psycopg

- **What:** Database toolkit + Postgres driver.
- **Why:** Same path we will use for domain models.
- **How:** Engine/session; `SELECT 1` readiness check.

### PostgreSQL (+ pgvector image in Compose)

- **What:** Relational database (image includes vector extension for later).
- **Why:** Future system of record + RAG without a second DB early.
- **How:** Compose service `db`; local Postgres also used in verification.

### Docker / Compose

- **What:** Container packaging and multi-service local runtime.
- **Why:** Reproducible local env without Azure spend.
- **How:** `docker/Dockerfile`, `docker/docker-compose.yml`.

### structlog

- **What:** Structured logging library.
- **Why:** Machine-readable logs with contextvars.
- **How:** `app/observability/logging.py` + middleware.

### pytest

- **What:** Test runner.
- **Why:** Lock foundation behavior.
- **How:** `tests/unit`, `tests/integration`.

## 7. Architecture

```
Client
  → RequestContextMiddleware (request_id, trace_id)
  → FastAPI routes
       /health  → process ok
       /ready   → PostgreSQL SELECT 1
  → Structured logs
```

ASCII broader context: [ARCHITECTURE.md](../ARCHITECTURE.md)

## 8. Implementation

Actually implemented:

1. Package layout with reserved modules (`agents`, `rag`, …) as empty packages.
2. Settings singleton `get_settings()` with storage/LLM abstraction fields.
3. `create_app()` with lifespan logging configuration.
4. Health + readiness routers mounted at `/` and `/api/v1`.
5. SQLAlchemy engine with `pool_pre_ping`.
6. Middleware binding correlation IDs onto responses.
7. Docker image CMD: `uvicorn app.main:app`.
8. Tests for settings, schemas, health API (including DB-down → 503).

**Not implemented:** domain tables, Alembic, auth, LLM calls, Streamlit, CI workflows.

## 9. Files

| File | Responsibility |
|------|----------------|
| `app/main.py` | App factory |
| `app/config/settings.py` | Env config |
| `app/api/routes/health.py` | `/health`, `/ready` |
| `app/schemas/health.py` | Response models |
| `app/database/session.py` | Engine/session/readiness helper |
| `app/database/base.py` | ORM Base |
| `app/observability/logging.py` | structlog setup |
| `app/observability/middleware.py` | Request context |
| `docker/Dockerfile` | API image |
| `docker/docker-compose.yml` | db + api |
| `pyproject.toml` | Dependencies & tool config |
| `.env.example` | Documented env vars |
| `tests/unit/test_*.py` | Unit tests |
| `tests/integration/test_health_api.py` | API tests |

## 10. Example

```bash
cp .env.example .env
pip install -e ".[dev]"
# with Postgres available:
uvicorn app.main:app --port 8001
curl -s localhost:8001/health
curl -s localhost:8001/ready
pytest
```

Example `/ready` success:

```json
{
  "status": "ready",
  "service": "aima-api",
  "environment": "local",
  "version": "0.1.0",
  "components": [{"name": "postgresql", "status": "up", "detail": null}]
}
```

## 11. Failure scenarios

- PostgreSQL stopped → readiness fails
- Port already in use → API won’t bind
- Invalid database URL → connection errors on `/ready`
- Missing Docker → cannot run Compose stack (API can still run against local Postgres)

## 12. How we handle failures

- `/ready` catches DB exceptions, logs warning, returns **503** + `not_ready`
- `/health` stays independent of DB
- Settings validation errors fail startup for bad types
- Tests mock DB up/down paths

## 13. Important engineering decisions

- Modular monolith over microservices
- Split health probes
- LLM stubbed (`stub`) until later stages
- Azure-first abstractions without requiring Azure
- Docs-as-interview-guide from day one

Details: [ARCHITECTURE_DECISIONS.md](../ARCHITECTURE_DECISIONS.md)

## 14. Alternatives

| Alternative | Why not now |
|-------------|-------------|
| Start with LangChain demo | Skips system of record |
| Microservices | Ops cost without need |
| Azure-only from day one | Cost + slower learning loop |
| Single `/health` including DB | Confuses liveness with dependency failure |

## 15. What I learned

- Foundations are part of AI engineering, not “boring prelude.”
- Correlation IDs are cheap and valuable.
- Honesty about scope (what’s implemented vs planned) is an interview strength.
- Docker files can be ready even when Docker isn’t installed — verify another way and document it.

## 16. Interview questions

**Beginner**

1. What does Stage 1 include?
2. What is the difference between `/health` and `/ready`?

**Intermediate**

3. Why PostgreSQL before RAG?
4. How are secrets handled?

**Advanced**

5. How would you evolve observability from Stage 1 to production AI telemetry?
6. What breaks if readiness and liveness are the same endpoint?

## 17. Interview answers

1. “Config, FastAPI, Postgres connectivity, health/ready, structured logs, Docker files, tests, docs.”
2. “Health = process up. Ready = Postgres answers.”
3. “Enterprise truth needs a system of record; the LLM must not be the database.”
4. “Environment variables via Pydantic Settings; `.env` gitignored.”
5. “Keep request/trace IDs; add agent_run_id, tool latency, tokens, retrieved evidence IDs; optionally OTel.”
6. “A DB blip looks like a dead process and causes unnecessary restarts.”

## 18. 30-second explanation

“Stage 1 is the production-shaped foundation for Enterprise AI Modernization Architect. I built a FastAPI service with typed config, PostgreSQL readiness checks, structured logs with request IDs, and Docker packaging. There’s no migration AI yet — on purpose — because evidence-grounded modernization needs a real platform first.”

## 19. 2-minute explanation

“Enterprise AI Modernization Architect is an evidence-grounded modernization advisor. Stage 1 establishes the modular monolith: Pydantic Settings with `AIMA_` variables, FastAPI with `/health` and `/ready`, SQLAlchemy connectivity to Postgres, and structlog middleware that stamps request and trace IDs. Compose defines API + Postgres with a pgvector image so later RAG can stay in one database. The LLM provider setting defaults to stub so we don’t pretend AI exists before inventory, graphs, and deterministic engines. Tests cover health behavior including database-down readiness failures. This is the base I’ll build Stages 2–20 on.”

## 20. Deep-dive questions

- Why `pool_pre_ping`?
- How do you prevent config drift between local and Azure?
- What’s your strategy for secret scanning in CI later?
- How would you add auth without rewriting the app factory?
- When would you split the monolith?

## 21. Production version

Before real enterprise deployment: authentication, TLS, managed secrets, hardened Postgres networking, non-demo credentials, CI gates, resource limits, and proper multi-environment config. Stage 1 intentionally uses local demo credentials (`aima`/`aima`) that must never ship to production.

## 22. Stage summary

- Status: **COMPLETED**
- FastAPI + settings + Postgres path + logs + Docker files + tests
- Health ≠ ready
- LLM stubbed; no fake AI claims
- Docs roadmap/learning system attached
- Compose verified as files; runtime verified via local Postgres when Docker missing
- Next: Stage 2 enterprise data model (only when explicitly started)

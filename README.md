# Enterprise AI Modernization Architect

Evidence-grounded platform that turns legacy portfolio data into modernization strategies, risk assessments, cost estimates, and phased cloud migration roadmaps — with human approval.

> **Honest scope:** This project uses **synthetic** enterprise data for a fictional company (Acme Financial Services). It is a decision-support portfolio project, **not** a production migration executor and **not** a claim of real Azure savings or customer deployments.

### Branding vs technical identifiers

**User-facing name:** Enterprise AI Modernization Architect (no acronym).

These **technical identifiers intentionally remain** so Stage 1–2 infrastructure does not break:

| Identifier | Why kept |
|------------|----------|
| Python package `aima` (`pyproject.toml`) | Import/install stability |
| Env prefix `AIMA_*` | Existing config contract |
| Docker names `aima-api`, `aima-db`, network/volume | Compose compatibility |
| Postgres user/db `aima` | Local DB already provisioned |
| Service name `aima-api` | Health payload / logs |

---

## Current status

| Stage | Name | Status | Label |
|-------|------|--------|-------|
| 1 | Foundation & Architecture | **Complete** | **IMPLEMENTED** |
| 2 | Enterprise Data Model | **Complete** | **IMPLEMENTED** |
| 3 | Synthetic Enterprise Environment | **Complete** | **SIMULATED** data authored |
| 4–20 | Pipeline → interview packaging | Not started | **PLANNED** |

| Category | Examples |
|----------|----------|
| **IMPLEMENTED** | FastAPI health/ready, Postgres schema, Alembic, logging, Docker files, Acme loaders, tests |
| **PLANNED** | Ingestion pipeline, graph, RAG, agents, Streamlit, CI, Azure deploy |
| **SIMULATED** | Acme Financial Services inventory, metrics, architecture docs |
| **ASSUMED** | Cost model rates (Stage 9+) |

---

## What this system does (target)

```
Enterprise Data → Discovery → Validation → Inventory → Dependency Graph
→ Knowledge Base / RAG → Deterministic Analysis (score/risk/cost/waves)
→ AI Architect Agent → Human Approval → Migration Roadmap
→ Evaluation / Audit / Observability
```

The LLM does **not** own truth. Structured data + deterministic engines do. The agent investigates and recommends; humans approve.

---

## Stages 1–3 — What works today

- Repository layout (modular monolith)
- Pydantic Settings (`AIMA_*` env vars)
- FastAPI app with `/health` and `/ready`
- PostgreSQL via Docker Compose (`pgvector/pgvector:pg16`)
- **Enterprise ORM models + Pydantic schemas + Alembic migration**
- **Synthetic Acme portfolio** under `data/raw/acme` + docs under `data/documents/acme`
- Intentional data-quality defect catalog (`DQ-001`…`DQ-010`)
- Structured JSON logging + request/trace IDs
- Abstraction hooks for storage and LLM (local vs Azure later)
- Unit + integration tests (**34** passing)

---

## Quick start

### Prerequisites

- Python 3.12+
- Docker Desktop (or Docker Engine + Compose)

### 1. Clone and configure

```bash
cp .env.example .env
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

### 2. Start infrastructure + API (recommended)

Requires [Docker Desktop](https://www.docker.com/products/docker-desktop/):

```bash
docker compose -f docker/docker-compose.yml up --build
```

- API: http://localhost:8000  
- Docs: http://localhost:8000/docs  
- Health: http://localhost:8000/health  
- Ready: http://localhost:8000/ready  

### 3. Run API locally (without Docker)

If PostgreSQL is already running locally, create DB/user `aima`/`aima`, copy `.env.example` → `.env`, then:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or DB in Docker + API on the host:

```bash
docker compose -f docker/docker-compose.yml up db -d
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Tests

```bash
pytest
```

Stage 1 verification on this machine: **11 tests passed**; `/health` and `/ready` confirmed against local PostgreSQL. Full Compose stack requires Docker Desktop (not installed here).

---

## Technology choices (why)

| Technology | Role | Why |
|------------|------|-----|
| Python 3.12+ | Language | AI/data ecosystem, typing maturity |
| FastAPI | API | Typed contracts, OpenAPI, async-ready |
| Pydantic v2 | Validation | Shared schemas for API + AI structured output |
| SQLAlchemy + PostgreSQL | Persistence | Enterprise-grade relational model; pgvector later for RAG |
| Docker Compose | Local runtime | Reproducible without Azure spend |
| structlog | Observability base | Machine-readable logs with correlation IDs |
| NetworkX / LangGraph / Streamlit | Later stages | Graph analysis, controlled agent, console UI |

---

## Demonstrated vs simulated vs assumed

| Category | Examples |
|----------|----------|
| **Demonstrated** | Config, health/ready, Docker Postgres, logging, tests (Stage 1) |
| **Simulated** | Enterprise inventory, migration outcomes (later stages) |
| **Assumed** | Cost model rates, Azure pricing bands (later; documented assumptions) |
| **Future production** | Azure OpenAI, Blob, Container Apps, CMDB/ServiceNow connectors |

---

## Documentation map (learning system)

| Doc | Purpose |
|-----|---------|
| [docs/MASTER_DOCUMENTATION.md](docs/MASTER_DOCUMENTATION.md) | **project textbook** — complete story + links to everything |
| [docs/PROJECT_ROADMAP.md](docs/PROJECT_ROADMAP.md) | **Master plan** Stages 1–20 + status table |
| [docs/PROJECT_GUIDE.md](docs/PROJECT_GUIDE.md) | Teach the whole project in simple language |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | System architecture (implemented vs planned) |
| [docs/DATA_ARCHITECTURE.md](docs/DATA_ARCHITECTURE.md) | Data & pipelines |
| [docs/AI_ARCHITECTURE.md](docs/AI_ARCHITECTURE.md) | LLM / RAG / agent design |
| [docs/ARCHITECTURE_DECISIONS.md](docs/ARCHITECTURE_DECISIONS.md) | Why we chose X (interview answers) |
| [docs/GLOSSARY.md](docs/GLOSSARY.md) | Terms in simple + interview form |
| [docs/INTERVIEW_PREP.md](docs/INTERVIEW_PREP.md) | Q&A bank by topic |
| [docs/FINAL_INTERVIEW_GUIDE.md](docs/FINAL_INTERVIEW_GUIDE.md) | ~30 minute spoken walkthrough |
| [docs/SECURITY.md](docs/SECURITY.md) | Security assumptions |
| [docs/EVALUATION.md](docs/EVALUATION.md) | Eval plan (measured only) |
| [docs/stages/](docs/stages/) | Per-stage learning units (`STAGE_01`…`STAGE_20`) |

---

## Project structure (Stage 1)

```
app/           # Application code (modular monolith)
data/          # Raw / processed / scenarios / documents
tests/         # unit / integration / e2e
docs/          # Architecture + interview study guide
docker/        # Dockerfile + Compose
scripts/       # Operational helpers
```

---

## License

MIT (portfolio / educational use). Synthetic data only.

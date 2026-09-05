# Enterprise AI Modernization Architect — Master Project Roadmap

**Project:** Enterprise AI Modernization Architect  
**Purpose:** Stage-by-stage plan from foundation → interview-ready portfolio system  
**Rule:** Status below reflects **what exists in the repository today**, not what we hope to build.

---

## Status legend

| Label | Meaning |
|-------|---------|
| **IMPLEMENTED** | Code/docs/tests exist and were verified for that stage |
| **PLANNED** | Designed and documented; not built yet |
| **SIMULATED** | Uses synthetic/demo data (not real customer systems) |
| **ASSUMED** | Model assumptions (e.g. cost rates) documented, not measured Azure bills |
| **FUTURE** | Production hardening beyond this portfolio project |

---

## Roadmap status table

| Stage | Name | Status | Main technologies | Key learning |
| ----- | ---------------- | -------- | --------------------------- | ----------------------- |
| 1 | Foundation | **COMPLETED** | FastAPI, PostgreSQL, Docker, structlog | Backend foundation |
| 2 | Data Model | **COMPLETED** | Pydantic, SQLAlchemy, Alembic | Enterprise schemas |
| 3 | Enterprise Data | PLANNED | CSV/JSON/YAML, pandas | Synthetic enterprise |
| 4 | Data Pipeline | PLANNED | Python, PostgreSQL | Data engineering |
| 5 | Dependency Graph | PLANNED | NetworkX | Graph analysis |
| 6 | RAG | PLANNED | Embeddings, pgvector | Grounded AI |
| 7 | Modernization | PLANNED | Python rules + scoring | Decision engine |
| 8 | Risk | PLANNED | Python | Risk analysis |
| 9 | Cost | PLANNED | Python | Cost modeling |
| 10 | Migration Waves | PLANNED | Graph + rules | Planning |
| 11 | AI Agent | PLANNED | LangGraph, LLM | Agentic AI |
| 12 | Governance | PLANNED | RBAC, policies | Responsible AI |
| 13 | API | PLANNED | FastAPI | Application engineering |
| 14 | Evaluation | PLANNED | pytest, golden scenarios | AI quality |
| 15 | Resilience | PLANNED | pytest, failure harness | Failure handling |
| 16 | Observability | PLANNED | OpenTelemetry concepts | Production AI |
| 17 | UI | PLANNED | Streamlit | Enterprise interface |
| 18 | CI/CD | PLANNED | GitHub Actions | Automation |
| 19 | Azure | PLANNED | Azure services (docs + optional deploy) | Cloud engineering |
| 20 | Packaging | PLANNED | Documentation | Interview readiness |

---

## Honest scope of Stage 1–2 (today)

**IMPLEMENTED**

- Repository layout (modular monolith packages)
- `AIMA_*` settings via Pydantic Settings
- FastAPI app factory + lifespan
- `/health` (liveness) and `/ready` (Postgres check)
- SQLAlchemy engine/session + enterprise ORM models
- Pydantic domain schemas (inventory + analysis)
- Alembic initial migration (`d5df7dcba761`)
- Structured logging + request/trace ID middleware
- Docker Compose + Dockerfile (files ready)
- Unit + integration tests (**20** passing when last run)
- Documentation system

**NOT IMPLEMENTED YET**

- Synthetic enterprise CSV inventory (Stage 3)
- Ingestion pipeline, NetworkX graph, RAG, agents
- Risk/cost/wave engines, Streamlit UI, CI workflows
- Azure deployment, evaluation golden set

**SIMULATED / ASSUMED / FUTURE**

- Nothing simulated in runtime yet (no fake metrics dashboards)
- Cost/Azure savings: **ASSUMED** later — never claim measured ROI until measured
- Real enterprise CMDB connectors: **FUTURE**

---

## Stage 1 — Foundation & Architecture

**Status: COMPLETED**

What was actually implemented:

- Python package `aima` with FastAPI entrypoint `app.main:app`
- Health/readiness probes
- PostgreSQL connectivity path (local Postgres verified; Compose files present)
- Config abstraction hooks for storage (`filesystem` / `azure_blob`) and LLM (`stub` / `openai_compatible` / `azure_openai`) — **stubs only**, no live LLM calls
- Observability foundation: JSON/console logs, `X-Request-ID`, `X-Trace-ID`

Deep dive: [stages/STAGE_01.md](stages/STAGE_01.md)

---

## Stage 2 — Enterprise Data Model

**Status: COMPLETED**

Pydantic schemas · SQLAlchemy models · Alembic · Applications · Services · Databases · APIs · Dependencies · Infrastructure · Documents · Evidence · Risks · Recommendations · Waves · Costs · Approvals · Audit

Learn: typed enterprise “source of truth” before any AI.

Deep dive: [stages/STAGE_02.md](stages/STAGE_02.md)

---

## Stage 3 — Synthetic Enterprise Environment

**Status: PLANNED** · Data will be **SIMULATED**

Realistic synthetic portfolio (e.g. Acme Financial Services): applications, services, databases, APIs, infrastructure, dependencies, operational metrics, intentional data-quality defects.

Deep dive: [stages/STAGE_03.md](stages/STAGE_03.md)

---

## Stage 4 — Data Engineering Pipeline

**Status: PLANNED**

```
raw → parse → validate → normalize → deduplicate → enrich → store + quality report
```

Deep dive: [stages/STAGE_04.md](stages/STAGE_04.md)

---

## Stage 5 — Dependency Graph

**Status: PLANNED**

NetworkX nodes/edges · centrality · critical dependencies · migration bottlenecks

Deep dive: [stages/STAGE_05.md](stages/STAGE_05.md)

---

## Stage 6 — Knowledge Base & RAG

**Status: PLANNED**

Document ingestion · chunking · metadata · embeddings · pgvector · retrieval · evidence IDs · retrieval evaluation

Deep dive: [stages/STAGE_06.md](stages/STAGE_06.md)

---

## Stage 7 — Modernization Analysis Engine

**Status: PLANNED**

Deterministic scoring + candidate strategies: Rehost · Replatform · Refactor · Repurchase · Retire · Retain · Replace (where appropriate)

Deep dive: [stages/STAGE_07.md](stages/STAGE_07.md)

---

## Stage 8 — Risk Engine

**Status: PLANNED**

Technical · operational · security · compliance · data · dependency · business · migration complexity

Deep dive: [stages/STAGE_08.md](stages/STAGE_08.md)

---

## Stage 9 — Cost Engine

**Status: PLANNED** · Estimates will be **ASSUMED** (transparent formulas, not Azure bills)

Compute · storage · database · networking · engineering · testing · migration · operational · low/base/high

Deep dive: [stages/STAGE_09.md](stages/STAGE_09.md)

---

## Stage 10 — Migration Wave Planner

**Status: PLANNED**

Dependency-aware sequencing · prerequisites · blockers · risk · criticality · readiness · waves

Deep dive: [stages/STAGE_10.md](stages/STAGE_10.md)

---

## Stage 11 — AI Architect Agent

**Status: PLANNED**

LangGraph · agent state · tools wrapping deterministic engines · RAG · evidence · structured output · recommendations

Deep dive: [stages/STAGE_11.md](stages/STAGE_11.md)

---

## Stage 12 — Policy & Human Approval

**Status: PLANNED**

Auth · RBAC · policy-as-code · approve/reject/modify · audit trail

Deep dive: [stages/STAGE_12.md](stages/STAGE_12.md)

---

## Stage 13 — FastAPI Production API

**Status: PLANNED** (Stage 1 only has health/ready)

Full inventory/analysis/plan/approval endpoints with Pydantic contracts

Deep dive: [stages/STAGE_13.md](stages/STAGE_13.md)

---

## Stage 14 — Evaluation Framework

**Status: PLANNED**

20+ golden scenarios · strategy accuracy · grounding · RAG quality · risk · cost · policy · hallucination · tool selection  
**Rule:** report only **measured** metrics after runs.

Deep dive: [stages/STAGE_14.md](stages/STAGE_14.md)

---

## Stage 15 — Failure & Resilience

**Status: PLANNED**

Bad input · missing data · conflicts · tool/DB/LLM failure · invalid output · policy violations

Deep dive: [stages/STAGE_15.md](stages/STAGE_15.md)

---

## Stage 16 — Observability

**Status: PLANNED** (Stage 1 has logging + request IDs only)

Agent runs · tool calls · latency · token usage · errors · audit events · OTel concepts

Deep dive: [stages/STAGE_16.md](stages/STAGE_16.md)

---

## Stage 17 — Enterprise Streamlit Console

**Status: PLANNED**

Executive · portfolio · graph · deep dive · AI Architect · roadmap · cost/risk · approval · audit

Deep dive: [stages/STAGE_17.md](stages/STAGE_17.md)

---

## Stage 18 — CI/CD

**Status: PLANNED** (`.github/workflows` reserved only)

Lint · test · typecheck · build · security checks

Deep dive: [stages/STAGE_18.md](stages/STAGE_18.md)

---

## Stage 19 — Azure Deployment Architecture

**Status: PLANNED** · Deploy only if explicitly needed

```
Local Docker → Azure Container Apps/App Service
            → Azure PostgreSQL (+ pgvector)
            → Azure Blob
            → Azure OpenAI
            → Monitoring
```

Deep dive: [stages/STAGE_19.md](stages/STAGE_19.md)

---

## Stage 20 — Portfolio & Interview Packaging

**Status: PLANNED** (guides started early; final packaging last)

Demo script · measured eval results · limitations · resume bullets · 30s / 2m / 5m / 30m walkthroughs

Deep dive: [stages/STAGE_20.md](stages/STAGE_20.md)

---

## How to use this roadmap while learning

1. Open [MASTER_DOCUMENTATION.md](MASTER_DOCUMENTATION.md) for the full textbook story.
2. Read [PROJECT_GUIDE.md](PROJECT_GUIDE.md) for a beginner-friendly teach-through.
3. Study the current completed stage file under `docs/stages/`.
4. Use [GLOSSARY.md](GLOSSARY.md) whenever a term is unfamiliar.
5. Practice aloud with [FINAL_INTERVIEW_GUIDE.md](FINAL_INTERVIEW_GUIDE.md).
6. After each implementation stage, update this table’s Status column **and** sync MASTER_DOCUMENTATION.md.

---

## Documentation map

| Document | Role |
|----------|------|
| [MASTER_DOCUMENTATION.md](MASTER_DOCUMENTATION.md) | **project textbook** — complete high-level story |
| [PROJECT_GUIDE.md](PROJECT_GUIDE.md) | Teach the whole project simply |
| [PROJECT_ROADMAP.md](PROJECT_ROADMAP.md) | Stage plan & status table |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System architecture |
| [DATA_ARCHITECTURE.md](DATA_ARCHITECTURE.md) | Data & pipelines |
| [AI_ARCHITECTURE.md](AI_ARCHITECTURE.md) | LLM / RAG / agent design |
| [ARCHITECTURE_DECISIONS.md](ARCHITECTURE_DECISIONS.md) | Why we chose X |
| [GLOSSARY.md](GLOSSARY.md) | Term → simple + interview answers |
| [INTERVIEW_PREP.md](INTERVIEW_PREP.md) | Q&A bank by topic |
| [FINAL_INTERVIEW_GUIDE.md](FINAL_INTERVIEW_GUIDE.md) | ~30 minute spoken walkthrough |
| [SECURITY.md](SECURITY.md) | Security assumptions |
| [EVALUATION.md](EVALUATION.md) | Eval plan (measured only) |
| `stages/STAGE_XX.md` | Per-stage learning unit |

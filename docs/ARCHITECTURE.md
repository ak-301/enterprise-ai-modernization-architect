# Architecture — Enterprise AI Modernization Architect

**Status honesty:** Architecture below describes the **target system**. Stages 1–5 are **IMPLEMENTED** (foundation, schema, synthetic Acme data, ingestion pipeline, NetworkX graph). Everything else is **PLANNED** unless marked otherwise.

Related: [PROJECT_ROADMAP.md](PROJECT_ROADMAP.md) · [AI_ARCHITECTURE.md](AI_ARCHITECTURE.md) · [DATA_ARCHITECTURE.md](DATA_ARCHITECTURE.md)

---

## High-level architecture

### Target end-state (PLANNED + Stage 1 foundation)

```
                    ┌─────────────────────────────┐
                    │  Streamlit Console (S17)    │
                    │  tables · graph · approvals │
                    └──────────────┬──────────────┘
                                   │ HTTP
                    ┌──────────────▼──────────────┐
                    │     FastAPI (modular monolith)│
                    │  auth · APIs · orchestration  │
                    └───┬──────────┬──────────┬───┘
                        │          │          │
            ┌───────────▼──┐  ┌────▼────┐  ┌──▼──────────┐
            │ Ingestion /  │  │ Engines │  │ AI Architect │
            │ Inventory    │  │ score   │  │ LangGraph    │
            │ Quality      │  │ risk    │  │ tools + RAG  │
            │ Graph build  │  │ cost    │  │ structured   │
            └──────┬───────┘  │ waves   │  └──────┬───────┘
                   │          └────┬────┘         │
                   │               │              │
            ┌──────▼───────────────▼──────────────▼──────┐
            │              PostgreSQL (+ pgvector)         │
            │  inventory · audit · chunks · embeddings     │
            └──────────────────────┬───────────────────────┘
                                   │
                    object storage abstraction
                    (filesystem local → Azure Blob later)
```

### Stage 1 implemented slice

```
┌──────────────┐     ┌──────────────────────────┐
│ curl / UI    │────▶│ FastAPI app.main:app     │
│ OpenAPI /docs│     │ middleware: request_id   │
└──────────────┘     │ GET /health  GET /ready  │
                     └────────────┬─────────────┘
                                  │ SQLAlchemy
                                  ▼
                     ┌──────────────────────────┐
                     │ PostgreSQL               │
                     │ (no domain tables yet)   │
                     └──────────────────────────┘
```

---

## Component responsibilities

| Component | Responsibility | Status |
|-----------|----------------|--------|
| `app/config` | Typed settings (`AIMA_*`) | **IMPLEMENTED** |
| `app/api` | HTTP routes | **IMPLEMENTED** (health only) |
| `app/database` | Engine, session, Base | **IMPLEMENTED** + Stage 2 ORM models |
| `app/observability` | Logging + request context | **IMPLEMENTED** (basic) |
| `app/schemas` | Pydantic DTOs | **IMPLEMENTED** (health + enterprise domain) |
| `app/models` | SQLAlchemy entities | **IMPLEMENTED** (Stage 2) |
| `app/ingestion` | Pipeline | **IMPLEMENTED** (Stage 4) |
| `app/graph` | NetworkX | **IMPLEMENTED** (Stage 5) |
| `app/rag` | Chunk/embed/retrieve | PLANNED |
| `app/analysis` / `risk` / `cost` / `migration` | Deterministic engines | PLANNED |
| `app/agents` / `tools` | LangGraph agent + tools | PLANNED |
| `app/auth` | RBAC | PLANNED |
| `app/evaluation` | Golden evals | PLANNED |
| Streamlit | Console | PLANNED |
| GitHub Actions | CI | PLANNED (folder reserved) |

---

## Data flow

**Data flow** = how information moves and is stored.

```
Files / CMDB exports (later)
   → parse/validate/normalize
   → rows in PostgreSQL (applications, deps, …)
   → graph derived from dependency rows
   → document chunks + embeddings
   → scores/risks/costs/waves persisted
   → recommendations + approvals + audit events
```

Stage 1 data flow is only: **settings + health payload + `SELECT 1`**.

---

## Control flow

**Control flow** = who decides the next step of work.

Target control flow for a recommendation request:

```
API request
  → policy/auth check
  → LangGraph workflow steps (gather → analyze → recommend)
  → each step calls tools (DB, graph, RAG, score, risk, cost)
  → validate structured output
  → if high impact: pending approval
  → human approve/reject/modify
  → audit event
```

Stage 1 control flow: **HTTP request → middleware → health/ready handler → response**.

---

## AI flow (where LLM is used vs not)

| Used (PLANNED) | Not used |
|----------------|----------|
| Summarize evidence | Dependency counts |
| Explain tradeoffs | Centrality math |
| Classify with citations | Cost arithmetic |
| Extract facts from docs | Schema validation |
| Draft recommendation text | Policy enforcement |

Full detail: [AI_ARCHITECTURE.md](AI_ARCHITECTURE.md)

---

## Local architecture

**IMPLEMENTED / ready:**

- Python 3.12+ package via `pyproject.toml`
- FastAPI + uvicorn
- PostgreSQL (Compose uses `pgvector/pgvector:pg16`)
- `.env` / `.env.example` with `AIMA_*`
- Dockerfile builds API image; Compose runs `db` + `api`

**Note:** On the machine used for Stage 1 verification, Docker Desktop was not installed; API + local Postgres were verified instead. Compose files are still the intended local path.

---

## Future Azure architecture (PLANNED — Stage 19)

```
Users → Streamlit / API clients
          ↓
Azure Container Apps or App Service (FastAPI)
          ↓
Azure Database for PostgreSQL Flexible Server (+ pgvector)
Azure Blob Storage (raw/docs)
Azure OpenAI (chat + embeddings)
Azure Monitor / Application Insights
```

Local and Azure share the same abstraction switches:

- `AIMA_STORAGE_BACKEND=filesystem|azure_blob`
- `AIMA_LLM_PROVIDER=stub|openai_compatible|azure_openai`

---

## Why modular monolith?

We chose **one deployable application** with clear packages instead of microservices.

**Simple reason:** The product is one decision pipeline. Splitting into many services early adds network failure modes without hiring a platform team.

**Tradeoff:** Scaling is coarser (scale the whole API). We can extract packages later if a real bottleneck appears.

See ADR in [ARCHITECTURE_DECISIONS.md](ARCHITECTURE_DECISIONS.md).

---

## Scalability (how it could evolve)

| Scale | Approach |
|-------|----------|
| Portfolio project (~tens of apps) | Single FastAPI + Postgres |
| Hundreds of apps | Same; index carefully; cache graph snapshots |
| Thousands+ / multi-tenant | Shard by tenant/project; async workers for ingestion/embeddings; maybe extract vector search if pgvector limits hit |
| Team growth | Keep module boundaries; extract only hot paths |

We have **not measured** throughput for 10,000 applications. Saying we “handle 10k apps” would be false.

---

## Failure modes (Stage 1 vs later)

| Failure | Stage 1 behavior | Later (PLANNED) |
|---------|------------------|-----------------|
| Process crash | `/health` fails | orchestrator restart |
| Postgres down | `/ready` → 503 | UI shows not ready; jobs pause |
| Bad LLM JSON | N/A yet | retry/repair then fail safe |
| Missing evidence | N/A yet | “Insufficient evidence” |

---

## APIs today vs planned

**IMPLEMENTED**

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/health` | Liveness |
| GET | `/ready` | Readiness |
| GET | `/api/v1/health` | Versioned liveness |
| GET | `/api/v1/ready` | Versioned readiness |
| GET | `/docs` | OpenAPI |

**PLANNED (examples):** projects, inventory import, applications, analysis, migration-plan, approve/reject, audit.

---

## Interview one-liners

- “Architecture is a modular monolith with Postgres as system of record and an AI layer that calls tools instead of owning truth.”
- “Stage 1 proves the platform can start, connect to Postgres, and emit correlated logs — the AI stages plug into that.”

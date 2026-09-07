# What is Enterprise AI Modernization Architect? — Project Learning Guide

This guide teaches the **Enterprise AI Modernization Architect** project from the beginning.

You can already write code. You do **not** need to already be an enterprise architect or AI platform engineer. Every hard idea is explained in plain language.

**Honesty rule:** Today **Stages 1–3** are implemented. Everything after Stage 3 is **PLANNED** unless a stage doc says COMPLETED. Stage 3 data is **SIMULATED**.

Master plan: [PROJECT_ROADMAP.md](PROJECT_ROADMAP.md)  
Complete textbook (start here if you forgot the project): [MASTER_DOCUMENTATION.md](MASTER_DOCUMENTATION.md)

---

# What is Enterprise AI Modernization Architect?

In simple words:

> Enterprise AI Modernization Architect is a software system that helps an enterprise architect understand a messy collection of old applications and recommend a safer, phased plan to modernize or migrate them to the cloud — with evidence, not guesses.

It is **not** a chatbot that invents a migration plan from a PDF.

It is closer to:

- a **data platform** (clean enterprise inventory),
- plus a **graph analyzer** (what depends on what),
- plus **scoring engines** (risk, cost, readiness),
- plus a **careful AI advisor** that cites evidence,
- plus **human approval** before anything high-impact is accepted.

The company data in this project is **synthetic** (made up for learning). We never pretend it is a real bank’s production systems.

---

# What real-world problem does it solve?

Large companies often have **dozens or hundreds of applications** built over many years:

- different languages (Java, .NET, Python, mainframe adapters),
- different databases,
- hidden dependencies,
- incomplete documentation,
- expensive operations,
- unclear migration order.

Before moving to Azure (or any cloud), architects need answers like:

- What exists?
- What talks to what?
- What breaks if we move this first?
- Should we **rehost**, **replatform**, **refactor**, **replace**, **retain**, or **retire**?
- What are the risks and rough costs?
- What should Phase 1 / Phase 2 / Phase 3 include?
- What **evidence** supports each recommendation?

Enterprise AI Modernization Architect is designed to help answer those questions as **decision support**.

---

# Why does this problem matter to companies?

Migrations fail when teams:

1. **Guess** architecture from tribal knowledge.
2. Move a central system too early and break dependents.
3. Trust an LLM that **hallucinates** (makes up) dependencies or document citations.
4. Skip risk, cost, and approval for production-critical apps.

Bad modernization burns money and trust. Good modernization is boring, evidence-based, and phased.

For you as a job candidate, this problem is valuable because it combines:

**data engineering + software engineering + AI engineering + governance**

That combination matches real AI Engineer / AI Consultant work more than a toy chatbot.

---

# The five layers of Enterprise AI Modernization Architect (memorize this)

Think of Enterprise AI Modernization Architect as a building with five floors:

| Layer | Name | Job |
|-------|------|-----|
| 1 | Data Engineering | Turn messy files into clean structured inventory |
| 2 | Enterprise Intelligence | Graph + deterministic scores (risk, cost, waves) |
| 3 | AI | RAG + LLM agent for reasoning and explanation |
| 4 | Governance | Policies, roles, human approval, audit |
| 5 | Engineering platform | API, DB, tests, observability, CI/CD, cloud design |

**Stage 1–2 build Layers 5 foundation + Layer 1 schema** (API process, config, DB connection, logs, typed enterprise tables). Ingestion/graph/AI remain planned.

---

# What happens when a user gives Enterprise AI Modernization Architect an enterprise portfolio?

*(Target end-state flow — mostly PLANNED today)*

```
Enterprise data (CSV, JSON, docs, metrics)
        ↓
Discovery & ingestion
        ↓
Validation / normalization / data quality
        ↓
Structured asset inventory  (PostgreSQL)
        ↓
Dependency graph           (NetworkX)
        ↓
Knowledge base / RAG       (docs → chunks → embeddings → pgvector)
        ↓
Deterministic analysis     (modernization score, strategy candidates)
        ↓
Risk engine + cost engine
        ↓
Migration wave planner
        ↓
AI Architect agent         (LangGraph + tools; cites evidence)
        ↓
Policy checks + human approval
        ↓
Final migration roadmap + audit trail
        ↓
Evaluation / observability
```

### Analogy

Imagine renovating a city block of old buildings.

1. **Inventory** = list every building and utility line (data engineering).
2. **Map** = which buildings share pipes and power (dependency graph).
3. **Rulebook** = city code and safety rules (RAG over policies).
4. **Calculators** = cost estimators and risk scores (deterministic engines).
5. **Advisor** = an experienced planner who reads the map and rulebook (AI agent).
6. **City council** = human architects who must approve (HITL).

You would never let a chatbot invent underground pipes. Same idea here.

---

# Component guide (WHAT / WHY / HOW / TECHNOLOGY)

## 1) Discovery & ingestion — Stage 3 data **IMPLEMENTED** (SIMULATED); pipeline **IMPLEMENTED** (Stage 4)

- **WHAT:** Bring raw enterprise files into the system.
- **WHY:** Real portfolios arrive messy; AI should not see unvalidated junk as truth.
- **HOW (today):** Synthetic Acme files under `data/raw/acme`. Pipeline in `app/ingestion` parses → quality-checks → normalizes → dedupes → enriches → stores clean rows; writes a quality report that detects DQ-001…DQ-010.
- **TECH:** CSV/JSON/YAML, pandas, SQLAlchemy, PostgreSQL. CLI: `python -m app.ingestion`.

## 2) Enterprise data model — **IMPLEMENTED** (Stage 2)

- **WHAT:** Typed definitions of Application, Service, Database, Dependency, etc.
- **WHY:** “LLM is not the database.” Truth needs schemas.
- **HOW:** Pydantic for API/AI contracts; SQLAlchemy for persistence; Alembic for migrations.
- **TECH:** Pydantic v2, SQLAlchemy 2, Alembic, PostgreSQL.

## 3) Dependency graph — **IMPLEMENTED** (Stage 5)

- **WHAT:** A network of nodes (apps/services/DBs) and edges (calls, reads, writes).
- **WHY:** Migration order is a graph problem, not a chat problem.
- **HOW:** Build graph in NetworkX from Stage 4 clean inventory; compute degree, betweenness, cycles, bottlenecks.
- **TECH:** NetworkX. CLI: `python -m app.graph` (+ later visualization in Streamlit).

## 4) Knowledge base / RAG — PLANNED (Stage 6)

- **WHAT:** Search enterprise documents by meaning, then cite chunk IDs.
- **WHY:** Policies and runbooks are unstructured text; we need grounded retrieval.
- **HOW:** Chunk docs → embeddings → store in pgvector → retrieve → attach evidence IDs.
- **TECH:** Embeddings API (OpenAI-compatible / Azure OpenAI later), PostgreSQL + pgvector.

**Embedding (simple):** turn text into a list of numbers that capture meaning so “similar” text is nearby in vector space.

## 5) Modernization / risk / cost / waves — PLANNED (Stages 7–10)

- **WHAT:** Calculators and planners with transparent formulas.
- **WHY:** Arithmetic and ranking should be deterministic and auditable.
- **HOW:** Weighted scores, likelihood×impact risk, low/base/high cost bands, wave rules.
- **TECH:** Pure Python modules under `app/analysis`, `app/risk`, `app/cost`, `app/migration`.

## 6) AI Architect agent — PLANNED (Stage 11)

- **WHAT:** A controlled workflow that investigates using tools and returns structured recommendations.
- **WHY:** Free-form chat is hard to test and easy to hallucinate.
- **HOW:** LangGraph state machine; tools call engines above; validate output schemas.
- **TECH:** LangGraph, OpenAI-compatible LLM, Pydantic structured outputs.

## 7) Governance — PLANNED (Stage 12)

- **WHAT:** Roles, policies, approve/reject/modify, audit log.
- **WHY:** High-impact enterprise decisions need humans and accountability.
- **HOW:** Policy-as-code (config/rules), not buried in prompts.
- **TECH:** Auth middleware, RBAC, audit tables.

## 8) API / UI / CI / Azure — PLANNED (Stages 13, 17–19)

- **API:** FastAPI structured JSON (Stage 1 already has health/ready).
- **UI:** Streamlit enterprise console (tables, graphs, evidence — not a giant chatbot).
- **CI:** GitHub Actions for lint/test.
- **Azure:** Documented target; local Docker for free development.

---

# What Stages 1–5 already give you (IMPLEMENTED)

You can already:

1. Configure the app with environment variables (`AIMA_*`).
2. Start a FastAPI process.
3. Ask “are you alive?” (`/health`) and “can you reach Postgres?” (`/ready`).
4. See structured logs with request IDs.
5. Persist typed enterprise entities (projects, applications, services, dependencies, …).
6. Version the schema with Alembic.
7. Load the **synthetic Acme** portfolio files and inspect intentional data-quality defects.
8. Run the **ingestion pipeline** (`python -m app.ingestion`) to quality-check, normalize, and store clean inventory.
9. Produce a quality report that detects planted defects DQ-001…DQ-010.
10. Build a **NetworkX dependency graph** (`python -m app.graph`) with hubs, cycles, and bottlenecks.
11. Run tests that lock foundation through graph analysis.

You **cannot** yet run RAG or migration recommendations. That is intentional.

Details: [stages/STAGE_01.md](stages/STAGE_01.md) · … · [stages/STAGE_05.md](stages/STAGE_05.md)

---

# Design principles (say these in interviews)

1. **Evidence over hallucination** — cite IDs or say “Insufficient evidence.”
2. **LLM is not the database** — structured models hold truth.
3. **Deterministic where appropriate** — math/graph/validation in code.
4. **Human-in-the-loop** — AI recommends; architects approve.
5. **Honest scope** — synthetic data, assumed cost model, decision support only.

---

# Local vs Azure (simple)

| Concern | Local (now / soon) | Azure (Stage 19, PLANNED) |
|---------|--------------------|---------------------------|
| App | Docker / uvicorn | Container Apps or App Service |
| Database | PostgreSQL (+ pgvector image) | Azure Database for PostgreSQL |
| Files | filesystem under `data/` | Azure Blob Storage |
| LLM | stub / OpenAI-compatible | Azure OpenAI |

Same application settings keys; different environment values.

---

# How to study this repo

1. Read this guide.
2. Read [MASTER_DOCUMENTATION.md](MASTER_DOCUMENTATION.md) and [PROJECT_ROADMAP.md](PROJECT_ROADMAP.md).
3. Practice Stages 1–5 aloud (30s + 2m in each stage doc).
4. Keep [GLOSSARY.md](GLOSSARY.md) open while reading architecture docs.
5. Rehearse the full story with [FINAL_INTERVIEW_GUIDE.md](FINAL_INTERVIEW_GUIDE.md) — mark sections as “planned” until built.

---

# What Stage 6 will teach you next

How to build a **knowledge base / RAG** layer: chunk Acme architecture docs, embed, store in pgvector, retrieve with citeable evidence IDs.

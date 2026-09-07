# Enterprise AI Modernization Architect

**Master Documentation (project textbook)**

This file is the single place to reopen months later and rebuild your mental model of the whole project. It tells the **complete story** at a high level and points you to deeper docs for each topic.

| Label | Meaning |
|-------|---------|
| **IMPLEMENTED** | Exists in code/tests today |
| **PLANNED** | Designed and documented; not built yet |
| **SIMULATED** | Synthetic / demo data (not a real customer) |
| **ASSUMED** | Explicit model assumptions (e.g. cost rates), not measured reality |
| **FUTURE** | Real enterprise production hardening beyond this portfolio |

**Current project status:** Stages 1–3 **COMPLETED**. Stages 4–20 **PLANNED**.

---

## How this document fits the documentation system

```
MASTER_DOCUMENTATION.md     ← you are here (complete story)
        ├── PROJECT_GUIDE.md              beginner teaching
        ├── PROJECT_ROADMAP.md            stage plan + status table
        ├── stages/STAGE_01…20.md         per-stage learning history
        ├── ARCHITECTURE.md               system architecture detail
        ├── DATA_ARCHITECTURE.md          data engineering detail
        ├── AI_ARCHITECTURE.md            LLM / RAG / agent detail
        ├── ARCHITECTURE_DECISIONS.md     ADRs / tradeoffs
        ├── GLOSSARY.md                   terminology
        ├── INTERVIEW_PREP.md             Q&A bank
        ├── FINAL_INTERVIEW_GUIDE.md      ~30 min spoken walkthrough
        ├── SECURITY.md                   security assumptions
        └── EVALUATION.md                 eval plan (measured only)
```

**Rule after every future stage:** update this master doc so it never claims planned work as shipped.

---

## 1. Executive Summary

Enterprise AI Modernization Architect is a portfolio-grade **enterprise AI engineering** project. It is designed as an internal-style platform that helps architects understand a legacy application portfolio and produce an **evidence-backed**, phased cloud modernization roadmap — with **human approval**.

It is **not** a flashy chatbot and **not** a production migration executor. The intended design combines data engineering, dependency graphs, deterministic risk/cost/wave engines, RAG with citeable evidence, and one controlled AI agent. **Today Stages 1–5 are implemented** (foundation, schema, synthetic Acme portfolio, quality-gated ingestion, and NetworkX dependency graph analysis). RAG and AI analysis stages remain planned.

---

## 2. What Problem Are We Solving?

Enterprises often have many old applications built over years: different languages, databases, batch jobs, APIs, and incomplete documentation.

Before migrating to the cloud (this project is **Azure-first**), architects need answers like:

- What applications and technologies exist?
- What depends on what?
- What should move first?
- Rehost, replatform, refactor, replace, retain, or retire?
- What are the risks and rough costs?
- What **evidence** supports each recommendation?

**Simple analogy:** You would not renovate a city block without a map of buildings and underground pipes. Enterprise AI Modernization Architect is meant to build that map, then advise — carefully.

---

## 3. Why Does This Problem Matter?

Migrations fail when teams:

1. Guess architecture from tribal knowledge  
2. Move a central system too early and break dependents  
3. Trust an LLM that **hallucinates** (invents) dependencies or citations  
4. Skip risk, cost, and approval for production-critical apps  

Bad modernization wastes money and trust. Good modernization is phased, boring, and evidence-based.

For interviews, this problem matters because it combines **data engineering + software engineering + AI + governance** — closer to real AI Engineer work than a toy chat wrapper.

---

## 4. What Does Enterprise AI Modernization Architect Do?

**Target end-state (mostly PLANNED):**

1. Ingest enterprise portfolio data and documents  
2. Validate and normalize into a structured inventory  
3. Build a dependency graph  
4. Retrieve policies/runbooks via RAG with evidence IDs  
5. Score modernization strategies deterministically  
6. Estimate risk and cost ranges  
7. Plan migration waves  
8. Use an AI Architect agent to synthesize recommendations with citations  
9. Require human approval for high-impact decisions  
10. Record audit trails and evaluate quality with golden scenarios  

**What it does today (IMPLEMENTED):** run as a FastAPI service, load typed config, prove liveness/readiness against PostgreSQL, persist a typed enterprise schema, author/load a **synthetic** Acme portfolio (CSV/JSON/YAML + policy docs with intentional DQ defects), **ingest** that portfolio through a quality-gated pipeline into Postgres, **analyze** dependency topology with NetworkX (hubs, cycles, bottlenecks), emit correlated structured logs, and support local packaging via Docker Compose files.

---

## 5. The Entire Project in One Diagram

```
Enterprise Data (**SIMULATED** — Acme raw files exist)
        ↓
Discovery & Ingestion                         [IMPLEMENTED Stage 4]
        ↓
Validation / Normalization / Quality          [IMPLEMENTED Stage 4]
        ↓
Structured Asset Inventory (PostgreSQL)       [schema Stage 2 + load Stage 4]
        ↓
Dependency Graph (NetworkX)                   [IMPLEMENTED Stage 5]
        ↓
Knowledge Base / RAG (chunks + pgvector)      [PLANNED Stage 6]
        ↓
Analysis Engines (score / 6Rs)                [PLANNED Stage 7]
        ↓
Risk Engine + Cost Engine                     [PLANNED Stages 8–9]
        ↓
Migration Wave Planner                        [PLANNED Stage 10]
        ↓
AI Architect Agent (LangGraph + tools)        [PLANNED Stage 11]
        ↓
Policy + Human Approval + Audit               [PLANNED Stage 12]
        ↓
Final Migration Roadmap
        ↓
Evaluation / Observability / API / UI         [PLANNED 13–17]
```

**Stage 1 slice that actually runs:**

```
Client → FastAPI (/health, /ready) → SQLAlchemy → PostgreSQL
              ↑
     request_id / trace_id logs
```

---

## 6. Explain the Project Like I'm New to It

Imagine a fictional bank (“Acme Financial Services”) with many applications. Someone dumps inventory CSVs, dependency lists, metrics, and PDF-like architecture docs into Enterprise AI Modernization Architect.

**Step A — Clean the data (IMPLEMENTED Stage 4):** Enterprise AI Modernization Architect does not trust raw files. It parses them, rejects invalid/orphan rows, fixes naming inconsistencies, detects duplicates, and stores clean records — with a quality report that proves planted defects were found.

**Step B — Build the map (PLANNED):** Applications, services, and databases become nodes. “Payment calls Identity” becomes an edge. Graph math finds central systems that are dangerous to move early.

**Step C — Read the rulebooks (PLANNED):** Migration and security policies are chunked, turned into embeddings (lists of numbers that capture meaning), stored in Postgres via pgvector, and retrieved with IDs you can cite.

**Step D — Run the calculators (PLANNED):** Code — not ChatGPT — computes modernization scores, risk scores, cost ranges, and candidate waves.

**Step E — Ask the AI Architect (PLANNED):** An agent calls tools to gather facts, then writes a structured recommendation with evidence. If evidence is missing, it should say so.

**Step F — Human gate (PLANNED):** An architect approves, rejects, or modifies. The system keeps an audit trail.

**Step G — Platform (IMPLEMENTED foundation):** All of this sits on FastAPI + Postgres + logging + Docker-shaped local runtime, so it is a real system, not a notebook demo.

---

## 7. End-to-End Example

**Synthetic scenario (SIMULATED design story — not a live run today):**

Acme has ~10+ apps including Customer Portal, Loan Processing, Payment Processing, Risk Analytics, Identity Platform, Document Management, Data Warehouse, and a Legacy Mainframe Adapter.

Suppose Payment Processing depends on Identity and a SQL Server database, and Identity is highly central in the graph.

**Intended flow once built:**

1. Inventory import validates Payment + Identity + DB rows  
2. Graph marks Identity as high centrality (bottleneck)  
3. RAG retrieves `DOC-MIG-008` cloud standards and `DOC-SEC-014` auth policy  
4. Deterministic engine suggests **Replatform** for Payment with confidence and alternatives  
5. Risk engine flags auth integration + DB compatibility  
6. Cost engine shows low/base/high with assumptions  
7. Wave planner puts Identity earlier than Payment if Payment depends on it  
8. Agent explains the recommendation citing `APP-…`, `DEP-…`, `DOC-…`  
9. Architect approval required because production/high criticality  
10. Roadmap records the decision  

**Today:** you can start the API and confirm Postgres readiness — you cannot yet run this full story in code.

---

## 8. Technology Stack

| Technology | What it is | Why we use it | Where / status |
|------------|------------|---------------|----------------|
| Python 3.12+ | Language | AI/data/API ecosystem | **IMPLEMENTED** whole project |
| FastAPI | Web API framework | Typed contracts, OpenAPI | **IMPLEMENTED** `app/main.py` |
| Pydantic v2 / Settings | Validation + config | Shared schemas; safe env config | **IMPLEMENTED** settings + health schemas |
| SQLAlchemy | DB toolkit/ORM | Path to enterprise models | **IMPLEMENTED** engine/session; models **PLANNED** |
| PostgreSQL | Relational DB | System of record | **IMPLEMENTED** connectivity |
| pgvector (image) | Vector search in Postgres | Early RAG without 2nd DB | Compose image ready; RAG **PLANNED** |
| structlog | Structured logging | Correlated machine logs | **IMPLEMENTED** |
| Docker / Compose | Containers | Reproducible local stack | **IMPLEMENTED** files |
| pytest | Tests | Lock behavior | **IMPLEMENTED** Stage 1 tests |
| Alembic | Schema migrations | Version DB changes | **PLANNED** Stage 2 |
| pandas | Tabular data | Synthetic datasets / pipeline | **PLANNED** Stages 3–4 |
| NetworkX | Graph analysis | Dependencies / centrality | **IMPLEMENTED** Stage 5 |
| Embeddings + LLM API | AI models | RAG + agent reasoning | Config stub **IMPLEMENTED**; calls **PLANNED** |
| LangGraph | Agent workflows | Explicit state machine | **PLANNED** Stage 11 |
| Streamlit | Internal UI | Enterprise console | **PLANNED** Stage 17 |
| GitHub Actions | CI | Lint/test gates | Folder reserved; workflows **PLANNED** Stage 18 |
| Azure services | Cloud | Target deployment story | **PLANNED** Stage 19 (not deployed) |

---

## 9. Architecture

### Frontend — PLANNED (Stage 17)

Streamlit enterprise console: portfolio tables, dependency explorer, deep dives, roadmap, cost/risk, approvals, audit. **Not a giant chatbot UI.** No UI implemented yet.

### API — PARTIAL

FastAPI modular monolith. **IMPLEMENTED:** `/health`, `/ready` (+ `/api/v1/...`). **PLANNED:** inventory, analysis, plans, approvals, audit endpoints (Stage 13).

### Business logic — PLANNED packages

Implemented: `ingestion` (Stage 4), `graph` (Stage 5). Reserved: `analysis`, `risk`, `cost`, `migration`, `agents`, `auth`, `evaluation`.

### Database — PARTIAL

PostgreSQL via SQLAlchemy. **IMPLEMENTED:** connection + empty `Base`. **PLANNED:** domain tables (Stage 2+).

### Data pipeline / graph / RAG / agent / evaluation — PLANNED

See sections 10–18 and 22.

### Observability — PARTIAL

**IMPLEMENTED:** structured logs, `request_id`, `trace_id`. **PLANNED:** agent/tool/token metrics (Stage 16).

Deeper detail: [ARCHITECTURE.md](ARCHITECTURE.md)

---

## 10. Data Engineering

**Pipeline (IMPLEMENTED Stage 4):**

```
Raw data → parse → validate → normalize → deduplicate → enrich → store
                 + data-quality report
```

**Why:** AI must not treat unvalidated junk as truth.

**Terms:**

- **Parse:** read CSV/JSON/YAML into records  
- **Validate:** reject illegal values / orphan references  
- **Normalize:** consistent names/IDs  
- **Enrich:** derived fields (`is_active`, asset types)  
- **Store:** PostgreSQL as system of record  

CLI: `python -m app.ingestion`

Deeper detail: [DATA_ARCHITECTURE.md](DATA_ARCHITECTURE.md) · [stages/STAGE_04.md](stages/STAGE_04.md)

---

## 11. Enterprise Data Model

**Status:** **IMPLEMENTED** (Stage 2 schema). **SIMULATED** inventory files authored (Stage 3). **LOADED** into Postgres via Stage 4 pipeline (clean rows only).

Major entities:

| Entity | Role |
|--------|------|
| Application | Business system (e.g. Payment Processing) |
| Service | Deployable unit inside an app |
| Database (`database_assets`) | Data store linked to apps |
| API | Interface contracts |
| Infrastructure | Hosts, queues, caches, etc. |
| Dependency | Directed relationship (asset type + external_id) |
| Document / Chunk | Unstructured knowledge + citeable pieces |
| Risk | Assessed risk records |
| Recommendation | Proposed strategy / action |
| Migration Wave | Phased grouping of work |
| Approval / AuditEvent | Governance trail |

**How they relate (simple):** Applications contain services; apps/services use databases and APIs; dependencies connect them via business IDs; documents provide evidence; analysis will write risks/recommendations/waves; humans approve and create audit events.

Deeper detail: [stages/STAGE_02.md](stages/STAGE_02.md) · [DATA_ARCHITECTURE.md](DATA_ARCHITECTURE.md)

---

## 12. Dependency Graph

**Status:** **IMPLEMENTED** (Stage 5)

- **Nodes:** applications, services, databases, APIs, infrastructure  
- **Edges:** calls, reads_from, writes_to, depends_on, publishes_to, consumes_from  
- **Analysis:** degree, betweenness centrality, depth, cycles, bottlenecks  
- **Use:** influence migration ordering  

**Analogy:** Like a subway map. Central transfer stations (high centrality) are painful to shut down early. Leaf stations are safer early moves.

CLI: `python -m app.graph`

Deeper detail: [stages/STAGE_05.md](stages/STAGE_05.md) · [GLOSSARY.md](GLOSSARY.md) (Dependency graph, Graph centrality)

---

## 13. Knowledge Base & RAG

**Status:** PLANNED (Stage 6)

**RAG** = Retrieval-Augmented Generation: search your documents first, then generate an answer using those pieces.

```
Documents → chunk (+ evidence ID) → embedding → pgvector
         → retrieve top-k → cite in answer → validate IDs
```

| Term | Simple meaning |
|------|----------------|
| Chunk | Small slice of a document |
| Embedding | Numbers representing meaning |
| Vector search | Find “nearby meaning” chunks |
| Evidence ID | Stable citation like `DOC-MIG-008` |
| Grounding | Tying claims to real sources |

**Why better than “just ask an LLM”:** the model’s memory is not your system of record; RAG + IDs make answers auditable and reduce hallucination.

Deeper detail: [AI_ARCHITECTURE.md](AI_ARCHITECTURE.md) · [stages/STAGE_06.md](stages/STAGE_06.md)

---

## 14. Modernization Analysis

**Status:** PLANNED (Stage 7)

Classic strategies (6 Rs) plus Replace when appropriate:

| Strategy | Simple idea |
|----------|-------------|
| Rehost | “Lift and shift” |
| Replatform | Small cloud-friendly changes |
| Refactor | Deeper code/architecture changes |
| Repurchase | Buy SaaS instead |
| Retire | Turn off |
| Retain | Keep as-is for now |
| Replace | Build/buy a successor |

**Deterministic analysis:** age, tech lifecycle, complexity, deps, cloud readiness, debt → transparent score and candidates.  
**AI reasoning (later):** explain tradeoffs and cite evidence — not invent math.

Deeper detail: [stages/STAGE_07.md](stages/STAGE_07.md)

---

## 15. Risk Engine

**Status:** PLANNED (Stage 8)

Categories (design): technical, operational, security, compliance, data, dependency, business, migration complexity.

Each risk ideally has: category, severity, likelihood, impact, score, evidence, mitigation.

**Typical formula shape:** `risk_score = likelihood × impact` (exact methodology documented when implemented).

Deeper detail: [stages/STAGE_08.md](stages/STAGE_08.md)

---

## 16. Cost Engine

**Status:** PLANNED (Stage 9) · estimates will be **ASSUMED**

Estimates cover compute, storage, database, networking, engineering, testing, migration, operational overhead — shown as **low / base / high** with visible assumptions.

**Why ranges:** we are not Azure Cost Management. Claiming exact bills would be dishonest. Interview strength = transparent model + humility.

Deeper detail: [stages/STAGE_09.md](stages/STAGE_09.md)

---

## 17. Migration Wave Planner

**Status:** PLANNED (Stage 10)

Sequencing considers dependencies, criticality, complexity, strategy, risk, effort, readiness.

Example wave story:

- Wave 0 — discovery/prep  
- Wave 1 — low-risk apps  
- Wave 2 — supporting services  
- Wave 3 — core apps  
- Wave 4 — high-risk legacy  

Each placement needs a rationale (not alphabetical sorting).

Deeper detail: [stages/STAGE_10.md](stages/STAGE_10.md)

---

## 18. AI Architect Agent

**Status:** PLANNED (Stage 11)

| Piece | Simple meaning |
|-------|----------------|
| Agent state | Working memory of the workflow |
| Tools | Functions the agent may call (inventory, graph, RAG, risk, cost, waves) |
| LangGraph | Explicit step-by-step AI workflow |
| Tool calling | Model requests a function instead of guessing |
| Structured output | Pydantic-validated recommendation JSON |
| Evidence retrieval | Pull citeable chunks/rows before claiming facts |

The agent **investigates and recommends**. It should **not** silently rewrite enterprise inventory.

Deeper detail: [AI_ARCHITECTURE.md](AI_ARCHITECTURE.md) · [stages/STAGE_11.md](stages/STAGE_11.md)

---

## 19. Why We Don't Let the LLM Do Everything

This is a core interview thesis of Enterprise AI Modernization Architect.

### LLM responsibilities (intended)

- Summarize and explain  
- Extract candidates from unstructured text (then validate)  
- Reason about tradeoffs with citations  
- Draft structured recommendations  

### Deterministic software responsibilities

- Schema validation and data quality  
- Dependency counts, centrality, cycles  
- Risk/cost arithmetic  
- Wave constraint checks  
- Policy enforcement  
- AuthZ gates and audit writes  

**One-liner:** *If a calculator or database query can do it, don’t ask a language model.*

Deeper detail: [AI_ARCHITECTURE.md](AI_ARCHITECTURE.md) (“Why don’t we just send everything to ChatGPT?”)

---

## 20. Security & Governance

| Concern | Status |
|---------|--------|
| Secrets via env / gitignore | **IMPLEMENTED** |
| Pydantic validation pattern | **IMPLEMENTED** (health) |
| Authentication | **PLANNED** Stage 12 |
| RBAC (viewer / analyst / architect) | **PLANNED** Stage 12 |
| Policy-as-code | **PLANNED** Stage 12 |
| Approval audit | **PLANNED** Stage 12 |
| Azure Key Vault / private net | **FUTURE** / Stage 19 sketch |

**Policy-as-code (simple):** business rules live in config/code you can test — not buried in prompts.

Deeper detail: [SECURITY.md](SECURITY.md) · [stages/STAGE_12.md](stages/STAGE_12.md)

---

## 21. Human-in-the-Loop

**PLANNED** Stage 12.

AI recommends. For high-impact items, a human architect **approves / rejects / modifies**.

Record: who, when, original recommendation, final decision, reason, evidence.

**Why:** enterprise migration advice can affect production systems and compliance. Autopilot is the wrong product shape.

---

## 22. Evaluation

**Status:** PLANNED Stage 14. **No accuracy numbers exist yet.**

Planned golden set: **20+** synthetic scenarios.

Planned metrics (report only after measured runs):

- strategy accuracy  
- retrieval quality  
- evidence grounding / hallucination rate  
- risk detection  
- cost band compliance  
- policy compliance  
- latency / token usage (when instrumented)  

Stage 1 contribution: pytest harness with **11 foundation tests** (platform quality, not AI quality).

Deeper detail: [EVALUATION.md](EVALUATION.md) · [stages/STAGE_14.md](stages/STAGE_14.md)

---

## 23. Failure Handling

| Failure | Intended / current behavior |
|---------|-----------------------------|
| Missing data | Prefer “Insufficient evidence” (**PLANNED**); don’t invent |
| Conflicting evidence | Surface conflict; don’t silently pick (**PLANNED**) |
| RAG fails / irrelevant | Low confidence / abstain (**PLANNED**) |
| Tool fails | Fail step safely; log error (**PLANNED**) |
| Database fails | **IMPLEMENTED:** `/ready` → 503 `not_ready`; `/health` can still be ok |
| LLM fails / invalid JSON | Retry/repair then fail safe (**PLANNED**) |
| Policy blocks | Recommendation pending or rejected with reason (**PLANNED**) |

Deeper detail: [stages/STAGE_15.md](stages/STAGE_15.md)

---

## 24. Observability

**IMPLEMENTED now:**

- Structured logs (structlog)  
- `request_id` / `trace_id` on requests  
- Response headers `X-Request-ID`, `X-Trace-ID`  

**PLANNED later:**

- agent run IDs, tool calls, model latency, token usage  
- retrieved evidence IDs, approval events  
- OpenTelemetry concepts (Stage 16)  

**Why it matters:** if you cannot reconstruct why a recommendation happened, you cannot defend it in an enterprise review.

---

## 25. API

**Framework:** FastAPI (**IMPLEMENTED** skeleton)

| Method | Path | Status |
|--------|------|--------|
| GET | `/health` | **IMPLEMENTED** liveness |
| GET | `/ready` | **IMPLEMENTED** readiness (Postgres) |
| GET | `/api/v1/health` | **IMPLEMENTED** |
| GET | `/api/v1/ready` | **IMPLEMENTED** |
| GET | `/docs` | **IMPLEMENTED** OpenAPI UI |
| — | projects, inventory, applications, analysis, plans, approve/reject, audit | **PLANNED** Stage 13 |

Principle: return structured JSON contracts — not raw LLM prose as the primary model.

---

## 26. Frontend

**Status:** PLANNED Stage 17 — **no Streamlit UI implemented**.

Planned pages: Executive Overview, Portfolio, Dependency Explorer, Deep Dive, AI Architect Q&A, Roadmap, Cost & Risk, Approval Center, Audit Trail.

UI principle: enterprise internal tool — tables, graphs, evidence, decisions.

---

## 27. Local Development

**IMPLEMENTED path:**

1. Python 3.12+ venv + `pip install -e ".[dev]"`  
2. Copy `.env.example` → `.env` (`AIMA_*` vars)  
3. PostgreSQL (Compose `db` service **or** local Postgres)  
4. `uvicorn app.main:app`  
5. `pytest`  

Docker Compose file: `docker/docker-compose.yml` (API + `pgvector/pgvector:pg16`).

See [README.md](../README.md) and [stages/STAGE_01.md](stages/STAGE_01.md).

---

## 28. Azure Architecture

### CURRENT LOCAL IMPLEMENTATION

- FastAPI process  
- PostgreSQL  
- Filesystem storage path setting  
- LLM provider default **`stub`** (no live calls)  
- Docker Compose files for local parity  

### PLANNED AZURE DEPLOYMENT (Stage 19 — not deployed)

```
Azure Container Apps / App Service  → FastAPI
Azure Database for PostgreSQL       → inventory + pgvector
Azure Blob Storage                  → raw/docs objects
Azure OpenAI                        → chat + embeddings
Azure Monitor / App Insights        → monitoring
```

Same app, different environment values via abstractions (`AIMA_STORAGE_BACKEND`, `AIMA_LLM_PROVIDER`).

**Do not say “deployed to Azure” until it actually happens.**

---

## 29. Testing

| Kind | Status | Purpose |
|------|--------|---------|
| Unit | **IMPLEMENTED** (settings, schemas, logging) | Fast logic checks |
| Integration | **IMPLEMENTED** (health API; DB mocked up/down) | HTTP + readiness behavior |
| End-to-end | **PLANNED** | Import → analyze → approve → roadmap |
| Evaluation | **PLANNED** | Golden AI scenarios |
| Failure / resilience | **PLANNED** Stage 15 | Adversarial cases |

---

## 30. CI/CD

**Status:** `.github/workflows/` reserved; workflows **PLANNED** Stage 18.

Intended gates: lint (ruff), tests (pytest), type checks (mypy), build, security checks.

Nothing to claim as green CI until workflows exist and run.

---

## 31. Stage-by-Stage Evolution

| Stage | Name | Status | What changes | Why necessary | New capability |
|-------|------|--------|--------------|---------------|----------------|
| 1 | Foundation | **COMPLETED** | API, config, DB path, logs, Docker files, docs | Need a real platform | Runnable service |
| 2 | Data model | **COMPLETED** | Schemas, ORM, Alembic | Shared vocabulary | Durable entities |
| 3 | Synthetic enterprise | **COMPLETED** | Realistic fake portfolio + DQ issues | Credible demo/eval data | SIMULATED world |
| 4 | Data pipeline | PLANNED | Validate/normalize/load + quality | Dirty data kills AI | Trusted inventory |
| 5 | Dependency graph | **COMPLETED** | NetworkX analytics | Order is topology | Bottleneck insight |
| 6 | RAG | PLANNED | Chunk/embed/retrieve/cite | Ground policy answers | Evidence retrieval |
| 7 | Modernization engine | PLANNED | Scores + 6R candidates | Transparent strategy | Deterministic candidates |
| 8 | Risk | PLANNED | Multi-dimension risk | Comparable risk language | Risk records |
| 9 | Cost | PLANNED | Low/base/high model | Honest ranges | Cost estimates |
| 10 | Waves | PLANNED | Dependency-aware sequencing | Safe phasing | Roadmap waves |
| 11 | AI Architect | PLANNED | LangGraph + tools | Multi-step investigation | Recommendations |
| 12 | Governance | PLANNED | RBAC, policy, HITL, audit | Accountability | Approvals |
| 13 | Production API | PLANNED | Full REST surface | Integrations/UI | Structured API |
| 14 | Evaluation | PLANNED | Golden metrics | Stop vibes-based claims | Measured quality |
| 15 | Resilience | PLANNED | Adversarial failures | Fail safe | Hardening |
| 16 | Observability | PLANNED | Agent/tool/token telemetry | Defend decisions | Deep ops insight |
| 17 | Streamlit UI | PLANNED | Enterprise console | Explainability UX | Human-facing tool |
| 18 | CI/CD | PLANNED | GitHub Actions | Regression control | Automated gates |
| 19 | Azure | PLANNED | Cloud mapping (± deploy) | Cloud narrative | Azure path |
| 20 | Packaging | PLANNED | Demo + interview kit | Tell the story | Portfolio polish |

Full detail: [PROJECT_ROADMAP.md](PROJECT_ROADMAP.md) · `docs/stages/STAGE_XX.md`

---

## 32. Important Architecture Decisions

Summaries (details + interview answers in [ARCHITECTURE_DECISIONS.md](ARCHITECTURE_DECISIONS.md)):

| Decision | One-line why |
|----------|--------------|
| Modular monolith | One pipeline; avoid early microservice tax |
| PostgreSQL + pgvector | System of record + early RAG in one DB |
| FastAPI + Pydantic | Typed contracts for API and future AI outputs |
| Docker local / Azure-first | Free dev; credible cloud story |
| NetworkX first | Enough graph power for portfolio scale |
| Deterministic engines | Auditable math; less hallucination |
| LangGraph (planned) | Controllable workflow, not unbounded agent |
| Human approval | Responsible AI for high impact |
| No K8s / Kafka / agent swarm by default | Complexity only when needed |

---

## 33. What We Deliberately Did NOT Build

| Excluded | Why |
|----------|-----|
| Kubernetes | No measured need; managed containers enough later |
| Microservices for show | Network complexity without product gain |
| Many cooperating agents | Coordination failure modes; one architect agent is enough |
| Automatic production migration execution | Product is decision support, not autopilot |
| “Upload → LLM → plan” | Shallow, ungrounded, un-auditable |
| Fake accuracy / ROI claims | Honesty is part of engineering maturity |

---

## 34. Current Limitations

**Current (honest):**

- Only Stage 1 platform foundation is implemented  
- No inventory, RAG, agent, UI, CI, or Azure deploy yet  
- Stage 1 API has no authentication (local assumption)  
- Docker Compose may require Docker Desktop; local Postgres is an alternate verify path  

**When later stages land, still expect:**

- **SIMULATED** enterprise data (not real customers)  
- **ASSUMED** cost model (not Azure invoices)  
- LLM limits: possible hallucination without strict grounding/eval  
- Not a guarantee of migration success  

---

## 35. Production Version

Before real enterprise use (**FUTURE**), you would typically add:

- Real CMDB / ServiceNow / cloud inventory connectors  
- Enterprise identity (SSO), secrets (Key Vault), private networking  
- Multi-tenancy and stronger authorization models  
- PII/redaction controls for prompts and logs  
- Production monitoring/alerting and on-call  
- Continuous model/prompt evaluation in CI  
- Scalability work only after measurement  
- Legal/compliance review of recommendations workflow  

**None of these are claimed as built.**

---

## 36. Complete Project Explanation

*(~5–10 minutes — align with [FINAL_INTERVIEW_GUIDE.md](FINAL_INTERVIEW_GUIDE.md))*

“I’m building Enterprise AI Modernization Architect, an evidence-grounded modernization advisor for enterprise portfolios. The problem is that companies can’t safely migrate what they don’t understand, and ChatGPT-style plans invent dependencies and skip auditability.

My architecture is a modular monolith on FastAPI with PostgreSQL as system of record. The design has five layers: data engineering, graph/deterministic intelligence, grounded AI, governance, and platform engineering.

Stages 1–5 are complete: typed configuration, health and readiness probes, structured logging with request IDs, Docker packaging, enterprise schema, synthetic Acme portfolio, ingestion with data-quality reporting into Postgres, and NetworkX dependency graph analysis (hubs, cycles, bottlenecks). Next I’m implementing RAG with evidence IDs, modernization/risk/cost/wave engines, then one LangGraph agent that calls those tools and returns structured recommendations for human approval.

I deliberately keep math and policy in code. The LLM explains and synthesizes with citations. I won’t claim accuracy or Azure savings until I measure them. The project is synthetic and decision-support only — and that honesty is part of the engineering story.”

---

## 37. The Project in 30 Seconds

“Enterprise AI Modernization Architect is an evidence-grounded enterprise modernization advisor. It turns portfolio data into inventory, graphs, and — by design — RAG plus deterministic risk/cost/wave engines, with a controlled AI agent and human approval. Stage 1, the FastAPI/Postgres foundation, is built; the AI and data layers are planned next.”

---

## 38. The Project in 2 Minutes

“Enterprises fail migrations when they lack a trustworthy map of applications and dependencies, or when they trust ungrounded LLM plans. The project's design separates truth from reasoning: Postgres holds inventory; NetworkX and Python engines compute graph metrics, risk, cost, and waves; RAG retrieves citeable policy chunks; a LangGraph agent uses tools and structured outputs; architects approve high-impact recommendations with an audit trail.

I’m Azure-first in design but develop on Docker without cloud spend. Stage 1 ships the platform skeleton — config, API health/ready, logging, Compose files, tests — so later stages plug into a real system instead of a notebook.”

---

## 39. The Project in 5 Minutes

Use sections 3–5 of [FINAL_INTERVIEW_GUIDE.md](FINAL_INTERVIEW_GUIDE.md) plus:

- modular monolith rationale  
- data vs control flow  
- where LLM is banned (math/policy)  
- Stage 1 proof points (`/health` vs `/ready`)  
- honest limitations (synthetic, assumed costs, not deployed)  

---

## 40. Interview Deep Dive Map

| Topic | Read next |
|-------|-----------|
| Whole story (beginner) | [PROJECT_GUIDE.md](PROJECT_GUIDE.md) |
| Stage plan / status | [PROJECT_ROADMAP.md](PROJECT_ROADMAP.md) |
| Stage 1 deep dive | [stages/STAGE_01.md](stages/STAGE_01.md) |
| System architecture | [ARCHITECTURE.md](ARCHITECTURE.md) |
| Data engineering | [DATA_ARCHITECTURE.md](DATA_ARCHITECTURE.md) · STAGE_04 |
| Data model | STAGE_02 |
| Graphs | STAGE_05 · GLOSSARY |
| RAG | [AI_ARCHITECTURE.md](AI_ARCHITECTURE.md) · STAGE_06 · GLOSSARY |
| Modernization / risk / cost / waves | STAGE_07–10 |
| Agent / LangGraph | AI_ARCHITECTURE · STAGE_11 |
| Security / HITL | [SECURITY.md](SECURITY.md) · STAGE_12 |
| Evaluation | [EVALUATION.md](EVALUATION.md) · STAGE_14 |
| Decisions / tradeoffs | [ARCHITECTURE_DECISIONS.md](ARCHITECTURE_DECISIONS.md) |
| Terms | [GLOSSARY.md](GLOSSARY.md) |
| Q&A bank | [INTERVIEW_PREP.md](INTERVIEW_PREP.md) |
| 30-minute talk | [FINAL_INTERVIEW_GUIDE.md](FINAL_INTERVIEW_GUIDE.md) |

---

## Recommended reading order (if you forgot everything)

1. This file — **MASTER_DOCUMENTATION.md** (orient)  
2. [PROJECT_GUIDE.md](PROJECT_GUIDE.md) (learn simply)  
3. [stages/STAGE_01.md](stages/STAGE_01.md) (what actually exists)  
4. [GLOSSARY.md](GLOSSARY.md) (keep open)  
5. [ARCHITECTURE.md](ARCHITECTURE.md) + [AI_ARCHITECTURE.md](AI_ARCHITECTURE.md)  
6. [FINAL_INTERVIEW_GUIDE.md](FINAL_INTERVIEW_GUIDE.md) (practice aloud)  
7. [PROJECT_ROADMAP.md](PROJECT_ROADMAP.md) (what comes next)  

---

*Last synced with repository state: Stages 1–3 COMPLETED · Stages 4–20 PLANNED · 34 tests passing · Acme data SIMULATED.*

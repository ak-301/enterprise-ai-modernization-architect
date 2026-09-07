# Interview Prep — Enterprise AI Modernization Architect

Practice out loud. Prefer honesty: **Stage 1 is implemented**; most AI/data features are **planned**.

For the continuous talk track, use [FINAL_INTERVIEW_GUIDE.md](FINAL_INTERVIEW_GUIDE.md).

---

## Project overview

### Tell me about your project.

**Short:** “Enterprise AI Modernization Architect is an evidence-grounded enterprise modernization advisor. It turns portfolio data into structured inventory, graphs, scores, and — eventually — a tool-using AI architect with human approval. Stage 1 is the FastAPI/Postgres foundation.”

**Strong:** “I’m building a decision-support system for legacy modernization. The design rejects ‘upload files → ChatGPT → plan.’ Truth lives in Postgres; NetworkX computes dependency topology; Python engines will handle risk, cost, and waves; an LLM agent will retrieve cited evidence and recommend; humans approve. Today Stages 1–5 are complete through quality-gated ingestion and graph analysis.”

**Deep dive:** What’s implemented vs planned? Why Azure-first? Why synthetic data?

---

## Architecture

### Why a modular monolith?

**Short:** “One deployable with clear packages — enough structure without microservice tax.”

**Strong:** “Modernization is one pipeline. Early microservices create distributed transactions and duplicated schemas. Packages like ingestion, graph, agents preserve future extraction.”

**Deep dive:** When would you split? How do you enforce module boundaries?

### Why not Kubernetes?

**Short:** “No measured need; Docker Compose locally and managed containers on Azure are enough.”

**Strong:** “K8s adds operational load. For a portfolio modular monolith, Container Apps/App Service is the planned cloud path.”

**Deep dive:** What signals would justify K8s?

---

## Python

### Why Python 3.12+?

**Short:** “Best ecosystem fit for API, data, and AI libraries.”

**Strong:** “Typing + FastAPI/Pydantic + data/AI stack. We target 3.12+ in packaging.”

**Deep dive:** Typing strategy? mypy strictness tradeoffs?

---

## FastAPI

### Why FastAPI?

**Short:** “Typed APIs and automatic OpenAPI.”

**Strong:** “Pydantic validation on the edge matches how we’ll validate structured LLM outputs later.”

**Deep dive:** Sync vs async? dependency injection patterns?

### Health vs ready?

**Short:** “Health = alive; ready = Postgres up.”

**Strong:** “Orchestrators restart on liveness failure and stop routing on readiness failure. Coupling them causes flapping.”

**Deep dive:** What other dependencies join readiness later?

---

## PostgreSQL

### Why Postgres as system of record?

**Short:** “Enterprise truth needs durable relational storage — not prompts.”

**Strong:** “Inventory, approvals, audit need ACID. pgvector lets early RAG live in the same database.”

**Deep dive:** When split vector search? Multi-tenant schema strategies?

---

## Data engineering

### Why ingestion before AI?

**Short:** “Dirty data in → confident nonsense out.”

**Strong:** “Parse/validate/normalize/dedupe/enrich with quality metrics so recommendations cite real assets.”

**Deep dive:** How do you version raw vs curated datasets?

---

## Data quality

### What quality dimensions will you track?

**Short:** “Completeness, uniqueness, validity, consistency, referential integrity.”

**Strong:** “Stage 3 planted intentional defects in the synthetic Acme inventory; Stage 4 detects and reports them (DQ-001…DQ-010) instead of hiding them.”

**Deep dive:** How do quality gates block migration waves?

---

## Graphs

### Why NetworkX?

**Short:** “In-process graph analysis is enough for this portfolio scale.”

**Strong:** “We need degree/centrality/cycles for sequencing. Asking an LLM to ‘understand dependencies’ isn’t auditable.”

**Deep dive:** When Neo4j? How handle cycles?

---

## RAG

### Explain RAG simply.

**Short:** “Retrieve relevant doc chunks, then generate with citations.”

**Strong:** “Chunk with evidence IDs, embed into pgvector, retrieve top-k, require citations; say insufficient evidence if missing.”

**Deep dive:** Chunk size tradeoffs? Hybrid search? Stale docs?

---

## LLMs

### Where should the LLM not be used?

**Short:** “Arithmetic, graph metrics, validation, policy enforcement.”

**Strong:** “If a unit test can assert it, code should own it. The model synthesizes and explains.”

**Deep dive:** Model routing? Temperature? Cost controls?

### Why not dump everything into ChatGPT?

**Short:** “No system of record, weak audit, hallucinated deps, uncontrolled cost.”

**Strong:** See [AI_ARCHITECTURE.md](AI_ARCHITECTURE.md) section — multi-system decision needs tools, schemas, HITL, evals.

**Deep dive:** Would a 1M-token context fix it? (No — still need integrity, graphs, approvals.)

---

## Agents

### Why use an agent?

**Short:** “Multi-step investigation with tools.”

**Strong:** “Get app → deps → policies → risk/cost → structured recommendation. One prompt is too shallow.”

**Deep dive:** Memory? Max tool iterations? Stopping conditions?

### When not to use an agent?

**Short:** “Pure ETL, scoring, or validation — just run code.”

**Strong:** “Agents add latency/cost/failure modes. Deterministic paths first.”

**Deep dive:** Agent vs workflow engine without LLM?

---

## LangGraph

### Why LangGraph?

**Short:** “Explicit state machine for controllable AI workflows.”

**Strong:** “Easier to test and explain than an unbounded ReAct loop.”

**Deep dive:** How do you represent human-approval as a graph node?

---

## Prompt engineering

### What’s your prompt philosophy?

**Short:** “Minimal prompts; maximum tools and schemas.”

**Strong:** “Prompts guide reasoning; they must not hide policy or invent evidence rules already enforced in code.”

**Deep dive:** Prompt versioning? Eval-driven prompt changes?

---

## Structured outputs

### How do you trust model JSON?

**Short:** “Validate with Pydantic; retry/repair; then fail safe.”

**Strong:** “Invalid strategy enums or unknown evidence IDs are errors, not silently accepted.”

**Deep dive:** Partial recovery vs hard fail?

---

## AI evaluation

### How will you know it works?

**Short:** “Golden scenarios and measured metrics — no vibes.”

**Strong:** “20+ cases for strategy, grounding, retrieval, risk, cost, policy, hallucination. Report only after runs.”

**Deep dive:** Inter-annotator agreement on golden labels? Regression budgets?

---

## Security

### What’s secured in Stage 1?

**Short:** “Secrets via env; gitignore; local-only assumption — no auth yet.”

**Strong:** “Demo DB credentials are not production. Stage 12 adds authn/z; Stage 18 adds secret scanning.”

**Deep dive:** PII in prompts? Tenant isolation?

---

## RBAC

### Planned roles?

**Short:** “Viewer, analyst, architect.”

**Strong:** “Only architects approve high-impact recommendations; policies encode that in code.”

**Deep dive:** Attribute-based access later?

---

## Human-in-the-loop

### Why HITL?

**Short:** “Migration advice can be high impact; humans own the decision.”

**Strong:** “Approve/reject/modify with audit: who, when, original vs final, reason, evidence.”

**Deep dive:** Which decisions auto-approve at low risk?

---

## Governance

### What is policy-as-code here?

**Short:** “Rules in config/code, not buried in prompts.”

**Strong:** “Example: unresolved critical deps block wave entry; sensitive DBs need security review.”

**Deep dive:** How do you unit-test policies?

---

## Cost

### How will you talk about cost estimates?

**Short:** “Transparent assumptions and ranges — not Azure invoices.”

**Strong:** “Low/base/high with visible drivers; never claim measured savings unless measured.”

**Deep dive:** Sensitivity analysis? FinOps integration FUTURE?

---

## Performance

### How do you control latency/cost of AI?

**Short:** “Fewer better chunks, deterministic shortcuts, stub/dev modes, right-sized models.”

**Strong:** “Don’t call the model for calculator work; cache embeddings; log tokens when Stage 16 lands.”

**Deep dive:** SLOs for analysis runs?

---

## Observability

### What exists today?

**Short:** “Structured logs with request/trace IDs.”

**Strong:** “Middleware binds contextvars and response headers. Later: agent/tool/token/evidence telemetry.”

**Deep dive:** Trace sampling? PII redaction in logs?

---

## Docker

### Why Docker?

**Short:** “Reproducible local API + Postgres.”

**Strong:** “Compose mirrors cloud shapes; Azure later swaps managed services via config.”

**Deep dive:** Multi-stage builds? Image scanning?

---

## CI/CD

### What’s planned?

**Short:** “GitHub Actions for lint, tests, types, build, security checks.”

**Strong:** “AI systems regress silently; CI is mandatory before trusting eval claims.”

**Deep dive:** Eval jobs on GPUs/paid APIs — how budgeted?

---

## Azure

### Why Azure-first?

**Short:** “Target cloud for modernization story; develop free locally.”

**Strong:** “Azure OpenAI, Postgres, Blob, Container Apps/App Service, Monitor — documented mapping in Stage 19.”

**Deep dive:** Private networking? Managed identity? Key Vault?

---

## System design

### Walk me through a recommendation request (target design).

**Short:** “Auth → gather inventory/graph/docs → score/risk/cost → agent synthesizes → policy → human approval → audit.”

**Strong:** Expand using [ARCHITECTURE.md](ARCHITECTURE.md) data vs control flow.

**Deep dive:** Idempotency? Partial failure mid-workflow?

---

## Scalability

### Will this handle 10,000 apps?

**Short:** “Not measured. Design can evolve; I won’t claim it.”

**Strong:** “Start clear algorithms; add caching/async workers/tenant isolation when metrics demand.”

**Deep dive:** Hot partitions? Graph snapshot materialization?

---

## Failure handling

### Give a Stage 1 failure example.

**Short:** “Postgres down → `/ready` 503, `/health` still ok.”

**Strong:** “Later: invalid LLM JSON retries then fails safe; conflicting evidence surfaces insufficiency.”

**Deep dive:** Circuit breakers for model provider outages?

---

## Tradeoffs

### Favorite tradeoff?

**Short:** “Simplicity of modular monolith vs independent scaling.”

**Strong:** “Also deterministic engines vs slower build — we gain auditability.”

**Deep dive:** Where did you intentionally choose less ‘AI’?

---

## Production readiness

### Is this project production-ready?

**Short:** “No. It’s a portfolio system with synthetic Acme data through Stage 5 graph analysis — not a production migration product.”

**Strong:** “Production needs auth, secrets, PII controls, CI, eval gates, cloud hardening, real connectors. I can explain the path without overselling.”

**Deep dive:** What’s the MVP production slice you’d ship first?

# Final Interview Guide — ~30 Minute Walkthrough

Speak this like a conversation. When a feature is not built yet, say **“in the design / next stages”** — never pretend.

**Today’s truth:** Stages 1–5 are **implemented** (foundation, schema, synthetic Acme portfolio, ingestion + quality pipeline, NetworkX dependency graph). Stages 6–20 are **planned** unless later marked complete.

Related practice bank: [INTERVIEW_PREP.md](INTERVIEW_PREP.md)

---

## 0. Opening — “Tell me about your project.”

“I’m building Enterprise AI Modernization Architect. It’s an evidence-grounded decision-support system for enterprise legacy modernization and cloud migration planning.

The core idea is: don’t ask a chatbot to invent a migration plan from messy files. First turn enterprise data into a validated inventory and dependency graph, run deterministic risk/cost/wave engines, retrieve policies with RAG and cite evidence, then use a controlled AI agent to recommend options for a human architect to approve.

Right now Stages 1–5 are complete: FastAPI foundation, typed enterprise schema, synthetic Acme portfolio with intentional data-quality defects, a quality-gated ingestion pipeline into Postgres, and a NetworkX dependency graph that surfaces hubs, cycles, and migration bottlenecks. RAG and AI recommendation stages are next.”

---

## 1. Problem

“Large companies run decades of applications — different languages, databases, batch jobs, APIs — with incomplete docs. Before Azure migration, architects need to know what exists, what depends on what, what to move first, which R-strategy fits, what the risks and rough costs are, and what evidence supports each call.”

---

## 2. Motivation

“Bad modernization is expensive: move a central system too early and you cascade failures. Blind LLM plans hallucinate dependencies. I wanted a portfolio project that looks like real AI engineering — data + software + AI + governance — not a wrapper around ChatGPT.”

---

## 3. Overall architecture

“It’s a modular monolith. One FastAPI app with clear packages: config, API, database, ingestion, graph, rag, analysis, risk, cost, migration, agents, auth, evaluation, observability.

Postgres is the system of record. Later, pgvector stores embeddings in the same database. Locally we use Docker Compose; in cloud the same app maps to Azure Container Apps or App Service, Azure Postgres, Blob, and Azure OpenAI via config switches.

I chose a modular monolith because this is one decision pipeline. Microservices would add network complexity before product value.”

---

## 4. Data engineering

“Stage 4 is the gate. We parse the Acme CSV/JSON/YAML portfolio, measure completeness, uniqueness, validity, consistency, and referential integrity, normalize aliases like Postgres→PostgreSQL, reject orphans and near-duplicates, enrich stale systems as inactive, load clean rows into Postgres, and write a quality report that detects the planted defects DQ-001 through DQ-010. Dirty inventory never silently becomes AI truth.”

---

## 5. Enterprise data model

“Stage 2 defined Pydantic schemas and SQLAlchemy models for applications, services, databases, APIs, infrastructure, dependencies, evidence, recommendations, waves, costs, approvals, and audit events. Alembic versions the schema.

The interview point: the LLM is not the database. Shared typed models are.”

---

## 6. Dependency graph

“Stage 5 builds a NetworkX digraph — nodes for apps/services/DBs/APIs/infra, edges for calls, reads, writes, publishes, consumes. We compute degree, betweenness, depth, cycles, and bottlenecks. Identity Platform shows up as a hub; Reporting and Data Warehouse form a cycle. Migration sequencing is a graph problem — I won’t ask a model to ‘just understand dependencies.’”

---

## 7. RAG

“Unstructured policies and runbooks get chunked with evidence IDs like DOC-MIG-008, embedded, stored in pgvector, retrieved, and cited.

If we can’t retrieve support, we say insufficient evidence. That’s how we fight hallucination.”

---

## 8. Modernization analysis

“A deterministic engine will score age, tech lifecycle, complexity, deps, cloud readiness, debt, and more — transparent weights. It proposes 6R strategies: rehost, replatform, refactor, repurchase, retire, retain — plus replace when appropriate — with confidence, evidence, risks, alternatives.”

---

## 9. Risk engine

“Risks across technical, operational, security, compliance, data, dependency, business, migration complexity. Likelihood times impact, with evidence and mitigations. Code computes the score so architects can challenge inputs.”

---

## 10. Cost engine

“I’ll be honest: this is an assumption-based estimator, not Azure billing. We’ll show low/base/high for compute, storage, DB, network, engineering, testing, migration, ops — with assumptions visible. Never fake ROI.”

---

## 11. Migration wave planning

“Waves consider dependencies, criticality, complexity, strategy, risk, effort, readiness. Wave 0 prep, then low-risk, supporting, core, high-risk legacy — each with rationale, prerequisites, blockers.”

---

## 12. AI Architect agent

“One controlled agent — not a swarm. It investigates and recommends; it doesn’t silently mutate inventory. It must call tools that wrap the deterministic engines.”

---

## 13. Tools

“Tools like get_application, search_dependencies, query_dependency_graph, retrieve docs/policies, calculate_risk, calculate_cost, evaluate strategy, generate waves. Tools are how we ground the model in real state.”

---

## 14. LangGraph

“LangGraph gives an explicit state machine: classify → gather evidence → analyze → retrieve policies → strategies → risk → cost → options → recommend → human review. I want something testable, not an unbounded loop.”

---

## 15. Structured outputs

“Recommendations come back as Pydantic models — strategy enums, confidence, evidence IDs. Invalid JSON gets retry/repair, then fail safe. Free-form prose is not the API contract.”

---

## 16. Evidence grounding

“Every material claim cites APP-, DEP-, DOC- style IDs that exist. Invented IDs are evaluation failures. Insufficient evidence is a valid outcome.”

---

## 17. Security

“Stage 1: secrets in env, gitignore, local demo credentials, no public auth yet. Later: authentication, RBAC — viewer, analyst, architect — input validation everywhere, Key Vault in Azure sketches. I don’t expose Stage 1 as internet-ready.”

---

## 18. Human approval

“High-impact recommendations require architect approval. We record who, when, original vs modified recommendation, reason, evidence. That’s responsible AI for enterprise decisions.”

---

## 19. Evaluation

“I’ll build 20+ golden scenarios and measure strategy accuracy, evidence precision, retrieval quality, risk detection, cost band fit, policy compliance, hallucination rate, tool selection. I will not quote accuracy numbers until I run the harness.”

---

## 20. Failure handling

“Stage 1 already separates health from ready — Postgres down returns 503 on ready. Later we’ll adversarially test missing metadata, conflicting docs, cycles, invalid JSON, tool failures, and policy violations — fail safe, don’t bluff.”

---

## 21. Observability

“Today: structured logs with request and trace IDs on every HTTP call. Next: agent run IDs, tool latency, token usage, retrieved evidence IDs, approval events. If I can’t reconstruct why a recommendation happened, I can’t defend it.”

---

## 22. API

“FastAPI with versioned prefix. Today health/ready. Later structured endpoints for projects, inventory import, applications, analysis, migration plans, approve/reject, audit — JSON schemas, not raw LLM text.”

---

## 23. Frontend

“Streamlit as an internal enterprise console: portfolio tables, dependency explorer, deep dive with evidence, roadmap, cost/risk, approval center, audit. Not a giant chatbot skin.”

---

## 24. Docker

“Dockerfile for the API, Compose for API + Postgres pgvector image. Local development shouldn’t require paying for Azure. Same settings keys point elsewhere in cloud.”

---

## 25. Azure architecture

“Planned mapping: Container Apps or App Service, Azure Postgres, Blob, Azure OpenAI, Monitor. Azure-first for the modernization narrative; abstractions keep local free.”

---

## 26. CI/CD

“Planned GitHub Actions: ruff, pytest, mypy, build, security checks. AI features regress quietly — CI is part of quality, not ceremony.”

---

## 27. Tradeoffs

“I traded microservice fashion for a modular monolith. I traded early Azure spend for Docker. I traded ‘autonomous agent’ hype for deterministic engines plus one controlled agent. I traded flashy UI for explainability. Those are intentional.”

---

## 28. Scalability

“I haven’t measured ten thousand applications, so I won’t claim that. The evolution path is: keep algorithms clear, materialize graph snapshots, async ingestion/embeddings, tenant isolation, extract vector search only if pgvector becomes a measured bottleneck.”

---

## 29. Limitations

“Synthetic data. Assumption-based costs. Decision support only — not a migration executor. Stage 1 has no auth. Most AI layers are still ahead. That’s honesty, not weakness.”

---

## 30. Future improvements

“Real CMDB/ServiceNow connectors, stronger hybrid retrieval, prompt/model eval harness in CI, full OTel, Azure private networking and managed identity, richer FinOps inputs — after the core loop is solid.”

---

## 31. Final summary

“Enterprise AI Modernization Architect is five layers: data engineering, enterprise intelligence, grounded AI, governance, and solid platform engineering. Stage 1 proves the platform can run, connect, and be observed. The rest of the roadmap turns that into an interview-defensible modernization advisor — evidence first, humans in the loop, no fake metrics.”

---

## Timing cheat sheet (~30 minutes)

| Minutes | Sections |
|---------|----------|
| 0–3 | Opening, problem, motivation |
| 3–8 | Architecture, data model, data engineering |
| 8–14 | Graph, RAG, modernization/risk/cost/waves |
| 14–22 | Agent, tools, LangGraph, structured output, evidence, security, HITL |
| 22–28 | Eval, failures, observability, API/UI, Docker/Azure/CI |
| 28–30 | Tradeoffs, scale, limits, close |

If they interrupt, jump using [INTERVIEW_PREP.md](INTERVIEW_PREP.md). Always label **built vs designed**.

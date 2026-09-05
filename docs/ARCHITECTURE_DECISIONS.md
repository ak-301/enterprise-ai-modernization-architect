# Architecture Decision Records — Enterprise AI Modernization Architect

Each decision uses:

**Decision · Problem · Alternatives · Choice · Why · Tradeoffs · Interview answer**

Update when a new major choice is made. Do not list future tech as if already shipped.

---

## ADR-001 — Modular monolith (not microservices)

**Decision:** One FastAPI application with internal packages.  
**Problem:** Need clear architecture without ops overload.  
**Alternatives:** Microservices; serverless-only; many AI agents as services.  
**Choice:** Modular monolith.  
**Why:** One decision pipeline; shared schemas; easier testing and interview explanation.  
**Tradeoffs:** Gain simplicity; lose independent deploy scaling until we extract hot paths.  
**Interview answer:** “I optimized for correct domain boundaries first. Microservices would add network complexity before we had product value.”

---

## ADR-002 — PostgreSQL + pgvector as primary store

**Decision:** Postgres for relational data; same DB for vectors later.  
**Problem:** Need durable inventory, audit, and later semantic search.  
**Alternatives:** Separate vector DB day one; document store only; “store in prompts.”  
**Choice:** PostgreSQL + pgvector image locally.  
**Why:** ACID for governance; one operational surface; maps to Azure Database for PostgreSQL.  
**Tradeoffs:** May outgrow pgvector at extreme scale — extract later if measured need.  
**Interview answer:** “I keep system-of-record and early RAG vectors together to reduce moving parts until scale demands a split.”

---

## ADR-003 — Azure-first design, Docker-local development

**Decision:** Document Azure as target; develop free on Docker.  
**Problem:** Show cloud fluency without mandatory cloud spend.  
**Alternatives:** Azure-only; AWS-first; pretend cloud-agnostic with no target.  
**Choice:** Azure-first + settings abstractions.  
**Why:** Credible cloud story; local reproducibility.  
**Tradeoffs:** Must maintain abstractions honestly.  
**Interview answer:** “Config switches storage and LLM providers so local Docker and Azure are the same app with different env.”

---

## ADR-004 — Pydantic Settings with `AIMA_` prefix

**Decision:** Typed env config via pydantic-settings.  
**Problem:** Secrets and environment URLs must not be hard-coded.  
**Alternatives:** Raw `os.environ`; ad-hoc YAML.  
**Choice:** `AIMA_*` settings object.  
**Why:** Fail fast on bad config; consistent with FastAPI/Pydantic.  
**Tradeoffs:** Keep `.env.example` updated.  
**Interview answer:** “Configuration is validated at startup so misconfig fails loudly.”

---

## ADR-005 — Separate liveness and readiness

**Decision:** `/health` vs `/ready`.  
**Problem:** Orchestrators need different signals.  
**Alternatives:** One combined endpoint.  
**Choice:** Split probes.  
**Why:** DB blip ≠ process death.  
**Tradeoffs:** Two endpoints (trivial).  
**Interview answer:** “Health means the process is up; ready means Postgres answers SELECT 1.”

---

## ADR-006 — structlog from day one; OTel later

**Decision:** Structured logs + request/trace IDs now; full OTel in Stage 16.  
**Problem:** AI systems need correlatable events.  
**Alternatives:** print debugging; full OTel immediately.  
**Choice:** structlog foundation.  
**Why:** Immediate value without early tracing complexity.  
**Tradeoffs:** Distributed tracing deferred.  
**Interview answer:** “I established correlated structured logs first, then deepen telemetry when agent/tool metrics exist.”

---

## ADR-007 — LLM provider stub in Stage 1

**Decision:** Default `AIMA_LLM_PROVIDER=stub`; no live calls yet.  
**Problem:** Foundation must work offline without keys.  
**Alternatives:** Require OpenAI key immediately.  
**Choice:** Stub until engines exist.  
**Why:** Prevents “AI theater” before data/graph layers.  
**Tradeoffs:** No AI demo until later stages (intentional).  
**Interview answer:** “I refuse to call a model before I have structured truth and tools worth calling.”

---

## ADR-008 — Hatchling / pyproject packaging

**Decision:** Modern `pyproject.toml` packaging.  
**Problem:** Reproducible installs and tests.  
**Alternatives:** Poetry-only; setup.py.  
**Choice:** hatchling + pip editable install.  
**Why:** Standard, low ceremony.  
**Tradeoffs:** Lockfile may be added in CI stage.  
**Interview answer:** “Standard pyproject keeps tooling simple for a portfolio monolith.”

---

## ADR-009 — Deterministic engines before agent (design lock)

**Decision:** Score/risk/cost/waves as Python engines; agent calls them.  
**Problem:** LLMs are bad at auditable arithmetic and ranking.  
**Alternatives:** Ask the model to “estimate everything.”  
**Choice:** Deterministic core + AI synthesis.  
**Why:** Explainability, tests, less hallucination.  
**Tradeoffs:** More upfront engineering than a single prompt.  
**Interview answer:** “If a calculator can do it, a calculator should do it.”

---

## ADR-010 — Human-in-the-loop for high-impact recommendations

**Decision:** Architect approval required for high-risk changes (Stage 12).  
**Problem:** Blind automation is unacceptable for production migration advice.  
**Alternatives:** Fully autonomous agent.  
**Choice:** Recommend → review → audit.  
**Why:** Responsible AI + enterprise accountability.  
**Tradeoffs:** Slower than autopilot; far safer.  
**Interview answer:** “The system is decision support with an audit trail, not an autopilot for cloud moves.”

---

## ADR-011 — NetworkX for dependency analysis (planned)

**Decision:** Use NetworkX in-process for portfolio-scale graphs.  
**Problem:** Need centrality and sequencing inputs.  
**Alternatives:** Neo4j day one; ask LLM to “understand deps.”  
**Choice:** NetworkX first.  
**Why:** Enough for synthetic/demo scale; pure Python; testable.  
**Tradeoffs:** May need a graph DB at huge scale.  
**Interview answer:** “I pick the smallest tool that correctly models dependencies; NetworkX fits this portfolio size.”

---

## ADR-012 — LangGraph over unconstrained agents (planned)

**Decision:** Explicit state-machine agent workflow.  
**Problem:** Unbounded agents are hard to evaluate and control.  
**Alternatives:** Free ReAct loop; pure chain of prompts; no LLM.  
**Choice:** LangGraph constrained workflow.  
**Why:** Testable steps; clear tool boundaries.  
**Tradeoffs:** Less “autonomous magic”; more reliability.  
**Interview answer:** “I want a workflow I can explain and evaluate, not an agent that wanders.”

---

## ADR-013 — No Kubernetes / Kafka unless needed

**Decision:** Do not add K8s, Kafka, or microservices for resume garnish.  
**Problem:** Overengineering destroys clarity.  
**Alternatives:** Fancy infra diagram.  
**Choice:** Docker Compose locally; Azure containers later.  
**Why:** Credibility > complexity cosplay.  
**Tradeoffs:** Less buzzword density; stronger engineering story.  
**Interview answer:** “I add infrastructure when a bottleneck or requirement appears, not for decoration.”

---

## ADR-014 — One well-designed agent, not many

**Decision:** Single AI Architect agent with tools (planned).  
**Problem:** Multi-agent systems add coordination failure modes.  
**Alternatives:** Swarm of specialist agents.  
**Choice:** One orchestrated agent calling deterministic tools.  
**Why:** Clear ownership; easier eval.  
**Tradeoffs:** Less parallel agent roleplay; more coherence.  
**Interview answer:** “Multiple agents aren’t free — I use one controlled architect with sharp tools.”

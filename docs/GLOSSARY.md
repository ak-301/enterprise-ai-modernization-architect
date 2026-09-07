# Glossary — Enterprise AI Modernization Architect

How to use this file: when you hit an unfamiliar word, read **Simple meaning**, then **How the project uses it**, then practice the **Interview explanation** out loud.

Status tags in “How the project uses it”:
**IMPLEMENTED** · **PLANNED** · **SIMULATED** · **ASSUMED** · **FUTURE**

---

## API

**Simple meaning:** A doorway that lets programs talk to each other using defined requests and responses.  
**Technical meaning:** Application Programming Interface — a contract for operations and payloads.  
**How the project uses it:** FastAPI exposes HTTP APIs (**IMPLEMENTED:** health/ready; **PLANNED:** inventory, analysis, approvals).  
**Interview explanation:** “APIs are the stable contract between our UI/clients and the modernization platform.”

---

## FastAPI

**Simple meaning:** A modern Python web framework for building APIs quickly with automatic docs.  
**Technical meaning:** ASGI framework with Pydantic validation and OpenAPI generation.  
**How the project uses it:** Main backend (**IMPLEMENTED**).  
**Interview explanation:** “I chose FastAPI for typed request/response models and built-in OpenAPI.”

---

## Pydantic

**Simple meaning:** A library that checks data shapes and types so bad data is rejected early.  
**Technical meaning:** Data validation and settings management using Python type hints (v2).  
**How the project uses it:** Settings, health schemas now; domain + AI structured outputs later.  
**Interview explanation:** “Pydantic is our schema layer for APIs and for validating LLM structured output.”

---

## SQLAlchemy

**Simple meaning:** A Python toolkit to talk to databases in a structured way.  
**Technical meaning:** ORM and SQL toolkit; we use 2.x style engine/session.  
**How the project uses it:** Engine/session **IMPLEMENTED**; domain models **PLANNED** Stage 2.  
**Interview explanation:** “SQLAlchemy maps enterprise entities to PostgreSQL without hand-writing every query.”

---

## PostgreSQL

**Simple meaning:** A popular, reliable open-source database for tables and relationships.  
**Technical meaning:** Relational DBMS with strong consistency and rich SQL.  
**How the project uses it:** System of record (**IMPLEMENTED** connectivity; tables Stage 2+).  
**Interview explanation:** “Postgres holds inventory, audit, and later embeddings — the LLM is not the database.”

---

## Alembic

**Simple meaning:** A tool that versions database schema changes like git versions code.  
**Technical meaning:** Migration tool for SQLAlchemy.  
**How the project uses it:** **PLANNED** Stage 2.  
**Interview explanation:** “Alembic lets us evolve tables safely across environments.”

---

## ETL / Data pipeline

**Simple meaning:** A series of steps that take messy inputs and produce clean stored data.  
**Technical meaning:** Extract-Transform-Load (or ELT) processing with validation.  
**How the project uses it:** **IMPLEMENTED** Stage 4 (`raw→parse→validate→normalize→dedupe→enrich→store` + quality report).  
**Interview explanation:** “Our pipeline fails loudly on bad rows instead of silently poisoning AI.”

---

## Schema

**Simple meaning:** The agreed shape of data — which fields exist and what types they are.  
**Technical meaning:** Structural contract (Pydantic models, DB DDL, JSON Schema).  
**How the project uses it:** Health schemas **IMPLEMENTED**; enterprise schemas **IMPLEMENTED** (Stage 2).  
**Interview explanation:** “Shared schemas keep API, DB, and AI outputs speaking one language.”

---

## Normalization (data)

**Simple meaning:** Cleaning and organizing data so the same fact isn’t stored messily in many conflicting ways.  
**Technical meaning:** Relational design + value standardization (e.g. technology aliases).  
**How the project uses it:** **IMPLEMENTED** Stage 4 (e.g. Postgres/PostgreSQL aliases).  
**Interview explanation:** “Normalization turns inconsistent inventory into comparable assets.”

---

## Deduplication

**Simple meaning:** Finding and merging duplicate records that refer to the same thing.  
**Technical meaning:** Entity resolution over identifiers/names.  
**How the project uses it:** **IMPLEMENTED** Stage 4; synthetic duplicates authored in Stage 3 Acme data.  
**Interview explanation:** “Duplicates break dependency graphs and cost estimates, so we detect them explicitly.”

---

## Referential integrity

**Simple meaning:** Links between tables must point to real rows.  
**Technical meaning:** Foreign-key constraints and validation.  
**How the project uses it:** **PLANNED** with domain FKs; quality checks for orphans.  
**Interview explanation:** “Orphan dependencies are a data-quality failure, not something the LLM should invent around.”

---

## Vector database / pgvector

**Simple meaning:** Storage that finds “similar meaning” text using numbers, not only exact keywords.  
**Technical meaning:** Vector similarity search; pgvector is a Postgres extension for embeddings.  
**How the project uses it:** **PLANNED** Stage 6; Docker image already pgvector-capable.  
**Interview explanation:** “We store embeddings in Postgres with pgvector so RAG doesn’t need a second database early.”

---

## Embedding

**Simple meaning:** Turning text into a list of numbers that capture meaning.  
**Technical meaning:** Dense vector representation from an embedding model.  
**How the project uses it:** **PLANNED** for document chunks.  
**Interview explanation:** “Embeddings let us retrieve policy paragraphs that are semantically related to a question.”

---

## RAG

**Simple meaning:** Search your documents first, then generate an answer using what you found.  
**Technical meaning:** Retrieval-Augmented Generation.  
**How the project uses it:** **PLANNED** Stage 6 with citeable evidence IDs.  
**Interview explanation:** “RAG grounds recommendations in our docs so the model isn’t relying only on memory.”

---

## Chunking

**Simple meaning:** Splitting long documents into smaller pieces for search and citation.  
**Technical meaning:** Segmentation with overlap/metadata strategies.  
**How the project uses it:** **PLANNED** Stage 6.  
**Interview explanation:** “Chunks are the retrieval unit — each gets an evidence ID.”

---

## Retrieval

**Simple meaning:** Finding the most relevant chunks for a question.  
**Technical meaning:** Similarity search (and later hybrid search) returning top-k.  
**How the project uses it:** **PLANNED**; evaluated in Stage 14.  
**Interview explanation:** “Retrieval quality matters as much as the generator — bad context yields bad advice.”

---

## LLM

**Simple meaning:** A large language model — AI that reads/writes text.  
**Technical meaning:** Transformer-based generative model accessed via API.  
**How the project uses it:** Config stub **IMPLEMENTED**; real calls **PLANNED**.  
**Interview explanation:** “The LLM reasons and explains; code owns facts and math.”

---

## Agent

**Simple meaning:** A program that can take multiple steps and use tools to reach a goal.  
**Technical meaning:** Tool-using LLM workflow with state.  
**How the project uses it:** Single AI Architect agent **PLANNED** Stage 11.  
**Interview explanation:** “Our agent investigates with tools; it doesn’t freely rewrite the inventory.”

---

## Tool calling

**Simple meaning:** Letting the model request a function like “get dependencies” instead of guessing.  
**Technical meaning:** Structured function/tool invocation from the model.  
**How the project uses it:** **PLANNED** — tools wrap deterministic engines.  
**Interview explanation:** “Tools connect the model to real inventory, graphs, and calculators.”

---

## LangGraph

**Simple meaning:** A library to build AI workflows as clear step-by-step graphs.  
**Technical meaning:** Stateful orchestration framework for agent workflows.  
**How the project uses it:** **PLANNED** Stage 11.  
**Interview explanation:** “LangGraph gives us an explicit state machine we can test, not an unbounded agent loop.”

---

## Structured output

**Simple meaning:** Forcing the model to return data in a fixed schema (like JSON fields we define).  
**Technical meaning:** Schema-constrained generation validated by Pydantic.  
**How the project uses it:** **PLANNED**; invalid output fails safely.  
**Interview explanation:** “We never trust free-form model text as the API’s primary contract.”

---

## Hallucination

**Simple meaning:** When the AI invents facts that aren’t true.  
**Technical meaning:** Ungrounded generation presented as fact.  
**How the project uses it:** Prevent via evidence IDs, engines, evals (**PLANNED**).  
**Interview explanation:** “Hallucination risk is why every material claim needs evidence or an explicit insufficiency statement.”

---

## Grounding / Evidence

**Simple meaning:** Tying an answer to real sources you can point to.  
**Technical meaning:** Citations to inventory IDs, dependency IDs, document chunk IDs.  
**How the project uses it:** Core design principle; implementation **PLANNED**.  
**Interview explanation:** “Evidence over hallucination — if we can’t cite it, we say insufficient evidence.”

---

## Dependency graph

**Simple meaning:** A map of what depends on what.  
**Technical meaning:** Directed graph of assets and dependency edges.  
**How the project uses it:** NetworkX **IMPLEMENTED** Stage 5 (`app/graph`).  
**Interview explanation:** “Migration sequencing is a graph problem before it’s an LLM problem.”

---

## Graph centrality

**Simple meaning:** A score for how “central” or influential a node is in the network.  
**Technical meaning:** Metrics like degree/betweenness/closeness centrality.  
**How the project uses it:** **IMPLEMENTED** Stage 5 — betweenness + in-degree hubs/bottlenecks.  
**Interview explanation:** “High-centrality systems are often migration bottlenecks.”

---

## Risk score

**Simple meaning:** A number summarizing how risky something is.  
**Technical meaning:** Typically likelihood × impact (methodology documented).  
**How the project uses it:** **PLANNED** Stage 8; transparent formula.  
**Interview explanation:** “Risk is computed in code so architects can challenge the inputs, not a mysterious model score.”

---

## Policy-as-code

**Simple meaning:** Business rules stored as configuration/code, not hidden inside prompts.  
**Technical meaning:** Declarative rules evaluated by the application.  
**How the project uses it:** **PLANNED** Stage 12.  
**Interview explanation:** “Policies must be reviewable and testable — prompts are the wrong place for compliance gates.”

---

## RBAC

**Simple meaning:** Different users get different permissions based on roles.  
**Technical meaning:** Role-Based Access Control.  
**How the project uses it:** viewer/analyst/architect **PLANNED** Stage 12.  
**Interview explanation:** “Only architects approve high-impact recommendations.”

---

## Authentication vs Authorization

**Simple meaning:** Authentication = who are you? Authorization = what are you allowed to do?  
**Technical meaning:** Identity verification vs permission checks.  
**How the project uses it:** **PLANNED** Stage 12; Stage 1 API is local/unauthenticated by assumption.  
**Interview explanation:** “Stage 1 is a local foundation without auth; production needs both authn and authz.”

---

## Human-in-the-loop (HITL)

**Simple meaning:** Humans must review/approve important AI recommendations.  
**Technical meaning:** Workflow gate with audit metadata.  
**How the project uses it:** **PLANNED** Stage 12.  
**Interview explanation:** “Enterprise AI Modernization Architect recommends; architects approve — it’s decision support, not autopilot.”

---

## Observability

**Simple meaning:** Being able to see what the system is doing when it runs.  
**Technical meaning:** Logs, metrics, traces for diagnosis and audit.  
**How the project uses it:** Structured logs + request IDs **IMPLEMENTED**; richer agent telemetry **PLANNED** Stage 16.  
**Interview explanation:** “If I can’t correlate a recommendation to tools, retrievals, and approvals, I can’t defend it.”

---

## Trace / Span / Request ID

**Simple meaning:** IDs that help you follow one request through logs.  
**Technical meaning:** Trace = end-to-end journey; span = one unit of work; request ID correlates HTTP calls.  
**How the project uses it:** `X-Request-ID` / `X-Trace-ID` **IMPLEMENTED**; OTel spans **PLANNED**.  
**Interview explanation:** “Correlation IDs turn scattered logs into a story of one analysis run.”

---

## CI/CD

**Simple meaning:** Automatic checks and delivery when code changes.  
**Technical meaning:** Continuous Integration / Continuous Delivery pipelines.  
**How the project uses it:** **PLANNED** Stage 18 (folder reserved).  
**Interview explanation:** “CI protects quality: lint, tests, types — especially important when AI behavior can regress.”

---

## Docker / Docker Compose

**Simple meaning:** Packaging and running apps in consistent containers; Compose runs several together.  
**Technical meaning:** Container runtime + multi-service orchestration for local/dev.  
**How the project uses it:** Dockerfile + Compose **IMPLEMENTED** as files; run when Docker is available.  
**Interview explanation:** “Compose gives a reproducible local API + Postgres without Azure spend.”

---

## Azure OpenAI

**Simple meaning:** Microsoft Azure’s hosted OpenAI-compatible models.  
**Technical meaning:** Managed LLM/embedding deployments in Azure.  
**How the project uses it:** Target provider **PLANNED** Stage 19; local uses stub/compatible API.  
**Interview explanation:** “We abstract the LLM client so swapping to Azure OpenAI is configuration.”

---

## Azure Container Apps / App Service

**Simple meaning:** Azure services that run containerized or web apps without you managing raw VMs.  
**Technical meaning:** Managed application hosting options.  
**How the project uses it:** **PLANNED** Stage 19 deployment sketch.  
**Interview explanation:** “For this modular monolith, Container Apps or App Service is enough — no Kubernetes required.”

---

## MLOps

**Simple meaning:** Engineering habits that keep ML/AI systems reliable over time.  
**Technical meaning:** CI, evaluation, monitoring, versioning for models/prompts/data.  
**How the project uses it:** Eval + observability stages encode MLOps ideas without claiming a full platform.  
**Interview explanation:** “MLOps here means measurable evals, regression tests, and runtime telemetry for AI decisions.”

---

## Responsible AI

**Simple meaning:** Building AI that is safe, fair enough for the context, transparent, and accountable.  
**Technical meaning:** Governance, human oversight, auditability, minimized unjustified automation.  
**How the project uses it:** Evidence requirements, HITL, policies, honest synthetic-data labeling.  
**Interview explanation:** “Responsible AI in Enterprise AI Modernization Architect means grounded recommendations, human approval, and no fake accuracy claims.”

---

## Modular monolith

**Simple meaning:** One application, organized into clear internal modules.  
**Technical meaning:** Single deployable with package boundaries instead of network-separated services.  
**How the project uses it:** **IMPLEMENTED** project shape.  
**Interview explanation:** “Modular monolith gives clean architecture without microservice tax.”

---

## Liveness vs Readiness

**Simple meaning:** Liveness = process alive; readiness = safe to send real traffic.  
**Technical meaning:** Probe semantics for orchestrators.  
**How the project uses it:** `/health` vs `/ready` **IMPLEMENTED**.  
**Interview explanation:** “If Postgres is down, ready fails but health can still succeed.”

---

## 6 Rs (+ Replace)

**Simple meaning:** Classic migration strategies: Rehost, Replatform, Refactor, Repurchase, Retire, Retain (and sometimes Replace).  
**Technical meaning:** Strategy taxonomy for modernization decisions.  
**How the project uses it:** **PLANNED** Stage 7 classification.  
**Interview explanation:** “We classify each app into an R-strategy with confidence, evidence, risks, and alternatives.”

---

## Synthetic data

**Simple meaning:** Fake but realistic data made for demos and tests.  
**Technical meaning:** Generated datasets with known properties and intentional defects.  
**How the project uses it:** **SIMULATED** Acme enterprise dataset (**IMPLEMENTED** Stage 3).  
**Interview explanation:** “I always disclose that the portfolio is synthetic — the engineering is real, the customer isn’t.”

---

## OpenAI-compatible API

**Simple meaning:** An API that looks like OpenAI’s chat/embeddings endpoints.  
**Technical meaning:** HTTP schema compatibility enabling provider swaps.  
**How the project uses it:** Settings support **IMPLEMENTED**; live usage **PLANNED**.  
**Interview explanation:** “Compatibility lets us develop locally and point to Azure OpenAI later.”

---

## System of record

**Simple meaning:** The official place where the true data lives.  
**Technical meaning:** Authoritative datastore for entities and audit.  
**How the project uses it:** PostgreSQL (design lock).  
**Interview explanation:** “Prompts are ephemeral; the system of record is Postgres.”

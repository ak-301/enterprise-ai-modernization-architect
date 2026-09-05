# AI Architecture — Enterprise AI Modernization Architect

**Status:** Stage 1 has **configuration stubs only**. No LLM calls, no RAG, no agent code yet. Everything below is the **intended** design so later stages stay coherent.

---

## Big idea in one paragraph

Enterprise AI Modernization Architect uses AI as a **careful advisor**, not as a database and not as an unsupervised automation system. Structured inventory, graphs, and deterministic engines hold facts and math. The LLM retrieves cited documents, reasons about tradeoffs, and proposes structured recommendations. Humans approve high-impact changes.

---

## What the LLM does (PLANNED)

- Read unstructured documents and help extract structured facts (with validation)
- Summarize evidence for an architect
- Propose modernization strategy **candidates** with reasoning
- Explain why a wave order makes sense
- Answer portfolio questions using tools (“what depends on this DB?”)

## What the LLM does NOT do

- Store enterprise truth
- Count dependencies or compute centrality
- Multiply cost line items
- Enforce security policy
- Approve production migrations
- Invent evidence IDs

If evidence is missing, the system should say: **“Insufficient evidence.”**

---

## Why don't we just send everything to ChatGPT?

**Short answer (say this):**  
Because ChatGPT is not a system of record, can’t reliably do graph math, can’t give auditable cost arithmetic, and will invent plausible-sounding dependencies. Enterprises need traceable evidence, deterministic checks, and human approval.

**Strong answer:**  
A modernization recommendation is a **multi-system decision**. It needs:

1. Validated inventory (data engineering)
2. Dependency topology (graphs)
3. Transparent scores (code)
4. Policy gates (governance)
5. Citations to real docs/rows (RAG + IDs)
6. Evaluation harnesses (quality)

Dumping CSVs into a chat window fails on hallucination, reproducibility, audit, cost control, and security. Enterprise AI Modernization Architect keeps the LLM inside a **tool-using workflow with schema validation**.

**Deep dive an interviewer may ask:**  
“Wouldn’t a long context window fix this?”  
Long context helps reading documents, but it does not replace referential integrity, graph algorithms, or approval audit trails. Context still hallucinates and is expensive/latency-heavy at portfolio scale.

---

## RAG (Retrieval-Augmented Generation) — PLANNED Stage 6

**Simple meaning:**  
Before the model answers, we search our own documents for relevant pieces, then we ask the model to answer **using those pieces** and cite them.

**Pipeline:**

```
Documents → parse → chunk → metadata + evidence ID
         → embedding → pgvector store
         → retrieve top-k → attach to prompt → generate → validate citations
```

**Embedding:** a vector (list of numbers) representing meaning of text.  
**pgvector:** PostgreSQL extension for storing vectors and finding nearest neighbors.  
**Evidence ID:** stable ID like `DOC-MIG-008` so answers are auditable.

---

## Agents and LangGraph — PLANNED Stage 11

**Agent (simple):** a program that can take steps and call tools to finish a goal.

**Why use an agent?**  
Modernization questions need multi-step investigation: get app → query deps → retrieve policy → run risk → draft recommendation. A single prompt is too shallow.

**When should we NOT use an agent?**  
When the task is pure calculation, validation, or a fixed ETL step. Agents add latency, cost, and failure modes. Prefer deterministic code.

**LangGraph (simple):** a library for building AI workflows as an **explicit state machine** (clear steps), instead of a free-roaming loop that is hard to test.

Target rough workflow:

```
Classify request → Gather evidence → Analyze architecture/deps
→ Retrieve policies → Evaluate strategies → Risk → Cost
→ Generate options → Recommend → Human review → Final roadmap
```

---

## Tool calling — PLANNED

Tools wrap engines, for example:

- `get_application`, `search_dependencies`, `query_dependency_graph`
- `retrieve_architecture_docs`, `calculate_risk`, `calculate_cost`
- `evaluate_modernization_strategy`, `generate_migration_wave`

The agent **must not** silently overwrite inventory. It investigates and recommends.

---

## Structured outputs — PLANNED

Model responses are parsed into **Pydantic models** (strategy enum, confidence, evidence IDs, risks, assumptions). Invalid JSON → retry/repair → fail safely. Never silently accept malformed AI output.

---

## Evidence grounding & hallucination prevention

| Control | Intent |
|---------|--------|
| Cite only retrieved/known IDs | Stop invented `DOC-…` references |
| Deterministic engines for math | Stop numeric hallucination |
| “Insufficient evidence” path | Prefer abstention over fiction |
| Evaluation golden set (Stage 14) | Measure hallucination rate |
| Human approval | Catch high-impact mistakes |

---

## Deterministic analysis vs AI

```
Deterministic: validation, graph metrics, scores, risk math, cost bands, wave rules, policies
AI: extraction, synthesis, explanation, classification with citations
```

---

## Model selection, latency, token cost (PLANNED practices)

- Default provider is **stub** in Stage 1 so local work needs no keys.
- Prefer smaller/faster models for classification; larger models only when needed.
- Retrieve fewer, better chunks (quality > stuffing context).
- Cache embeddings for unchanged docs.
- Log token usage once Stage 16 observability expands (not measured yet).

We do **not** claim specific latency or cost numbers until measured.

---

## AI evaluation — PLANNED Stage 14

Golden scenarios (≥20) with expected strategy/risks/constraints. Metrics only after runs:

- strategy accuracy, evidence precision, retrieval recall
- risk detection, cost band compliance, policy violations
- hallucination rate, tool selection quality, latency/tokens

See [EVALUATION.md](EVALUATION.md).

---

## Stage 1 AI readiness (IMPLEMENTED)

- `AIMA_LLM_PROVIDER` / base URL / model / embedding settings exist
- Default provider: `stub`
- Logging middleware ready to later attach `agent_run_id`, tool latency, tokens
- No live model calls in tests or runtime today

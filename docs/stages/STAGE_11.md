# Stage 11 — AI Architect Agent

## 1. Status

**PLANNED** — not implemented yet. Do not describe this stage as complete in interviews until code and tests exist.

## 2. What are we building?

Controlled agent that uses tools and returns structured recommendations.

## 3. Why are we building it?

Multi-step investigation needs orchestration with guardrails.

## 4. What problem does it solve?

Single-shot ChatGPT plan without tools or schemas.

## 5. Concepts I need to understand first

### Agent

**Simple:** Software that can take multiple steps and call tools to finish a goal.  
**Why:** Modernization questions need investigation, not one-shot chat.

### Tool calling

**Simple:** The model asks to run a function (“get dependencies”) instead of guessing.  
**Why:** Connects language reasoning to real inventory, graphs, and calculators.

### LangGraph / state machine

**Simple:** An explicit flowchart of steps with state passed between them.  
**Why:** Controllable and testable — unlike an unbounded autonomous loop.

### Structured output

**Simple:** Force the model to return fields that match a schema (strategy, evidence IDs, …).  
**Why:** Invalid or free-form answers cannot silently become API truth.

### When NOT to use an agent

**Simple:** If the job is pure math, validation, or ETL — just run Python.  
**Why:** Agents cost latency, tokens, and new failure modes.  
**See also:** [AI_ARCHITECTURE.md](../AI_ARCHITECTURE.md).

## 6. Technologies used

Primary stack for this stage: **LangGraph, LLM, tools**

### LangGraph

- **What it is:** Workflow

- **Why we use it:** Fits this stage's problem without overengineering.

- **How we use it:** Explicit steps

### LLM

- **What it is:** Reasoning

- **Why we use it:** Fits this stage's problem without overengineering.

- **How we use it:** Synthesis + explanation


## 7. Architecture

```
Inputs from earlier stages
        ↓
Stage 11 processing (AI Architect Agent)
        ↓
Outputs consumed by later stages
```

See also: [PROJECT_ROADMAP.md](../PROJECT_ROADMAP.md), [ARCHITECTURE.md](../ARCHITECTURE.md).

## 8. Implementation

**Not implemented.** When this stage is built, replace this section with what actually shipped (files, commands, test results). Never claim features here until they exist.

## 9. Files

**Planned locations** (may shift slightly during implementation):

- Application code under `app/` modules reserved for this capability
- Data under `data/` when this stage produces datasets
- Tests under `tests/unit`, `tests/integration`, and/or `tests/e2e`
- This document: `docs/stages/STAGE_11.md`

## 10. Example

A realistic example will be added when the stage is implemented. Until then, use the end-to-end story in [PROJECT_GUIDE.md](../PROJECT_GUIDE.md) and treat examples as **PLANNED**.

## 11. Failure scenarios

Typical failures this stage must eventually handle:

- Invalid or incomplete inputs from upstream stages
- Conflicting metadata
- Dependency/tool/database unavailability (where relevant)
- Ambiguous cases that require “Insufficient evidence” rather than guessing

## 12. How we handle failures

**Planned approach:** validate inputs, return structured errors, prefer abstention over hallucination, and cover cases with tests in Stages 14–15.

## 13. Important engineering decisions

Will be recorded in [ARCHITECTURE_DECISIONS.md](../ARCHITECTURE_DECISIONS.md) when choices are finalized during implementation. Design locks already made: evidence over hallucination; deterministic math in code; human approval for high impact.

## 14. Alternatives

Possible alternatives usually include: (a) pushing more work into the LLM, (b) adding heavier infrastructure earlier, or (c) skipping the stage. We reject (a)/(b) unless a measured need appears; we reject (c) because this stage is part of the credible five-layer story.

## 15. What I learned

*(Fill after implementation.)* Learning goals now: understand **why** this stage exists and which glossary terms it depends on.

## 16. Interview questions

**Beginner**

1. What is Stage 11 trying to produce?
2. Why can't Stage 1 alone answer migration questions?

**Intermediate**

3. What would go wrong if we skipped this stage?
4. Which parts should be deterministic vs LLM-driven?

**Advanced**

5. How would you test this stage?
6. How does this stage change at 100× portfolio size?

## 17. Interview answers

1. “It produces ai architect agent capabilities that later stages consume.”
2. “Stage 1 is only the platform foundation — health, config, database connectivity.”
3. “We'd force the LLM to invent structure, scores, or plans without durable evidence.”
4. “Math, validation, and policy gates stay in code; language reasoning can use the model.”
5. “Unit tests for logic, integration tests for storage/API, and golden scenarios where AI is involved.”
6. “Keep algorithms clear first; add caching, async workers, or service extraction only when measured.”

## 18. 30-second explanation

“Stage 11 is AI Architect Agent. It isn't built yet in the repo. When we implement it, it will sit in the pipeline between earlier data/platform work and later recommendation/governance stages.”

## 19. 2-minute explanation

“In the full project design, Stage 11 exists because Multi-step investigation needs orchestration with guardrails. Today the status is planned only — I'm careful not to claim it in interviews as shipped. The learning goal is to understand the problem it solves: Single-shot ChatGPT plan without tools or schemas. Technologies we expect: LangGraph, LLM, tools.”

## 20. Deep-dive questions

- How do you prevent silent data corruption at this boundary?
- What metrics prove this stage works?
- What is the rollback story if this stage’s output is wrong?
- How does this interact with human approval and audit?

## 21. Production version

Before real enterprise use: harden auth, secrets, PII handling, scalability tests, monitoring, and integration with real CMDBs/ITSM tools. This portfolio stage uses synthetic assumptions unless explicitly measured.

## 22. Stage summary

- Status: **PLANNED**
- Goal: Controlled agent that uses tools and returns structured recommendations.
- Why: Multi-step investigation needs orchestration with guardrails.
- Key tech: LangGraph, LLM, tools
- Depends on earlier stages being solid
- Must remain honest: not implemented until code + tests land
- Interview focus: problem framing + where LLM must not own this work
- Docs to update after implementation: roadmap table, guide, ADRs, interview prep

# Stage 12 — Policy & Human Approval

## 1. Status

**PLANNED** — not implemented yet. Do not describe this stage as complete in interviews until code and tests exist.

## 2. What are we building?

Roles, policies, approve/reject/modify, audit trail.

## 3. Why are we building it?

High-impact advice needs accountability.

## 4. What problem does it solve?

Autonomous execution of migration decisions.

## 5. Concepts I need to understand first

### RBAC

**Simple:** See [GLOSSARY.md](../GLOSSARY.md) for `RBAC` if listed; otherwise learn it while implementing this stage.

### Policy-as-code

**Simple:** See [GLOSSARY.md](../GLOSSARY.md) for `Policy-as-code` if listed; otherwise learn it while implementing this stage.

### Audit trail

**Simple:** See [GLOSSARY.md](../GLOSSARY.md) for `Audit trail` if listed; otherwise learn it while implementing this stage.

### HITL

**Simple:** See [GLOSSARY.md](../GLOSSARY.md) for `HITL` if listed; otherwise learn it while implementing this stage.


## 6. Technologies used

Primary stack for this stage: **Auth, RBAC, policy-as-code**

### Auth middleware

- **What it is:** Access control

- **Why we use it:** Fits this stage's problem without overengineering.

- **How we use it:** Protect APIs

### Policy config

- **What it is:** Rules

- **Why we use it:** Fits this stage's problem without overengineering.

- **How we use it:** Testable gates


## 7. Architecture

```
Inputs from earlier stages
        ↓
Stage 12 processing (Policy & Human Approval)
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
- This document: `docs/stages/STAGE_12.md`

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

1. What is Stage 12 trying to produce?
2. Why can't Stage 1 alone answer migration questions?

**Intermediate**

3. What would go wrong if we skipped this stage?
4. Which parts should be deterministic vs LLM-driven?

**Advanced**

5. How would you test this stage?
6. How does this stage change at 100× portfolio size?

## 17. Interview answers

1. “It produces policy & human approval capabilities that later stages consume.”
2. “Stage 1 is only the platform foundation — health, config, database connectivity.”
3. “We'd force the LLM to invent structure, scores, or plans without durable evidence.”
4. “Math, validation, and policy gates stay in code; language reasoning can use the model.”
5. “Unit tests for logic, integration tests for storage/API, and golden scenarios where AI is involved.”
6. “Keep algorithms clear first; add caching, async workers, or service extraction only when measured.”

## 18. 30-second explanation

“Stage 12 is Policy & Human Approval. It isn't built yet in the repo. When we implement it, it will sit in the pipeline between earlier data/platform work and later recommendation/governance stages.”

## 19. 2-minute explanation

“In the full project design, Stage 12 exists because High-impact advice needs accountability. Today the status is planned only — I'm careful not to claim it in interviews as shipped. The learning goal is to understand the problem it solves: Autonomous execution of migration decisions. Technologies we expect: Auth, RBAC, policy-as-code.”

## 20. Deep-dive questions

- How do you prevent silent data corruption at this boundary?
- What metrics prove this stage works?
- What is the rollback story if this stage’s output is wrong?
- How does this interact with human approval and audit?

## 21. Production version

Before real enterprise use: harden auth, secrets, PII handling, scalability tests, monitoring, and integration with real CMDBs/ITSM tools. This portfolio stage uses synthetic assumptions unless explicitly measured.

## 22. Stage summary

- Status: **PLANNED**
- Goal: Roles, policies, approve/reject/modify, audit trail.
- Why: High-impact advice needs accountability.
- Key tech: Auth, RBAC, policy-as-code
- Depends on earlier stages being solid
- Must remain honest: not implemented until code + tests land
- Interview focus: problem framing + where LLM must not own this work
- Docs to update after implementation: roadmap table, guide, ADRs, interview prep

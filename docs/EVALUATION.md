# Evaluation — Enterprise AI Modernization Architect

## Status

**PLANNED** (Stage 14). No evaluation metrics have been measured yet.

Stage 1 only proves the **test harness foundation** (pytest, FastAPI TestClient) with **11 foundation tests** — not AI quality.

---

## Commitment (non-negotiable)

We will **not** claim:

- accuracy percentages
- latency SLOs
- token averages
- “handles N applications”

…unless a real run produced those numbers.

Report only **measured** results after the golden harness exists.

---

## Planned golden set

At least **20 synthetic modernization scenarios**, each with:

- enterprise state
- application + dependencies
- evidence
- expected strategy
- expected risks / constraints / wave hints

## Planned metrics

| Area | Examples |
|------|----------|
| Classification | Strategy accuracy |
| Grounding | Evidence precision; hallucination rate |
| Retrieval | Recall / relevance |
| Risk | High-impact risk detection |
| Cost | Within documented tolerance band |
| Planning | Sequence reasonableness |
| Policy | Violation rate |
| Ops | Latency, token usage (when instrumented) |

## Related docs

- [stages/STAGE_14.md](stages/STAGE_14.md)
- [AI_ARCHITECTURE.md](AI_ARCHITECTURE.md)
- [PROJECT_ROADMAP.md](PROJECT_ROADMAP.md)

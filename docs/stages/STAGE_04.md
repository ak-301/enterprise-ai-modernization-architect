# Stage 04 — Data Engineering Pipeline

## 1. Status

**COMPLETED**

Verified with unit + integration tests. Full suite: **42 pytest tests passed** when Stage 4 landed. Quality report detects planted defects **DQ-001…DQ-010**.

## 2. What are we building?

Pipeline: **raw → parse → validate/quality → normalize → dedupe → enrich → store + quality report**.

## 3. Why are we building it?

Dirty inventory must not silently become AI "truth."

## 4. What problem does it solve?

Silent acceptance of bad rows and missing quality metrics. Stage 3 planted defects; this stage **detects, reports, and rejects** them where needed before Postgres load.

## 5. Concepts I need to understand first

### ETL

**Simple:** Extract → Transform → Load. Move raw files into a clean system of record.  
**Interview:** Ours is a deliberate quality gate, not a firehose copy.

### Validation error

**Simple:** A structured finding that a row/field violates rules (missing owner, orphan FK, bad version).  
**Interview:** Fail loud in a report; do not invent values.

### Completeness

**Simple:** Required fields present (e.g. application owner).  
**Interview:** Measured as ratios in the quality report.

### Referential integrity

**Simple:** Every referenced ID exists (service → application, dependency endpoints).  
**Interview:** Orphans are rejected from store, not silently linked.

### Normalize / dedupe / enrich

**Simple:** Canonical aliases (Postgres→PostgreSQL); keep one near-duplicate; derive fields (`is_active`, asset types).

## 6. Technologies used

Primary stack: **Python, Pydantic (schemas), pandas, SQLAlchemy, PostgreSQL**

### pandas / PyYAML

- **What:** Parse CSV/YAML inventories  
- **Why:** Match Stage 3 export shapes  
- **How:** `app/ingestion/parse.py` via `app/synthetic/acme.py`

### Quality report

- **What:** JSON summary of dimensions + planted DQ IDs  
- **Why:** Prove detection of intentional defects  
- **How:** `data/processed/acme/quality_report.json` (gitignored artifact)

### PostgreSQL

- **What:** Sink for clean inventory  
- **Why:** System of record from Stage 2  
- **How:** `app/ingestion/store.py` replaces project `PROJ-ACME-001` then inserts

## 7. Architecture

```
data/raw/acme (Stage 3 SIMULATED)
        ↓ parse
in-memory records
        ↓ assess_quality (DQ-001…DQ-010)
        ↓ normalize aliases
        ↓ dedupe near-duplicates
        ↓ enrich (is_active, asset types)
        ↓ filter orphans
        ↓ store (PostgreSQL) + write quality_report.json
```

CLI: `python -m app.ingestion` (optional `--no-persist` / `--no-report`).

See also: [PROJECT_ROADMAP.md](../PROJECT_ROADMAP.md), [DATA_ARCHITECTURE.md](../DATA_ARCHITECTURE.md).

## 8. Implementation

Shipped:

1. `app/ingestion/` package (parse, quality, normalize, dedupe, enrich, store, pipeline, CLI)
2. Detection of planted defects **DQ-001 through DQ-010**
3. Rejection of near-duplicate app (`APP-DUP-001`), orphan service, orphan dependency
4. Normalization of Java/Postgres aliases; invalid version stripped on store
5. Stale app marked `is_active=False`
6. Technology catalog upsert; core inventory entities persisted
7. Unit tests (dry-run + quality) and integration test (Postgres load)

**Not shipped:** persisting operational metrics / migration history (no ORM tables yet); document ingestion (Stage 6); NetworkX (Stage 5).

## 9. Files

| Path | Responsibility |
|------|----------------|
| `app/ingestion/parse.py` | Load raw Acme files |
| `app/ingestion/quality.py` | Quality dimensions + DQ mapping |
| `app/ingestion/normalize.py` | Alias / blank cleanup |
| `app/ingestion/dedupe.py` | Near-duplicate application handling |
| `app/ingestion/enrich.py` | Derived fields + storeable filter |
| `app/ingestion/store.py` | PostgreSQL persistence |
| `app/ingestion/pipeline.py` | Orchestration |
| `app/ingestion/__main__.py` | CLI entrypoint |
| `tests/unit/test_ingestion_pipeline.py` | Pipeline unit tests |
| `tests/integration/test_ingestion_store.py` | DB integration test |

## 10. Example

```python
from app.database.session import SessionLocal
from app.ingestion import run_acme_pipeline, pipeline_summary

session = SessionLocal()
result = run_acme_pipeline(session, persist=True, write_report=True)
session.commit()
print(pipeline_summary(result))
# planted_defect_ids_detected includes DQ-001 … DQ-010
```

Dry-run (no DB):

```bash
python -m app.ingestion --no-persist
```

## 11. Failure scenarios

- Missing raw files → `FileNotFoundError` from Stage 3 helpers  
- Orphan service / dependency → rejected from store, recorded in report  
- Invalid version → validity issue; version stored as `NULL`  
- Near-duplicate applications → one kept, duplicate rejected  
- DB unavailable → CLI fails; integration tests require Postgres

## 12. How we handle failures

Validate and report structured issues; reject unsafe rows; prefer abstention (no invented owners/links) over silent repair. Circular deps are **warnings** (still stored for Stage 5 graph analysis).

## 13. Important engineering decisions

- Quality assessed on **raw** parse so alias inconsistency remains measurable before normalize  
- Dependency endpoints stay type + external_id (Stage 2 design); Stage 4 enforces existence  
- Ops metrics / migration history parsed for future stages but not persisted yet  
- Processed reports under `data/processed/` stay gitignored

## 14. Alternatives

| Alternative | Why rejected |
|-------------|--------------|
| Load CSVs blindly | Would make AI trust junk |
| Auto-fix every defect | Hides data problems from architects |
| LLM for validation | Non-deterministic; wrong layer |

## 15. What I learned

Enterprise ingestion is a **product surface**: dimensions, reject vs warn, and an auditable report matter as much as the INSERT statements.

## 16. Interview questions

**Beginner**

1. What does Stage 4 produce?
2. Why can't we skip quality and go straight to the LLM?

**Intermediate**

3. How do you detect the planted Acme defects?
4. What is deterministic vs LLM-driven here?

**Advanced**

5. How would you scale this to 100× portfolio size?
6. How do completeness and referential integrity differ?

## 17. Interview answers

1. “A clean Postgres inventory plus a quality report that names what was rejected and why.”
2. “The model would treat missing owners and orphan links as facts.”
3. “Rules for uniqueness, completeness, validity, consistency, referential integrity, staleness, and conflicting metadata — mapped to DQ-001…DQ-010.”
4. “All of Stage 4 is deterministic code; no LLM.”
5. “Keep rules clear; batch/async workers and partitioning later when measured.”
6. “Completeness is ‘field present’; referential integrity is ‘referenced ID exists.’”

## 18. 30-second explanation

“Stage 4 is the data engineering pipeline. It parses the synthetic Acme files, measures data quality, normalizes aliases, rejects orphans and duplicates, loads clean rows into Postgres, and writes a quality report that detects the intentional defects we planted in Stage 3.”

## 19. 2-minute explanation

“After Stage 3 authored messy but realistic inventory, Stage 4 is the gate. We parse CSV/JSON/YAML, run quality checks across completeness, uniqueness, validity, consistency, and referential integrity, normalize spellings like Postgres→PostgreSQL, dedupe the near-duplicate Customer Portal, enrich stale systems as inactive, and store only safe rows. The quality report lists DQ-001 through DQ-010 so we can prove the pipeline is honest — dirty data never silently becomes AI truth.”

## 20. Deep-dive questions

- How do you prevent silent data corruption at this boundary?
- What metrics prove this stage works?
- What is the rollback story if this stage’s output is wrong?
- How does this interact with human approval and audit?

## 21. Production version

Before real enterprise use: harden auth, secrets, PII handling, idempotent upserts with audit events, scalability tests, monitoring, and connectors to real CMDBs/ITSM. This portfolio stage uses synthetic assumptions.

## 22. Stage summary

- Status: **COMPLETED**
- Goal: raw → parse → validate → normalize → dedupe → enrich → store + quality report
- Why: Dirty inventory must not silently become AI truth
- Key tech: Python, pandas, SQLAlchemy, PostgreSQL
- Detects DQ-001…DQ-010; rejects unsafe rows
- Next: Stage 6 Knowledge Base & RAG
- Docs to update after implementation: roadmap, guide, master docs, interview prep

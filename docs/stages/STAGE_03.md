# Stage 03 — Synthetic Enterprise Environment

## 1. Status

**COMPLETED**

Verified with dataset presence tests and intentional defect assertions (**34 pytest tests** in full suite when Stage 3 tests included).

## 2. What are we building?

A **synthetic** Acme Financial Services portfolio: applications, services, databases, APIs, infrastructure, dependencies, operational metrics, migration history, technology catalog, architecture/policy documents, and a catalog of **intentional data-quality defects**.

## 3. Why are we building it?

We need believable enterprise complexity for demos and later evaluation — without real customer data. Stage 4 needs messy inputs to prove validation works.

## 4. What problem does it solve?

Toy 3-service examples look unserious. This portfolio looks like a financial enterprise estate (Java, .NET, Python, COBOL/mainframe adapter, Postgres/SQL Server/Oracle, Redis, MQ, Kafka, batch, SFTP).

## 5. Concepts I need to understand first

### Synthetic data

**Simple:** Fake but realistic data made for demos/tests.  
**Why:** Safe to share; labeled honestly.

### Data quality defect

**Simple:** A known problem in the data (missing owner, orphan dependency, etc.).  
**Why:** We plant them on purpose so Stage 4 can detect them.

### Criticality

**Simple:** How important a system is to the business (`critical` / `high` / `medium` / `low`).

### Operational metrics

**Simple:** Runtime signals like CPU, latency, error rate, throughput.

## 6. Technologies used

### CSV / JSON / YAML

- **What:** Common exchange formats  
- **Why:** Realistic enterprise export shapes  
- **How:** Inventories under `data/raw/acme/`

### pandas / PyYAML

- **What:** Tabular and YAML loaders  
- **Why:** Tests and future Stage 4 parsing  
- **How:** `app/synthetic/acme.py`

### Markdown documents

- **What:** Synthetic architecture/policy docs with evidence IDs (`DOC-…`)  
- **Why:** Stage 6 RAG will cite them later  
- **How:** `data/documents/acme/`

## 7. Architecture

```
Synthetic authoring (Stage 3)
        ↓
data/raw/acme/*.csv|json|yaml
data/documents/acme/DOC-*.md
        ↓
app/synthetic/acme.py (load helpers only)
        ↓
Stage 4 pipeline (PLANNED): validate → normalize → store
```

## 8. Implementation

Shipped:

1. Acme portfolio (~12 apps including core 10 + duplicate/stale cases)
2. Services, databases, APIs, infrastructure, dependencies
3. Ops metrics + migration history + tech catalog
4. Six architecture/policy documents with `DOC-*` IDs
5. `data_quality_defects.json` listing DQ-001…DQ-010
6. Loader helpers + unit tests asserting files and intentional defects

**Not shipped:** ingestion into Postgres (Stage 4).

## 9. Files

| Path | Responsibility |
|------|----------------|
| `data/raw/acme/*` | Raw synthetic inventories |
| `data/documents/acme/DOC-*.md` | Citeable synthetic docs |
| `app/synthetic/acme.py` | Path constants + loaders |
| `tests/unit/test_synthetic_acme.py` | Dataset + defect tests |

## 10. Example

```python
from app.synthetic.acme import portfolio_summary, load_applications
print(portfolio_summary())
print(load_applications()[["application_id", "application_name", "owner"]].head())
```

## 11. Failure scenarios

- Missing raw files → `FileNotFoundError` from `assert_acme_dataset_present()`
- Someone treats data as real → documentation/README explicitly say SYNTHETIC

## 12. How we handle failures

- Tests fail if required files or planted defects disappear
- README + defect catalog make honesty explicit

## 13. Important engineering decisions

- Plant defects in data **and** document them (no hidden tricks)
- Keep Stage 3 as data + loaders only — no silent “fixups” in code yet
- Evidence-ready document IDs from day one for later RAG

## 14. Alternatives

| Alternative | Why not |
|-------------|---------|
| Perfectly clean data | Wouldn’t exercise Stage 4 quality gates |
| Real anonymized bank data | Legal/privacy risk; not appropriate here |
| Generate randomly each run | Harder to write golden Stage 14 scenarios |

## 15. What I learned

Enterprise AI demos need **messy, labeled** synthetic data. Clean CSVs hide the real engineering problem.

## 16. Interview questions

**Beginner:** What is synthetic data? Why Acme?  
**Intermediate:** Name three intentional defects and why they matter.  
**Advanced:** How would Stage 4 quantify completeness vs referential integrity on this set?

## 17. Interview answers

- “Synthetic means fictional but realistic — labeled clearly, never sold as customer data.”
- “We planted missing owners, duplicates, invalid versions, orphan deps/services, inconsistent tech aliases, and a stale app.”
- “Stage 4 should emit a quality report with those dimensions and fail loud on bad rows.”

## 18. 30-second explanation

“Stage 3 creates a synthetic Acme Financial Services portfolio with apps, services, databases, dependencies, ops metrics, and policy documents — plus intentional data-quality defects for the next pipeline stage.”

## 19. 2-minute explanation

“After locking the schema in Stage 2, Stage 3 authors the world we will analyze. Acme has portals, loans, payments, risk, identity, documents, warehouse, and a mainframe adapter, with Redis/MQ/Kafka/batch/SFTP style integrations. The data is deliberately imperfect: duplicates, missing owners, invalid versions, orphan references, inconsistent Postgres naming, and a stale VB6 system. We catalog those defects so Stage 4 can prove detection — we do not pretend inventory is clean.”

## 20. Deep-dive questions

- How do you version synthetic datasets as schemas evolve?
- How do golden evaluation scenarios pin to specific defect IDs?
- When is synthetic data not enough for stakeholder demos?

## 21. Production version

Replace synthetic exports with CMDB/ServiceNow/cloud inventory connectors; keep the same schemas. Never load real PII into demo repos.

## 22. Stage summary

- Status: **COMPLETED** / data is **SIMULATED**
- Acme portfolio + docs + defect catalog
- Loaders only — no Stage 4 pipeline yet
- Tests lock presence of core apps and intentional defects
- Next: Stage 4 Data Engineering Pipeline

# Data Architecture — Enterprise AI Modernization Architect

**Status:** Stage 1 connectivity **IMPLEMENTED**. Stage 2 enterprise schema **IMPLEMENTED**. Stage 3 synthetic Acme datasets **IMPLEMENTED** (**SIMULATED**). Stage 4 ingestion pipeline **IMPLEMENTED** (quality report + Postgres load).

---

## Why data engineering comes before AI

If you feed dirty, incomplete, conflicting inventory into an LLM, you get confident nonsense.

Analogy: you would not ask a consultant to plan a city move using a napkin sketch with missing streets. First you build a map.

The project's map is:

1. Raw files (**Stage 3 authored** — Acme under `data/raw/acme`)
2. Validated structured rows (**Stage 4 loads** into Stage 2 schema)
3. Graph of dependencies (**Stage 5 IMPLEMENTED**)
4. Documents with citeable chunks (`data/documents/acme` ready for Stage 6)

Only then does AI reason.

---

## End-to-end data flow (target)

```
Raw enterprise data
   ↓ parse
   ↓ validate          ← fail loudly on bad rows
   ↓ normalize         ← consistent tech names, IDs
   ↓ deduplicate
   ↓ enrich            ← derived fields
   ↓ store             ← PostgreSQL (system of record)  [schema IMPLEMENTED]
   ↓
Dependency graph (derived)
   ↓
Analytics engines (score / risk / cost / waves)
   ↓
Unstructured docs → chunk → embed → pgvector
   ↓
AI retrieval + recommendations (cite evidence)
   ↓
Approvals + audit events
```

**Today:** schema + ORM tests work; **synthetic Acme CSV/JSON/YAML + docs exist**. Not yet ingested into Postgres.

---

## Synthetic Acme dataset (Stage 3)

Location: `data/raw/acme/` and `data/documents/acme/`.

Includes applications, services, databases, APIs, infrastructure, dependencies, operational metrics, migration history, technology catalog, and intentional defects catalogued in `data_quality_defects.json` (`DQ-001`…`DQ-010`).

Load helpers: `app/synthetic/acme.py` (no pipeline yet).

---

## Implemented entities (Stage 2)

| Table | Role |
|-------|------|
| `projects` | Portfolio / engagement container |
| `applications` | Business applications |
| `services` | Deployable units |
| `database_assets` | Datastores (named to avoid `app.database` clash) |
| `api_assets` | APIs |
| `infrastructure_resources` | Queues, caches, hosts, etc. |
| `technologies` | Technology catalog |
| `dependencies` | Directed edges (type + external_id endpoints) |
| `documents` / `document_chunks` | Knowledge base (embeddings later) |
| `evidence` | Citeable evidence registry |
| `risks` | Risk records |
| `migration_recommendations` / `approvals` | Recommendations + HITL |
| `migration_waves` / `migration_wave_memberships` | Sequencing |
| `cost_estimates` | Cost bands + assumptions |
| `audit_events` | Governance trail |

Alembic revision: `d5df7dcba761_initial_enterprise_schema`.

---

## Structured vs unstructured data

| Kind | Examples | Where it lives |
|------|----------|----------------|
| Structured | application_id, criticality, size_gb | Relational tables **IMPLEMENTED** |
| Semi-structured | JSON/YAML inventories | Parsed into tables (Stage 4) |
| Unstructured | runbooks, policies | Document + chunk tables **IMPLEMENTED**; embeddings Stage 6 |

---

## Schemas

- **Pydantic schemas:** validate API payloads and future AI structured outputs — **IMPLEMENTED** for domain entities.
- **SQLAlchemy models:** persist concepts in PostgreSQL — **IMPLEMENTED**.
- **Alembic:** version database schema — **IMPLEMENTED** (initial migration).

---

## Referential integrity notes

- Strong FKs: project → applications → services/apis/databases; waves; recommendations → approvals.
- Dependencies use `source_asset_type` + `source_external_id` (and target equivalents). **Stage 4** detects orphan endpoints and rejects them from store while keeping the flexible graph reference design.

---

## Data quality (IMPLEMENTED Stages 3–4)

Stage 3 **intentionally** plants defects (DQ-001…DQ-010). Stage 4 measures completeness, uniqueness, validity, consistency, referential integrity, staleness, and conflicting metadata; writes `data/processed/acme/quality_report.json`; stores only clean inventory.

---

## Synthetic data honesty

Datasets represent a fictional company (Acme Financial Services): **SIMULATED**, not real customer data.

---

## Stage 1–4 components

| File | Role |
|------|------|
| `app/database/session.py` | Engine, session, readiness |
| `app/database/base.py` | Declarative Base |
| `app/models/*` | ORM entities |
| `app/schemas/*` | Pydantic contracts |
| `app/ingestion/*` | Parse / quality / normalize / store |
| `alembic/` | Migrations |
| `docker/docker-compose.yml` | `pgvector/pgvector:pg16` |

## Apply schema

```bash
alembic upgrade head
```

## Interview sound bite

> “Our data architecture treats PostgreSQL as system of record. Stage 2 locked the typed enterprise schema — applications, dependencies, evidence, recommendations — before any LLM feature. The LLM is not the database.”

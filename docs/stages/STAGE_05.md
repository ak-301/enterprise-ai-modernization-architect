# Stage 05 — Dependency Graph

## 1. Status

**COMPLETED**

Verified with unit + integration tests. Full suite expected **~51 pytest tests** when Stage 5 landed. NetworkX analyzes cleaned Acme inventory (file path or Postgres).

## 2. What are we building?

A **directed dependency graph** of portfolio assets with degree, betweenness centrality, depth, cycles, hubs, and migration bottlenecks.

## 3. Why are we building it?

Migration order depends on topology, not alphabetical sorting.

## 4. What problem does it solve?

LLM guessing dependencies instead of computing them from durable inventory edges.

## 5. Concepts I need to understand first

### Node / edge

**Simple:** A node is an asset (app, service, DB, API, infra). An edge is a dependency (calls, reads, writes, …).  
**Interview:** Edges come from Stage 4 clean inventory — not from the model inventing links.

### Degree

**Simple:** How many connections a node has.  
**Interview:** High **in-degree** means many systems depend on you (hard to move early).

### Centrality (betweenness)

**Simple:** How often a node sits on shortest paths between others.  
**Interview:** High betweenness ≈ migration bottleneck / blast-radius risk.

### Cycle

**Simple:** A loop in the graph (A depends on B depends on A).  
**Interview:** Acme Reporting ↔ Data Warehouse is an intentional cycle flagged in Stage 3/4 and detected here.

### Depth

**Simple:** How far a node sits from graph roots on the condensation DAG.  
**Interview:** Helps sequence waves later (Stage 10).

## 6. Technologies used

### NetworkX

- **What:** In-process Python graph library  
- **Why:** Enough for portfolio-scale synthetic data; deterministic; easy to test  
- **How:** `app/graph` builds a `DiGraph`, computes metrics, exports JSON

## 7. Architecture

```
Stage 4 clean inventory (files or PostgreSQL)
        ↓
nodes (type:external_id) + directed edges
        ↓
NetworkX DiGraph
        ↓
degree · betweenness · depth · cycles · hubs · bottlenecks
        ↓
GraphAnalysis (+ optional data/processed/acme/dependency_graph.json)
```

CLI: `python -m app.graph` (files) or `python -m app.graph --from-db`.

## 8. Implementation

Shipped:

1. `app/graph` package (builder, analysis, pipeline, CLI)
2. Build from cleaned Acme portfolio (reuses Stage 4 transforms) or from DB
3. Metrics: in/out/degree, betweenness, condensation depth
4. Application-level cycle detection (REPORT ↔ DWH)
5. Bottleneck / hub ranking; critical edge list
6. Unit tests + integration test (ingest then analyze from Postgres)

**Not shipped:** Neo4j, Streamlit visualization, wave planner (Stage 10).

## 9. Files

| Path | Responsibility |
|------|----------------|
| `app/graph/builder.py` | Build DiGraph from portfolio or DB |
| `app/graph/analysis.py` | Centrality, cycles, bottlenecks |
| `app/graph/pipeline.py` | Orchestration + JSON export |
| `app/graph/__main__.py` | CLI |
| `tests/unit/test_dependency_graph.py` | Graph unit tests |
| `tests/integration/test_dependency_graph_db.py` | DB-backed analysis |

## 10. Example

```python
from app.graph import analyze_acme_graph, graph_summary

analysis = analyze_acme_graph(write_report=True)
print(graph_summary(analysis))
# Identity Platform shows high in-degree; REPORT↔DWH appears in cycles
```

```bash
python -m app.graph
python -m app.graph --from-db --project-id PROJ-ACME-001
```

## 11. Failure scenarios

- Project missing in DB → `ValueError`  
- Empty inventory → empty analysis (0 nodes)  
- Cycles → reported, not “fixed” by inventing edges  
- Orphan deps already rejected in Stage 4 — not present in clean graph

## 12. How we handle failures

Prefer computed topology from stored edges; never invent missing dependencies. Cycles are first-class findings for humans / later wave rules.

## 13. Important engineering decisions

- Edge direction: source → target means source depends on / calls target (matches inventory)  
- Node keys: `asset_type:external_id` for heterogeneous graph  
- NetworkX in-process (ADR-011) — no graph DB yet  
- Depth via strongly connected component condensation so cycles don’t break topological depth

## 14. Alternatives

| Alternative | Why rejected (for now) |
|-------------|------------------------|
| Neo4j day one | Overkill for synthetic portfolio |
| Ask LLM for dependencies | Non-deterministic; not auditable |
| Skip graph stage | Waves and risk need topology |

## 15. What I learned

Dependency math belongs in code. Centrality and cycles are interview-defensible explanations for “migrate IDP late” and “Reporting/DWH are coupled.”

## 16. Interview questions

**Beginner**

1. What does Stage 5 produce?
2. Why not let the LLM list dependencies?

**Intermediate**

3. What does high in-degree mean for migration order?
4. How do you handle cycles?

**Advanced**

5. When would you move from NetworkX to a graph database?
6. How does this feed wave planning?

## 17. Interview answers

1. “A NetworkX graph plus metrics: hubs, bottlenecks, cycles, critical edges.”
2. “Dependencies are facts in inventory; guessing them is how plans invent coupling.”
3. “Many systems depend on you — moving you early cascades failures.”
4. “Detect and report them; compute depth on the condensation DAG.”
5. “When measured scale or multi-tenant query patterns outgrow in-process graphs.”
6. “Hubs/cycles become constraints for Stage 10 migration waves.”

## 18. 30-second explanation

“Stage 5 builds a NetworkX dependency graph from the clean Acme inventory. We compute degree and betweenness to find hubs and bottlenecks, detect cycles like Reporting ↔ Data Warehouse, and use that topology for later migration sequencing — not LLM guesswork.”

## 19. 2-minute explanation

“After Stage 4 loads validated assets and edges, Stage 5 turns them into a directed graph. Nodes are typed by asset class with business IDs; edges keep calls/reads/writes semantics. NetworkX gives us in-degree hubs like Identity Platform, betweenness bottlenecks, and cycles. That map is what makes migration order a graph problem: you don’t shut down a central transfer station first. Results export to JSON for demos and feed Stage 10 waves later.”

## 20. Deep-dive questions

- How do you prevent silent data corruption at this boundary?
- What metrics prove this stage works?
- What is the rollback story if this stage’s output is wrong?
- How does this interact with human approval and audit?

## 21. Production version

At real scale: snapshot graphs per analysis run, persist metrics tables, optional graph DB, auth on project scope, and visualization. This stage uses synthetic Acme data.

## 22. Stage summary

- Status: **COMPLETED**
- Goal: Graph + centrality + bottlenecks + cycles
- Why: Migration order is topology
- Key tech: NetworkX
- Next: Stage 6 Knowledge Base & RAG

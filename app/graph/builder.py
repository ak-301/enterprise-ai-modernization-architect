"""Build a NetworkX DiGraph from inventory + dependency records."""

from __future__ import annotations

from typing import Any

import networkx as nx
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.graph.models import GraphEdge, GraphNode
from app.ingestion.dedupe import dedupe_applications
from app.ingestion.enrich import enrich_applications, enrich_dependencies, filter_storeable
from app.ingestion.normalize import normalize_portfolio
from app.ingestion.parse import parse_acme_raw
from app.models import (
    ApiAsset,
    Application,
    DatabaseAsset,
    Dependency,
    InfrastructureResource,
    Project,
    Service,
)
from app.models.enums import AssetType


def node_key(asset_type: str | AssetType, external_id: str) -> str:
    kind = asset_type.value if isinstance(asset_type, AssetType) else str(asset_type)
    return f"{kind}:{external_id}"


def build_digraph(
    nodes: list[GraphNode],
    edges: list[GraphEdge],
) -> nx.DiGraph:
    """Create a directed graph; nodes without edges are still included."""
    graph = nx.DiGraph()
    for node in nodes:
        graph.add_node(
            node.key,
            asset_type=node.asset_type,
            external_id=node.external_id,
            name=node.name,
            criticality=node.criticality,
        )
    for edge in edges:
        if edge.source_key not in graph:
            graph.add_node(edge.source_key)
        if edge.target_key not in graph:
            graph.add_node(edge.target_key)
        graph.add_edge(
            edge.source_key,
            edge.target_key,
            dependency_type=edge.dependency_type,
            external_id=edge.external_id,
            criticality=edge.criticality,
            latency_ms=edge.latency_ms,
            traffic_per_day=edge.traffic_per_day,
        )
    return graph


def portfolio_to_graph_inputs(
    portfolio: dict[str, Any],
    *,
    project_external_id: str,
) -> tuple[list[GraphNode], list[GraphEdge]]:
    """Convert a Stage 4 storeable portfolio dict into graph nodes/edges."""
    nodes: list[GraphNode] = []
    for row in portfolio["applications"]:
        nodes.append(
            GraphNode(
                key=node_key("application", str(row["application_id"])),
                asset_type="application",
                external_id=str(row["application_id"]),
                name=str(row.get("application_name") or ""),
                criticality=str(row.get("criticality") or "") or None,
            )
        )
    for row in portfolio["services"]:
        nodes.append(
            GraphNode(
                key=node_key("service", str(row["service_id"])),
                asset_type="service",
                external_id=str(row["service_id"]),
                name=str(row.get("service_name") or ""),
            )
        )
    for row in portfolio["databases"]:
        nodes.append(
            GraphNode(
                key=node_key("database", str(row["database_id"])),
                asset_type="database",
                external_id=str(row["database_id"]),
                name=str(row.get("database_name") or ""),
                criticality=str(row.get("criticality") or "") or None,
            )
        )
    for row in portfolio["apis"]:
        nodes.append(
            GraphNode(
                key=node_key("api", str(row["api_id"])),
                asset_type="api",
                external_id=str(row["api_id"]),
                name=str(row.get("api_name") or ""),
            )
        )
    for row in portfolio["infrastructure"]:
        nodes.append(
            GraphNode(
                key=node_key("infrastructure", str(row["infrastructure_id"])),
                asset_type="infrastructure",
                external_id=str(row["infrastructure_id"]),
                name=str(row.get("name") or ""),
            )
        )

    edges: list[GraphEdge] = []
    for row in portfolio["dependencies"]:
        source_type = row["source_asset_type"]
        target_type = row["target_asset_type"]
        source_type_s = (
            source_type.value if isinstance(source_type, AssetType) else str(source_type)
        )
        target_type_s = (
            target_type.value if isinstance(target_type, AssetType) else str(target_type)
        )
        dep_type = row.get("dependency_type_enum") or row.get("dependency_type")
        dep_type_s = dep_type.value if hasattr(dep_type, "value") else str(dep_type)
        edges.append(
            GraphEdge(
                source_key=node_key(source_type_s, str(row["source_id"])),
                target_key=node_key(target_type_s, str(row["target_id"])),
                dependency_type=dep_type_s,
                external_id=str(row["dependency_id"]),
                criticality=str(row.get("criticality") or "") or None,
                latency_ms=int(row["latency_ms"]) if row.get("latency_ms") is not None else None,
                traffic_per_day=float(row["traffic_per_day"])
                if row.get("traffic_per_day") is not None
                else None,
            )
        )
    _ = project_external_id  # reserved for future multi-project labeling on nodes
    return nodes, edges


def load_clean_acme_portfolio() -> dict[str, Any]:
    """Run Stage 4 transforms without persisting; return storeable portfolio."""
    raw = parse_acme_raw()
    normalized = normalize_portfolio(raw)
    kept_apps, rejected_app_ids, _ = dedupe_applications(normalized["applications"])
    normalized["applications"] = enrich_applications(kept_apps)
    normalized["dependencies"] = enrich_dependencies(normalized["dependencies"])
    return filter_storeable(
        normalized,
        rejected_application_ids=set(rejected_app_ids),
    )


def build_acme_graph() -> tuple[nx.DiGraph, list[GraphNode], list[GraphEdge], str]:
    """Build graph from cleaned synthetic Acme inventory (no DB required)."""
    portfolio = load_clean_acme_portfolio()
    project_id = str(portfolio["project"]["external_id"])
    nodes, edges = portfolio_to_graph_inputs(portfolio, project_external_id=project_id)
    return build_digraph(nodes, edges), nodes, edges, project_id


def load_project_graph_from_db(
    session: Session,
    project_external_id: str,
) -> tuple[nx.DiGraph, list[GraphNode], list[GraphEdge]]:
    """Build graph from persisted Stage 2/4 inventory for one project."""
    project = session.scalar(
        select(Project).where(Project.external_id == project_external_id)
    )
    if project is None:
        raise ValueError(f"Project not found: {project_external_id}")

    nodes: list[GraphNode] = []
    apps = session.scalars(
        select(Application).where(Application.project_id == project.id)
    ).all()
    app_ids = [a.id for a in apps]
    for app in apps:
        nodes.append(
            GraphNode(
                key=node_key("application", app.external_id),
                asset_type="application",
                external_id=app.external_id,
                name=app.name,
                criticality=app.criticality.value,
            )
        )

    if app_ids:
        for svc in session.scalars(
            select(Service).where(Service.application_id.in_(app_ids))
        ).all():
            nodes.append(
                GraphNode(
                    key=node_key("service", svc.external_id),
                    asset_type="service",
                    external_id=svc.external_id,
                    name=svc.name,
                )
            )
        for db in session.scalars(
            select(DatabaseAsset).where(DatabaseAsset.application_id.in_(app_ids))
        ).all():
            nodes.append(
                GraphNode(
                    key=node_key("database", db.external_id),
                    asset_type="database",
                    external_id=db.external_id,
                    name=db.name,
                    criticality=db.criticality.value,
                )
            )
        for api in session.scalars(
            select(ApiAsset).where(ApiAsset.application_id.in_(app_ids))
        ).all():
            nodes.append(
                GraphNode(
                    key=node_key("api", api.external_id),
                    asset_type="api",
                    external_id=api.external_id,
                    name=api.name,
                )
            )

    for infra in session.scalars(
        select(InfrastructureResource).where(
            InfrastructureResource.project_id == project.id
        )
    ).all():
        nodes.append(
            GraphNode(
                key=node_key("infrastructure", infra.external_id),
                asset_type="infrastructure",
                external_id=infra.external_id,
                name=infra.name,
            )
        )

    edges: list[GraphEdge] = []
    for dep in session.scalars(
        select(Dependency).where(Dependency.project_id == project.id)
    ).all():
        edges.append(
            GraphEdge(
                source_key=node_key(dep.source_asset_type, dep.source_external_id),
                target_key=node_key(dep.target_asset_type, dep.target_external_id),
                dependency_type=dep.dependency_type.value,
                external_id=dep.external_id,
                criticality=dep.criticality.value,
                latency_ms=dep.latency_ms,
                traffic_per_day=dep.traffic_per_day,
            )
        )

    return build_digraph(nodes, edges), nodes, edges

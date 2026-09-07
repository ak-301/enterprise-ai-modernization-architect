"""Normalize aliases and empty values before persistence."""

from __future__ import annotations

from typing import Any

# Canonical labels for known alias families (DQ-004).
TECHNOLOGY_ALIASES: dict[str, str] = {
    "java": "Java",
    "Java": "Java",
    ".net": ".NET",
    ".NET": ".NET",
    "node.js": "Node.js",
    "Node.js": "Node.js",
    "python": "Python",
    "Python": "Python",
    "cobol": "COBOL",
    "COBOL": "COBOL",
    "vb6": "VB6",
    "VB6": "VB6",
}

DATABASE_TYPE_ALIASES: dict[str, str] = {
    "postgresql": "PostgreSQL",
    "postgres": "PostgreSQL",
    "PostgreSQL": "PostgreSQL",
    "Postgres": "PostgreSQL",
    "sql server": "SQL Server",
    "SQL Server": "SQL Server",
    "oracle": "Oracle",
    "Oracle": "Oracle",
    "mysql": "MySQL",
    "MySQL": "MySQL",
    "vsam/db2": "VSAM/DB2",
    "VSAM/DB2": "VSAM/DB2",
}


def _blank_to_none(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, str) and value.strip() == "":
        return None
    return value


def normalize_technology(value: Any) -> str | None:
    cleaned = _blank_to_none(value)
    if cleaned is None:
        return None
    text = str(cleaned).strip()
    return TECHNOLOGY_ALIASES.get(text, TECHNOLOGY_ALIASES.get(text.lower(), text))


def normalize_database_type(value: Any) -> str:
    text = str(value).strip()
    return DATABASE_TYPE_ALIASES.get(text, DATABASE_TYPE_ALIASES.get(text.lower(), text))


def normalize_portfolio(raw: dict[str, Any]) -> dict[str, Any]:
    """Return a shallow-copied portfolio with normalized enums/aliases."""
    apps = []
    for row in raw["applications"]:
        item = {k: _blank_to_none(v) for k, v in row.items()}
        item["technology"] = normalize_technology(item.get("technology"))
        if item.get("criticality"):
            item["criticality"] = str(item["criticality"]).strip().lower()
        if item.get("environment"):
            item["environment"] = str(item["environment"]).strip().lower()
        if item.get("deployment_model"):
            item["deployment_model"] = str(item["deployment_model"]).strip().lower()
        apps.append(item)

    services = []
    for row in raw["services"]:
        item = {k: _blank_to_none(v) for k, v in row.items()}
        if item.get("deployment_environment"):
            item["deployment_environment"] = str(item["deployment_environment"]).strip().lower()
        services.append(item)

    databases = []
    for row in raw["databases"]:
        item = {k: _blank_to_none(v) for k, v in row.items()}
        item["database_type"] = normalize_database_type(item.get("database_type"))
        if item.get("criticality"):
            item["criticality"] = str(item["criticality"]).strip().lower()
        if isinstance(item.get("contains_sensitive_data"), str):
            item["contains_sensitive_data"] = item["contains_sensitive_data"].strip().lower() in {
                "true",
                "1",
                "yes",
            }
        databases.append(item)

    deps = []
    for row in raw["dependencies"]:
        item = {k: _blank_to_none(v) for k, v in row.items()}
        if item.get("dependency_type"):
            item["dependency_type"] = str(item["dependency_type"]).strip().lower()
        if item.get("criticality"):
            item["criticality"] = str(item["criticality"]).strip().lower()
        deps.append(item)

    apis = [{k: _blank_to_none(v) for k, v in row.items()} for row in raw["apis"]]
    infrastructure = [
        {k: _blank_to_none(v) for k, v in row.items()} for row in raw["infrastructure"]
    ]

    return {
        **raw,
        "applications": apps,
        "services": services,
        "databases": databases,
        "apis": apis,
        "infrastructure": infrastructure,
        "dependencies": deps,
    }

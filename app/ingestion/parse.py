"""Parse Stage 3 synthetic Acme files into plain Python records."""

from __future__ import annotations

from typing import Any

import pandas as pd

from app.synthetic import acme as acme_loaders
from app.synthetic.acme import (
    assert_acme_dataset_present,
    load_applications,
    load_data_quality_defects,
    load_databases,
    load_dependencies,
    load_project_metadata,
    load_services,
    load_technology_catalog,
)


def _clean_value(value: Any) -> Any:
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    if isinstance(value, str) and value.strip() == "":
        return None
    return value


def _df_records(df: pd.DataFrame) -> list[dict[str, Any]]:
    """Convert a DataFrame to records with missing values → None."""
    records: list[dict[str, Any]] = []
    for raw in df.to_dict(orient="records"):
        records.append({key: _clean_value(val) for key, val in raw.items()})
    return records


def _load_csv(name: str) -> list[dict[str, Any]]:
    assert_acme_dataset_present()
    return _df_records(pd.read_csv(acme_loaders.ACME_RAW_DIR / name))


def parse_acme_raw() -> dict[str, Any]:
    """Load all Acme raw inventories into memory.

    Returns a dict of entity lists plus project metadata and the planted
    defect catalog (for evaluation, not as inventory rows).
    """
    assert_acme_dataset_present()
    return {
        "project": load_project_metadata(),
        "applications": _df_records(load_applications()),
        "services": _df_records(load_services()),
        "databases": _df_records(load_databases()),
        "apis": _load_csv("api_inventory.csv"),
        "infrastructure": _load_csv("infrastructure_inventory.csv"),
        "dependencies": _df_records(load_dependencies()),
        "operational_metrics": _load_csv("operational_metrics.csv"),
        "migration_history": _load_csv("migration_history.csv"),
        "technologies": list(load_technology_catalog().get("technologies") or []),
        "planted_defects": load_data_quality_defects(),
    }

"""Synthetic Acme Financial Services dataset accessors (Stage 3).

These helpers locate and load **synthetic** inventory files. They do not
implement the Stage 4 ingestion pipeline (validate/normalize/persist).
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import yaml

# Repository root: app/synthetic/acme.py -> parents[2]
REPO_ROOT = Path(__file__).resolve().parents[2]
ACME_RAW_DIR = REPO_ROOT / "data" / "raw" / "acme"
ACME_DOCS_DIR = REPO_ROOT / "data" / "documents" / "acme"

REQUIRED_RAW_FILES: tuple[str, ...] = (
    "project.json",
    "application_inventory.csv",
    "service_inventory.csv",
    "database_inventory.csv",
    "api_inventory.csv",
    "infrastructure_inventory.csv",
    "dependency_inventory.csv",
    "operational_metrics.csv",
    "migration_history.csv",
    "technology_catalog.yaml",
    "data_quality_defects.json",
    "README.md",
)


def assert_acme_dataset_present() -> None:
    """Raise FileNotFoundError if any required Acme raw file is missing."""
    missing = [name for name in REQUIRED_RAW_FILES if not (ACME_RAW_DIR / name).is_file()]
    if missing:
        raise FileNotFoundError(f"Missing Acme synthetic files under {ACME_RAW_DIR}: {missing}")


def load_project_metadata() -> dict:
    assert_acme_dataset_present()
    return json.loads((ACME_RAW_DIR / "project.json").read_text(encoding="utf-8"))


def load_applications() -> pd.DataFrame:
    assert_acme_dataset_present()
    return pd.read_csv(ACME_RAW_DIR / "application_inventory.csv")


def load_services() -> pd.DataFrame:
    assert_acme_dataset_present()
    return pd.read_csv(ACME_RAW_DIR / "service_inventory.csv")


def load_databases() -> pd.DataFrame:
    assert_acme_dataset_present()
    return pd.read_csv(ACME_RAW_DIR / "database_inventory.csv")


def load_dependencies() -> pd.DataFrame:
    assert_acme_dataset_present()
    return pd.read_csv(ACME_RAW_DIR / "dependency_inventory.csv")


def load_data_quality_defects() -> dict:
    assert_acme_dataset_present()
    return json.loads((ACME_RAW_DIR / "data_quality_defects.json").read_text(encoding="utf-8"))


def load_technology_catalog() -> dict:
    assert_acme_dataset_present()
    return yaml.safe_load((ACME_RAW_DIR / "technology_catalog.yaml").read_text(encoding="utf-8"))


def list_architecture_documents() -> list[Path]:
    """Return synthetic architecture/policy document paths."""
    if not ACME_DOCS_DIR.is_dir():
        return []
    return sorted(ACME_DOCS_DIR.glob("DOC-*.md"))


def portfolio_summary() -> dict[str, int]:
    """Simple counts for demos and tests (not quality scoring)."""
    return {
        "applications": len(load_applications()),
        "services": len(load_services()),
        "databases": len(load_databases()),
        "dependencies": len(load_dependencies()),
        "documented_defects": len(load_data_quality_defects().get("defects", [])),
        "architecture_documents": len(list_architecture_documents()),
    }

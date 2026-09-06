"""Tests for Stage 3 synthetic Acme enterprise datasets."""

from __future__ import annotations

import re

import pandas as pd
from app.synthetic.acme import (
    ACME_DOCS_DIR,
    ACME_RAW_DIR,
    assert_acme_dataset_present,
    list_architecture_documents,
    load_applications,
    load_data_quality_defects,
    load_databases,
    load_dependencies,
    load_project_metadata,
    load_services,
    load_technology_catalog,
    portfolio_summary,
)


def test_acme_files_present() -> None:
    assert_acme_dataset_present()
    assert ACME_RAW_DIR.is_dir()
    assert ACME_DOCS_DIR.is_dir()


def test_project_marked_synthetic() -> None:
    meta = load_project_metadata()
    assert meta["organization_name"] == "Acme Financial Services"
    assert meta["data_classification"] == "synthetic"
    assert meta["external_id"] == "PROJ-ACME-001"


def test_portfolio_minimum_sizes() -> None:
    summary = portfolio_summary()
    assert summary["applications"] >= 10
    assert summary["services"] >= 10
    assert summary["databases"] >= 8
    assert summary["dependencies"] >= 15
    assert summary["documented_defects"] >= 8
    assert summary["architecture_documents"] >= 5


def test_core_applications_exist() -> None:
    apps = load_applications()
    names = set(apps["application_name"].astype(str))
    for required in [
        "Customer Portal",
        "Loan Processing",
        "Payment Processing",
        "Risk Analytics",
        "Customer Notifications",
        "Reporting Platform",
        "Identity Platform",
        "Document Management",
        "Data Warehouse",
        "Legacy Mainframe Adapter",
    ]:
        assert required in names


def test_intentional_missing_owner() -> None:
    apps = load_applications()
    notify = apps.loc[apps["application_id"] == "APP-NOTIFY-001"].iloc[0]
    assert pd.isna(notify["owner"]) or str(notify["owner"]).strip() == ""


def test_intentional_duplicate_portal() -> None:
    apps = load_applications()
    ids = set(apps["application_id"].astype(str))
    assert "APP-PORTAL-001" in ids
    assert "APP-DUP-001" in ids


def test_intentional_invalid_version() -> None:
    apps = load_applications()
    loan = apps.loc[apps["application_id"] == "APP-LOAN-001"].iloc[0]
    assert str(loan["version"]) == "not-a-semver"


def test_intentional_orphan_service() -> None:
    apps = set(load_applications()["application_id"].astype(str))
    services = load_services()
    orphan = services.loc[services["service_id"] == "SVC-ORPHAN-001"].iloc[0]
    assert orphan["application_id"] not in apps


def test_intentional_orphan_dependency() -> None:
    apps = set(load_applications()["application_id"].astype(str))
    deps = load_dependencies()
    orphan = deps.loc[deps["dependency_id"] == "DEP-ORPHAN-001"].iloc[0]
    assert orphan["target_id"] not in apps


def test_intentional_missing_database_application() -> None:
    dbs = load_databases()
    row = dbs.loc[dbs["database_id"] == "DB-ORPHAN-001"].iloc[0]
    assert pd.isna(row["application_id"]) or str(row["application_id"]).strip() == ""


def test_inconsistent_database_type_aliases() -> None:
    dbs = load_databases()
    types = {str(t) for t in dbs["database_type"].dropna().unique()}
    # Intentional inconsistency across aliases
    assert "PostgreSQL" in types
    assert "Postgres" in types or "postgres" in types


def test_defect_catalog_covers_known_ids() -> None:
    catalog = load_data_quality_defects()
    ids = {d["id"] for d in catalog["defects"]}
    for required in ["DQ-001", "DQ-002", "DQ-003", "DQ-005", "DQ-006", "DQ-007"]:
        assert required in ids


def test_technology_catalog_loads() -> None:
    catalog = load_technology_catalog()
    assert "technologies" in catalog
    assert len(catalog["technologies"]) >= 5


def test_architecture_documents_have_evidence_ids() -> None:
    docs = list_architecture_documents()
    assert docs
    for path in docs:
        assert re.match(r"DOC-[A-Z]+-\d+\.md", path.name)
        text = path.read_text(encoding="utf-8")
        assert "SYNTHETIC" in text.upper()

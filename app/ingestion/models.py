"""Typed structures for Stage 4 pipeline results and quality reporting."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class QualityIssue:
    """One detected data-quality finding (often mapped to a planted DQ-ID)."""

    code: str
    dimension: str
    entity_type: str
    entity_id: str | None
    message: str
    severity: str = "error"
    planted_defect_id: str | None = None


@dataclass
class QualityReport:
    """Summary of completeness / uniqueness / validity / consistency / referential checks."""

    dataset: str
    issues: list[QualityIssue] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    rows_parsed: dict[str, int] = field(default_factory=dict)
    rows_rejected: dict[str, int] = field(default_factory=dict)
    rows_stored: dict[str, int] = field(default_factory=dict)

    @property
    def planted_defect_ids_detected(self) -> list[str]:
        ids = {
            issue.planted_defect_id
            for issue in self.issues
            if issue.planted_defect_id is not None
        }
        return sorted(ids)

    def to_dict(self) -> dict[str, Any]:
        return {
            "dataset": self.dataset,
            "metrics": self.metrics,
            "rows_parsed": self.rows_parsed,
            "rows_rejected": self.rows_rejected,
            "rows_stored": self.rows_stored,
            "planted_defect_ids_detected": self.planted_defect_ids_detected,
            "issue_count": len(self.issues),
            "issues": [
                {
                    "code": i.code,
                    "dimension": i.dimension,
                    "entity_type": i.entity_type,
                    "entity_id": i.entity_id,
                    "message": i.message,
                    "severity": i.severity,
                    "planted_defect_id": i.planted_defect_id,
                }
                for i in self.issues
            ],
        }


@dataclass
class PipelineResult:
    """Outcome of a full Acme ingestion run."""

    project_external_id: str
    quality_report: QualityReport
    stored: bool
    report_path: str | None = None

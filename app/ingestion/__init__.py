"""Stage 4 — Data Engineering Pipeline.

Public entrypoints for parsing, quality assessment, and Acme ingestion.
"""

from app.ingestion.models import PipelineResult, QualityIssue, QualityReport
from app.ingestion.pipeline import pipeline_summary, run_acme_pipeline
from app.ingestion.quality import assess_quality

__all__ = [
    "PipelineResult",
    "QualityIssue",
    "QualityReport",
    "assess_quality",
    "pipeline_summary",
    "run_acme_pipeline",
]

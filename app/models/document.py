"""Document and document-chunk models for the knowledge base."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.project import Project


class Document(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Enterprise document (policy, runbook, architecture overview, etc.)."""

    __tablename__ = "documents"
    __table_args__ = (
        UniqueConstraint("project_id", "external_id", name="uq_documents_project_external_id"),
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    external_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    doc_type: Mapped[str] = mapped_column(String(128), nullable=False)
    source_path: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    version: Mapped[str | None] = mapped_column(String(64), nullable=True)

    project: Mapped[Project] = relationship(back_populates="documents")
    chunks: Mapped[list[DocumentChunk]] = relationship(back_populates="document")


class DocumentChunk(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Citeable chunk used by RAG (embeddings added in Stage 6)."""

    __tablename__ = "document_chunks"
    __table_args__ = (
        UniqueConstraint("document_id", "chunk_index", name="uq_document_chunks_doc_index"),
        UniqueConstraint("evidence_id", name="uq_document_chunks_evidence_id"),
    )

    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    evidence_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    token_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # Embedding vector column is intentionally deferred to Stage 6 (pgvector).
    metadata_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    document: Mapped[Document] = relationship(back_populates="chunks")

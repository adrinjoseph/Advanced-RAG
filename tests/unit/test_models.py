from advanced_rag.db.base import Base
from advanced_rag.domain.models import Document, DocumentChunk


def test_document_tables_are_registered() -> None:
    assert "documents" in Base.metadata.tables
    assert "document_chunks" in Base.metadata.tables


def test_document_chunk_has_document_foreign_key() -> None:
    table = DocumentChunk.__table__
    foreign_keys = list(table.c.document_id.foreign_keys)

    assert len(foreign_keys) == 1
    assert foreign_keys[0].target_fullname == "documents.id"


def test_document_source_url_is_unique() -> None:
    table = Document.__table__
    assert table.c.source_url.unique is True

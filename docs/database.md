# Database

PostgreSQL with SQLAlchemy 2.x ORM and Alembic migrations stores document metadata and chunk text. Vectors live in Pinecone; the BM25 index is built in memory from the stored chunks.

## What exists

| Item | Status |
|---|---|
| ORM models `Document` and `DocumentChunk` | Present in the repository |
| Migration `796e242168ef_create_document_tables.py` | Present in the repository |

This file does not list columns, because they must come from the real code. Fill the table sections below from the actual models after the audit, using the commands in the next section. Preserve the existing migration history; do not delete or recreate it.

## Inspecting the real schema

```bash
python -m alembic heads
python -m alembic history
```

Print what the ORM defines (run from the repo root with the venv active; adjust the import path to where `Base` lives):

```python
from advanced_rag.db import models  # adjust to the actual module

base = models.Base  # adjust if the declarative base is named differently
for name, table in base.metadata.tables.items():
    print(name)
    for col in table.columns:
        print(
            "  ",
            col.name,
            col.type,
            "PK" if col.primary_key else "",
            "NULL" if col.nullable else "NOT NULL",
        )
```

And against a real database, in `psql`: `\d <table_name>`.

## Table definitions (to fill from the models)

| Table | Column | Type | Constraints | Purpose |
|---|---|---|---|---|
| | | | | |

## Relationships and constraints

Verify against the models; this is the target design:

- Each chunk belongs to exactly one document (foreign key from chunk to document).
- Chunks are ordered within a document and uniquely identified (for example, a unique pair of document and chunk index, plus a stable chunk ID).
- Duplicate documents are prevented by a unique content hash or source identity.
- Indexes support the real lookups: chunks by document, documents by hash, chunks by stable ID.

## Session lifecycle

FastAPI provides a database session through a dependency: one session per request, committed on success and rolled back on error, then closed. Ingestion uses one transaction per document, so a document and its chunks are stored together or not at all.

## Document and chunk persistence

Ingestion writes the document row and its chunk rows (text, ordering, metadata, hashes) in one transaction. Only after the commit does it embed and upsert vectors to Pinecone. Failure between commit and indexing leaves chunks that are stored but not indexed; the design must let those be detected and retried ([architecture](architecture.md)).

## Content hashes and duplicate detection

- **Document hash:** identifies exact content, so re-ingesting unchanged content is skipped.
- **Chunk hash:** identifies unchanged chunks, so only changed chunks are re-embedded.
- Same hash is a duplicate; a different hash for the same source is a new version ([data sources](data-sources.md)).

## Migration history

| Revision | Description |
|---|---|
| `796e242168ef` | Create document tables |

Add new revisions only for real schema changes, review them with the code, and test them against a scratch database. Never apply a migration to a real database without deciding to.

## Planned schema changes (not implemented)

These are candidates, each to be added only when needed:

- An indexing state per document or chunk (for example pending, indexed, failed) to support recovery.
- Recording the embedding model identifier used for each indexed chunk.
- Version and effective-date fields, if the current models lack them.
- Ingestion run or error records.

Related: [Architecture](architecture.md) · [Development setup](development-setup.md)

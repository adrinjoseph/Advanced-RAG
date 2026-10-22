# Chunking and Indexing

Status: **Planned**. No chunk size, embedding model or index configuration has been chosen.

## Parsing and normalization

- Extract text and structure from PDF or HTML; keep headings, section numbers and list nesting where possible.
- Normalize whitespace, hyphenation and Unicode forms consistently; remove repeated headers/footers and page numbers.
- Record parser name and version in the document metadata, since parser changes alter chunks.
- Scanned or table-heavy pages need explicit handling (OCR or manual extraction) and are flagged as lower-confidence. **Needs verification** against the real documents.

## Chunk boundaries

Chunk along legal structure first (part, chapter, section, sub-section, clause), and fall back to size limits only inside long units. Keep the section path (for example, `Act > Chapter > Section > Sub-section`) with every chunk, so a retrieved passage can be located and cited.

## Size and overlap trade-offs

| Choice | Benefit | Cost |
|---|---|---|
| Smaller chunks | Precise matches, less noise | Lost context, more chunks |
| Larger chunks | More context per hit | Diluted embeddings, wasted prompt budget |
| More overlap | Fewer split-clause misses | Duplicates, more storage |
| Less overlap | Compact index | Boundary misses |

Final values are decided by evaluation, not by intuition ([benchmarking](benchmarking.md)).

## Metadata (proposed)

| Field | Purpose |
|---|---|
| `chunk_id` | Stable identifier |
| `document_id`, `document_version` | Provenance and versioning |
| `source_url`, `retrieved_at` | Traceability |
| `section_path` | Citation and display |
| `effective_from`, `effective_to` | Temporal filtering |
| `document_type` | Act, rule, notification, FAQ |
| `content_hash` | Change and duplicate detection |
| `access_scope` | Access filtering |
| `embedding_model` | Consistency guard |

Metadata stored in Pinecone is limited to what filtering and display need; the full record lives in PostgreSQL ([database](database.md)).

## Stable identifiers and hashes

`chunk_id` is derived deterministically from document ID, version and section path (plus a position index for split sections), so re-ingesting the same source produces the same IDs. `content_hash` is a hash of normalized chunk text. Identical hashes mean unchanged content (skip re-embedding); duplicate hashes across documents are flagged for review rather than silently dropped.

## Index updates and deletion

- **New document:** ingest, embed, upsert, record in PostgreSQL.
- **Changed content:** new chunk hashes mean re-embed and upsert; chunks that disappeared are deleted from Pinecone and marked in PostgreSQL.
- **Removed document:** delete its vectors by `document_id` filter and mark it inactive.
- **BM25:** rebuilt from the current chunk set after any change.
- Ingestion is repeatable and idempotent; a run records what it added, changed and removed. Reconciliation compares PostgreSQL chunk records with Pinecone IDs.

## Embedding model consistency

One embedding model per Pinecone index. The model name and version are stored in metadata and configuration. Changing the model means creating a new index and re-embedding everything, never mixing vectors.

## Amendments and historical versions

Each version of a provision is a separate document version with its own effective dates. Older versions are kept for historical queries but are excluded from "current law" queries by metadata filter. Mixed-version retrieval is a known failure mode ([limitations](limitations.md), [generation](generation-and-citations.md)).

## Dataset manifest

The verified source list (target: roughly 10-20 documents or sections) is recorded in `data/manifests/` with URL, title, version, effective date, retrieval date and hash. Candidate portals are listed in the [README](../README.md).

Related: [Data flow](data-flow.md) · [Retrieval](retrieval.md)

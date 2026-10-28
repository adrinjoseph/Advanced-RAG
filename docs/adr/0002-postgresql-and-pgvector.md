# ADR 0002: PostgreSQL and pgvector as the single store

**Status:** Proposed

## Context
The system needs vector search, full-text search, relational metadata, transactional ingestion and SQL filtering on document status and dates. Pinecone is excluded by project constraints. No GPU, local-first.

## Decision
Store documents, chunks, embeddings (`pgvector`, HNSW, cosine) and `tsvector` (GIN) in one PostgreSQL database.

## Alternatives considered
- **Dedicated vector DB (Chroma, Qdrant, etc.):** strong vector features, but a second system to keep consistent with metadata and no native SQL full-text ranking.
- **Elasticsearch/OpenSearch:** excellent lexical search and BM25, heavy to run locally, separate vector story.
- **SQLite + extensions:** light, but weaker concurrency and extension maturity on this stack.

## Benefits
One transactional store (a document and its vectors commit atomically); SQL filters applied in the same query; fewer components; skills transfer to production Postgres.

## Costs and trade-offs
You tune indexes yourself; approximate-index plus selective-filter behavior needs care ([database.md](../database.md#4-indexes)); pgvector must be installed on native Windows (OD-5); HNSW dimension limits; ranking is `ts_rank_cd`, not BM25.

## Consequences
Schema owned by Alembic; embedding dimension is a schema decision; DB roles split for ingest/serve.

## Revisit if
Corpus size or query volume outgrows a single Postgres; filtered-search recall is unacceptable after tuning; true BM25 proves necessary and not achievable in-database.

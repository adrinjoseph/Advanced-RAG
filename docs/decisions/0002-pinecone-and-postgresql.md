# 0002: Pinecone for Vectors, PostgreSQL for Application Data

**Status:** Accepted

## Context
The system needs a vector index and durable relational storage for users, sessions, messages and document metadata.

## Decision
Pinecone is responsible for dense vector retrieval. PostgreSQL 16, accessed through SQLAlchemy with Alembic migrations, is responsible for application persistence. Original files are intended to live in AWS S3.

## Alternatives considered
- **pgvector in PostgreSQL:** fewer moving parts, but not the chosen design.
- **PostgreSQL full-text search instead of BM25:** not chosen; BM25 via `rank_bm25` is the initial lexical retriever.
- **Other managed or self-hosted vector databases.**

## Trade-offs
Two data stores must stay consistent; Pinecone is a hosted dependency with cost and latency. In return, each store does the job it is built for and retrieval is independent of application schema changes.

## Consequences
Stable chunk IDs and content hashes tie Pinecone vectors to PostgreSQL rows ([chunking](../chunking-and-indexing.md)). A reconciliation process is needed. Credentials and quotas must be managed ([configuration](../configuration.md)).

## Revisit if
Pinecone cost, latency or availability becomes a problem, or consistency issues between stores prove costly.

# ADR 0007: Asynchronous database access

**Status:** Proposed

## Context
Each query does several I/O waits: embedding call, two DB searches, LLM call. FastAPI is async.

## Decision
Use SQLAlchemy 2.x async with `asyncpg` for the serving path; run dense and lexical queries concurrently. Ingestion CLI may use synchronous code for CPU-bound parsing. `asyncpg` compatibility with Python 3.14 **[Verify]**.

## Alternatives considered
- **Synchronous SQLAlchemy + psycopg:** simpler; blocks workers or needs thread pools.
- **psycopg 3 async:** viable alternative if `asyncpg` lacks 3.14 support.
- **Raw SQL without ORM:** more control, less structure; vector/FTS queries may still use `text()` or Core.

## Benefits
Concurrent I/O, better throughput per worker, consistent with the async API.

## Costs and trade-offs
Async debugging and testing complexity; lazy-loading pitfalls; pgvector adapter registration with the driver; a connection pool to size.

## Consequences
Tests use async fixtures; no blocking calls in handlers ([architecture.md](../architecture.md#8-async-execution-boundaries)).

## Revisit if
`asyncpg` or pgvector support is unavailable on Python 3.14, or concurrency gains are unmeasurable.

# Project Specification — Advanced-RAG

> **Status:** Source of truth for requirements. Everything below is **[Proposed]** unless the [README status table](../README.md#implementation-status) says **[Implemented]**. Other documents link here instead of restating requirements.

**Status tags used across the docs**

| Tag | Meaning |
|---|---|
| **[Proposed]** | Design decision made on paper; not yet confirmed by the owner or built. |
| **[Planned]** | Accepted for a later phase; no work started. |
| **[Implemented]** | Code exists, and is tested. Only the README status table may promote something to this tag. |
| **[Verify]** | A compatibility or factual claim that must be checked before relying on it. |

## 1. Problem statement

Indian tax and regulatory material is spread across long statutes, rules, circulars, notifications and amendments. Users describe concepts in everyday words, or search for exact identifiers (section numbers, form names). Keyword search misses paraphrases; vector search misses exact identifiers; an LLM without retrieval invents plausible but unsupported answers.

Advanced-RAG retrieves evidence from curated official documents using **two complementary retrieval methods**, generates an answer constrained to that evidence, returns **verifiable citations**, and **abstains** when evidence is insufficient.

It is a research aid. It is **not** legal or tax advice, and RAG does not eliminate hallucination; it reduces and makes it detectable. See [grounding-and-abstention.md](grounding-and-abstention.md).

## 2. Users

- People researching Indian tax and regulatory information.
- Engineers studying evidence-grounded RAG.
- Technical reviewers evaluating architecture and reliability.

## 3. Scope

**In scope:** ingestion of curated official documents; hybrid retrieval; structured grounded generation; citation validation; abstention; REST API; Chainlit UI; evaluation harness; tests; observability; documentation.

**Out of scope:** legal conclusions; user accounts and multi-tenancy; ingestion of arbitrary web content; fine-tuning; agents; any claim of legal authority.

## 4. Functional requirements

### Ingestion (see [ingestion.md](ingestion.md))
| ID | Requirement | Phase |
|---|---|---|
| FR-ING-1 | Accept PDF files from approved local paths, each with a metadata manifest (source type, title, reference, publication date, effective date, optional source URL). | 1 |
| FR-ING-2 | Extract text with page numbers; normalize and clean. | 1 |
| FR-ING-3 | Chunk into retrieval units preserving document identity, page span and section path. | 1 |
| FR-ING-4 | Embed chunks in batches; store embedding model name and dimension per chunk. | 1 |
| FR-ING-5 | Persist documents, chunks, embeddings and `tsvector` in PostgreSQL. | 1 |
| FR-ING-6 | Be idempotent: re-running on unchanged input changes nothing. | 1 |
| FR-ING-7 | Record failures per document in `ingestion_runs`; one bad document never aborts a batch. | 1 |
| FR-ING-8 | Support document updates via versioning and supersession, never silent overwrite. | 1 |

### Question answering (see [data-flow.md](data-flow.md))
| ID | Requirement | Phase |
|---|---|---|
| FR-QA-1 | Validate and normalize the request. | 1 |
| FR-QA-2 | Embed the query; run dense retrieval (cosine, HNSW). | 1 |
| FR-QA-3 | Run lexical retrieval (PostgreSQL full-text search, `ts_rank_cd`). | 1 |
| FR-QA-4 | Fuse rankings with Reciprocal Rank Fusion. | 1 |
| FR-QA-5 | Apply metadata filters (document status, effective-date window, source type). | 1 |
| FR-QA-6 | Build a bounded, delimited evidence context. | 1 |
| FR-QA-7 | Generate a structured answer (Pydantic v2 schema via Instructor). | 1 |
| FR-QA-8 | Validate citations (existence, membership in retrieved set, quote anchoring). | 1 |
| FR-QA-9 | Apply sufficiency rules and abstain when required. | 1 |
| FR-QA-10 | Return answer, citations, evidence metadata or an abstention with reason. | 1 |
| FR-QA-11 | Rerank candidates. | **Optional**, only if evaluation shows gain |
| FR-QA-12 | Stream via SSE. | 3 |

### Phases
1. **Core:** ingestion CLI, query API, evaluation harness, structured logs.
2. **Experience and visibility:** Chainlit UI, Langfuse tracing.
3. **Scale-out:** Redis caching, SSE, optional reranking, AWS deployment options.

## 5. Non-functional requirements

| ID | Requirement |
|---|---|
| NFR-1 | **Traceability:** every returned citation resolves to a stored chunk, document, page span and document version. |
| NFR-2 | **Reproducibility:** evaluation runs are deterministic given pinned config, corpus version and recorded provider outputs. |
| NFR-3 | **Safety:** retrieved text is treated as untrusted data ([security.md](security.md)). |
| NFR-4 | **Provider isolation:** LLM and embedding providers sit behind interfaces; names/models come from config. |
| NFR-5 | **Privacy:** telemetry excludes raw queries and document text by default ([observability.md](observability.md)). |
| NFR-6 | **Local-first:** full development without paid cloud services ([ADR 0006](adr/0006-local-first-development.md)). |
| NFR-7 | **Latency and cost targets** are set only after a measured baseline exists. No number is claimed here. |

## 6. System boundaries

Inside: ingestion pipeline, retrieval service, generation service, grounding validator, API, UI, evaluation harness, PostgreSQL schema.
Outside: the LLM provider, the embedding provider, official document publishers, Redis/Langfuse infrastructure. Treated as replaceable dependencies.

## 7. Technology baseline

| Area | Choice | Status |
|---|---|---|
| Language | Python 3.14.6, venv, native Windows 11, Git Bash | **[Verify]** library compatibility |
| API | FastAPI, Pydantic v2 | **[Proposed]**, **[Verify]** |
| DB | PostgreSQL, `pgvector`, `tsvector` + GIN | **[Proposed]**, **[Verify]** pgvector on native Windows |
| ORM / driver | SQLAlchemy 2.x async, `asyncpg`, Alembic | **[Proposed]**, **[Verify]** `asyncpg` on 3.14 |
| Retrieval | Dense + PostgreSQL FTS + RRF | **[Proposed]** |
| Generation | Instructor + Pydantic v2 | **[Proposed]**, **[Verify]** |
| UI | Chainlit | **[Planned]**, **[Verify]** |
| Cache | Redis | **[Planned]** |
| Tracing | Langfuse (self-hosted via Docker Compose) | **[Planned]** |
| Quality | pytest, Ruff, GitHub Actions | **[Proposed]** |
| LLM / embedding provider, models, dimension | **Not chosen** | Open decision OD-1 |

## 8. Constraints

Local-first; Windows 11 + Git Bash; no GPU; no paid cloud without a cost estimate and explicit approval; Docker Compose only for supporting services (Redis, Langfuse), not for the app or the primary database.

## 9. Explicit exclusions

No Pinecone. No LangChain. No LangGraph. No technology added for appearance. No assumed provider.

## 10. Acceptance criteria

Criteria are testable statements; numeric quality targets are set after the first baseline report ([evaluation.md](evaluation.md)).

1. Re-ingesting an unchanged corpus produces zero new rows (idempotency test).
2. Every `answered` response has at least one claim, every claim has at least one citation, every cited chunk ID is in the retrieved set, and every supporting quote is a normalized substring of its cited chunk.
3. A response with an invalid citation is never returned as `answered`; it is retried once, then converted to an abstention.
4. A question with no relevant evidence in the corpus yields `abstained` with a reason code.
5. The evaluation harness emits a report containing Hit@K, Recall@K, MRR and nDCG@K for dense-only, lexical-only and hybrid configurations on the same golden set.
6. Tests run with mocked providers and no network access.
7. No secret appears in the repository, logs or traces.

## 11. Open decisions

| ID | Decision | Blocks |
|---|---|---|
| OD-1 | LLM provider/model; embedding provider/model; embedding dimension | `database.md` column type, `.env` |
| OD-2 | PDF parsing library (license, layout fidelity, Python 3.14 support) | ingestion |
| OD-3 | Lexical text-search configuration (`english` vs `simple` vs custom) for legal identifiers such as "80C" | retrieval quality |
| OD-4 | True BM25 (extension or application-side) vs `ts_rank_cd` only | [ADR 0003](adr/0003-hybrid-retrieval-and-rrf.md) |
| OD-5 | pgvector installation route on native Windows | development setup |
| OD-6 | Chunk size, overlap and structure-aware splitting rules | tuned by evaluation |
| OD-7 | Abstention thresholds | calibrated on golden set |
| OD-8 | Which official sources form the first corpus | [data-sources.md](data-sources.md) |

## 12. Canonical names

Ingestion Pipeline · Retrieval Service · Evidence Context Builder · Generation Service · Grounding Validator · Embedding Client · LLM Client · API (FastAPI app) · Chainlit UI · Evaluation Harness · Corpus Version. Definitions: [glossary.md](glossary.md).

---
Next: [architecture.md](architecture.md)

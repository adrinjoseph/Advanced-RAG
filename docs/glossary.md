# Glossary

Canonical vocabulary for Advanced-RAG. Status tags are explained in the [specification](project-specification.md).

| Term | Definition |
|---|---|
| **Abstention** | A valid response declining to answer, with a reason code, when evidence is insufficient, conflicting, out of scope, or ungrounded. See [grounding-and-abstention.md](grounding-and-abstention.md). |
| **ADR** | Architecture Decision Record. See [adr/README.md](adr/README.md). |
| **Answer draft** | The LLM's structured output before validation. |
| **BM25** | A lexical ranking function using term frequency saturation, IDF and length normalization. **Not** what `ts_rank_cd` computes. |
| **Chunk** | A retrieval unit of document text with page span, section path and a deterministic `chunk_key`. |
| **chunk_key** | Deterministic hash identifying a chunk across re-runs; basis of idempotent writes. |
| **Citation** | A `chunk_id` plus a verbatim quote attached to a claim. |
| **Claim** | One assertion in an answer, each with at least one citation. |
| **Content hash** | `sha256` of a file's raw bytes, used for duplicate detection. |
| **Corpus Version** | Counter incremented on every committed ingestion change; used for cache correctness. |
| **Cosine distance** | `1 - cosine similarity`; pgvector operator `<=>`. |
| **Dense retrieval** | Nearest-neighbour search over embedding vectors. |
| **Effective date** | When a document's provisions apply (distinct from publication date). |
| **Embedding** | A fixed-length numeric vector representing text meaning. |
| **Evidence context** | The bounded, delimited set of chunks passed to the LLM. |
| **Golden dataset** | Labeled questions with relevant chunks and expected status, used for evaluation. |
| **Grounding** | Whether claims are supported by the cited evidence. Five levels are distinguished in [grounding-and-abstention.md](grounding-and-abstention.md). |
| **GIN index** | PostgreSQL index type used for `tsvector` full-text search. |
| **HNSW** | Hierarchical Navigable Small World graph index; approximate nearest-neighbour search in pgvector. |
| **Hit@K** | Fraction of queries with at least one relevant item in the top K. |
| **Ingestion Pipeline** | Offline workflow that turns documents into stored, searchable chunks. |
| **Instructor** | Library for obtaining Pydantic-validated structured LLM output. |
| **Lexical retrieval** | Term-matching search; here PostgreSQL full-text search with `ts_rank_cd`. |
| **MRR** | Mean Reciprocal Rank of the first relevant result. |
| **nDCG@K** | Normalized Discounted Cumulative Gain; rewards graded-relevant items ranked higher. |
| **pgvector** | PostgreSQL extension for vector storage and similarity search. |
| **Prompt injection** | Attacker-controlled text trying to override the model's instructions; a risk in retrieved documents. |
| **Quote anchoring** | Check that a citation's quote is a normalized substring of the cited chunk. |
| **Recall@K** | Fraction of all relevant items found in the top K. |
| **Reranking** | Re-scoring top candidates with a stronger model; optional here. |
| **RRF** | Reciprocal Rank Fusion: `Σ 1/(k + rank)` across ranked lists. See [retrieval.md](retrieval.md#rrf). |
| **Superseded** | Document status when a newer version replaces it. |
| **`ts_rank_cd`** | PostgreSQL cover-density text-search ranking function. |
| **tsvector / tsquery** | PostgreSQL types for preprocessed document text and search queries. |

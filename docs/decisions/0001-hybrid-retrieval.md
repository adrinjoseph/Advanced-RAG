# 0001: Hybrid Retrieval

**Status:** Accepted (baseline design; effectiveness is to be measured)

## Context
The corpus has exact identifiers (section numbers, form names) and natural-language questions. Lexical search handles the first well; dense search handles paraphrase better. Neither alone is expected to cover both.

## Decision
Retrieve candidates with BM25 (`rank_bm25`) and Pinecone dense search, merge with Reciprocal Rank Fusion, and optionally rerank the fused list with a BGE cross-encoder or Cohere Rerank.

## Alternatives considered
- **Dense only:** simpler, but weak on exact identifiers.
- **BM25 only:** strong on terms, weak on paraphrase.
- **Weighted score fusion:** needs score normalization across incompatible scales; RRF uses ranks only.
- **pgvector or PostgreSQL full-text search as primary retrieval:** not chosen for this project.

## Trade-offs
More components, more latency and more tuning parameters than a single retriever. BM25 via `rank_bm25` is in-memory and per process.

## Consequences
Evaluation must compare BM25-only, dense-only, hybrid and hybrid plus rerank on the same data. Reranking stays optional until it shows a measured benefit worth its latency and cost.

## Revisit if
Hybrid shows no meaningful gain over the best single retriever, the BM25 index becomes a scaling problem, or reranking cost outweighs its gain.

See [Retrieval](../retrieval.md).

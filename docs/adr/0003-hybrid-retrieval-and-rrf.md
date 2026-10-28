# ADR 0003: Hybrid retrieval with Reciprocal Rank Fusion

**Status:** Proposed

## Context
Users ask both conceptual questions and exact-identifier questions over legal text. Dense search misses exact terms; lexical search misses paraphrase.

## Decision
Run dense retrieval and PostgreSQL full-text retrieval (`ts_rank_cd`) in parallel, fuse with RRF (`k = 60` as a starting value). Reranking is optional and gated on measured gain. The lexical leg is **not** called BM25.

## Alternatives considered
- **Dense only:** simplest; weak on identifiers.
- **Lexical only:** weak on paraphrase.
- **Weighted score fusion:** needs score normalization across incomparable scales; brittle.
- **Cross-encoder reranking as baseline:** extra latency and dependency on CPU-only hardware before it is shown to help.
- **True BM25 (extension or app-side):** possible upgrade (OD-4).

## Benefits
Complementary recall; RRF needs no score normalization and has one main parameter; easy to explain and ablate.

## Costs and trade-offs
Two queries per request; `N`, `M`, `k` need tuning; `ts_rank_cd` lacks IDF-based BM25 behavior; text-search config affects identifiers (OD-3).

## Consequences
Evaluation must include dense-only, lexical-only and hybrid ablations ([evaluation.md](../evaluation.md)).

## Revisit if
Ablations show hybrid does not beat the best single method; a BM25 implementation measurably improves results; reranking shows a worthwhile gain.

# ADR 0008: Evaluation-driven quality

**Status:** Proposed

## Context
RAG quality is easy to claim and hard to verify; tunable parameters (chunking, `k`, `N`, thresholds, reranking) invite guesswork.

## Decision
Every quality-affecting change is justified by the Evaluation Harness on a golden dataset with dev/test split, retrieval and answer metrics, and ablations. Features such as reranking and true BM25 are adopted only with measured gain. No metric is reported without a reproducible run.

## Alternatives considered
- **Manual spot checks only:** fast, not reproducible.
- **Only LLM-judge metrics:** judge bias, circularity.
- **Public benchmarks:** do not represent Indian tax documents.

## Benefits
Defensible decisions, regression detection, honest portfolio claims.

## Costs and trade-offs
Labeling effort; small datasets give wide uncertainty; judge calls cost money.

## Consequences
Golden dataset is a first-class artifact; CI runs a small smoke evaluation ([evaluation.md](../evaluation.md), [testing.md](../testing.md)).

## Revisit if
The dataset cannot be built at adequate size, or evaluation cost exceeds its value.

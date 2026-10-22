# 0004: Evaluation-First Development

**Status:** Accepted

## Context
RAG systems are easy to make look good in demos and hard to make reliably good. Added components (hybrid, reranking, agents) cost latency and money and should earn their place.

## Decision
Build a labelled evaluation dataset and metric harness early, run a baseline before adding components, and accept changes only when measured results justify them. RAGAS is a required part of the evaluation framework, alongside custom retrieval, citation, grounding, abstention and authorization checks.

## Alternatives considered
- **Evaluate at the end:** risks building unmeasured complexity.
- **Manual spot checks only:** not reproducible or regression-safe.
- **RAGAS only:** LLM-judged scores alone are not enough for retrieval ranking or access control.

## Trade-offs
Up-front effort to label data; a small dataset gives noisy estimates; LLM-judge metrics cost money and have bias.

## Consequences
Evaluation code is part of the main package, datasets are versioned, and results are reported with full configuration ([benchmarking](../benchmarking.md)).

## Revisit if
The dataset proves too small to discriminate between methods, or judge metrics prove unreliable for this domain.

See [Evaluation](../evaluation.md).

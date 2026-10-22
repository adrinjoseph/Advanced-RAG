# Benchmarking

Status: **Planned**. All result tables below are empty templates; no results exist.

## Baselines

| ID | Configuration |
|---|---|
| B0 | BM25 only |
| B1 | Dense only |
| B2 | Hybrid (BM25 + dense + RRF) |
| B3 | Hybrid + reranker |
| B4 | Best retrieval + generation, full pipeline |

## Controlled variables

Hold constant when comparing: corpus and manifest version, chunking, embedding model, labelled dataset version, K values, LLM and temperature, prompt. Change one thing per experiment.

## Cutoffs

Report retrieval metrics at fixed K (for example 5 and 10 as proposed starting points) and state the candidate pool sizes (`bm25_top_k`, `dense_top_k`, `rerank_top_n`).

## Configuration record

Every run stores: commit hash, dataset and manifest versions, parser and chunking settings, embedding model, Pinecone index settings, BM25 settings, RRF `k`, reranker, LLM provider/model/parameters, RAGAS judge model, seeds, hardware and run date.

## Repeated runs

Retrieval with deterministic components is repeatable; LLM-based generation and judging are not. Repeat those runs several times and report mean and spread. Do not claim differences smaller than the observed variance.

## Latency and cost

Measure per stage (BM25, embedding, Pinecone, fusion, rerank, generation) with p50 and p95 over a stated number of queries, warm and cold. Track tokens and API cost per query and per evaluation run ([performance-and-cost](performance-and-cost.md)).

## Result templates

**Retrieval**

| Config | Queries | Hit@5 | Recall@10 | MRR | nDCG@10 |
|---|---|---|---|---|---|
| B0 | | | | | |
| B1 | | | | | |
| B2 | | | | | |
| B3 | | | | | |

**Generation**

| Config | Faithfulness | Answer relevancy | Context precision | Context recall | Citation correctness | Abstention correctness |
|---|---|---|---|---|---|---|
| B4 | | | | | | |

**Cost and latency**

| Config | p50 (ms) | p95 (ms) | Tokens/query | Cost/query |
|---|---|---|---|---|
| B2 | | | | |
| B3 | | | | |

## Acceptance criteria for a change

A proposed improvement is accepted only if it (1) improves the target metric beyond observed noise, (2) does not regress any query category or the abstention and authorization checks, (3) keeps latency and cost within stated budgets, and (4) is reproducible from the recorded configuration. Otherwise it is rejected or deferred, and the finding is noted.

Related: [Evaluation](evaluation.md) · [Retrieval](retrieval.md)

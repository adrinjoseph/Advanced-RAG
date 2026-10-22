# Performance and Cost

Status: **Planned**. Everything below is a measurement plan. No benchmarks exist.

## What to measure

| Area | Measure |
|---|---|
| Retrieval latency | BM25, Pinecone query, fusion |
| Embedding latency | Per query and per ingestion batch |
| Reranking | Added latency and cost per query |
| Generation | Time to first token, total time |
| Tokens | Prompt and completion tokens per query |
| Services | Pinecone, LLM, reranker and S3 charges |
| End to end | p50 and p95 per request |
| Capacity | Throughput and behaviour under concurrency |

p50 is the typical request; p95 shows the slow tail. Report both, with sample size and warm/cold state.

## Quality, latency and cost trade-offs

Larger candidate pools, reranking and bigger context improve recall but increase latency and cost. Decisions are made against evaluation results and stated budgets, not preference ([benchmarking](benchmarking.md)).

## Load testing with Locust

Scenarios: sustained queries, bursts, mixed query and session traffic, authenticated users. Record concurrency levels, error rates and latency percentiles. Use test data and mocked or budget-capped external services to avoid cost and rate-limit surprises. The in-process BM25 index limits horizontal scaling and should be observed under load.

## Measurement template

| Run ID | Config | Concurrency | Requests | p50 ms | p95 ms | Errors | Tokens/query | Cost/query |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

Related: [Deployment](deployment.md) · [Retrieval](retrieval.md)

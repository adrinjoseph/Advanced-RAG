# Interview Guide

> **Honesty rule:** every answer below describes the **design** ([Proposed]). In an interview, say which parts you built and measured. Template: *"I designed X; I implemented Y; I measured Z; I have not yet done W."* Never cite a metric you have not produced. Update this file with real numbers once evaluation reports exist.

## Architecture walkthrough

**Q: Walk me through the system.**
Two workflows share PostgreSQL: offline ingestion (parse, clean, chunk, embed, persist) and online QA (embed query, dense + full-text retrieval, RRF, evidence context, structured generation, citation validation, answer or abstain). Ingestion is separate because it is batch, failure-prone and write-heavy, while serving is read-mostly and latency-sensitive ([architecture.md](architecture.md)).

**Q: Why not LangChain?** The flow is a small, fixed pipeline; a framework would hide the parts I need to evaluate and test. Explicit components with interfaces for providers and repositories give testability without framework coupling ([ADR 0004](adr/0004-application-service-boundaries.md)).

## Retrieval and RRF

**Q: Why hybrid retrieval?** Dense finds paraphrases but can miss exact identifiers like section numbers; lexical finds exact terms but misses paraphrase. Hybrid covers both; I would prove it with a dense/lexical/hybrid ablation ([ADR 0003](adr/0003-hybrid-retrieval-and-rrf.md)).

**Q: Explain RRF.** Score = sum of 1/(k + rank) across lists. It uses ranks, so cosine and `ts_rank_cd` need no normalization. k=60 is a common starting value I would tune. Example: a chunk at rank 1 in dense and rank 2 in lexical scores 1/61 + 1/62 ≈ 0.0325 ([retrieval.md](retrieval.md#rrf)).

**Q: Is your lexical search BM25?** No. PostgreSQL `ts_rank_cd` is cover-density ranking, not BM25; it lacks the standard IDF and term-frequency saturation behavior. I call it full-text search ranked with `ts_rank_cd` and treat true BM25 as an evaluated option.

**Q: When would you add a reranker?** Only if an ablation shows an nDCG or answer-quality gain that justifies CPU latency.

## Database and indexing

**Q: Why PostgreSQL + pgvector instead of a vector DB?** One transactional store, SQL filters for status and dates in the same query, fewer systems. Cost: I tune indexes myself ([ADR 0002](adr/0002-postgresql-and-pgvector.md)).

**Q: HNSW trade-offs?** Approximate; `ef_search` trades recall for speed; build cost and memory; with selective filters, an approximate index scan can return too few rows, so I would measure and consider over-fetching or iterative scans if the installed pgvector supports them. I would verify index recall against exact search on the golden set.

**Q: How do you handle changing the embedding model?** Per-chunk model/dimension columns, shadow column, resumable backfill, new index, A/B on the golden set, then switch ([retrieval.md](retrieval.md#re-embedding)).

## Grounding and citations

**Q: Does your citation check prevent hallucination?** No. It proves identifier validity, membership in the retrieved set, and that the quote exists in the chunk. It does not prove entailment or legal correctness. I evaluate claim support separately with human review or a calibrated judge ([grounding-and-abstention.md](grounding-and-abstention.md)).

**Q: How do you decide to abstain?** Reason codes: no evidence, low-similarity evidence, conflicting sources, out of scope, generation failure, ungrounded output. Thresholds are calibrated on a golden set that includes unanswerable questions; I do not use raw RRF scores as confidence.

**Q: How do you handle prompt injection?** Evidence is delimited data; the model has no tools or secrets; output is schema- and citation-validated; approved sources only. Residual risk: a poisoned approved document ([security.md](security.md)).

## Testing and evaluation

**Q: How do you test without calling an LLM?** Provider interfaces with a deterministic fake embedder and a scripted LLM, including malformed and hostile outputs ([testing.md](testing.md)).

**Q: How do you avoid fooling yourself in evaluation?** Dev/test split, labels by chunk key from source documents, paraphrased questions, unanswerable questions, no-retrieval baseline, judge calibrated against human labels ([evaluation.md](evaluation.md)).

## Production reliability

**Q: What happens when the LLM provider is down?** Retries with backoff inside an overall deadline, then 503/504 with a request ID; the cache and tracing are optional and never block the answer ([observability.md](observability.md)).

**Q: How would you deploy it?** Not deployed. Options and cost controls are documented; I would first choose a target, estimate cost, and add auth and rate limiting ([deployment.md](deployment.md)).

## Trade-off questions

- **Why abstain instead of answering partially?** In a legal domain an unsupported answer costs more than a missed one; I measure both rates.
- **Why not stream tokens?** Citations must be validated before display; I stream validated results only.
- **Why async DB access?** Concurrent I/O in a request; trade-off is complexity ([ADR 0007](adr/0007-async-database-access.md)).
- **What would you do with more time?** Build the golden set, run ablations, evaluate true BM25 and reranking, then deploy with auth.

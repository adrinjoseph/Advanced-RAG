# Learning And Interview Guide

## Learning Guide

# Learning Guide

> Written for the project owner. Each topic follows the same structure, ends with one exercise, and links to the design. Do the exercise before moving on. Everything referenced is **[Proposed]** until built.

Suggested order is the order below; each topic builds on the previous.

## 1. Python package architecture
- **What:** `src` layout, packaging, imports, typed settings.
- **Why here:** several subsystems need clear boundaries ([ADR 0001](adr/0001-python-src-layout.md)).
- **Where:** repo root, `src/advanced_rag/`.
- **Learn first:** modules vs packages, `pyproject.toml`, editable installs, virtual environments.
- **Demonstrates understanding:** a package that installs with `pip install -e .` and whose tests import it like a user would.
- **Mistakes:** circular imports; putting config reads at import time.
- **Exercise:** create a two-module package where `domain` imports nothing and `api` imports `domain`; add a test that fails if the direction reverses.

## 2. API boundaries
- **What:** request/response contracts, validation, error mapping.
- **Why:** UI, tests and the harness depend on a stable contract ([api-and-ui.md](api-and-ui.md)).
- **Where:** `api/`.
- **First:** FastAPI routing, Pydantic models, dependency injection, HTTP status semantics.
- **Demonstrates:** abstention returning 200 while a provider timeout returns 504, tested.
- **Mistakes:** leaking exceptions; business logic in handlers.
- **Exercise:** build `/healthz` and a stub `/v1/query` with strict validation.

## 3. Database and migrations
- **What:** relational schema, constraints, Alembic.
- **Why:** PostgreSQL is the system of record ([database.md](database.md)).
- **First:** primary/foreign keys, unique constraints, transactions, `EXPLAIN`.
- **Demonstrates:** idempotent inserts and a migration that adds a column with up/down.
- **Mistakes:** editing applied migrations; missing indexes; ignoring transactions.
- **Exercise:** create `documents` and `chunks`, insert twice with `ON CONFLICT DO NOTHING`, confirm one row.

## 4. Ingestion
- **What:** parse, clean, chunk, persist ([ingestion.md](ingestion.md)).
- **First:** PDF text extraction quirks, Unicode normalization, hashing.
- **Demonstrates:** running ingestion twice changes nothing; a corrupt PDF fails alone.
- **Mistakes:** non-deterministic chunk IDs; cleaning that destroys section numbers.
- **Exercise:** write a chunker with a deterministic key and a test that proves it.

## 5. Embeddings
- **What:** text to vectors; dimension and model compatibility ([retrieval.md](retrieval.md#embeddings)).
- **First:** cosine similarity by hand, batching, rate limits.
- **Demonstrates:** startup refuses a model/dimension mismatch.
- **Mistakes:** mixing models in one column; forgetting query/document prefix conventions.
- **Exercise:** implement cosine similarity with NumPy on small vectors, then compare with pgvector's `<=>` on the same data.

## 6. Dense and lexical retrieval
- **What:** HNSW search and full-text search.
- **First:** `to_tsvector`, `websearch_to_tsquery`, `ts_rank_cd`, ANN trade-offs.
- **Demonstrates:** a query where dense wins and one where lexical wins, with evidence.
- **Mistakes:** calling `ts_rank` BM25; trusting approximate recall untested.
- **Exercise:** find a section-number query that FTS finds and dense misses; explain why.

## 7. RRF
- **What:** rank fusion ([retrieval.md](retrieval.md#rrf)).
- **First:** why raw scores are not comparable.
- **Demonstrates:** unit test reproducing the worked example; a `k` sweep.
- **Mistakes:** fusing scores instead of ranks; forgetting docs present in one list only.
- **Exercise:** implement RRF in plain Python and verify 0.03252 for the top chunk in the example.

## 8. Generation and structured outputs
- **What:** prompt, schema, validation ([generation.md](generation.md)).
- **First:** Pydantic v2 models, Instructor retry behavior, prompt delimiting.
- **Demonstrates:** malformed LLM output becomes an abstention, not a crash.
- **Mistakes:** parsing free text with regex; unbounded context.
- **Exercise:** write the `AnswerDraft` schema and a scripted fake LLM that returns three malformed variants.

## 9. Citations and abstention
- **What:** the five grounding levels and abstention rules ([grounding-and-abstention.md](grounding-and-abstention.md)).
- **First:** distinguishing "exists" from "supports".
- **Demonstrates:** a test where a real quote under a wrong claim passes levels 1 to 3 and is caught by evaluation.
- **Mistakes:** claiming citations guarantee truth; thresholds on raw RRF scores.
- **Exercise:** write a validator and craft one answer that fools it, then describe what would catch it.

## 10. Evaluation
- **What:** golden sets and metrics ([evaluation.md](evaluation.md)).
- **First:** Hit@K, Recall@K, MRR, nDCG by hand.
- **Demonstrates:** an ablation table (dense vs lexical vs hybrid) from a real run.
- **Mistakes:** tuning on the test set; reporting percentages on 15 questions.
- **Exercise:** compute all four metrics for three hand-made queries on paper, then in code.

## 11. Observability
- **What:** logs, traces, metrics ([observability.md](observability.md)).
- **First:** structured logging, correlation IDs.
- **Demonstrates:** finding the slowest span of a query from a trace.
- **Mistakes:** logging raw questions; no request ID.
- **Exercise:** add a request ID that appears in every log line of one request.

## 12. Deployment
- **What:** environments, CI/CD, hardening ([deployment.md](deployment.md)).
- **First:** environment variables, health checks, GitHub Actions basics.
- **Demonstrates:** CI that runs lint and tests with fakes and no secrets.
- **Mistakes:** provisioning without a teardown plan; deploying without auth.
- **Exercise:** write a workflow that runs `ruff` and `pytest` on a push.

---

## Interview Guide

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

---

## Glossary

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

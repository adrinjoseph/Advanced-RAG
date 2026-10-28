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

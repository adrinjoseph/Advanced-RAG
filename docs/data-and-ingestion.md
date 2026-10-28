# Data And Ingestion

## Data Sources

# Data Sources

> **Status:** **[Proposed]** policy. No corpus, document count or source URL is asserted here. Which sources form the first corpus is open decision OD-8 in the [specification](project-specification.md#11-open-decisions).

## 1. Supported source types

| Source type | Examples of kind (not a claimed corpus) | Why it matters |
|---|---|---|
| Statute / Act | primary legislation text | highest authority; long; amended over time |
| Rules | delegated legislation | operational details, forms, deadlines |
| Circular / Notification | administrative clarifications, date changes | frequently supersede earlier guidance |
| Official guidance / FAQ | departmental explanatory material | helpful but lower authority than statute |

Only documents obtained from the official publisher and added deliberately by the owner are ingested. No scraping of third-party commentary. URLs must be recorded only after the owner has verified them.

## 2. Provenance

Every document carries a manifest (YAML or JSON, **[Proposed]** format):

```yaml
source_type: circular
title: "<title as published>"
reference: "<official reference number>"
publisher: "<issuing authority>"
source_url: "<verified URL, optional>"
publication_date: 2000-01-01   # placeholder
effective_date: 2000-01-01     # placeholder
```

The manifest, the raw file hash and the ingestion run ID together let any chunk be traced to *what file, from where, ingested when*.

## 3. Dates, amendments and versioning

- **publication_date** is when it was issued; **effective_date** is when it applies. They differ often.
- An amendment is a **new document version** linked via `supersedes_document_id`, not an in-place edit. The old version gets `status = superseded` but stays queryable for historical questions.
- Default retrieval filters to `active` documents; a request may include `as_of_date` to retrieve what applied on a given day.
- The system must not silently mix versions: evidence blocks always show effective date and status.

## 4. Duplicate detection

1. Exact: identical raw-byte `sha256` → skipped.
2. Same `reference` with different hash → treated as a candidate new version and flagged for owner review rather than auto-superseding.
3. Chunk-level: identical normalized chunk text within a version is deduplicated by `text_hash`.

## 5. Update strategy

Add the new file with its manifest, run ingestion, mark the old version superseded in the manifest (`supersedes: <reference>`), review the ingestion report. Corpus Version increments on every committed change ([caching.md](caching.md)).

## 6. Authority and applicability caveats

- Retrieved ≠ authoritative. A circular may be superseded, scoped to certain taxpayers or assessment years, or conditional.
- Applicability (who, which year, which conditions) is a legal judgment the system **surfaces but does not decide**.
- Every answer carries the notice that this is a research aid, not advice.
- Documents that appear to conflict are reported as conflicting ([grounding-and-abstention.md](grounding-and-abstention.md#contradictory-sources)).

---
Related: [ingestion.md](ingestion.md) · [database.md](database.md)

---

## Ingestion

# Ingestion

> **Status:** **[Proposed]**. No ingestion code exists yet; the CLI entry point named below is **[Planned]**.

Ingestion converts official documents into searchable evidence. It is a separate batch workflow so failures, retries and re-embedding never affect serving ([architecture.md](architecture.md#1-system-context)).

## 1. Pipeline

```mermaid
flowchart LR
  L["Load file + manifest"] --> H["Hash"]
  H --> P["Parse"]
  P --> C["Clean"]
  C --> K["Chunk"]
  K --> E["Embed"]
  E --> W["Persist (one transaction)"]
  W --> V["Bump Corpus Version"]
```

Planned entry point **[Planned]**: `python -m advanced_rag.ingestion <path>`.

## 2. Stages

**Load.** Accept only files from configured approved directories; require a manifest ([data-sources.md](data-sources.md)). Reject non-PDF, zero-byte, oversized, or encrypted files with a typed error.

**Hash.** `content_hash = sha256(raw bytes)`. If present in `documents`, stop: idempotent no-op.

**Parse.** Extract text per page. Library choice is OD-2: evaluate on real samples for layout fidelity (tables, multi-column, footnotes), maintenance on Python 3.14 **[Verify]**, and license (e.g. some PDF libraries are AGPL, which matters if you ever distribute). Scanned PDFs with no text layer are detected (very low characters per page) and **rejected with a clear error** in the initial scope. OCR is out of scope.

**Clean.** Unicode NFKC, remove repeated headers/footers detected by page-frequency, fix hyphenated line breaks, collapse whitespace, preserve section numbers and punctuation exactly (they matter for lexical search). Cleaning must be deterministic.

**Chunk.** Structure-aware first: split on detected headings (Chapter, Section, Rule, Clause markers), then on token windows when a unit exceeds the limit. Starting proposal: target ~400 tokens, ~15% overlap, never split mid-sentence if avoidable; these are **tunable hypotheses** (OD-6) validated by [evaluation](evaluation.md), not facts. Each chunk records `ordinal`, `page_start/end`, `section_path`, `token_count`.

**Embed.** Batch requests, bounded concurrency, per-request timeout, exponential backoff with jitter on 429/5xx, no retry on 4xx validation errors. Store `embedding_model` and `embedding_dim` per row ([retrieval.md](retrieval.md#embeddings)).

**Persist.** One transaction per document: insert document, chunks (with generated `tsv`), vectors; bump `corpus_state.corpus_version`. A failure rolls back the whole document, so searchable state never contains half a document.

## 3. Idempotency and identifiers

- File identity: `content_hash`.
- Chunk identity: `chunk_key = sha256(document_content_hash + ordinal + text_hash)[:32]`, deterministic, so re-running yields the same keys and `INSERT ... ON CONFLICT (chunk_key) DO NOTHING` is safe.
- If chunking rules change, keys change, so a **new document version path** or an explicit `--rechunk` run is required; never mix chunking generations silently.

## 4. Errors and retries

| Failure | Handling |
|---|---|
| Missing/invalid manifest | reject document, log `ingestion_runs` row |
| Parse failure | record `error_class`, continue batch |
| Embedding provider transient error | retry with backoff, then mark run failed |
| Embedding dimension mismatch | fail fast; configuration error |
| DB error mid-transaction | rollback; document remains absent |

The batch exit code is non-zero if any document failed, but successful documents stay committed. Re-running retries only absent documents.

## 5. Updates and deletion

- **Update:** new file → new `documents` row, `supersedes_document_id` set, old row `superseded` (see [data-sources.md](data-sources.md#3-dates-amendments-and-versioning)).
- **Withdraw:** set `status = withdrawn`; excluded from retrieval, retained for audit.
- **Hard delete:** explicit CLI flag only; cascades to chunks; bumps Corpus Version.

## 6. Testing

Fixture PDFs (small, synthetic, committed) with golden expected chunks; idempotency test (run twice, assert no diff); failure tests (corrupt PDF, wrong dimension via a fake embedder); rollback test (inject error after chunk insert); chunk determinism test. Embedding provider is always a deterministic fake in tests ([testing.md](testing.md)).

---
Related: [database.md](database.md) · [data-flow.md](data-flow.md) · [security.md](security.md#untrusted-document-content)

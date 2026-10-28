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

# Data Sources

Status: **Planned**. No curated corpus is claimed to exist. This document defines what may enter the system and how it is recorded.

## Approved source categories

- Income-tax legislation and official rules.
- CBDT circulars and notifications.
- GST legislation, rules, notifications and official guidance.
- Other official government publications only when they fit this scope.

Start with a small, manageable corpus, not the whole tax and legal ecosystem.

## Candidate portals

Candidates only; availability and terms must be checked before use.

- [Income Tax Department](https://www.incometaxindia.gov.in/)
- [CBIC Tax Information Portal](https://taxinformation.cbic.gov.in/)
- [India Code](https://www.indiacode.nic.in/)

## Verification before ingestion

For every document, confirm and record:

1. The exact canonical URL, opened and checked.
2. The publishing authority (an official body, not a reposted copy).
3. Document type and whether it is the current or a superseded text.
4. Publication date and effective date, if stated.
5. Reuse and licensing conditions, where stated.
6. That the file parses into usable text.

Do not assume a document is current, or that a portal allows unrestricted reuse.

## Dates are different things

| Date | Meaning |
|---|---|
| Publication date | When the authority published the document |
| Effective date | When the provisions apply (may differ, may be retrospective) |
| Retrieval / ingestion timestamp | When this project fetched and processed it |

Record each separately. If a date is not stated, leave it empty; never infer or fabricate it.

## Provenance manifest

One manifest (for example `data/manifests/corpus.json` or `.yaml`) lists every source. Illustrative entry; values are placeholders, not real documents:

```json
{
  "manifest_version": "<integer or tag>",
  "documents": [
    {
      "document_id": "<stable internal id>",
      "title": "<verified title>",
      "canonical_url": "<verified official URL>",
      "source_authority": "<issuing body>",
      "document_type": "<act | rules | circular | notification | guidance>",
      "publication_date": null,
      "effective_date": null,
      "version_note": "<amendment or version information, if any>",
      "licence_note": "<stated reuse conditions, or 'not stated'>",
      "retrieved_at": "<timestamp>",
      "content_hash": "<hash of the file or normalized text>",
      "ingestion_status": "<pending | ingested | failed>"
    }
  ]
}
```

Evaluation records the manifest version it ran against ([evaluation](evaluation.md)).

## Content hashing and version tracking

A content hash identifies exact content. If a re-fetched document has the same hash, nothing changes. If the hash differs, treat it as a new version: keep the old record, link or label the relationship, and re-ingest only what changed. Never silently overwrite a version that evaluation labels refer to.

## Licensing and reuse

Government publications often have specific terms, and some portals restrict automated use. Record the stated terms per document, respect them, and keep raw source files out of the repository unless reuse is clearly permitted. When unsure, store only the URL and hash in the manifest.

## Update and re-ingestion strategy

1. Periodically re-check the canonical URL and compare hashes.
2. If changed, ingest as a new version with its own dates.
3. Re-index only changed chunks (stable chunk IDs and hashes make this possible).
4. Re-run evaluation after corpus changes, since chunk IDs and relevance labels may shift.

Related: [Database](database.md) · [Architecture](architecture.md)

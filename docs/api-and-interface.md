# Api And Interface

## Api And Ui

# API and UI

> **Status:** Every endpoint, schema and UI behavior here is **[Proposed]**. None exists yet. Merged from separate API and UI notes because the UI is a thin client of the API.

## 1. API

Base path `/v1`. Ingestion is **not** exposed over HTTP; it is a CLI ([ingestion.md](ingestion.md)).

| Method | Path | Purpose | Phase |
|---|---|---|---|
| POST | `/v1/query` | ask a question | 1 |
| GET | `/v1/chunks/{chunk_id}` | fetch a chunk and its document metadata (for citation display) | 1 |
| GET | `/v1/documents` | list ingested documents (filterable) | 1 |
| GET | `/healthz` | liveness | 1 |
| GET | `/readyz` | readiness: DB reachable, embedding config matches stored vectors | 1 |
| POST | `/v1/query/stream` | SSE variant | 3 |

### `POST /v1/query` request

```json
{
  "question": "string, 3 to 1000 chars",
  "as_of_date": "YYYY-MM-DD (optional)",
  "source_types": ["circular", "statute"],
  "debug": false
}
```

`debug` returns ranked lists and is disabled outside development.

### Response (answered)

```json
{
  "request_id": "uuid",
  "status": "answered",
  "answer": "string",
  "claims": [
    {"text": "string",
     "citations": [{"chunk_id": "string", "quote": "string",
                    "document": {"title": "", "reference": "", "effective_date": "", "status": "active"},
                    "pages": "12-13"}]}
  ],
  "corpus_version": 0,
  "disclaimer": "Research aid, not legal or tax advice."
}
```

### Response (abstained)

```json
{
  "request_id": "uuid",
  "status": "abstained",
  "reason": "insufficient_evidence",
  "message": "User-safe explanation.",
  "related_sources": [{"chunk_id": "string", "document": {"title": ""}}],
  "disclaimer": "..."
}
```

Both are HTTP 200: abstention is a valid result.

### Status codes and errors

| Code | When |
|---|---|
| 200 | answered or abstained |
| 404 | unknown chunk/document ID |
| 422 | validation failure |
| 429 | rate limit (future) |
| 503 | DB or provider unavailable |
| 504 | provider timeout |
| 500 | unexpected; generic body only |

Error format: `{"error": {"code": "string", "message": "string", "request_id": "uuid"}}`. Validation details list field names, not internals.

### Timeouts

Overall request deadline (configurable), shorter per-provider timeouts inside it. On deadline expiry return 504 with a request ID.

### Streaming

**[Planned, phase 3].** Citations must be validated before display, so token-by-token streaming of the draft answer is unsafe. Proposed SSE events: `retrieval_done` (evidence metadata), `final` (the validated response), `error`. Raw LLM tokens are not streamed. Revisit only if latency data justifies a design that streams provisional text and clearly marks it unvalidated.

### Authentication

None in the baseline. Local use only. Before any exposure: authentication, authorization, per-client rate limits, strict CORS ([security.md](security.md)).

## 2. UI (Chainlit)

Flow: user types a question → UI calls `POST /v1/query` → shows a progress indicator → renders the result.

Responsibilities of the UI's API client: base URL from config, timeouts, translate error responses to friendly messages, never access the database or providers directly (see [architecture.md](architecture.md#4-package-layout-and-dependency-direction-proposed)).

Display rules:
- **Answered:** answer text; each claim with numbered citation chips; expanding a chip shows the quote, document title, reference, effective date, status and pages. Superseded documents are visibly flagged.
- **Abstained:** plain-language reason, no invented answer, optional "possibly related sources".
- **Errors:** short message plus request ID.
- **Always:** the research-aid disclaimer and a note not to enter personal identifiers.

---
Related: [generation.md](generation.md) · [grounding-and-abstention.md](grounding-and-abstention.md) · [observability.md](observability.md)

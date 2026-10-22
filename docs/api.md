# API

Status: **Proposed**. Nothing here is implemented; routes, schemas and errors are illustrative. A generated OpenAPI spec will exist only once FastAPI runs. Rationale: [ADR 0003](decisions/0003-fastapi-and-chainlit.md).

All endpoints except health require authentication ([security](security.md)). Paths use a proposed `/api/v1` prefix.

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Liveness and dependency readiness |
| POST | `/query` | Ask a question, get a cited answer or abstention |
| POST | `/ingestion/documents` | Start ingestion (privileged) |
| GET | `/ingestion/documents/{document_id}` | Ingestion and document status |
| POST | `/sessions` | Create a conversation session |
| GET | `/sessions/{session_id}/messages` | List messages in a session |

## Health

`GET /health` returns `{"status": "ok"}` when the process is up. A readiness variant may report database and Pinecone reachability. Errors: `503` when a required dependency is down.

## Query

Request (illustrative):
```json
{"session_id": "<uuid>", "question": "string, 1-2000 chars"}
```
Response (illustrative):
```json
{
  "message_id": "<uuid>",
  "answer": "string or null",
  "abstained": false,
  "citations": [
    {"id": "S1", "document_title": "string", "section_path": "string", "version": "string", "chunk_id": "string"}
  ]
}
```
Validation: non-empty, length-capped, session must belong to the caller. Errors: `401` unauthenticated, `403` forbidden, `404` unknown session, `422` invalid body, `429` rate limited, `502/504` upstream failure. Streaming is planned as a later addition.

## Ingestion

`POST /ingestion/documents` (privileged) accepts a source reference (and optionally a file) plus metadata such as title, version and effective date. Returns `202` with a `document_id` and run status. Validation: allowed types, size limits, approved source domains. Errors: `401`, `403`, `409` duplicate content hash, `413` too large, `415` unsupported type, `422`.

`GET /ingestion/documents/{document_id}` returns state (`pending`, `processing`, `indexed`, `failed`), chunk counts and error details if any. `404` if unknown.

## Sessions and messages

`POST /sessions` returns `{"session_id": "<uuid>"}`. `GET /sessions/{session_id}/messages` returns messages with citations for the owner only. Errors: `401`, `403`, `404`.

## Error format (proposed)

```json
{"error": {"code": "string", "message": "string", "request_id": "string"}}
```
Domain errors (for example insufficient evidence) are mapped to HTTP responses in the `api` layer; internals and stack traces are never returned.

Related: [Architecture](architecture.md) · [Database](database.md)

# Security

## Security

# Security Design

> **Status:** **[Proposed]** threat model and controls. Reporting policy: [../SECURITY.md](../SECURITY.md). No control here is claimed as implemented or audited.

## 1. Assets and trust boundaries

| Trust level | Items |
|---|---|
| Trusted | application code, config, owner-approved ingestion list |
| Semi-trusted | official PDFs (authentic source, but arbitrary content and parser attack surface) |
| Untrusted | user questions, LLM output, any text inside documents once it reaches a prompt |
| External | LLM/embedding providers (they receive question and evidence text) |

## Untrusted document content

Prompt injection can live in a PDF ("ignore previous instructions"). Controls:

- Evidence is delimited and labelled as data; system prompt tells the model to ignore instructions inside it.
- The LLM has **no tools** and **no access** to secrets, DB or network, so injected text can at worst corrupt an answer.
- Output is constrained by schema and validated; a hijacked answer still needs quotes that exist in cited chunks.
- Ingestion is limited to an owner-approved source list; no arbitrary URL fetching.
- Delimiter strings inside chunks are neutralized.
- Residual risk: a poisoned *approved* document can still skew answers. Review new sources before ingestion.

## 3. Malformed and unsafe files

Enforce size and page limits, timeouts on parsing, reject encrypted/non-PDF files, parse in a separate process in the ingestion CLI, keep parser libraries updated.

## 4. Input and output validation

Requests: max length, type checks, Unicode normalization via Pydantic. SQL: parameterized queries only; never interpolate user text. Output: schema validation, citation validation, and size limits. Responses never echo stack traces.

## 5. Secrets

Environment variables only; `.env` is git-ignored; `.env.example` holds placeholders; CI uses repository secrets; secret scanning enabled on the repo **[Planned]**. Secrets are never logged or placed in traces, prompts or documentation.

## 6. Sensitive data and privacy

Users may type personal tax details. Treat questions as potentially sensitive: do not persist raw questions by default; telemetry stores hashes, lengths, timings and IDs ([observability.md](observability.md)); warn users in the UI not to enter identifiers; document that questions and evidence are sent to the external providers, and review the chosen provider's data-retention terms **[Verify]**.

## 7. Safe errors

User-facing errors carry a code and request ID, never internals. Provider errors are mapped, not passed through.

## 8. Database permissions

Separate ingest (write) and app (read-only on corpus) roles ([database.md](database.md#6-database-permissions)); least privilege; no superuser from the app; TLS to remote databases if ever used.

## 9. Dependencies and deployment

Pin versions, lock file, `pip-audit` (or equivalent) in CI **[Planned]**, Dependabot or equivalent. Python 3.14 is new: prefer packages with published 3.14 support **[Verify]**. Deployment hardening is in [deployment.md](deployment.md#production-hardening). The API has **no authentication** in the baseline; before any non-local exposure, add authentication, rate limiting and CORS rules.

## 10. Security tests

Injection fixtures (documents with hostile instructions), delimiter-escape tests, oversized/corrupt PDFs, SQL-injection strings in queries, secret-leak checks on logs ([testing.md](testing.md)).

---
Related: [generation.md](generation.md) · [ingestion.md](ingestion.md) · [grounding-and-abstention.md](grounding-and-abstention.md)

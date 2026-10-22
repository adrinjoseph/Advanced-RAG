# Security

Status: **Planned**. No formal security audit has been performed. Related: [Threat model](threat-model.md).

## Core rule

**Authorization cannot rely on prompt instructions.** Telling the model "do not reveal restricted documents" is not access control. Restricted text must never enter the model's context.

## Authentication and authorization

- Authentication is handled in the API layer (`security/authentication.py`); the mechanism (for example API keys or tokens) is a decision to record in an ADR.
- Authorization (`security/authorization.py`) maps an authenticated user to an **access scope**: the documents they may read and the actions they may perform (query, ingest, administer).
- Ingestion is a privileged action, not available to ordinary users.

## Document-level access control

1. Resolve the user's allowed document set from PostgreSQL.
2. Apply it as a filter in Pinecone and to BM25 candidates.
3. Re-verify returned chunk IDs against PostgreSQL before building evidence.
4. Build the prompt only from verified chunks.
5. Citations expose only titles and links the user may already access.

## Prompt injection

Documents and user input are untrusted. A retrieved passage might say "ignore previous instructions". Mitigations: delimit and label evidence as data; keep the system instruction separate; give the model no tools beyond an allow-list ([ADR 0006](decisions/0006-bounded-agent-orchestration.md)); validate model output (citation IDs must exist); screen documents at ingestion (`security/injection.py`, planned); never let model output trigger privileged actions directly. These reduce risk but do not eliminate it.

## Tool permissions

A workflow or the model may use only allow-listed, read-only retrieval functions with fixed schemas. No file system, shell, network or write access from model-driven steps.

## Input validation

Pydantic schemas enforce types, length limits and allowed values; file uploads check type, size and source before parsing; identifiers are validated, never interpolated into queries.

## Secrets management

Secrets come from environment variables or a secret store, never from Git. `.env` is gitignored; `.env.example` holds placeholders only. Rotate any key that leaks. See [configuration](configuration.md).

## Logging and sensitive data

Log request IDs, timings, document IDs and decisions. Do not log secrets, full prompts with private text, or user credentials by default. Redact before logging. Set retention limits.

## Session isolation

Sessions and messages are owned by a user; every read and write checks ownership. Session IDs are unguessable. One user's history never appears in another's context.

## Database access

Use parameterized queries via SQLAlchemy; a least-privilege database role for the application; migrations run with a separate, more privileged role where practical.

## Dependency and deployment risks

Pin and review dependencies; scan them in CI; keep images minimal; do not expose PostgreSQL publicly; use HTTPS in any real deployment ([deployment](deployment.md)).

## Security test scenarios

Cross-user retrieval attempts; restricted document in top-K; injected instructions in a test document; oversized or malformed input; ingestion by a non-privileged user; forged session ID; secret in logs; citation to an unauthorized document. These live in `tests/security/` ([testing](testing.md)).

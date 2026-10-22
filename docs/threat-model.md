# Threat Model

A lightweight, design-time model. It is **not** a formal security audit, and it will change as the implementation does. Controls: [security](security.md).

## Assets

User accounts and credentials; session and message history; original and indexed documents (including any access-restricted ones); API and service keys (Pinecone, LLM, AWS); the evaluation dataset and results; service availability and cost budget.

## Trust boundaries

User/browser to Chainlit; Chainlit to FastAPI; FastAPI to PostgreSQL, Pinecone, S3 and the LLM provider; ingested document content to the model context. See the diagram in [data-flow](data-flow.md).

## Threat actors

Anonymous internet user; authenticated but malicious user; a user with legitimate but narrower access; author of a malicious document; compromised dependency or leaked credential.

## Attack surfaces

HTTP API; Chainlit UI; ingestion endpoint and file parsers; prompt context built from retrieved text; secrets in env/CI; third-party services and packages.

## Abuse scenarios

| Scenario | Mitigation | Residual risk | Verification |
|---|---|---|---|
| Cross-user data leakage (session or retrieval) | Ownership checks; access filter before context; re-check in PostgreSQL | Filter bug or misconfigured scope | Security tests with two users |
| Malicious document with injected instructions | Evidence labelled as data; output validation; no privileged tools | Model may still be influenced | Injection fixtures; grounding checks |
| Unauthorized ingestion | Privileged-only endpoint; source validation; audit log | Stolen admin credential | Authorization tests |
| Exposed API credentials | Env/secret store; gitignore; secret scanning; rotation | Human error | CI secret scan; log redaction test |
| Citation leakage (titles/snippets of restricted docs) | Citations resolved only from verified, accessible chunks | Metadata leaks via error messages | Test restricted-doc citations |
| Resource abuse (cost, DoS) | Rate limits; input size caps; timeouts; budgets | Distributed abuse | Locust and limit tests |
| Dependency compromise | Pinning; scanning; minimal images | Zero-day | CI dependency scan |

## Residual risk summary

Prompt injection cannot be fully eliminated; access control correctness depends on tested code paths; third-party services are trusted to the extent their terms allow. These are accepted for a portfolio-scale system and stated in [limitations](limitations.md).

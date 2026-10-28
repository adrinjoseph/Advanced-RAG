# ADR 0006: Local-first development

**Status:** Proposed

## Context
Native Windows 11, Git Bash, no GPU, no paid cloud budget.

## Decision
Develop and test entirely locally. Application and primary PostgreSQL run natively; Docker Compose only for Redis and self-hosted Langfuse. No paid cloud resources without cost estimate and approval. External LLM/embedding APIs are the only paid dependency, behind interfaces and mocked in tests.

## Alternatives considered
- **Everything in Docker:** reproducible, but explicitly not wanted for the app/DB here.
- **Cloud-first:** realistic, but costs money and slows iteration.
- **WSL:** possible, but adds an environment the owner has not chosen.

## Benefits
Zero infrastructure cost, fast feedback, full control.

## Costs and trade-offs
pgvector on native Windows is harder to install (OD-5); "works on my machine" risk; no local GPU models; deployment realism deferred.

## Consequences
CI (Linux, service containers) becomes the portability check; setup docs must be explicit and verified ([development-setup.md](../development-setup.md)).

## Revisit if
Native Windows setup proves unreliable, or a deployment target is chosen.

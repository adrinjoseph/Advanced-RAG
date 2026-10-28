# Architecture Decision Records

An ADR records **one significant decision**, why it was made, what else was considered, and what it costs. They explain the project to future you, reviewers and interviewers.

> **Status:** All ADRs are **Proposed** until the project owner confirms them. A Proposed ADR is a design decision on paper, not a statement that anything is implemented.

## Format

`NNNN-short-title.md` containing: Status · Context · Decision · Alternatives considered · Benefits · Costs and trade-offs · Consequences · Conditions to revisit.

Status values: `Proposed` → `Accepted` → (`Superseded by NNNN` | `Deprecated`). Never edit an Accepted ADR's decision; write a new ADR that supersedes it.

## When to write one

When a choice is hard to reverse, affects several components, excludes reasonable alternatives, or you would otherwise have to re-explain it in an interview. Not for routine library upgrades or naming.

## Index

| ADR | Title | Status |
|---|---|---|
| [0001](0001-python-src-layout.md) | Python `src` layout | Proposed |
| [0002](0002-postgresql-and-pgvector.md) | PostgreSQL and pgvector as the single store | Proposed |
| [0003](0003-hybrid-retrieval-and-rrf.md) | Hybrid retrieval with RRF | Proposed |
| [0004](0004-application-service-boundaries.md) | Application service boundaries | Proposed |
| [0005](0005-structured-grounded-generation.md) | Structured, grounded generation | Proposed |
| [0006](0006-local-first-development.md) | Local-first development | Proposed |
| [0007](0007-async-database-access.md) | Asynchronous database access | Proposed |
| [0008](0008-evaluation-driven-quality.md) | Evaluation-driven quality | Proposed |

Back to [architecture](../architecture.md) · [specification](../project-specification.md).

# Contributing

This is currently a solo portfolio project. These conventions keep the work consistent and reviewable, and make outside contributions easy if they ever happen.

## Workflow

1. Create a branch from `main`: `feat/<topic>`, `fix/<topic>`, `docs/<topic>`, `test/<topic>` or `chore/<topic>`.
2. Keep changes small and focused on one concern.
3. Open a pull request, even when working alone. CI results and the diff are the review record.
4. Squash or rebase so history stays readable.

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/): `feat(retrieval): add RRF fusion`, `fix(ingestion): handle empty pages`, `docs(security): clarify access filtering`.

## Code quality

- Type hints on public functions; Pydantic models at API and configuration boundaries.
- Respect the dependency direction in [docs/architecture.md](docs/architecture.md): `domain` imports nothing from the project, and `api` never contains retrieval logic.
- External services (Pinecone, LLM, S3) are accessed only through `integrations/` so they can be mocked.
- No secrets in code, tests or logs. See [docs/security.md](docs/security.md).
- The formatter and linter will be chosen and recorded in `pyproject.toml`. Do not mix tools.

## Testing

- New behaviour needs tests at the appropriate level ([docs/testing.md](docs/testing.md)).
- Tests must not call paid or networked services by default.
- Retrieval or generation changes also need an evaluation run, not just unit tests.

## Documentation

Update the relevant file in `docs/` in the same pull request as the change. Docs must say whether something is **Planned**, **Proposed**, **Implemented** or **Needs verification**, and must not describe unbuilt features as working.

## Proposing architecture changes

Open an issue or draft pull request that adds a new decision record in `docs/decisions/` (next number, status `Proposed`) covering context, decision, alternatives, trade-offs and consequences. Superseding a decision means marking the old record `Superseded` and linking to the new one. See [docs/decisions/README.md](docs/decisions/README.md).

## Reporting evaluation results

A result is only valid if it records: commit hash, dataset version, configuration (models, chunking, K values, fusion and rerank settings), run date, and the metric values with the number of queries. No number may be quoted without this. See [docs/benchmarking.md](docs/benchmarking.md).

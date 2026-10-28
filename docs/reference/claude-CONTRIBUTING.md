# Contributing

> Tooling named here (Ruff, pytest, CI) is **[Planned]** until its configuration exists in the repo.

## Workflow

1. Open or pick an issue; keep changes small and focused.
2. Branch from `main`: `feat/<topic>`, `fix/<topic>`, `docs/<topic>`, `test/<topic>`.
3. Commit with Conventional Commits: `feat(retrieval): add RRF fusion`, `fix(ingestion): handle empty pages`, `docs: update database ER diagram`.
4. Open a pull request; do not push directly to `main`.

## Code quality

`ruff check .` and `ruff format --check .` must pass; type hints on public functions; no secrets, no print-debugging in committed code.

## Testing requirements

New behavior needs tests ([testing strategy](docs/testing.md)). Providers are mocked; no test may use the network. Retrieval or prompt changes need an evaluation run compared against the previous baseline ([evaluation](docs/evaluation.md)).

## Documentation expectations

If you change behavior, update the matching doc in the same PR, keep status tags honest (Proposed → Implemented only via the README status table), update the ADR or write a new one for significant decisions ([ADR guide](docs/adr/README.md)), and keep component names canonical ([glossary](docs/glossary.md)).

## Pull-request checklist

- [ ] Tests added or updated and passing
- [ ] Lint and format pass
- [ ] Docs and README status table updated
- [ ] No secrets or real personal data
- [ ] No new dependency without checking Python 3.14 support and licence
- [ ] Evaluation compared, if retrieval/generation changed
- [ ] ADR added for any significant decision

# ADR 0001: Python `src` layout

**Status:** Proposed

## Context
The project is a Python package with several subsystems plus tests, migrations and a UI script. Python 3.14.6 on native Windows.

## Decision
Use a `src/advanced_rag/` package layout with `pyproject.toml`, tests in `tests/`, and the Chainlit entry script outside the package in `ui/`.

## Alternatives considered
- **Flat layout** (package at repo root): simpler, but tests can import the working directory copy and hide packaging errors.
- **Single-file scripts:** fast to start, unmaintainable and untestable at this size.
- **Monorepo of multiple packages:** overkill for one deployable.

## Benefits
Tests run against the installed package (`pip install -e .`), catching missing-module and packaging bugs; clear import boundaries; standard for modern tooling.

## Costs and trade-offs
Slightly more setup; editable install required; contributors unfamiliar with `src` layout need a note.

## Consequences
All imports use `advanced_rag.*`. Dependency direction is enforced by convention ([architecture.md](../architecture.md#4-package-layout-and-dependency-direction-proposed)).

## Revisit if
The project splits into independently deployed services, or packaging tools drop `src` layout support.

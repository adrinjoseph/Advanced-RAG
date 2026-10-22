# 0005: Python Version and Dependency Compatibility

**Status:** Proposed

## Context
The local interpreter is Python 3.14.6. Whether the full stack (FastAPI, Pydantic, SQLAlchemy, Alembic, Pinecone client, `rank_bm25`, RAGAS, LangGraph, Chainlit, reranker libraries, ML dependencies) supports it has **not been verified**.

## Decision
Treat the project's Python version as an explicit, verified constraint. Before depending on the stack, install it in a clean virtual environment and run the test suite. Record the verified version in `.python-version` and `requires-python` in `pyproject.toml`. If a critical dependency does not support the installed interpreter, use a Python version that all required dependencies support; no specific version is chosen yet.

## Alternatives considered
- **Assume compatibility:** risks late breakage.
- **Pin an older Python immediately:** may be unnecessary if 3.14 works.
- **Containers only:** hides the problem locally and diverges from the dev environment.

## Trade-offs
Early verification costs time; an older Python may lag on language features.

## Consequences
CI uses the same version as local development. Dependency additions that break the constraint are rejected or isolated.

## Revisit if
Compatibility is verified, or a required dependency drops or adds support.

See [Development setup](../development-setup.md).

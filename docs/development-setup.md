# Development Setup

> **Status:** **None of these commands has been executed against this project.** Sections marked *(depends on planned files)* will work only after those files exist. Update this table as each step is verified.

| Step | Verified? |
|---|---|
| Python 3.14.6 + venv | not yet |
| Dependency install | not yet (no lock file exists) |
| PostgreSQL + pgvector on Windows | not yet |
| Migrations, ingestion, tests | not yet (code does not exist) |

## 1. Shell

Use **Git Bash** on Windows 11. Paths use forward slashes.

## 2. Python 3.14.6 and virtual environment

```bash
py -3.14 --version            # confirm interpreter is installed and reports 3.14.x
py -3.14 -m venv .venv
source .venv/Scripts/activate # Git Bash activation path on Windows
python --version
```

Do not downgrade Python silently. If a dependency lacks 3.14 support, record it in the compatibility table in the [specification](project-specification.md#7-technology-baseline) and decide deliberately.

### Compatibility check to run first **[Verify]**

In a clean venv, attempt to install each and note failures: `fastapi`, `pydantic`, `sqlalchemy`, `asyncpg`, `alembic`, `pgvector` (Python package), `instructor`, `chainlit`, `redis`, `httpx`, the chosen PDF library, `pytest`, `ruff`. Record versions that work.

## 3. Dependencies *(depends on planned `pyproject.toml`)*

```bash
pip install -e ".[dev]"       # planned; pyproject.toml does not exist yet
```

## 4. Environment variables

```bash
cp .env.example .env          # then edit; never commit .env
```

See [../.env.example](../.env.example).

## 5. PostgreSQL and pgvector prerequisites

1. Install PostgreSQL natively for Windows; confirm `psql --version`.
2. Install the pgvector extension. On native Windows the upstream project documents building from source with Visual Studio's C++ build tools (`nmake /F Makefile.win`) **[Verify against the pgvector README for your PostgreSQL and pgvector versions]**. Prebuilt binaries may exist; verify provenance before trusting them (OD-5).
3. Create the database and enable the extension:

```bash
psql -U postgres -c "CREATE DATABASE advanced_rag;"
psql -U postgres -d advanced_rag -c "CREATE EXTENSION IF NOT EXISTS vector;"
psql -U postgres -d advanced_rag -c "SELECT extversion FROM pg_extension WHERE extname='vector';"
```

Record the pgvector version; it determines features such as iterative index scans ([database.md](database.md#4-indexes)).

## 6. Redis and Langfuse (only when needed, phases 2 and 3)

Docker Compose file is **[Planned]**: `docker compose up -d redis langfuse`. Follow Langfuse's current self-hosting guide **[Verify]**.

## 7. Migrations, ingestion, run *(depend on planned code)*

```bash
alembic upgrade head                                  # planned
python -m advanced_rag.ingestion path/to/docs         # planned
uvicorn advanced_rag.api.main:app --reload            # planned
chainlit run ui/chainlit_app.py                       # planned
```

## 8. Tests and lint *(depend on planned tooling config)*

```bash
ruff check .
ruff format --check .
pytest
```

---
Related: [testing.md](testing.md) · [deployment.md](deployment.md) · [../CONTRIBUTING.md](../CONTRIBUTING.md)

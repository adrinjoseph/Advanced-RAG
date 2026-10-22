# Development Setup

Windows-focused (Git Bash). The application cannot be launched yet; this describes preparing the environment. Commands are illustrative and not guaranteed until the project files they depend on exist.

## Prerequisites

- **Git** for Windows (includes Git Bash).
- **Python.** Python 3.14.6 is currently installed locally. Compatibility of the full dependency stack with this version has **not** been validated ([ADR 0005](decisions/0005-python-and-dependency-compatibility.md)). If a dependency fails to install, use a Python version all dependencies support.
- **PostgreSQL 16**, either a local installer or a container.
- **Docker Desktop** (needs WSL 2 or Hyper-V on Windows).
- An editor and a GitHub account.

## Clone and virtual environment (Git Bash)

```bash
git clone https://github.com/adrinjoseph/Advanced-RAG.git
cd Advanced-RAG
python -m venv .venv
source .venv/Scripts/activate
python --version
```

## Environment file

```bash
cp .env.example .env
```
Fill in placeholders locally; never commit `.env`. Setting names: [configuration](configuration.md).

## Dependencies (once manifests are ready)

```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
```
The extras name depends on what `pyproject.toml` defines. Verify the install in a clean environment before relying on it.

## PostgreSQL

Option A: run PostgreSQL 16 in Docker via `compose.yaml` once it defines the service. Option B: install locally and create a database and user for development. Point `DATABASE_URL` at it.

## Migrations (once configured)

```bash
alembic upgrade head
```

## Running tests

```bash
pytest
```
Unit tests need no external services; integration, evaluation and e2e tests may need a test database or credentials ([testing](testing.md)).

## Common problems

| Symptom | Likely cause and fix |
|---|---|
| `source .venv/Scripts/activate` fails | Use Git Bash, not CMD; in PowerShell use `.venv\Scripts\Activate.ps1` |
| Package install fails on 3.14 | Dependency lacks support; try a supported Python (see ADR 0005) |
| Docker will not start | WSL 2 or virtualization not enabled; update Docker Desktop |
| `psql` or PostgreSQL not found | Not installed or not on PATH; use the Docker service instead |
| Port 5432 in use | Another PostgreSQL instance is running; stop it or change the port |
| Line-ending warnings | Set `git config core.autocrlf` as appropriate for the repo |

Related: [Testing](testing.md) · [Deployment](deployment.md)

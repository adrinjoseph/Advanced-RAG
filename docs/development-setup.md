# Development Setup

Commands are labelled by shell. Treat them as starting points and confirm against the actual project files (`pyproject.toml`, `.env.example`, `compose.yaml`).

## Python

Check the version the project requires (`requires-python` in `pyproject.toml`). The local interpreter has been Python 3.14.6, and compatibility of the full dependency stack with it has **not** been verified. If a dependency fails to install, use a Python version that every required package supports.

```bash
python --version
```

## Virtual environment

Git Bash:
```bash
python -m venv .venv
source .venv/Scripts/activate
```

PowerShell:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

## Install dependencies

```bash
python -m pip install --upgrade pip
pip install -e .
```

`pyproject.toml` must not point to a deleted README; fix its `readme` field to `README.md` if the build fails. Check for duplicate dependency definitions (`pyproject.toml` versus `requirements.txt`) and keep one source of truth.

## Environment variables

```bash
cp .env.example .env
```

Fill in values locally. `.env.example` is the source of truth for variable names. Never commit `.env`, and never paste its contents into issues or chat. See [security](security.md).

## PostgreSQL

Either run PostgreSQL via Docker Compose (if `compose.yaml` defines the service), or install it locally and create a development database and user. Set the database URL variable from `.env.example` accordingly. Use a throwaway database for tests.

## Alembic

```bash
python -m alembic heads
python -m alembic history
python -m alembic upgrade head
```

Run `upgrade head` only against a development database you control.

## Run FastAPI

```bash
python -m uvicorn advanced_rag.api.main:app --reload
```

Confirm the module path and app object name in `api/main.py`. Once the health route exists, check it in a browser or with `curl`.

## Run Chainlit

```bash
chainlit run ui/chainlit_app.py
```

The UI needs the API running and its base URL configured. Confirm the file name under `ui/`.

## Tests and linting

```bash
python -m ruff check .
python -m ruff format --check .
python -m pytest -q
git diff --check
python -m pip install -e . --no-deps
```

Do not assume these pass; read the actual output.

## Troubleshooting

| Symptom | Likely cause and fix |
|---|---|
| `pip install -e .` fails on the readme | `pyproject.toml` references a deleted README; point it to `README.md` |
| Dependency won't install on this Python | Package lacks support; try a supported Python version |
| `alembic` cannot find the database | Wrong or missing database URL in `.env`; PostgreSQL not running |
| `alembic` cannot import models | Package not installed (`pip install -e .`) or wrong import path in `migrations/env.py` |
| `ModuleNotFoundError: advanced_rag` | Virtual environment not active, or package not installed |
| Port already in use | Another process uses the port; stop it or choose a different port |
| Docker will not start | Docker Desktop not running, or WSL 2 not enabled |
| Activation script blocked | PowerShell execution policy; see above |

Related: [Database](database.md) · [Architecture](architecture.md)

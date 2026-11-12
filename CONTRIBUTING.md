# Contributing

This is a solo portfolio project. The bar for external contributions is high
because every line of code must be explainable by the owner in a technical
interview. That said, bug reports, test improvements, and documentation fixes
are very welcome.

## Before you open a PR

- Check [open issues](../../issues) first to avoid duplicate work.
- For anything beyond a small fix, open an issue first and describe what
  you want to change and why. Wait for a response before writing code.
- Read [SECURITY.md](SECURITY.md) if the change touches auth, retrieval
  isolation, guardrails, or any input/output path.

## Dev setup

```bash
git clone https://github.com/adrinjoseph/advanced-rag.git
cd advanced-rag

# Install Python tooling (outside Docker, for lint and tests)
pip install uv
uv sync --all-extras

# Copy and fill in env vars
cp .env.example .env

# Start the full local stack
docker compose -f docker-compose.yml -f docker-compose.override.yml up -d

# Apply migrations
docker compose exec api alembic upgrade head
```

**Python version:** whatever is pinned in `pyproject.toml` → `requires-python`.
Do not use a different version.

## Branch naming
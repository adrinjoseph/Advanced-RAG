# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project does not follow Semantic Versioning — it is a portfolio project.
Entries describe phases and milestones rather than semver releases.

## [Unreleased]

### Added
- Repository created with governance files, `pyproject.toml`, and CI skeleton.
- `ADVANCED_RAG_SPEC_AZURE.md` — full project specification including locked
  decisions, fact ledger, Azure architecture, and build phases.

---

<!-- Phases will be added here as they are completed. Example format:

## [Phase 1 — Foundation] - 2026-MM-DD

### Added
- Alembic migrations for all tables (users, collections, documents, chunks, query_logs).
- `/health` liveness endpoint (leaks no internals).
- `seed_user.py` script for local development.
- Auth: `POST /auth/login` returns a signed short-lived token.

### Changed
- N/A (first real phase).

### Fixed
- N/A.

### Security
- N/A.

## [Phase A — Repo skeleton] - 2026-11-12

### Added
- All GitHub governance files (README, LICENSE, CoC, SECURITY, CONTRIBUTING,
  CHANGELOG, PR template, issue templates, CODEOWNERS, dependabot).
- `pyproject.toml` with Ruff and pytest config.
- `.gitignore`, `.env.example`.
- `ci.yml` skeleton: lint + unit smoke test.
- `deploy.yml` skeleton: placeholder, implemented in Phase 10.
- Branch protection on `main`.

-->
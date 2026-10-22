# Testing

Status: **Planned**. Test directories exist as placeholders: `tests/unit`, `integration`, `evaluation`, `security`, `e2e`.

| Level | Purpose | External services |
|---|---|---|
| Unit | Pure logic: chunking, fusion, metrics, citation validation, config | None; fakes |
| Integration | Components together: API with a test database, repositories, migrations | Test PostgreSQL; mocked Pinecone, LLM, S3 |
| Retrieval evaluation | Metrics on a small fixed set; guards against regressions | Mocked or cached embeddings |
| Security | Access control, injection fixtures, ownership, secret handling | Test database |
| End-to-end | UI/API through the full flow on a small corpus | Controlled environment; optional live services |
| Regression | Compare current results to stored baselines per category | As above |

## Principles

- **Isolation:** each test sets up and tears down its own state; no order dependence.
- **Mock external services** through the `integrations/` interfaces. Default test runs make no paid or network calls.
- **Fixtures** in `tests/conftest.py` and `tests/fixtures/`: sample chunks, tiny corpora, fake clients.
- **Deterministic assertions:** fix seeds, avoid asserting on free-form LLM text; assert on structure, citation IDs and abstention flags.
- **Test databases:** a separate database (or schema) migrated with Alembic per run, reset between tests; never the development or production database.
- **Live-service tests** are marked and opt-in.

## What to test first

RRF and metric functions (known inputs and outputs), chunk ID and hash stability, citation validation, access filtering, API validation, and migration up/down.

## CI

GitHub Actions runs fast tests on every pull request (unit, integration with a service container, security) and a small evaluation subset. Full evaluations and load tests are manual ([deployment](deployment.md)).

Related: [Security](security.md) · [Evaluation](evaluation.md)

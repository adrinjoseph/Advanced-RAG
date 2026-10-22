# Architecture Decision Records

Each record states context, decision, alternatives, trade-offs, consequences and revisit conditions. No experiments are claimed unless a record says so. Dates are intentionally omitted; use Git history.

| # | Title | Status |
|---|---|---|
| [0001](0001-hybrid-retrieval.md) | Hybrid retrieval (BM25 + dense + RRF) | Accepted |
| [0002](0002-pinecone-and-postgresql.md) | Pinecone for vectors, PostgreSQL for application data | Accepted |
| [0003](0003-fastapi-and-chainlit.md) | FastAPI backend with a Chainlit UI over HTTP | Accepted |
| [0004](0004-evaluation-first-development.md) | Evaluation-first development | Accepted |
| [0005](0005-python-and-dependency-compatibility.md) | Python version and dependency compatibility | Proposed |
| [0006](0006-bounded-agent-orchestration.md) | Bounded agent orchestration with LangGraph | Proposed |

Statuses: **Proposed**, **Accepted**, **Superseded**. To change a decision, add a new record and mark the old one Superseded ([CONTRIBUTING](../../CONTRIBUTING.md)).

Back to the [documentation index](../README.md).

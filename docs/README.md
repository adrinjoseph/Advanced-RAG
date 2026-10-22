# Documentation Index

Everything here describes the project's design and intended behaviour. Unless a document states otherwise, treat components as **Planned** or **Proposed** until the code and tests exist. Labels used: **Planned**, **Proposed**, **Implemented**, **Needs verification**.

## Architecture
- [Architecture](architecture.md): components, boundaries, dependency direction
- [Data flow](data-flow.md): document and query lifecycles, trust boundaries, failure points

## Retrieval and ingestion
- [Retrieval](retrieval.md): BM25, dense, hybrid, RRF, reranking, filters
- [Chunking and indexing](chunking-and-indexing.md): parsing, chunking, metadata, identifiers, versioning

## Generation and security
- [Generation and citations](generation-and-citations.md)
- [Security](security.md)
- [Threat model](threat-model.md)

## Evaluation
- [Evaluation](evaluation.md)
- [Evaluation dataset](evaluation-dataset.md)
- [Benchmarking](benchmarking.md)

## API and persistence
- [API](api.md)
- [Database](database.md)
- [Configuration](configuration.md)

## Development and deployment
- [Development setup](development-setup.md)
- [Testing](testing.md)
- [Deployment](deployment.md)
- [Performance and cost](performance-and-cost.md)

## Product usage and limitations
- [User guide](user-guide.md)
- [Limitations](limitations.md)
- [Glossary](glossary.md)

## Architecture decisions
- [Decision index](decisions/README.md)
- [0001 Hybrid retrieval](decisions/0001-hybrid-retrieval.md)
- [0002 Pinecone and PostgreSQL](decisions/0002-pinecone-and-postgresql.md)
- [0003 FastAPI and Chainlit](decisions/0003-fastapi-and-chainlit.md)
- [0004 Evaluation-first development](decisions/0004-evaluation-first-development.md)
- [0005 Python and dependency compatibility](decisions/0005-python-and-dependency-compatibility.md)
- [0006 Bounded agent orchestration](decisions/0006-bounded-agent-orchestration.md)

Project root: [README](../README.md) · [Contributing](../CONTRIBUTING.md) · [Changelog](../CHANGELOG.md)

# Configuration

Status: **Proposed**. Variable names are not final and are not yet implemented. Settings are meant to be loaded and validated in `config.py` (Pydantic).

## Principles

Configuration comes from environment variables. `.env` is gitignored; `.env.example` lists names with placeholder values only. Secrets are never committed, logged or baked into images ([security](security.md)).

## Planned settings

| Setting (proposed) | Purpose | Secret |
|---|---|---|
| `APP_ENV` | `development`, `test`, `production` | No |
| `LOG_LEVEL` | Logging verbosity | No |
| `DATABASE_URL` | PostgreSQL connection | Yes |
| `PINECONE_API_KEY` | Pinecone access | Yes |
| `PINECONE_INDEX_NAME` | Index to use | No |
| `EMBEDDING_MODEL` | Embedding model name (not yet chosen) | No |
| `LLM_PROVIDER`, `LLM_MODEL` | Generation provider and model (not yet chosen) | No |
| `LLM_API_KEY` | Provider credential | Yes |
| `AWS_REGION`, `S3_BUCKET_NAME` | Original document storage | No |
| AWS credentials | Via standard AWS mechanisms, not committed | Yes |
| `RERANKER` | `none`, BGE, or Cohere | No |
| `COHERE_API_KEY` | Only if Cohere Rerank is used | Yes |
| `RAGAS_JUDGE_MODEL` | Judge model for evaluation | No |
| Retrieval settings | `bm25_top_k`, `dense_top_k`, `rrf_k`, `rerank_top_n`, `final_k` | No |

## Environments

Separate values for development, test and production. Tests use a throwaway database and mocked external services by default ([testing](testing.md)).

## Secret management

Local: `.env`. CI: GitHub Actions secrets. Deployment: platform secret store. Rotate on suspected exposure; use least-privilege keys; keep separate keys per environment.

Related: [Development setup](development-setup.md) · [Deployment](deployment.md)

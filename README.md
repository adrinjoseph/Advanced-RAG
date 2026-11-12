
---

## Stack

| Layer | Tool | Responsibility |
|---|---|---|
| API | FastAPI, Uvicorn, Pydantic v2 | Endpoints, validation, orchestration |
| Database | ParadeDB (Postgres + pgvector + pg_search) | Vectors, BM25, relational data |
| ORM / migrations | SQLAlchemy 2 async, asyncpg, Alembic | Async queries, schema versioning |
| Extraction | PyMuPDF | Text blocks with page provenance |
| Embeddings | bge-small-en-v1.5 (384-dim) via onnxruntime | CPU-only, no PyTorch |
| Tokenization | transformers AutoTokenizer | Real token counts for chunking |
| LLM | Groq via httpx, hand-written adapter | Structured generation, retry/backoff |
| UI | Chainlit | Thin HTTP client only |
| Proxy | Caddy | HTTPS, auto-certificates |
| Cloud | Azure VM (amd64), Bicep, GitHub Actions | Deployment, IaC, CI/CD |

---

## Quickstart (local)

**Requirements:** Docker Desktop, Git, Python 3.x (for linting/tests outside Docker).

```bash
git clone https://github.com/adrinjoseph/advanced-rag.git
cd advanced-rag

# Copy and fill in required env vars
cp .env.example .env

# Start the full stack (db, api, ui, caddy)
docker compose -f docker-compose.yml -f docker-compose.override.yml up -d

# Check all services are healthy
docker compose ps

# Run migrations
docker compose exec api alembic upgrade head

# Seed a test user
docker compose exec api python scripts/seed_user.py

# Open the UI
open http://localhost
```

**Run tests:**

```bash
pip install uv && uv sync --all-extras
pytest -m unit
pytest -m integration   # requires Docker stack running
pytest -m security
```

**Lint:**

```bash
ruff check .
ruff format --check .
```

---

## Configuration

All configuration via environment variables. Copy `.env.example` to `.env` and fill in values.
Never commit `.env` — it is in `.gitignore`.

| Variable | Description | Required |
|---|---|---|
| `SECRET_KEY` | Signed token secret (min 32 random bytes) | Yes |
| `GROQ_API_KEY` | Groq API key | Yes |
| `DATABASE_URL` | Async Postgres URL (`postgresql+asyncpg://...`) | Yes |
| `ALLOWED_ORIGINS` | CORS origins (comma-separated) | Yes |
| `DENSE_CANDIDATES` | HNSW candidates per query (default: 20) | No |
| `BM25_CANDIDATES` | BM25 candidates per query (default: 20) | No |
| `RRF_K` | RRF constant (default: 60) | No |
| `FINAL_CONTEXT_CHUNKS` | Chunks in LLM context (default: 8) | No |
| `CHUNK_TOKENS` | Target chunk size in tokens (default: 450) | No |
| `CHUNK_OVERLAP` | Overlap in tokens (default: 50) | No |
| `MAX_UPLOAD_MB` | Upload size cap | No |
| `MAX_PAGES` | PDF page cap | No |
| `MAX_QUERY_CHARS` | Query length cap (default: 2000) | No |
| `LLM_MODEL` | Groq model name | Yes |
| `LLM_TIMEOUT_S` | Groq call timeout seconds | No |

---

## Results

> All tables filled only after eval harness is complete (Phase 4+). Numbers come from committed files in `eval/results/`.

### Retrieval — dev split (~60%, N questions)

| Mode | Recall@5 | Recall@10 | MRR | nDCG@10 |
|---|---|---|---|---|
| Dense only | not yet measured | not yet measured | not yet measured | not yet measured |
| BM25 only | not yet measured | not yet measured | not yet measured | not yet measured |
| Hybrid (RRF) | not yet measured | not yet measured | not yet measured | not yet measured |

### Chunk-size ablation (dev split)

| Chunk tokens | Recall@10 | nDCG@10 |
|---|---|---|
| 300 | not yet measured | not yet measured |
| 450 (default) | not yet measured | not yet measured |

### Generation — test split (40%)

| Metric | Value |
|---|---|
| Citation validity (chunk_id in evidence) | not yet measured |
| Quote-match rate (normalized substring) | not yet measured |
| Abstention precision | not yet measured |
| Abstention recall | not yet measured |
| Answer correctness (manual sample) | not yet measured |

### Held-out gap (2 unseen document types, ~15 questions)

| | Dev split | Held-out | Gap |
|---|---|---|---|
| Recall@10 | not yet measured | not yet measured | not yet measured |
| Answer correctness | not yet measured | not yet measured | not yet measured |

### System performance

| Metric | Value |
|---|---|
| p50 query latency (end-to-end) | not yet measured |
| p95 query latency (end-to-end) | not yet measured |
| Ingestion speed (seconds/page) | not yet measured |
| Tokens per query (avg) | not yet measured |
| Cold-start time (VM start → /health) | not yet measured |
| Peak RAM on Azure VM | not yet measured |
| OS disk usage | not yet measured |
| Data disk usage | not yet measured |

---

## Limitations

- **Text PDFs only.** Scanned / image PDFs are rejected with a clear error message. OCR is out of scope.
- **No DOCX, TXT, Markdown, spreadsheets, audio, video, or website crawling.**
- **Non-streaming only.** Citation verification requires the complete response before returning.
- **Sequential chunking.** Semantic / heading-based chunking is not implemented — PDF layouts are too unreliable.
- **No reranker.** Planned as future work if ablations show a ranking problem.
- **No self-service registration.** Chainlit password login only. No roles or billing system.
- **No guaranteed correctness.** A valid citation proves the model cited real text. Whether the answer is correct is sampled manually — it is not guaranteed.
- **Single VM.** No horizontal scaling, no Redis, no Kubernetes.
- **Provider dependency.** Generation requires Groq to be reachable. The system does not fall back to a local model.

---

## Security

- Collection and owner filter enforced in SQL on **both** retrieval paths (dense and BM25).
- Three-stage guardrails: input validation, context isolation (delimiters + token budget), output schema + quote verification.
- No secrets in the repo, images, logs, or LLM prompts.
- Forged `collection_id` attacks tested in `tests/security/`.
- Cross-owner document read and delete attempts tested.
- Injection-pattern detection is logged — it is **not** the security boundary.

See [SECURITY.md](SECURITY.md) to report a vulnerability.

---

## Azure deployment and cost control

Hosted on a single Azure Linux VM running Docker Compose. All infrastructure defined in `infra/` (Bicep).

### Power modes

| Mode | VM state | Compute billed | Disks billed | Command |
|---|---|---|---|---|
| **RUN** | Running | Yes | Yes | `scripts/azure/up.sh` |
| **PAUSE** | **Deallocated** | **No** | Yes | `scripts/azure/down.sh` |
| **DESTROY** | Deleted | No | No (data EBS detached first) | `scripts/azure/destroy.sh` |

> **Important:** "Stopped" ≠ deallocated. Only `Deallocated` stops compute billing. `down.sh` verifies the state is `deallocated` before exiting.

### Cost guardrails

- Budget alerts at 50%, 75%, and 90% of credit.
- VM auto-shutdown enabled daily.
- Weekly credit log in `docs/cost-control.md`.
- Backups in a separate resource group (`rg-advancedrag-backups`) — survive `DESTROY`.

### Deployment

```bash
# Pause (deallocate)
./scripts/azure/down.sh

# Resume and deploy latest image
./scripts/azure/up.sh

# Full status
./scripts/azure/status.sh

# Destroy everything (backups survive)
./scripts/azure/destroy.sh
```

GitHub Actions deploy (`deploy.yml`) uses OIDC — no Azure secrets stored in GitHub.
See [docs/runbook.md](docs/runbook.md) for the full deploy, restore, and rollback guide.

---

## Resource usage (measured)

| Resource | Value |
|---|---|
| Peak RAM on VM | not yet measured |
| Data disk (pgdata + uploads) | not yet measured |
| Cold-start time (deallocated → /health healthy) | not yet measured |
| ONNX Runtime image size contribution | not yet measured |

---

## Project structure
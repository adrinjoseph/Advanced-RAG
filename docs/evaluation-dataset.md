# Evaluation Dataset

Status: **Planned schema**. The dataset does not exist yet. Files will live in `data/evaluation/` and be versioned.

## Format

One JSON object per line (JSONL), validated by Pydantic in `evaluation/datasets.py`.

| Field | Type | Meaning |
|---|---|---|
| `query_id` | string | Unique, stable ID |
| `query` | string | The question text |
| `category` | enum | See categories below |
| `answerable` | bool | Whether the corpus supports an answer |
| `relevant_chunk_ids` | list[string] | Expected relevant chunks (empty if unanswerable) |
| `relevance_grades` | map (optional) | Graded labels for nDCG |
| `reference_answer` | string (optional) | Short reference where applicable |
| `expected_sources` | list (optional) | Expected document and section references |
| `as_of_date` | date (optional) | For temporal queries |
| `user_role` | string (optional) | For access-restricted cases |
| `notes` | string | Edge cases and labelling rationale |

Dataset version, corpus manifest version and labeller notes are stored in a header file beside the data.

## Categories

| Category | Tests |
|---|---|
| Exact statutory reference | Lexical strength (section/form numbers) |
| Paraphrase | Dense strength |
| Exception or condition | Reading conditions correctly |
| Temporal | Version and effective-date handling |
| Multi-passage | Needs several chunks |
| Ambiguous | Clarification or stated assumption |
| Unanswerable | Correct abstention |
| Access-restricted | Authorization and leakage |

## Illustrative examples (fictional, not legal facts)

```json
{"query_id": "ex-001", "query": "What does Section X of the Example Act require?", "category": "exact_reference", "answerable": true, "relevant_chunk_ids": ["<chunk-id>"], "notes": "Placeholder; replace with a real, verified reference."}
{"query_id": "ex-002", "query": "What is the weather in Thrissur tomorrow?", "category": "unanswerable", "answerable": false, "relevant_chunk_ids": [], "notes": "Out of corpus; expect abstention."}
{"query_id": "ex-003", "query": "Show me the restricted internal memo.", "category": "access_restricted", "answerable": false, "relevant_chunk_ids": [], "user_role": "standard", "notes": "Must not leak restricted content or its citation."}
```

## Labelling guidelines (to be completed with real data)

Label relevance against the verified corpus, record why a chunk is relevant, include hard negatives (similar but wrong sections), and have an unambiguous rule for partial relevance. Re-label if chunking changes, since chunk IDs change.

Related: [Evaluation](evaluation.md) · [Benchmarking](benchmarking.md)

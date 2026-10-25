# Evaluation

Status: **Planned**. No dataset has been built and no evaluation has been run. Do not quote any metric until a recorded run produced it.

## Goals

1. Show whether hybrid retrieval beats BM25-only and dense-only on this corpus.
2. Check that answers are grounded in retrieved evidence, with valid citations.
3. Check that the system abstains when it should, and answers when it can.
4. Make every result reproducible and comparable across changes.

Evaluation reuses the application's retrieval and generation code ([architecture](architecture.md)).

## Approach

Start with transparent custom metrics and pytest-based checks. RAGAS may be added later if it gives measurable value and can be maintained without needless dependencies.

## Dataset structure

A versioned file (for example JSONL under `data/evaluation/`), one example per line:

| Field | Meaning |
|---|---|
| `query_id` | Stable unique ID |
| `query` | The question |
| `category` | For example exact reference, paraphrase, temporal, multi-passage, unanswerable |
| `answerable` | Whether the corpus supports an answer |
| `relevant_chunk_ids` | Expected relevant chunks (or documents); empty if unanswerable |
| `relevance_grades` | Optional graded labels, for nDCG |
| `reference_answer` | Optional short reference |
| `notes` | Edge cases and labelling rationale |

Labels refer to chunk IDs, so they must be reviewed whenever chunking or the corpus changes. The dataset has its own version, recorded with every run.

## Retrieval metrics

Computed per query against labelled relevant items, averaged over the query set; K is the cutoff.

- **Hit@K:** 1 if at least one relevant item is in the top K, else 0.
- **Recall@K:** relevant items in the top K divided by all relevant items.
- **MRR:** mean over queries of 1 / rank of the first relevant item (0 if none).
- **nDCG@K:** $\mathrm{DCG@K}=\sum_{i=1}^{K}\frac{rel_i}{\log_2(i+1)}$ divided by the DCG of the ideal ordering; needs graded labels, or binary labels as a simple case.

Metric functions get their own unit tests on tiny hand-computed examples.

## Citation and grounding checks

- **Citation validity:** every citation refers to a chunk that was actually retrieved and supplied to the model; no invented IDs, URLs or sections.
- **Evidence grounding:** each claim in the answer is supported by a cited passage.
- **Unsupported claims:** claims with no support are counted and reported.
- **Basic answer relevance:** the answer addresses the question asked.

Automated checks cover validity (a deterministic lookup). Grounding and relevance may need a judge model or manual review; record which was used.

## Abstention evaluation

On answerable queries, the system should answer; on unanswerable queries, it should abstain. Report both error types: wrong answers to unanswerable questions, and abstentions on answerable ones.

## Reproducibility

Each run records: code commit, dataset version, corpus manifest version, chunking settings, embedding model identifier, LLM model identifier and parameters, retrieval parameters (K, candidate pool sizes, RRF constant), and the date. Prefer deterministic settings; repeat runs that involve an LLM and report the spread.

## How to run

A CLI in `scripts/` will run the evaluation and write a report, and pytest will run a small fast subset. Exact commands will be documented here once they exist. *Planned.*

## Interpreting results and limitations

- A small dataset gives noisy estimates; do not claim small differences.
- Labels are subjective for legal relevance; keep written labelling guidelines.
- Retrieval metrics say nothing about answer quality, and answer checks say little about ranking.
- LLM-judged scores can be biased or inconsistent; spot-check by hand.
- Report results by category, not only the overall average.

Related: [Data sources](data-sources.md) · [Security](security.md)

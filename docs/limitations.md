# Limitations

Honest boundaries of the design. Many apply only once the system exists, but they shape how it should be built and reported.

- **Source coverage and freshness.** Only a small curated set is indexed. Laws are amended; the index can be stale. Each answer should state the version it used.
- **Parsing and chunking.** PDFs and tables can parse badly; chunks can split provisions. Errors here propagate to everything downstream.
- **Retrieval misses.** BM25 misses paraphrase; dense search misses exact identifiers; hybrid reduces but does not remove misses. Reranking can also demote correct passages.
- **Generation errors.** LLMs can misread evidence, over-generalize or omit conditions even with good context.
- **Citation errors.** A citation can point to a real passage that does not support the claim. Citation correctness is checked, not guaranteed.
- **Historical-version confusion.** Mixing old and new provisions is a known failure mode; metadata filters help but depend on correct dates.
- **Evaluation limits.** A small dataset gives noisy estimates; LLM judges are biased and inconsistent; labels for legal relevance are subjective ([evaluation](evaluation.md)).
- **Latency and cost.** Hybrid search, reranking and large contexts add delay and spend; hosted services add rate limits and dependencies.
- **Security.** Prompt injection and access-control bugs cannot be fully ruled out; no formal audit has been done ([security](security.md), [threat model](threat-model.md)).
- **Scalability.** The in-process BM25 index limits scaling across workers.
- **Not legal or tax advice.** Output is an engineering demonstration. Consult qualified professionals for real decisions.

# Caching

> **Status:** **[Planned]**, phase 3. Nothing is cached in the baseline. Redis is an optimization, never a source of truth ([architecture.md](architecture.md#6-data-ownership)).

## 1. What to cache

| Item | Cache? | Reason |
|---|---|---|
| Query embeddings | Yes | deterministic per (model, text); saves provider cost and latency |
| Retrieval results (fused list) | Yes, keyed with Corpus Version | deterministic for a given corpus and config |
| Final answers | Cautiously; later, if at all | depend on prompt, model, evidence; stale-answer risk in a legal domain |
| Raw user questions as readable keys | **No** | privacy; use hashes |
| Secrets, API keys | **Never** | |
| Failures/abstentions caused by provider errors | **No** | transient |

## 2. Key design

```
advrag:v1:emb:{embedding_model}:{sha256(normalized_query)}
advrag:v1:ret:{corpus_version}:{config_hash}:{sha256(normalized_query + filters)}
```

`v1` is a key-schema version. `config_hash` covers `N`, `M`, `k`, text-search config and filters. Because `corpus_version` is part of retrieval keys, every committed ingestion invalidates old entries automatically without a flush.

## 3. TTLs and invalidation

Embeddings: long TTL (they only change if the model changes, which changes the key). Retrieval results: shorter TTL as a safety net plus Corpus Version keying. Manual flush by key prefix is available for emergencies. Document supersession bumps Corpus Version, so superseded text cannot be served from cache.

## 4. Correctness risks

- Serving evidence from a withdrawn or superseded document (mitigated by Corpus Version).
- Mixing embedding models (model is in the key).
- Serving a cached answer built with an older prompt or model (not cached initially).
- Cache poisoning via malformed values: store typed, versioned JSON; validate on read.

## 5. Bypass and failure behavior

A `Cache-Control: no-cache`-style request option or `debug` mode bypasses reads. Redis errors or timeouts are logged and treated as a **miss**; the request proceeds without caching. Short Redis timeouts prevent the cache from slowing the system it is meant to speed up.

---
Related: [retrieval.md](retrieval.md#embeddings) · [observability.md](observability.md) · [deployment.md](deployment.md)

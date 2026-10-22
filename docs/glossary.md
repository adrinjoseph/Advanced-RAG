# Glossary

| Term | Definition |
|---|---|
| **RAG** | Retrieval-Augmented Generation: retrieve relevant passages, then have a language model answer using them. |
| **BM25** | A lexical ranking function scoring documents by term frequency, term rarity and length normalization. |
| **Lexical retrieval** | Matching on the actual words in the query and text (for example BM25). |
| **Embedding** | A numeric vector representing text so that similar meanings are close together. |
| **Dense retrieval** | Retrieving by similarity between query and chunk embeddings. |
| **Hybrid retrieval** | Combining lexical and dense retrieval results. |
| **RRF** | Reciprocal Rank Fusion: merges ranked lists by summing 1/(k + rank) per list. |
| **Cross-encoder reranking** | Rescoring top candidates with a model that reads query and passage together. |
| **Recall@K** | Share of all relevant items found in the top K results. |
| **Hit@K** | Whether at least one relevant item appears in the top K. |
| **MRR** | Mean Reciprocal Rank: average of 1/rank of the first relevant result. |
| **nDCG** | Normalized Discounted Cumulative Gain: ranking quality with graded relevance, rewarding relevant items near the top. |
| **Faithfulness** | Whether answer claims are supported by the retrieved context. |
| **Answer relevancy** | How well the answer addresses the question (RAGAS metric). |
| **Context precision** | How much of the retrieved context is relevant, with relevant items ranked high (RAGAS metric). |
| **Context recall** | How much of the needed information is present in the retrieved context (RAGAS metric). |
| **Abstention** | Declining to answer because evidence is insufficient. |
| **Chunk** | A segment of a document that is indexed and retrieved as a unit. |
| **Provenance** | The recorded origin of content: source, version, dates, location. |
| **Prompt injection** | Text in input or documents that tries to override the model's instructions. |
| **RAGAS** | An evaluation framework for RAG systems with LLM-judged metrics. |
| **ADR** | Architecture Decision Record. |

Related: [Retrieval](retrieval.md) · [Evaluation](evaluation.md) · [Security](security.md)

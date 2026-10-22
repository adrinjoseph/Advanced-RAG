# 0006: Bounded Agent Orchestration with LangGraph

**Status:** Proposed

## Context
A single retrieve-then-generate pass may fail on multi-part or ambiguous questions. A multi-step workflow could help, but unbounded agents are hard to test, slow and costly.

## Decision
Build and evaluate the baseline pipeline first. Introduce LangGraph only when evaluation shows a class of queries the baseline fails and a multi-step flow can address. Any workflow will have a fixed graph, a step limit, a token and latency budget, and restricted tools. No LangGraph workflow is implemented yet.

## Alternatives considered
- **Plain function pipeline:** simplest; the baseline.
- **Open-ended agent with free tool use:** flexible, but unpredictable and a larger security surface.

## Trade-offs
A graph adds state and tracing complexity, plus extra LLM calls (cost and latency).

## Consequences
Tools exposed to a workflow are an allow-list; every step is logged and testable; the workflow must beat the baseline on the same dataset.

## Revisit if
The baseline meets quality goals without orchestration (drop it), or evaluation shows a clear multi-step need (adopt it).

See [Security](../security.md) and [Evaluation](../evaluation.md).

# ADR 0004: Application service boundaries

**Status:** Proposed

## Context
Retrieval, generation and validation could be tangled inside route handlers, making them hard to test and swap.

## Decision
Separate components with narrow interfaces: Retrieval Service, Evidence Context Builder, Generation Service, Grounding Validator, Embedding Client, LLM Client, repositories. The API orchestrates; the UI talks to the API only over HTTP; ingestion is a separate CLI sharing repositories and the Embedding Client.

## Alternatives considered
- **Logic in route handlers:** fastest to write; untestable and provider-coupled.
- **Microservices:** operational cost unjustified at this scale.
- **A generic orchestration framework:** excluded (no LangChain/LangGraph); adds abstraction without need.

## Benefits
Fakes for providers in tests; each component evaluable in isolation (the Evaluation Harness calls Retrieval directly); clear failure domains.

## Costs and trade-offs
More files and interfaces; risk of premature abstraction, so only providers and repositories get interfaces.

## Consequences
Dependency direction rules ([architecture.md](../architecture.md#4-package-layout-and-dependency-direction-proposed)). Final package structure is confirmed when implementation starts; this ADR may be revised then.

## Revisit if
A component needs independent scaling or a different language/runtime.

# ADR 0005: Structured, grounded generation

**Status:** Proposed

## Context
Free-text LLM answers cannot be reliably checked for citations or abstention.

## Decision
The LLM returns a Pydantic v2 schema (via Instructor, or provider-native structured output if Instructor is unavailable on Python 3.14): claims, each with citations containing `chunk_id` and a verbatim `quote`. The Grounding Validator checks identifier existence, membership in retrieved evidence and quote anchoring, with one retry before abstention.

## Alternatives considered
- **Free text with `[1]` markers:** hard to validate.
- **Post-hoc citation matching by embedding similarity:** probabilistic, can fabricate support.
- **LLM-as-judge at serving time:** adds cost and latency; kept for evaluation.

## Benefits
Deterministic, cheap checks; traceable claims; clean abstention path; testable with a scripted LLM.

## Costs and trade-offs
Structured output can reduce answer fluency; quote anchoring does not prove entailment; added retry latency; Instructor compatibility **[Verify]**.

## Consequences
Level 1 to 3 checks at serving time, level 4 in evaluation, level 5 never automated ([grounding-and-abstention.md](../grounding-and-abstention.md)).

## Revisit if
Quote requirements degrade answer quality measurably, or a validated entailment checker proves practical.

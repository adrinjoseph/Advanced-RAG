# 0003: FastAPI Backend with a Chainlit UI over HTTP

**Status:** Accepted

## Context
The project needs a testable backend and a chat interface with streaming, citations and sessions, without duplicating retrieval logic in the UI.

## Decision
FastAPI with Pydantic serves all retrieval, generation and ingestion over HTTP. Chainlit is a separate process that calls the API through a client in `ui/`.

## Alternatives considered
- **Chainlit calling retrieval code directly:** quicker, but couples UI and pipeline and bypasses the API's auth and validation.
- **Custom web frontend:** more control, much more effort.
- **Gradio or Streamlit:** viable, but Chainlit's chat and source-inspection model fits the use case.

## Trade-offs
An extra network hop and a client layer to maintain; streaming must be carried over HTTP. In return the API is independently testable, secured and load-testable.

## Consequences
Auth, validation and session ownership are enforced once, in the API. The UI contains no business logic.

## Revisit if
The HTTP boundary blocks required UI features, or a different frontend becomes necessary.

See [API](../api.md) and [Architecture](../architecture.md).

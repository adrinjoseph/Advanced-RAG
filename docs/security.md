# Security

Scope: safe configuration, input validation and prompt-injection defences for an educational, single-user system. **There is no authentication or authorization**; full identity management and multi-tenancy are out of scope. Do not expose the API publicly.

## Secret management

- API keys and database credentials come from environment variables; nothing is hardcoded.
- `.env` is gitignored and never committed or pasted into logs, issues or chat. `.env.example` holds names with placeholder values only.
- Keep separate values for development and any shared environment; rotate a key if it may have leaked.
- CI uses repository secrets, not files.

## Input validation

- Pydantic schemas enforce types and limits on every request; queries have a maximum length.
- Documents have a maximum size and an allowed type list; ingestion runs through a controlled CLI, not an open upload endpoint.
- Identifiers and filters are validated; database access uses parameterized queries via SQLAlchemy.

## Prompt-injection threat model

Retrieved documents are untrusted. A passage may contain text like "ignore your instructions", or try to make the model emit fake citations or reveal configuration.

Mitigations:
- Keep system instructions, the user question and source text in clearly separated, labelled sections; state that source text is data, not instructions.
- Never execute or act on instructions found in retrieved content.
- Give the model no tools, so a successful injection cannot trigger actions.
- Validate output: citations must map to chunks that were actually supplied.
- Screen documents at ingestion for obvious instruction-like patterns (`security/`); this is a heuristic, not a guarantee.

## Grounded generation and citation validation

The model may only cite identifiers from the supplied evidence. After generation, code checks each citation against the retrieved chunk set and rejects or removes anything invalid. URLs and section references shown to users come from stored metadata, never from model text. A citation is not a claim of legal authority or currency; that depends on the source and its recorded dates ([data sources](data-sources.md)).

## Logging

Log request IDs, timings, document and chunk IDs and decisions. Do not log secrets, authorization headers, full environment values, or full prompts containing source text by default. Redact before logging.

## Current limitations

- No authentication, authorization or rate limiting.
- Prompt-injection defences reduce risk but cannot eliminate it.
- No formal security audit or dependency scanning has been done.
- Third-party services (LLM, embeddings, Pinecone) receive query and evidence text.

Related: [Architecture](architecture.md) · [Development setup](development-setup.md)

# Security Policy

Design and threat model: [docs/security.md](docs/security.md).

## Reporting a vulnerability

Do not open a public issue containing exploit details. Use GitHub's private vulnerability reporting (repository **Security** tab → **Report a vulnerability**) if it is enabled. If it is not, open a minimal public issue stating only that you have a security report and asking for a private channel. No email address is published here. **[Owner: enable private reporting or add a contact before publishing.]**

## Handling guidelines

- **Secrets:** environment variables only; never commit `.env`; rotate any key that leaks.
- **Documents:** ingest only owner-approved official sources; treat file content as untrusted; do not ingest files containing personal data.
- **Prompt injection:** retrieved text is data, never instructions.
- **Malformed files:** size, page and time limits; parse in isolation.
- **Logging and telemetry:** no raw questions, evidence text or secrets.
- **Dependencies:** pin, audit regularly, prefer packages with Python 3.14 support.

## Scope note

The baseline API has no authentication and is intended for local use only.

# Security Policy

## Project Status

Advanced-RAG is an educational project for evidence-grounded question answering over Indian tax and regulatory documents.

It is intended for local development and learning. It has not been established as production-ready or independently security-audited.

## Supported Versions

Until versioned releases are published, security fixes are handled against the latest development version on the default branch.

## Reporting a Vulnerability

Please report suspected security vulnerabilities privately rather than publishing exploit details in a public issue.

Include the following where possible:

- A description of the vulnerability and its potential impact.
- The affected component or file.
- Steps to reproduce the issue safely.
- Relevant sanitized logs or error messages.
- A suggested mitigation, if known.

Never include API keys, passwords, access tokens, personal information, or confidential source documents in a report.

For now, contact the repository maintainer through a private channel. A dedicated security reporting address or GitHub private vulnerability reporting can be configured separately.

Please allow reasonable time for investigation and remediation before publicly disclosing a vulnerability.

## Security Scope

Areas of interest include:

- **Secrets management:** accidental exposure of API keys, database credentials, or environment variables.
- **Prompt injection:** malicious instructions embedded in retrieved documents or user queries.
- **Retrieval and citations:** fabricated citations, untrusted source metadata, or evidence that does not support an answer.
- **Input validation:** malformed, excessively large, or unexpected requests and documents.
- **Database safety:** SQL injection, unsafe query construction, unauthorized writes, and unintended data modification.
- **Dependency security:** vulnerable packages and insecure configuration.
- **Logging and error handling:** leakage of credentials, sensitive data, or internal implementation details.
- **API exposure:** missing authentication, excessive resource consumption, or unauthorized access.

## Security Expectations

Contributors should follow these practices:

1. Keep real credentials in local environment configuration or an appropriate secret manager.
2. Never commit `.env` files, API keys, passwords, access tokens, or private credentials.
3. Treat retrieved documents and user-provided content as untrusted input.
4. Never treat instructions embedded in retrieved source text as trusted system instructions.
5. Validate model-generated citations against trusted, stored source metadata and the evidence retrieved for the current request.
6. Use parameterized database operations and avoid executing untrusted input as code or SQL.
7. Avoid logging secrets, unnecessary raw document contents, or sensitive user data.
8. Test security-sensitive changes and document known limitations.

These are security requirements, not a claim that every control is already implemented or independently verified.

## Deployment Limitations

The project is intended for educational and local use unless additional security controls have been implemented and reviewed.

Before exposing it to other users or deploying it publicly, assess and address at least:

- Authentication and authorization.
- Network access and API exposure.
- Rate limiting and request-size limits.
- Database permissions, backups, and recovery.
- Secret storage and rotation.
- Dependency updates and vulnerability scanning.
- Monitoring, logging, and incident response.
- Prompt-injection and data-exfiltration risks.

Do not expose an unauthenticated development API to the public internet.

## Responsible Disclosure

Please act in good faith, avoid accessing or modifying other people's data, and avoid testing that could disrupt services or destroy data.

This policy may evolve as the project gains functionality and stronger security controls.

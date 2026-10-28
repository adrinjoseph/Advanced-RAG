# Security Policy

## Scope

Advanced-RAG processes legal and regulatory source material and may accept user questions. Security issues can affect application availability, confidentiality, integrity, source attribution, or the trustworthiness of generated answers.

The project is under active development. Do not assume that every control described here is already implemented.

## Reporting a vulnerability

Please report suspected vulnerabilities privately to the project maintainer using the contact method listed in the repository profile or project hosting settings.

Include, where safe:
- a concise description of the issue;
- affected component, file, or endpoint;
- steps to reproduce or a proof of concept;
- potential impact; and
- any suggested mitigation.

Do not include real secrets, personal data, or sensitive production data in the report. Do not publicly disclose an exploitable issue before maintainers have had a reasonable opportunity to investigate and address it.

A response timeline has not been formally committed. The maintainer should acknowledge reports, investigate severity, coordinate a fix, and communicate status as promptly as practical.

## Security priorities

The implementation should address the following areas:

- **Secrets:** keep API keys, database credentials, and deployment tokens out of source control and logs.
- **Database access:** use parameterized statements or safe ORM expressions; use least-privilege credentials.
- **Input validation:** validate request shape and size, and handle malformed input safely.
- **Resource controls:** apply sensible timeouts, bounded work, and controlled connection pooling.
- **Retrieved content:** treat source documents and retrieved text as untrusted data, not as privileged instructions.
- **Citations and integrity:** do not fabricate sources or claim that retrieved passages support statements they do not support.
- **Errors and logs:** avoid leaking secrets, connection strings, stack traces, or sensitive user content to clients or logs.
- **Dependencies and deployment:** keep dependencies reviewed, configure hosting secrets securely, and restrict deployment permissions.
- **Cloud costs:** set usage limits and monitor provider quotas where available.

## Reporting AI/RAG-specific issues

Please report examples of:
- fabricated or misattributed citations;
- answers that contradict the retrieved evidence;
- failure to abstain when evidence is inadequate;
- incorrect temporal or jurisdiction filtering;
- prompt injection through retrieved documents that changes system behavior; or
- leakage of confidential information across requests.

Provide the question, relevant source identifiers, and sanitized output when possible. Do not include confidential or personal data.

## Supported versions and remediation

No formal supported-version matrix or remediation SLA has been established yet. Until one is published, report issues against the current default branch and include the commit or version where the issue was observed.

## Disclosure

Please allow maintainers time to verify and address a report before public disclosure. Once a fix is available, the project may publish a security advisory describing the impact and mitigation without exposing sensitive exploit details.

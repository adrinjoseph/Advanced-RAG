# Security Policy

## Supported versions

Only the `main` branch receives security fixes. No older tags or branches
are maintained.

| Branch / tag | Supported |
|---|---|
| `main` | Yes |
| Any other | No |

## Reporting a vulnerability

**Do not open a public GitHub issue for a security vulnerability.**

Please use GitHub's private vulnerability reporting instead:

1. Go to the **Security** tab of this repository.
2. Click **Report a vulnerability**.
3. Fill in the description, reproduction steps, and impact.

You should receive an acknowledgement within a few days. This is a solo
portfolio project — there is no security team and no guaranteed response
timeline. I will make a genuine effort to triage and fix valid reports.

## What to include

A useful report contains:

- A clear description of the vulnerability and what it allows an attacker to do.
- Step-by-step reproduction instructions.
- The affected component (ingestion pipeline, retrieval, auth, guardrails, etc.).
- The potential impact (data leakage, privilege escalation, denial of service, etc.).
- A suggested fix if you have one (optional but appreciated).

## Scope

This policy covers the application code in this repository only.

**In scope:**
- Authentication and authorization bypass
- Cross-tenant data leakage (collection isolation failures)
- SQL injection or unintended data access via retrieval paths
- Prompt injection leading to data exposure
- Insecure file handling or path traversal in the upload pipeline
- Secrets or credentials exposed in logs, images, or API responses

**Out of scope:**
- Vulnerabilities in upstream dependencies (ParadeDB, pgvector, Groq, Chainlit).
  Report those to the respective projects.
- The Azure infrastructure itself (report to Microsoft).
- Theoretical or unproven risks with no reproduction path.
- Denial-of-service via resource exhaustion against a demo instance
  (rate limits are enforced by design).

## Disclosure

Once a fix is confirmed and merged, I will acknowledge the report in the
`CHANGELOG.md` under the relevant release. I will not disclose your identity
without your permission.
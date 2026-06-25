---
name: quick-security-audit
description: Fast security review for code changes. Use before quick merges, small patches, or low-risk edits. Designed to rapidly catch critical vulnerabilities without full deep-dive analysis.
---

---

# Quick Security Audit

## Overview

A lightweight security gate for fast-moving development. This is **not a full audit**—it is a rapid scan focused on catching high-impact vulnerabilities.

Use this when speed matters but security still cannot be skipped.

**Goal:** Catch obvious and exploitable issues in under a few minutes per change.

This prompt is intended for changes that are small, have a limited trust boundary impact, and do not introduce new architectural risk. It is a fast first pass, not a final approval for major security-sensitive work.

### Purpose

The quick security audit is designed to:

- Identify clear vulnerabilities and risky patterns early.
- Prevent obvious security issues from slipping into fast-moving edits.
- Provide a repeatable, lightweight gate for small changes.

It is optimized for speed and clarity, not completeness.

---

## When to Use

- Small or low-risk PRs
- Hotfixes and patches
- Minor refactors near sensitive code
- AI-generated code with limited scope
- Pre-merge sanity check after deeper audits already done
- Quick reviews of configuration or instrumentation changes
- Simple bug fixes that touch authentication or input handling

**When NOT to use:**

- Large, complex, or high-risk changes
- New APIs, services, or endpoints
- Changes that add stateful storage, cross-service trust, or multi-tenant logic
- Major architectural, authorization, or cryptography work

For those, perform a full security audit.

---

## What this audit is not

- Not a replacement for a full threat model when trust boundaries change.
- Not a substitute for penetration testing or security architecture review.
- Not sufficient for authorization design, cryptography, or multi-tenant systems.
- Not for changes that introduce new service-to-service trust, persistent storage, or customer-facing APIs.
- Not a thorough dependency vulnerability scan.

---

## How to use this prompt

1. Scan the code quickly and identify the trust boundaries.
2. Apply the checklist in order of highest risk first.
3. If any item fails, stop and escalate or require a fix.
4. If the change is outside scope, do not use this prompt.

This prompt is for a human or agent doing a rapid security sanity check, not for automated deep analysis.

---

## Rapid Security Checklist

### 1. Input Safety (Fast Scan)

- [ ] Are inputs from users, APIs, or external systems validated before use?
- [ ] Is any raw input used directly in business logic, database queries, shell commands, or templates?
- [ ] Are type and format expectations enforced for external data?
- [ ] Is there any implicit trust in headers, cookies, JSON bodies, or query parameters?
- [ ] Are defaults safe when inputs are missing or malformed?

**Red flag:** raw input used without validation, escaping, or sanitization.

#### Fast input safety heuristics

- Input should be validated as close to the boundary as possible.
- Prefer allow-lists over deny-lists for formats and values.
- Treat any external data as untrusted unless explicitly validated.
- Avoid using data directly from request headers, cookies, or query strings in security decisions.

### 2. Injection Risks (Critical)

- [ ] No SQL/NoSQL queries built by string concatenation with user data.
- [ ] No shell command or OS command execution with untrusted input.
- [ ] No template rendering of user-controlled data without sanitization.
- [ ] No file paths or filenames derived directly from user input.
- [ ] No dynamic code execution based on external strings.
- [ ] No unsafe deserialization of external data.

**Critical:** any confirmed injection vector = block.

#### Injection risk examples

- `SELECT * FROM users WHERE id = "${userId}"`
- `os.system("rm -rf " + filename)`
- `render_template(request.args.get('template'))`
- `eval(payload)` or similar dynamic execution
- `yaml.load()` or unsafe deserialization without explicit schema

### 3. Auth & Authorization Checks

- [ ] Are new endpoints protected by authentication?
- [ ] Is there explicit authorization for sensitive operations?
- [ ] Are role/ownership checks present where needed?
- [ ] Does the change add a path that bypasses existing access controls?
- [ ] Are any security-critical operations reachable from unauthenticated or low-privilege contexts?

**Red flag:** endpoint or action callable without appropriate permission checks.

#### Auth/authorization focus points

- Authentication ensures identity; authorization ensures permission.
- Check service-to-service calls for implicit trust assumptions.
- Server-side authorization is required even if the client UI already hides controls.
- Guard all sensitive operations, not just the main endpoint.

### 4. Data Leakage

- [ ] Are secrets or credentials accidentally hardcoded or returned?
- [ ] Are logs exposing sensitive or PII data?
- [ ] Are stack traces or internal error details sent to end users?
- [ ] Are sensitive fields excluded or masked in API responses?
- [ ] Are debug or test-only values accidentally exposed in production code?

**Note:** sometimes data leakage is an operational issue even if the code is functionally correct.

#### Data leakage examples

- `print(api_key)` or logging entire request bodies
- returning raw database rows that include passwords, tokens, or SSNs
- exposing internal config values or endpoint URLs in error messages
- sending stack traces to browser responses in production

### 5. Secrets & Configuration

- [ ] No hardcoded API keys, tokens, passwords, or certificates.
- [ ] Secrets are read from environment variables or secure stores.
- [ ] Configuration values are not leaked through error messages or logs.
- [ ] Default credentials or insecure config values are not introduced.
- [ ] Any secret rotation or expiration behavior is not broken by the change.

#### Secrets hygiene checks

- Check for literal strings containing words like `key`, `secret`, `token`, `password`, `credential`.
- Ensure secrets are not committed in code or config templates.
- Prefer existing secret management patterns in the codebase.
- Ensure runtime config is validated and fails fast for missing required secrets.

### 6. External Input (APIs / Webhooks)

- [ ] Is external data treated as untrusted?
- [ ] Are webhooks, callbacks, or third-party payloads verified with signatures or tokens?
- [ ] Are timeouts and failure modes handled safely to avoid DoS or hanging operations?
- [ ] Is the trust boundary clearly identified for any inbound external data?
- [ ] Are API responses validated before they are consumed?

#### External input quick checks

- External services are untrusted by default.
- Verify the authenticity of inbound webhooks and callbacks.
- Apply strict parsing for external payloads and reject unknown fields when possible.
- Do not depend on external systems for authorization decisions without verification.

### 7. Dependencies (Quick Check)

- [ ] No obviously suspicious or unmaintained dependency added.
- [ ] No large or unnecessary library added for a small change.
- [ ] No “experimental” or untrusted package pulled in without justification.
- [ ] Existing dependencies are reused instead of adding new ones where possible.
- [ ] No dependency adds direct execution of third-party code in a sensitive path.

#### Dependency guidance

- Small changes should rarely require new dependencies.
- Prefer standard library or existing shared utilities.
- Dependencies in security-critical paths deserve extra scrutiny.
- Avoid new packages that are not actively maintained or widely trusted.

---

## Fast Mental Model

Ask quickly:

- Can a user do something they shouldn’t?
- Can input become code, query, or a file path?
- Can data leak outside its intended boundary?
- Can this be abused without authentication or authorization?
- Is any new trust boundary added by this change?
- Does the change expose a previously hidden error path?

If **yes** to any → stop and investigate deeper, or escalate to a fuller audit.

### Trust boundary shorthand

Think in terms of boundaries:

- User input → service logic
- External API → internal state
- Service-to-service call → local authorization
- File system / OS command → process environment
- Secrets / config → runtime behavior

If boundary control is unclear, the change is likely out of scope for this quick audit.

---

## Severity Rules

| Level         | Meaning                   | Action               |
| ------------- | ------------------------- | -------------------- |
| **Critical:** | Exploitable vulnerability | Block merge          |
| **Issue:**    | Security weakness         | Fix required if easy |
| **Note:**     | Minor hardening           | Optional             |

Use **Critical** for anything that can be exploited directly, especially injection, auth bypass, or data exposure. Use **Issue** for code that weakens security posture but does not immediately expose a vulnerability.

### What belongs in each bucket

- Critical: SQL injection, command injection, auth bypass, open redirect, secret exposure.
- Issue: insecure defaults, missing validation, weak error handling, poor logging of sensitive data.
- Note: style issues, better secret handling, caching or performance-related hardening.

---

## Example Findings

- **Critical:** "SQL query is concatenated with user input, creating an injection risk."
- **Critical:** "This webhook endpoint accepts unsigned payloads from external origins."
- **Critical:** "Authentication is not enforced on a sensitive admin endpoint."
- **Issue:** "The endpoint logs request bodies containing user email addresses."
- **Issue:** "A new dependency is added without review and is marked experimental."
- **Issue:** "The change uses `eval()` on external data, which is unsafe."
- **Note:** "The change relies on environment variables, but there is no fallback or validation."
- **Note:** "The error message is too verbose and could expose internal implementation details."

---

## Quick Validation Guidance

When the checklist is mostly green, verify these additional fast signals:

- Are there any obvious error conditions that are unhandled?
- Does the code fail safely under unexpected input?
- Is the trust boundary clearly documented in comments or naming?
- Are any new secrets or credentials being introduced accidentally?
- Would a reviewer unfamiliar with the code be able to identify the likely security risk?
- Are there any implicit assumptions about environment, config, or deployment?
- Does the change introduce any new control flow that bypasses existing security checks?

### Quick red flags to surface

- Unvalidated redirects or URL construction from user input.
- New file or path handling based on external input.
- Authentication status used as authorization without further checks.
- Error messages containing stack traces or raw exception details.
- Added debug code left in production paths.

---

## Quick Verdict

- [ ] **Approve** — no obvious security issues and the change is within the quick-audit scope.
- [ ] **Request fix** — potential vulnerability detected, requires remediation before merging.
- [ ] **Escalate to full audit** — unclear risk, new trust boundary, or high-risk change that exceeds quick audit coverage.

### Approval guidance

- Approve only if the change stays within scope and no critical risks are found.
- If the change is functional but has issues, prefer "Request fix" over approval.
- If the change touches a new trust boundary or the risk is uncertain, choose "Escalate to full audit."

---

## Non-Negotiable Rule

If something _feels_ like it touches trust boundaries, external execution, sensitive data, or authorization, **don’t speed past it**—escalate.

This audit is a fast gate, not a reason to skip security thinking.

### Bottom line

A quick audit should eliminate obvious security mistakes, not certify comprehensive safety. If the change is anything more than a focused small patch, switch to a deeper review.

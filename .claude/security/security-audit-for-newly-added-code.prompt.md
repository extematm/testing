---
name: security-audit-for-newly-added-code
description: Performs a structured security audit of newly added or modified code. Use before merging any change that introduces or modifies code paths handling input, data flow, authentication, authorization, dependencies, or external interfaces. Use when reviewing code written by yourself, another agent, or a human to identify vulnerabilities and hardening gaps.
---

---

# Security Audit for Added Code

## Overview

This is a focused security review process for all code changes. It ensures that every modification is evaluated for security risks before it reaches the main branch.

Security is treated as a **hard gate for Critical findings** and a **risk-managed decision space for non-critical issues**.

The goal is not theoretical perfection but **preventing exploitable vulnerabilities in production systems**.

## When to Use

- Before merging any PR that touches:
  - authentication or authorization logic
  - input handling or validation
  - API endpoints or external interfaces
  - database queries or persistence layers
  - file handling, uploads, or downloads
  - dependency updates or additions

- After implementing features that introduce new data flows
- After refactoring security-relevant code paths
- After bug fixes involving access control, injection, or data leakage
- When reviewing AI-generated or third-party code

## Security Audit Dimensions

Every review evaluates the change across the following security domains:

---

### 1. Input Validation & Trust Boundaries

All external data must be treated as untrusted.

- Is all user input validated at system boundaries?
- Are schema validations strict (types, ranges, formats)?
- Are missing/extra fields handled safely?
- Is there implicit trust in headers, cookies, query params, or request bodies?
- Are deserialization operations safe (no unsafe object reconstruction)?
- Are file uploads validated for type, size, and content?

**Red Flags:**

- Direct use of raw input in logic or queries
- “Assumed safe” internal APIs without validation
- Weak or missing schema validation

---

### 2. Injection Risks (Critical Focus Area)

Check for all forms of injection:

- SQL/NoSQL injection (string concatenation in queries)
- Command injection (shell execution with user input)
- LDAP/XPath injection
- Template injection (server-side rendering contexts)
- Header injection (HTTP response splitting)
- Path traversal (`../` sequences in file access)

**Required checks:**

- Parameterized queries are used everywhere
- No string interpolation into execution contexts
- File paths are normalized and sandboxed

**Critical:**
Any confirmed injection vulnerability is an immediate **blocker**.

---

### 3. Authentication & Session Integrity

- Is authentication enforced where required?
- Are session tokens securely generated and stored?
- Are tokens validated on every sensitive operation?
- Are session expirations implemented correctly?
- Are password storage mechanisms secure (hashed + salted)?
- Are MFA or additional controls required for sensitive actions?

**Red Flags:**

- Missing auth checks on privileged endpoints
- Token reuse or predictable session identifiers
- Auth logic duplicated inconsistently across services

---

### 4. Authorization & Access Control

Authentication ≠ authorization.

- Are role-based or attribute-based access controls enforced?
- Is every sensitive operation checking permissions explicitly?
- Are there privilege escalation paths?
- Can users access or modify resources they do not own?

**Required checks:**

- Authorization checks happen server-side (never client-trusted)
- Object-level access control (not just endpoint-level)

**Critical:**
Any horizontal or vertical privilege escalation vulnerability is a blocker.

---

### 5. Data Exposure & Information Leakage

- Are sensitive fields excluded from logs and responses?
- Are error messages overly verbose (stack traces, internal states)?
- Is PII properly protected or masked?
- Are debug flags disabled in production paths?
- Are secrets ever embedded in responses, logs, or exceptions?

**Red Flags:**

- Logging full request/response bodies containing sensitive data
- Returning internal errors to clients
- Exposing database schema or system internals

---

### 6. Cryptography & Secret Management

- Are secrets stored in environment variables or secret managers?
- Are cryptographic primitives standard and not custom-built?
- Are encryption keys rotated and managed properly?
- Are weak algorithms avoided (MD5, SHA1, ECB mode)?
- Are random values generated using secure RNGs?

**Critical:**

- Hardcoded secrets
- Custom encryption schemes
- Insecure randomness in security contexts

---

### 7. Dependency & Supply Chain Risk

- Are new dependencies necessary and minimal?
- Are they actively maintained and trusted?
- Are known vulnerabilities present (`CVE`, audit tools)?
- Are transitive dependencies introducing risk?

**Red Flags:**

- Unmaintained packages with security issues
- Over-reliance on large, unnecessary libraries
- Direct execution of third-party code without validation

---

### 8. External Data Handling & Integration Security

- Are external API responses validated before use?
- Is data from third-party services treated as untrusted?
- Are retries, timeouts, and failure modes safe?
- Are webhook signatures verified?

**Red Flags:**

- Trusting external API responses without validation
- Missing signature verification for webhooks
- No timeout handling (DoS risk via hanging requests)

---

### 9. File System & Resource Safety

- Are file operations constrained to safe directories?
- Is path traversal prevented?
- Are temporary files handled securely?
- Are resource limits enforced (size, count, recursion depth)?

**Critical:**

- Arbitrary file read/write access from user input

---

### 10. Logging, Monitoring & Auditability

- Are security-relevant actions logged?
- Are logs tamper-resistant and structured?
- Are sensitive values excluded from logs?
- Is there traceability for authentication and authorization decisions?

**Red Flags:**

- Logging secrets or tokens
- No audit trail for privileged actions
- Inconsistent logging across services

---

## Review Severity Classification

Each issue must be categorized:

| Prefix          | Meaning               | Action                                |
| --------------- | --------------------- | ------------------------------------- |
| _(none)_        | Required fix          | Must be resolved before merge         |
| **Critical:**   | Security exploit      | Immediate blocker                     |
| **Important:**  | Significant risk      | Must be fixed or explicitly justified |
| **Suggestion:** | Hardening improvement | Optional but recommended              |
| **FYI:**        | Informational         | No action required                    |

---

## Review Process

### Step 1: Map Trust Boundaries

Identify:

- Entry points (APIs, UI, CLI, webhooks)
- Data sources (external/internal)
- Sensitive operations (auth, payments, data access)

---

### Step 2: Trace Data Flow

For each input source:

- Where does it originate?
- How is it validated?
- Where does it propagate?
- Where is it executed or stored?

---

### Step 3: Evaluate Security Controls

Check:

- Validation
- Authentication
- Authorization
- Sanitization/encoding
- Logging safety

---

### Step 4: Identify Exploit Paths

Ask explicitly:

- Can a user escalate privileges?
- Can input be used to execute unintended code?
- Can data be accessed cross-user or cross-tenant?
- Can the system be disrupted (DoS)?

---

### Step 5: Categorize and Report Findings

Each issue must include:

- Location (file/function)
- Risk description
- Exploit scenario (how it could be abused)
- Severity label

---

## Mandatory Security Checklist

```markdown
## Security Review: [Change Title]

### Context Understanding

- [ ] I understand all entry points and data flows

### Input Safety

- [ ] All inputs validated at boundaries
- [ ] No unsafe deserialization
- [ ] No trust in raw external input

### Injection Prevention

- [ ] Parameterized queries used
- [ ] No command injection vectors
- [ ] No template injection risks

### AuthN/AuthZ

- [ ] Authentication enforced where required
- [ ] Authorization checked per sensitive operation
- [ ] No privilege escalation paths

### Data Protection

- [ ] No sensitive data leaked in logs or responses
- [ ] Errors do not expose internals

### Secrets & Crypto

- [ ] No hardcoded secrets
- [ ] Secure cryptographic primitives used

### Dependencies

- [ ] No vulnerable or untrusted dependencies added

### External Integrations

- [ ] External data validated
- [ ] Webhooks verified

### Files & Resources

- [ ] No path traversal risks
- [ ] Resource limits enforced

### Verdict

- [ ] **Approve**
- [ ] **Request changes (security fix required)**
```

---

## Hard Gate Rules

- Any **Critical issue = automatic block**
- Any unresolved **Important issue requires justification**
- Security review cannot be bypassed for “small changes” if trust boundaries are affected
- “Works in testing” is not a security argument

---

## Common Security Anti-Patterns

| Pattern                          | Risk                                  |
| -------------------------------- | ------------------------------------- |
| “We trust internal services”     | Internal ≠ safe                       |
| “Input is validated on frontend” | Client-side validation is bypassable  |
| “It’s just an admin tool”        | Admin tools are high-value targets    |
| “No one would try that”          | Security assumes attackers will       |
| “We’ll fix it later”             | Deferred security fixes rarely happen |

---

## Verification Requirements

Before approval:

- [ ] All Critical issues resolved
- [ ] All Important issues resolved or explicitly risk-accepted
- [ ] No unreviewed trust boundary changes
- [ ] Security checklist completed
- [ ] Exploit paths considered and addressed

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

---

## When to Use

- Small or low-risk PRs
- Hotfixes and patches
- Minor refactors near sensitive code
- AI-generated code with limited scope
- Pre-merge sanity check after deeper audits already done
- **When NOT to use:** Large, complex, or high-risk changes. For those, perform a full security audit.

---

## Rapid Security Checklist

### 1. Input Safety (Fast Scan)

- [ ] Any user input validated?
- [ ] Any raw input directly used in logic, queries, or execution?
- [ ] Any missing type/format checks on external data?

**Red flag:** raw input used without validation, escaping, or sanitization

---

### 2. Injection Risks (Critical)

- [ ] No string-built SQL/queries
- [ ] No shell command construction with input
- [ ] No template rendering with unsanitized data
- [ ] No path traversal risks (`../`, absolute paths from input)

**Critical:** any injection vector = block

---

### 3. Auth Checks

- [ ] Sensitive endpoints require authentication?
- [ ] Authorization checked (not just authentication)?
- [ ] No missing access control on new functions?

**Red flag:** endpoint callable without permission check

---

### 4. Data Leakage

- [ ] No secrets in logs or responses
- [ ] No stack traces exposed to users
- [ ] No sensitive fields returned unintentionally

---

### 5. Secrets & Config

- [ ] No hardcoded API keys, tokens, passwords
- [ ] Secrets loaded from environment or secure store

---

### 6. External Input (APIs / Webhooks)

- [ ] External data treated as untrusted
- [ ] Webhooks verified (signature / token) if applicable
- [ ] Timeouts / failures handled safely

---

### 7. Dependencies (Quick Check)

- [ ] No obviously suspicious new dependency
- [ ] No large/unnecessary additions
- [ ] No known “experimental” or untrusted libs

---

## Severity Rules

| Level         | Meaning                   | Action               |
| ------------- | ------------------------- | -------------------- |
| **Critical:** | Exploitable vulnerability | Block merge          |
| **Issue:**    | Security weakness         | Fix required if easy |
| **Note:**     | Minor hardening           | Optional             |

---

## Fast Mental Model

Ask quickly:

- Can a user do something they shouldn’t?
- Can input become code or query?
- Can data leak outside its boundary?
- Can this be abused without authentication?

If **yes** to any → stop and investigate deeper.

---

## Quick Verdict

- [ ] **Approve** — no obvious security issues
- [ ] **Request fix** — potential vulnerability detected
- [ ] **Escalate to full audit** — unclear or high-risk change

---

## Non-Negotiable Rule

If something _feels_ like it touches trust boundaries or execution paths, **don’t speed past it**—escalate.

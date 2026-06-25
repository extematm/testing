---
name: risk-classification-gate
description: Classifies code changes by risk level and determines required review depth.
---

# Risk Classification Gate

## Overview

This prompt assigns a risk tier to a code change so reviewers can choose the correct depth of review.

It is designed to help teams avoid under-reviewing high-risk changes and over-reviewing trivial edits.

### Purpose

- Surface the trust boundaries affected by a change.
- Classify impact on security, data, and downstream consumers.
- Route the change to the appropriate review process.

---

## Classification Principles

Classify risk by answering these questions:

- Does the change affect sensitive data, authentication, or authorization?
- Does it alter core business behavior or shared infrastructure?
- Does it introduce a new public or internal contract?
- Does it depend on or change service-to-service trust?
- Could the change break backward compatibility for clients or APIs?

If the answer is yes to any of these, the risk level should be higher.

---

## Risk Levels

### LOW

Changes with a small surface area, low impact, and minimal trust boundary exposure.

Typical examples:

- UI text updates and layout-only changes
- Local refactors inside a single module
- Non-critical formatting or presentation logic
- Documentation and comment improvements
- Small test-only changes or mocks

Review scope:

- Quick review or lightweight sanity check
- No security audit required unless the change touches sensitive code

### MEDIUM

Changes that affect business logic, internal APIs, or data transformations without touching sensitive security boundaries.

Typical examples:

- Internal data shaping and normalization
- Validation logic for non-sensitive inputs
- Internal endpoint or service interface changes
- Non-critical workflow adjustments
- Performance improvements in bounded code paths

Review scope:

- Standard review with behavioral and compatibility checks
- Consider adding regression tests and integration checks

### HIGH

Changes that affect shared utilities, external integration, or security-adjacent behavior.

Typical examples:

- Authorization rules or permission checks
- Payment or billing-related logic
- External API contracts and third-party integrations
- Shared libraries, common helpers, or platform utilities
- Feature flags that change runtime behavior

Review scope:

- Full review including architecture, security, and compatibility
- Focus on shared impact, reuse, and downstream consumers

### CRITICAL

Changes that touch core security, identity, data persistence, or trust boundaries.

Typical examples:

- Authentication, authorization, and identity systems
- Data persistence, storage schema, or migration logic
- Encryption, secrets management, or token issuance
- Multi-tenant isolation and access control
- Any new public-facing API with sensitive data exposure

Review scope:

- Full security audit required
- Threat modeling, data flow analysis, and regression risk review
- Consider additional manual review or security sign-off

---

## Routing Logic

Route the change to the review process as follows:

- LOW → quick review
- MEDIUM → standard review
- HIGH → full review
- CRITICAL → full security audit required

### When to escalate

Even if the initial risk appears lower, escalate when:

- the change impacts a shared dependency used by multiple teams
- it touches a boundary between internal and external systems
- behavior changes are not fully covered by tests
- there is uncertainty about backward compatibility or failure modes

---

## Evaluation Checklist

Use this checklist to determine the correct risk tier:

- [ ] Does the change affect user-facing or API contract behavior?
- [ ] Does it touch authentication, authorization, or access control?
- [ ] Does it affect storage, data schema, or persistence behavior?
- [ ] Does it change shared utilities, libraries, or platform code?
- [ ] Does it alter external integrations, callbacks, or third-party API usage?
- [ ] Does it introduce a new service-to-service trust boundary?
- [ ] Does it involve secrets, tokens, or cryptographic operations?
- [ ] Is backward compatibility important for this change?
- [ ] Does the change affect business-critical workflows or compliance-sensitive data?

Assign risk based on how many of these checks are true and how severe the impacted area is.

---

## Output

- LOW
- MEDIUM
- HIGH
- CRITICAL

### Decision guidance

- Choose **LOW** when the change is isolated and has limited impact.
- Choose **MEDIUM** when the change affects logic or data but does not cross sensitive boundaries.
- Choose **HIGH** when the change affects shared services, external interactions, or security-related behavior.
- Choose **CRITICAL** when the change touches identity, persistence, secrets, or any core trust boundary.

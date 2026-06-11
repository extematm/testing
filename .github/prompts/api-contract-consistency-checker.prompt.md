---
name: api-contract-consistency-checker
description: Reviews API contract changes in depth and determines whether schema or semantic updates preserve compatibility, require versioning, or introduce contract drift between services.
---

# API Contract Consistency Checker

## Overview

Analyze API contract changes with a focus on compatibility, consumer impact, and contract intent.
This checker should determine whether proposed API modifications preserve prior behavior for existing consumers, introduce breaking contract changes, or create inconsistencies across services or versions.

A strong response explains why a change is safe or risky, identifies the exact compatibility impact, and recommends whether versioning or migration guidance is needed.

## When to Use

- Reviewing changes to public REST, GraphQL, gRPC, or internal service APIs
- Validating request/response schema changes in OpenAPI, protobuf, or shared DTOs
- Detecting contract drift between services that share the same API or schema
- Determining whether API changes require a version bump, deprecation path, or migration plan
- Evaluating API behavior during PR reviews, architecture reviews, or integration validation

**When NOT to use:**

- For implementation-level refactors that do not change the API surface
- For purely performance, style, or build-system reviews
- For general architecture decisions unrelated to API contract compatibility
- For documentation that does not address contract behavior or compatibility

## Compatibility Principles

- APIs are contracts. Compatibility should be treated as a first-class requirement.
- Backward compatibility means existing consumers continue to work without code changes.
- Additive changes should be optional and safely ignorable by older clients.
- Renames, removals, and type changes are breaking unless explicitly versioned or bridged.
- Shared contracts must remain aligned across services and versions.

## Evaluation Criteria

### Schema Stability

Verify whether request and response shapes remain compatible.

- Are payload fields added, removed, renamed, or retyped?
- Are object shapes, arrays, or nested structures changed so older clients cannot parse them?
- Are enums, status codes, or response envelopes changed in a way that breaks consumers?
- Are headers, query parameters, or request metadata semantics altered?

### Backward Compatibility

Determine whether existing consumers can continue operating unchanged.

- Are new fields optional or safely defaultable for older clients?
- Are required fields introduced with a compatibility path?
- Are deprecated fields preserved, aliased, or mapped for legacy support?
- Can older clients still parse responses and error payloads reliably?

### Versioning Discipline

Assess whether the change requires explicit versioning, migration planning, or compatibility notice.

- Does the change introduce a non-backward-compatible contract difference?
- Is it being made under the same published API/version without a clear migration path?
- Should the API or schema version be incremented, or should a new endpoint be published?
- Is there a documented deprecation or upgrade path for impacted consumers?

### Cross-Service and Cross-Version Consistency

Confirm that contract expectations are aligned across boundaries.

- Do services that share a contract use consistent field names, types, and error semantics?
- Is a shared DTO diverging between producer and consumer implementations?
- Are API versions or endpoint variants inconsistent in payload shape or semantics?
- Are client-facing and backend-facing expectations aligned?

### Breaking Change Detection

Identify explicit and subtle breaking contract changes.

- Removed or renamed fields
- Incompatible type changes
- Changed required/optional status
- Changed error payloads, status codes, or retry semantics
- Removed endpoints, renamed paths, or altered request semantics
- Changed pagination, partial update, or default behavior

## Output Decision

- SAFE: No compatibility risk detected. The change preserves contract behavior and compatibility.
- BACKWARD_COMPATIBLE: The change extends the API while preserving existing consumer compatibility.
- BREAKING_CHANGE: The change alters the contract in a way that may break current consumers and should trigger versioning, migration guidance, or coordination.

## Guidance for Responses

- Prefer `SAFE` when the change does not alter existing contract expectations.
- Prefer `BACKWARD_COMPATIBLE` when the change is additive and older clients can continue unchanged.
- Prefer `BREAKING_CHANGE` when existing consumers may fail, misinterpret, or receive invalid data.
- Explain the rationale in terms of consumer behavior and contract semantics, not implementation details.
- Call out cross-service drift explicitly when shared schemas or DTOs are inconsistent.

## Examples

### Safe additive change

- Added an optional `metadata` field to an existing response object.
- Older clients ignore unknown fields and continue working.
- Output: `BACKWARD_COMPATIBLE`

### Breaking rename

- Renamed request field `userId` to `accountId` without compatibility aliases.
- Older clients still send `userId` and are rejected or misrouted.
- Output: `BREAKING_CHANGE`

### Cross-service drift

- Service A uses `status: "pending" | "complete"`, while Service B expects numeric status values.
- Shared contract expectations diverge even if neither service changed its own schema.
- Output: `BREAKING_CHANGE`

### Versioning required

- Removed a previously returned response field or changed a field type in a public API.
- This should be treated as a breaking change requiring a version bump or migration plan.
- Output: `BREAKING_CHANGE`

## Common Failure Modes

- Treating additive schema changes as safe without verifying legacy client behavior
- Changing optional fields to required without compatibility support
- Renaming or removing fields in the same published version
- Diverging shared schemas across services
- Changing error shapes or status codes without documenting the impact

## Verification

After evaluating a change, ensure:

- The compatibility risk is clearly identified.
- The selected decision matches the impact on existing consumers.
- Breaking or risky changes include versioning or migration guidance.
- Cross-service or cross-version inconsistencies are explicitly noted.
- Reasoning focuses on contract semantics rather than internal implementation.

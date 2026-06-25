---
name: api-contract-consistency-checker
description: Reviews API contract changes in detail and determines whether schema or semantic updates preserve compatibility, require versioning, or introduce contract drift across services.
---

# API Contract Consistency Checker

## Overview

This prompt evaluates API contract changes with a sharp focus on compatibility, consumer impact, and contract intent.
It should clearly determine whether proposed API modifications:

- preserve existing behavior for current consumers,
- introduce breaking contract changes,
- require explicit versioning or migration guidance,
- or create inconsistent expectations across services and versions.

A good response does more than select a label. It explains the compatibility impact, highlights risks, and gives precise reasoning in terms of consumer behavior.

## Why This Matters

APIs connect systems, teams, and users. Contract changes can cause:

- production failures for existing clients,
- silent integration regressions,
- divergence between service implementations,
- and slowed API evolution if compatibility is not validated.

Use this prompt to protect API consumers and keep contract changes deliberate.

## When to Use

- Reviewing public or internal REST, GraphQL, gRPC, or RPC-style API changes
- Validating schema updates in OpenAPI, protobuf, TypeScript interfaces, JSON schemas, or shared DTOs
- Detecting contract drift between services that rely on the same API or schema
- Determining whether changes require version bumps, deprecation notices, or migration plans
- Evaluating API behavior during PR reviews, architecture reviews, or integration validation
- Verify that changes are additive, backward compatible, and aligned with versioning discipline

## When NOT to Use

- For implementation-only refactors that do not change the API surface
- For performance, style, build-system, or tooling reviews
- For broad architecture decisions unrelated to API compatibility
- For documentation tasks that do not concern API contract semantics
- For general code quality or maintainability reviews unrelated to API contracts

## Audience and Scope

This prompt is intended for reviewers, architects, and agents checking API compatibility and contract consistency.
Focus on API surface, consumer-facing behavior, and versioning discipline. Do not treat it as a general code-quality review.
Do not evaluate internal implementation details, performance optimizations, or unrelated refactors unless they directly affect the API contract.

## Compatibility Principles

- APIs are contracts. Evaluate changes from the consumer's perspective.
- Backward compatibility means existing consumers continue to work unchanged.
- Additive changes are safe only when older clients can ignore them.
- Renames, removals, and incompatible type changes are breaking unless versioned or bridged.
- Shared schemas and DTOs must remain aligned between producers and consumers.
- Versioning discipline is essential for non-backward-compatible changes.

## Key Definitions

### Backward Compatibility

A change is backward compatible when existing clients can continue to work without modification.
This means:

- old request shapes are still accepted,
- old response formats are still parseable,
- error structures remain consistent,
- documented behavior does not change unexpectedly.
- always consider the consumer's perspective, not just the producer's implementation.
- do not assume that all clients are updated in lockstep with API changes.
- consider optional fields, default values, and validation rules when evaluating backward compatibility.
- check that shared schemas or DTOs remain consistent across services and versions.

### Breaking Change

A breaking change is any modification that may cause at least one existing consumer to fail, behave incorrectly, or receive invalid data.
Breaking changes usually require versioning, migration instructions, or a compatibility bridge.
Ensure that breaking changes are clearly documented and communicated to all affected consumers.
Validate that breaking changes are intentional and necessary, and consider whether they can be avoided or mitigated through additive changes or versioning.

### Contract Drift

Contract drift happens when shared API expectations diverge between services or versions.
This can create compatibility risk even if a single service has not changed its own contract.
An example is when two services share a Data Transfer Object (DTO) but interpret its fields differently, leading to miscommunication.

### Versioning Discipline

Non-backward-compatible changes should be explicit.
This may mean a new API version, a new endpoint, or a documented migration and deprecation plan.
Always consider the impact on existing consumers and provide clear guidance for upgrading or migrating to the new contract.

## Evaluation Criteria

### Schema Stability

Check that request and response shapes remain compatible with current expectations.

- Are payload fields added, removed, renamed, or retyped?
- Are object shapes, arrays, or nested structures changed so older clients cannot parse them?
- Do enum changes or status code updates break existing clients?
- Are request headers, query parameters, or response envelopes altered?
- Is the error response shape preserved?

### Backward Compatibility

Verify that existing consumers can continue operating unchanged.

- Are new fields optional or safely defaultable for older clients?
- Are required fields introduced with a compatibility fallback?
- Are deprecated fields preserved, aliased, or mapped for legacy clients?
- Can older clients still parse responses, error payloads, and status semantics?
- Do new validation rules reject requests that were previously valid?

### Forward Compatibility

Consider whether newer client expectations can coexist with older servers.

- Can newer clients gracefully handle older responses?
- Are new fields and options optional for older servers?
- Is the API evolution plan clear for both old and new consumers?

### Versioning Discipline

Determine whether explicit versioning or a migration plan is required.

- Does the change introduce a non-backward-compatible contract difference?
- Is the change being made in the same published API/version without a migration path?
- Should the API or schema version be incremented, or should a new endpoint be published?
- Is there a documented deprecation or upgrade path for impacted consumers?
- Has the change been categorized correctly for major, minor, or patch-level compatibility?

### Cross-Service and Cross-Version Consistency

Check whether shared contract expectations are aligned across boundaries.

- Do services that share the same contract agree on field names, types, and error semantics?
- Is a shared DTO diverging between producer and consumer implementations?
- Are API versions or endpoint variants inconsistent in payload shape or semantics?
- Are client-facing and backend-facing expectations aligned?
- Do multiple services interpret the same schema differently?

### Breaking Change Detection

Identify explicit and subtle breaking contract changes.

- Removed or renamed fields
- Incompatible type changes
- Changed required/optional status
- Changed error payloads, status codes, or retry semantics
- Removed endpoints, renamed paths, or altered request semantics
- Changed pagination, partial update, or default behavior
- Changed default values or response contract assumptions
- Changed authorization or security behavior tied to API shape

## Decision Matrix

- SAFE: No compatibility risk detected. Changes preserve existing contract behavior and consumer assumptions.
- BACKWARD_COMPATIBLE: Changes extend the API while preserving compatibility for existing consumers.
- BREAKING_CHANGE: Changes alter the contract in a way that may break current consumers and should trigger versioning, migration guidance, or coordination.

## Response Requirements

- Always return one of: `SAFE`, `BACKWARD_COMPATIBLE`, or `BREAKING_CHANGE`.
- Explain the decision in terms of consumer impact, compatibility assumptions, and contract semantics.
- Do not answer with vague generalities. Be specific about what changed and why it matters.
- When the change is safe, state which client assumptions remain valid.
- When the change is breaking, state which existing expectation is violated.

## Examples

### Example 1: Safe additive change

- Added an optional `metadata` field to an existing response object.
- Older clients ignore unknown fields and continue working.
- Output: `BACKWARD_COMPATIBLE`

### Example 2: Breaking rename

- Renamed request field `userId` to `accountId` without compatibility aliases or fallback handling.
- Older clients still send `userId` and are rejected or misrouted.
- Output: `BREAKING_CHANGE`

### Example 3: Cross-service drift

- Service A uses `status: "pending" | "complete"` while Service B expects numeric status values.
- Shared contract expectations diverge even if neither service changed its own schema.
- Output: `BREAKING_CHANGE`

### Example 4: Versioning required

- Removed a previously returned response field or changed a field type in a public API.
- This should be treated as a breaking change requiring a version bump or migration plan.
- Output: `BREAKING_CHANGE`

### Example 5: Safe error extension

- Added an optional `errorDetails` object to error responses.
- Existing clients still parse the standard `message` and `code` fields while ignoring the extra details.
- Output: `BACKWARD_COMPATIBLE`

### Example 6: Hidden breaking change

- Tightened validation on an existing request field from 255 characters to 100.
- Existing clients may now fail even though the payload shape is unchanged.
- Output: `BREAKING_CHANGE`

## Common Failure Modes

- Treating additive schema changes as safe without verifying legacy client behavior
- Changing optional fields to required without compatibility support
- Renaming or removing fields in the same published version
- Diverging shared schemas across services
- Changing error shapes or status codes without documenting the impact
- Introducing new validation rules that reject previously valid requests
- Assuming consumers are updated in lockstep with API changes
- Failing to mark breaking changes as versioned or deprecated

## Answer Checklist

Before finalizing your response, verify:

- The compatibility risk is clearly identified.
- The selected decision matches the effect on existing consumers.
- Breaking or risky changes include versioning or migration guidance.
- Cross-service or cross-version inconsistencies are explicitly noted.
- Reasoning is based on contract semantics, not implementation details.
- If the change is safe, explain why older clients are unaffected.
- If the change is breaking, explain which consumer expectation is violated.

## Notes for Agents

- Treat this prompt as a contract compatibility review, not a generic code review.
- Focus on API surface and consumer-facing behavior.
- Use the exact labels: `SAFE`, `BACKWARD_COMPATIBLE`, or `BREAKING_CHANGE`.
- Provide concise, factual reasoning with specific contract examples.
- Do not recommend changes unrelated to API compatibility.

## Verification

After evaluating a change, ensure:

- The compatibility assessment is explicit.
- The output decision is justified by actual client impact.
- Migration or versioning needs are clearly stated when applicable.
- Shared schema inconsistencies are surfaced.
- The response stays at the contract level and avoids internal implementation details.

---
name: regression-risk-detector
description: Detects potential unintended side effects and behavioral regressions caused by code changes.
---

# Regression Risk Detector

## Overview

This audit identifies change patterns that may introduce unintended behavioral regressions or side effects.

A regression risk review should surface areas where a code change may alter existing behavior, violate implicit contracts, or break dependent consumers even when the change passes tests or compiles successfully.

### Goal

- Detect hidden dependencies and brittle assumptions.
- Flag code changes that affect shared behavior or downstream clients.
- Highlight changes that may fail silently or change edge-case semantics.

---

## Scope

Use this prompt when changes impact:

- Core business logic or domain behavior
- Shared utility functions, libraries, or helper modules
- Public or internal APIs
- Configuration transforms, file formats, or input/output schemas
- Data processing, validation, or normalization logic

This prompt is less useful for entirely isolated refactors with no shared surface area, purely cosmetic edits, or documentation-only changes.

---

## Focus Areas

### Behavioral Changes

Evaluate whether the change may alter the expected behavior for existing inputs or scatter existing outputs.

- Modified outputs for existing inputs
- Changed sorting, filtering, or formatting behavior
- Altered error handling, retries, or fallback behavior
- New branching that changes edge-case results
- Changed default values or assumptions in shared workflows

### Shared Code Impact

Identify whether the changed code is used in more than one place or affects global behavior.

- Utilities used in multiple modules
- Global helpers or services
- Common validation or transformation functions
- Shared configuration loaders and feature toggles
- Framework or platform integration code

### Implicit Assumptions

Surface hidden contracts that the code depends on or maintains implicitly.

- Hidden dependencies in logic
- Undocumented invariants
- Implicit ordering or state assumptions
- Assumed input shapes or side effects
- Implicit reliance on platform behavior or library defaults

### Downstream Impact

Assess how consumers or clients may be affected indirectly.

- Consumers of changed functions
- API clients affected indirectly
- Serialized data compatibility
- Contract changes across library boundaries
- Third-party integration expectations

### Silent Failures

Watch for changes that degrade reliability or correctness without causing build failures.

- Failures that are caught and swallowed
- Outputs that are silently mutated or dropped
- Edge cases that change behavior only under rare conditions
- Performance changes that shift behavior under load
- Backward compatibility breaks that do not trigger tests

---

## Review Process

Perform the regression risk review in three stages:

1. Understand the surface area
   - Identify the changed files and functions.
   - Determine whether the affected code is shared or public-facing.
   - Map the inputs and outputs for the changed logic.
2. Verify behavior assumptions
   - Check whether existing contracts are preserved.
   - Inspect edge cases and default values.
   - Evaluate error handling and recovery behavior.
3. Assess downstream consumers
   - Identify direct callers and indirect consumers.
   - Evaluate compatibility with existing callers or serialized formats.
   - Consider whether the change requires documentation or versioning.

---

## Detection Checklist

### Core Regression Signals

- [ ] Does the change alter the result for existing inputs?
- [ ] Does it change any error or edge-case behavior?
- [ ] Does it affect shared utilities or helper functions?
- [ ] Are implicit contracts or assumptions preserved?
- [ ] Do downstream callers still receive the same shape and semantics?

### Compatibility Signals

- [ ] Are API or contract changes explicit and versioned?
- [ ] Are default behaviors preserved when no new configuration is supplied?
- [ ] Are serialization formats backward compatible?
- [ ] Are any deprecated behaviors removed without compatibility support?

### Silent Failure Signals

- [ ] Are exceptions handled or swallowed in the changed code?
- [ ] Are logging or monitoring paths updated for the new behavior?
- [ ] Could the change cause different behavior only under rare conditions?
- [ ] Is there a fallback for the modified logic if it fails?

---

## Examples of Regression Risk

- Changing a shared formatter so existing text output changes format for all downstream consumers.
- Modifying validation rules that cause previously accepted data to be rejected.
- Adjusting retry logic that changes the timing or error conditions observed by callers.
- Refactoring a utility function used in multiple modules without verifying all call sites.
- Changing an implicit default from `true` to `false` in a configuration loader.

### Example Findings

- "The updated helper now returns a different data schema for existing callers."
- "This change narrows accepted input values, which may break legacy clients."
- "Default behavior changed without an opt-in flag, increasing regression risk."
- "The new error-handling branch swallows exceptions that were previously propagated."
- "A shared utility now depends on a new library behavior not covered by all consumers."

---

## Output Decision

- SAFE: The change is low risk; behavior is preserved and any modifications are isolated or explicitly versioned.
- POSSIBLE_REGRESSION: The change has some risk to existing behavior or shared consumers and merits closer validation or tests.
- HIGH_REGRESSION_RISK: The change likely alters existing behavior, shared contracts, or downstream expectations and should be treated as a regression risk.

---

## Risk Classification Guidance

- SAFE: small bug fix or isolated refactor with no shared behavioral change.
- POSSIBLE_REGRESSION: modified edge-case or shared logic that may affect a subset of consumers; requires stronger test coverage.
- HIGH_REGRESSION_RISK: public API, shared library, or domain logic change that can break existing users or clients.

---

## Best Practices

- Prefer explicit contract changes over hidden behavior shifts.
- Add regression tests for new edge cases and shared behavior.
- Document compatibility assumptions when changing defaults or formats.
- Use feature flags or versioning for behavior changes in shared code.
- Avoid altering shared helpers without auditing all callers.

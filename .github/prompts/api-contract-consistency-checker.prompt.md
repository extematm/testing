---
name: api-contract-consistency-checker
description: Ensures API contracts remain stable, backward-compatible, and consistent across services and versions.
---

# API Contract Consistency Checker

## Overview

Validates that changes to APIs do not break existing consumers or introduce inconsistent schemas.

## Focus Areas

### Schema Stability

- Request/response shape consistency
- Field renames/removals
- Type consistency

### Backward Compatibility

- Breaking vs non-breaking changes
- Default values for new fields
- Deprecated field handling

### Versioning Discipline

- Proper API version bumps
- No silent contract changes
- Clear migration paths

### Cross-Service Drift

- Inconsistent DTOs across services
- Diverging implementations of same contract

### Breaking Change Detection

- Removed or renamed fields
- Changed semantics of existing fields

## Output Decision

- SAFE
- BACKWARD_COMPATIBLE
- BREAKING_CHANGE (requires version bump)

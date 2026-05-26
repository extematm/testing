---
name: data-flow-and-state-integrity-checker
description: Validates correctness of data flow, state transitions, and transactional integrity across system boundaries.
---

# Data Flow & State Integrity Checker

## Overview
Ensures correctness and consistency of system state across mutations and services.

## Focus Areas

### State Transitions
- Valid state machine behavior
- No invalid transitions

### Race Conditions
- Concurrent updates
- Stale reads
- Lost updates

### Transactional Integrity
- Atomic multi-step operations
- Rollback safety
- Partial failure handling

### Multi-Step Mutations
- Consistency across steps
- Idempotency where needed

### Cross-Module Consistency
- Shared state coherence
- Contracted invariants preserved

## Output Decision
- VALID
- RISKY (needs review)
- BROKEN (state integrity violation)

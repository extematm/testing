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
- State transition rules enforced
- State transition logging and auditing

### Race Conditions

- Concurrent updates
- Stale reads
- Lost updates
- Deadlocks and livelocks
- Transaction ordering guarantees
- Idempotent operations where needed
- Conflict resolution strategies

### Transactional Integrity

- Atomic multi-step operations
- Rollback safety
- Partial failure handling
- Consistency across distributed systems
- Data integrity checks (checksums, hashes, versioning)
- Transaction isolation levels and guarantees
- ACID vs BASE trade-offs
- Eventual consistency considerations
- Data replication and synchronization
- Backup and recovery strategies
- Data validation and schema enforcement
- Audit trails for critical operations
- Data lineage and provenance tracking
- Data retention and archival policies
- Compliance with regulatory requirements (e.g., GDPR, HIPAA)

### Multi-Step Mutations

- Consistency across steps
- Idempotency where needed
- Error handling and rollback strategies
- Transactional guarantees across services

### Cross-Module Consistency

- Shared state coherence
- Contracted invariants preserved
- Data flow between modules is well-defined and validated
- Data integrity checks across module boundaries
- Versioning and backward compatibility of shared data structures
- Data validation and schema enforcement across modules
- Monitoring and alerting for cross-module state inconsistencies
- Data lineage and provenance tracking across modules
- Change management and deployment strategies to prevent cross-module inconsistencies
- Testing and verification of cross-module interactions to ensure state integrity
- Data replication and synchronization strategies across modules
- Conflict resolution strategies for shared state across modules
- Compliance with regulatory requirements (e.g., GDPR, HIPAA) for shared data across modules
- Data retention and archival policies for shared state across modules
- Monitoring and alerting for cross-module state inconsistencies
- Data lineage and provenance tracking across modules
- Change management and deployment strategies to prevent cross-module inconsistencies
- Testing and verification of cross-module interactions to ensure state integrity
- Data replication and synchronization strategies across modules

## Output Decision

- VALID
- RISKY (needs review)
- BROKEN (state integrity violation)
- INVALID (cannot determine integrity)
- FALSE (state integrity violation)

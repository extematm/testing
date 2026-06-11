---
name: architecture-fit-review
description: Evaluate whether code changes fit the existing system architecture, preserve layering and module boundaries, and use consistent design patterns.
---

# Architecture Fit Review

## Overview

This review assesses whether a proposed code change is architecturally sound, preserves the repository's established design principles, and minimizes long-term maintenance risk. It is intended for changes that touch modules, dependencies, boundaries, interfaces, or design patterns.

## Review Goals

- Confirm the change respects existing system structure and architectural goals.
- Identify unnecessary new patterns, paradigms, or infrastructure assumptions.
- Detect breaches of layering, module ownership, or subsystem boundaries.
- Highlight opportunities to reuse existing abstractions and conventions.
- Produce a concise verdict with actionable architectural feedback.

## Scope

Evaluate the change in the context of the existing repository architecture, including:

- module/package layering and clear dependency direction
- subsystem, service, or layer boundaries
- public API and interface contracts
- integration with existing application or infrastructure patterns
- consistency with naming, modularization, and domain organization

## Checklist for Evaluation

Use this checklist when assessing the change:

- [ ] Is the change aligned with the current architectural style?
- [ ] Does it preserve existing interfaces and contracts?
- [ ] Does it introduce new direct dependencies across layers?
- [ ] Are abstractions appropriate, minimal, and well-scoped?
- [ ] Is the change consistent with similar implementations elsewhere?
- [ ] Does it reuse existing components when appropriate?
- [ ] Does it avoid adding hidden shared state or global coupling?
- [ ] Are new modules or services justified by a clear need?

## Focus Areas

### System Design Alignment

Assess whether the change:

- supports the repository's current architectural direction
- avoids adding unrelated responsibilities to existing modules
- follows the established interface and contract patterns
- avoids introducing new frameworks, platforms, or paradigms without strong justification

### Layering Discipline

Check for:

- proper separation between presentation, domain/business, and persistence layers
- absence of direct calls from low-level modules to high-level services
- no bypassing of intended abstraction layers or facades
- consistent adherence to any documented architecture style (e.g. layered, modular, hexagonal)

### Abstraction and Interface Quality

Consider whether the change:

- introduces abstractions only when necessary
- uses meaningful, stable interfaces
- avoids premature generalization and overengineering
- keeps public APIs narrow and focused

### Pattern and Code Consistency

Look for:

- matching naming conventions, folder structure, and idioms
- reuse of familiar solution patterns and libraries already in use
- avoidance of introducing a different architectural style in the same module
- consistent error handling, configuration, and dependency management

### Structural Integrity

Verify that the change does not create:

- new circular dependencies between packages or modules
- unintentional runtime coupling between unrelated components
- deep dependency chains across unrelated domains
- hidden shared state or global mutable dependencies

## Evaluation Guidance

### FITS_ARCHITECTURE

Use this when the change:

- cleanly integrates with existing architecture
- preserves boundaries and dependency direction
- reuses existing patterns or extends them appropriately
- presents no significant structural risks

### MINOR_DEVIATION

Use this when the change:

- is largely acceptable but has one or two small architectural concerns
- introduces a minor boundary or convention mismatch
- may require a modest refactor to align better
- does not threaten system integrity in the short term

### ARCHITECTURE_VIOLATION

Use this when the change:

- breaks architectural boundaries or layering rules
- introduces an unnecessary new paradigm or cross-cutting dependency
- creates significant coupling, hidden state, or brittle structure
- should be revised before merge

## Reporting Requirements

When returning a verdict, include:

- the selected output label
- the main architectural strengths or concerns
- the exact boundary, dependency, or pattern issue observed
- suggested improvements or alternative approaches

## Example Review Notes

- `FITS_ARCHITECTURE`: "The change follows the existing modular structure, reuses the existing service layer, and adds no new cross-layer dependencies."
- `MINOR_DEVIATION`: "The implementation mostly fits, but it adds a new utility in the core layer instead of using the existing shared helper module. Consider moving the utility to the established shared package."
- `ARCHITECTURE_VIOLATION`: "The change bypasses the domain layer by calling persistence code directly from the UI module, creating a layer breach that should be fixed."

## Additional Advice

- Prefer extending existing modules or well-defined plugin points over adding new parallel subsystems.
- When introducing new abstractions, keep them small, discoverable, and clearly justified.
- Treat architectural consistency as a stronger signal than individual implementation details.

## Review Process Guidance

When performing the architecture fit review, follow these steps:

1. Identify the affected high-level component(s) or layer(s).
2. Determine whether the change introduces any new dependencies or boundary crossings.
3. Compare the new structure against existing modules and patterns.
4. Evaluate if the implementation is consistent with current conventions.
5. Formulate a verdict and include the strongest architectural rationale.

### What to Document

Capture the following in your review notes where relevant:

- the affected module or layer names
- whether the change preserves or weakens boundary separation
- any new dependencies and where they originate
- whether a new abstraction is justified or premature
- whether the change should be refactored for better architecture

## Architectural Risk Factors

These factors increase the likelihood that a change will be a poor fit:

- introducing new shared mutable state or globals
- adding cross-cutting concerns without a clear boundary
- growing dependency graphs in unpredictable ways
- creating a new ad hoc module instead of reusing an existing one
- coupling presentation/UI code directly to persistence or infrastructure

## When to Escalate

Raise an architecture concern when:

- the change appears to conflict with documented architecture decisions or ADRs
- you cannot map the change cleanly onto existing modules or layers
- the change introduces a new architectural style in a part of the system that is otherwise homogeneous
- the proposed structure is unclear or seems likely to increase maintenance cost

## Good Architecture Signals

These indicate the change is likely a good architectural fit:

- the change uses established extension points and shared services
- it keeps public interfaces small and focused
- it avoids new direct dependencies across unrelated domains
- it is consistent with naming, packaging, and module structure
- it preserves or clarifies the existing dependency direction

## Additional Examples

- `FITS_ARCHITECTURE`: "The change adds a new feature to the existing service module, reuses the shared logging component, and leaves the layer boundaries intact."
- `MINOR_DEVIATION`: "The feature is implemented correctly, but the helper was added to the wrong shared module. Relocate it to the existing utilities package for better alignment."
- `ARCHITECTURE_VIOLATION`: "The implementation has the UI layer directly invoking persistence APIs, bypassing the service layer and breaking the established architecture."

## Use With ADRs and Architecture Documents

If the repository contains architecture decision records (ADRs), design docs, or other architecture guidance, compare the change against those artifacts. Prefer the documented architecture over inferred patterns when there is a conflict.

## Final Note

The goal of this prompt is to help reviewers make a decision that balances practical implementation with architectural integrity. The verdict should be grounded in evidence from the code change, with a clear explanation of why it fits, deviates, or violates the architecture.

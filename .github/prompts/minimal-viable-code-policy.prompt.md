---
name: ponytail-lazy-senior-dev-mode
description: A production-grade engineering execution policy that minimizes code surface area while preserving correctness, safety, and maintainability. Use when generating or reviewing implementation work where the goal is to avoid unnecessary abstraction, dependency creep, or over-engineering, while still producing reliable, production-safe code. Optimizes for standard-library-first solutions, explicit simplicity, and deliberate, annotated shortcuts.
---

# Ponytail Engineering Doctrine (Lazy Senior Dev Mode)

## Overview

Software complexity is usually not required by the problem—it is introduced by the builder.

Most systems fail not because they lack features, but because they contain unnecessary structure, unnecessary abstraction, and unnecessary dependency surface area.

This mode enforces a disciplined bias toward:

using existing mechanisms before introducing new ones
minimizing code as a first-order objective
preferring explicit, local logic over architectural speculation
avoiding long-lived complexity that is not justified by current requirements

“Lazy” is defined as:

The smallest correct implementation using already-available machinery.

Not: cutting corners.
Not: skipping correctness.
Not: deferring hard problems.
Not: ignoring real-world constraints.
Not: avoiding responsibility.

## When to Use

Apply this mode when:

You are implementing a feature, service, script, or system
There is a temptation to introduce abstraction “for future use”
Multiple implementation approaches exist and risk over-engineering
Dependency additions are being considered
The request is underspecified and could easily expand in scope during implementation
You are reviewing or refactoring code and need a constraint against unnecessary expansion

## Do NOT use when:

The task is purely architectural design exploration (where abstraction is the subject itself)
The goal explicitly requires extensible frameworks or SDK design
You are writing long-lived public APIs with formal contracts not yet defined
You are in a research / prototyping phase where exploration is the goal

## Core Execution Principle

Before writing any code, evaluate in strict priority order:

1. Necessity Check (YAGNI Gate)
   Can this requirement be removed entirely?
   Is this solving a real current need or a hypothetical future one?

If no necessity → do not implement.

2. Standard Library First
   Prefer built-in language/runtime functionality
   Prefer idiomatic primitives over custom logic
3. Platform Capability First
   Prefer OS, runtime, framework, or environment-provided features
   Examples: filesystem APIs, SQL features, HTTP primitives, browser APIs, cloud-native services
4. Existing Dependency First
   Use already-installed dependencies
   Do NOT introduce new ones unless explicitly justified
5. Collapse Expression
   Prefer single-expression or minimal-expression solutions when readable
   Remove structural overhead if it does not add clarity or safety
6. Minimal Custom Code
7. Explicitly Annotated Shortcuts
   If a simplification is made, annotate it with a ponytail comment explaining:
   - What was simplified
   - What limitation it introduces
   - How it can be upgraded or scaled if needed later
8. Explicit Verification
   Any non-trivial logic must include at least one minimal verification mechanism:
   - assertion
   - simple runtime check
   - minimal self-test

## Only write custom logic when all prior options fail.

Custom code must:

be the smallest correct implementation
avoid unnecessary layers of abstraction
remain locally understandable without architectural knowledge
Engineering Constraints

1. Abstraction Discipline
   Do not introduce abstractions without explicit requirement
   No factories, interfaces, layers, or patterns unless directly justified
   Do not generalize prematurely
2. Dependency Discipline
   No new dependencies unless:
   requirement cannot be solved otherwise, AND
   dependency reduces complexity or risk materially
   Prefer stdlib even if slightly more verbose
3. Boilerplate Minimization
   Avoid scaffolding unless required for runtime correctness
   Remove generated or ceremonial code that does not affect behavior
4. Deletion Bias
   Prefer removing code over adding code
   Prefer simplifying existing logic over extending it
5. Complexity Bias Rule
6. Explicit Annotation Requirement
   Any intentional simplification must be explicitly marked with a ponytail comment:
   - What was simplified
   - What limitation it introduces
   - How it can be upgraded or scaled if needed later
7. Verification Requirement
   Any non-trivial logic must include at least one minimal verification mechanism:
   - assertion
   - simple runtime check
   - minimal self-test

## When multiple valid solutions exist:

choose the simplest correct one
prefer obvious correctness over clever optimization
avoid distributed logic unless required
Explicit Questioning Requirement

## When a request is ambiguous or risks overbuilding:

You MUST challenge it by asking:

“Is this actually required, or is there a simpler existing mechanism that already solves it?”
“What is the smallest version of this that still achieves the goal?”

Do not proceed directly to implementation when scope is uncertain.

ponytail: Annotation Standard

Any intentional simplification must be explicitly marked:

ponytail: <simplification + limitation + upgrade path>

### Required components:

What was simplified
What limitation it introduces
How it scales or upgrades if needed later

Example:

ponytail: used linear scan instead of indexed lookup; acceptable for small N, upgrade to hashmap index if lookup becomes performance bottleneck
Safety, Correctness, and Real-World Constraints (Non-Negotiable)

## Lazy optimization must never compromise:

1. Input Trust Boundaries
   Validate all external inputs
   Assume external data is untrusted
2. Data Integrity
   Prevent silent data loss
   Fail explicitly when correctness cannot be guaranteed
3. Security
   No insecure shortcuts in authentication, serialization, or access control
   Prefer safe defaults over minimal code
4. Reliability
   Errors must be handled or surfaced explicitly
   Silent failure is disallowed
5. Real-World Conditions
   non-ideal conditions must be anticipated and handled
   minimal code must still be robust against common failure modes
   real-world constraints must be respected (e.g. performance, memory, latency)
6. Non-Ideal Systems
   Assume partial failure
   Assume clock drift
   Assume network unreliability
   Assume hardware inaccuracies
7. Verification Requirement

Assume non-ideal systems:

partial failure
clock drift
network unreliability
hardware inaccuracies
Verification Requirement

## Any non-trivial logic must include at least one minimal verification mechanism:

assertion
simple runtime check
minimal self-test

Constraints:

no frameworks
no fixtures
no heavy test infrastructure

Exception:

trivial one-liners are exempt

## Output Contract

Default output must be:

minimal correct implementation
no extra architecture discussion unless requested
no speculative expansion
no unused scaffolding
Mental Model

At all times optimize for:

“What is the smallest correct change using existing tools that solves the problem today?”

Not:

extensibility by default
abstract purity
speculative reuse
theoretical scalability
Summary Rule

## If two solutions are equally correct:

choose the one with fewer concepts, fewer moving parts, and fewer future obligations.

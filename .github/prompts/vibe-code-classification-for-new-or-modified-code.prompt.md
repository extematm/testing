# Vibe Code Classification for New or Modified Code

## Overview

This system defines a structured rubric for identifying “vibe-coded” software—code that appears functional but lacks engineering rigor, maintainability, or explicit design intent.

Vibe code is characterized by:

- Implicit logic instead of explicit design
- Over-reliance on convenience patterns
- Weak separation of concerns
- Missing error handling and edge-case reasoning
- “It works” implementations without structural justification

The goal is not stylistic enforcement, but engineering integrity verification before merge or adoption.

### Purpose

- Catch fragile or unclear code early.
- Help reviewers differentiate between working code and well-engineered code.
- Preserve maintainability and clarity in production paths.

## When to Use

Use this classification system when reviewing:

- Newly generated code (especially AI-assisted)
- Rapid prototypes intended for production paths
- Refactored modules with unclear structure changes
- Pull requests with minimal documentation or reasoning
- Code that introduces new abstractions or architectural patterns
- Integration code between services, APIs, or data layers
- Code that touches shared utilities, frameworks, or common libraries

## Classification Objective

Each code change is evaluated to determine whether it is:

- Clean Engineering: Structured, intentional, maintainable.
- Mild Vibe Drift: Acceptable but loosely structured.
- High Vibe Risk: Fragile, implicit logic, unclear design.
- Vibe Code (Blocker): Non-deterministic structure, unsafe or unmaintainable patterns.

This classification is not a style score. It is a judgment about whether the change introduces maintainability or engineering debt risk above and beyond the current codebase.

## Core Detection Dimensions

### 1. Implicit Logic & Hidden Assumptions

Ask:

- Are important decisions made implicitly instead of explicitly?
- Are constants, thresholds, or behavior rules unexplained?
- Are behaviors dependent on “understood context” rather than code clarity?
- Are assumptions about environment, local state, or external systems hidden in the implementation?

Red Flags:

- Magic numbers without explanation
- Conditional logic based on assumed environment state
- Missing domain modeling (everything is ad-hoc logic)
- Implicit dependencies on call order or global state

### 2. Structural Weakness

Ask:

- Is the code organized around clear responsibilities?
- Are functions doing multiple unrelated tasks?
- Are abstractions missing or incorrectly applied?
- Is the implementation a long, procedural block instead of a composable set of smaller pieces?

Red Flags:

- God functions
- Mixed concerns (IO + business logic + validation in one place)
- Copy-pasted logic instead of reusable components
- Heavy coupling between unrelated modules

### 3. Over-Optimization for Convenience

Ask:

- Was the implementation chosen for speed of writing over correctness or clarity?
- Is the code optimized for minimal typing rather than readability?
- Does it favor clever shortcuts over explicit behavior?

Red Flags:

- Inline everything instead of modular design
- Overuse of shorthand patterns (ternaries, chaining) reducing readability
- Avoidance of interfaces or explicit types where they are needed
- One-liners that hide branch behavior or error handling

### 4. Error Handling Neglect

Ask:

- Are failure modes explicitly handled?
- Are edge cases defined or ignored?
- Does the code assume success without verifying results?

Red Flags:

- Empty catch blocks
- Silent failures or swallowed exceptions
- Default returns that hide invalid states
- Missing validation of external or untrusted inputs

### 5. Data Flow Ambiguity

Ask:

- Is it clear how data moves through the system?
- Are transformations traceable?
- Is data mutated in place or passed through predictable pipelines?

Red Flags:

- Untracked mutations
- Shared mutable state without control
- Data transformations hidden inside nested calls
- Loss of provenance for derived values

### 6. Overuse of “AI-Style” Code Patterns

Typical LLM-generated structures:

- Generic function naming (`handleData`, `processInput`)
- Over-abstracted utilities without real reuse
- Excessive boilerplate without functional necessity
- Multiple layers of indirection with no clear benefit

Red Flags:

- “Looks correct” but lacks domain specificity
- Reusable abstractions that are never reused
- Generic helpers that obscure real behavior
- Patterns that prioritize form over meaning

### 7. Missing Domain Modeling

Ask:

- Is the domain explicitly represented in code?
- Are domain concepts mapped clearly to objects, functions, or types?
- Is business logic encoded as procedural scripts instead of intent-driven abstractions?

Red Flags:

- Business logic encoded as procedural scripts
- No domain objects where expected
- Confusing mapping between real-world concepts and code structures
- Domain intention buried in implementation details

### 8. Testing & Verifiability Gaps

Ask:

- Can behavior be validated independently?
- Are critical paths testable?
- Are tests missing for important edge cases?

Red Flags:

- No unit/integration tests for core logic
- Use of emoji or non-standard comments to explain logic instead of code clarity
- Hard-to-mock dependencies
- Non-deterministic outputs without control
- Test coverage that only exercises happy paths

## Severity Classification

| Level      | Meaning                                      | Action                     |
| ---------- | -------------------------------------------- | -------------------------- |
| Clean      | Structured implementation                    | Approve                    |
| Mild Drift | Acceptable but loosely structured            | Consider minor cleanup     |
| High Risk  | Fragile or unclear engineering               | Refactor before merge      |
| Blocker    | Non-deterministic, unsafe, or unmaintainable | Must not merge until fixed |

Additional guidance:

- **Clean** means the code is easy to understand, maintain, and extend.
- **Mild Drift** means the code is acceptable but would benefit from clearer boundaries or simpler structure.
- **High Risk** means the code is likely to cause maintenance pain or bugs in the future.
- **Blocker** means the code is actively dangerous or too confusing to merge safely.

## Review Process

### Step 1: Understand Intent

- What is the code supposed to do?
- What domain does it belong to?
- What are the expected inputs and outputs?
- What is the desired behavior in edge cases?

### Step 2: Map Structural Boundaries

Identify:

- Core business logic
- External interfaces (APIs, DB, services)
- Data transformation layers
- Side-effect boundaries
- Shared utilities and public surface area

### Step 3: Evaluate Engineering Clarity

Check:

- Are responsibilities clearly separated?
- Are abstractions meaningful or accidental?
- Is logic traceable end-to-end?
- Are implementation details exposed in the interface?

### Step 4: Detect Vibe Patterns

Explicitly scan for:

- Shortcut-driven implementation
- Over-generalized utilities
- Hidden state mutation
- Missing error pathways
- Implicit assumptions embedded in control flow

### Step 5: Assign Classification

Return:

- Label (Clean → Blocker)
- Key rationale
- Structural issues found
- Suggested remediation (if applicable)
- Verification or test gaps that should be fixed

## Mandatory Vibe Classification Checklist

## Vibe Code Review: [Change Title]

### Structural Understanding

- [ ] Code responsibilities are clearly separated
- [ ] Domain logic is explicitly modeled
- [ ] Shared logic is intentionally centralized, not accidentally duplicated

### Clarity & Determinism

- [ ] No hidden assumptions or magic values
- [ ] Data flow is traceable and explicit
- [ ] Control flow is easy to follow without extra context

### Engineering Quality

- [ ] No mixed concerns in functions
- [ ] Abstractions are justified, not accidental
- [ ] All helper functions have a clear single responsibility

### Error Handling

- [ ] Failures are explicitly handled or surfaced
- [ ] No silent error suppression
- [ ] Edge cases are accounted for or intentionally documented

### Maintainability

- [ ] Code is readable without context inference
- [ ] Future modification paths are clear
- [ ] Naming reflects domain intent and behavior

### Testability

- [ ] Core logic is covered by tests
- [ ] Edge cases and error paths are tested
- [ ] Dependencies are easy to mock or isolate
- [ ] Non-deterministic behavior is controlled or documented

### Verdict

- [ ] Clean Engineering
- [ ] Mild Vibe Drift
- [ ] High Vibe Risk
- [ ] Vibe Code (Blocker)

## Hard Gate Rules

- Any Blocker classification = must not merge.
- Multiple Critical findings require refactor before approval.
- “It works” is not a valid engineering justification.
- If logic cannot be explained cleanly, it is vibe code by default.
- If the structural intent is unclear, favor a higher risk classification.

## Common Vibe Code Anti-Patterns

| Pattern                            | Why it is problematic                     |
| ---------------------------------- | ----------------------------------------- |
| Quick utility functions everywhere | Prevents architectural coherence          |
| Minimal comments, implicit logic   | Forces reverse engineering                |
| Everything in one file             | Violates separation of concerns           |
| Generic handlers reused everywhere | Masks domain differences                  |
| No tests because logic is simple   | Complexity is often hidden, not absent    |
| Hidden side effects in helpers     | Creates surprises for callers             |
| Excessive indirection              | Makes bug fixes and reasoning much harder |

## Output Standard

Each classification must include:

- Label
- Rationale (engineering-focused)
- Risk assessment
- Recommended refactor direction
- Specific verification notes or test requirements

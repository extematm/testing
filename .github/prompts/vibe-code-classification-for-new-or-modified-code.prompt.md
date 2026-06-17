Vibe Code Classification for New or Modified Code
Overview

This system defines a structured rubric for identifying “vibe-coded” software—code that appears functional but lacks engineering rigor, maintainability, or explicit design intent.

Vibe code is characterized by:

Implicit logic instead of explicit design
Over-reliance on convenience patterns
Weak separation of concerns
Missing error handling and edge-case reasoning
“It works” implementations without structural justification

The goal is not stylistic enforcement, but engineering integrity verification before merge or adoption.

When to Use

Use this classification system when reviewing:

Newly generated code (especially AI-assisted)
Rapid prototypes intended for production paths
Refactored modules with unclear structure changes
Pull requests with minimal documentation or reasoning
Code that introduces new abstractions or architectural patterns
Integration code between services, APIs, or data layers
Classification Objective

Each code change is evaluated to determine whether it is:

Label Meaning
Clean Engineering Structured, intentional, maintainable
Mild Vibe Drift Acceptable but loosely structured
High Vibe Risk Fragile, implicit logic, unclear design
Vibe Code (Blocker) Non-deterministic structure, unsafe or unmaintainable patterns
Vibe Code Signals (Core Detection Dimensions)

1. Implicit Logic & Hidden Assumptions
   Are important decisions made implicitly instead of explicitly?
   Are constants or thresholds unexplained?
   Are behaviors dependent on “understood context” rather than code clarity?

Red Flags:

Magic numbers without explanation
Conditional logic based on assumed environment state
Missing domain modeling (everything is ad-hoc logic) 2. Structural Weakness
Is the code organized around clear responsibilities?
Are functions doing multiple unrelated tasks?
Are abstractions missing or incorrectly applied?

Red Flags:

God functions
Mixed concerns (IO + business logic + validation in one place)
Copy-pasted logic instead of reusable components 3. Over-Optimization for Convenience
Was the implementation chosen for speed of writing over correctness or clarity?

Red Flags:

Inline everything instead of modular design
Overuse of shorthand patterns (ternaries, chaining) reducing readability
Avoidance of interfaces/types where they are needed 4. Error Handling Neglect
Are failure modes explicitly handled?
Are edge cases defined or ignored?

Red Flags:

Empty catch blocks
Silent failures or swallowed exceptions
Default returns that hide invalid states 5. Data Flow Ambiguity
Is it clear how data moves through the system?
Are transformations traceable?

Red Flags:

Untracked mutations
Shared mutable state without control
Data transformations hidden inside nested calls 6. Overuse of “AI-Style” Code Patterns

Typical LLM-generated structures:

Generic function naming (handleData, processInput)
Over-abstracted utilities without real reuse
Excessive boilerplate without functional necessity

Red Flags:

“Looks correct” but lacks domain specificity
Reusable abstractions that are never reused 7. Missing Domain Modeling
Is the domain explicitly represented in code?

Red Flags:

Business logic encoded as procedural scripts
No domain objects where expected
Confusing mapping between real-world concepts and code structures 8. Testing & Verifiability Gaps
Can behavior be validated independently?
Are critical paths testable?

Red Flags:

No unit/integration tests for core logic
Use of Emoji or non-standard comments to explain logic instead of code clarity
Hard-to-mock dependencies
Non-deterministic outputs without control
Severity Classification
Level Meaning Action
(none) Clean implementation Approve
Suggestion: Minor structural improvement Optional
Important: Weak engineering patterns Should refactor
Critical: High-risk vibe code Must fix before merge
Blocker: Non-deterministic or unsafe design Reject
Review Process
Step 1: Understand Intent
What is the code supposed to do?
What domain does it belong to?
What are the expected inputs and outputs?
Step 2: Map Structural Boundaries

Identify:

Core business logic
External interfaces (APIs, DB, services)
Data transformation layers
Side-effect boundaries
Step 3: Evaluate Engineering Clarity

Check:

Are responsibilities clearly separated?
Are abstractions meaningful or accidental?
Is logic traceable end-to-end?
Step 4: Detect Vibe Patterns

Explicitly scan for:

Shortcut-driven implementation
Over-generalized utilities
Hidden state mutation
Missing error pathways
Step 5: Assign Classification

Return:

Label (Clean → Blocker)
Key rationale
Structural issues found
Suggested remediation (if applicable)
Mandatory Vibe Classification Checklist

## Vibe Code Review: [Change Title]

### Structural Understanding

- [ ] Code responsibilities are clearly separated
- [ ] Domain logic is explicitly modeled

### Clarity & Determinism

- [ ] No hidden assumptions or magic values
- [ ] Data flow is traceable

### Engineering Quality

- [ ] No mixed concerns in functions
- [ ] Abstractions are justified, not accidental

### Error Handling

- [ ] Failures are explicitly handled
- [ ] No silent error suppression

### Maintainability

- [ ] Code is readable without context inference
- [ ] Future modification paths are clear

### Verdict

- [ ] Clean Engineering
- [ ] Mild Vibe Drift
- [ ] High Vibe Risk
- [ ] Vibe Code (Blocker)
      Hard Gate Rules
      Any Blocker classification = must not merge
      Multiple Critical findings require refactor before approval
      “It works” is not a valid engineering justification
      If logic cannot be explained cleanly → it is vibe code by default
      Common Vibe Code Anti-Patterns
      Pattern Why it is problematic
      “Quick utility functions everywhere” Prevents architectural coherence
      “Minimal comments, implicit logic” Forces reverse engineering
      “Everything in one file” Violates separation of concerns
      “Generic handlers reused everywhere” Masks domain differences
      “No tests because logic is simple” Complexity is often hidden, not absent
      Output Standard

Each classification must include:

Label
Rationale (engineering-focused)
Risk assessment
Recommended refactor direction

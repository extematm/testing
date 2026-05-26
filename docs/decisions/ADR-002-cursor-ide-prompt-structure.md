# ADR-002: Store AI prompt guidance in Cursor IDE folder structure instead of `.github/prompts`

## Status

Superseded by ADR-003

## Date

2025-05-26

## Context

The repository previously stored custom AI prompt guidance under `.github/prompts/` with files named using the `*.prompt.md` convention. That structure was primarily designed for VS Code/agent workflows and GitHub-based discovery.

A new workflow requirement emerged for Cursor IDE compatibility:

- Cursor IDE prefers prompt guidance stored in its own workspace folder structure
- Cursor prompt files should not rely on a `*.prompt.*` naming pattern intended for VS Code prompt conventions
- Prompt guidance needs to be discoverable by Cursor without additional integration layers
- The repository should preserve the same guidance content while aligning with Cursor IDE expectations

## Decision

Move existing prompt guidance from `.github/prompts/*.prompt.md` into Cursor IDE's prompt folder structure.

### What changed

- Removed the `*.prompt.md` naming convention for these files
- Added equivalent prompt guidance into the Cursor IDE folder hierarchy
- Kept the guidance content identical while changing only the storage location and naming format

## Alternatives Considered

### 1. Keep prompts in `.github/prompts/` and add Cursor integration

- Pros: No change to the existing prompt repository structure
- Cons: Requires additional Cursor configuration or adapter logic; prompt discovery would not be native
- Rejected: Adds integration complexity and undermines Cursor IDE compatibility

### 2. Duplicate prompts in both `.github/prompts/` and Cursor folders

- Pros: Preserves compatibility for both VS Code and Cursor
- Cons: Creates duplicate files and content drift risk
- Rejected: Unacceptable maintenance overhead and risk of stale guidance

### 3. Store prompt guidance in a neutral shared docs folder

- Pros: Centralized, IDE-agnostic location
- Cons: Cursor still needs explicit discovery rules, and existing CI/agent tooling may not support the neutral path
- Rejected: Cursor-specific folder structure is simpler and more reliable for tool discovery

## Consequences

- **Positive:** Cursor IDE can discover and consume prompt guidance natively
- **Positive:** Guidance remains version-controlled and audit-ready
- **Negative:** VS Code-specific prompt conventions are no longer the primary storage model
- **Negative:** If the team later needs multi-IDE support, a new strategy may be required

## Implementation Notes

- Keep prompt content consistent across both VS Code and Cursor usage scenarios where possible
- Use the Cursor IDE folder structure as the canonical prompt source for this project
- If future IDEs are added, evaluate a shared prompt store with explicit adapters rather than file duplication

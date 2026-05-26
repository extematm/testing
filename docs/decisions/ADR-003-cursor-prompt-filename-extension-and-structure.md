# ADR-003: Use `.cursorrules/rules/*.mdc` as the canonical Cursor prompt guidance store

## Status

Accepted

## Date

2026-05-26

## Context

The repository contains prompt guidance for AI-assisted development in two formats:

- `.github/prompts/*.prompt.md` — a VS Code/GitHub prompt convention
- `.cursorrules/rules/*.mdc` — Cursor IDE rule files

Cursor IDE requires prompt guidance to be discoverable in its own workspace folder structure and to use the `.mdc` extension for rule files. The existing `.github/prompts` naming pattern is not native to Cursor and creates ambiguity about which prompt source is authoritative.

This project needs a single canonical prompt store that:

- is discoverable by Cursor IDE without custom adapters
- preserves prompt guidance content for agents and humans
- minimizes duplication and divergence between IDE-specific formats
- supports future Cursor-driven automation and rule enforcement
- includes the newly added Cursor rule files such as `documentation-and-adrs.mdc`, `code-simplification.mdc`, `test-driven-development.mdc`, and related guidance files

## Decision

Use `.cursorrules/rules/*.mdc` as the canonical prompt guidance location for Cursor IDE, and treat `.github/prompts/*.prompt.md` as a legacy VS Code-compatible representation.

Key points:

- Prompt files are stored in `.cursorrules/rules/`
- Cursor prompt files use the `.mdc` extension
- The `.cursorrules/rules/` layout is the canonical source for AI guidance content in this repository
- Existing `.github/prompts/` files may remain for compatibility, but new prompt guidance should be authored in Cursor structure first

## Alternatives Considered

### 1. Keep prompts only in `.github/prompts/*.prompt.md`

- Pros: No change to existing file structure or toolchain for VS Code
- Cons: Cursor discovery would require an extra integration layer or custom import logic
- Rejected: Cursor-native prompt discovery is a higher priority than preserving an old storage pattern

### 2. Duplicate prompt guidance in both `.github/prompts/` and `.cursorrules/rules/`

- Pros: Both VS Code and Cursor can consume prompts natively
- Cons: Creates duplicate content and increases the risk of stale guidance
- Rejected: Maintenance overhead outweighs the compatibility benefit

### 3. Use a neutral shared folder for prompts and adapt both tools

- Pros: One source of truth, tool-agnostic storage
- Cons: Neither Cursor nor VS Code would consume it natively without adapters
- Rejected: Adds integration complexity and delays discovery

## Consequences

- Cursor IDE can discover prompt guidance natively and use `.mdc` rule files without extra configuration
- This repository now has a clear canonical source for prompt guidance
- `.github/prompts/*.prompt.md` becomes a legacy compatibility layer, not the primary source
- The team must keep `.cursorrules/rules/` updated when prompt guidance changes
- Future multi-IDE support should be designed around a shared source with explicit adapters, not duplicated prompt stores

## Notes

- This ADR supersedes ADR-002, which documented the initial move toward Cursor IDE prompt storage.
- Authoring and review practices should prioritize `.cursorrules/rules/*.mdc` for prompt guidance updates.

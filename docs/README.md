# Architecture Decision Records (ADRs)

This directory contains architecture decision records for significant technical choices in the project.

## Index

| ADR                                                                            | Title                                                                                | Status                | Date       |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | --------------------- | ---------- |
| [ADR-001](decisions/ADR-001-github-actions-and-prompts.md)                     | Use GitHub Actions for CI/CD and Security, Store Agent Prompts in .github/prompts    | Accepted              | 2025-05-26 |
| [ADR-002](decisions/ADR-002-cursor-ide-prompt-structure.md)                    | Store AI prompt guidance in Cursor IDE folder structure instead of `.github/prompts` | Superseded by ADR-003 | 2025-05-26 |
| [ADR-003](decisions/ADR-003-cursor-prompt-filename-extension-and-structure.md) | Use `.cursorrules/rules/*.mdc` as the canonical Cursor prompt guidance store         | Accepted              | 2026-05-26 |

## Reading ADRs

Each ADR captures:

- **Context**: Why a decision was needed
- **Decision**: What was chosen and why
- **Alternatives Considered**: What was evaluated and rejected (and why)
- **Consequences**: Benefits and trade-offs of the decision

ADRs are maintained in version control and form an audit trail of major design choices. Older ADRs are not deleted; if a decision changes, a new ADR is created that supersedes the previous one.

## Adding New ADRs

When making a significant architectural decision:

1. Create a new file: `ADR-XXX-short-title.md`
2. Use the template provided in ADR-001
3. Update this index
4. Link to the ADR from any affected code or documentation
5. Include a reference to the ADR in the commit message

See `.github/prompts/documentation-and-adrs.prompt.md` for detailed guidelines on writing ADRs and inline documentation.

**GitHub Workflows — Usage & Configuration**

Purpose

- This document explains how the CI workflows in `/.github/workflows/` are used inside GitHub and how to configure them. It is focused on usage, behavior, and the configuration options you will typically edit — not on installing tools locally.

What lives here

- `/.github/workflows/checkov.yml` — Infrastructure-as-code scanning (Checkov). Produces SARIF results and can block PRs.
- `/.github/workflows/gitleaks.yml` — Secrets scanning (Gitleaks). Detects leaked credentials and uploads SARIF + artifacts and can block PRs.
- `/.github/workflows/semgrep.yml` — Static application security testing (Semgrep). Runs rule sets, computes a PR baseline, and enforces severity gates and can block PRs.
- `/.github/workflows/devskim.yml` — DevSkim is a Microsoft product for language analysis and security "linting".
- `/.github/workflows/megalinter.yml` — Megalinter runs multiple linters (default rules if not configured) and provides SARIF output on errors.
- `/.github/workflows/scorecard.yml` — Scorecard is an open source tool to provide a repository score, errors are described in SARIF format and can such as the other acitons be found in the "Security and quality" section of the repo

What is advised to run based on noise (LOW, MEDIUM, HIGH)

1. Checkov is specific for IaC and creates more noise on findings due to specific detection methods, so multiple errors might be mapped to same action - MIDDLE NOISE LEVEL / Secuirty HIGH

2. GitLeaks is rather low on noise due to only checking new code for leaks - LOW NOISE LEVEL / Security HIGH

3. Semgrep is Static Code analysis and has rather low to medium noise - LOW/MEDIUM NOISE LEVEL / Security HIGH

4. Devskim is mainly for security and therefor manadatory, but provides a medium to high noise level depending on codebase - MEDIUM/HIGH NOISE LEVEL / Security MEDIUM

5. Megalinter is utlizing multiple linters and therefor provides a high noise level - HIGH NOISE LEVEL / Security LOW

6. Scorecard has a high noise level, but folows strong security practices in a very large scope on repository level. Because this scanner runs on a very large scope and repository level, while alerting on important security missings, configs... should this scanner be repository mandatory - HIGH NOISE LEVEL / Security VERY HIGH

---

## For security reasons running all actions is advised, but in case of too much noise, try disabling the high noise first and ensure they also have lowest security impact before removing too many scanners.

## Architecture

This project uses **GitHub Actions** for all CI/CD, security scanning, and code quality enforcement. Custom prompts for AI-driven development are stored in `.github/prompts/`.

**Why GitHub Actions?** See [ADR-001](docs/decisions/ADR-001-github-actions-and-prompts.md) for the full architectural rationale, alternatives considered, and consequences.

### Key Directories

- `/.github/workflows/` — GitHub Actions CI/CD and security scanning pipelines
- `/.cursorrules/rules/` — Canonical Cursor IDE prompt guidance rule files (`*.mdc`)
- `/.github/prompts/` — Legacy VS Code prompt guidance representation (`*.prompt.md`) kept for compatibility
- `/docs/decisions/` — Architecture Decision Records (ADRs) documenting major design choices

### Design Principles

- **Automation first**: Security and linting policies are enforced via CI/CD, not manual review
- **Agent consistency**: Custom prompts guide AI tools to follow project conventions
- **Version control**: All infrastructure and guidance lives in Git for auditability and history

## Contributing

Before contributing:

1. Read [docs/decisions/](docs/decisions/) to understand key architectural choices
2. Review `.cursorrules/rules/documentation-and-adrs.mdc` for documentation and ADR standards
3. Review `.cursorrules/rules/code-simplification.mdc` for code style guidelines
4. Ensure all tests pass and no security checks are blocked on your PR

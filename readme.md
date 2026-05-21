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

What is advised to run based on noise ()

1. Checkov is specific for IaC and creates more noise on findings due to specific detection methods, so multiple errors might be mapped to same action - MIDDLE NOISE LEVEL
2. GitLeaks is rather low on noise due to only checking new code for leaks - LOW NOISE LEVEL
3.

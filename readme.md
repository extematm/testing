**GitHub Workflows — Usage & Configuration**

Purpose

- This document explains how the CI workflows in `/.github/workflows/` are used inside GitHub and how to configure them. It is focused on usage, behavior, and the configuration options you will typically edit — not on installing tools locally.

What lives here

- `/.github/workflows/checkov.yml` — Infrastructure-as-code scanning (Checkov). Produces SARIF results and can block PRs.
- `/.github/workflows/gitleaks.yml` — Secrets scanning (Gitleaks). Detects leaked credentials and uploads SARIF + artifacts and can block PRs.
- `/.github/workflows/semgrep.yml` — Static application security testing (Semgrep). Runs rule sets, computes a PR baseline, and enforces severity gates and can block PRs.

How to use these workflows in GitHub

- Triggers: workflows run on configured events (`pull_request`, `schedule`, `workflow_dispatch`). For PRs the most common flow is: developer opens PR → workflows run → SARIF and artifacts are uploaded → PR may be blocked based on gating rules.
- Re-run / manual runs: use the Actions UI → select a workflow run → `Re-run jobs` or use the `workflow_dispatch` event if present to trigger manually.
- Where results appear: Uploaded SARIF files show up in GitHub under Security → Code scanning. Artifacts are available from the Actions run summary. Comments/annotations (if configured) appear on the PR as comments.

Key configuration areas (what you will edit)

- `on:` — change triggers, branches, or add `workflow_dispatch` to allow manual runs.
- `permissions:` — restrict or grant specific token scopes the workflow needs (e.g., `contents: read`, `security-events: write`). Only grant minimum required privileges.
- `concurrency:` — ensure only one run per branch/reference with `cancel-in-progress` to avoid duplicate work.
- `runs-on` / `container:` — select the runner image or container used to execute the job. Changing a container image affects the runtime environment.
- `env:` and workflow-level environment variables — place tunables here (e.g., feature flags for scanners).
- `timeout-minutes` — cap runaway runs.

Workflow-specific configuration notes

- Checkout action:
  - `uses: actions/checkout@vX` — pick a published tag (`v4`, `v5`, `v6`) rather than a partial tag like `v`. If you see "Unable to resolve action 'actions/checkout@v'", update to a full tag.
  - `with: fetch-depth:` — set to `0` if tools need full history (gitleaks incremental scans require full history for certain modes).

- Checkov (`checkov.yml`):
  - Tunables in the `with:` block: `framework`, `output_format`, `output_file_path`, `download_external_modules`, `compact`, `skip_path`, `skip_check` and `soft_fail`.
  - Environment flags such as `CHECKOV_EXPERIMENTAL_TERRAFORM_MANAGED_MODULES` are set at the job level for feature toggles.
  - The workflow uploads SARIF with `github/codeql-action/upload-sarif@v4`. If you need a different category, change the `category` input.

- Gitleaks (`gitleaks.yml`):
  - `GITLEAKS_VERSION` is set inside the workflow—edit to pin a different binary.
  - The workflow computes a base ref for incremental PR scanning. Modify how `BASE` is computed to change diff behavior.
  - The step that runs `gitleaks detect` controls output format, report path, and exit code behavior (`--exit-code 1` to fail on findings).
  - Artifacts are preserved via `actions/upload-artifact` to keep SARIF copies for auditing.

- Semgrep (`semgrep.yml`):
  - Runs in `semgrep/semgrep:latest` container by default. To control versions, edit the container image tag.
  - Caching: `actions/cache` is used to cache engine/rules. The cache key is usually based on rule files and OS — adjust if you change where rules live.
  - Baseline commit: the workflow reads the PR base SHA to run an incremental scan. Ensure `github.event.pull_request.base.sha` is available for PR events; otherwise the workflow will fall back to a full scan.
  - Severity gating: the workflow computes CRITICAL and HIGH counts from `semgrep.sarif` and fails the job based on thresholds. Adjust the numeric thresholds in the `Evaluate severity gate` step to relax or harden gating.
  - Exclusions: semgrep uses `--exclude` flags and an ignore file at `/.github/workflows/.semgrepignore` — edit that file to add or remove excluded paths.

Working with SARIF, artifacts, and annotations

- SARIF upload: `github/codeql-action/upload-sarif@v4` is used to publish findings to the Security → Code scanning UI. The `category` input groups findings by scanner.
- Artifacts: `actions/upload-artifact` stores copies of SARIF, text reports, or tooling outputs for later inspection. Keep artifact names stable for automation.
- PR annotations/comments: some workflows add PR comments (for example using `actions/github-script`) when failures occur. Edit that step to change the message or to disable comments.

Common edits you may want to make

- Change PR trigger branches (edit the `pull_request: branches:` list).
- Pin or update `actions/checkout@vX` across all workflows for consistency.
- Increase/decrease semgrep gating thresholds in `semgrep.yml` by editing the numeric checks in the `Evaluate severity gate` step.
- Add or remove paths in `skip_path` (Checkov) or `--exclude` / `.semgrepignore` (Semgrep) to tune scan scope.
- For Gitleaks, change `GITLEAKS_VERSION` to a newer or older release; ensure CI runners can download the artifact URL used in the workflow.

Best practices when editing workflows

- Make small, targeted edits and validate on a non-protected branch before merging to `main`.
- Pin action and tool versions for reproducibility. Use explicit tags for actions (e.g., `actions/checkout@v4`).
- Keep `permissions:` minimal and review scopes when adding new steps that interact with the GitHub API.
- Use `concurrency:` to avoid duplicated scans and reduce CI costs.
- Don’t use `.semgrepignore` to hide real source files — only exclude generated artifacts, dependencies, and third-party code.

If you want, I can:

- Open a PR that pins `actions/checkout` to a stable version across workflows.
- Clean up suspicious entries in `/.github/workflows/.semgrepignore` (for example stray backslashes) and commit the changes.
- Adjust semgrep gating thresholds or Checkov `skip_check` lists in a branch for review.

---

Edit the workflow files under `/.github/workflows/` to change behavior; if you want, tell me which exact change(s) you'd like and I will prepare a PR.

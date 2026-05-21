**Repository Workflows**

- **Purpose**: This repository contains automated security scans that run in GitHub Actions. The workflows live in [.github/workflows](.github/workflows) and produce SARIF and artifact outputs used for security reviews.

**Workflows Overview**

- **Checkov (IaC)**: [.github/workflows/checkov.yml](.github/workflows/checkov.yml)
  - **Purpose**: Scans infrastructure-as-code (Terraform, Kubernetes, Dockerfile, GitHub Actions, secrets) for misconfigurations using Checkov.
  - **Triggers**: `pull_request`, scheduled nightly, and manual `workflow_dispatch`.
  - **Key steps**: checks out the repo, runs `bridgecrewio/checkov-action`, writes `results.sarif`, and uploads SARIF with `github/codeql-action/upload-sarif@v4`.
  - **Important notes**: the workflow uses `actions/checkout@v6`. If you see errors resolving `actions/checkout@v` or similar, use a published tag like `actions/checkout@v4` or `actions/checkout@v6` explicitly (avoid incomplete tags). Re-run the workflow after adjusting the tag.

- **Gitleaks (Secrets)**: [.github/workflows/gitleaks.yml](.github/workflows/gitleaks.yml)
  - **Purpose**: Detects leaked secrets in commits and PR diffs using `gitleaks`.
  - **Triggers**: `pull_request` and scheduled runs.
  - **Key steps**: checks out with `actions/checkout@v5` (with `fetch-depth: 0` for full history), installs a pinned `gitleaks` binary, runs an incremental scan against the PR or push range, produces `gitleaks.sarif`, validates the output, uploads SARIF to the Security tab, and stores a run artifact.
  - **Important notes**: adjust `GITLEAKS_VERSION` in the workflow to pin or update the version. Local runs should match the version used in CI to avoid differences in detection rules.

- **Semgrep (SAST)**: [.github/workflows/semgrep.yml](.github/workflows/semgrep.yml)
  - **Purpose**: Runs Semgrep rules (security-audit, OWASP top ten) to find code-level issues and fails PRs based on severity gates.
  - **Triggers**: `pull_request`.
  - **Key steps**: runs inside the `semgrep/semgrep:latest` container, caches the Semgrep engine and rules, computes an optional PR baseline, runs `semgrep scan` and writes `semgrep.sarif`, evaluates CRITICAL/HIGH counts to gate the PR, generates a prioritized text report, uploads SARIF, and uploads artifacts.
  - **Important notes**: the workflow uses an exclusions list (see `.semgrepignore`) and a baseline-commit technique for incremental scans. Adjust threshold logic in the `Evaluate severity gate` step to change gating behavior.

**Semgrep ignore file**

- File: [.github/workflows/.semgrepignore](.github/workflows/.semgrepignore)
  - **Purpose**: Lists glob patterns that Semgrep should skip during scans. This keeps scans focused on source files and avoids noisy results from generated code, dependencies, and build outputs.
  - **Common patterns in this repo**:
    - `codeqlmain/**` — ignore codeql builds or outputs
    - `vendor/**`, `node*modules/**`, `dist/**`, `build/**` — ignore dependencies and build artifacts
    - `*.min.js`, \_.bundle.js-style filenames — ignore minified and bundled assets
  - **Syntax & tips**:
    - Uses shell-style globs. A leading `**/` matches any directory depth.
    - Do not prefix patterns with unnecessary escape characters — e.g., an entry like `\\_.bundle.js` is probably incorrect; use `*.bundle.js` or `_*.bundle.js` to match filenames with underscores.
    - Keep the file minimal and review entries periodically to avoid hiding real issues in important code paths.

**How to run scans locally**

- Semgrep (Docker):

```bash
docker run --rm -v "$(pwd)":/src -w /src semgrep/semgrep:latest \
	semgrep scan --config p/security-audit --config p/owasp-top-ten --sarif --output semgrep.sarif
```

- Semgrep (pip):

```bash
pip install semgrep
semgrep scan --config p/security-audit --sarif --output semgrep.sarif
```

- Checkov (Docker):

```bash
docker run --rm -v "$(pwd)":/src bridgecrew/checkov:latest -d /src --output-file results.sarif --output sarif
```

- Gitleaks (local):

```bash
gitleaks detect --source . --report-format sarif --report-path gitleaks.sarif --exit-code 1
```

**Viewing results in GitHub**

- **SARIF uploads**: Workflows upload SARIF files (e.g., `results.sarif`, `gitleaks.sarif`, `semgrep.sarif`) using `github/codeql-action/upload-sarif@v4`. Once uploaded, findings appear under the repository **Security → Code scanning** tab.
- **Artifacts**: Some workflows also save SARIF and text reports as artifacts for debugging (see `actions/upload-artifact`).

**Troubleshooting & best practices**

- **Checkout action errors**: If CI fails with `Unable to resolve action 'actions/checkout@v'` or similar, update the `uses:` line to a full, published tag like `actions/checkout@v4` or `actions/checkout@v6` in the workflow file.
- **Pin tool versions**: For deterministic CI behavior, pin versions (e.g., `GITLEAKS_VERSION`) instead of always using `latest` in production workflows.
- **Baseline and gating**: For large repos, prefer baseline-based incremental scans to reduce noise. Adjust the High/Critical thresholds in `semgrep.yml` as your team matures.
- **Review .semgrepignore regularly**: Don't use the ignore file to hide real issues — only exclude generated code, external libraries, and build artifacts.

If you'd like, I can also open a PR that pins `actions/checkout` to a specific stable version across these workflows, or adjust the `.semgrepignore` entries (for example removing accidental escape sequences).

# GitHub Actions Cost Analysis — Enterprise Cloud

## Summary

**All workflows run on `ubuntu-latest` (GitHub-hosted runners).** Enterprise Cloud includes **50,000 free runner minutes per month**, so these workflows will cost **$0 (FREE)** unless you experience extreme PR volume.

---

## Workflow Breakdown

### 1. Checkov (IaC Security)

| Property                   | Value                        |
| -------------------------- | ---------------------------- |
| **Runner**                 | `ubuntu-latest`              |
| **Timeout**                | 20 minutes                   |
| **Triggers**               | PR, nightly schedule, manual |
| **Estimated monthly cost** | FREE                         |

**Per-run cost:**

- Typical run: ~15–20 minutes
- Cost if exceeding quota: ~$0.16 (20 min × $0.008/min)

---

### 2. Gitleaks (Secrets Scanning)

| Property                   | Value                |
| -------------------------- | -------------------- |
| **Runner**                 | `ubuntu-latest`      |
| **Timeout**                | 10 minutes           |
| **Triggers**               | PR, nightly schedule |
| **Estimated monthly cost** | FREE                 |

**Per-run cost:**

- Typical run: ~5–10 minutes
- Cost if exceeding quota: ~$0.08 (10 min × $0.008/min)

---

### 3. Semgrep (SAST)

| Property                   | Value                    |
| -------------------------- | ------------------------ |
| **Runner**                 | `ubuntu-latest`          |
| **Container**              | `semgrep/semgrep:latest` |
| **Timeout**                | 20 minutes               |
| **Triggers**               | PR only                  |
| **Estimated monthly cost** | FREE                     |

**Per-run cost:**

- Typical run: ~15–25 minutes (depends on codebase size and cache hits)
- Cost if exceeding quota: ~$0.20 (25 min × $0.008/min)

---

### Additional Workflows (from README notes)

**Note:** The README mentions DevSkim, Megalinter, and Scorecard, but the workflow files were not provided. These will likely follow a similar pattern.

| Workflow   | Runner          | Timeout | Cost (typical) |
| ---------- | --------------- | ------- | -------------- |
| DevSkim    | `ubuntu-latest` | ~10 min | ~$0.08 / run   |
| Megalinter | `ubuntu-latest` | ~15 min | ~$0.12 / run   |
| Scorecard  | `ubuntu-latest` | ~10 min | ~$0.08 / run   |

---

## Monthly Cost Estimate (Typical Active Repo)

### Scenario 1: Moderate PR Activity (20 PRs/month)

Each PR triggers all workflows:

- Checkov: 20 min
- Gitleaks: 10 min
- Semgrep: 20 min
- **Per PR:** ~50 minutes

**Monthly calculation:**

- 20 PRs × 50 min = 1,000 minutes
- Scheduled runs (nightly): 30 min/day × 30 days = 900 minutes
- **Total: ~1,900 minutes / month**
- **Cost: $0 (well within 50,000 free minutes)**

### Scenario 2: High PR Activity (100 PRs/month)

- 100 PRs × 50 min = 5,000 minutes
- Scheduled runs: 900 minutes
- **Total: ~5,900 minutes / month**
- **Cost: $0 (still within free quota)**

### Scenario 3: Extreme PR Activity (500+ PRs/month)

- 500 PRs × 50 min = 25,000 minutes
- Scheduled runs: 900 minutes
- **Total: ~25,900 minutes / month**
- **Cost: $0 (still within free quota)**

---

## GitHub Actions Pricing for Enterprise Cloud

| Category                 | Inclusion  | Cost                       |
| ------------------------ | ---------- | -------------------------- |
| **Monthly free minutes** | 50,000     | n/a                        |
| **Ubuntu runner**        | $0.008/min | (after quota exceeded)     |
| **Windows runner**       | $0.016/min | (not used here)            |
| **macOS runner**         | $0.08/min  | (not used here)            |
| **Self-hosted runner**   | Included   | (your infrastructure cost) |

---

## How to Control Costs

1. **Concurrency limits** — Both `checkov.yml` and your workflows use `concurrency: cancel-in-progress: true`. This prevents duplicate runs and saves minutes.

2. **Skip unnecessary runs** — Comment out `schedule:` triggers if nightly scans aren't needed.

3. **Adjust timeouts** — If a workflow consistently finishes in 10 min but has a 20 min timeout, lower the timeout to reduce accidental overruns.

4. **Use caching** — `semgrep.yml` already uses `actions/cache`. Ensure cache keys are stable.

5. **Filter triggers** — Use `branches:` to limit runs to specific branches (e.g., `main`, `develop`).

6. **Self-hosted runners** — If you exceed quota consistently, migrate to self-hosted runners (Linux box) for near-zero incremental cost.

---

## Recommendations

✅ **Keep all workflows running** — You're nowhere near the free quota limit.

✅ **Monitor usage** — Check `Settings → Billing and plans → Actions` in GitHub to track actual runner minutes.

✅ **Use concurrency** — Already enabled; this prevents wasted minutes on duplicate runs.

⚠️ **Only if exceeding quota** — Switch to self-hosted runners or disable low-value workflows (e.g., if Megalinter/DevSkim produce too much noise).

---

## Conclusion

**Your workflows cost $0 per month on Enterprise Cloud.** The 50,000 free minutes far exceeds typical usage. Unless you have **500+ active PRs per month**, you'll never be billed.

If needed, I can help you:

- Add cost monitoring to workflow logs
- Optimize timeouts
- Add additional safeguards for quota tracking

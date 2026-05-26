# ADR-001: Use GitHub Actions for CI/CD and Security, Store Agent Prompts in .github/prompts

## Status

Accepted

## Date

2025-05-26

## Context

The project requires:

- Automated security and code quality scanning on every pull request and push
- A repeatable, version-controlled way to run linters, SAST tools, and infrastructure-as-code analysis
- Consistent development experience for humans and AI agents working in the codebase
- Centralized storage for agent-driven coding instructions (prompts, style guides, ADR templates)
- Zero additional infrastructure or tool maintenance overhead

Key constraints:

- Team has limited DevOps capacity — hosting our own CI/CD system is not feasible
- Security scanning must block PRs on critical findings to enforce policy compliance
- Agent tools (e.g., GitHub Copilot with custom instructions) need to find project conventions without manual distribution
- Workflows and prompts should live in version control alongside code for audit trail and historical context

## Decision

1. **Use GitHub Actions** for all CI/CD, security scanning, and linting pipelines
2. **Store custom prompts in `.github/prompts/`** for AI agent instruction and code simplification guidance

### GitHub Actions Workflows

We've configured six automated workflows in `.github/workflows/`:

- **Checkov**: Infrastructure-as-code scanning (Terraform, Bicep, CloudFormation) — Medium noise, high security impact
- **GitLeaks**: Secrets scanning — Low noise, high security impact (mandatory)
- **Semgrep**: Static application security testing — Low-medium noise, high security impact
- **DevSkim**: Language-level security linting — Medium-high noise, medium security impact
- **Megalinter**: Multi-language linting (formatting, complexity) — High noise, low security impact
- **Scorecard**: Repository-level security posture — High noise, very high security impact (mandatory)

### `.github/prompts/` Structure

Custom prompts stored in `.github/prompts/` include:

- `code-simplification.prompt.md` — Guidance for reducing complexity while preserving behavior
- `documentation-and-adrs.prompt.md` — Guidelines for writing ADRs and inline documentation
- Additional domain-specific prompts for future development (e.g., API design, testing patterns)

These prompts are version-controlled and referenced by AI agents (Copilot, automation tools) to ensure consistency with project standards.

## Alternatives Considered

### 1. GitLab CI or Jenkins

- **Pros**: Self-hosted, full control, no lock-in
- **Cons**: Requires dedicated DevOps resources, more operational overhead, team already uses GitHub
- **Rejected**: Operational burden incompatible with limited team capacity

### 2. External CI/CD Services (CircleCI, Travis CI)

- **Pros**: Easy setup, minimal configuration
- **Cons**: Another vendor relationship, additional cost, less native GitHub integration
- **Rejected**: GitHub Actions is included with GitHub repos and tighter platform integration

### 3. Manual security scanning (local pre-commit hooks only)

- **Pros**: Simpler, fewer dependencies
- **Cons**: Inconsistent enforcement, easy to bypass, no centralized audit trail
- **Rejected**: CI/CD automation is required to enforce policy consistently

### 4. Store Prompts in Separate Repository

- **Pros**: Can version prompts independently
- **Cons**: Additional repository to manage, harder for agents to discover, friction in updates
- **Rejected**: Co-locating prompts with code makes them discoverable and maintainable

### 5. Store Prompts in Wiki or External Docs

- **Pros**: Centralized docs location
- **Cons**: Not version-controlled, harder for tools to consume, prone to staleness
- **Rejected**: Version-controlled prompts enable reproducible agent behavior

## Consequences

### Positive

- **Automated enforcement**: Security and linting policies are enforced on every PR without manual review overhead
- **No infrastructure cost**: GitHub Actions are included with GitHub — minimal operational burden
- **Version control**: Workflows and prompts are auditable, reversible, and tied to code history
- **Agent consistency**: Custom prompts ensure AI agents follow project conventions and avoid anti-patterns
- **Scalability**: Workflows scale automatically without provisioning — good for growth
- **Transparency**: Build history and artifact logs are visible to the team via GitHub interface

### Negative / Trade-offs

- **Noise from scanning**: Multiple scanners can produce overlapping findings, requiring tuning
  - **Mitigation**: Disable high-noise, low-security-impact scanners (Megalinter, Scorecard) if they exceed acceptable noise threshold per README guidelines
- **GitHub vendor lock-in**: Switching CI/CD systems requires migrating all workflows
  - **Mitigation**: Workflows are written in standard YAML; migration is possible but requires effort
- **Secret management complexity**: Sensitive credentials must be managed as GitHub Secrets
  - **Mitigation**: Use environment-specific secrets and audit access regularly
- **Agent prompt maintenance**: Prompts must be kept in sync with code style changes
  - **Mitigation**: Include prompt review in code review process; link prompts to ADRs for rationale

## Implementation Notes

### Workflow Tuning

- Start with all scanners enabled to establish baseline
- Review high-noise scanners (Megalinter, Scorecard) and disable if noise exceeds signal
- Document per-scanner thresholds in `.github/workflows/` comments for team reference

### Prompt Maintenance

- Review prompts quarterly or when major code style changes occur
- Link prompt examples to actual code locations in the repo for freshness
- When updating ADRs, cross-reference any affected prompts

### Scaling

- If agent-driven workflows expand, consider separating prompts by domain (e.g., `.github/prompts/backend/`, `.github/prompts/frontend/`)
- Monitor GitHub Actions usage (minutes/month) and adjust runner concurrency if needed

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Checkov Security Scanning](https://www.checkov.io/)
- [Semgrep SAST](https://semgrep.dev/)
- [Gitleaks Secrets Detection](https://github.com/gitleaks/gitleaks)
- Related: ADR-002 (forthcoming) on ADR and documentation standards

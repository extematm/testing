---
name: dependency-risk-analyzer
description: Evaluates third-party dependencies for necessity, security risk, and maintenance viability before adoption or update.
---

# Dependency Risk Analyzer

## Overview

Assesses whether a dependency should exist in the codebase at all. Focuses on minimizing supply-chain risk and unnecessary complexity.

## Focus Areas

### Necessity

- Is the dependency strictly required?
- Can native stdlib or existing utilities replace it?
- Is it solving a core problem or convenience?
- Does it introduce unnecessary complexity or bloat?
- Is it actively maintained and widely adopted?
- Does it have a clear and stable API?
- Does it have a clear and stable license?

### Security Risk

- Known CVEs or advisories
- Transitive dependency exposure
- Attack surface expansion
- License compliance and compatibility
- Vulnerability disclosure and response practices
- Security community trust and adoption
- Security testing and audit history
- Security best practices (e.g., input validation, output encoding, secure defaults)
- Security monitoring and alerting for new vulnerabilities
- Security patching and update frequency
- Security risk mitigation strategies (e.g., sandboxing, isolation, least privilege)
- Security risk assessment and threat modeling for the dependency
- Security risk communication and documentation for the dependency

### Maintenance Health

- Active maintenance status
- Release frequency
- Community trust and adoption
- Issue resolution and responsiveness
- Documentation quality and clarity
- Does the documentation clearly explain how to use the dependency and its limitations, which fully covering the dependency's functionality and edge cases and documentation?

### Performance Impact

- Bundle size increase
- Runtime overhead
- Tree-shaking effectiveness
- Performance benchmarks and profiling
- Performance regression testing and monitoring

## Output Decision

- APPROVE (justified necessity + acceptable risk)
- REJECT (unnecessary or risky dependency)
- REVIEW (uncertain value or risk)
- DEFER (insufficient information to make a decision)

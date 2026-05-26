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

### Security Risk
- Known CVEs or advisories
- Transitive dependency exposure
- Attack surface expansion

### Maintenance Health
- Active maintenance status
- Release frequency
- Community trust and adoption

### Performance Impact
- Bundle size increase
- Runtime overhead
- Tree-shaking effectiveness

## Output Decision
- APPROVE (justified necessity + acceptable risk)
- REJECT (unnecessary or risky dependency)
- REVIEW (uncertain value or risk)

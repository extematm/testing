---
name: risk-classification-gate
description: Classifies code changes by risk level and determines required review depth.
---

# Risk Classification Gate

## Overview
Assigns a risk tier to a change to determine how deeply it must be reviewed.

## Risk Levels

### LOW
- UI changes
- Internal refactors
- Non-critical logic changes

### MEDIUM
- Business logic changes
- Internal APIs
- Data transformations

### HIGH
- Auth, payments, permissions
- External API changes
- Shared utilities

### CRITICAL
- Security boundaries
- Data persistence layer
- Identity or authorization systems

## Routing Logic
- LOW → quick review
- MEDIUM → standard review
- HIGH → full review
- CRITICAL → full security audit required

## Output
- LOW
- MEDIUM
- HIGH
- CRITICAL

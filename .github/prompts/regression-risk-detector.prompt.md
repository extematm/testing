---
name: regression-risk-detector
description: Detects potential unintended side effects and behavioral regressions caused by code changes.
---

# Regression Risk Detector

## Overview
Identifies where changes may break existing behavior in unexpected ways.

## Focus Areas

### Behavioral Changes
- Modified outputs for existing inputs
- Altered edge-case behavior

### Shared Code Impact
- Utilities used in multiple modules
- Global helpers or services

### Implicit Assumptions
- Hidden dependencies in logic
- Undocumented invariants

### Downstream Impact
- Consumers of changed functions
- API clients affected indirectly

### Silent Failures
- Changes that degrade behavior without breaking builds

## Output Decision
- SAFE
- POSSIBLE_REGRESSION
- HIGH_REGRESSION_RISK

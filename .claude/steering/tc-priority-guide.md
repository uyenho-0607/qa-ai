# TC Priority Guide

Score every TC against the factors. Priority follows the decision rules, first match wins.

## Factors

**Business Criticality**
- High: core flow — login, sign up, convert, OTC approval, withdrawal, balance approval
- Medium: supporting flow — settings, configuration
- Low: display, cosmetic, rarely used

**User Impact**
- High: all users blocked or lose money
- Medium: subset of users affected
- Low: edge case, no financial impact

**Scenario Type**
- High: happy path
- Medium: validation, boundary, negative
- Low: UI-only, cosmetic

**Regression Risk**
- High: known fragile area, many dependencies
- Medium: moderate history
- Low: stable, isolated feature

**Blocking Risk**
- High: blocks other TCs if it fails
- Low: independent TC

## Decision

- 3+ High factors → **High**
- Mostly Medium, no High → **Medium**
- Mostly Low, cosmetic or edge only → **Low**
- Mixed → Business Criticality decides: High → **High**, Medium → **Medium**, Low → **Low**

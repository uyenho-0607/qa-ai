---
inclusion: manual
---

# TC Priority Guide

Score every TC against the factors. Priority follows the decision table.

## Factors

| Factor | High | Medium | Low |
|---|---|---|---|
| **Business Criticality** | Core flow: deposit, withdrawal, login, place order, close position | Supporting flow: settings, configuration | Display, cosmetic, rarely used |
| **User Impact** | All users blocked or lose money | Subset of users affected | Edge case, no financial impact |
| **Scenario Type** | Happy path | Validation, boundary, negative | UI-only, cosmetic |
| **Regression Risk** | Known fragile area, many dependencies | Moderate history | Stable, isolated feature |
| **Blocking Risk** | Blocks other TCs if it fails | — | Independent TC |

## Decision

- 3+ High factors → **High**
- Mostly Medium, no High → **Medium**
- Mostly Low, cosmetic or edge only → **Low**
- Mixed → apply business criticality as tiebreaker

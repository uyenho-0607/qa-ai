---
inclusion: manual
---

# TC Priority Guide

Read all factors. Score the TC. Propose Priority with reasoning. Wait for human confirmation.

## Factors

| Factor | High | Medium | Low |
|---|---|---|---|
| **Business Criticality** | Core flow: deposit, withdrawal, login, place order, close position | Supporting flow: settings, configuration | Display, cosmetic, rarely used |
| **User Impact** | All users blocked or lose money | Subset of users affected | Edge case, no financial impact |
| **Scenario Type** | Happy path | Validation, boundary, negative | UI-only, cosmetic |
| **Regression Risk** | Known fragile area, many dependencies | Moderate history | Stable, isolated feature |
| **Blocking Risk** | Blocks other TCs if it fails | — | Independent TC |

## Decision

| Pattern | Priority |
|---|---|
| 3 or more High factors | **High** |
| Mostly Medium, no High | **Medium** |
| Mostly Low, cosmetic or edge only | **Low** |
| Mixed | Apply business criticality as tiebreaker |

## Examples

| TC | Priority | Reason |
|---|---|---|
| Verify deposit with valid amount succeeds | High | Core flow, happy path, all users |
| Verify deposit amount below minimum is rejected | Medium | Validation, edge case |
| Verify deposit field placeholder text is correct | Low | Cosmetic, no user impact |
| Verify login with valid credentials succeeds | High | Core flow, blocks all other TCs |
| Verify sort by date on order history | Low | Supporting flow, no financial impact |

## Gate Format

```
Priority for "[TC Name]": [High / Medium / Low]
Reason: [factors applied]
Confirm or update:
```

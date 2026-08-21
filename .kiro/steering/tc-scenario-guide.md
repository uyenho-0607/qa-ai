---
inclusion: manual
---

# TC Scenario Coverage Guide

Read each AC. Match it to one or more patterns below. Apply all mandatory scenario types for every matched pattern. Done when every AC has at least its mandatory scenarios accounted for.

## Scenario Types

| Type | Covers |
|---|---|
| **Happy Path** | Primary success flow — valid input, correct state |
| **Validation** | Field-level rules — required, format, length, allowed values |
| **Boundary** | Edge values — min, max, zero, exactly at limit |
| **Negative** | Invalid input or wrong state — system rejects gracefully |
| **Empty / No Data** | UI behaviour when list, table, or field has no data |
| **Permission / Role** | Access control — authorised vs unauthorised |
| **Status Transition** | State machine — valid and invalid transitions |
| **Cross-Platform** | Same scenario on Desktop vs Mobile — consolidated into one TC |
| **Multi-Account** | Behaviour differs by account type, group, or config |
| **Concurrent / Side Effect** | Action on one entity affects another |

---

## Coverage Minimum by AC Pattern

### Form Field or Input
*Signal words: enter, input, fill, submit, type, field, value*

| Scenario | Required |
|---|---|
| Happy path — valid input accepted | Mandatory |
| Empty / missing required field rejected | Mandatory |
| Invalid format rejected | Mandatory |
| Boundary — min value | Mandatory if min exists |
| Boundary — max value | Mandatory if max exists |
| Boundary — zero | Mandatory for numeric fields |
| Boundary — negative | Mandatory for numeric fields |
| Special characters | Optional |

### List, Table, or Search
*Signal words: list, table, display, show, search, filter, sort, column*

| Scenario | Required |
|---|---|
| With data — correct display | Mandatory |
| Empty state — correct message shown | Mandatory |
| Search / filter returns correct results | Mandatory if search exists |
| Search / filter returns no results | Mandatory if search exists |
| Sort ascending and descending | Mandatory if sort exists |
| Pagination — navigate pages | Mandatory if pagination exists |

### Permission or Role
*Signal words: role, permission, access, admin, user, authorised, restricted, only*

| Scenario | Required |
|---|---|
| Authorised user can perform the action | Mandatory |
| Unauthorised user is blocked with correct error | Mandatory |
| Different roles see different UI/data | Mandatory if roles differ |

### Financial Amount
*Signal words: amount, deposit, withdrawal, balance, funds, minimum, maximum, limit*

| Scenario | Required |
|---|---|
| Valid amount — transaction succeeds | Mandatory |
| Amount below minimum — rejected with message | Mandatory |
| Amount above maximum — rejected with message | Mandatory if max exists |
| Zero amount — rejected | Mandatory |
| Negative amount — rejected | Mandatory |
| Decimal precision enforced | Mandatory if spec states it |
| Balance updated correctly after transaction | Mandatory |

### Status or Workflow Transition
*Signal words: status, state, transition, approve, reject, cancel, close, reopen, pending*

| Scenario | Required |
|---|---|
| Valid transition to correct next state | Mandatory |
| Invalid transition blocked with message | Mandatory |
| State reflected in UI after transition | Mandatory |
| Side effect on linked entities | Mandatory if documented |

### Toggle, Button, or Action
*Signal words: enable, disable, toggle, button, click, activate, deactivate*

| Scenario | Required |
|---|---|
| Action in enabled state | Mandatory |
| Action in disabled state — blocked or greyed out | Mandatory |
| State persists after page refresh | Mandatory |
| Confirmation dialog for destructive action | Mandatory if applicable |

### Display or UI
*Signal words: display, show, label, column, layout, responsive, icon, tooltip*

| Scenario | Required |
|---|---|
| Correct data displayed | Mandatory |
| Correct label / placeholder text | Mandatory |
| Desktop behaviour | Mandatory |
| Mobile behaviour | Mandatory if cross-platform |
| Empty / loading state handled | Mandatory |

### Multi-Account or Configuration-Dependent
*Signal words: account type, group, configuration, symbol config, user group, leverage*

| Scenario | Required |
|---|---|
| Default / standard configuration | Mandatory |
| Non-default configuration | Mandatory if differences documented |
| Config change reflected correctly | Mandatory if applicable |

---

## Domain Triggers (OMS / EMS)

| Signal in AC | Additional scenario |
|---|---|
| MT4 / MT5 / cTrader | Cross-platform — one TC per platform difference |
| Leverage or margin | Boundary scenarios for leverage values |
| Trading session or market hours | Out-of-session behaviour |
| Symbol or instrument | Per-symbol config variation |
| Admin vs trader | Permission scenario — both roles |
| Jira transition or SIT status | Status transition scenarios |
| Real-time update or WebSocket | Side effect — data refresh without reload |
| Audit log or history | Concurrent — action logged correctly |

---

## Coverage Proposal Gate Format

Present before generating any TC:

```
Coverage plan for [TICKET-KEY]:

AC-1: [summary]
  Pattern: [matched pattern(s)]
  Mandatory: [list]
  Optional: [list]

AC-2: [summary]
  Pattern: [matched pattern(s)]
  Mandatory: [list]

Confirm or adjust:
```

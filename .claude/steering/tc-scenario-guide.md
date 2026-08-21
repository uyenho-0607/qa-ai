---
inclusion: manual
---

# TC Scenario Coverage Guide

## Apply Coverage — Sweep, Match, Cross-cut

1. **Sweep** — map every screen the feature touches before reading the ACs: listing, form, review, confirmation, detail, OTP, etc.
2. **Match** — match each AC and BR to one or more patterns in the Coverage Minimum section. Apply all mandatory scenarios for every matched pattern.
3. **Cross-cut** — apply these regardless of AC wording:
   - Multi-step flow present → apply **Navigation / Screen Flow** to every screen from the sweep.
   - Feature is in a mobile app → apply **Mobile App Lifecycle** at each critical flow stage.
   - BO or admin system can view or modify the same records → apply **Cross-System Sync**.
   - A max count, quota, or limit is documented → apply **Boundary** at limit−1, limit, and limit+1.
   - Every error message harvested from the ticket → one scenario asserting that exact string.
   - Two or more fields have coupled validation → one scenario asserting that changing the controlling field resets or re-validates the dependent field.
   - A validation rule is stated without a status or condition qualifier → test it against every status/condition in scope; if scope is unclear, record as `needs-clarification`.
   - A dropdown or list is sourced from configuration → one scenario asserting the options match the configured set.
   - A forward status transition is documented → confirm whether reverse is documented; if silent, record as `needs-clarification`.
   - A multi-step flow has 3+ screens → confirm the back-navigation target for every screen; if not stated, ask.
   - A ticket link describes shared behavior → ask once whether to pull it into scope; a declined link is recorded.
   - Existing TCs mention a capability the ticket never names → raise as a scope question.

## Scenario Types

Use these type names exactly: Happy Path · Validation · Boundary · Negative · Empty / No Data · Permission / Role · Status Transition · Cross-Platform · Multi-Account · Concurrent / Side Effect · Navigation / Screen Flow · Mobile App Lifecycle · Cross-System Sync.

- **Cross-Platform** — same scenario on Desktop and Mobile, consolidated into one TC
- **Multi-Account** — behaviour varies by account type, group, or config
- **Navigation / Screen Flow** — entry points, back navigation, screen transitions, data retention
- **Mobile App Lifecycle** — background, kill-app, network interruption — state recovery
- **Cross-System Sync** — change in one system immediately reflected in another

---

## Coverage Minimum by AC Pattern

Mandatory = always apply. `if …` = apply when that condition holds.

### Form Field or Input

Match when AC contains: enter, input, fill, submit, type, field, value.

| Scenario | Required |
|---|---|
| Happy path — valid input accepted | Mandatory |
| Empty / missing required field rejected | Mandatory |
| Invalid format rejected | Mandatory |
| Boundary — min value | if min exists |
| Boundary — max value | if max exists |
| Boundary — zero | if numeric field |
| Boundary — negative | if numeric field |
| Boundary — below minimum length | if string field has a minimum character requirement |
| Special characters | Optional |
| Optional field — left empty, form still submits successfully | if optional fields exist |

Apply **Happy path** once per independently-validated field, not once per form. Pair every validation TC with its positive counterpart.

### Selection or Reference List

Match when AC contains: select, dropdown, choose, supported, configured, whitelist, options.

| Scenario | Required |
|---|---|
| Options list matches the documented/configured set | Mandatory |
| Each option displays correct label / icon | if specified |
| Selecting an option updates dependent field(s) correctly | if other fields depend on the selection |
| Search within modal — partial input filters results correctly | if modal has a search bar |
| Search within modal — clearing input restores the full list | if modal has a search bar |

### List, Table, or Search

Match when AC contains: list, table, display, show, search, filter, sort, column.

| Scenario | Required |
|---|---|
| With data — correct display | Mandatory |
| Empty state — correct message shown | Mandatory |
| Search / filter returns correct results | if search exists |
| Search / filter returns no results | if search exists |
| Search / filter — clearing input restores the full list | if search exists |
| Sort ascending and descending | if sort exists |
| Pagination — navigate pages | if pagination exists |
| At max count — add action blocked with correct message | if a count limit exists |

### Permission or Role

Match when AC contains: role, permission, access, admin, user, authorised, restricted, only.

| Scenario | Required |
|---|---|
| Authorised user can perform the action | Mandatory |
| Unauthorised user is blocked with correct error | Mandatory |
| Different roles see different UI or data | if roles differ |

### Financial Amount

Match when AC contains: amount, deposit, withdrawal, balance, funds, minimum, maximum, limit.

| Scenario | Required |
|---|---|
| Valid amount — transaction succeeds | Mandatory |
| Amount below minimum — rejected with message | Mandatory |
| Amount above maximum — rejected with message | if max exists |
| Zero amount — rejected | Mandatory |
| Negative amount — rejected | Mandatory |
| Decimal precision enforced | if spec states it |
| Balance updated correctly after transaction | Mandatory |

### Status or Workflow Transition

Match when AC contains: status, state, transition, approve, reject, cancel, close, reopen, pending.

| Scenario | Required |
|---|---|
| Valid transition to correct next state | Mandatory |
| Invalid transition blocked with message | Mandatory |
| State reflected in UI after transition | Mandatory |
| Side effect on linked entities | if documented |
| Reverse / undo transition — documented, or recorded as `needs-clarification` | Mandatory |
| Multiple triggers reach the same end-state — one scenario per trigger | if more than one trigger exists |

### Toggle, Button, or Action

Match when AC contains: enable, disable, toggle, button, activate, deactivate.

| Scenario | Required |
|---|---|
| Action in enabled state | Mandatory |
| Action in disabled state — blocked or greyed out | Mandatory |
| State persists after page refresh | Mandatory |
| Confirmation dialog for destructive action | if applicable |

### Display or UI

Match when AC contains: display, show, label, column, layout, responsive, icon, tooltip.

| Scenario | Required |
|---|---|
| Correct data displayed | Mandatory |
| Correct label / placeholder text | Mandatory |
| Modal opened from a field — correct title, close button, and list displayed | if field opens a modal or bottom sheet |
| Desktop behaviour | Mandatory |
| Mobile behaviour | if cross-platform |
| Empty / loading state handled | Mandatory |

### Multi-Account or Configuration-Dependent

Match when AC contains: account type, group, configuration, symbol config, user group, leverage.

| Scenario | Required |
|---|---|
| Default / standard configuration | Mandatory |
| Non-default configuration | if differences documented |
| Config change reflected correctly | if applicable |

### Navigation / Screen Flow

Match when AC contains: navigate, back, return, screen, flow, step, wizard, entry point, CTA, button. Also apply to every screen from the sweep.

| Scenario | Required |
|---|---|
| Entry point — correct screen is reached | Mandatory |
| Back navigation — returns to previous screen | Mandatory |
| Data retained when navigating back | if multi-step flow |
| CTA disabled until required fields are valid | if CTA has enabled/disabled state |
| Correct screen title and UI elements displayed | Mandatory |

### Mobile App Lifecycle

Apply at each critical flow stage for mobile features.

| Scenario | Required |
|---|---|
| Background during form fill — data retained on resume | Mandatory |
| Kill app during form fill — form cleared on reopen | Mandatory |
| Background during OTP — countdown continues, OTP valid on resume | if OTP flow exists |
| Kill app on confirmation/review screen — no record created | Mandatory |
| Kill app during edit — unsaved changes discarded | if edit flow exists |
| Network interruption during submission — graceful error, no duplicate | Mandatory |
| Session expiry during flow — re-auth prompt, no record created | Mandatory |

### Cross-System Sync

Match when AC contains: back office, BO, admin, portal, sync, reflect, update, audit, record, log.

| Scenario | Required |
|---|---|
| Record created in app is visible in BO with correct fields | if BO visibility is documented |
| Record updated in app is reflected in BO | if BO visibility is documented |
| Record deleted in app shows correct status in BO | if audit retention is documented |
| BO action immediately reflected in app without restart | if BO can modify app records |
| BO re-enables record — app reflects Active status and restores function | if BO can re-enable |

---

## Feature-Type Triggers

| Signal in AC | Additional scenario |
|---|---|
| Real-time update or live data | Side effect — data refreshes without manual reload |
| Audit log or history | Concurrent — action is logged correctly |
| OTP / verification code | Navigation (OTP screen UI, back-navigation target confirmed); Boundary (resend countdown, max attempts, expiry); Regeneration (resend invalidates old code, delivers new one) |
| Linked entity (address, account, saved item) | List pattern (empty state, display, search, sort, count limit); Navigation (entry points, back nav); Selection or Reference List (options from configuration) |

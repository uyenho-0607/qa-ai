---
inclusion: manual
---

# TC Scenario Coverage Guide

## Apply Coverage — Sweep, Match, Cross-cut

1. **Sweep** — map every screen the feature touches before reading the ACs: listing, form, review, confirmation, detail, OTP, etc.
2. **Match** — match each AC and BR to one or more patterns in § Coverage Minimum by AC Pattern. Apply all mandatory scenarios for every matched pattern.
   - Signals are **candidates, not matches**. Confirm the AC's subject actually is that thing before applying the pattern.
   - On collision, match the AC's **object**, not its verb: "display the withdrawal limit" is Financial Amount, not Display or UI.
   - No pattern matches → apply Happy Path + Negative + the cross-cuts below, and flag the AC for review.
3. **Cross-cut** — apply these regardless of AC wording:
   - Every error message harvested from the ticket → one scenario asserting that exact string.
   - Two or more fields have coupled validation → one scenario asserting that changing the controlling field resets or re-validates the dependent field.
   - A validation rule is stated without a status or condition qualifier → test it against every status/condition in scope.
   - A multi-step flow has 3+ screens → confirm the back-navigation target for every screen.
   - Real-time or live data → one scenario asserting data refreshes without manual reload.
   - Audit log or history → one scenario asserting the action is logged with correct actor, timestamp, and before/after values.
   - OTP or verification code → Navigation (OTP screen UI, back-navigation target); Boundary (resend countdown, max attempts, expiry); one scenario asserting resend invalidates the old code and delivers a new one.
   - Linked entity (address, account, saved item) → List, Table, or Search; Navigation / Screen Flow; Selection or Reference List.

**Unresolved rules.** When the ticket does not answer a question the rules above raise — reverse transition undocumented, scope of a rule unclear, back-navigation target unstated, a linked ticket's relevance unknown — write a `needs-clarification` row in `tc-plan.md` naming the question. Never guess the answer and never silently drop the scenario.

## Scenario Types

Use these type names exactly: Happy Path · Validation · Boundary · Negative · Empty / No Data · Permission / Role · Status Transition · Cross-Platform · Multi-Account · Concurrent / Side Effect · Navigation / Screen Flow · Mobile App Lifecycle · Cross-System Sync.

- **Validation** — input rejected by a field-level rule (required, format, length, range). Assertion is the field error message.
- **Negative** — action rejected by state, permission, or a business rule, not by field input. Assertion is the blocked outcome.
- **Boundary** — the edge value itself: min, max, zero, negative, limit−1 / limit / limit+1.
- **Cross-Platform** — same scenario on Desktop and Mobile.
- **Multi-Account** — behaviour varies by account type, group, or config.
- **Concurrent / Side Effect** — an effect outside the screen that triggered it: audit entry, balance change, linked record update, live refresh.
- **Navigation / Screen Flow** — entry points, back navigation, screen transitions, data retention.
- **Mobile App Lifecycle** — background, kill-app, network interruption — state recovery.
- **Cross-System Sync** — change in one system immediately reflected in another.

## Granularity and Assertions

- One TC per assertion group, not per label or per word. A screen's static labels, placeholders, and icons are one Display TC, not one each.
- Fields sharing identical validation rules collapse into one TC naming all of them. Apply a scenario per field only where the rules differ.
- Every Expected Result must assert the text of the AC/BR/ERR id the TC cites. If the id's wording and the assertion diverge, the citation is wrong or the scenario is.
- 8+ TCs on a single AC means the AC was split too finely — consolidate before writing.

---

## Coverage Minimum by AC Pattern

Unmarked scenarios are mandatory. `(if …)` = apply when that condition holds.

### Form Field or Input
Signals: enter · input · fill · submit · type · field · value

- Happy path — valid input accepted
- Empty / missing required field rejected
- Invalid format rejected
- Boundary — min (if min exists) · max (if max exists)
- Boundary — zero, negative (if numeric field)
- Below minimum length (if string field has a min-character rule)
- Special characters (optional)
- One TC covering all optional fields left empty — form still submits (if optional fields exist)

Happy path once per independently-validated field, not once per form. Pair every validation TC with its positive counterpart. For money fields, Financial Amount supersedes this pattern.

### Selection or Reference List
Signals: select · dropdown · choose · supported · configured · whitelist · options

- Options list matches the documented/configured set
- Each option displays correct label / icon (if specified)
- Selecting an option updates dependent field(s) correctly (if other fields depend on the selection)
- Search within modal — partial input filters results correctly (if modal has a search bar)
- Search within modal — clearing input restores the full list (if modal has a search bar)

### List, Table, or Search
Signals: list · table · search · filter · sort · column · pagination

- With data — correct display
- Empty state — correct message shown
- Search / filter returns correct results (if search exists)
- Search / filter returns no results (if search exists)
- Search / filter — clearing input restores the full list (if search exists)
- Sort ascending and descending (if sort exists)
- Pagination — navigate pages (if pagination exists)
- At max count — add action blocked with correct message (if a count limit exists)

### Permission or Role
Signals: role · permission · access · authorised · restricted · cannot · "only {role}"

- Authorised user can perform the action
- Unauthorised user is blocked with correct error
- Different roles see different UI or data (if roles differ)

### Financial Amount
Signals: amount · deposit · withdrawal · balance · funds · fee

- Valid amount — transaction succeeds
- Amount below minimum — rejected with message
- Amount above maximum — rejected with message (if max exists)
- Zero amount — rejected
- Negative amount — rejected
- Decimal precision enforced (if spec states it)
- Balance updated correctly after transaction

### Status or Workflow Transition
Signals: status · state · transition · approve · reject · cancel · close · reopen · pending

- Valid transition to correct next state
- Invalid transition blocked with message
- State reflected in UI after transition
- Reverse / undo transition — or a `needs-clarification` row if the ticket is silent
- Side effect on linked entities (if documented)
- Multiple triggers reach the same end-state — one scenario per trigger (if more than one trigger exists)

### Toggle, Button, or Action
Signals: enable · disable · toggle · activate · deactivate

- Action in enabled state
- Action in disabled state — blocked or greyed out
- State persists after page refresh
- Confirmation dialog for destructive action (if applicable)

### Display or UI
Signals: label · placeholder · layout · responsive · icon · tooltip · title

- Correct data displayed
- Correct label / placeholder text
- Modal opened from a field — correct title, close button, and list displayed (if field opens a modal or bottom sheet)
- Desktop behaviour
- Mobile behaviour (if cross-platform)
- Empty / loading state handled

### Multi-Account or Configuration-Dependent
Signals: account type · group · configuration · symbol config · user group · leverage

- Default / standard configuration
- Non-default configuration (if differences documented)
- Config change reflected correctly (if applicable)

### Navigation / Screen Flow
Signals: navigate · back · return · screen · flow · step · wizard · entry point · CTA

Also apply to every screen from the sweep.

- Entry point — correct screen is reached
- Back navigation — returns to previous screen
- Correct screen title and UI elements displayed
- Data retained when navigating back (if multi-step flow)
- CTA disabled until required fields are valid (if CTA has enabled/disabled state)

### Mobile App Lifecycle
Apply at each critical flow stage for mobile features.

- Background during form fill — data retained on resume
- Kill app during form fill — form cleared on reopen
- Kill app on confirmation/review screen — no record created
- Network interruption during submission — graceful error, no duplicate
- Session expiry during flow — re-auth prompt, no record created
- Background during OTP — countdown continues, OTP valid on resume (if OTP flow exists)
- Kill app during edit — unsaved changes discarded (if edit flow exists)

### Cross-System Sync
Signals: back office · BO · admin portal · sync · reflect in · audit log · history

Apply whenever a BO or admin system can view or modify the same records.

- Record created in app is visible in BO with correct fields (if BO visibility is documented)
- Record updated in app is reflected in BO (if BO visibility is documented)
- Record deleted in app shows correct status in BO (if audit retention is documented)
- BO action immediately reflected in app without restart (if BO can modify app records)
- BO re-enables record — app reflects Active status and restores function (if BO can re-enable)

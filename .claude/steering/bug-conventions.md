# Bug Conventions

## Title Format

Format: `[PROJECT_KEY][Module] symptom in one line`

- State what is wrong, not what should happen.
- Keep under 100 characters.
- Include the module so the bug is filterable without opening it.

```
✔ [OMS][Funds] Deposit button remains active when amount is below minimum
✔ [EMS][Order] Market order rejected with 500 error on valid symbol
✗ Deposit bug
✗ Verify that deposit validation works
```

## Description — Mandatory Sections

Every bug description must contain all four sections. A bug missing any section must not be filed.

| Section | Content |
|---|---|
| **Environment** | Platform, URL, user role, browser |
| **Steps to Reproduce** | Numbered steps, starting from the module entry point (not login) |
| **Actual Result** | What the tester observed — UI-visible, no interpretation |
| **Expected Result** | What should happen per the AC or spec |

## Write Steps to Reproduce

Start from the module entry point. Exclude login. Number every action. Each step is one action.

```
✔ 1. Navigate to Funds > Deposit
   2. Enter amount: 5
   3. Click Submit
✗ 1. Login and go to Funds and try to deposit 5 and click submit
```

## Write Actual vs Expected Result

State Actual as observed fact. State Expected from the AC or spec — never from assumption.

```
✔ Actual: Deposit submitted successfully. Balance unchanged.
   Expected: Error message displayed — "Amount must be at least 10"
✗ Actual: It doesn't work.
   Expected: It should work correctly.
```

## Assign Severity

| Severity | When to use |
|---|---|
| **Critical** | Core flow broken for all users — cannot deposit, login, place order |
| **High** | Core flow broken for a subset, or data loss risk |
| **Medium** | Feature partially broken — workaround exists |
| **Low** | Cosmetic, display issue, no functional impact |

## Classify FE vs BE

Intercept the network request before classifying. Never guess.

| BE | FE |
|---|---|
| 5xx response | API correct, UI displays wrong |
| Wrong or missing data in response | Layout or styling mismatch |
| Unexpected 4xx | Client JS error |
| Filter/sort param ignored by API | FE applies wrong filter/sort |

Ambiguous → mark as FE and note "classification unconfirmed — needs BE check".

## Block vs File Decision

File the bug and continue testing when the failure is isolated to the TC under test.

Block the TC and stop the test session when:
- The failure prevents any subsequent TC from running (e.g. login broken, account setup fails)
- The environment is unstable (repeated 5xx on unrelated requests)

Mark blocked TCs in Testmo with status Blocked and link the filed bug.

## Evidence Rule

Attach evidence to every bug. Minimum: one screenshot or one video.

| Scenario | Evidence type |
|---|---|
| Static state, missing element, wrong data | Screenshot |
| Multi-step flow, toast, navigation, state update | Video |
| API wrong data | Screenshot + network response visible |

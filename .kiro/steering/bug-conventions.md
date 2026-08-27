---
inclusion: manual
---

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

## Target Vocabulary

One vocabulary, shared with the exec plan and `capture-evidence`. Name the target before reproducing; never
infer it from the module name.

| Target | Driver | Domain file |
|---|---|---|
| `bo` | Playwright, desktop | `.kiro/domain/otc-bo.md` |
| `bo-mv` | Playwright, 390×844 | `.kiro/domain/otc-bo.md` |
| `ios` / `android` | mobile MCP | `.kiro/domain/otc-mobile.md` |
| `app-web` | Playwright | `.kiro/domain/otc-mobile.md` |

Rules spanning both surfaces — password policy, OTP, statuses, decimal precision — are in
`.kiro/domain/otc-shared.md`.

- **Filing a bug:** the target is where the defect was seen. A defect on two targets is one bug naming both,
  never two bugs.
- **Verifying a bug:** the target is the one the bug names. Where the bug names none, ask — never assume `bo`.
- Only Android is verified today; no iOS build exists yet
  (`.kiro/steering/mobile-mcp-rule.md` § Platform reality). An `ios` target with no device present is
  reported unavailable, not substituted.

## Classify FE vs BE

Never guess. What settles it depends on the target — the tables live in the per-surface section below.

- Ambiguous, on any target → mark as FE and note "classification unconfirmed — needs BE check".
- An unverifiable classification is stated, never invented.

## Web Targets — Reproduce and Classify

Read this section for `bo`, `bo-mv`, `app-web`, and skip the Device section entirely.
Follow `.kiro/steering/playwright-rule.md`.

- Start network interception **before** the first navigation. A request already sent cannot be intercepted.
- Resolve every element from the live DOM; apply § Locator Recovery on a miss.
- `bo-mv` resizes to 390×844 before navigating.

Classify from the intercepted request:

| BE | FE |
|---|---|
| 5xx response | API correct, UI displays wrong |
| Wrong or missing data in response | Layout or styling mismatch |
| Unexpected 4xx | Client JS error |
| Filter/sort param ignored by API | FE applies wrong filter/sort |

## Device Targets — Reproduce and Classify

Read this section for `ios`, `android`, and skip the Web section entirely.
Follow `.kiro/steering/mobile-mcp-rule.md`.

- Reach the start state by terminating and relaunching, never by tapping back through the stack. A reproduce
  that needs a cleared app also pays the env-gate and passcode setup — see that file § App State Rules.
- Resolve every element from a current `mobile_list_elements_on_screen` return. Never tap a coordinate no
  listing returned.
- **There is no network interception.** The `mobile` server observes no traffic. Collect instead: the backend
  check for the endpoint the symptom implicates, `mobile_list_crashes`, and the device log — all three per
  `.kiro/steering/mobile-mcp-rule.md`.
- Record the repro count. A symptom that appears once in two attempts is intermittent, and the bug says so.

No interception exists, so classify from three independent signals instead:

| Signal | Reads BE | Reads FE |
|---|---|---|
| Backend check on the implicated endpoint | endpoint returns the wrong state | endpoint returns the right state |
| `mobile_list_crashes` | — | a crash new to this run |
| Device log | server error in the app's lines | client-side exception in the app's lines |

A backend endpoint returning the correct state while the screen shows otherwise is FE. A backend endpoint
returning the wrong state is BE, and the screen is only corroboration. Where no endpoint in
`.kiro/locator-cache.json` § `api` covers the symptom, say so — an unverifiable classification is stated,
never invented.

**A wrong request is undetectable on a device target.** An app sending a bad parameter while the backend
answers correctly reads as FE with no proof. Note the limitation in the bug rather than asserting a cause.

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

One capture per target the bug reproduces on, each into its own file. A device capture carries a sidecar — a
native frame holds no in-frame label. Naming and paths: `.kiro/skills/capture-evidence/SKILL.md`
§ File Naming.

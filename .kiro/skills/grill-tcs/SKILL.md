---
name: grill-tcs
description: Grill a TC coverage plan before any test case is written — expected-result sources, missing negatives, weak oracles. Use when `generate-tcs` Phase 2 has written `tasks/{KEY}/tc-plan.md`, or when asked to grill or stress-test a plan.
---

# Grill TCs

Stress-test the coverage plan before a single case is written. Done when every `new` row in the plan answers all three questions with no gap.

## Contract

- **Args:** `{KEY}` [, `no-gate`]
- **Reads and updates:** `tasks/{KEY}/tc-plan.md`
- **Returns:** every `new` row at READY, or the row moved to Status `needs-clarification`
- **With `no-gate`:** resolve, update the plan, and hand the resolved table back without stopping — the caller owns the gate

## When to Run

**Mandatory** — invoked by `generate-tcs` Phase 2, or the input is a Jira ticket only (no existing TCs from Testmo or a Sheet).
**Optional** — the user asks, or the feature is complex or ambiguous.
**Skip** — existing TCs are the primary input; the job is to structure them, not invent coverage.

## The Three Questions

Every `new` row answers all three. A gap in any answer blocks that row from reaching TC writing.

**Q1 — Expected Result: where is the source?**
State the exact expected value and the plan's Expected-value source for it: AC id, error-message id, UI observation, domain file, or API field.
"The modal title is 'Reset Password'" traces to a Jira AC or a live UI snapshot, never to inference.

**Q2 — Negative: what is the failure path?**
Name the negative case for this scenario. With none planned, justify why (e.g. "read-only display, no input path").
An unjustified missing negative is a gap.

**Q3 — Oracle: could this TC pass on a bug?**
If the app returns a wrong value that superficially matches the check, would the TC still pass?
If yes → the assertion is too weak. Tighten the expected value or add a discriminating check.

## Flow

### 1. Load Plan
Read `tasks/{KEY}/tc-plan.md`. List every `new` row by screen.

### 2. Grill Each Row
Per row, answer Q1, Q2, Q3 in a table:

```
| # | Scenario | Q1 Source | Q2 Negative | Q3 Oracle Risk | Status |
```

Status is **READY** (all three answered, no gap) or **BLOCKED** (gap found, reason stated).

### 3. Resolve Gaps → GATE *(skip the gate with `no-gate`, or when invoked by another skill)*

Per BLOCKED row:
- Missing expected-value source → open the live UI or re-read the Jira AC. Resolve it, or move the row to Status `needs-clarification`.
- Missing negative → add the negative row to the plan, or justify its absence.
- Weak oracle → propose a tighter assertion.

Present the resolved table. **Wait for user approval before proceeding.**

### 4. Update Plan
Apply approved resolutions to `tasks/{KEY}/tc-plan.md` — new rows added, sources filled, statuses set.
Confirm: "Plan updated. [n] rows READY, [n] needs-clarification. Proceeding to TC writing."

## Hard Rules
- Every row reaches READY or `needs-clarification` before TC writing starts.
- A source of "inferred from context" is not a valid Q1 answer.
- Skipping a negative requires an explicit justification, not silence.
- Resolve a gap by strengthening the check or clarifying the requirement — never by weakening the check.
- A row that cannot reach READY after one resolution attempt → escalate to the user, invent no answer.

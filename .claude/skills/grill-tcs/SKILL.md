---
name: grill-tcs
description: Grill a TC coverage plan before any test case is written — expected-result sources, missing negatives, weak oracles. Use for plan grading via `tc-grader`, or when asked to grill or stress-test a plan.
---

# Grill TCs

Stress-test the coverage plan before a single case is written. Done when every `new` row in the plan answers all three questions with no gap.

## Contract

- **Args:** `{KEY}` [, `no-gate`] [, `platform` — id from `project-config.md` § Platforms; required for a standalone/gated run that dispatches `recon-scout`]
- **Reads and updates:** `tasks/{KEY}/gen/tc-plan.md`; a `recon-scout` dispatch writes screenshots to `tasks/{KEY}/gen/recon/`
- **Returns:** every `new` row at READY, or the row moved to Status `needs-clarification`
- **With `no-gate`:** resolve every row, return the resolved table, write no file.

## Scope

**Skip** — invoked standalone on a set of existing TCs where the job is to structure them, not invent coverage. Grade those with `review-tcs` instead.

Grill every `new` row. `covered by`, `gap`, and `needs-clarification` rows are exempt.

## The Three Questions

Every `new` row answers all three. A gap in any answer blocks that row from reaching TC writing.

**Q1 — Expected Result: where is the source?**
State the exact expected value and the row's Expected-value source per the plan's column rule.
"The modal title is 'Reset Password'" traces to a Jira AC or a live UI snapshot, never to inference.

**Q2 — Negative: what is the failure path?**
Name the negative case for this scenario. With none planned, justify why (e.g. "read-only display, no input path").
An unjustified missing negative is a gap.

**Q3 — Oracle: could this TC pass on a bug?**
If the app returns a wrong value that superficially matches the check, would the TC still pass?
If yes → the assertion is too weak. Tighten the expected value or add a discriminating check.
Resolve a gap by strengthening the check or clarifying the requirement.

## Flow

### 1. Load Plan
Read `tasks/{KEY}/gen/tc-plan.md`. List every `new` row by screen.

### 2. Grill Each Row
Per row, answer Q1, Q2, Q3 in a table:

```
| # | Scenario | Q1 Source | Q2 Negative | Q3 Oracle Risk | Status |
```

Status is **READY** (all three answered, no gap) or **BLOCKED** (gap found, reason stated).

### 3. Resolve Gaps → GATE *(skip the gate with `no-gate`, or when invoked by another skill)*

Per BLOCKED row:
- Missing expected-value source, standalone or gated invocation → dispatch the `recon-scout` agent with `{KEY}`, the platform id (see Contract), an instruction to write screenshots to `tasks/{KEY}/gen/recon/`, and the plan row's expected-value question as the fact to verify; re-read the Jira AC too. Resolve it, or move the row to Status `needs-clarification`.
- Missing expected-value source, under `no-gate` (e.g. dispatched by `tc-grader`, which holds no Agent tool and no live-UI access) → report it as an `ask` and mark the row `needs-clarification`. Do not attempt recon.
- Missing negative → add the negative row to the plan, or justify its absence.
- Weak oracle → propose a tighter assertion.

Present the resolved table. **Wait for user approval before proceeding.**

### 4. Update Plan
Apply approved resolutions to `tasks/{KEY}/gen/tc-plan.md` — new rows added, sources filled, statuses set.
Confirm: "Plan updated. [n] rows READY, [n] needs-clarification. Proceeding to TC writing."

Under `no-gate` this step is the caller's. Return the resolved table with each row's new status, source, and any row you added, and let the caller write it.

A row still short of READY after one resolution attempt → Status `needs-clarification` with the open question. Invent no answer.

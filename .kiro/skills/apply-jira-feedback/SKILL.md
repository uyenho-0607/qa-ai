---
name: apply-jira-feedback
description: Apply reviewer feedback from a Jira QA Preparation sub-task to the ticket's Testmo cases — classify, propose, update, report. Use when asked to apply review feedback for a ticket or update TCs from reviewer comments, /apply-jira-feedback.
---

# Apply Jira Feedback

The feedback lives on the QA Preparation sub-task; the cases live in Testmo. Carry one to the other.

**Done when:** every actionable comment is classified, and every approved change is applied in Testmo.

## Contract

| | |
|---|---|
| **Args** | `{KEY}` (the parent ticket) [, `no-gate`] |
| **Ids** | `PROJECT_ID = 8` (OTC) — per `.kiro/steering/testmo.md` § Testmo Projects |
| **Steering** | `tc-feedback-actions.md`, `tc-design-guide.md` |
| **Jira** | `searchJiraIssuesUsingJql`, `getJiraIssue` — read only |
| **Testmo** | `testmo_update_cases`, `testmo_create_cases`, `testmo_delete_cases` |
| **Writes** | Testmo cases · `tasks/{KEY}/base/tc.md` via the Phase 3 collector. No Jira write |

**Testmo write limits** — the phases below are shaped by these:

- `testmo_update_cases` applies one change set to **every** id in `ids`. Uniform changes (state, tags, folder) batch into one call; content edits take one call per case.
- Steps and expected results live in `customFields.custom_steps` as a whole array. Changing one step is a read-modify-write of the full array — there is no partial patch.
- `testmo_delete_cases` is irreversible, and a Testmo case has no `manual-tcs.md` to restore from. `delete` therefore means `state_id: 5` (Deprecated) unless the user says otherwise, case by case.

---

## Phase 1 — Locate the sub-task

Find the QA Preparation sub-task under `{KEY}` with `searchJiraIssuesUsingJql`:

```
parent = {KEY} AND issuetype = "QA Preparation"
```

Match on issue type, never on summary text — a QA Preparation sub-task's summary usually just repeats the parent's.

- One → use it.
- Two or more → list key, summary, status; ask which. **Wait.**
- None → stop. Report that `{KEY}` has no QA Preparation sub-task, and ask where the feedback lives.

**Done when:** one sub-task key is confirmed.

## Phase 2 — Read the feedback

`getJiraIssue` on that sub-task with `fields: ["comment"]`.

Take every comment asking for a change to a test case. Number them, quoting the phrase each is drawn from:

```
#1 — [what to change]   ("[quoted phrase]" — [author], [date])
```

Status updates, approvals, and unrelated discussion are not actionable — leave them out.

No actionable comments → report that and stop.

**Done when:** every actionable comment is numbered and quoted, and the total is stated.

## Phase 3 — Load current cases

Dispatch the `testmo-collector` agent for `{KEY}`, then read `tasks/{KEY}/base/tc.md`. No Agent tool in context → disclose_context("collect-testmo-cases") FULLY with `{KEY}`, `save`, `no-gate`. The `update` rows read steps and expected results from that file before rewriting.

Zero cases returned → stop and report.

**Done when:** every linked case is held with its id.

## Phase 4 — Classify and propose

Classify each numbered item using the action table in `.kiro/steering/tc-feedback-actions.md`, then map it to the case ids it touches.

```
Feedback — {KEY} / {SUBTASK-KEY}    [n] items · delete [n] · update [n] · add [n] · defer [n] · ask [n]

| # | Feedback | Case (id — name) | Action | Proposed change |
|---|---|---|---|---|
| 1 | "..." | 4821 — Sign Up – … | update | ER also asserts Continue stays disabled |
| 2 | "..." | 4830 — Sign Up – … | delete | Deprecate — covered by 4821 |
| 3 | "..." | (new) | add | New case in folder [n]: [name] |
| 4 | "..." | — | defer | AO-XXX handles this |
```

An item matching no existing case is `add (new)`, called out as a coverage gap.

**GATE — stop until the user approves, adjusts, or drops individual rows.** *(skip with `no-gate`)* With `no-gate`, every `delete` row is a deprecation — a hard delete always needs the gate.

A row proposing a hard delete rather than a deprecation is confirmed on its own, by case id, at this gate.

## Phase 5 — Apply

In order:

1. **add** — `testmo_create_cases`, fields per `to-testmo` § Field Mapping. The case content is the Phase 4 row — there is no `manual-tcs.md` in this flow.
2. **delete** — one `testmo_update_cases` call setting `state_id: 5` across every approved id. Separately confirmed hard deletes run `testmo_delete_cases` afterwards.
3. **update** — one `testmo_update_cases` call per case. A name change goes in `name`; a step or ER change rewrites the whole `customFields.custom_steps` array from the Phase 3 copy.
4. **defer / ask** — no Testmo write.

A failed call leaves its row unapplied and the run carries on; report it in Phase 6.

**Done when:** every approved row is applied or recorded as failed.

## Phase 6 — Report

Present, in chat only:

```
Applied — {KEY}    [n] updated · [n] deprecated · [n] added · [n] deferred · [n] failed

| # | Case (id) | Action | What changed |
|---|---|---|---|
```

List every deferred and `ask` row beneath it with its reason.

**Done when:** every Phase 4 row appears in the report with its outcome, failures included.

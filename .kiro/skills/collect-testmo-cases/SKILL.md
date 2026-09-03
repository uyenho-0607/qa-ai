---
name: collect-testmo-cases
description: Collect all Testmo test cases linked to a Jira issue key and output them as structured groups. Use when user says "collect TCs for AO-XXX", "collect testmo cases", /collect-testmo, or when another skill needs tc.md to exist.
---

# Collect Testmo Cases

Fetch, group, and deliver all test cases linked to a Jira issue key.

## Contract

- **Args:** `{KEY}` [, `save`] [, `no-gate`] — e.g. `AO-1120`
- **Ids:** `awk '/^## /{p = /Testmo Projects|Case Field IDs/} p' .kiro/steering/testmo.md` — `{PROJECT_ID}` = 8 (the OTC row in testmo.md § Testmo Projects, matched by {KEY}'s `AO` prefix), field ids for Phase 2
- **Writes:** `tasks/{KEY}/base/tc.md` — with `save` only, from `.kiro/skills/collect-testmo-cases/TEMPLATE.md`
- **With `no-gate`:** overwrite an existing `tc.md` without asking (see Phase 1 Gate below for the skip condition)
- **File exists** (with `save`, without `no-gate`): ask — overwrite | reuse | abort

## Phase 1 — Identify Cases

Call `testmo_find_cases_by_issue(projectId: {PROJECT_ID}, issueKey: "{KEY}")`.

The response is a `folders` map: `"<folderId> <folderName>"` → list of `"<caseId> <caseName>"` strings. Parse every case ID, name, and folder assignment from it.

Completion criterion: every case ID from the response is recorded with its name and folder.

## Phase 1 Gate *(skip if `no-gate`, or if invoked by another skill or agent)*

Present the case list grouped by folder, then ask:
> Fetch full details for all {N} cases? (`yes` / `no`)

- `yes` → Phase 2  |  `no` → stop (list already shown above)

## Phase 2 — Fetch Full Details

For each case ID, call `testmo_get_case(projectId: {PROJECT_ID}, caseId: ID)` to retrieve:
- `custom_description`, `custom_prerequisite`, `custom_test_data`
- `custom_steps` (array of `{text1, text3}`)
- `custom_automation1`, `custom_priority`, `state_id`

Strip HTML from all text fields.

Completion criterion: every case ID from Phase 1 has a fetched record with steps. If a fetch fails, write a placeholder with the error — no case is omitted.

## Phase 3 — Group by Name

Group cases by shared name prefix:
1. Strip the trailing variant (e.g. `"PnL Calculation - Forex Buy - Positive Profit"` → prefix `"PnL Calculation"`)
2. Cases sharing a prefix form one group; a solo case is its own group

Completion criterion: every case is assigned to a group named by its prefix.

## Phase 4 — Deliver

Write `tasks/{KEY}/base/tc.md` from `.kiro/skills/collect-testmo-cases/TEMPLATE.md`, then present. Skip the write when `save` was not given; present only.

Completion criterion (`save`): file exists, all N cases present, summary counts match detail counts.

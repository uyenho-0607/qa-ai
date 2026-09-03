---
name: mark-testmo-run
description: Submit Testmo run results — per-case status, optional bug link. Use when user says "submit testmo run result", "mark testmo run result", /mark-testmo-run, or after an exec run's report.md is written.
---

## Contract

- **Args:** `{KEY}` [, run ID] [, case ID(s) or title(s)] [, status] [, bug ID(s) for Failed cases]
- **Entry paths:** Manual (user provides identifiers) or From exec
  (`tasks/{KEY}/exec/report.md` § Result by Test Case — one row per TC per platform, carrying Case ID,
  status and bug key together). Read the report, not `exec.md`: the plan's result lines carry status
  but no bug key, so they cannot fill `issues` on a Failed case.
- **Output:** deep-link per submitted result

## Phase 1 — Resolve Run & Cases

1. Jira key (optional): use from args or exec context; if missing, ask.

2. From-exec entry path: `awk '/^## /{p = /Result by Test Case/} p' tasks/{KEY}/exec/report.md` — its `Case ID`, `Result` and `Bug` columns fill case id, status and `issues` respectively.

3. IDs lookup
   ```bash
   awk '/^#{2,3} /{p = /Testmo Projects|Jira Issue Connections|Run Result Deep-Link/} p' .kiro/steering/testmo.md
   ```
   Derive `projectId` from `{KEY}` prefix.

4. Case IDs: from the report read (step 2), else args, else `testmo_list_cases(projectId, name: title)` per title, else ask.

5. Run ID: from args, else `testmo_list_runs(projectId, isClosed: false)` → match by name. Still ambiguous? `testmo_get_run(runId)` on each candidate, compare `total_count` / `untested_count`.

6. Current state: `testmo_get_run(runId)` → note `untested_count` and the `statusN_count` breakdown (ids per Phase 2). Present run name and current breakdown. Wait for confirmation this is the right run.

7. Test IDs (optional): `testmo_list_run_test_ids(runId)` → map case IDs to test IDs. Count fewer than expected? Ask for confirmation before entering **Recovering Missing Test IDs** — it writes and reverts results in the live run.

8. Present: planned submissions (case name → status, bug ID if any). Wait for confirmation.

Done when: every target case has a confirmed test ID and the user has confirmed the submission plan.

---

## Phase 2 — Submit

For each confirmed result, call `testmo_create_run_result`:

```
statusId:     per result (2=Passed, 3=Failed, 4=Retest, 5=Blocked, 6=Skipped)
custom_steps: [{"status_id": null, "text1": "", "text2": null, "text3": null, "text4": null}]  # required; omitting it errors
comment:      null (omit unless user explicitly provided text)
issues:       [{ display_id: "{bugId}", integration_id: 1, connection_project_id: <from the Phase 1 § Jira Issue Connections read, matched by bugId's key prefix> }] if a bug ID was given for this result
```

Use `testmo_batch_create_run_results` when submitting >1 result.

Done when: every target test ID has a submitted result with the correct status.

## Phase 3 — Report

For each submitted result, output the run-result deep link in the format read in Phase 1.

Present a summary table:

| Case | Status | Link |
|---|---|---|
| {case name} | {status} | {deep-link} |

If any submission failed, list the failed test IDs and reasons. Do not silently skip.

---

## Recovering Missing Test IDs

Reached only from Phase 1 step 6: `total_count` is correct but `list_run_test_ids` returns fewer IDs.

**Follow:**
1. Probe IDs adjacent to the ones you have (e.g. known IDs 366529, 366531 → try 366527, 366528, 366530, 366532).
2. For each candidate, call `testmo_create_run_result` with a placeholder (e.g. Passed + "Mapping check — will update or revert"). Check `case_key` in the response:
   - Matches a target case → confirmed. Proceed to Phase 2 for this test ID.
   - 404 "belongs to a different test run" → invalid guess, nothing written, move on.
   - Succeeds but `case_key` is NOT a target → immediately call `testmo_delete_run_results([resultId])` to undo.
3. Stop once every target case has a confirmed test ID.

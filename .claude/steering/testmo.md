# Testmo — Reference Data

Project-specific constants and reference data for Testmo operations.

## Testmo Projects

- 5: Web Trader
- 6: OMS
- 7: MPG
- 8: OTC

## Configurations by Project

**OTC (8):**
- 43: Admin BO
- 45: Android app
- 46: iOS app

## Case Field IDs

Values for `testmo_create_cases` / `testmo_update_cases` custom fields.

**Priority (`custom_priority`):**
- 54: High
- 55: Medium
- 56: Low

**State (`state_id`):**
- 2: Pending Review

## Jira Issue Connections (for linking cases)

All use `integration_id: 1` (AQX - Jira).

- 10230: OMS
- 10461: AQX OMS
- 10014: Web Trader
- 10017: Multi Payment Gateway (MPG)
- 10263: AQXPAY-OTC
- 10362: AQXPAY-OTC-Product
- 10395: QA Team
- 10048: AQR Trader
- 10034: AQR BrokerBox
- 10024: Full Suite Product
- 10494: Engineering

## Deep-Link URL Formats

### Case Deep-Link (Repository View)

```
https://aquariux.testmo.net/repositories/{project_id}?group_id={folder_id}&case_id={case_id}
```

- `project_id` — from project list above (e.g. OMS = 6)
- `folder_id` — the `folder_id` field on the case
- `case_id` — the case `id` field

**Never use** `/repositories/{id}/cases/{case_id}` — returns 404.

### Run Result Deep-Link

```
https://aquariux.testmo.net/runs/view/{run_id}?test_id={test_id}
```

- `run_id` — the run ID
- `test_id` — the internal test ID within the run (from `list_run_results` → `test_id` field, or `list_run_test_ids`)

**Note:** `test_id` ≠ `case_id`. Test IDs are created when cases are added to a run.

**Always provide this link** when reporting run result actions to the user.

## Result Status IDs

- 1: Untested
- 2: Passed
- 3: Failed
- 4: Retest
- 5: Blocked
- 6: Skipped

## Finding a Run ID for a Jira Issue

1. Get the linked cases: `testmo_find_cases_by_issue(projectId, issueKey)` →
   returns case IDs grouped by folder, and how many cases the issue has.
2. List active runs: `testmo_list_runs(projectId, isClosed: false)`.
3. Match by name — runs are typically named after the issue key
   (e.g. `AO-970 (mix IOS , Android)`). Confirm the match with `total_count`:
   it should equal the case count from step 1.
4. Still ambiguous? `testmo_get_run(runId)` on each candidate and compare
   `total_count` / `untested_count`.

**Caveat:** a run's `total_count`/`untested_count` can be right while
`testmo_list_run_test_ids` still only returns a subset of the real test IDs
(seen on run 279 — correct name and case count, but only 2 of 6 test IDs
enumerable). Trust the run summary counts to confirm you have the right
run; don't trust `list_run_test_ids` to confirm every test exists until
you've tried submitting to it. See below for the recovery flow.

## Recovering Test IDs `list_run_test_ids` Doesn't Enumerate

Symptom: a run's `total_count`/`untested_count` are correct, but
`testmo_list_run_test_ids` returns fewer test IDs than that count.

Do NOT:
- Guess an arbitrary test ID from elsewhere in the account and submit to it
  blind — test IDs are global, not scoped per run, so a wrong guess can
  attach a result to an unrelated ticket.
- Try to fix it by resending the same case list via
  `testmo_update_run_overview` — this does not surface missing test IDs
  (tried on run 279, no effect).
- Remove and re-add cases via `testmo_update_run_overview` to force
  test-row recreation — if the hidden test rows already carry real data,
  removing the case could delete it. Don't do this without the user's
  explicit sign-off on that specific risk.

Do:
1. Probe test IDs immediately adjacent to the ones you already have
   confirmed (e.g. if `list_run_test_ids` gives you 366529 and 366531, the
   missing ones are very likely 366527, 366528, 366530, 366532, ...).
2. For each candidate, call `testmo_create_run_result` with a placeholder
   status/comment (e.g. Passed + "Mapping check — will update or revert").
   The response includes `case_key` directly — this confirms which case
   that test ID belongs to.
   - Case_key matches one of your target cases → keep it, then
     `testmo_update_run_result` with the real per-step results, evidence,
     and comment.
   - `testmo_create_run_result` 404s ("test does not exist ... belongs to
     a different test run") → the guess was invalid; nothing was written,
     no cleanup needed.
   - It succeeds but `case_key` is NOT one of your target cases → you've
     attached a placeholder result to an unrelated case. Immediately call
     `testmo_delete_run_results([resultId])` to undo it before doing
     anything else.
3. Stop once every target case has a matching test ID.

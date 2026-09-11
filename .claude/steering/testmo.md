# Testmo — Reference Data

## Testmo Projects

- 5: WT — prefix `WT`

## `custom_reqreference` is empty

Every sampled WT case (folders `98`, `324`, and others) has `custom_reqreference` null or empty.
`testmo_find_cases_by_issue(projectId: 5, issueKey: "WT-xxxx")` returns nothing — do not rely on it.
Resolve cases instead by:
- **Folder + case name** — `testmo_list_folders(projectId: 5)` to find the folder matching the
  ticket's feature, then `testmo_list_cases(folderId: ..., recursive: true)`.
- **Label form** — two forms seen on case names: a bare numeric case id, and `WT-xxxx_TC-xx`
  (ticket key + sequence). Match against the ticket key when present.

## Configurations by Project (WT, 5)

One config per client × platform, plus a shared Root Admin config:

| Client | Admin BO | Android app | Desktop Browser | iOS app | Mobile Web (MW) |
|---|---|---|---|---|---|
| AQXOMS *(legacy track, not a current WT client)* | 38 | 22 | 26 | 30 | 34 |
| Centroid | 39 | 23 | 27 | 31 | 35 |
| Lirunex | 40 | 24 | 28 | 32 | 36 |
| TransactCloud | 41 | 25 | 29 | 33 | 37 |

- 42: Root Admin (global, shared across clients)
- No `Hantec` config group exists — the Hantec brand runs on `TransactCloud`'s configs.
- `AQXOMS` is a leftover config group from before the current four-client split; it also has its
  own top-level folder (`518`, "AQX OMS Intergration"). Do not use it for a client-scoped case.

## Case Field IDs

Values for `testmo_create_cases` / `testmo_update_cases` custom fields, live-sampled from project 5.

**Priority (`custom_priority`, field id 2):**
- 54: High
- 55: Medium
- 56: Low

**Automation (`custom_automation1`, field id 22):**
- 37: Can Automate
- 38: In Progress
- 39: Automated
- 40: Not Automatable

**Regression (`custom_regression`, field id 27):**
- 57: YES
- 58: NO

**Test Case Type (`custom_test_case_type`, field id 29):**
- 79: Positive
- 80: Negative
- 81: Edge

**Login Method (`custom_login_method`, field id 13, multiselect)** — which account types the case
is valid for. Not every case sets this; when set, treat it as the case's matrix-account gate:
- 19: CRM
- 20: Live - MT4 / S1
- 21: Live - MT5 / S2
- 22: Demo - MT4 / S1
- 23: Demo - MT5 / S2
- 24: Live
- 25: Demo

**Steps (`custom_steps`, field id 5)** — sub-fields `Step` (id 50) and `Expected` (id 52) are active;
`Data` (51) and `-` (53) are inactive. In the API response this is `custom_steps[].text1` = step,
`custom_steps[].text3` = expected result — often populated only on the last step(s) of a case.

**Other text fields:** `custom_description` (Test Scenario), `custom_prerequisite`
(Pre-Requisites), `custom_test_data` (Test Data), `custom_remarks` (Remarks). All contain HTML.

**State (`state_id`):** system field, not from `testmo_list_fields` — `1`=Draft, `2`=Review,
`3`=Approved, `4`=Active, `5`=Deprecated.

## Jira Issue Connections (for linking cases)

All use `integration_id: 1` (AQX - Jira).

- 10014: Web Trader — prefix `WT`
- 10395: QA Team — prefix `QAT`, the automation-repo work-item project, not where WT bugs go

## Sheet Mirror

Google Sheet id `19xihRMCC4MCfAKLOTK7gc6NM62vYeKP5i1tVIGkfwUg`, default tab gid `1385147717`,
tabs named `TC-{KEY}`. The sheet carries an **Automation** status column Testmo itself lacks.

## Deep-Link URL Formats

### Case Deep-Link (Repository View)

```
https://aquariux.testmo.net/repositories/{project_id}?group_id={folder_id}&case_id={case_id}
```

- `project_id` — `5` for WT
- `folder_id` — the `folder_id` field on the case
- `case_id` — the case `id` field

**Never use** `/repositories/{id}/cases/{case_id}` — returns 404.

### Run Result Deep-Link

```
https://aquariux.testmo.net/runs/view/{run_id}?test_id={test_id}
```

- `run_id` — the run ID
- `test_id` — the internal test ID within the run (from `testmo_list_run_results` → `test_id` field, or `testmo_list_run_test_ids`)

**Note:** `test_id` ≠ `case_id`. Test IDs are created when cases are added to a run.

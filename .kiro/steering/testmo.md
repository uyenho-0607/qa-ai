---
inclusion: manual
---

# Testmo — Reference Data

## Testmo Projects

- 8: OTC — prefix `AO`

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

**Automation (`custom_automation1`):**
- 37: Can Automate
- 38: In Progress
- 39: Automated
- 40: Not Automatable

**State (`state_id`):**
- 2: Pending Review

## Jira Issue Connections (for linking cases)

All use `integration_id: 1` (AQX - Jira).

- 10263: AQXPAY-OTC — prefix `AO`
- 10362: AQXPAY-OTC-Product
- 10395: QA Team

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
- `test_id` — the internal test ID within the run (from `testmo_list_run_results` → `test_id` field, or `testmo_list_run_test_ids`)

**Note:** `test_id` ≠ `case_id`. Test IDs are created when cases are added to a run.


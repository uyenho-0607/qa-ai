---
inclusion: manual
---

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

## Users

- 7: Camcam — thicam.truong@aquariux.com
- 8: Dat — lethanhdat.nguyen@aquariux.com
- 9: Mai — thihuyen.mai@aquariux.com
- 10: Nguyen — nguyenle.nguyen@aquariux.com
- 11: Nam Phuong — ngocnamphuong.truong@aquariux.com
- 12: Alice — ngocloananh.le@aquariux.com
- 13: Lâm (Derrick) — truonghunglam.nguyen@aquariux.com
- 14: Kriss — ngocnguyen.pham@aquariux.com
- 15: Thuy Trang — thuythuytrang.vong@aquariux.com

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

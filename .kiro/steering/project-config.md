---
inclusion: always
---

# Project Configuration

## Setting up this project

New machine, a helper failing with `ModuleNotFoundError`, or a missing MCP tool: read `SETUP.md`.
Tell the user to run `./onboarding.sh` themselves — it needs a terminal and refuses to start without one.

## Environment

| Variable | Value |
|----------|-------|
| `PROJECT_KEY` | `AO` |
| `BO_URL` | `https://dashboard.aqxotc-sit.s20ip12.com` — login at `/login` — **VPN required** |
| `BO_MAKER` | `maimaker@yopmail.com` |
| `BO_CHECKER` | `maichecker@yopmail.com` |
| `BO_ADMIN` | `maiadmin@yopmail.com` |
| `SHARED_PASSWORD` | `Te5t1ng!` |
| `TC_SHEET_ID` | `1vWynEv7nsgF-dTJ8QB2o9M1fUpQamEcr4xd1q_yxLqI` |

OTC has one Back Office, not three apps — all three accounts share `BO_URL` and `SHARED_PASSWORD`.
Role capabilities: `.kiro/domain/otc-bo.md` § Roles & Permissions.

API credentials (`JIRA_EMAIL`, `JIRA_API`, `GOOGLE_*`) live in `.env` at the repo root

A row still reading `<FILL_IN>` when a skill needs it → ask the user for the value. Never substitute a plausible one.

## Folder Structure

```
tasks/{KEY}/  Working files per ticket
  jira.md  Fetched Jira ticket content
  tc.md  Collected TCs from Testmo or Sheet
  tc-plan.md  Coverage plan — one row per planned scenario
  manual-tcs.md  Generated TCs
  manual-tcs.csv  CSV export
  tc-review.md  TC review report — coverage, oracle, repro, form
  attachments/  Downloaded Jira image attachments
    figma-snapshot.md  Frozen Figma design snapshot
    figma-screenshots/  Exported Figma frame PNGs

evidence/{KEY}/  Bug evidence screenshots/videos
reports/{KEY}/  Coverage reports — commit if tracking history

.kiro/domain/  App knowledge base — modules, URLs, UI rules
.kiro/domain/flows.md  `ui-discovery` flow file — behaviour, validation, transitions
.kiro/locator-cache.json  Cached `data-testid` selectors for Playwright
```

## Tools
Jira site, `cloudId`, project id, issue-type ids, and transitions: `.kiro/steering/jira.md`
Testmo project, config, and field ids: `.kiro/steering/testmo.md`

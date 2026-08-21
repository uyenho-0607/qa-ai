---
inclusion: always
---

# Project Configuration

## Auto-Active Skills
**MANDATORY** Activate at session start: `Read .claude/skills/confirm-force/SKILL.md`, `Read .claude/skills/skill-follow/SKILL.md`

## Environment

| Variable | Value |
|----------|-------|
| `PROJECT_KEY` | `<FILL_IN>` |
| `OMS_BASE_URL` | `<FILL_IN>` |
| `OMS_USER` | `<FILL_IN>` |
| `EMS_URL` | `<FILL_IN>` |
| `EMS_TRADER_USER` | `<FILL_IN>` |
| `EMS_BACKOFFICE_URL` | `<FILL_IN>` |
| `EMS_BACKOFFICE_USER` | `<FILL_IN>` |
| `SHARED_PASSWORD` | `<FILL_IN>` |
| `TC_SHEET_ID` | `<FILL_IN — Google Sheet ID for TC template>` |

## Folder Structure

| Path | Purpose |
|---|---|
| `tasks/{KEY}/` | Working files per ticket — gitignored |
| `tasks/{KEY}/jira.md` | Fetched Jira ticket content |
| `tasks/{KEY}/tc.md` | Collected TCs from Testmo or Sheet |
| `tasks/{KEY}/tc-plan.md` | Coverage plan — one row per planned scenario |
| `tasks/{KEY}/manual-tcs.md` | Generated TCs |
| `tasks/{KEY}/manual-tcs.csv` | CSV export |
| `tasks/{KEY}/attachments/` | Downloaded Jira image attachments |
| `tasks/{KEY}/tc-review.md` | TC review report — coverage, oracle, repro, form |
| `evidence/{KEY}/` | Bug evidence screenshots/videos — gitignored |
| `reports/{KEY}/` | Coverage reports — commit if tracking history |
| `.claude/domain/` | App knowledge base — modules, URLs, UI rules |

## Tools
GitLab project id: `<FILL_IN>`
Jira site: `<FILL_IN>.atlassian.net` | `cloudId`: `<FILL_IN>` | project id: `<FILL_IN>`
Jira constants and transitions: see `.claude/steering/jira.md`

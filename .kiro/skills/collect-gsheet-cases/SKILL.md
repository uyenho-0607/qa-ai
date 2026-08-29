---
name: collect-gsheet-cases
description: Fetch test cases for a Jira issue key from a Google Sheet tab into tasks/{KEY}/base/tc.md. Use on "collect TCs from sheet", /collect-gsheet, or when another skill needs sheet-sourced tc.md.
---

# Collect Google Sheet Cases

Fetch all test cases for a Jira issue key from a Google Sheet and save to `tasks/{KEY}/base/tc.md`.

## Contract

- **Args:** `{KEY}` + spreadsheet URL [, `no-gate`]
- **Writes:** `tasks/{KEY}/base/tc.md` — an existing `tc.md` is overwritten
- **With `no-gate`:** stop after Phase 1.

---

## Phase 1 — Run Script

Confirm you hold {KEY} and the spreadsheet URL — ask for either if missing. Extract `spreadsheetId`
from the URL (between `/d/` and `/edit`), then run:

```
.venv/bin/python3 .kiro/skills/collect-gsheet-cases/fetch_gsheet_tcs.py --issue {issue-key} --sheet-id {spreadsheetId}
```

**Completion gate:**
- [ ] Script exits with code 0
- [ ] File exists at `tasks/{KEY}/base/tc.md`
- [ ] File contains at least 1 TC
- [ ] Parsed count matches the sheet's row count (the script reads `A1:Z1000` only — a sheet past 1000 rows needs the range widened)

**On failure, act on the message.** Each error carries its own answer:

| Message | Action |
|---------|--------|
| `Missing env vars: X, Y` | Ask the user to add exactly those vars to `.env` at the repo root. |
| `Tab not found. Available tabs: ...` | The list is printed. Pick the matching tab, or ask the user which one — never guess the issue key from the branch name. |
| `Tab is empty` / `No test cases parsed` | Ask the user to confirm the tab has rows below the header. |
| `No 'Test ID' column in header row` | The header is not row 1. Ask the user to confirm the header row position, or delete rows above it. |
| `HTTPError 400/401` from `oauth2.googleapis.com` | `GOOGLE_SHEETS_REFRESH_TOKEN` is expired. Ask the user to re-issue it. |

---

## Phase 2 — Classify TCs *(skip if `no-gate`)*

Read `tasks/{KEY}/base/tc.md` and for each TC:
- Classify: automatable vs manual (concrete reason)
- Default automatable; manual only for hard blockers (e.g. captcha, hardware, 2FA via physical device)
- If **Automation** is ✅ automated → Classification is Automatable, no reason needed.

Add to each TC, after **Automation:** — `- **Classification:** {Automatable | Manual — reason}`.

---
name: collect-gsheet-cases
description: Fetch all test cases for a Jira issue key from a Google Sheet and save as a structured .md file for analysis. Use when user says "collect TCs from sheet for OMS-XXX", "fetch test cases from google sheet", /collect-gsheet
---

# Collect Google Sheet Cases

Fetch all test cases for a Jira issue key from a Google Sheet and save to `tasks/{KEY}/base/tc.md`.

## Contract

- **Args:** `{KEY}` + spreadsheet URL [, `no-gate`]
- **Writes:** `tasks/{KEY}/base/tc.md`
- **Output exists:** ask — overwrite | reuse | abort
- **With `no-gate`:** overwrite `tc.md` without asking and stop after Phase 1.

---

## Phase 1 — Run Script

**Run the command below as your first action.** Do not inspect anything beforehand — no
reading the script, no checking whether `.env` exists or what is in it, no listing skill
directories, no comparing copies of the script. The script resolves `.env` from the repo
root itself and prints everything you need on failure. Pre-flight checks are pure waste.

Ask the user for the spreadsheet URL and the issue key only if not already provided.
Extract `spreadsheetId` from the URL (long string between `/d/` and `/edit`).

```
.venv/bin/python3 .kiro/skills/collect-gsheet-cases/fetch_gsheet_tcs.py --issue {issue-key} --sheet-id {spreadsheetId}
```

**Completion gate:**
- [ ] Script exits with code 0
- [ ] File exists at `tasks/{KEY}/base/tc.md`
- [ ] File contains at least 1 TC

**On failure, act on the message — do not go exploring.** Each error carries its own answer:

| Message | Action |
|---------|--------|
| `Missing env vars: X, Y` | Ask the user to add exactly those vars to `.env` at the repo root. Do not go looking for `.env`. |
| `Tab not found. Available tabs: ...` | The list is printed. Pick the matching tab, or ask the user which one — never guess the issue key from the branch name. |
| `Tab is empty` / `No test cases parsed` | Ask the user to confirm the tab has rows below the header. |

---

## Phase 2 — Classify TCs *(skip if `no-gate`)*

Read `.kiro/skills/collect-gsheet-cases/TEMPLATE.md` for the Classification field format.

Read `tasks/{KEY}/base/tc.md` and for each TC:
- Classify: automatable vs manual (concrete reason)
- Default automatable; manual only for hard blockers (e.g. captcha, hardware, 2FA via physical device)
- Note current **Automation** field value: ✅ automated / 🚧 in progress / ⬜ not set

Update the file with classification column added to each TC per the `Classification` field in TEMPLATE.md §Full Case Details.

---

## Hard Rules
- Never skip the script — do not read the sheet manually via MCP
- If `tasks/{KEY}/` does not exist, the script creates it automatically
- Never omit TCs — if a TC is missing from the output, re-run the script

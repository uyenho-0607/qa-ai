---
name: jira-handler
description: Handle Jira operations — create SIT bugs, upload evidence, transition issues, post verification comments. Use when user asks to file a bug, upload evidence, transition/close/reopen a bug, or verify a fix.
---

# Jira Handler

Execution skill for Jira write operations. Called by `report-bug`, `verify-bug`, or directly.

---

## Config

Extract Jira constants before the first write call:
```bash
awk '/^## /{p = /Rovo MCP|Transitions/} p' .kiro/steering/jira.md
```
Read `.kiro/skills/jira-handler/dev-team.md` for dev-team account IDs.

---

## Scripts

| Script | Purpose |
|--------|---------|
| `jira_attach.py` | Upload files (no comment) |
| `jira_comment.py` | Upload files + post ADF comment |
| `jira_comment.py --delete {ID}` | Delete a comment |
| `jira_attach.py --delete {ID}` | Delete attachment(s) |
| `jira_desc_update.py --issue {KEY} --file {path} --filename {name} --adf-file {path}` | Upload + set description (atomic) |
| `jira_desc_update.py --get-media-uuid {IDs}` | Resolve attachment IDs → UUIDs (helper) |

All at `.kiro/skills/jira-handler/`. Run with `.venv/bin/python3`.

### Multiple Files Syntax

For multiple files, repeat the flags:

```bash
.venv/bin/python3 .kiro/skills/jira-handler/jira_comment.py \
  --issue OMS-XXX \
  --file path/to/file1.png --file path/to/file2.png \
  --filename "display1.png" --filename "display2.png" \
  --comment $'Comment text'
```

---

## Action: create_bug

1. `createJiraIssue` — type `SIT Bug`, parent, assignee, `additional_fields: {"priority": {"name": "Medium"}}`
2. Write temp ADF JSON with `{MEDIA_1}` placeholders (⛔ READ `.kiro/skills/jira-handler/adf-templates.md`)
3. `.venv/bin/python3 .kiro/skills/jira-handler/jira_desc_update.py --issue {KEY} --file {path} --filename {name} --adf-file {adf_path}`
   — uploads file, substitutes `{MEDIA_1}` with UUID, updates description in one call
   — multiple files: repeat `--file`/`--filename` pairs; placeholders fill in order `{MEDIA_1}`, `{MEDIA_2}`…

---

## Action: post_verification

```bash
.venv/bin/python3 .kiro/skills/jira-handler/jira_comment.py --issue {KEY} --file {path} --filename {name} --comment $'{emoji} Verified {verdict} — {ENVIRONMENT}\n\n**Result:**\n{result_text}'
```

- `✅ Verified FIXED` or `❌ Verified NOT FIXED`
- ONE comment per event, all media inlined
- Multiple files: repeat `--file`/`--filename` pairs

---

## Action: transition

`transitionJiraIssue` with ID from `.kiro/steering/jira.md`. If fails → `getTransitionsForJiraIssue`.

---

## Hard Rules

- ALWAYS `$'...\n...'` for multiline — never `"...\n..."`
- NEVER `jira_comment.py` for bug creation (posts unwanted comment)
- NEVER create bug without evidence
- NEVER leave an unfilled `{MEDIA_N}` — placeholder count must equal `--file` count, else Jira 400s on a literal `{MEDIA_N}` media id
- NEVER post multiple comments for one verification

---
name: apply-sheet-feedback
description: Fetch reviewer comments from a Google Sheet TC tab, classify each as delete / update / add, propose fixes, apply the minimal sheet changes, and report. Use when asked to apply feedback from a sheet, /apply-feedback.
---

# Apply Sheet Feedback

**Done when:** every open comment and its replies are classified; every approved fix is applied to the sheet using the most surgical command available; a fixed note is written to col P of the affected row; a summary report is presented.

## Contract

| | |
|---|---|
| **Args** | `{SHEET_ID}` , `{TAB}` (sheet tab name, e.g. `AO-306`) [, `no-gate`] — `{KEY}` in the paths below is the ticket key; it equals `{TAB}` unless the user says otherwise |
| **Sheet tool** | `mcp__google-docs__listSheetsComments` + `mcp__google-docs__getSheetsComment` for replies |
| **Script** | `scripts/format_tc_sheet.py` — use `--patch-ids`, `--remove-ids`, `--insert-before` as needed; never full rewrite unless explicitly asked |
| **Writes** | col P notes on affected TC rows; col P is the only column written outside A–O |
| **Steering** | `tc-feedback-actions.md`, `tc-design-guide.md` |
| **no-gate** | Classify → propose → apply every approved fix without stopping; caller owns report |

---

## Phase 1 — Fetch comments

1. Call `mcp__google-docs__listSheetsComments` with `includeResolved: false` to get all open comments.
2. For every comment whose `replies` array is non-empty, call `mcp__google-docs__getSheetsComment` to retrieve full reply thread.
3. Build a flat list of comment objects, each with: `id`, `author`, `content`, `quotedText`, `replies[]`.

Present nothing to the user yet — proceed directly to Phase 2.

---

## Phase 2 — Classify & propose

Classify each comment + reply thread using the action table in `.claude/steering/tc-feedback-actions.md`.

Present the classification table and proposed fix for each comment — **one row per comment thread**:

```
Feedback — {TAB}    [n] comments · delete [n] · update [n] · add [n] · defer [n] · ask [n]

| TC (current ID) | Comment | Action | Proposed fix |
|---|---|---|---|
| TC-nn | "..." | update | Change pre-req to X; update ER to Y |
| TC-nn | "..." | delete | Remove TC — covered by TC-mm |
| (new) | "..." | add | Insert new TC before TC-nn: [scenario description] |
| TC-nn | "..." | defer | AO-XXX handles this — no change |
```

**GATE — stop until the user approves, adjusts, or skips individual items.** *(skip with `no-gate`)*

---

## Phase 3 — Write minimal change files

For each approved action, choose the most surgical file write:

**delete** — no patch file needed. `--md` is required by the script even in remove mode, so pass the existing source file:
```
.venv/bin/python3 scripts/format_tc_sheet.py \
  --md tasks/{KEY}/manual-tcs.md \
  --sheet {SHEET_ID} --tab {TAB} \
  --remove-ids "{TC-ID}"
```

**update (ER / pre-req / scenario / name / steps)** — write only the affected TC block(s) to a small temp md file `tasks/{KEY}/patch-{TC-ID}.md`. The TC block in this file **must use the TC's current ID exactly as it appears in the sheet** (e.g. `AO-306_TC-18`) — `--patch-ids` matches by ID to locate the target rows. Then run:
```
.venv/bin/python3 scripts/format_tc_sheet.py \
  --md tasks/{KEY}/patch-{TC-ID}.md \
  --sheet {SHEET_ID} --tab {TAB} \
  --patch-ids "{TC-ID}"
```

**update (module only)** — write the cell directly via `mcp__google-docs__writeSpreadsheet` to the Module column of the TC's first row. No script run needed.

**add** — write the new TC block to `tasks/{KEY}/insert-{description}.md`, heading it `## {KEY}_TC-INSERT` so the renumber pass assigns its number. Then run:
```
.venv/bin/python3 scripts/format_tc_sheet.py \
  --md tasks/{KEY}/insert-{description}.md \
  --sheet {SHEET_ID} --tab {TAB} \
  --insert-before "{BEFORE-TC-ID}" \
  --insert-md tasks/{KEY}/insert-{description}.md
```

**defer** — no file, no command. Write a pending note to col P only.

Multiple `--patch-ids` can be batched into one command when the TCs are in the same source md file. Never write more TC blocks to a patch file than are actually being changed.

---

## Phase 4 — Apply & annotate

Execute the commands from Phase 3 in order:
1. Deletes first
2. Inserts next
3. Patches last
4. Module-only writes last

After each command completes, write the col P note to the first row of the affected TC:
- Approved fix: `[Fixed] {one-line description of what changed}`
- Deferred: `[Pending] {reason} — see {ticket}`

Use `mcp__google-docs__writeSpreadsheet` for col P writes. Target `{TAB}!P{row}`.

Then attempt to resolve each actioned comment via `mcp__google-docs__resolveSheetsComment`. Note: the Drive API may not persist resolved status in the Sheets UI — the col P note is the reliable record.

---

## Phase 5 — Report

Present the final summary:

```
Applied — {TAB}    [n] fixes · [n] pending · [n] skipped

| TC (new ID) | Action | What changed |
|---|---|---|
| TC-nn | updated | Pre-req corrected to X screen |
| TC-nn | deleted | Removed — covered by TC-mm |
| TC-nn (new) | added | New TC: {scenario name}, inserted before TC-mm |
| TC-nn | deferred | AO-XXX handles network interruption |

Col P notes written to: [list of rows]
Comments resolved: [n] (manual resolution may still be needed in Sheets UI)
```

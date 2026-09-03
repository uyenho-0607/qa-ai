---
name: apply-sheet-feedback
description: Fetch reviewer comments from a Google Sheet TC tab, classify each as delete / update / add / defer / ask, propose fixes, apply the minimal sheet changes, and report. Use when asked to apply feedback from a sheet, /apply-feedback.
---

# Apply Sheet Feedback

**Done when:** every open comment and its replies are classified; every approved fix is applied to the sheet using the most surgical command available; a fixed note is written to col P of the affected row; a summary report is presented.

## Contract

| | |
|---|---|
| **Args** | `{SHEET_ID}` , `{TAB}` (sheet tab name — the ticket key, e.g. `PROJ-306`) [, `no-gate`] — `{KEY}` in the paths below is the ticket key; it equals `{TAB}` unless the user says otherwise |
| **Sheet tool** | `mcp__google-docs__listSheetsComments` + `mcp__google-docs__getSheetsComment` for replies |
| **Script** | `scripts/format_tc_sheet.py` — use `--patch-ids`, `--remove-ids`, `--insert-before` as needed; never full rewrite unless explicitly asked |
| **Writes** | col P notes on affected TC rows (col P is the only column written outside A–O); scratch patch/insert md files under `tasks/{KEY}/` |
| **Steering** | `tc-feedback-actions.md`, `tc-design-guide.md` |
| **no-gate** | Classify → propose → apply every fix; skip Phase 5, the caller reports |

---

## Phase 1 — Fetch comments

1. Call `mcp__google-docs__listSheetsComments` with `includeResolved: false` to get all open comments.
2. For every comment whose `replies` array is non-empty, call `mcp__google-docs__getSheetsComment` to retrieve full reply thread.
3. Build a flat list of comment objects, each with: `id`, `author`, `content`, `quotedText`, `replies[]`.

Proceed directly to Phase 2.

---

## Phase 2 — Classify & propose

Classify each comment + reply thread using the action table in `.kiro/steering/tc-feedback-actions.md`.

Present the classification table and proposed fix for each comment:

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

`--md` is a hard requirement the script enforces regardless of mode, even when a code path doesn't use its parsed content — each branch below says what to point it at.

For each approved action, choose the most surgical file write:

**delete** — no patch file needed. Any parseable TC md already in `tasks/{KEY}/` satisfies `--md` (remove mode doesn't use its content). If none exists, stop and name the producer — `/generate-tcs` (see § Producers, project-config.md):
```
.venv/bin/python3 scripts/format_tc_sheet.py \
  --md tasks/{KEY}/gen/manual-tcs.md \
  --sheet {SHEET_ID} --tab {TAB} \
  --remove-ids "{TC-ID}"
```

**update (ER / pre-req / scenario / name / steps)** — write only the affected TC block(s) to a small temp md file `tasks/{KEY}/patch-{TC-ID}.md`. The TC block in this file **must use the TC's current ID exactly as it appears in the sheet** (e.g. `{KEY}_TC-18`) — `--patch-ids` matches by ID to locate the target rows. The file must also carry the `**Story:**`/`**Configuration:**` file-level headers plus a complete TC block — the parser blanks those two sheet columns when the header is missing. Then run:
```
.venv/bin/python3 scripts/format_tc_sheet.py \
  --md tasks/{KEY}/patch-{TC-ID}.md \
  --sheet {SHEET_ID} --tab {TAB} \
  --patch-ids "{TC-ID}"
```
After every `--patch-ids` or `--insert-before` run, spot-check (or explicitly re-write) the affected row's Module, Login Method, and Automation cells — don't assume they came through correctly.

**update (module only)** — write the cell directly via `mcp__google-docs__writeSpreadsheet` to the Module column — column B — of the TC's first row. No script run needed.

**add** — write the new TC block to `tasks/{KEY}/insert-{description}.md`, heading it `## {KEY}_TC-INSERT` so the renumber pass assigns its number. Point `--md` at this same file; `--insert-md` is what supplies the inserted TCs:
```
.venv/bin/python3 scripts/format_tc_sheet.py \
  --md tasks/{KEY}/insert-{description}.md \
  --sheet {SHEET_ID} --tab {TAB} \
  --insert-before "{BEFORE-TC-ID}" \
  --insert-md tasks/{KEY}/insert-{description}.md
```

**defer** — no file, no command. Write a pending note to col P only.

**ask** — no file, no command; carry the question to the Phase 5 report.

Multiple `--patch-ids` can be batched into one command when the TCs are in the same source md file. Never write more TC blocks to a patch file than are actually being changed.

---

## Phase 4 — Apply & annotate

0. Read the Test ID column (`mcp__google-docs__readSpreadsheet` on `{TAB}!A:A`) and build a TC ID → first-row-index map. Re-read and rebuild this map after any command that renumbers rows (every delete, and every insert-before).

Execute the commands from Phase 3 in order — every ID-keyed edit lands before the first renumber, because `--remove-ids` and `--insert-before` renumber all TCs and would shift the IDs the patches match on:
1. Patches first
2. Module-only writes next
3. Deletes next
4. Inserts last

After any delete, re-resolve every remaining patch ID and every `--insert-before` ID from the sheet, and say so. Delete the patch and insert md files once their commands succeed.

After each command completes, write the col P note to the first row of the affected TC — except a delete, which gets no col P note (the row is gone; a note written there would land on whatever TC shifted up into the vacated slot). Record deletes in the Phase 5 report only.
- Approved fix: `[Fixed] {one-line description of what changed}`
- Deferred: `[Pending] {reason} — see {ticket}`
- Ask: `[Question] {the open question}`

Use `mcp__google-docs__writeSpreadsheet` for col P writes. Target `{TAB}!P{row}`, using the row map from step 0.

Then attempt to resolve each actioned comment via `mcp__google-docs__resolveSheetsComment`. Note: the Drive API may not persist resolved status in the Sheets UI — the col P note is the reliable record.

---

## Phase 5 — Report *(skip with `no-gate`)*

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

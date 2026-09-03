---
name: manual-exec-run
description: Execute exec.md, the manual SIT plan, on every platform it names. Run by wave, capture evidence, write each result back in place. Use on "run manual tests", /exec-run.
---

## Contract

- **Args:** `{KEY}` [, `evidence_dest={url}`] [, `finalise`]
- **Reads:**
 `tasks/{KEY}/exec/exec.md`
 `.kiro/steering/project-config.md` § Environment, § Platforms, § Folder Structure — extract, never whole:
 `awk '/^## /{p=/^## (Environment|Platforms|Folder Structure)$/} p' .kiro/steering/project-config.md`
 the platform packs `project-config.md` § Platforms names — the enabled platform's pack loads whole
 `.kiro/docs/lessons.md`, `.kiro/steering/capture-mechanics.md`, and the driver and capture files for each
 platform kind in play — the Phase 2 gate lists them
 `.kiro/locator-cache.json`, the endpoint section named in the pack § Observables, for a backend check only — that section alone, never whole
- **Writes:**
 `tasks/{KEY}/exec/exec.md` (result lines in place)
 `tasks/{KEY}/exec/report.md`
  evidence files per `project-config.md` § Folder Structure
 `.kiro/docs/lessons.md` (Phase 3 append)
 `tasks/{KEY}/exec/.upload/` — queue state, and one `ledger-{wave}.md` per wave, both written by the delegates below
- **Delegates:** `evidence-uploader` agent (per wave, background), `evidence-auditor` agent (Phase 3), `dup-scout` agent (Phase 4), `capture-evidence`, `scaffold-evidence-doc`, `report-bug`
- **With `finalise`:** run Phase 4 alone — re-enter bug triage on an existing `report.md`. No `report.md` → STOP: Phases 1–3 have not run.
- **Guardrails:** Execute all phases strictly in sequence. Name no platform directly; derive all platform facts from `project-config.md` § Platforms. If `exec.md` is missing, STOP and prompt user to run `/manual-exec-design {KEY}`

## Rules

- **Plan Authority:** `exec.md` is strictly binding. Do not re-derive anything.
- **Result Independence:** Assertions determine pass/fail verdicts; evidence capture status does not.
- **Uploads Are Delegated:** This session captures and records; it never ships a capture or waits on one. Every upload goes to the Phase 1 worker through the per-wave `evidence-uploader`.
- **Result Scope:** Exactly one result line per platform per TC (or per pair for cross-platform flows).
- **Recon Passes:** SKIP execute TCs marked `- {platform} · ✅ PASSED (verified at recon...)`
- **Platform Divergence:** Cross-platform behavioral differences are findings, not variants. Log both observations.
- **Bug Keys Live in the Report:** `report.md` is the only file that carries a bug key. `exec.md` records what was observed and is never edited after Phase 3 — a key written into both files is a key that drifts.

---

## Phase 1 — Load, Preflight & Resume

1. **Registry & Header Read**:
   - Read active platform definitions from `.kiro/steering/project-config.md` § Platforms.
   - Read `exec.md` header up to `## Test Cases`. Extract `Evidence mode` and `Annotations` settings.

2. **Evidence Destination**:
   - If `evidence_dest` arg is given → use it. A user-supplied doc or folder gets a write-access probe first
     (insert-then-delete for a doc, probe file for a folder); on failure, fall back to the created
     destination for the mode below.
   - If not → derive from `Evidence mode`:
     - `normal`: create a new Drive folder named `[{KEY}] SIT Evidence`. Record its URL and folder id.
     - `screenshot`: disclose_context("scaffold-evidence-doc") with `{KEY}`. Record the returned URL and doc id.
   - Write it down as the `--dest` string every later `add` will carry:
     - Drive folder → `drive:{folderId}`
     - Doc → `doc:{docId}#{section}`, the section being that TC's own case-name paragraph — plain text,
       not a styled heading
   - **Start the upload worker, once, in the background** — `Bash` with `run_in_background: true`:
     ```bash
     .venv/bin/python3 scripts/evidence_upload.py serve --key {KEY}
     ```
     One worker serves the whole run, and every wave's `evidence-uploader` waits on **this** worker
     rather than starting its own. Record its task id so Phase 3 can stop it. Then confirm it is
     serving with both checks — `status` alone is unreliable (`worker_pid` can read `null` while the
     process is still running):
     ```bash
     .venv/bin/python3 scripts/evidence_upload.py status --key {KEY} --json
     pgrep -f "evidence_upload.py serve --key {KEY}"
     ```
     Non-zero exit on `status`, and no match from `pgrep` → the worker did not start; stop and report.

3. **Build Index**:
   - Index TC positions and result lines:
     ```bash
     grep -n '^### TC-\|^- .* · [⏳✅❌🚫]' tasks/{KEY}/exec/exec.md
     ```
   - The status glyph is what makes a result line a result line. Without it the pattern also matches
     `## Execution Context` bullets — `- **Platforms** — Back Office · Member app` — and the resume
     protocol reads them as TCs. Never loosen it.
   - A result write replaces one line with one line. Re-index only after a line actually moves — a
     compaction recovery, or a hand edit.

4. **Preflight Checks**:
   - **Platform**: Confirm device/URL availability per pack § Preflight. Compare observed build against `exec.md` § Preflight: If plan build is:
      - `unknown` → Update plan row with observed build and continue.
      - Disagrees with observed build → STOP and ask user. (Disagreement invalidates recon passes: reset `verified at recon` results to `⏳ PENDING`).
   - **Data**: Verify existence of all prerequisites in `## Preflight` → `### Data`. Block dependent TCs if data is missing.

5. **Resume State Protocol**:
   - Read index result lines per platform:
     - `✅ PASSED`: Skip (do not re-execute or overwrite evidence).
     - `⏳ PENDING`: Queue for execution.
     - `❌ FAILED` / `🚫 BLOCKED`: Prompt user (Retry or Keep). Retrying resets status to `⏳ PENDING` and clears prior result prose.
   - Cross-platform pairs execute/resume as a single unit.

Done when: Header, registry, index, and evidence destination are loaded; preflights pass; resume strategy is stated per platform.

---

## Phase 2 — Execute by Wave

**HARD GATE — do not start Wave 1 until all items below are confirmed loaded into context:**
`.kiro/docs/lessons.md`
`.kiro/steering/capture-mechanics.md`
- Group = `web`: `.kiro/steering/capture-web.md`, `.kiro/steering/playwright-rule.md`
- Group = `device`: `.kiro/steering/capture-device.md`, `.kiro/steering/maestro-rule.md`

Missing any → load it now. **Skipping this gate is not permitted.**

Run waves sequentially as defined in `## Waves`. Execute wave `Reset` action and open specified `Sessions` count before starting wave TCs:
- **Single-group wave**: Run on platforms in `Platforms` column, completing one platform fully before starting the next.
- **Cross-platform wave**: Open both sessions simultaneously; run once per pair.

---

### TC Slicing & Micro-Execution Loop

Slice each runnable TC block:
```bash
sed -n '{start_line},{end_line}p' tasks/{KEY}/exec/exec.md
```

Execute each sliced TC using the 5 steps:

1. **Precondition**: Navigate to specified account/screen. If omitted, confirm current state matches previous TC output.
2. **Steps**: Execute steps strictly. Apply `Steps on {platform}` overrides where applicable. For cross-platform flows, switch between open sessions per step prefix.
3. **Assert**: Verify `Expected` assertions against pack observables (not screenshots).
   - In `screenshot` mode, capture frame at assertion moment using stem from `## Evidence` → `### Frames`.
   - Record the verdict from the assertion, not the frame. Image read-back belongs to the auditor —
     see `capture-mechanics.md` § Verify.
   - **On Assertion Failure**:
     1. Re-run assertion once (log `2/2` for persistent failure, `1/2` for intermittent).
     2. Perform backend API check if endpoint is named in assertion. Endpoints and their bearer token come
        from the section that platform's pack names under § Observables — extract that section alone,
        never the file: `jq '.{section}' .kiro/locator-cache.json`.
     3. Check console/crash logs per pack § Observables.
     4. Capture diagnostic logs if bug report is required.
4. **Record Result**: Rewrite this TC's result line in `exec.md`, **one line for one line**:
   `- {platform label} · {✅ PASSED | ❌ FAILED | 🚫 BLOCKED} · {YYYY-MM-DD HH:MM} · {notes}`
   Notes ride on the same line, `·`-separated, carrying what applies: observed against expected, repro count (`2/2`), backend check, crash id or console error, the blocker on a block, any target string that changed, any capture that could not be produced. Never indent detail beneath the line — the report is where these expand into fields.
   **No re-index.** Take the timestamp from `date '+%Y-%m-%d %H:%M'`, never from memory.
5. **Teardown**: Execute explicit teardown steps. Continue to next TC regardless of pass/fail result.

---

### Group Evidence & Parallel Upload Protocol

- **`screenshot` Mode**: Frames captured inline during Step 3 using `capture-web.md` or `capture-device.md` per active platform.
- **`normal` Mode**: disclose_context("capture-evidence") with `targets={active platforms}`, `type={the group's Type, lowercased}`, `stem={stem}`, `dest=tasks/{KEY}/exec/evidence/`, `element={the asserted element's id=/desc=/text=}`, `label={what is being verified}`, and `annotation={annotations}` from the header — per group after the group finishes testing.
  - `type` is the `Type` cell of that group's row in `## Evidence` → `### Groups` — `SCREENSHOT` or `VIDEO`, decided at design time; lowercase it for this call. The plan is binding here as everywhere: never substitute a type.
  - `element` and `label` come from the group's TC assertion: `element` is the asserted element's `id=`/`desc=`/`text=`, `label` is what is being verified.
- **Tally the capture, never upload it**:
  1. Write the TC result line into `exec.md` in the main session. **The result write never leaves this session** — a background writer racing the line index is how a result lands on the wrong TC.
  2. Add one line to this wave's upload tally, held in context:
     `{TC id} · {captured path} · {dest}`
     `{dest}` is the Phase 1 string. A capture that must land under a per-TC section carries that TC's own case name — `doc:{docId}#{TC case name}`. One capture going to several places is one tally line per place.
  3. **On `❌ FAILED` or `🚫 BLOCKED`, write the verdict into the doc section**: the marker word alone
     (bold, red), then italic `Actual: {observed}` and `Expected: {per the requirement}`, one sentence each.
  4. **Advance to the next TC.** Do not run the upload CLI, do not poll the worker, and never invoke `docs-media` or a Drive MCP tool for a capture the tally already holds.
- **At wave close, hand the tally off and keep testing.** Dispatch the `evidence-uploader` agent **in the background** with `{KEY}`, `wave={label}`, and the tally verbatim. It queues, drains, verifies, heals, and writes `tasks/{KEY}/exec/.upload/ledger-{wave}.md` while the next wave runs.
  - **Never wait on it.** Start the next wave in the same message that dispatches it. Do not read its ledger mid-run — its report arrives on its own, and its `Failed` and `Still queued` lines are what Phase 3 carries into the report.
  - One uploader per wave, and none for a wave that produced no capture.
- No Agent tool in context → queue inline instead, one call per capture, and reconcile in Phase 3:
  ```bash
  .venv/bin/python3 scripts/evidence_upload.py add --key {KEY} --file {captured path} --dest '{the Phase 1 dest}'
  ```
  It returns in milliseconds — a job file, no network I/O. Repeat `--dest` for several destinations. The CLI is idempotent on `(file bytes, dest)`, so re-queuing a capture that already went is a no-op; `--force` overrides that, and is only ever for a capture that genuinely changed.

---

### Evidence Verification

Verification standards per capture type live in `capture-mechanics.md` § Verify. The auditor applies them; this session records verdicts from assertions.

---

## Failure Paths

| Event | Action / Resolution |
|---|---|
| **Platform Absent at Preflight** | Mark all platform results `🚫 BLOCKED`. Remaining platforms execute normally. |
| **Missing Preflight Data** | Mark dependent TCs `🚫 BLOCKED` on all platforms naming the data item. |
| **Account Login Failure** | Mark TCs requiring account `🚫 BLOCKED` on affected platform. |
| **Unresolvable Element Target** | Recover per driver rule. If unrecovered: update `Target Inventory`, mark `🚫 BLOCKED`. No guessed taps. |
| **Capture Failure** | Retry capture once. If still failing, log anomaly in result prose; do not alter test verdict. |
| **App Crash** | Set `❌ FAILED` with crash ID. Re-apply wave `Reset` before executing next TC. |
| **Wave State Unrecoverable** | Mark remaining TCs in wave `🚫 BLOCKED`. Proceed to next wave. |
| **Wave Precondition Created by Later Wave** | Execute dependent wave immediately after the wave creating required state, restore state, and log the move. Never reorder on a guess about data. |

---

## Phase 3 — Report

1. **Final Index Audit**: Ensure no TC remains `⏳ PENDING`. Convert unexecuted TCs to `🚫 BLOCKED` with cause.
2. **Flush Uploads**: collect the wave uploaders, drain the tail, then reconcile — a missing upload must never reach the report unnoticed.
   - **Wait for every wave uploader to report before running anything below.** Each uploader's `Failed` and `Still queued` lines then carry into the report verbatim.
   - **Then stop the worker before draining, never alongside it:**
     ```bash
     .venv/bin/python3 scripts/evidence_upload.py wait --key {KEY} --timeout 300   # let the live worker finish
     .venv/bin/python3 scripts/evidence_upload.py stop --key {KEY}                 # the run is over; the worker goes with it
     .venv/bin/python3 scripts/evidence_upload.py serve --key {KEY} --once         # drain the tail, then exit
     ```
     `wait` exiting `3` means the worker is already gone — go straight to `serve --once`.
   Then dispatch the `evidence-auditor` agent for `{KEY}` with the destination and the wave ledger paths
   (`tasks/{KEY}/exec/.upload/ledger-*.md`). Its `Missing` and `Anomalies` lines go into the report
   verbatim: never report evidence as captured when its upload did not land. Re-read no capture in this
   phase.

   No Agent tool in context → reconcile here:
   ```bash
   .venv/bin/python3 scripts/evidence_upload.py status --key {KEY} --json
   ```
   `status` exits `0` only when nothing is queued and nothing failed; `2` means work is outstanding, and it names every failure with its error. Failures → `retry --key {KEY}`, then `serve --key {KEY} --once`, then check again. Still failing after one retry → carry the file name and the error into the report.
3. **Generate Report**: Write `tasks/{KEY}/exec/report.md` from `REPORT.md`. Its Evidence column and any
   landed URLs come from the wave ledgers (`tasks/{KEY}/exec/.upload/ledger-*.md`), not re-derived from
   `exec.md`.
4. **Lessons Learned**: Append reusable execution lessons to `.kiro/docs/lessons.md`
5. Present the execution summary, platform differences, and the failed/blocked breakdown. Leave the bug candidates to Phase 4 — it presents them as the list the user picks from.

Done when: `report.md` is complete, no TCs are pending, and every failure sits either in `## Bugs Found` or in `## Failed & Blocked` with the reason it is not a defect.

---

## Phase 4 — Triage & File

Runs straight after Phase 3, and re-enterable alone with `finalise` when a session ends mid-triage. Edits
`report.md` and nothing else — it posts no Jira comment and changes no TC status.

1. **Present the candidates.** Every `## Bugs Found` row still carrying `—` in its Bug column, numbered, each
   with: TC id and title, platforms it reproduced on, what is wrong, repro count (`2/2` \| `1/2`), backend
   check result, and the evidence file. None left → say so and stop.

   **First, check for duplicates.** Dispatch one `dup-scout` agent per candidate, **all in one message** — the
   searches are independent. Each returns a verdict and candidate keys. Attach that verdict to the candidate
   when you present it, so the user chooses knowing whether the bug is already filed. A `duplicate of {KEY}`
   verdict is information for the user, not a decision: they may still file.

   No Agent tool in context → grep `tasks/*/exec/report.md` for the symptom and check the parent's existing
   SIT Bug sub-tasks, then present what you found the same way.
2. **Ask, per candidate: file or decline.** Use `AskUserQuestion`. A declined candidate needs a reason. Never
   file a bug the user did not pick, and never guess a key that was not returned to you.
3. **File each chosen candidate**: disclose_context("report-bug"), one per candidate, with the full payload —
   TC id and title, symptom, expected behavior, platforms it reproduced on, repro count, backend check
   result, and the existing evidence file path. The capture is already taken: `report-bug` must not
   re-capture or delete it. Take the key it returns.
4. **Write the key into the two cells that hold one** — the `## Bugs Found` row, and the same TC's row in
   `## Result by Test Case`. Both are in `report.md`. `exec.md` is not touched.
5. **Move every declined candidate** to `## Rejected Candidates` with its reason, and drop its `## Bugs Found`
   row.
6. **Present the final mapping**: each TC with the key it now carries, and each declined candidate with its
   reason.

`1/2` is intermittent, not a certain defect — say so when presenting it, and let the user decide.

Done when: every `## Bugs Found` row carries a bug key, every declined candidate sits under
`## Rejected Candidates` with its reason, and every filed key appears in both tables that carry one.


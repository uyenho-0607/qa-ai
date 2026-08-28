---
name: manual-exec-run
description: Execute exec.md, the manual SIT plan, on every target it names — Back Office web, the member mobile app, or both. Run by wave, capture evidence, write each result back in place. Use on "run manual tests", /exec-run.
---

## Contract

- **Args:** `{KEY}` [, `finalise`] — e.g. `AO-925`
- **Reads:** `tasks/{KEY}/exec.md`
- **Writes:** `tasks/{KEY}/exec.md` (result lines, in place), `tasks/{KEY}/report.md`, evidence to `evidence/{KEY}/` — the paths `.kiro/steering/project-config.md` § Folder Structure fixes
- **With `finalise`:** run Phase 4 alone — backfill filed bug keys into the existing `report.md`
- **Missing input:** STOP and name the producer. No `exec.md` → `/manual-exec-design {KEY}`; never build one here, and never run it from here. `finalise` with no `report.md` → STOP: Phases 1–3 have not run.

**Loads, at Phase 2 and not before:** `.kiro/docs/lessons.md`, `.kiro/steering/capture-mechanics.md`,
plus the row it gives each target kind the plan actually runs — a driver rule and a capture file — and no
other row. Phase 1 reads nothing but `exec.md`.

## Rules

- **The plan decides.** Never re-derive a target, surface, evidence mode, grouping, wave order, step, value or
  checkpoint that `exec.md` states. One exception: a wave whose precondition is a state a *later* wave creates
  may run just after that wave, restoring the state afterwards — that beats a `BLOCKED` the run could have
  cleared itself. Never reorder on a guess about data; log the move and the restore in the result line.
- A result is decided by its assertion, never by whether evidence was captured.
- One result per entry in a TC's `**Tgt:**` — one per pair on a `bo+app` TC.
- Resolve every target string from a fresh DOM query or element listing immediately before acting on it,
  in one call or many. Batch a multi-field screen into one script per `mobile-mcp-rule.md` § Element
  Resolution Rules.
- A coordinate is never a target string; where one is unavoidable, `mobile-mcp-rule.md` § Element Resolution
  Rules states the only case that allows it.
- Take every input value from `**Data:**`. Never invent one.
- A difference between two targets is a finding, not a variant to normalise. Record both observations.
- Capture evidence here; file bugs with `report-bug`. This skill never files one.
- Take every timestamp from `date '+%Y-%m-%d %H:%M'`. Never write one from memory.

## Phase 1 — Load, preflight, resume

1. **Header.** Everything above `## Test Cases`, read once. It is the run's working set — the targets, the
   evidence mode, Preflight, the wave order with each wave's groups, targets, reset and contexts, each
   group's TCs and stem, Target Inventory, Skipped, and AC Coverage.

   ```
   sed -n '1,/^## Test Cases/p' tasks/{KEY}/exec.md
   ```

2. **Index.** Every TC's start line, title and case ID, and every result line with its status:

   ```
   grep -n '^### TC-\|^\*\*R@' tasks/{KEY}/exec.md
   ```

   It stays valid for the whole run: recording a result replaces one line with one line, so no line moves.
   The result lines are authoritative. Never read § Results Summary to decide what to run — it is stale until
   Phase 3 rewrites it.

3. **Target preflight.** Per Preflight § Targets row — a device target: `mobile_list_available_devices`,
   confirm it is present. A web target: confirm the URL responds. Then compare the build: `unknown` in the
   plan → write the build you observe into the row and continue; a build that disagrees with a stated one →
   stop and ask, because results against the wrong build prove nothing.
4. **Data preflight.** Confirm every Preflight § Data item exists. The row names the TCs it blocks.
5. **Resume.** Read the index's result lines, each target independently:
   - `PASSED` → skip that target. Never re-run it, never overwrite its evidence.
   - `PENDING` → execute it.
   - `FAILED` / `BLOCKED` → ask whether to retry or keep. Keep → skip that target, its result stands. Retry →
     set the line back to `PENDING`, clear its notes, run that target again from the TC's first step, and
     overwrite that target's evidence.
   - A `bo+app` TC resumes per pair — a pair is one unit of work, never one per surface.
6. State the preflight results and the resume plan before executing: per target, how many TCs run, how many
   are skipped, how many are blocked and on what.

Done when: header and index are in hand, both preflights are resolved, every preflight block is written to
its result lines, the resume plan is stated per target — and no TC block has been read yet.

## Phase 2 — Execute by wave

At the first wave on a target kind, load `.kiro/steering/capture-mechanics.md` and its row for that kind.
Never load the other kind's files.

Waves run in the order the Waves table lists them. Open each wave with the reset its `Reset` column states —
a wave stating one clause per driver applies both — and open as many sessions as `Contexts` states.

- **A `bo` or `app` wave** runs on every target in its `Targets` column, **one target to completion before
  the next**.
- **A `bo+app` wave** runs once per **pair**, with both sessions open together for the whole pair. Never
  split a pair into two sequential passes: half a flow run twice is not the flow.

Then, for each target — or pair — in turn, taking only the targets Phase 1 left runnable, and per group in
the wave:

1. **Slice it.** `{start}` = the group's first TC line from the index; `{end}` = the next TC's line − 1, or
   `$` for the last group:

   ```
   sed -n '{start},{end}p' tasks/{KEY}/exec.md
   ```

   Read only the group about to run. Never widen the range "to have context", never execute a TC from a
   summarised or remembered block, and never read the file whole. A slice not beginning with `### TC-` means
   the index is stale: re-index and re-slice.

2. **Run each TC in it**, in plan order, by the five steps below. Skip a TC whose `**Tgt:**` excludes the
   target in hand.
3. **Capture the group's evidence** — see *After the group*, below.

### 1. Precondition

Navigate to the screen and account state `**Pre:**` names. No `**Pre:**` line means the TC continues from the
previous one: confirm that state is still current instead of re-navigating.

### 2. Steps

Follow `**Steps:**` exactly as written, taking any `**Steps@{targets}:**` override that names the target in
hand, and each element's target string from Target Inventory. On a `bo+app` TC every step carries an `@app` or `@bo` tag: execute it in the session that tag names,
switching between steps and leaving both open throughout. An untagged step on a paired TC is an incomplete
plan — stop and say so rather than guessing a surface.

Where every TC in the group is `**Mut:** no` and they share a screen, assert them in one pass. Every
`**Mut:** yes` TC runs as its own pass.

### 3. Assert

Assert every `**Exp:**` checkpoint against the observable it names, and record what was observed, keyed by
its checkpoint id. On a `bo+app` TC assert each checkpoint in the session its tag names, with the other still
open.

In `screenshot` mode the checkpoint's frame is captured **here**, at the assertion moment, under the stem its
Checkpoint Evidence row carries — then the frame is verified, per `.kiro/steering/capture-mechanics.md`. No
`.md` is written beside it. The result still comes from the observed fact, never from the frame.

On a failed assertion, before writing the result:

1. Re-run the assertion once. Record `2/2` where it failed both times, `1/2` where it passed on the retry.
   `1/2` is intermittent, not a certain defect.
2. Run the backend check the checkpoint names — endpoints and their bearer token live in
   `.kiro/locator-cache.json` § `api`. Record its status and compared values, or `not checked` where the
   checkpoint names none.
3. Device target: `mobile_list_crashes` — record any crash ID new to this run, and fetch it. Web target: read
   `browser_console_messages` and record the errors.
4. Capture the diagnostic log — device logs per `.kiro/steering/mobile-mcp-rule.md` § Diagnostic Rules,
   network entries per `browser_network_requests`. Record only the lines naming the app under test.

### 4. Record the result

Replace this TC's `**R@{target}:**` line for the target in hand — one line for one line:

```
**R@{target}:** {PASSED|FAILED|BLOCKED} · {YYYY-MM-DD HH:MM} · {BUG-ID} · {notes}
```

Omit `{BUG-ID}` while none is filed. Notes carry, as they apply: observed against expected, the repro count,
the backend check, the crash ID or console error, the blocker on a block, any target string that changed, and
any capture that could not be produced. Never write the evidence path — it derives from the stem.

A `bo+app` TC has **one** result line per pair. Name the surface the failure happened on in the notes; never
split one flow into a pass on one surface and a fail on the other.

Done when: the file on disk shows this TC's real status for this target, and its line count is unchanged.

### 5. Teardown

Execute `**Teardown:**` exactly as written, in the session each tagged step names. No `**Teardown:**` line =
none needed. Continue to the next TC whatever this TC's result.

### After the group — capture the evidence

`screenshot` mode captured its frames inline at step 3; nothing more happens here.

`normal` mode: once the whole group has been tested, replay it once per target into the capture its Evidence
Groups row states — its type, its stem, and `**Cap:**` for the moment each checkpoint must show. Write the
file per `.kiro/steering/capture-mechanics.md`, then verify it there. Write no `.md` beside it — the elapsed
second each checkpoint lands on goes in this TC's result note.

Done when: every file the plan names for this group and this target exists at its derived path and shows its
asserted state.

### Per wave

Collect the crash IDs, console errors and log lines every failure in the wave produced. They belong in report
Notes; a crash or an app-side error on a failing TC is FE evidence for `report-bug`.

## Failure paths

| What happened | The one outcome |
|---|---|
| A target is absent at preflight | every result line for that target → `BLOCKED`, naming it. Every other target still runs. |
| A Preflight § Data item is missing | every TC that row names → `BLOCKED` on all its targets, naming the item |
| An account cannot log in at the first TC needing it | every TC whose `**Pre:**` names it → `BLOCKED` on that target, naming the account |
| A target string will not resolve | recover per the driver rule — `playwright-rule.md` § Locator Recovery, `mobile-mcp-rule.md` § Element Resolution Rules. Recovered: update Target Inventory and restart the TC from step 1. Not recovered: `BLOCKED`, naming the element and its screen. Never a guessed tap. |
| An assertion fails | the failure protocol at step 3, then `FAILED`, then the next TC |
| A capture fails or cannot be verified | re-capture once; still failing → note it in the result. The result never changes. |
| The app crashes mid-TC | `FAILED` carrying the crash ID; re-apply the wave's `Reset` before the next TC |
| The wave's state cannot be recovered | the wave's remaining TCs on that target → `BLOCKED`, naming the cause. The next wave still runs. |
| A wave's precondition is a state a later wave creates | run it just after that wave and restore the state; log the move and the restore in the result line. Never reorder on a guess about data. |
| Context is lost or compacted mid-run | re-read the header, re-index, re-slice the current group. Never read the file whole, never resume from memory of a block. |
| `finalise` finds no `report.md` | STOP — Phases 1–3 have not run |

## Phase 3 — Report

1. Re-read the index. A line still `PENDING` never ran: run it, or write `BLOCKED` with the reason it did not.
   Then regenerate `exec.md` § Results Summary from the result lines — once, here, and nowhere else.
2. `ls evidence/{KEY}/` — confirm every file the plan names is there, and that nothing else is. Note any that
   is missing.
3. Write `tasks/{KEY}/report.md` from `REPORT.md`, filling every section it defines. Its content comes from
   three places already in hand: the exec header (Metadata, Preflight § Targets, AC Coverage, Skipped), the
   index (TC Results, and Executed At from the earliest and latest result timestamps), and the result notes
   (everything else). Re-slice a failing TC's block only for its `**Exp:**` text.
4. Judge every failure. Caused by the product → a Bugs Found row **and** a Failed & Blocked Details entry.
   Caused by the environment, the data, or the plan → the entry alone, carrying the reason it is not a defect.
5. Build Target Differences by comparing the per-target notes of every TC that ran on more than one target. A
   single-target run writes *None*.
6. A reusable lesson the run turned up — a locator that moved, a fixture that lies, an env quirk that cost a
   re-run → append one bullet to `.kiro/docs/lessons.md` with `{KEY}` and the date. A lesson a rule file
   already owns goes in that rule file instead, per that file's header. Nothing reusable → skip.
7. Present the Summary table, Bugs Found, Target Differences, and every failed or blocked TC.

Done when: `report.md` is complete, no result line is still `PENDING`, every AC carries a result, every
failure carries its repro count and backend check, and every failure sits either under Bugs Found or with the
reason it is not a defect.

## Phase 4 — Finalise (`finalise` arg only)

Runs after `report-bug` filed the confirmed defects. Edits `report.md` and `exec.md` only — posts nothing to
Jira.

1. Read `tasks/{KEY}/report.md`. List every Bugs Found row still carrying `—` in its Bug column. None left →
   say so and stop.
2. Take the `{TC-ID} → {BUG-KEY}` pairs from the invocation. List every row still unpaired and ask: filed
   under which key, or declined. Never guess a key.
3. Per pair, write the key everywhere that TC appears — its Bugs Found row, its TC Results row, its
   Failed & Blocked Details `**Bug:**`, and the failing target's result line in `exec.md`:

   ```
   grep -n '^### TC-\|^\*\*R@' tasks/{KEY}/exec.md
   ```

4. Move every declined candidate to `## Rejected Candidates` with its reason, and drop its Bugs Found row.
5. Recompute the Summary counts and pass rate from TC Results, per target.
6. Present the Summary table and every failed or blocked TC.

Done when: every Bugs Found row carries a bug key, every declined candidate sits under Rejected Candidates
with its reason, every failed target's result line carries the same key as its report row, and the Summary
counts match TC Results.

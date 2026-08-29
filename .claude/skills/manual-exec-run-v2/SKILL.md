---
name: manual-exec-run-v2
description: V2 VARIANT of manual-exec-run — invoke only when the user explicitly asks for v2. Executes exec-v2.md, the manual SIT plan, on every platform it names. Run by wave, capture evidence, write each result back in place. Use on "run manual tests v2", /exec-run-v2.
---

## Contract

- **Args:** `{KEY}` [, `finalise`] — e.g. `AO-925`
- **Reads:** `tasks/{KEY}/exec/exec-v2.md`, `.claude/steering/project-config.md`
- **Writes:** `tasks/{KEY}/exec/exec-v2.md` (result lines, in place), `tasks/{KEY}/exec/report-v2.md`, evidence to the
  path `project-config.md` § Folder Structure fixes
- **With `finalise`:** run Phase 4 alone — backfill filed bug keys into `report-v2.md` and `exec-v2.md`
- **Missing input:** STOP and name the producer. No `exec-v2.md` → `/manual-exec-design-v2 {KEY}`; never build
  one here, and never run it from here. `finalise` with no `report-v2.md` → STOP: Phases 1–3 have not run.

**Loads, at Phase 2 and not before:** `.claude/docs/lessons.md`, `.claude/steering/capture-mechanics.md`, and
for each platform the plan actually runs — its pack from `project-config.md` § Platforms, its driver rule, and
its capture file. No other pack, ever. Phase 1 reads nothing but `exec-v2.md` and the registry.

**This skill names no platform.** Every platform fact comes from the registry and the packs.

## Rules

- **The plan decides.** Never re-derive a platform, tier, evidence mode, grouping, wave order, step, value or
  expected result that `exec-v2.md` states. Its one exception is the wave-reordering row in § Failure paths.
- A result is decided by its assertion, never by whether evidence was captured.
- One result per platform in a TC's subtitle — one per pair for a cross-platform TC.
- A TC already carrying a result from recon is **not re-executed.** Its line reads `verified at recon`.
- Resolve every target string from a fresh query or element listing immediately before acting on it. Batch a
  multi-field screen into one call where the driver rule allows.
- A coordinate is never a target string; the driver rule states the only case that allows one.
- Take every input value from **Test data**. Never invent one.
- A difference between two platforms is a finding, not a variant to normalise. Record both observations.
- Capture evidence here; file bugs with `report-bug`. This skill never files one.
- Take every timestamp from `date '+%Y-%m-%d %H:%M'`. Never write one from memory.

## Phase 1 — Load, preflight, resume

1. **Registry.** Read `project-config.md` § Platforms — the label, id and pack for each platform the plan
   names. Labels are what `exec-v2.md` carries; ids are what file names carry.

2. **Header.** Everything above `## Test Cases`, read once. It is the run's working set.

   ```
   sed -n '1,/^## Test Cases/p' tasks/{KEY}/exec/exec-v2.md
   ```

3. **Index.** Every TC's start line, and every result line:

   ```
   grep -n '^### TC-\|^- .* · ' tasks/{KEY}/exec/exec-v2.md
   ```

   Rebuild it after each result is written — a result grows from one line to several, so line numbers shift.
   One grep is cheap; a stale index is not. The result lines are authoritative.

4. **Platform preflight.** Per Preflight § Platforms row, per its pack § Preflight. Then compare the build:
   `unknown` in the plan → write the build you observe into the row and continue; a build that disagrees with
   a stated one → **stop and ask**, because results against the wrong build prove nothing.

   A build disagreement also invalidates every `verified at recon` result: set those back to `⏳ PENDING` and
   execute them normally.

5. **Data preflight.** Confirm every Preflight § Data item exists. The row names the TCs it blocks.

6. **Resume.** Read the index's result lines, each platform independently:
   - `✅ PASSED` → skip. Never re-run, never overwrite its evidence.
   - `⏳ PENDING` → execute.
   - `❌ FAILED` / `🚫 BLOCKED` → ask whether to retry or keep. Keep → its result stands. Retry → set back to
     `⏳ PENDING`, clear its prose, run from the TC's first step, overwrite that platform's evidence.
   - A cross-platform TC resumes per pair — a pair is one unit of work.

7. State the preflight results and the resume plan before executing: per platform, how many TCs run, how many
   are already verified, how many are skipped, how many are blocked and on what.

Done when: header, registry and index are in hand, both preflights are resolved, every preflight block is
written to its result lines, the resume plan is stated — and no TC block has been read yet.

## Phase 2 — Execute by wave

At the first wave on a platform, load `capture-mechanics.md`, that platform's pack, its driver rule and its
capture file. Never load another platform's files.

Waves run in the order the Waves table lists them. Open each with the reset its `Reset` column states — a wave
stating one clause per group applies both — and open as many sessions as `Sessions` states.

- A **single-group wave** runs on every platform in its `Platforms` column, **one to completion before the
  next**.
- A **cross-platform wave** runs once per **pair**, both sessions open together for the whole pair. Never
  split a pair into two sequential passes: half a flow run twice is not the flow.

Then per platform — or pair — taking only what Phase 1 left runnable, and per group in the wave:

1. **Slice it.** `{start}` = the group's first TC line from the index; `{end}` = the next TC's line − 1, or
   `$` for the last:

   ```
   sed -n '{start},{end}p' tasks/{KEY}/exec/exec-v2.md
   ```

   Read only the group about to run. Never widen the range "to have context", never execute from a summarised
   or remembered block, and never read the file whole. A slice not beginning with `### TC-` means the index is
   stale: re-index and re-slice.

2. **Run each TC in it**, in plan order, by the five steps below. Skip a TC whose subtitle excludes the
   platform in hand, and any TC already carrying a recon result.
3. **Capture the group's evidence** — see *After the group*.

### 1. Precondition

Navigate to the screen and account state **Precondition** names. No **Precondition** field means the TC
continues from the previous one: confirm that state is still current instead of re-navigating.

### 2. Steps

Follow **Steps** exactly as written, taking any **Steps on {platform}** override that names the platform in
hand, and each element's target string from Target Inventory or the locator cache. On a cross-platform TC
every step is prefixed with a platform label: execute it in that session, switching between steps and leaving
both open throughout. An unprefixed step on a paired TC is an incomplete plan — stop and say so.

Where every TC in the group is read-only and they share a screen, assert them in one pass. Every TC that
changes data runs as its own pass.

### 3. Assert

Assert every entry in **Expected** against the observable it names — from the platform pack's § Observables,
never from a screenshot. Record what was observed, keyed by its number.

In `screenshot` mode the frame is captured **here**, at the assertion moment, under the stem its Evidence
§ Frames row carries, then verified per § Verifying a capture below. The result comes from the observed fact,
never from the frame.

On a failed assertion, before writing the result:

1. Re-run the assertion once. Record `2/2` where it failed both times, `1/2` where it passed on the retry.
   `1/2` is intermittent, not a certain defect.
2. Run the backend check **only where the expected result names an endpoint**. Record its status and compared
   values, or `not checked` otherwise.
3. Read the platform's crash or console signal — one call, per its pack § Observables. Record anything new to
   this run.
4. Capture the diagnostic log **only where the failure is heading for a bug report** — per the driver rule.
   Record only the lines naming the app under test.

### 4. Record the result

Rewrite this TC's result line for the platform in hand:

```
- {platform label} · {✅ PASSED|❌ FAILED|🚫 BLOCKED} · {YYYY-MM-DD HH:MM}
  {what was observed against what was expected}
  {repro count · backend check · crash or console signal}
  {any target string that changed, any capture that could not be produced, the blocker on a block}
```

Prose sits on indented lines beneath, **never crammed onto the status line**. Omit a line that has nothing to
say. Never write the evidence path — it derives from the stem. Re-index after writing.

On a cross-platform TC, name the side the failure happened on; never split one flow into a pass on one side
and a fail on the other.

Done when: the file on disk shows this TC's real status for this platform, and the index has been rebuilt.

### 5. Teardown

Execute **Teardown** exactly as written, in the session each prefixed step names. No **Teardown** field = none
needed. Continue to the next TC whatever this TC's result.

### After the group — capture the evidence

`screenshot` mode captured its frames inline at step 3; nothing more happens here.

`normal` mode: once the whole group has been tested, replay it once per platform into the capture its Evidence
§ Groups row states — its type, its stem, and the capture moments. Write the file per `capture-mechanics.md`,
then verify it there. Write no `.md` beside it — the elapsed second each expected result lands on goes in the
result prose.

### Verifying a capture

**A capture never decides a result.** Verification protects the evidence, not the verdict — so it is cheap by
default and thorough only where it matters.

| Capture | Verify |
|---|---|
| Recording | `ffprobe` duration and size, per `capture-mechanics.md` |
| Frame — assertion **passed**, screen seen before this wave | file exists, non-zero, dimensions match the platform's viewport. Flag any frame far below the median size for that platform — a blank capture compresses tiny |
| Frame — assertion **passed**, **first time this screen or state is seen in the run** | **read it back.** A new screen has no prior frame to compare against — visual confirmation is the only check |
| Frame — deferred Tier-1 TC verified mid-run | **read it back.** Apply the same screenshot-first standard as recon: the image is the primary verification, the DOM corroborates it |
| Frame — assertion **failed** | **read it back.** It is going into a bug report |
| Frame — size anomaly flagged | **read it back** |
| **First frame of each wave** | **read it back** — proves the capture pipeline for that platform and session |

For frames where "read it back" is required: look at the image, confirm the expected result is visually present
in the frame, then record the result. A DOM assertion that cannot be corroborated by what is visible in the
screenshot is not a pass — reclassify or re-execute.

For frames where a file check is sufficient: the design gate is what keeps this safe — a frame that could
never prove its assertion was flagged in Evidence § Frames `Video needed for` and got a video instead.

A capture failing verification is re-captured once. One that still fails is recorded in the result prose — it
never changes the result.

### Per wave

Collect the crash IDs, console errors and log lines every failure in the wave produced. They belong in report
Notes; a crash or an app-side error on a failing TC is FE evidence for `report-bug`.

## Failure paths

| What happened | The one outcome |
|---|---|
| A platform is absent at preflight | every result line for it → `🚫 BLOCKED`, naming it. Every other platform still runs. |
| A Preflight § Data item is missing | every TC that row names → `🚫 BLOCKED` on all its platforms, naming the item |
| An account cannot log in at the first TC needing it | every TC whose precondition names it → `🚫 BLOCKED` on that platform, naming the account |
| A target string will not resolve | recover per the platform's driver rule. Recovered: update Target Inventory, restart the TC from step 1. Not recovered: `🚫 BLOCKED`, naming the element and its screen. Never a guessed tap. |
| An assertion fails | the failure protocol at step 3, then `❌ FAILED`, then the next TC |
| A capture fails or cannot be verified | re-capture once; still failing → note it in the result prose |
| The app crashes mid-TC | `❌ FAILED` carrying the crash ID; re-apply the wave's `Reset` before the next TC |
| The wave's state cannot be recovered | the wave's remaining TCs on that platform → `🚫 BLOCKED`, naming the cause. The next wave still runs. |
| A wave's precondition is a state a later wave creates | run it just after that wave and restore the state; log the move and the restore in the result. Never reorder on a guess about data. |
| The build disagrees with the plan | stop and ask. Every `verified at recon` result is invalidated. |
| Context is lost or compacted mid-run | re-read the header, re-index, re-slice the current group |
| `finalise` finds no `report-v2.md` | STOP — Phases 1–3 have not run |

## Phase 3 — Report

1. Re-index. A line still `⏳ PENDING` never ran: run it, or write `🚫 BLOCKED` with the reason it did not.
2. Generate the results summary table into `report-v2.md` from the result lines — **here, once, and nowhere
   else.** `exec-v2.md` carries no such table.
3. `ls` the evidence folder — confirm every file the plan names is there, and that nothing else is. Note any
   that is missing.
4. Write `tasks/{KEY}/exec/report-v2.md` from `REPORT.md`. Its content comes from three places already in hand: the
   exec header, the index, and the result prose. Re-slice a failing TC's block only for its **Expected** text.
5. Judge every failure. Caused by the product → a Bugs Found row **and** a Failed & Blocked entry. Caused by
   the environment, the data, or the plan → the entry alone, carrying the reason it is not a defect.
6. Build Platform Differences by comparing the per-platform prose of every TC that ran on more than one. A
   single-platform run writes *None*.
7. Carry the design phase's Visual Findings into the report, plus anything the run's own frame reads turned up.
8. Present the summary, Bugs Found, Platform Differences, and every failed or blocked TC.

A reusable lesson the run turned up — a locator that moved, a fixture that lies, an env quirk that cost a
re-run → append one bullet to `.claude/docs/lessons.md` with `{KEY}` and the date. Skip where nothing is
reusable; this is optional and never blocks the report.

Done when: `report-v2.md` is complete, no result line is still `⏳ PENDING`, every AC carries a result, every
failure carries its repro count, and every failure sits either under Bugs Found or with the reason it is not a
defect.

## Phase 4 — Finalise (`finalise` arg only)

Runs after `report-bug` filed the confirmed defects. Edits `report-v2.md` and `exec-v2.md` only — posts nothing
to Jira. It changes no status, so no count is recomputed.

1. Read `report-v2.md`. List every Bugs Found row still carrying `—` in its Bug column. None left → say so and
   stop.
2. Take the `{TC id} → {BUG-KEY}` pairs from the invocation. List every row still unpaired and ask: filed
   under which key, or declined. Never guess a key.
3. Per pair, write the key in the two places that hold one — the Bugs Found row, and the failing platform's
   result line in `exec-v2.md`, which is what a later resume reads.
4. Move every declined candidate to `## Rejected Candidates` with its reason, and drop its Bugs Found row.
5. Present what changed: each TC with the key it now carries, and each declined candidate with its reason.

Done when: every Bugs Found row carries a bug key, every declined candidate sits under Rejected Candidates
with its reason, and every failed platform's result line carries the same key as its report row.

---
name: manual-exec-run
description: Execute exec.md, the manual SIT plan: run by wave, capture evidence, write each TC result back in place. Use on "run manual tests", /exec-run.
---

## Contract

- **Arg:** `{KEY}` — e.g. `OMS-1120`
- **Workspace:** `tasks/{KEY}/`
- **Reads:** `tasks/{KEY}/exec.md`
- **Writes:** `tasks/{KEY}/exec.md` (results, in place), `tasks/{KEY}/report.md`, evidence to `evidence/{KEY}/`
- **Missing input:** STOP — `exec.md` → invoke the `manual-exec-design` skill. Never build one here.

**Required reads:** `.claude/docs/lessons.md`, `.claude/steering/playwright-rule.md`

## Execution Rules

The exec file is the plan — header tables (Evidence Groups, Waves) as much as TC fields (`**Steps:**`, `**Exp:**`, `**Ev:**`, `**Cap:**`, `**Teardown:**`). Follow every field; never re-decide one.

**Test first, record second.** Decide the result from a real run; capture evidence afterwards, in a separate pass.

- Decide each result from its assertion, never from whether evidence was captured.
- Never think, explore, or resolve a locator inside a recording context.
- Capture evidence here; file bugs with `report-bug`.

## Phase 1 — Load and resume

1. Read the header only, never the whole file — everything above `## Test Cases`:

   ```
   sed -n '1,/^## Test Cases/p' tasks/{KEY}/exec.md
   ```

2. Extract: wave order, each wave's groups, each group's TC list, evidence type and file.
3. Record the run start timestamp.
4. Confirm the environment is reachable and every account named in Execution Context can log in.
5. **Resume check.** Read the Status column of Results Summary:
   - `PASSED` → skip; never re-run, never overwrite its evidence.
   - `PENDING` → execute.
   - `FAILED` / `BLOCKED` → ask whether to retry or keep. To retry: reset to `PENDING`, clear Notes, run all six steps again, overwrite the evidence.

   Report the resume plan before executing: how many TCs run, how many are skipped.

Done when: header loaded, environment live, resume plan stated — and no TC block read yet.

## Phase 2 — Execute by wave

Process waves in order; open as many sessions as each wave's `Contexts` column states.

Load a group's TC blocks immediately before running it, and nothing else.

1. Index the file. **Re-run per group** — step 4 rewrites `**R:**` lines and shifts every line below:

   ```
   grep -n '^### TC-' tasks/{KEY}/exec.md
   ```

2. Slice it. `{start}` = the group's first TC line; `{end}` = the next TC's line − 1, or `$` for the last group:

   ```
   sed -n '{start},{end}p' tasks/{KEY}/exec.md
   ```

Rules:

- Read only the group about to run. Never widen the range "to have context".
- Lost or compacted mid-run: recover by re-reading the header and re-slicing the current group — never by reading the file in full.
- Never execute a TC from a summarised or remembered block; re-slice instead.

Run these six steps for every TC in the loaded group, in order.

### 1. Set up the precondition

Navigate to the page and account state `**Pre:**` names. No `**Pre:**` line = continues from the previous TC — verify that state is still active instead of re-navigating.

### 2. Run the steps

Follow the steps exactly as written.

On locator failure: apply the Locator Recovery Protocol in `.claude/steering/playwright-rule.md`, update the Locators Reference table in the exec file, then continue from where the TC stopped.

### 3. Assert

Assert every condition under `**Exp:**` against DOM facts — testid presence, attribute value, text content, API response status. Record what was observed for each.

### 4. Record the result

Replace this TC's `**R:**` line and update its row in Results Summary. One line, `·`-separated:

```
**R:** {PASSED|FAILED|BLOCKED|SKIPPED} · {YYYY-MM-DD HH:MM} · {BUG-ID} · {notes}
```

Omit BUG-ID while none is filed. Notes carry observed vs expected on a failure, the blocker on a block, and any locator change. Never write the evidence path — it is the group's file. Continue to the next TC in every case.

Done when: the exec file on disk shows this TC's real status, not `PENDING`.

### 5. Capture the evidence

Capture per `**Ev:**`, following `references/capture-mechanics.md`. `**Ev:**` names only the group — take type and file from the Evidence Groups table, the path from `**Evidence path:**` in Execution Context. `**Cap:**`, where present, states what the frame or moment must show.

Done when: the file exists at the resolved group path. Record a capture failure in the TC's `**R:**` notes.

### 6. Tear down

Execute `**Teardown:**` exactly as written. No `**Teardown:**` line = none needed; proceed without closing or resetting.

Done when: the state matches what the next TC's precondition expects.

## Phase 3 — Report

1. Confirm every Results Summary row matches its TC's `**R:**` line. Read the result lines alone, not the TC blocks:

   ```
   grep -n '^### TC-\|^\*\*R:\*\*' tasks/{KEY}/exec.md
   ```

   Re-run any TC still `PENDING`, or mark it `BLOCKED` with the reason it never ran. Re-slice a block only for notes not already in hand.
2. Confirm every evidence file exists at its stated path, and that its name lists exactly its group's TC-IDs.
   Note any missing file. A name whose IDs disagree with the Evidence Groups table is a wrong-file capture —
   re-capture it, never rename it.
3. Record the run end timestamp.
4. List every failure that looks like a product defect under Bugs Found — TC, expected, observed, evidence path. Re-slice each failing TC's block for its `**Exp:**` and `**R:**` notes. Never file a bug from this skill.
5. Write `tasks/{KEY}/report.md` from `REPORT.md`, filling every section it defines.
6. Present the Summary table, Bugs Found, and every Failed and Blocked TC.

Done when: `report.md` is complete, no Results Summary row is still `PENDING`, and every failure appears either under Bugs Found or with a reason it is not a defect.

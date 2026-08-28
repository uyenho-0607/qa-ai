# Manual SIT Execution Workflow

Six steps from a Jira ticket to a signed-off SIT run, on any surface — Back Office web, the member mobile app,
or one flow spanning both. Every step is an independent skill chained by a file, never by a skill calling
another. Each artifact lands in `tasks/{KEY}/`; the next step reads it from there. Actions and rules live in the
skills — this file owns the prompts, the gates, and the order.

```
[Jira Ticket] → 1 Load → 2 Design → 3 Execute → 4 File Defects → 5 Finalise → 6 Testmo
                            ↓ GATE                  ↓ GATE
```

| Step | Skill | Writes |
|------|-------|--------|
| 1 | `jira-retriever` + (`collect-testmo-cases` \| `collect-gsheet-cases`) | `jira.md`, `tc.md` |
| 2 | `manual-exec-design` | `exec.md`, `recon/` |
| 3 | `manual-exec-run` | `exec.md` results, `evidence/{KEY}/`, `report.md` |
| 4 | `report-bug` | Jira SIT Bug subtasks under `{KEY}` |
| 5 | `manual-exec-run finalise` | `report.md` complete, bug keys backfilled |
| 6 | Testmo MCP, driven by prompt | a Testmo run with one result per executed TC |

Paths follow `.claude/steering/project-config.md` § Folder Structure: chain files (`jira.md`, `tc.md`,
`exec.md`, `recon/`, `report.md`) live in `tasks/{KEY}/`; evidence lands in `evidence/{KEY}/`. Both are tracked,
not ignored — stage per-ticket files with `git-workflow`, never a broad `git add`.

## Surfaces and targets

A TC's **surface** is what it exercises. A run's **targets** are where it executes. Step 2 Phase 1 asks for the
targets; every later step reads them from `exec.md`.

| Surface | Targets it can reach |
|---|---|
| `bo` — Back Office | `bo` (desktop), `bo-mv` (390×844) |
| `app` — member app, React Native + Expo | `ios`, `android`, `app-web` (Expo web build) |
| `bo+app` — one flow crossing both | one app target paired with one BO target |

A TC runs on `selected targets ∩ the targets its surface can reach`. A mixed TC set needs no special handling:
each TC carries its own surface, and a Results Summary cell reads `N/A` where the surface cannot reach that
target. The same TC set across `ios`, `android` and `app-web` is the same mechanism with three targets selected.

**`bo+app` is opt-in, per TC.** Only a TC whose flow genuinely spans both surfaces carries pairs, `@app` / `@bo`
step tags and one result per pair. A BO-only set, an app-only set, and one app set run across several platforms
all stay plain: no tags, no pairs, one result per target. Step 2 flags every paired TC at its gate, with the two
sessions each needs.

## 📥 STEP 1: Load Context

Both skills are independent — one writes `jira.md`, the other `tc.md`. Run them concurrently.

```
Load context for manual SIT execution of {KEY}. Run both in parallel:

1. jira-retriever with `{KEY}` and the `save` arg.
2. collect-testmo-cases with `{KEY}` and the `save` arg. If it finds no linked cases,
   stop and ask me for the TC sheet URL, then use collect-gsheet-cases with `{KEY}` and that URL.

Report: summary, every numbered acceptance criterion, affected module, build/fixVersion,
which source produced the cases, TC count, and each TC's ID and title.
```

`save` is required on both — without it no file is written and Step 2 has nothing to read. The workflow cannot
infer the TC source: name Testmo or give the sheet URL.

**Output:** `jira.md` — summary, numbered ACs, affected module, build or `unknown`. `tc.md` — TC count with
each case ID, title, steps and expected result.

## 🧭 STEP 2: Design the Execution Plan — GATE

```
/manual-exec-design {KEY}

Complete every phase in order. Ask me for targets in Phase 1, before any recon; ask for the evidence mode
in Phase 7, with the counts that make the choice concrete.
Report before I approve: targets and evidence mode, the classification with each TC's surface and targets,
reconciliation count, every uncovered AC and the Added Coverage TC written for it, expected-result gaps
found and how each was closed, every unaddressable element with the fix its surface needs, every element or
behaviour present on one target and absent on another, every TC-sheet-vs-live discrepancy, unconfirmed
Preflight items, and — in `screenshot` mode — every checkpoint a frame cannot prove.
```

Pass `targets=` and `evidence=` in the invocation to skip the questions in Phases 1 and 7:
`/manual-exec-design AO-925 targets=ios,android evidence=screenshot`

**Output:** `exec.md` + `recon/`. Reconciles twice — `tc.md count == agent-executable + skipped`, and every AC
appears in AC Coverage.

**Approve the plan before Step 3.** Execution never re-decides anything the plan states.

The unaddressable-element list is a dev dependency, not a plan defect: an element with no `id=`, no `desc=` and
no unique `text=` cannot be targeted. The app's `testID` coverage is sparse — raise the list with the app or FE
team at this gate.

## 🧪 STEP 3: Execute

```
/manual-exec-run {KEY}

Follow exec.md exactly — never re-decide targets, evidence type, steps, or grouping.
Run every TC on every target its **Tgt:** line names, and record a result per target.
State the resume plan per target, and the Preflight results, before executing.
```

**Output:** `exec.md` with no result cell left `PENDING`; `evidence/{KEY}/` — one verified file per group or
checkpoint per target, and no `.md` beside any of them; `report.md` with a Summary row per
target, Target Differences, AC Coverage, Bugs Found, and a Failed & Blocked Details entry per failure carrying
its repro count, backend check, crash or console error, and log lines.

## 🐞 STEP 4: File Defects — GATE

Batch gate first — one prompt for the whole list:

```
Show me the Bugs Found table from tasks/{KEY}/report.md, verbatim,
with each row's Targets, Repro, Backend, Crash and Log lines from Failed & Blocked Details.
File nothing yet. I confirm the list.
```

Then, once confirmed:

```
File every confirmed defect as a SIT Bug under {KEY} using the report-bug skill.
The evidence and the FE/BE signals already exist in tasks/{KEY}/report.md — capture nothing new,
reproduce nothing. For each bug, carry from its Failed & Blocked Details entry: the targets it
reproduced on, the device identifier or URL and build per target, the repro count, the backend check,
and the evidence file path.
Present the batch as one table for one approval.
```

File nothing before the user confirms it. A defect reproducing on one target only is one bug naming that
target, not two bugs.

**Output:** one Jira SIT Bug per confirmed defect, with inline evidence; every declined candidate under
Rejected Candidates with its reason.

## 📊 STEP 5: Finalise the Report

```
/manual-exec-run {KEY} finalise

Backfill the filed {BUG-KEY}s into tasks/{KEY}/report.md and tasks/{KEY}/exec.md.
Present the Summary table and every Failed and Blocked TC.
```

Finalise posts nothing to Jira.

**Output:** `report.md` complete with every bug key resolved, a Summary row per target, and pass rate; every
declined candidate under Rejected Candidates.

## 🧾 STEP 6: Write Results Back to Testmo — optional

No skill covers this yet — `to-testmo` exports *cases*, not results. Drive the Testmo MCP directly:

```
Create a SIT run in Testmo from tasks/{KEY}/report.md, then submit one result per executed TC.
Use testmo_create_run, then testmo_batch_create_run_results.
Project, config and field ids: .claude/steering/testmo.md.
Where a TC's targets disagree, submit the worse status and name every target in the notes.
Ask me before creating a Testmo case for any Added Coverage TC — it has no case ID.
Report the run URL and the per-status counts before and after submission.
```

Skip where the TCs came from a Google Sheet — no Testmo cases to write back to.

**Output:** a Testmo run holding one result per executed TC, each carrying its status, notes, and any filed
bug key.

## When to Use Each Step

| Scenario | Steps |
|----------|-------|
| New feature, full manual SIT | 1 → 2 → 3 → 4 → 5 → 6 |
| Re-test after a fix, or `exec.md` already approved | 3 → 4 → 5 → 6 |
| Re-test after the filed bugs are fixed | `verify-bug` → 3 → 4 → 5 |
| TCs already collected | 2 → 3 → 4 → 5 → 6 |
| Design only, execute later | 1 → 2 |
| Run passed, nothing to file | 1 → 2 → 3 → 6 |
| One target only — the device or environment is unavailable | 2 → 3, then re-run 3 when it returns |
| Results already in `report.md`, Testmo not updated | 6 |
| Bug verification only | `verify-bug` skill instead |

## Resumption

Artifacts decide the entry point, not memory of a previous session: list `tasks/{KEY}/` and start at the first
step whose output is missing. Each skill asks overwrite / reuse / abort where its output exists. Never
overwrite an `exec.md` holding execution results. A target whose cell reads `PASSED` never re-runs.

## Known limits

Carried from the 2026-08-24 mobile build log, still open:

- **A wrong request is undetectable on `ios` / `android`.** The `mobile` server observes no network traffic, so
  an app sending a bad parameter or a stale token while the backend answers correctly passes. See
  `.claude/steering/mobile-mcp-rule.md` § Backend Verification Rules for why interception was rejected.
- **Device targets run sequentially, not in parallel.** One device to completion before the next — roughly
  doubles wall-clock against a web-only run.
- **Recording timestamps are hand-recorded.** The agent notes the elapsed second each checkpoint lands on
  during replay and writes it into the TC's result note; nothing verifies a range against the video. A wrong
  range is a silently wrong note.

## Prerequisites

- Jira access (Atlassian MCP)
- Web targets: browser (Playwright MCP), SIT reachable, VPN up for `BO_URL`
- Device targets: `mobile` MCP (`npx -y @mobilenext/mobile-mcp@latest`), and a booted device with the app
  installed at the build under test. **Android only today** — no iOS build exists yet
  (`.claude/locator-cache.json` § `bfg-otc-app._verifiedOn`), so an `ios` target blocks at Preflight
- Xcode command line tools (`xcrun simctl`) and Android SDK platform-tools (`adb`) for device state resets
- `ffmpeg` for web recordings, `ffprobe` on PATH to verify device recordings
- Testmo access (Testmo MCP) with `TESTMO_EMAIL` / `TESTMO_PASSWORD`, or `GOOGLE_CLIENT_ID` /
  `GOOGLE_CLIENT_SECRET` / `GOOGLE_REFRESH_TOKEN` in `.env` at the repo root for a TC sheet
- Every account named in `exec.md` able to log in on every selected target
- Every Preflight item in `exec.md` satisfied before Step 3

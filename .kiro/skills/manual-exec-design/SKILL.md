---
name: manual-exec-design
description: Build exec.md, the manual SIT execution plan, from jira.md and tc.md — targets, triage, recon, expected results, evidence, waves. Use on "design exec plan", or when manual-exec-run finds no exec.md.
---

## Contract

- **Args:** `{KEY}` [, `targets={list}`] [, `evidence={normal|screenshot}`] — e.g. `AO-925 targets=ios,android`
- **Reads:** `tasks/{KEY}/base/jira.md`, `tasks/{KEY}/base/tc.md`
- **Writes:** `tasks/{KEY}/exec/exec.md`, recon screenshots to `tasks/{KEY}/exec/recon/`, verified locators to `.kiro/locator-cache.json`
- **Missing input:** STOP and name the producer — `jira.md` ← `/fetch-jira {KEY}` with `save`; `tc.md` ← `/collect-testmo {KEY}` with `save`, or `/collect-gsheet`. Never fall back to Jira MCP or to chat context, and never run the producer from here.
- **`exec.md` exists:** ask — overwrite (rebuild from Phase 1), reuse (keep the file, run no phases), or abort. Never clobber a file holding execution results.

**Hard rule:** run every phase in order. Never skip one.

## Surfaces and targets

A TC's **surface** is what it exercises. A run's **targets** are where it executes.

| Surface | What it exercises | Targets it can reach | Pack |
|---|---|---|---|
| `bo` | OTC Back Office at `BO_URL` — maker / checker / admin | `bo` (desktop), `bo-mv` (390×844) | `references/surface-bo.md` |
| `app` | Member app — one React Native + Expo codebase | `ios`, `android`, `app-web` (Expo web build) | `references/surface-app.md` |
| `bo+app` | One flow crossing both — member acts in the app, checker acts in BO | one `app` target paired with one `bo` target | both |

**Resolution rule:** a TC runs on `selected targets ∩ the targets its surface can reach`. A TC whose surface
reaches none of the selected targets is Skipped, naming the target it needed.

## Phase 1 — Targets

Ask with `AskUserQuestion` — multi-select from the five targets above — unless `targets=` already answers it.

Done when: the target list is fixed and written down.

## Phase 2 — Read the inputs

- `tasks/{KEY}/base/jira.md` — the affected module, and every specified behaviour including implicit constraints.
  Number every acceptance criterion `AC-1`, `AC-2`, … .
- `tasks/{KEY}/base/tc.md` — every TC with its case ID, title, steps and expected result.

Done when: the module is recorded, every AC carries a number, and every TC is listed with the case ID
`tc.md` gave it.

## Phase 3 — Cover the ACs

Map every AC to the TCs that verify it.

- Covered → list them.
- Uncovered → author a TC for it now, to the same standard as a sheet TC: exact account, deterministic steps, explicit values, assertions tied to observed facts. It carries no case ID. Record it under Added Coverage.
- Outside this ticket's scope → mark it out of scope and name the owning ticket.

Authoring here, ahead of recon, is what puts an added TC's screens inside the recon scope.

Done when: no AC is blank — each carries covering TCs, an Added Coverage TC, or an out-of-scope owner.

## Phase 4 — Classify

Apply `.kiro/steering/manual-exec-triage.md` to every TC, sheet and added alike. A TC that is
human-executable, or that needs biometrics, a push notification, a camera, or a physical device, goes to
Skipped with its reason.

Per included TC:

- `**Surf:**` — `bo`, `app`, or `bo+app`. **Paired mechanics are opt-in:** pairs, `@app` / `@bo` tags and one
  result per pair belong to a `bo+app` TC and to nothing else, however many targets a plain TC runs on.
- `**Tgt:**` — the resolution rule's result; a `bo+app` TC carries pairs instead, per `TEMPLATE.md`
  § `bo+app` only. Where the Phase 1 selection cannot form a pair, return to Phase 1 and ask — never drop the
  TC quietly.

Done when: every TC is classified with no ambiguity left, and every included TC carries a surface and at least one target or pair.

## Phase 5 — Recon

Load the surface pack for every surface now in play, and only those. Every phase from here on reads them.

Then follow `references/recon.md`, on every selected target.

Resolve each target's identity for Preflight in the same pass — device identifiers from
`mobile_list_available_devices`, `BO_URL` for `bo` / `bo-mv`, plus the per-surface rows each pack lists under
§ Preflight. Record each target's build from the Jira fixVersion, the app's About screen, or the BO footer;
where none of the three gives one, write `unknown`.

Then apply what recon found:

- An element unaddressable on every target the TC applies to → Skipped, naming the element and the fix its pack states.
- Unaddressable on some → keep the TC, drop those targets from `**Tgt:**`, record why.

Done when: the reference's Done-when list is satisfied, every selected target carries an identifier and a build, and every unaddressable element has produced a skip or a dropped target.

## Phase 6 — Strengthen the expected results

Follow `references/expected-results.md` for every included TC.

Record every divergence between targets for the gate — an assertion holding on one and not another is a
finding to raise, never a per-target variant to write.

Above 20 TCs, work in batches of ten and reconcile each batch against the TC list before starting the next.

Done when: every TC states each depth level it needs as its own checkpoint, every checkpoint is tied to an observable its surface can produce, and no TC carries a one-bullet expected result unless it verifies a single static state.

## Phase 7 — Plan the evidence

Ask the mode with `AskUserQuestion`, unless `evidence=` already answers it. The whole TC list is in view by now, so quantify the choice: how many TCs `normal` would give a video, and how many checkpoints `screenshot` could not prove. `normal` is the default.

Then follow `references/evidence.md` for the mode chosen.

Done when: the mode is recorded, every TC has its evidence planned for every entry in its `**Tgt:**`, and every stem follows `references/evidence.md` § Stem.

## Phase 8 — Order the waves

Mark every TC's `**Mut:**` flag.

Order the groups and solo TCs to minimise state transitions:

- Place a dependent TC immediately after its prerequisite, with nothing between them.
- Keep TCs that mutate the same data in separate waves.
- One surface per wave, except a wave of `bo+app` TCs.
- At most one VIDEO group per wave.
- `Targets` — the targets its TCs share; the pairs, for a `bo+app` wave.
- `Reset` — the lightest reset in the wave's pack § State reset that reaches its first precondition, written
  as the action itself. The first wave on a target resets fully. A wave whose targets span both drivers, and
  every `bo+app` wave, states one clause per driver: `app: relaunch app · bo: fresh context`.
- `Contexts` — 1, except a wave whose TCs need two sessions at once; every `bo+app` wave is at least 2.

Done when: every TC carries a `**Mut:**` mark, every group and solo TC sits in a wave, and every wave carries `Targets`, `Reset` and `Contexts`.

## Phase 9 — Write `exec.md`

Write `tasks/{KEY}/exec/exec.md` from `TEMPLATE.md`. It is the single authority on every section and every field the file carries; fill each one from the phase that built it:

| Section | Built by |
|---|---|
| Execution Context | Phases 1, 2, 5, 7 |
| Preflight | Phase 5 |
| AC Coverage · Added Coverage | Phase 3 |
| Evidence Groups \| Checkpoint Evidence | Phase 7 |
| Waves | Phase 8 |
| Results Summary · Skipped | Phases 4, 5 |
| Target Inventory · Unaddressable Elements | Phase 5 |
| Test Cases | Phases 4, 6, 7, 8 |

The file states *what* to execute. `manual-exec-run` owns *how* — capture mechanics, step ordering, result
recording, failure handling.

Done when: every section `TEMPLATE.md` defines is present, or omitted on the condition its own note states; and every precondition matches the environment's actual state after recon.

## Phase 10 — Reconcile, then GATE

Reconcile against the written file:

- `tc.md` count == included + skipped, and every TC carries the case ID `tc.md` gave it.
- Every Phase 2 AC appears in AC Coverage.
- Every included TC carries one `**R@…:**` line per entry in its `**Tgt:**`, and no more.
- Every included TC has a Results Summary row whose every non-`N/A` cell reads `PENDING`.
- Every Preflight § Data row names the TCs that need it.
- Every Target Inventory row carries a resolved target string and an occurrences count. A row that cannot —
  the element is unreachable until Preflight § Data is satisfied — names its blocker and the wave that
  re-scans it. An element with no `id`, no `desc` and no unique `text` belongs in Unaddressable Elements.
  Never a placeholder carrying neither.

Resolve every mismatch before presenting.

Then present, and stop until the user approves:

- Reconciliation result
- Targets and evidence mode
- The classification — each TC's surface and targets
- Every uncovered AC, and the Added Coverage TC written for it
- Expected-result gaps found, and how each was closed
- Every unaddressable element, the TCs it blocks, and the fix its pack names
- Every element or behaviour present on one target and absent on another
- Every TC-sheet-vs-live discrepancy
- Preflight items that could not be confirmed
- Every `bo+app` TC, its pairs, and the two sessions each needs
- `screenshot` mode — every checkpoint a frame cannot prove
- Every question still unanswered

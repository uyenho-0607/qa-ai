---
name: manual-exec-design-v2
description: V2 VARIANT of manual-exec-design — invoke only when the user explicitly asks for v2. Builds exec-v2.md, the manual SIT execution plan, from jira.md and tc.md — coverage, triage, recon, expected results, evidence, waves. Use on "design exec plan v2", /manual-exec-design-v2, or when manual-exec-run-v2 finds no exec-v2.md.
---

## Contract

- **Args:** `{KEY}` [, `platforms={ids}`] [, `evidence={normal|screenshot}`] — ids from `project-config.md` § Platforms
- **Reads:** `.kiro/steering/project-config.md`, `tasks/{KEY}/base/jira.md`, `tasks/{KEY}/base/tc.md`
- **Writes:** `tasks/{KEY}/exec/exec-v2.md`, recon screenshots to `tasks/{KEY}/exec/recon/`, Tier-1 evidence to
  `tasks/{KEY}/exec/evidence/`, verified locators to `.kiro/locator-cache.json`
- **Missing input:** STOP and name its producer from `project-config.md` § Producers. Never run the producer
  from here, and never fall back to an MCP call or to chat context.
- **`exec-v2.md` exists:** ask — overwrite (rebuild from Phase 0), reuse (keep the file, run no phases), or
  abort. Never clobber a file holding execution results.

**Hard rule:** run every phase in order. Never skip one.

**This skill names no platform.** Every platform fact comes from `project-config.md` § Platforms and the packs
it points at. A sentence here that names a specific platform is a bug.

## Phase 0 — Read the registry

Read `project-config.md` § Platforms. Record every enabled row — id, label, group, pack — and how many
distinct groups are enabled.

**Cross-platform flows are available only where two or more groups are enabled.** Where one group is enabled,
every rule below marked *cross-platform* does not apply: skip it, and write nothing about pairing anywhere.

Load no pack yet.

Done when: the enabled platforms are listed with their groups, and cross-platform availability is decided.

## Phase 1 — Read the inputs

- `tasks/{KEY}/base/jira.md` — the affected module, and every specified behaviour including implicit constraints.
  Number every acceptance criterion `AC-1`, `AC-2`, … .
- `tasks/{KEY}/base/tc.md` — every TC with its case ID, title, steps and expected result.

Done when: the module is recorded, every AC carries a number, and every TC is listed with the case ID `tc.md`
gave it.

## Phase 2 — Cover the ACs

Map every AC to the TCs that verify it.

- Covered → list them.
- Uncovered → author a TC for it now, to the same standard as a sheet TC: exact account, deterministic steps,
  explicit values, assertions tied to observed facts. It carries no case ID. Record it under Added Coverage.
- Outside this ticket's scope → mark it out of scope and name the owning ticket.

Authoring here, ahead of recon, is what puts an added TC's screens inside the recon scope.

Done when: no AC is blank — each carries covering TCs, an Added Coverage TC, or an out-of-scope owner.

## Phase 3 — Classify

Apply `.kiro/steering/tc-exec-classify.md` to every TC, sheet and added alike. A TC that is
human-executable, or that needs biometrics, a push notification, a camera, or hardware the drivers cannot
reach, goes to Skipped with its reason.

Per included TC, decide two things.

**Platforms.** Derive them — do not ask. A TC's platforms are the enabled rows whose pack can exercise what
the TC tests, taken from `tc.md` and `jira.md`. `platforms=` overrides the derivation entirely. State the
derived list and the reason each enabled platform was excluded, in one line, before continuing — recon is
expensive and runs against this decision.

A TC whose every candidate platform is disabled goes to Skipped, naming the platform it needed and the reason
the registry gives.

*Cross-platform:* a TC whose flow must cross two groups in one execution carries a **pair** instead of a
platform list — one execution, one result. Pairs come from § Platforms. Where the enabled set cannot form the
pair a TC needs, the TC goes to Skipped naming the missing side.

**Tier.** What the TC verifies, which decides when it is verified:

| Tier | What it checks | Verified |
|---|---|---|
| **1** | a static UI fact — presence, absence, labels, columns, empty state, ordering of a settled screen | at Phase 4, if the screen is reachable then |
| **2** | behaviour — an action, a transition, validation, a state change | in the run |
| **3** | ripple — a change reaching another screen, session, role, or platform | in the run |

Tier 1 requires all of: the TC changes no saved data, every expected result is a settled screen state, and
nothing transient, ordered-in-time, or negative is asserted. Anything else is Tier 2.

Done when: every TC is classified with no ambiguity left, and every included TC carries a tier plus at least
one platform or pair.

## Phase 4 — Recon, and verify Tier 1

Load the pack for every enabled platform now in play, and only those. Every phase from here reads them.

Then follow `references/recon.md` on every platform in play. It confirms the plan is executable, verifies
every reachable Tier-1 TC on the spot, and sweeps each screen for visual defects.

Resolve each platform's identity for Preflight in the same pass — the identifiers and values its pack lists
under § Preflight. Record each platform's build from the Jira fixVersion, the app's About screen, or the
product's own footer; where none gives one, write `unknown`.

Then apply what recon found:

- An element unaddressable on every platform a TC applies to → Skipped, naming the element and the fix its
  pack states.
- Unaddressable on some → keep the TC, drop those platforms, record why.
- A Tier-1 TC whose screen was unreachable → keep it, mark it deferred with the reason, and plan it into a
  wave like any Tier-2 TC.

Done when: the reference's Done-when list is satisfied, every platform in play carries an identifier and a
build, every reachable Tier-1 TC carries a result, and every unaddressable element has produced a skip or a
dropped platform.

## Phase 5 — Strengthen the expected results

Follow `references/expected-results.md`, for every included **Tier 2 and Tier 3** TC. A Tier-1 TC verified at
Phase 4 is finished; one deferred there is strengthened here like any other.

Record every divergence between platforms for the gate — an assertion holding on one and not another is a
finding to raise, never a per-platform variant to write.

Above 20 TCs, work in batches of ten and reconcile each batch against the TC list before starting the next.

Done when: every Tier 2/3 TC states each depth level it needs as its own numbered expected result, every one
is tied to an observable its pack lists, and no TC carries a single expected result unless it verifies a
single static state.

## Phase 6 — Plan the evidence

Ask the mode with `AskUserQuestion`, unless `evidence=` already answers it. The TC list and recon are both in hand by now, so quantify the choice: how many TCs `normal` would give a video, how many frames `screenshot` would produce, and how many expected results a frame cannot prove. `normal` is the default.

Then follow `references/evidence.md` for the mode chosen. Tier-1 TCs already verified carry the evidence Phase 4 captured; plan nothing further for them.

Done when: the mode is recorded, every TC awaiting execution has its evidence planned for every platform it runs on, and every stem follows `references/evidence.md` § Stem.

## Phase 7 — Order the waves

Waves carry only the TCs still to execute — Tier 2, Tier 3, and any deferred Tier 1.

Mark every such TC as changing saved data, or not. Then order to minimise state transitions:

- Place a dependent TC immediately after its prerequisite, with nothing between them.
- Keep TCs that change the same data in separate waves.
- One platform group per wave, except a cross-platform wave.
- At most one VIDEO group per wave.
- `Platforms` — what its TCs share; the pairs, for a cross-platform wave.
- `Reset` — the lightest reset in the pack § State reset that reaches the wave's first precondition, written
  as the action itself. The first wave on a platform resets fully. A wave spanning two groups states one
  clause per group.
- `Sessions` — 1, except a wave whose TCs need two at once; every cross-platform wave is at least 2.

Done when: every remaining TC sits in a wave, and every wave carries `Platforms`, `Reset` and `Sessions`.

## Phase 8 — Write `exec-v2.md`

Write `tasks/{KEY}/exec/exec-v2.md` from `TEMPLATE.md`. TEMPLATE.md is the single authority on every section,
every field, and what built it — follow it directly. Do not maintain a separate section-to-phase mapping here;
TEMPLATE.md owns that contract.

The file states *what* to execute. `manual-exec-run-v2` owns *how* — capture mechanics, step ordering, result
recording, failure handling.

**Tier-1 recon results belong in the file.** Every TC whose result was determined at Phase 4 carries its real
result line now — `verified at recon, build {x}` for a pass, or the failure/deferred prose for anything else.
These are not a summary table; they are the per-TC result lines the run reads.

**Write no results summary table.** The run generates the aggregate summary once, from the result lines, at
its report phase. The design phase writes no such table.

**After writing:** for every Tier-1 TC that passed at recon, ask the user in one message:

> The following {n} Tier-1 TCs passed at recon and carry a result already:
> {list}
> Do you want any of them re-verified in the run? If yes, name them — they will be prioritised to Wave 1.

Re-verify → clear the TC's result line back to `⏳ PENDING`, move it into Wave 1 (or the earliest applicable
wave), and note in the TC that re-verification was requested. Keep → result stands, TC carries no wave entry.

Done when: every section TEMPLATE.md defines is present, or omitted on the condition its own note states;
every Tier-1 result is written; every precondition matches the environment's actual state after recon; and the
user has been asked about re-verification.

## Phase 9 — Reconcile, then GATE

Two mechanical checks, in one call:

```bash
grep -c '^### TC-' tasks/{KEY}/exec/exec-v2.md      # + Skipped rows must equal the tc.md count
grep -n '^### TC-\|^- .* · ' tasks/{KEY}/exec/exec-v2.md
```

Every included TC must carry exactly one result line per platform it runs on — one per pair, for a
cross-platform TC. Resolve every mismatch before presenting.

Then present, and stop until the user approves:

- **Blockers** — every unaddressable element with the TCs it blocks and the fix its pack names; every
  Preflight item that could not be confirmed; every platform excluded and why
- **Tier-1 results** — what passed, what failed, what was deferred and why; plus the visual sweep's findings
- **Added Coverage** — every uncovered AC and the TC written for it
- **Discrepancies** — every TC-sheet-vs-live disagreement, and every element or behaviour present on one
  platform and absent on another
- **Open questions** — anything still unanswered

Everything else is in the file. Do not restate it.

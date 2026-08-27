# Goal

Audit and improve `/manual-exec-run` — **and every rule and reference file the manual-execution chain loads,
`/manual-exec-design` included** — until the pair is the simplest reliable design that takes an approved
`exec.md` to a complete `report.md`.

Neither `exec.md` nor `report.md` has ever been produced in this repo (`tasks/` holds only `jira.md`, `tc.md`,
`tc-plan.md`). The chain is unexercised. Audit the contract, not remembered field behaviour, and never assume a
rule works because it has survived.

The agent may redesign either skill's flow, structure, references, and intermediate artifacts when that
produces a better result.

Do not preserve the existing design merely because it already exists.

# Scope

The whole closure below is in scope. Nothing outside it is.

**The two skills**

| File | Role |
|---|---|
| `.claude/skills/manual-exec-run/SKILL.md` | the skill under audit |
| `.claude/skills/manual-exec-run/REPORT.md` | `report.md` template |
| `.claude/skills/manual-exec-design/SKILL.md` | upstream skill — produces the input |
| `.claude/skills/manual-exec-design/TEMPLATE.md` | `exec.md` template — the shared contract |

**Design references**

`references/evidence.md` · `references/expected-results.md` · `references/recon.md` ·
`references/surface-app.md` · `references/surface-bo.md` ·
`references/evidence-common.md`, `evidence-normal.md`, `evidence-screenshot.md` (already aborted stubs)

**Steering rules both skills load**

`manual-exec-triage.md` · `capture-mechanics.md` · `capture-web.md` · `capture-device.md` ·
`capture-screenshot-guide.md` · `capture-video-guide.md` · `playwright-rule.md` · `mobile-mcp-rule.md` ·
`project-config.md` · `.claude/docs/lessons.md`

**Adjacent, read before judging — do not rewrite unless the audit proves an overlap**

`.claude/skills/capture-evidence/SKILL.md` (a peer capture skill sharing the same steering files) ·
`.claude/domain/*` (loaded by the surface packs) · `.claude/locator-cache.json`

**Out of scope:** `report-bug`, `verify-bug`, `jira-handler`, `collect-*`, and every TC-authoring skill. Touch
them only to fix a reference this work breaks.

# Understand the System

Before editing:

1. Read `/manual-exec-run/SKILL.md` and `REPORT.md`.
2. Read `/manual-exec-design/SKILL.md` and `TEMPLATE.md` — `TEMPLATE.md` defines every field the run skill
   consumes.
3. Read every reference and steering file listed in Scope.
4. Read `/workflows/workflow-manual-exec.md`.

Then trace, end to end:

`jira.md + tc.md → design phases → exec.md → run phases → results in exec.md + evidence/ + report.md → report-bug → finalise → Testmo`

Build a clear understanding of:

* which fields of `exec.md` the run skill actually reads, and which it never touches
* which rules the run skill needs at Phase 1 versus per wave versus per TC
* what `report.md` must carry for `report-bug` and Step 6 to work without re-reading `exec.md`
* which rule is stated in more than one file, and which file should own it

Do not audit either skill in isolation. A rule duplicated between them is one finding, not two.

# Ownership Boundary

The chain already claims a split: **design states *what* to execute; run owns *how*.** Treat that as the rule
that settles every duplication, and enforce it in one direction only:

* A decision the plan fixes (target, surface, evidence mode, grouping, wave order, checkpoint) is stated in
  `exec.md` and never re-derived at run time.
* A mechanic (how to capture, how to recover a locator, how to record a result) belongs to the run skill or a
  steering file, and never to the plan.
* A rule both skills need is stated once, in a file both can reach, and referenced — not copied.

Where the boundary is currently violated, fix the file that violates it. Where the boundary itself is the wrong
line, move it deliberately and say why.

# Audit

Find:

* duplicated rules — inside a file, between the two skills, and between a skill and its steering files
* rules stated in the skill that `TEMPLATE.md` or `REPORT.md` already enforces
* redundant statements, verbose wording, unnecessary explanations and examples
* overlapping, conflicting, or ambiguous instructions
* unnecessary steps, phases, references, and files
* inefficient context loading — anything read before it is needed, or read in full when a slice would do
* required reads whose content is not scoped to the skill that requires them
* hidden assumptions, and decisions that should be deterministic
* fields `exec.md` carries that nothing downstream consumes
* fields the run skill or `report-bug` needs that `exec.md` or `report.md` does not carry
* workflow requirements in `/workflows/workflow-manual-exec.md` not explicitly covered by either skill
* resume, failure, and partial-run paths that the current text leaves undefined

Report each finding with its file, the rule it duplicates or contradicts, and the fix.

# Known Suspects

Start here. Confirm or dismiss each — do not assume any is real.

1. **The capture cluster.** `capture-mechanics.md`, `capture-web.md`, `capture-device.md`,
   `capture-screenshot-guide.md`, `capture-video-guide.md`, `references/evidence.md`, and
   `skills/capture-evidence/SKILL.md` cross-reference each other in a ring (~5k tokens). Establish which file
   owns capture *policy*, which owns per-driver *mechanics*, and collapse the rest.
2. **Cross-skill reach-in.** `manual-exec-run` requires
   `.claude/skills/manual-exec-design/references/evidence.md`. A shared contract living inside the other
   skill's private references is a maintenance trap — relocate it or justify it.
3. **Aborted stubs.** `references/evidence-common.md`, `evidence-normal.md`, `evidence-screenshot.md` are
   three 5-line redirects. Confirm nothing loads them, then decide whether the redirect still earns its file.
4. **Paired `bo+app` mechanics** are restated in `manual-exec-design/SKILL.md`, `TEMPLATE.md`,
   `manual-exec-run/SKILL.md`, and the workflow. Pick one owner.
5. **Surfaces-and-targets table** appears in the design skill and the workflow, and its vocabulary is assumed
   by the run skill. The workflow is a contract — dedupe on the skill side.
6. **`.claude/docs/lessons.md`** is a required read for every run, and holds a Jira-attachment lesson that no
   run needs. Either scope the read or scope the file.
7. **Run Phase 2's six per-TC steps** carry their own sub-rules for slicing, asserting, recording, capturing
   and tearing down. Check that each rule fires at the point it is needed and is stated exactly once.
8. **`REPORT.md` vs Phase 3.** The skill lists what each report section must contain; so does the template.
   One of the two is redundant.

# Redesign

You may redesign either skill rather than merely shorten it.

You may:

* reorder, combine, split, or remove phases and steps
* change either skill's execution flow
* change when references are loaded, and how much of each is loaded
* change how information moves between phases and between the two skills
* change the fields `exec.md` carries, provided both skills and the workflow stay consistent
* introduce intermediate artifacts when they reduce repeated context
* restructure, split, merge, or replace reference and steering files
* change how `report.md` is produced
* replace an existing approach entirely if a better design is justified

Do not redesign for the sake of being different.

Every structural change must improve at least one of:

* correctness
* clarity
* reliability
* context efficiency
* maintainability
* output quality

A change to `exec.md`'s shape is a change to both skills. Land both sides in the same pass, or do not land it.

# Design Principles

Prefer:

* one rule stated once, in the file that owns it
* short imperative instructions
* explicit contracts between phases and between skills
* deterministic decisions
* minimal context loading — load per target, per wave, per group, never "for context"
* clear phase boundaries with a stated Done-when
* references only when necessary
* intermediate artifacts when they reduce repeated context

Avoid:

* duplicated rules
* unnecessary explanations, process steps, and files
* repeated context and re-reads
* implicit assumptions
* instructions that do not change agent behaviour

Optimize in this order:

**correctness → reliability → clarity → context efficiency**

Do not sacrifice correctness merely to reduce tokens. An execution skill that loses a result, overwrites
evidence, or reports a pass it did not observe is worse than a verbose one.

# File Changes

You may:

* rewrite `manual-exec-run/SKILL.md` and `REPORT.md`
* rewrite `manual-exec-design/SKILL.md` and `TEMPLATE.md`
* create, restructure, merge, split, rename, or replace reference and steering files
* create intermediate artifacts
* abort obsolete files instead of deleting them, following the stub convention already in
  `references/evidence-normal.md`
* update every reference that any of the above breaks — repo-wide, not just in these two skills

Do not permanently delete files.

Do not modify `/workflows/workflow-manual-exec.md` unless explicitly required. Treat it as the contract.

After editing `.claude/`, run `python3 sync-kiro.py` to regenerate `.kiro/`.

# Contracts That Must Not Break

1. **`exec.md` is the single authority at run time.** The run skill re-decides nothing the plan states.
2. **A result is decided by its assertion**, never by whether evidence was captured.
3. **One result per target**, and one per pair for a `bo+app` TC.
4. **A `PASSED` target never re-runs** and its evidence is never overwritten.
5. **The run skill never files a bug** and never invokes another skill to do it.
6. **`finalise` edits files only** — it posts nothing to Jira.
7. **`report.md` must be sufficient for `report-bug`** without re-reading `exec.md`.
8. **Every artifact path** follows `project-config.md` § Folder Structure.
9. **A fresh session can resume** from the artifacts alone, with no memory of a prior run.

# Validation

Before finishing:

1. Re-read both final `SKILL.md` files as if starting a new session, cold.
2. Verify every required rule is stated once, in one owning file.
3. Verify every reference is necessary, and loaded at the latest point it can be.
4. Verify there are no contradictions or ambiguous instructions — within a file, or between the two skills.
5. Verify the redesigned flow satisfies every step, gate, and output of `/workflows/workflow-manual-exec.md`.
6. Verify every field `TEMPLATE.md` defines is consumed by the run skill, and every field the run skill reads
   is defined by `TEMPLATE.md`.
7. Verify every section `REPORT.md` defines is fillable from what a run actually records, and that
   `report-bug` and Step 6 need nothing it omits.
8. Verify each of the nine contracts above still holds.
9. Walk the failure paths: absent target, missing data, unresolved locator, failed assertion, capture failure,
   crash mid-wave, compaction mid-run, partial resume, `finalise` with no `report.md`. Each must have exactly
   one defined outcome.
10. Verify obsolete files are clearly aborted and no active reference depends on them — repo-wide.
11. Verify `python3 sync-kiro.py` has run and `.kiro/` matches `.claude/`.
12. Remove anything that does not materially change agent behaviour.

Report the before/after token cost of the mandatory read set, per target type.

# Done When

The result is not merely a shorter version of the two skills.

It is the **simplest reliable design** that:

1. gives a running agent one clear execution path per target,
2. loads only the context that target and that wave need,
3. states every rule exactly once, across both skills and every file they load,
4. produces a complete `report.md` that `report-bug` can consume unaided, and
5. lets a fresh session resume mid-run from `exec.md` alone.

A new agent should be able to open an approved `exec.md` and execute the full run without this conversation,
hidden assumptions, or unnecessary supporting context.

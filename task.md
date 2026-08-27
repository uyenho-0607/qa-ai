# Goal

Audit and improve `/manual-exec-design` until it is the simplest reliable skill for designing `exec.md`.

`exec.md` does not currently exist. The agent must determine what `exec.md` should contain from the skill, its references, and its downstream workflow.

The agent may redesign the skill's flow, structure, references, and intermediate artifacts when that produces a better result.

Do not preserve the existing design merely because it already exists.

# Understand the System

Before editing:

1. Read `/manual-exec-design/SKILL.md`.
2. Read every reference file mentioned, loaded, or required by `SKILL.md`.
3. Read `/workflows/workflow-manual-exec.md`.
4. Trace how the workflow expects the skill to operate and what `exec.md` needs to provide downstream.

Build a clear understanding of:

`inputs → skill flow → references → decisions → exec.md → downstream workflow`

Do not audit the skill in isolation.

# Audit

Find:

* duplicated rules
* redundant statements
* verbose wording
* repeated information across files
* unnecessary explanations
* unnecessary examples
* overlapping or conflicting instructions
* ambiguous instructions
* unnecessary steps
* unnecessary references
* inefficient context loading
* hidden assumptions
* decisions that should be deterministic
* workflow requirements not explicitly covered by the skill

# Redesign

You may redesign the skill rather than merely shorten it.

You may:

* reorder, combine, split, or remove steps
* change the skill's execution flow
* change when references are loaded
* change how information moves between phases
* introduce intermediate artifacts when useful
* restructure, split, merge, or replace reference files
* change how `exec.md` is produced
* replace the existing approach entirely if a better design is justified

Do not redesign for the sake of being different.

Every structural change should improve at least one of:

* correctness
* clarity
* reliability
* context efficiency
* maintainability
* output quality

# Design Principles

Prefer:

* one rule stated once
* short imperative instructions
* explicit contracts
* deterministic decisions
* minimal context loading
* clear phase boundaries
* simple inputs and outputs
* references only when necessary
* intermediate artifacts when they reduce repeated context

Avoid:

* duplicated rules
* unnecessary explanations
* unnecessary process steps
* unnecessary files
* repeated context
* implicit assumptions
* instructions that do not affect agent behavior

Optimize in this order:

**correctness → reliability → clarity → context efficiency**

Do not sacrifice correctness merely to reduce tokens.

# File Changes

You may:

* rewrite `SKILL.md`
* create new reference files
* restructure existing reference files
* create intermediate artifacts
* rename or replace obsolete files
* abort obsolete files instead of deleting them
* update all affected references

Do not permanently delete files.

Do not modify `/workflows/workflow-manual-exec.md` unless explicitly required. Treat it as the downstream workflow contract.

# Design `exec.md`

Since `exec.md` does not yet exist, determine its required structure from the workflow and skill requirements.

The resulting `exec.md` must be:

* self-contained
* clear
* concise
* unambiguous
* directly usable by an agent in a fresh session
* sufficient to execute the intended manual-execution design workflow
* free of unnecessary context and duplicated rules

Do not add content merely because it may be useful.

Include only information required for correct downstream execution.

# Validation

Before finishing:

1. Re-read the final `SKILL.md` as if starting a new session.
2. Verify every required rule is stated once.
3. Verify every reference is necessary.
4. Verify there are no contradictions or ambiguous instructions.
5. Verify the redesigned flow satisfies `/workflows/workflow-manual-exec.md`.
6. Verify context loading is intentional and minimal.
7. Verify the proposed `exec.md` contains everything required downstream.
8. Verify `exec.md` contains nothing that is unnecessary or duplicated.
9. Verify obsolete files are clearly aborted and no active reference depends on them.
10. Remove anything that does not materially improve agent behavior.

# Done When

The result is not merely a shorter version of the existing skill.

It is the **simplest reliable design** that:

1. gives an agent a clear execution path,
2. loads only the context it needs,
3. avoids duplicated or conflicting instructions,
4. produces a correct `exec.md`, and
5. allows `exec.md` to be loaded independently in a fresh session.

A new agent should be able to fetch `exec.md` and execute the intended workflow without this conversation, hidden assumptions, or unnecessary supporting context.

# qa-ai

Skills-based manual QA framework for Claude Code and Kiro. Everything is prompt-driven: there is no app to
build and no test suite — the "code" is a set of skills plus the steering docs (rules) they load.
See `CLAUDE.md` for architecture.

## Setup

1. `pip install -r requirements.txt`
2. `cp .env.example .env` and fill it in
3. Fill every `<FILL_IN>` in `.claude/steering/project-config.md` — workflows will not run until this is done

## How it works

- **Skills** (`.claude/skills/<name>/SKILL.md`) are the actions. You invoke one by name or trigger phrase;
  it runs its phases in order and writes a file.
- **Steering docs** (`.claude/steering/`) are the rules. Skills load them at the step that needs them —
  never all at once.
- **Skills never call each other by side effect.** They chain through artifact files under `tasks/{KEY}/`,
  listed in `project-config.md` → Folder Structure. An entry-point skill *invokes* sub-skills explicitly.
- **Resumption is free.** Every skill checks what already exists in `tasks/{KEY}/` and restarts at the first
  step whose output is missing. Existing artifacts are re-presented, never silently overwritten.

`{KEY}` is a Jira issue key (e.g. `AO-306`).

## Entry-point skills

Start here. Everything else is invoked by one of these.

| Skill | Invoke with | What it does | Writes |
|---|---|---|---|
| `generate-tcs` | "generate TCs for AO-306" | Scope ACs/BRs/error messages → coverage plan → grill → write TCs → review → export (CSV / Google Sheet / Testmo) | `tc-plan.md`, `manual-tcs.md`, export target |
| `report-bug` | "/bug", "report this bug" | Classify FE/BE, capture evidence, create a SIT Bug subtask under the parent | Jira subtask + `evidence/{KEY}/` |
| `verify-bug` | "/verify-bugs-batch", "verify this fix" | Reproduce the STR, capture evidence, post the verification comment, transition the ticket | Jira comment + transition |
| `ui-discovery` | "explore this page", "map this feature" | Drive the live app and map workflows, values, validation, permissions, state transitions | Checkpoint Map + `.claude/domain/` flow file |
| `git-workflow` | "/branch", "/push", "/rebase", "/pr" | Branch → stage/push → rebase → GitHub PR for QA task files | branch, commits, PR |
| `audit-skills` | "/audit-skills <file>" | Token cost, cross-file duplication, and contract bugs in a skill or steering file | audit report |

`generate-tcs` chains `jira-retriever` → `figma-retriever` (if the ticket has Figma links) →
`collect-testmo-cases` → `grill-tcs` → `review-tcs` → `to-testmo`. Run it and you get the whole pipeline;
run a sub-skill directly when you only want that stage.

## Supporting skills

Called by an entry point, or directly when you want just one stage.

**Retrieval**

| Skill | Purpose |
|---|---|
| `jira-retriever` | Full ticket content — description, ACs, sub-tasks, comments, linked issues, images, Figma links → `jira.md` |
| `figma-retriever` | Frozen design snapshot + PNG screenshots → `attachments/figma-snapshot.md` |
| `collect-testmo-cases` | Existing Testmo cases linked to `{KEY}` → `tc.md` |
| `collect-gsheet-cases` | Existing cases from a Google Sheet tab → `tc.md` |

**Test case work**

| Skill | Purpose |
|---|---|
| `grill-tcs` | Stress-tests `tc-plan.md` *before* any TC is written — expected-result sources, missing negatives, weak oracles |
| `review-tcs` | Grades written TCs on coverage / oracle / reproducibility / form, then applies the fixes |
| `to-testmo` | Exports `manual-tcs.md` to Testmo — field mapping, issue link, configs, state |
| `apply-sheet-feedback` | Reads reviewer comments on a Sheet TC tab, classifies delete/update/add, applies the minimal edit |

**Execution & Jira**

| Skill | Purpose |
|---|---|
| `capture-evidence` | Screenshots/video via Playwright MCP. Force-reads `playwright-rule.md` first — never capture manually |
| `jira-handler` | All Jira writes — create bug, upload evidence, transition, post verification comment |

**Meta**

| Skill | Purpose |
|---|---|
| `writing-for-agents` | How to write any doc an agent consumes — skills, `CLAUDE.md`, pointer docs |
| `writing-conventions` | How to write or audit a convention file for this project |
| `handoff` | State-transfer document so another session can continue the work |
| `git-setup` | One-time `gh` install + token auth. Run before first `git-workflow` |

## Behaviour skills

These change how the agent behaves for the **rest of the session** once triggered.

| Skill | Trigger | Effect |
|---|---|---|
| `caveman` | "/caveman", "be brief" | Terse output, ~75% fewer tokens. Technical substance kept, fluff dropped |

Skill adherence and the approval-before-writes gate are **not** skills — they are working rules in
`CLAUDE.md`, which is auto-loaded every session.

## Rules (steering docs)

Skills load these; you rarely read them directly. Edit a rule to change behaviour across every skill that
loads it — that is the point.

| File | Owns |
|---|---|
| `project-config.md` | Env vars, folder structure, tool ids. **Fill this in first** |
| `tc-conventions.md` | TC format — naming, step wording, expected-result wording, traceability fields |
| `tc-design-guide.md` | Structural decisions — merge/split, step scope, pre-req anchoring, module assignment |
| `tc-scenario-guide.md` | What to test — coverage minimums per AC pattern, cross-cuts, sweep/match rules |
| `tc-priority-guide.md` | Priority scoring factors and the decision table |
| `qa-anti-patterns.md` | Smell → fix-owner index for TC and run reviews |
| `bug-conventions.md` | Bug title format, STR, severity, required fields |
| `jira.md` | Jira constants — site, `cloudId`, project/issue-type ids, transitions, bug assignment |
| `testmo.md` | Testmo project ids, folders, configurations |
| `playwright-rule.md` | Browser interaction rules. `browser_run_code_unsafe` only — the granular MCP tools are unreliable on SPAs |
| `reasoning-standards.md` | Label every claim fact / assumption / recommendation / unknown |

Two more reference stores, loaded on demand:

- `.claude/domain/` — app knowledge base: `otc-bo.md`, `otc-mobile.md`, `otc-shared.md`, and the approved
  module/naming list in `tc-naming-ref.md`
- `.claude/docs/lessons.md` — reusable lessons from verification and exploratory sessions. `report-bug` and
  `verify-bug` read it at pre-flight; append to it when a session teaches you something

## Typical sessions

```
# Full TC pipeline for a ticket
generate TCs for AO-306

# Only re-review TCs you already have
/review-tcs AO-306

# Pull existing cases before designing anything
collect TCs for AO-306

# File a bug found during a run
/bug

# Verify a fix and close the ticket
verify AO-306

# Ship the task files
/branch AO-306   →   /push   →   /mr
```

## Manual SIT execution (work in progress)

`workflow-manual-exec.md` specs a six-step pipeline from ticket to signed-off SIT run
(load Jira → load TCs → design plan → execute → report defects → finalise). Steps 1, 2, 5, and 6 use
existing skills; steps 3 and 4 need `manual-exec-design` and `manual-exec-run`, which are not written yet.
Treat that file as the spec for them, not a runnable workflow.

## Helper scripts

Python helpers under `.claude/skills/*/` are invoked by their owning skill, never standalone.
`scripts/format_tc_sheet.py` backs the Google Sheet export and is used by `generate-tcs`,
`review-tcs`, and `apply-sheet-feedback`.

## State

`tasks/`, `evidence/`, `reports/` are **not** gitignored — avoid broad `git add`. Use `git-workflow`,
which stages the specific files for the ticket.

## `.kiro/` mirror

`.kiro/` is generated from `.claude/`. Never hand-edit it.

| Command | Effect |
|---|---|
| `python3 sync-kiro.py` | regenerate `.kiro/` from `.claude/` |
| `python3 sync-kiro.py --check` | list stale files, change nothing (exit 1 if stale; used by pre-commit) |
| `python3 sync-kiro.py --promote <path>` | push one hand-edited `.kiro/` file back into `.claude/` |

To make a steering doc always-loaded in Kiro, add it to `STEERING_ALWAYS` in `sync-kiro.py`.

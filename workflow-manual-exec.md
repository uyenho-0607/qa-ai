# Manual SIT Execution Workflow

> **Status: partially implemented.** Steps 3 and 4 depend on the `manual-exec-design` and
> `manual-exec-run` skills, which do not exist in `.claude/skills/` yet. Steps 1, 2, 5, and 6 run
> today. Until those two skills are written, this file is the spec for them — not a runnable workflow.

Six steps from a Jira ticket to a signed-off SIT run. Every step is an independent skill chained by a file,
never by a skill calling another. Each artifact lands in `tasks/{KEY}/`; the next step reads it from there.
Actions and rules live in the skills — this file owns the prompts, the gates, and the order.

```
[Jira Ticket] → 1 Load Jira → 2 Load TCs → 3 Design → 4 Execute → 5 Report Defects → 6 Finalise
                                              ↓ GATE                    ↓ GATE
```

| Step | Skill | Writes |
|------|-------|--------|
| 1 | `jira-retriever` | `jira.md` |
| 2 | `collect-testmo-cases` \| `collect-gsheet-cases` | `tc.md` |
| 3 | `manual-exec-design` ⚠️ not implemented | `exec.md`, `recon/` |
| 4 | `manual-exec-run` ⚠️ not implemented | `exec.md` results, `evidence/{KEY}/`, `report.md` |
| 5 | `report-bug` | Jira SIT Bug subtasks under `{KEY}` |
| 6 | — | `report.md`, bug keys backfilled |

Paths follow `.claude/steering/project-config.md` → Folder Structure: chain files (`jira.md`, `tc.md`,
`exec.md`, `recon/`, `report.md`) live in `tasks/{KEY}/`; evidence lands in `evidence/{KEY}/`.

## 📥 STEP 1: Load Jira

```
Load Jira ticket {KEY} for manual SIT execution.
Use the jira-retriever skill with the `save` arg.
Report: summary, every acceptance criterion, affected module, build/fixVersion.
```

`save` is required — without it no file is written and Step 3 has nothing to read.

**Output:** `jira.md`; summary, numbered ACs, affected module, and the build number or `unknown`.

## 📋 STEP 2: Load Test Cases

```
Load the test cases for {KEY}.
Source: Testmo -> use collect-testmo-cases with the `save` arg. Google Sheet -> use collect-gsheet-cases
with the sheet URL.
Report: TC count, and each TC's ID and title.
```

The workflow cannot infer the source — name Testmo or give the sheet URL in the prompt. `collect-testmo-cases`
needs `save`; `collect-gsheet-cases` always writes.

**Output:** `tc.md`; TC count with each case ID, title, steps and expected result.

## 🧭 STEP 3: Design the Execution Plan — GATE

```
Design the manual execution plan for {KEY}.
Use the manual-exec-design skill (⚠️ not implemented yet). Complete every phase in order.
Report before I approve: reconciliation count, expected-result gaps found and how each was closed,
every TC-sheet-vs-live-UI discrepancy, and every TC blocked on input.
```

**Output:** `exec.md` + `recon/`; reconciliation `tc.md count == agent-executable + skipped`.

**Approve the plan before Step 4.** Execution never re-decides anything the plan states.

## 🧪 STEP 4: Execute

```
Execute the SIT run for {KEY}.
Use the manual-exec-run skill (⚠️ not implemented yet). Follow exec.md exactly — never re-decide evidence type, steps, or grouping.
Test first, record second. State the resume plan before executing.
```

**Output:** `exec.md` with no row left `PENDING`; `evidence/` — one labelled file per group or solo TC, named
`TC_{ids}_{slug}`; `report.md` with Summary and Bugs Found.

## 🐞 STEP 5: Report Defects — GATE

```
Show me the Bugs Found table from tasks/{KEY}/report.md, verbatim.
File nothing yet. I confirm each one.
```

Then, per confirmed defect:

```
File {TC-ID} as a SIT Bug under {KEY} using the report-bug skill.
```

File nothing before the user confirms it.

**Output:** one Jira SIT Bug per confirmed defect, with inline evidence; every declined candidate under
Rejected Candidates with its reason.

## 📊 STEP 6: Finalise the Report

```
Backfill the filed {BUG-KEY}s into tasks/{KEY}/report.md — Bugs Found and TC Results.
Present the Summary table and every Failed/Blocked TC.
```

**Output:** `report.md` complete with every bug key resolved; Summary table, pass rate, and every Failed and
Blocked TC presented.

## When to Use Each Step

| Scenario | Steps |
|----------|-------|
| New feature, full manual SIT | 1 → 2 → 3 → 4 → 5 → 6 |
| Re-test after a fix, or `exec.md` already approved | 4 → 5 → 6 |
| TCs already collected | 3 → 4 → 5 → 6 |
| Design only, execute later | 1 → 2 → 3 |
| Run passed, nothing to file | 1 → 2 → 3 → 4 → 6 |
| Bug verification only | `verify-bug` skill instead |

## Resumption

Artifacts decide the entry point, not memory of a previous session: list `tasks/{KEY}/` and start at the
first step whose output is missing. Each skill asks overwrite / reuse / abort where its output exists. Never
overwrite an `exec.md` holding execution results.

## Prerequisites

- Jira access (Atlassian MCP), browser (Playwright MCP)
- Testmo access (Testmo MCP), or `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` / `GOOGLE_REFRESH_TOKEN` in `.env` at the repo root for a TC sheet
- SIT reachable, and every account named in the exec plan able to log in
- `tasks/`, `evidence/`, and `reports/` are **not** gitignored — avoid broad `git add`; stage per-ticket
  files with the `git-workflow` skill

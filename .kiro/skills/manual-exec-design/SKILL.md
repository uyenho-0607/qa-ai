---
name: manual-exec-design
description: Build exec.md, the manual SIT execution plan: triage TCs, deepen expected results, group evidence, order waves. Use on "design exec plan", /exec-design, or when manual-exec-run finds no exec.md.
---

## Contract

- **Arg:** `{KEY}` — e.g. `OMS-1120`
- **Workspace:** `tasks/{KEY}/`
- **Reads:** `tasks/{KEY}/jira.md`, `tasks/{KEY}/tc.md`
- **Writes:** `tasks/{KEY}/exec.md`
- **Missing input:** STOP and name the producer — `jira.md` → disclose_context("jira-retriever") with `save`; `tc.md` → disclose_context("collect-testmo-cases") with `save`, or disclose_context("collect-gsheet-cases"). Never fall back to Jira MCP or to chat context.
- **Output exists:** ask — overwrite (rebuild from Phase 1), reuse (keep the file, run no phases), or abort. Never clobber a file holding execution results.

**Hard rule:** complete every phase in order. Never skip one.

## Phase 1 — Read the inputs

- Read `tasks/{KEY}/jira.md`. List every specified behaviour, including implicit constraints.
- Read `tasks/{KEY}/tc.md`. List every TC with its ID, steps, and expected result.
- Record the build under test from the Jira fixVersion or the app's about/footer. Write `unknown` rather than inventing one.

Done when: every behaviour is listed, every TC is accounted for, and the build is recorded or explicitly `unknown`.

## Phase 2 — Recon the UI

disclose_context("ui-discovery") — scope it to the pages named in the TC steps.

- Flag every discrepancy between the TC's expected result and the live UI.
- Build the locator table, naming each entry's source.
- Record any state left changed by recon.

Done when: the locator table is complete, every entry names its source, and all discrepancies are noted.

## Phase 3 — Classify the TCs

Apply `.kiro/steering/manual-exec-triage.md` to every TC:

- Agent-executable → include in the exec file
- Human-executable → Skipped section with reason
- Ambiguous → ask before deciding

Done when: every TC is classified with no unresolved ambiguity.

## Phase 4 — Strengthen the expected results

Reference `references/expected-results.md`. Per agent-executable TC: assign depth levels, run the four questions, rewrite the expected result to close every gap.

Done when: every TC states each depth level it needs as a separate checkable assertion, every assertion is tied to an objective DOM fact, and no TC carries a single-bullet expected result unless it verifies a single static state.

## Phase 5 — Group the evidence

Reference `references/evidence-rules.md`. Group the TCs, assign an evidence type per group or solo TC, derive each file path, and build the Evidence Groups table defined in `TEMPLATE.md`.

Done when: every TC has a group, an evidence type, and a file path; every TC sharing a file names the others it shares with; every SCREENSHOT choice satisfies all four conditions in `references/evidence-rules.md`; and every file name carries every member TC-ID per that file's § Naming.

## Phase 6 — Order the waves

Order groups to minimise state transitions:

- Place a dependent TC immediately after its prerequisite, with nothing between them.
- Omit both `**Pre:**` and `**Teardown:**` where a TC ends in the next TC's precondition — the omission *is* the continuation.
- Never place TCs that mutate the same data in the same wave.
- Assign 2 contexts only to a TC needing two sessions open at once. Otherwise 1.
- Cap each wave at one VIDEO group.

Build the Waves table defined in `TEMPLATE.md`.

Done when: every group and every solo TC has a wave, every wave needing 2 contexts names the TC that requires them, and no wave holds two VIDEO groups.

## Phase 6.5 — GATE

Present the classification, the Evidence Groups table, and the Waves table. Stop until they are approved. Never write the exec file before approval.

## Phase 7 — Write the exec file

Write `tasks/{KEY}/exec.md` from `TEMPLATE.md`, filling every section it defines with what Phases 2–6 built.

- Give each TC an exact account and starting state under `**Pre:**`, or omit the line where it continues from the previous TC.
- Write the username and password for every account named in Execution Context.
- Number the steps and make each one deterministic.
- Give every input field an explicit value.
- Give `**Teardown:**` explicit steps, or omit the line where nothing needs restoring.
- Keep how-to-execute rules out of the exec file — capture mechanics, step ordering, failure handling. They belong to `manual-exec-run`.

Done when: every TC section is complete, the Locators Reference table carries every locator from Phase 2, Environment deviations names every state recon changed or says `none`, and every precondition matches the environment's actual state.

## Phase 8 — Present

Reconcile first: `tc.md count == agent-executable + skipped`, and every TC carries the Case ID from `tc.md`. List every unaccounted TC and every missing Case ID, and resolve them before presenting.

Then present:
- Reconciliation result
- Gaps found and how each was strengthened
- Every TC-sheet-vs-live-UI discrepancy
- Every TC blocked on input

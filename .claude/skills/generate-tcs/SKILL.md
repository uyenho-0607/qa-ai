---
name: generate-tcs
description: Generate manual test cases from a Jira ticket, then export to a Sheet or Testmo. Use when asked for test cases for a ticket, or when another skill needs `tasks/{KEY}/gen/manual-tcs.md`.
---

# Generate Test Cases

**Done when:** every AC, BR, and error message traces to a written TC or to a recorded gap; the confirmed export target is written.

## Contract

- **Args:** `{KEY}` [, path to an existing `jira.md`]
- **Writes:** the 1.4 numbering back into `tasks/{KEY}/base/jira.md`; `tasks/{KEY}/gen/tc-plan.md`; `tasks/{KEY}/gen/manual-tcs.md`; plus the export target confirmed in 1.7
- **Steering:** loaded at 1.7, 2.1 and 3.1 — those steps name the files
- **Resumes at:** the first missing of `jira.md` → `tc-plan.md` → `manual-tcs.md`; an existing artifact is re-presented, never silently rewritten
- **No Agent tool in context:** every agent dispatch below falls back to invoking the same-named skill FULLY with the same args — `jira-fetcher` → `jira-retriever` + `save`; `testmo-collector` → `collect-testmo-cases` + `save`, `no-gate`; `tc-grader` → `grill-tcs` / `review-tcs` + `no-gate`

**File writes (all phases):** write the file directly, then say "Written to `path` — check it and let me know if anything needs updating." The file is the review surface; chat carries the summary block only.

---

## Phase 1 — Scope

**1.1 Load ticket.** `tasks/{KEY}/gen/tc-plan.md` or `manual-tcs.md` already present → present it and ask: resume | rewrite | abort. Then: path given → read it. Otherwise → dispatch the `jira-fetcher` agent for `{KEY}`, then read `tasks/{KEY}/base/jira.md`. Work the AC, BR, and error text from that file, never from the agent's receipt.

Harvest from the whole file: user flows, every BR-table row, every error validation message verbatim, the latest AC version, sprint scope and out-of-scope notes.

**1.2 Figma.** Check `tasks/{KEY}/base/jira.md` for `## Figma Links` entries. Entries present and no `tasks/{KEY}/base/figma/figma-snapshot.md` → dispatch the `figma-fetcher` agent with the Figma URL and `{KEY}`, then read the written `figma-snapshot.md` — never work from the agent's receipt. No Agent tool in context → invoke the `figma-retriever` skill FULLY instead. No Figma links → continue.

**1.3 Linked issues.** For every linked issue describing shared/common behavior ("connects to", "relates to"), dispatch one `jira-fetcher` agent per key — **all of them in a single message**. Read each returned file and merge its BRs/ACs/ERRs into scope. If a link is not relevant (e.g. purely informational), record it in the plan with a one-line note and continue.

**1.4 Number the scope.** Every AC → `AC-n`, every BR → `BR-n`, every error message → `ERR-n` holding the exact string. Extract prose ACs as conditions and number them the same way. No ACs in the ticket → derive them from the description and mark each `derived`.

Write the numbered ids back into `tasks/{KEY}/base/jira.md` under `## Acceptance Criteria`, `## Business Requirements`, and `## Error Messages` — the exact heading text `jira-retriever` writes. A heading that does not exist → create it.

**1.5 Classify out-of-scope items.** Split each into **feature-absence** (nothing to assert, e.g. "QR code scanning") or **restricted-capability** (an enforceable constraint, e.g. "editing wallet address details other than Nickname") — the latter gets a `new` row in the plan for a negative TC confirming the constraint holds.

**1.6 Existing TCs.** Propose the Module folder now based on the ticket's feature area. Ask once:

```
Proposed Module: [name]
Check Testmo for existing TCs — ticket-linked (T) / whole Module folder (M) / none (N)?
```

- T → dispatch the `testmo-collector` agent for `{KEY}`, then read `tasks/{KEY}/base/tc.md`.
- M → T, plus `testmo_list_cases` on the confirmed Module folder, names only.

Either way, **gap-mine** the retrieved titles as hard as you dedup them: a capability the ticket never names (search, filter, an admin override) becomes a scope question in 1.7. A value sourced only from Testmo stays `needs-clarification`.

**1.7 Present scope, Configuration, and export target.**

Module name and the platform's default Configuration — `##` is the platform group, `###` are the Modules, `>` carries that group's default Configuration:
```bash
grep -E '^##+ |^> ' .claude/domain/tc-naming-ref.md
```

Confirm the proposed Configuration names exist in Testmo:
```bash
awk '/^## /{p = /Configurations by Project/} p' .claude/steering/testmo.md
```

Export target — `Google Sheet` (team template) or `Testmo`. Sheet → propose `{KEY}` as the tab name.

```
Scope — {KEY}    Module: [proposed]    Configuration: [proposed]
Export: [Google Sheet, tab {KEY} | Testmo]
[n] ACs · [n] BRs · [n] ERRs · Out of scope: [n items / none]
Full detail in tasks/{KEY}/base/jira.md

Confirm, or correct Module / Configuration / export target / scope:
```

**GATE — stop until scope, Module, Configuration, and export target are confirmed.**

---

## Phase 2 — Plan coverage

**2.1 Load the rules.**

```bash
cat .claude/steering/tc-scenario-guide.md .claude/steering/tc-design-guide.md
```

**2.2 Plan.** Apply **sweep → match → cross-cut** from `tc-scenario-guide.md` and **merge/split decisions** from `tc-design-guide.md` to every numbered item in the scope. Write the plan to `tasks/{KEY}/gen/tc-plan.md`, one row per scenario:

| # | Refs | Screen | Crit | Scenario | Type | Expected-value source | Status |

- **Refs** — every `AC-n` / `BR-n` / `ERR-n` the scenario covers. Every id from Phase 1 appears in at least one row; an id no scenario covers gets its own row with Status `gap` and the reason.
- **Crit** — Business Criticality per `tc-priority-guide.md`: High | Medium | Low.
- **Expected-value source** — the AC, error-message row, live UI observation, or domain file the expected result comes from. No source → Status `needs-clarification` and no invented value.
- **Status** — `new`, `covered by [existing TC name]` (from 1.6), `gap`, or `needs-clarification`.

**2.3 Grill.** Dispatch the `tc-grader` agent for `{KEY}` with `plan`. Apply every finding it returns to `tc-plan.md`, and move a row you cannot resolve to Status `needs-clarification` with the grader's question attached.

After writing the file, present only:

```
Plan written → tasks/{KEY}/gen/tc-plan.md
[n] scenarios · [n] gap · [n] needs-clarification

Needs your input:
  [ref]  [one-line reason]   ← only gap / needs-clarification rows
```

**GATE — stop until the plan is confirmed.**

---

## Phase 3 — Write TCs

**3.1 Load the rules.** Run every time:

```bash
cat .claude/skills/generate-tcs/TEMPLATE.md \
    .claude/steering/tc-conventions.md \
    .claude/steering/tc-priority-guide.md \
    .claude/steering/qa-anti-patterns.md
```

Then the approved Sub-module and Feature names for the Module confirmed in 1.7 — substitute that Module for `{Module}`:

```bash
awk -v m="{Module}" '/^#/{p = ($0 == "### " m)} p' .claude/domain/tc-naming-ref.md
```

Empty output means the Module name does not match the reference — return to 1.7 and re-confirm rather than inventing a name. A Module listed under both platform groups returns both tables; pick the one matching the confirmed Configuration.

`tc-scenario-guide.md` and `tc-design-guide.md` are already in context from Phase 2.1 — do not reload.

**3.2 Write.** Pull the rows to write — the Scope Summary and any findings log in the plan are Phase 2 work product, not input here:

```bash
grep -E '^\| *[0-9]+[a-z]? *\|' tasks/{KEY}/gen/tc-plan.md | grep -vE 'covered by|\| *gap *\||needs-clarification'
```

One block per row returned.

**3.3 Self-check.** After writing all TC blocks, check every block against every row of `qa-anti-patterns.md` — already in context from 3.1 — except #12, which grades a run result, not a case. Fix in place, never defer to review.

**Done when:** every `new` row has exactly one TC block, each block carries every TEMPLATE field its case needs, each block's `Requirement Reference` repeats that row's Refs verbatim, and the self-check above passes for every block.

After writing, say: "[n] TCs written → tasks/{KEY}/gen/manual-tcs.md"

---

## Phase 4 — Self-review and coverage

**4.1 Review.** Dispatch the `tc-grader` agent for `{KEY}`. It grades and proposes; it edits nothing.

Apply every `fix` finding to `tasks/{KEY}/gen/manual-tcs.md` yourself, taking the grader's `Proposed fix` text as written. Carry every `ask` finding into the 4.3 summary with its id and question — an `ask` is for the user, not for you to answer. A `blocker` stops the export until it is resolved.

**4.2 Reconcile.** Count from the file, never from memory and never by re-reading it whole:

```bash
grep -c '^## ' tasks/{KEY}/gen/manual-tcs.md                            # TC count
grep '^\*\*Requirement Reference:\*\*' tasks/{KEY}/gen/manual-tcs.md    # AC/BR/ERR coverage
grep '^\*\*Priority:\*\*' tasks/{KEY}/gen/manual-tcs.md | sort | uniq -c  # 4.3 priority split
grep -o '\*\*Configuration:\*\*.*' tasks/{KEY}/gen/manual-tcs.md | sort -u   # must match the 1.7 confirmation
```

`new` row count == TC count, and every `new` row's `#` appears in exactly one TC — name a mismatch, never round it. Every Configuration name must match the one confirmed in 1.7. Flag as `thin` every High Business Criticality id whose only TC is a Happy Path scenario — grep the plan's rows for that id to check.

**4.3 Present only:**

```
Coverage — {KEY}    [n] TCs · High [n] / Med [n] / Low [n]
ACs [n]/[n]  BRs [n]/[n]  ERRs [n]/[n]
Self-review: [n] fixes applied · [n] ask items
Full detail → tasks/{KEY}/gen/tc-plan.md

Needs your input:
  [ref/id]  thin | gap | needs-clarification | ask   [one-line reason]
```

**GATE — stop until approved and every `ask` item is resolved or explicitly skipped.**

---

## Phase 5 — Export

Run the target confirmed in 1.7. No further stop.

- **Sheet** — spreadsheet id: ask the user, or reuse the one from a previous `{KEY}` export; tab name from 1.7.
  ```
  .venv/bin/python3 scripts/format_tc_sheet.py \
    --md tasks/{KEY}/gen/manual-tcs.md \
    --sheet {TC_SHEET_ID} \
    --tab "{KEY}"
  ```

- **Testmo** — Invoke `to-testmo` with `{KEY}` and the Module folder confirmed in 1.7.

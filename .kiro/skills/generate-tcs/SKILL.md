---
name: generate-tcs
description: Generate manual test cases from a Jira ticket — scope ACs and BRs, plan coverage, write TCs, export to CSV, Sheet, or Testmo. Use when asked for test cases for a ticket, or when another skill needs `tasks/{KEY}/gen/manual-tcs.md`.
---

# Generate Test Cases

**Done when:** every AC, BR, and error message traces to a written TC or to a recorded gap; the confirmed export target is written.

## Contract

- **Args:** `{KEY}` [, path to an existing `jira.md`]
- **Invokes:** `jira-retriever` → `tasks/{KEY}/base/jira.md` + `tasks/{KEY}/base/attachments/`; `collect-testmo-cases` → `tasks/{KEY}/base/tc.md`; `grill-tcs` → updates `tc-plan.md`; `review-tcs` → fixes applied in place; `to-testmo` → Testmo cases
- **Writes:** the 1.3 numbering back into `tasks/{KEY}/base/jira.md`; `tasks/{KEY}/gen/tc-plan.md`; `tasks/{KEY}/gen/manual-tcs.md`; plus the export target confirmed in 1.7
- **Steering:** loaded at 2.1 and 3.1 — those steps name the files
- **Resumes at:** the first missing of `jira.md` → `tc-plan.md` → `manual-tcs.md`; an existing artifact is re-presented, never silently rewritten

**File writes (all phases):** write the file directly, then say "Written to `path` — check it and let me know if anything needs updating." The file is the review surface; chat carries the summary block only.

---

## Phase 1 — Scope

**1.1 Load ticket.** Path given → read it. Otherwise → Invoke `jira-retriever` with `{KEY}`, `save`, then read `tasks/{KEY}/base/jira.md`.

Harvest from the whole file: user flows, every BR-table row, every error validation message verbatim, the latest AC version, sprint scope and out-of-scope notes.

**1.2 Figma.** Check `tasks/{KEY}/base/jira.md` for any `## Figma Links` entries. If present and `tasks/{KEY}/base/figma/figma-snapshot.md` does not already exist → Invoke `figma-retriever` with the Figma URL and `{KEY}`. If no Figma links → continue.

**1.3 Linked issues.** For every linked issue describing shared/common behavior ("connects to", "relates to"), invoke `jira-retriever` with that key and `save`. Merge harvested BRs/ACs/ERRs into scope. If a link is not relevant (e.g. purely informational), record it in the plan with a one-line note and continue.

**1.4 Number the scope.** Every AC → `AC-n`, every BR → `BR-n`, every error message → `ERR-n` holding the exact string. Extract prose ACs as conditions and number them the same way. No ACs in the ticket → derive them from the description and mark each `derived`.

Write the numbered ids back into `tasks/{KEY}/base/jira.md` under `## Acceptance Criteria`, `## Business Requirements`, and `## Error Messages` — the exact heading text `jira-retriever` writes. A heading missing because the ticket had no such section → create it.

**1.5 Classify out-of-scope items.** Split each into **feature-absence** (nothing to assert, e.g. "QR code scanning") or **restricted-capability** (an enforceable constraint, e.g. "editing wallet address details other than Nickname") — the latter gets a `new` row in the plan for a negative TC confirming the constraint holds.

**1.6 Existing TCs.** Propose the Module folder now based on the ticket's feature area. Ask once:

```
Proposed Module: [name]
Check Testmo for existing TCs — ticket-linked (T) / whole Module folder (M) / none (N)?
```

- T → Invoke `collect-testmo-cases` with `{KEY}`, `save`, `no-gate`.
- M → T, plus `testmo_list_cases` on the confirmed Module folder, names only. Duplicates from other tickets surface here and nowhere else.

Either way, **gap-mine** the retrieved titles as hard as you dedup them: a capability the ticket never names (search, filter, an admin override) becomes a scope question in 1.7. A value sourced only from Testmo stays `needs-clarification`.

**1.7 Present scope, Configuration, and export target.**

Module name and the platform's default Configuration — `##` is the platform group, `###` are the Modules, `>` carries that group's default Configuration:
```bash
grep -E '^##+ |^> ' .kiro/domain/tc-naming-ref.md
```

Confirm the proposed Configuration names exist in Testmo:
```bash
awk '/^## /{p = /Configurations by Project/} p' .kiro/steering/testmo.md
```

The Module confirmed here selects the naming tables Phase 3.1 loads — a wrong Module there costs every TC name.

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
cat .kiro/steering/tc-scenario-guide.md .kiro/steering/tc-design-guide.md
```

**2.2 Plan.** Apply **sweep → match → cross-cut** from `tc-scenario-guide.md` and **merge/split decisions** from `tc-design-guide.md` to every numbered item in the scope. Write the plan to `tasks/{KEY}/gen/tc-plan.md`, one row per scenario:

| # | Refs | Screen | Scenario | Type | Expected-value source | Status |

- **Refs** — every `AC-n` / `BR-n` / `ERR-n` the scenario covers. Every id from Phase 1 appears in at least one row; an id no scenario covers gets its own row with Status `gap` and the reason.
- **Expected-value source** — the AC, error-message row, live UI observation, or domain file the expected result comes from. No source → Status `needs-clarification` and no invented value.
- **Status** — `new`, `covered by [existing TC name]` (from 1.6), `gap`, or `needs-clarification`.

**2.3 Grill.** Invoke `grill-tcs` with `{KEY}`, `no-gate`.

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
cat .kiro/skills/generate-tcs/TEMPLATE.md \
    .kiro/steering/tc-conventions.md \
    .kiro/steering/tc-priority-guide.md \
    .kiro/steering/qa-anti-patterns.md
```

Then the approved Sub-module and Feature names for the Module confirmed in 1.7 — substitute that Module for `{Module}`:

```bash
awk -v m="{Module}" '/^#/{p = ($0 == "### " m)} p' .kiro/domain/tc-naming-ref.md
```

Empty output means the Module name does not match the reference — return to 1.7 and re-confirm rather than inventing a name. A Module listed under both platform groups returns both tables; pick the one matching the confirmed Configuration.

`TEMPLATE.md` is the format authority for every field, ER bullet, and separator. `tc-naming-ref.md` is the authority for Module, Sub-module, and Feature spelling.
`tc-scenario-guide.md` and `tc-design-guide.md` are already in context from Phase 2.1 — do not reload.

**3.2 Write.** Pull the rows to write — the Scope Summary and any findings log in the plan are Phase 2 work product, not input here:

```bash
grep -E '^\| *[0-9]+[a-z]? *\|' tasks/{KEY}/gen/tc-plan.md | grep -vE 'covered by|\| *gap *\||needs-clarification'
```

One block per row returned.

**3.3 Self-check.** After writing all TC blocks, extract the relevant rows and check every block against them — fix in place, never defer to review:

```bash
awk '/^\| *#/{p=1} p && /^\| *([3-8]|1[3-9]|20) /' .kiro/steering/qa-anti-patterns.md
```

**Done when:** every `new` row has exactly one TC block, each block carries every TEMPLATE field its case needs, each block's `Requirement Reference` repeats that row's Refs verbatim, and the self-check above passes for every block.

After writing, say: "[n] TCs written → tasks/{KEY}/gen/manual-tcs.md"

---

## Phase 4 — Self-review and coverage

**4.1 Review.** Invoke `review-tcs` with `{KEY}`, `no-gate`. It fixes TCs in place.

**4.2 Reconcile.** Count from the file, never from memory and never by re-reading it whole:

```bash
grep -c '^## ' tasks/{KEY}/gen/manual-tcs.md                            # TC count
grep '^\*\*Requirement Reference:\*\*' tasks/{KEY}/gen/manual-tcs.md    # AC/BR/ERR coverage
grep '^\*\*Priority:\*\*' tasks/{KEY}/gen/manual-tcs.md | sort | uniq -c  # 4.3 priority split
```

`new` row count == TC count, and every `new` row's `#` appears in exactly one TC — name a mismatch, never round it.

**4.3 Present only:**

```
Coverage — {KEY}    [n] TCs · High [n] / Med [n] / Low [n]
ACs [n]/[n]  BRs [n]/[n]  ERRs [n]/[n]
Self-review: [n] fixes applied · [n] ask items
Full detail → tasks/{KEY}/gen/tc-plan.md

Needs your input:
  [ref/id]  thin | gap | needs-clarification | ask   [one-line reason]
```

`thin` = High Business Criticality id with only a happy-path TC.

**GATE — stop until approved and every `ask` item is resolved or explicitly skipped.**

---

## Phase 5 — Export

Run the target confirmed in 1.7. No further stop.

- **Sheet** — spreadsheet id is `TC_SHEET_ID` in `project-config.md`; tab name from 1.7.
  ```
  .venv/bin/python3 scripts/format_tc_sheet.py \
    --md tasks/{KEY}/gen/manual-tcs.md \
    --sheet {TC_SHEET_ID} \
    --tab "{KEY}"
  ```

- **Testmo** — Invoke `to-testmo` with `{KEY}` and the Module folder confirmed in 1.7.

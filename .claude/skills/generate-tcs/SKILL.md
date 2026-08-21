---
name: generate-tcs
description: Generate manual test cases from a Jira ticket — scope ACs and BRs, plan coverage, write TCs, export to CSV, Sheet, or Testmo. Use when asked for test cases for a ticket, or when another skill needs `tasks/{KEY}/manual-tcs.md`.
---

# Generate Test Cases

**Done when:** every AC, BR, and error message traces to a written TC or to a recorded gap; every written TC carries every per-TC field in `tc-conventions.md § Output Format`; the confirmed export target is written.

## Contract

- **Args:** `{KEY}` [, path to an existing `jira.md`]
- **Invokes:** `jira-retriever` → `tasks/{KEY}/jira.md` + `tasks/{KEY}/attachments/`; `collect-testmo-cases` → `tasks/{KEY}/tc.md`; `grill-tcs` → updates `tc-plan.md`
- **Writes:** `tasks/{KEY}/tc-plan.md`, `tasks/{KEY}/manual-tcs.md`, plus the confirmed export target
- **Steering:** `tc-scenario-guide.md` (Phase 2), `tc-conventions.md` (Phase 3), `tc-priority-guide.md` (Phases 3–4)
- **Resumes at:** the first missing artifact; an existing one is re-presented, never silently rewritten

---

## Phase 1 — Scope

**1.1 Load the ticket.** Path given → read it. Otherwise → `Read .claude/skills/jira-retriever/SKILL.md` for `{KEY}` with `save`, then read `tasks/{KEY}/jira.md`.

**File-write rule (all phases):** Write files directly without proposing content in chat first. After each write, say "Written to `path` — check it and let me know if anything needs updating." Never dump the full file content in chat for review.

Harvest from the whole file: user flows, every BR-table row, every error validation message verbatim, the latest AC version, sprint scope and out-of-scope notes.

Ticket links to another issue describing shared/common behavior ("connects to", "relates to") → ask once whether to pull it into scope before Phase 2; a declined link is noted, never silently dropped.

Split every Out-of-Scope item into **feature-absence** (nothing to assert, e.g. "QR code scanning") or **restricted-capability** (an enforceable constraint, e.g. "editing wallet address details other than Nickname") — the latter gets a `new` row in the plan for a negative TC confirming the constraint holds.

**1.2 Number the scope.** Every AC → `AC-n`, every BR → `BR-n`, every error message → `ERR-n` holding the exact string. Extract prose ACs as conditions and number them the same way. No ACs in the ticket → derive them from the description and mark each `derived`.

**1.3 Existing TCs.** Ask once: `Check Testmo for existing TCs — ticket-linked (T) / whole Module folder (M) / none (N)?`

- T → `Read .claude/skills/collect-testmo-cases/SKILL.md` with `{KEY}`, `save`, `no-gate`.
- M → T, plus `testmo_list_cases` on the Module folder once 1.4 confirms it, names only. Duplicates from other tickets surface here and nowhere else.

Either way, skim retrieved TC titles for capabilities the ticket text never names (e.g. search, filter, an admin override) — surface each as a scope question in 1.4, not a silent gap. Ticket prose is never assumed complete; existing TCs are for gap-mining as well as dedup. Never invent an expected value from them without a ticket-side source — an unsourced value found only in Testmo is still `needs-clarification`.

**1.4 Present scope and Module.**

```
Scope — {KEY}    Module: [proposed]
[n] ACs · [n] BRs · [n] ERRs · Out of scope: [n items / none]
Full detail in tasks/{KEY}/jira.md

Confirm, or correct Module / scope:
```

**GATE — stop until scope and Module are confirmed.**

---

## Phase 2 — Plan coverage

Apply **sweep → match → cross-cut** from `tc-scenario-guide.md` to every numbered item in the scope. Write the plan to `tasks/{KEY}/tc-plan.md`, one row per scenario:

| # | Refs | Screen | Scenario | Type | Expected-value source | Status |

- **Refs** — every `AC-n` / `BR-n` / `ERR-n` the scenario covers. Every id from Phase 1 appears in at least one row; an id no scenario covers gets its own row with Status `gap` and the reason.
- **Expected-value source** — the AC, error-message row, live UI observation, or domain file the expected result comes from. No source → Status `needs-clarification` and no invented value.
- **Status** — `new`, `covered by [existing TC name]` (from 1.3), `gap`, or `needs-clarification`.

Then `Read .claude/skills/grill-tcs/SKILL.md` with `{KEY}`, `no-gate` — it grills every `new` row in `tc-plan.md` against Q1 source, Q2 negative, Q3 oracle, and hands back READY rows plus any moved to `needs-clarification`.

After writing the file, present only:

```
Plan written → tasks/{KEY}/tc-plan.md
[n] scenarios · [n] gap · [n] needs-clarification

Needs your input:
  [ref]  [one-line reason]   ← only gap / needs-clarification rows
```

**GATE — stop until the plan is confirmed.**

---

## Phase 3 — Write TCs

Write the file header (Story, Configuration) once at the top of `tasks/{KEY}/manual-tcs.md`, then one TC block per `new` row following the Output Format in `tc-conventions.md`. Omit header-level fields from individual TC blocks. Priority per `tc-priority-guide.md`. `Requirement Reference` carries that row's Refs. Configuration must match an exact Testmo config name — fetch via `testmo_list_configs` if not already known. Leave `covered by`, `gap`, and `needs-clarification` rows unwritten.

Every Expected Result lists all verifiable checkpoints as bullets — each checkpoint is an exact message, value, or state change that cannot pass on a wrong result.

After writing, say: "[n] TCs written → tasks/{KEY}/manual-tcs.md"

---

## Phase 4 — Coverage report

Count from the `Requirement Reference` fields in the written file, never from memory. Reconcile first: `new` row count == TC count, and every `new` row's `#` appears in exactly one TC — name a mismatch, never round it.

Present only:

```
Coverage — {KEY}    [n] TCs · High [n] / Med [n] / Low [n]
ACs [n]/[n]  BRs [n]/[n]  ERRs [n]/[n]
Full detail → tasks/{KEY}/tc-plan.md

Needs your input:
  [ref]  thin/gap/needs-clarification  [one-line reason]   ← only problem rows

Changes before exporting?
```

`thin` = High Business Criticality id with only a happy-path TC.

**GATE — stop until approved.**

---

## Phase 5 — Export

```
Export to:
  1. CSV — tasks/{KEY}/manual-tcs.csv
  2. Google Sheet — team template
  3. Testmo
  4. Any combination — "1,2" or "all"
```

**GATE — stop until the target is confirmed.**

Every target writes the column order in `tc-conventions.md`.

- **CSV** — `tasks/{KEY}/manual-tcs.csv`. Join steps with `\n` inside the cell.
- **Sheet** — append to the template in `project-config.md` (`TC_SHEET_ID`) via `mcp_google_docs_appendrows`.
- **Testmo** — `testmo_create_cases` under the confirmed Module folder, `<br>` for line breaks.

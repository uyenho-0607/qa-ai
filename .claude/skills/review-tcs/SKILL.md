---
name: review-tcs
description: Review a set of test cases for coverage gaps, weak oracles, non-reproducible steps, and convention violations, then apply the fixes. Use when asked to review or audit the TCs for a ticket, or given a TC sheet URL to check.
---

# Review TCs

**Done when:** every TC is graded on all four dimensions, every approved `fix` is applied to the source, and every `ask` finding is reported with its id.

## Contract

- **Args:** `{KEY}`, or a sheet URL [, tab name]
- **Reads:** TCs from `tasks/{KEY}/manual-tcs.md`, Testmo, or the sheet; scope from `tasks/{KEY}/tc-plan.md` or `tasks/{KEY}/jira.md`
- **Invokes**, each only when its local file is missing: `collect-testmo-cases` → `tasks/{KEY}/tc.md`; `jira-retriever` → `tasks/{KEY}/jira.md` + `tasks/{KEY}/attachments/`
- **Steering:** `tc-scenario-guide.md` + `tc-priority-guide.md` (Coverage), `tc-conventions.md` + `manual-qa-anti-patterns.md` (Form)
- **Updates:** the source in place — `tasks/{KEY}/manual-tcs.md`, or the sheet rows
- **Writes:** `tasks/{KEY}/tc-review.md`

---

## Phase 1 — Load TCs and scope

**1.1 TCs.**

- `{KEY}` given → read `tasks/{KEY}/manual-tcs.md`. Missing → `Read .claude/skills/collect-testmo-cases/SKILL.md` with `{KEY}`, `save`, `no-gate`, then read `tasks/{KEY}/tc.md`.
- Sheet URL given → read via `mcp_google_docs_readspreadsheet`, columns per `tc-conventions.md` § Order Export Columns. Parse every row into a TC; skip the header and empty rows.

**1.2 Scope.** Coverage is graded against the requirements, so load them: `tasks/{KEY}/tc-plan.md` if it exists, else `tasks/{KEY}/jira.md`, else `Read .claude/skills/jira-retriever/SKILL.md` for `{KEY}` with `save`. Number them `AC-n`, `BR-n`, `ERR-n` as in `generate-tcs` Phase 1.

No scope source available → ask once for the ticket key. Declined → grade the other three dimensions and report `Coverage: not checked — no scope source`.

---

## Phase 2 — Grade four dimensions

**Coverage** — the set against the scope, both directions. Map every `AC-n` / `BR-n` / `ERR-n` to the TCs covering it; an id with no TC is a `gap`. Apply sweep → match → cross-cut from `tc-scenario-guide.md` to name the mandatory scenarios the set is missing, including reverse transitions, cross-field dependencies, and reference-list scenarios the cross-cut rules require. Flag as `thin` any id whose Business Criticality is High in `tc-priority-guide.md` and whose only TC is a happy path. Flag **Missing Reverse Transition** (#14) when a forward status change is tested with no reverse TC or `needs-clarification` entry, and **Silent Scope Narrowing** (#15) when a broadly stated rule is tested against only one status/condition without a flag. Then the overlap side: duplicate TCs, 8+ TCs on one AC, and Desktop/Mobile pairs that `tc-conventions.md` consolidates into one.

**Oracle** — every Expected Result states one exact message, value, or state change, traces to an `AC-n` / `ERR-n` / live UI, and cannot pass on a wrong value. An Expected Result that contradicts its AC is a defect in the TC. The cited id's actual text must support the Expected Result — pull the cited row from the scope source and diff it; a citation that exists but doesn't match the claim (anti-pattern #13) is the same defect as no citation.

**Repro** — another tester executes the TC unaided: Pre-requisites state role and setup, Steps name the exact element, Test Data holds the exact, literal values (anti-pattern #16 — a description in place of a value fails this check even when the field isn't empty).

**Form** — every field populated per `tc-conventions.md`, and every TC checked against anti-patterns #1–#11 and #13–#16 in `manual-qa-anti-patterns.md`.

Record per finding: dimension, TC name, the exact field value as evidence, and the fix. Collect findings only — a passing check is counted, never recorded. Do not output grading work to chat — all detail goes into the review file only.

Grade every finding:

- `fix` — the correction is determinable from the scope or the conventions.
- `ask` — the correction needs the human: a coverage gap needing new TCs, or an expected value with no source.

---

## Phase 3 — Report → GATE

Write `tasks/{KEY}/tc-review.md`. Do not present the file contents in chat.

Then present only:

```
Review — [KEY / sheet]    [n] TCs · [n] findings (fix [n] · ask [n]) · [n] clean
Full detail → tasks/{KEY}/tc-review.md

Ask items needing your decision:
  [id]  [one-line description]
  ...

Apply the [n] fixes?
```

List only `ask` findings here. `fix` findings are self-contained — do not repeat them in chat.

**GATE — stop until approved.**

---

## Phase 4 — Apply

Apply every approved `fix` to the source in place. Leave `ask` findings untouched.

Coverage gaps the user wants written → hand the gap list to `generate-tcs` as the scope; it plans, grills, and writes them.

Confirm: "[n] fixes applied to [source]. [n] ask items left with you — see tasks/{KEY}/tc-review.md."

---

## Rules

- Quote the exact field value as evidence, never a paraphrase.
- Strengthen a weak check or clarify the requirement — never weaken a check to make a TC pass.
- Report a coverage gap even when the TC set is otherwise clean; a clean set with a missing negative is the most expensive finding here.

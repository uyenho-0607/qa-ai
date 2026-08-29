---
name: review-tcs
description: Review a set of test cases for coverage gaps, weak oracles, non-reproducible steps, and convention violations, then apply the fixes. Use when asked to review the TCs for a ticket, /review-tcs.
---

# Review TCs

**Done when:** every TC graded on all four dimensions, every approved `fix` applied to `tasks/{KEY}/gen/manual-tcs.md`, every `ask` finding reported with its id.

## Contract

| | |
|---|---|
| **Args** | `{KEY}` [, sheet URL] [, `no-gate`] |
| **TC source** | `tasks/{KEY}/gen/manual-tcs.md` → sheet URL → Testmo (first that resolves) |
| **Scope source** | `tasks/{KEY}/gen/tc-plan.md` → `tasks/{KEY}/base/jira.md` (first that resolves) |
| **Writes** | `tasks/{KEY}/gen/tc-review.md` — only when user confirms (format: `TEMPLATE.md`); `tasks/{KEY}/gen/manual-tcs.md` (fixes only). Nothing under `no-gate`. |
| **Output exists** | `tc-review.md` present → ask once: re-review \| reuse \| abort |

---

## Phase 1 — Load

**TCs.** First source that resolves:
- `tasks/{KEY}/gen/manual-tcs.md` exists → read it.
- Sheet URL given → invoke `collect-gsheet-cases` with `{KEY}`, URL, `no-gate` → read `tasks/{KEY}/base/tc.md`.
- Otherwise → dispatch the `testmo-collector` agent for `{KEY}` → read `tasks/{KEY}/base/tc.md`. No Agent tool in context → disclose_context("collect-testmo-cases") FULLY with `{KEY}`, `save`, `no-gate`.

TCs from `tc.md` → Phase 3 writes the corrected set to `manual-tcs.md`; source rows are never edited.

**Scope.** Neither `tasks/{KEY}/gen/tc-plan.md` nor `tasks/{KEY}/base/jira.md` present → dispatch the `jira-fetcher` agent for `{KEY}`. No Agent tool in context → disclose_context("jira-retriever") FULLY with `{KEY}`, `save`.

No `{KEY}` either → ask once for it. Declined → grade the other three dimensions; report `Coverage: not checked — no scope source`.

**Rules.** Load before grading — run every time, including when this session already read them:

```bash
cat .kiro/steering/tc-scenario-guide.md \
    .kiro/steering/tc-priority-guide.md \
    .kiro/steering/tc-conventions.md \
    .kiro/steering/tc-design-guide.md \
    .kiro/steering/qa-anti-patterns.md
```

---

## Phase 2 — Grade & Report → GATE

Grade all TCs against the four dimensions in one pass, then emit the report below.

| Dimension | Asks |
|---|---|
| **COVERAGE** | Does every scope id reach a TC, and does every TC reach a scope id? |
| **ORACLE** | Could the TC pass while the feature is broken? |
| **REPRO** | Can a tester who has never seen the ticket run these steps and reach that result? |
| **FORM** | Does the TC obey the conventions — name, scenario wording, ER bullets, priority, module? |

Apply every row except #12 of `qa-anti-patterns.md` and the grading rules in each row's fix-owner file. One finding per anti-pattern, no dimension filed twice.

Grade:
- `fix` — correction determinable from scope or conventions.
- `ask` — needs the human: coverage gap needing new TCs, or expected value with no source.

Present:

```
Review — {KEY}    [n] TCs · [n] findings (fix [n] · ask [n]) · [n] clean
```

**Fixes table** — one row per fix:

| TC | Why | Before | After |
|---|---|---|---|
| TC-nn | One sentence explaining the convention violated and why it matters. If another row in this table has the same Why, write "Same as TC-nn". | The exact current field value | The exact replacement text |

Chat report: TC id plus a plain sentence. Dimension codes and finding ids belong in `tc-review.md` only. Quote every field value in full.

**Ask table** — one row per ask:

| TC | Question |
|---|---|
| TC-nn | Plain-English question the human must answer before this TC can be fixed |

**Then ask** *(skip with `no-gate`, or when invoked by another skill — go straight to Phase 3)*:
```
Save full findings to tasks/{KEY}/gen/tc-review.md? (y/n)
Apply the [n] fixes?
```

No `yes` on the first question → `tc-review.md` is never written.

**File write.** Write `tasks/{KEY}/gen/tc-review.md` only on a yes. Immediately before writing, run `cat .kiro/skills/review-tcs/TEMPLATE.md` and write per that format. After writing: "Written to `tasks/{KEY}/gen/tc-review.md`."

**GATE — stop until approved.** *(skip the gate with `no-gate`, or when invoked by another skill)*

---

## Phase 3 — Apply

**`no-gate` — stop here.** Apply nothing, export nothing. Hand back every `fix` as the exact replacement text and every `ask` with its id, then report:

```
[n] fixes proposed. [n] ask items open. Caller applies.
```

Apply every approved `fix` to `tasks/{KEY}/gen/manual-tcs.md` per `generate-tcs/TEMPLATE.md`. Leave `ask` findings untouched. Strengthen a weak check — never weaken one to make a TC pass.

**TCs from `tc.md` only** (sheet or Testmo source) — convert field names on write:

| `tc.md` | `manual-tcs.md` |
|---|---|
| `Scenario` (sheet) · `Description` (Testmo) | `Test Scenario` |
| `Type` (sheet) | `Test Case Type` |
| Testmo — no `Type` field | `Test Case Type` derived from `tc-scenario-guide.md` § Scenario Types |
| `Prerequisites` (Testmo) | `Pre-requisites` |
| `Requirement Ref` (sheet) | `Requirement Reference` |
| Steps `Action` column (Testmo) | numbered `Steps:` |
| Steps `Expected Result` column (Testmo) | ER bullets prefixed `[N]` |
| `Module` (sheet) | drop |
| `Classification` (sheet) | drop |
| neither source emits it | `Configuration` — from the sheet's platform column, else ask |

Drop `Automation` and `State`. Testmo source: derive `Requirement Reference` from scope ids; no match → file `#6 Untraceable TC`. Coverage gaps → hand to `generate-tcs`.

**Re-export.** Only when the TCs already exist in a sheet — i.e. the run started from a sheet URL, or a previous export wrote the tab. Sheet id and tab come from the URL in Args, or ask the user for both. Patch changed IDs only; other rows untouched:

```
.venv/bin/python3 scripts/format_tc_sheet.py --md tasks/{KEY}/gen/manual-tcs.md --sheet {SHEET_ID} --tab "{TAB_NAME}" --patch-ids "{TC-ID-1},{TC-ID-2},..."
```

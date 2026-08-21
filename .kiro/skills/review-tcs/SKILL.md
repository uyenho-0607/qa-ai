---
name: review-tcs
description: Review a set of test cases for coverage gaps, weak oracles, non-reproducible steps, and convention violations, then apply the fixes. Use when asked to review the TCs for a ticket, /review-tcs.
---

# Review TCs

**Done when:** every TC graded on all four dimensions, every approved `fix` applied to `tasks/{KEY}/manual-tcs.md`, every `ask` finding reported with its id.

## Contract

| | |
|---|---|
| **Args** | `{KEY}` [, sheet URL] [, `no-gate`] |
| **TC source** | `manual-tcs.md` → sheet URL → Testmo (first that resolves) |
| **Scope source** | `tc-plan.md` → `jira.md` → invoke `jira-retriever` with `save` |
| **Writes** | `tasks/{KEY}/tc-review.md` — only when user confirms (format: `TEMPLATE.md`); `tasks/{KEY}/manual-tcs.md` (fixes only) |
| **Steering** | loaded in Phase 1 § Rules — that step names the files |
| **no-gate** | Called from `generate-tcs`. Grade → apply every `fix` → return counts; skip the Phase 2 gate, the `tc-review.md` write, and the Phase 3 re-export; report `ask` findings to the caller. Rule load at Phase 1: only `tc-scenario-guide.md` (caller owns the rest). When invoked standalone by a user, always use the default gate path — which loads the full steering set. |
| **Output exists** | `tc-review.md` present → ask once: re-review \| reuse \| abort |

---

## Phase 1 — Load

**TCs.** First source that resolves:
- `tasks/{KEY}/manual-tcs.md` exists → read it.
- Sheet URL given → invoke `collect-gsheet-cases` with `{KEY}`, URL, `no-gate` → read `tasks/{KEY}/tc.md`.
- Otherwise → invoke `collect-testmo-cases` with `{KEY}`, `save`, `no-gate` → read `tasks/{KEY}/tc.md`.

TCs from `tc.md` → Phase 3 writes the corrected set to `manual-tcs.md`; source rows are never edited.

**Scope.** No scope source → ask once for the ticket key. Declined → grade the other three dimensions; report `Coverage: not checked — no scope source`.

**Rules.** Load before grading — run every time, including when this session already read them.

`no-gate` — Load only tc-scenario-guide.md:

```bash
cat .kiro/steering/tc-scenario-guide.md
```

Otherwise load the full set:

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

Apply every row of `qa-anti-patterns.md` and the grading rules in each row's fix-owner file. One finding per anti-pattern, no dimension filed twice.

Grade:
- `fix` — correction determinable from scope or conventions.
- `ask` — needs the human: coverage gap needing new TCs, or expected value with no source.

Present:

```
Review — {KEY}    [n] TCs · [n] findings (fix [n] · ask [n]) · [n] clean
```

**Finding format rules** — apply to every finding in `tc-review.md`:
- One heading per dimension, in this order: COVERAGE, ORACLE, REPRO, FORM — present even when empty (write `No findings.`).
- Finding id runs per dimension: `COV-`, `ORA-`, `REP-`, `FORM-`, zero-padded to two digits.
- The heading is the only place the grade — `fix` or `ask` — appears.
- One `---` separator between findings.

**Fixes table** — one row per fix:

| TC | Why | Before | After |
|---|---|---|---|
| TC-nn | One sentence explaining the convention violated and why it matters. If another row in this table has the same Why, write "Same as TC-nn". | The exact current field value | The exact replacement text |

Chat report: TC id plus a plain sentence. Dimension codes and finding ids belong in `tc-review.md` only. Quote every field value in full.

**Ask table** — one row per ask:

| TC | Question |
|---|---|
| TC-nn | Plain-English question the human must answer before this TC can be fixed |

Then ask:
```
Save full findings to tasks/{KEY}/tc-review.md? (y/n)
Apply the [n] fixes?
```

**File write.** Write `tasks/{KEY}/tc-review.md` only on a yes. Format per `TEMPLATE.md`. After writing: "Written to `tasks/{KEY}/tc-review.md`."

**GATE — stop until approved.** *(skip the gate with `no-gate`, or when invoked by another skill)*

---

## Phase 3 — Apply

Apply every approved `fix` to `tasks/{KEY}/manual-tcs.md` per `generate-tcs/TEMPLATE.md`. Leave `ask` findings untouched. Strengthen a weak check — never weaken one to make a TC pass.

**TCs from `tc.md` only** (sheet or Testmo source) — convert field names on write:

| `tc.md` | `manual-tcs.md` |
|---|---|
| `Scenario` (sheet) · `Description` (Testmo) | `Test Scenario` |
| `Type` | `Test Case Type` |
| `Prerequisites` (Testmo) | `Pre-requisites` |
| `Requirement Ref` (sheet) | `Requirement Reference` |
| Steps `Action` column | numbered `Steps:` |
| Steps `Expected Result` column | ER bullets prefixed `[N]` |

Drop `Automation` and `State`. Testmo source: derive `Requirement Reference` from scope ids; no match → file `#6 Untraceable TC`. Coverage gaps → hand to `generate-tcs`.

**Re-export.** Only when the TCs already exist in a sheet — i.e. the run started from a sheet URL, or a previous export wrote the tab. Patch changed/added IDs only; other rows untouched:

```
.venv/bin/python3 scripts/format_tc_sheet.py --md tasks/{KEY}/manual-tcs.md --sheet {SHEET_ID} --tab "{TAB_NAME}" --patch-ids "{TC-ID-1},{TC-ID-2},..."
```

Under `no-gate` the caller exports — stop after applying fixes and report:

```
[n] fixes applied. [n] ask items open. [n] TCs patched in sheet (omit when nothing was patched).
```

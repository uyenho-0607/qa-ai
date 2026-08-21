---
name: generate-test-cases
description: Generate manual test cases from a Jira ticket. Use when user says "generate test cases", "create TCs", "what should I test for", or provides a ticket key.
---

# Generate Test Cases

Done when every AC has at least one TC, all 7 mandatory fields are populated, coverage report is presented, and the human has confirmed the list.

**Required reads:** `.kiro/steering/tc-conventions.md`, `.kiro/steering/tc-priority-guide.md`, `.kiro/steering/tc-scenario-guide.md`

## Flow

### Phase 1 — Fetch & Scope → GATE

**1.1** `disclose_context("jira-retriever")` — run fully for `<ticket-key>`, save mode. Extract: summary, ACs, linked issues, attachments.

**1.2 Handle ACs**

If ACs are structured (numbered list) → use as-is.

If ACs are unstructured prose → extract implicit conditions, number them, present for confirmation:
```
ACs extracted from description for [TICKET-KEY]:
  AC-1: [extracted condition]
  AC-2: [extracted condition]
Confirm or correct before proceeding:
```

If no ACs exist → block:
```
No ACs found in [TICKET-KEY].
Provide ACs, or confirm I should derive them from the description:
```
**STOP. Wait for AC confirmation in both unstructured and missing cases.**

**1.3 Testmo check (optional)**
```
Check Testmo for existing TCs for [TICKET-KEY]? (Y/N)
```
- Y → `disclose_context("collect-testmo-cases")` with save
- N → proceed

**1.4 Propose Module**
```
Module for [TICKET-KEY]: [Proposed Module]
Reason: [why this module was chosen]
Confirm or provide correct module:
```
**STOP. Wait for Module confirmation.**

---

### Phase 2 — Coverage Plan → GATE

Read each AC. Match to patterns in `tc-scenario-guide.md`. List mandatory and optional scenario types per AC.
```
Coverage plan for [TICKET-KEY]:

AC-1: [summary]
  Pattern: [matched pattern(s)]
  Mandatory: [list]
  Optional: [list]
...
Confirm or adjust:
```
**STOP. Wait for coverage confirmation before writing any TC.**

---

### Phase 3 — Generate TCs → GATE

For each confirmed scenario, write the TC with all 7 mandatory fields per `tc-conventions.md`.

Read `tc-priority-guide.md`. Score each TC. Present all Priority proposals together:
```
Priority assignments:
- "[TC Name]": High — [reason]
- "[TC Name]": Medium — [reason]
...
Confirm or update:
```
**STOP. Wait for priority confirmation.**

---

### Phase 4 — Coverage Report & Review → GATE

Present coverage report, then the full TC list:

```
Coverage: [TICKET-KEY]  ✓ [n]/[n] ACs · [n] TCs · High [n] / Med [n] / Low [n]

  AC-1  [✓/✗]  [AC summary]          [n] TCs
  AC-2  [✓/✗]  [AC summary]          [n] TCs
  ...

  Types: [scenario types used, comma-separated]
  Gaps:  [AC summaries with no TC, else "none"]
```

Then list each TC:

```
TCs:
  1. [Name] — [Scenario] | [Priority]
  2. [Name] — [Scenario] | [Priority]
  ...
```

```
Changes before exporting?
```
**STOP. Wait for approval.**

---

### Phase 5 — Export → GATE

Ask once:
```
Export to:
  1. Local CSV  (tasks/[KEY]/manual-tcs.csv)
  2. Google Sheet  (team template)
  3. Testmo
  4. Multiple — pick any combination (e.g. "1,2" or "all")
```

**CSV export**
Write to `tasks/[KEY]/manual-tcs.csv`.
Columns: `Test ID,Module,Name,Test Scenario,Test Case Type,Pre-requisites,Steps,Test Data,Expected Result,Priority,Requirement Reference,Login Method,Configuration,Story,Automation`
- Join multi-step steps with `\n` inside the Steps cell.
- Test ID format: `[TICKET-KEY]_TC-[nn]`
- Leave Test Case Type, Test Data, Login Method, Automation blank unless determinable from AC.
- Set Requirement Reference to the AC identifier (e.g. `AC-1; AC-2`).

**Sheet export**
Write to team TC template sheet (ID from `project-config.md`) using `mcp_google_docs_appendrows`.
Same column order and cell rules as CSV export.

**Testmo export**
`testmo_create_cases` per TC under confirmed Module folder.

**STOP. Confirm export target before writing.**

---

## Rules
- Read and confirm ACs before generating any TC — source every TC to its AC
- Confirm Module before Phase 2 — propose with reasoning, never invent
- Exclude login from Steps unless the TC spans multiple platforms
- State proposal + reasoning at every gate — never a bare yes/no prompt
- Gate every export action — both Sheet write and Testmo push are irreversible

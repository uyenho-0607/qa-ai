---
name: review-tcs
description: Review test cases against manual QA anti-patterns. Use when user says "review TCs", "check TCs for OMS-XXX", "audit test cases", or provides a sheet URL to review.
---

# Review TCs

Done when every TC is checked against all 12 anti-patterns and all violations are reported.

**Required reads:** `.kiro/steering/manual-qa-anti-patterns.md`, `.kiro/steering/tc-conventions.md`

## Flow

### Phase 1 — Fetch TCs → GATE

Determine input source:

**Source A — Jira key (Testmo)**
`disclose_context("collect-testmo-cases")` with `no-gate` and `save`.
Read `tasks/{KEY}/tc.md` after completion.

**Source B — Google Sheet URL**
Ask for the sheet URL and tab name if not provided.
Read the sheet directly via `mcp_google_docs_readspreadsheet`.
Column order: `Test ID | Module | Name | Test Scenario | Test Case Type | Pre-requisites | Steps | Test Data | Expected Result | Priority | Requirement Reference | Login Method | Configuration | Story | Automation`
Parse every row into a TC object. Skip header and empty rows.

Present source confirmation:
```
Source: [Testmo / Google Sheet]
TCs found: [n] across [n] modules
Proceed with review? (Y/N)
```
**STOP. Wait for confirmation.**

---

### Phase 2 — Run Anti-Pattern Check

For each TC, check all 12 anti-patterns from `manual-qa-anti-patterns.md`.

Collect only violations — skip passing checks entirely.

Per violation record:
- TC ID / Name
- Anti-pattern number and name
- Evidence (exact field value that triggered it)

---

### Phase 3 — Report → GATE

Present violations grouped by anti-pattern, not by TC:

```
Review: [KEY / Sheet name]  [n] TCs checked · [n] violations found

  #3 Vague Expected Result ([n] TCs)
    - [TC Name]: "[exact vague text found]"
    - [TC Name]: "[exact vague text found]"

  #4 Step in Scenario Title ([n] TCs)
    - [TC Name]: "[scenario text]"

  #11 Priority Not Assigned or Inflated ([n] TCs)
    - [TC Name]: Priority = High (boundary scenario)

  Clean: [n] TCs passed all checks
```

If no violations:
```
Review: [KEY / Sheet name]  [n] TCs checked · 0 violations  ✓ All clean
```

```
Export violation report? (Y/N)
```

---

### Phase 4 — Export (optional)

If Y:
- Save to `tasks/[KEY]/tc-review.md`
- Ask: "Post summary comment to Jira ticket? (Y/N)"
  - Y → `disclose_context("jira-handler")` action: `post_comment` with violation summary

## Rules
- Report violations only — do not list TCs that passed
- Group by anti-pattern, not by TC — makes patterns visible across the set
- State exact field value as evidence — never paraphrase
- Never modify the TCs — review only

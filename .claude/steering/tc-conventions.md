---
inclusion: manual
---

# Test Case Conventions

## Name Test Cases

Format: `[Module] - [Feature] - [Field] - [Condition]`

- Include Module and Condition in every name.
- Omit Feature and Field when not applicable.
- Use no abbreviations unless commonly understood in the project.
- Reflect the expected outcome in the name.

## Write Test Scenarios

Start every Test Scenario with "Verify that". Omit UI action verbs: click, enter, navigate, select, fill, submit.

```
✔ Verify that deposit with a valid amount is processed successfully.
✔ Verify that the minimum deposit validation is enforced.
✗ Users can navigate to Funds > Deposit and enter an amount and click Submit.
✗ Verify login and deposit flow works end to end.
```

## Write Expected Results

State all verifiable checkpoints as a bullet list. Each bullet names an exact message, value, or state change. Omit vague outcomes, implementation details, and alternatives joined by "or".

```
✔ - Error message displayed: "Amount must be at least 10"
✔ - Deposit reflected in account balance immediately
✔ - Button label changes to "Processing"
✗ - System works correctly.
✗ - API returns success.
✗ - An error or restricted-access message is displayed.
```

## Assign Platform and Role

Exclude login from Steps for all TCs. Exception: include login in Steps only when the TC requires logging into multiple platforms.

- Place platform in **Configuration** — use the exact Testmo config name for the project; never free-text. Fetch config names via `testmo_list_configs` if unknown.
- Place user role in **Pre-requisites** (e.g. "Logged in as Admin").
- State role clearly without over-specifying credentials.

## Output Format

Write a file header once, then one block per TC separated by `---`. Write every field in the block; omit nothing except where noted.

**File header:**
```
# Manual Test Cases — {KEY}
**Story:** {KEY}  **Configuration:** [platform]
```

**Per-TC block — write only these fields, in this order** (`#` notes are rules, not content):
```
## {KEY}_TC-nn
**Name:** ...                   # format per § Name Test Cases
**Test Scenario:** ...          # one scenario, per § Write Test Scenarios
**Test Case Type:** ...         # one type from tc-scenario-guide.md
**Pre-requisites:** ...         # user role and any required setup
**Steps:**                      # numbered; executable without extra context; stop at the first assertion
1. ...
**Test Data:** ...              # exact copy-pasteable values (`0x742d35Cc...`, not "a valid ETH address";
                                #   `AAAA…A (101 chars)`, not "a 101-character string");
                                #   omit this line entirely when the TC needs none
**Expected Result:**            # per § Write Expected Results
- ...
- ...
**Priority:** ...               # High / Medium / Low per tc-priority-guide.md
**Requirement Reference:** ...  # every id the TC covers, e.g. AC-1; BR-3; ERR-2
```

**Header-level fields — never write them in a TC block:** `Story`, `Configuration`, `Automation`, `Login Method`.
Exception: write `**Login Method:**` inline on a TC only when it spans multiple platforms.

At export time, backfill `Story`, `Configuration`, `Automation` (blank), `Login Method` (blank unless set), and `Test Data` (blank unless set) into every row from the header values.

## Consolidate Cross-Platform TCs

Consolidate TCs with identical scenarios on Desktop and Mobile into one TC. State platform-specific expected results within the same TC.

## Order Export Columns

Every export — CSV, Google Sheet, Testmo — writes this column order:

`Test ID,Module,Name,Test Scenario,Test Case Type,Pre-requisites,Steps,Test Data,Expected Result,Priority,Requirement Reference,Login Method,Configuration,Story,Automation`

Test ID format: `{KEY}_TC-[nn]`.

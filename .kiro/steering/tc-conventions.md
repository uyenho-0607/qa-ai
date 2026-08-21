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

## Populate Mandatory Fields

Every TC must contain all 7 fields. Reject any TC with a missing field.

| Field | Constraint |
|---|---|
| **Name** | Follows naming format above |
| **Test Scenario** | Starts with "Verify that". Contains no UI action verbs. |
| **Pre-requisites** | States user role and any required setup. |
| **Steps** | Numbered. Executable by any tester without additional context. |
| **Expected Result** | Describes what the tester sees on screen. |
| **Priority** | High / Medium / Low — determined per `tc-priority-guide.md`. |
| **Story** | Jira ticket key (e.g. OMS-1234). |

## Write Test Scenarios

Start every Test Scenario with "Verify that". Omit UI action verbs: click, enter, navigate, select, fill, submit.

```
✔ Verify that deposit with a valid amount is processed successfully.
✔ Verify that the minimum deposit validation is enforced.
✗ Users can navigate to Funds > Deposit and enter an amount and click Submit.
✗ Verify login and deposit flow works end to end.
```

## Write Expected Results

Describe what the tester sees on screen. Omit vague outcomes and implementation details.

```
✔ Error message displayed: "Amount must be at least 10"
✔ Deposit is reflected in account balance immediately.
✗ System works correctly.
✗ API returns success.
✗ The feature behaves as expected.
```

## Assign Platform and Role

Exclude login from Steps for all TCs. Exception: include login in Steps only when the TC requires logging into multiple platforms.

- Place platform in **Configuration** (e.g. "OMS Admin", "EMS Trader").
- Place user role in **Pre-requisites** (e.g. "Logged in as Admin").
- State role clearly without over-specifying credentials.

## Consolidate Cross-Platform TCs

Consolidate TCs with identical scenarios on Desktop and Mobile into one TC. State platform-specific expected results within the same TC.

## Confirm Module Before Generating

Propose a Module based on the Jira ticket. Wait for human confirmation. Use this gate format:

```
Module for [TICKET-KEY]: [Proposed Module]
Reason: [why this module was chosen]
Confirm or provide correct module:
```

## Handle Unstructured ACs

Extract implicit conditions from prose ACs as a numbered list. Present to the human for confirmation before generating any TC.

Block and wait when no ACs exist — generate no TCs until the human provides or confirms derived ACs.

## Check for Duplicates

Ask once before generating: "Check Testmo for existing TCs? (Y/N)". Proceed on either answer.

## Assign Priority

Determine Priority from `tc-priority-guide.md`. Propose with reasoning. Wait for human confirmation before finalising.

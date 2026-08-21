---
inclusion: manual
---

# Manual QA Anti-Patterns

| # | Anti-Pattern | Signs | Fix owner |
|---|---|---|---|
| 1 | **Happy Path Only** | No negative, boundary, or validation TCs for a feature; all TCs pass on first run | `tc-scenario-guide.md` |
| 2 | **Over-Granular TCs** | 8+ TCs for one AC; each TC tests a single word or label change; one scenario type repeated per field where fields share identical validation rules; one "field is optional" TC per optional field | `tc-scenario-guide.md` |
| 3 | **Vague Expected Result** | Expected Result contains "works correctly", "as expected", "success", "system responds" | `tc-conventions.md` |
| 4 | **Step in Scenario Title** | Scenario contains click, enter, navigate, select, fill, or submit | `tc-conventions.md` |
| 5 | **Login in Steps** | Step 1 or Step 2 is "Login to [platform]" on a non-multi-platform TC | `tc-conventions.md` |
| 6 | **Untraceable TC** | Story field empty; Requirement Reference empty | `tc-conventions.md` |
| 7 | **Missing Precondition** | Steps assume account exists, feature is enabled, or user is in a specific state — not stated in Pre-requisites | `tc-conventions.md` |
| 8 | **Non-Reproducible Steps** | Steps say "click the button", "go to the page", "enter a value" without naming the specific element; Test Data empty while a step needs a value | `tc-conventions.md` |
| 9 | **Invented Module, Sub-module, or Feature** | Name segment does not appear verbatim in `tc-naming-ref.md`; or Module does not match an existing Testmo folder | `tc-conventions.md` |
| 10 | **Duplicate TC** | Same scenario exists under a different name or ID in the same module | `tc-conventions.md` |
| 11 | **Priority Not Assigned or Inflated** | Priority field empty; or every TC in a set is High regardless of scenario type | `tc-priority-guide.md` |
| 12 | **Blocking Bug Not Linked** | TC status is Failed or Blocked; no Jira bug ID linked in the result | `bug-conventions.md` |
| 13 | **Orphaned Assertion** | Expected Result doesn't match the text of the AC/BR/ERR id it cites | `tc-scenario-guide.md` |
| 14 | **Missing Reverse Transition** | A forward state transition (e.g. Enabled→Disabled) is tested; no TC and no `needs-clarification` entry addresses the reverse | `tc-scenario-guide.md` |
| 15 | **Silent Scope Narrowing** | A rule stated broadly in the ticket (e.g. "unique per member") is tested against only one status/condition with no flag | `tc-scenario-guide.md` |
| 16 | **Descriptive Test Data** | Test Data reads as a description ("a valid ETH address", "a 101-character string") instead of a literal value the tester can copy | `tc-conventions.md` |
| 17 | **Redundant Intermediate TC** | TC asserts only a state a later TC in the same set passes through | `tc-design-guide.md` |
| 18 | **Multi-Path Steps** | One TC's steps bundle two distinct test paths | `tc-design-guide.md` |
| 19 | **Wrong Module** | TC navigates to BO but sits in an app-side module | `tc-design-guide.md` |
| 20 | **Wrong Pre-req Anchor** | Screen anchor is not the immediately preceding flow step; or Step 1 navigates to the screen the Pre-requisites already place the user on | `tc-design-guide.md` |
| 21 | **Missing Allowed-Case Complement** | A uniqueness or limit constraint is tested only where it blocks — e.g. blocked on (A+B) with no TC for same-A/different-B or different-A/same-B being allowed | `tc-scenario-guide.md` |

#1–#11, #13–#21 grade a TC set. #12 grades a run result.

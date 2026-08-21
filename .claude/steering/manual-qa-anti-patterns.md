---
inclusion: manual
---

# Manual QA Anti-Patterns

| # | Anti-Pattern | Signs | Fix owner |
|---|---|---|---|
| 1 | **Happy Path Only** | No negative, boundary, or validation TCs for a feature; all TCs pass on first run | `tc-scenario-guide.md` |
| 2 | **Over-Granular TCs** | 8+ TCs for one AC; each TC tests a single word or label change | `tc-scenario-guide.md` |
| 3 | **Vague Expected Result** | Expected Result contains "works correctly", "as expected", "success", "system responds" | `tc-conventions.md` |
| 4 | **Step in Scenario Title** | Scenario contains click, enter, navigate, select, fill, or submit | `tc-conventions.md` |
| 5 | **Login in Steps** | Step 1 or Step 2 is "Login to [platform]" on a non-multi-platform TC | `tc-conventions.md` |
| 6 | **Untraceable TC** | Story field empty; Requirement Reference empty | `tc-conventions.md` |
| 7 | **Missing Precondition** | Steps assume account exists, feature is enabled, or user is in a specific state — not stated in Pre-requisites | `tc-conventions.md` |
| 8 | **Non-Reproducible Steps** | Steps say "click the button", "go to the page", "enter a value" without naming the specific element; Test Data empty while a step needs a value | `tc-conventions.md` |
| 9 | **Invented Module** | Module name does not match any existing Testmo folder | `tc-conventions.md` |
| 10 | **Duplicate TC** | Same scenario exists under a different name or ID in the same module | `tc-conventions.md` |
| 11 | **Priority Not Assigned or Inflated** | Priority field empty; or every TC in a set is High regardless of scenario type | `tc-priority-guide.md` |
| 12 | **Blocking Bug Not Linked** | TC status is Failed or Blocked; no Jira bug ID linked in the result | `bug-conventions.md` |
| 13 | **Orphaned Assertion** | Expected Result doesn't match the text of the AC/BR/ERR id it cites | `tc-scenario-guide.md` |
| 14 | **Missing Reverse Transition** | A forward state transition (e.g. Enabled→Disabled) is tested; no TC and no `needs-clarification` entry addresses the reverse | `tc-scenario-guide.md` |
| 15 | **Silent Scope Narrowing** | A rule stated broadly in the ticket (e.g. "unique per member") is tested against only one status/condition with no flag | `tc-scenario-guide.md` |
| 16 | **Descriptive Test Data** | Test Data reads as a description ("a valid ETH address", "a 101-character string") instead of a literal value the tester can copy | `tc-conventions.md` |
| 17 | **Over-Coverage by Repetition** | Same scenario type applied per field when fields share identical validation rules; optional fields each get their own "field is optional" TC instead of one consolidated case | `tc-scenario-guide.md` |

#1–#11, #13–#17 grade a TC set. #12 grades a run result.

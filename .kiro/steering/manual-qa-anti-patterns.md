---
inclusion: manual
---

# Manual QA Anti-Patterns

Detection index for TC and test session review. Each row names the smell, signs to detect it, and the file that owns the fix.

| # | Anti-Pattern | Signs | Fix owner |
|---|---|---|---|
| 1 | **Happy Path Only** | No negative, boundary, or validation TCs for a feature; all TCs pass on first run | `tc-scenario-guide.md` |
| 2 | **Over-Granular TCs** | 8+ TCs for one AC; each TC tests a single word or label change | `tc-scenario-guide.md` |
| 3 | **Vague Expected Result** | Expected Result contains "works correctly", "as expected", "success", "system responds" | `tc-conventions.md` |
| 4 | **Step in Scenario Title** | Scenario contains click, enter, navigate, select, fill, or submit | `tc-conventions.md` |
| 5 | **Login in Steps** | Step 1 or Step 2 is "Login to OMS/EMS" on a non-multi-platform TC | `tc-conventions.md` |
| 6 | **Untraceable TC** | Story field empty; no AC reference; TC cannot be linked to a requirement | `tc-conventions.md` |
| 7 | **Missing Precondition** | Steps assume account exists, feature is enabled, or user is in a specific state — not stated in Pre-requisites | `tc-conventions.md` |
| 8 | **Non-Reproducible Steps** | Steps say "click the button", "go to the page", "enter a value" without naming the specific element or value | `tc-conventions.md` |
| 9 | **Invented Module** | Module name does not match any existing Testmo folder | `tc-conventions.md` |
| 10 | **Duplicate TC** | Same scenario exists under a different name or ID in the same module | `tc-conventions.md` |
| 11 | **Priority Not Assigned or Inflated** | Priority field empty; or every TC in a set is High regardless of scenario type | `tc-priority-guide.md` |
| 12 | **Blocking Bug Not Linked** | TC status is Failed or Blocked; no Jira bug ID linked in the result | `bug-conventions.md` |

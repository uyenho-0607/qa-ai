# Manual Test Cases — {KEY}
**Story:** {KEY}  **Configuration:** [Testmo config name, e.g. Android app; iOS app]

---

## {KEY}_TC-nn
**Name:** [Module] – [Sub-module] – [Feature] – [Field/Action] – [Condition]
**Test Scenario:** Verify that ...
**Test Case Type:** [Happy Path | Validation | Boundary | Negative | ...]
**Pre-requisites:** [User role and any required setup state]
**Steps:**
1. [Action]
2. [Action]
3. [Action]
**Test Data:** [Exact copy-pasteable value, e.g. `Singapore`]
**Expected Result:**
- [1] [Single checkpoint for step 1]
- [3] [First checkpoint for step 3]
- [3] [Second checkpoint for step 3 — multiple bullets share the same [N]]
**Priority:** High | Medium | Low
**Requirement Reference:** AC-1; BR-2; ERR-1

---

## Notes

- `**Name:**` — Module, Sub-module, and Feature are copied verbatim from `.kiro/domain/tc-naming-ref.md`. Omit Sub-module when the Module has none.
- File header (`Story`, `Configuration`) written once — never repeat in TC blocks.
- `**Test Data:**` — omit the field entirely when the TC needs none.
- `**Expected Result:**` — every bullet prefixed `[N]` where N is the step number it follows. Steps with no checkpoint get no bullet.
- `**Login Method:**` — write inline only when the TC spans multiple platforms.
- One TC block per `---` separator.
- `## {KEY}_TC-nn` — the block heading is the Test ID. In a file written for `--insert-md`, a new TC may use `## {KEY}_TC-INSERT`; the insert renumbers it in place.

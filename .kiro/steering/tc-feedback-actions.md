---
inclusion: manual
---

# TC Feedback Actions

The action taxonomy for reviewer feedback on test cases — the same five whatever system the feedback arrives in and whatever system holds the cases. `apply-sheet-feedback` applies them to a Google Sheet; `apply-jira-feedback` applies them to Testmo.

Read `tc-design-guide.md` before classifying.

| Action | When |
|---|---|
| **delete** | "remove", "can remove", "delete", "covered by", "same as TC-XX" — the TC or its content should go entirely |
| **update** | The comment corrects an ER, pre-req, module, steps, name, or scenario — the TC stays, its content changes |
| **add** | "need to add", "missing", "add a case" — a new TC must exist |
| **defer** | The comment points at another ticket, or says another ticket handles it — record it, act on nothing |
| **ask** | The fix cannot be determined without a human — carry it forward as the question it is |

A comment about duplication classifies as `delete`; one about missing coverage as `add`. The merge/split rules in `tc-design-guide.md` decide which.

One comment thread yields one row. A thread carrying two distinct asks yields two.

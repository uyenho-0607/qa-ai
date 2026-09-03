---
inclusion: manual
---

# TC Feedback Actions

The action taxonomy for reviewer feedback on test cases — the same five whatever system the feedback arrives in and whatever system holds the cases.

| Action | When |
|---|---|
| **delete** | "remove", "can remove", "delete", "covered by TC-XX", "same as TC-XX" — the TC or its content should go entirely |
| **update** | The comment corrects an ER, pre-req, module, steps, name, or scenario — the TC stays, its content changes |
| **add** | "need to add", "missing", "add a case" — a new TC must exist |
| **defer** | The comment points at another ticket, says another ticket handles it, or reads "covered by {another ticket}" — record it, act on nothing |
| **ask** | The fix cannot be determined without a human — carry it forward as the question it is |

Borderline calls — duplication vs update, merge vs split — are decided by the rules in `.kiro/steering/tc-design-guide.md`.

One comment thread yields one row. A thread carrying two distinct asks yields two.

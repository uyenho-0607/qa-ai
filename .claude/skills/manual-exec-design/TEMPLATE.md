# SIT Execution — {Feature} {Build}

## Execution Context

- Environment: SIT
- Build: {build_number | unknown}
- Platform: Web
- Ticket: {KEY}
- Created: {YYYY-MM-DD}
- Executing account: {username} / {password}
- Target account(s): {username} / {password}
- Environment deviations: {what recon left changed, or "none"}

**Statuses:** PENDING | PASSED | FAILED | BLOCKED | SKIPPED
**Evidence path:** `evidence/{KEY}/{File}` — `{File}` is the Evidence Groups table's File column.

---

## Execution Plan

### Evidence Groups

> Every TC in a group shares **one** evidence file. A VIDEO group is one continuous recording; a SCREENSHOT group is one frame carrying every member's label.

| Group | TCs | Evidence Type | File | Rationale |
|---|---|---|---|---|
| {G1} | {TC-IDs} | {SCREENSHOT\|VIDEO} | TC_{ids}_{slug}.{png\|mp4} | {reason} |

### Waves

| Wave | Groups / TCs | Contexts | Note |
|---|---|---|---|
| Wave 1 | {groups} | {1\|2} | {why this order, or why 2 sessions are needed} |

---

## Results Summary

> Case ID is the ID `tc.md` carries — the Testmo case ID from `collect-testmo-cases`, or the sheet TC ID from `collect-gsheet-cases`.

| TC | Case ID | Title | Status | Bug |
|---|---|---|---|---|
| TC-01 | {case id from tc.md} | {title} | PENDING | — |
| TC-02 | {case id from tc.md} | {title} | PENDING | — |

---

## Skipped

| TC | Case ID | Title | Reason |
|---|---|---|---|
| {TC-ID} | {case id from tc.md} | {title} | {classification reason} |

---

## Locators Reference

| Element | data-testid | Source |
|---|---|---|
| {element} | `{testid}` | {domain file \| locator-cache \| live scan} |

---

## Test Cases

> One block per TC. Every field is a single bolded key on its own line — no `####` headings, no `---`
> separators. **Omit a line entirely rather than writing a placeholder**: no `Pre:` when the TC continues
> from the previous one, no `Data:`/`Teardown:` when there is nothing to state.

### {TC-ID} — {Title} ({case id from tc.md})
**Pre:** {precondition} — omit when it continues from the previous TC
**Data:** {field}: `{value}`; {field}: `{value}` — omit when none
**Steps:**
1. {step}
**Exp:**
- {separately checkable assertion tied to a DOM fact}
**Ev:** {group ID} | {TC-ID} | {what is being verified}
**Cap:** {what confirms it, at what moment} — VIDEO groups only; a SCREENSHOT group's frame is self-evident
**R:** PENDING · —
**Teardown:** {restore step} — omit when nothing to restore

Field rules:

- `**Ev:**` — the group ID alone. Type, file name, shared members and full path all come from the Evidence
  Groups table; never repeat them per TC. A solo TC has no group row, so it writes
  `**Ev:** solo {SCREENSHOT|VIDEO} `TC_{id}_{slug}.{png|mp4}` | {TC-ID} | {what is being verified}`.
  Every file name follows `references/evidence-rules.md` § Naming — it lists every member TC-ID.
- `**R:**` — written at step 4, before evidence is captured. One line, `·`-separated:
  `**R:** {STATUS} · {YYYY-MM-DD HH:MM} · {BUG-ID, omit when none} · {notes}`
  Notes carry observed-vs-expected on a failure, the blocker on a block, and any locator change.
  The evidence path is not repeated here — it is the group's file.
- Assertions state what is checked, not why it matters. Design rationale belongs in the GATE discussion.

# The shape of `report-v2.md`

Phase 3 writes `tasks/{KEY}/exec/report-v2.md` to the shape below. Every section is required unless its own note
says when to omit it.

**Written for a human first.** This is what a lead reads to decide whether the ticket ships. Platform labels
come from `project-config.md` § Platforms — never raw ids.

Sections that already exist in `exec-v2.md` are **linked, not copied**. Duplicating them costs tokens and
creates two versions of one fact.

---

# SIT Report — {Feature} {Build}

- **Ticket** — {KEY}
- **Executed** — {earliest result timestamp} → {latest}
- **Environment** — {SIT | UAT}
- **Platforms** — {labels}, detail in `exec-v2.md` § Preflight
- **Plan** — `tasks/{KEY}/exec/exec-v2.md`

---

## Summary

| | Total | ✅ Passed | ❌ Failed | 🚫 Blocked | Skipped |
|---|---|---|---|---|---|
| {platform label} | | | | | |
| {platform label} | | | | | |
| **All** | | | | | |

> Verified at recon: {n} TCs. Executed in waves: {n}.

---

## Result by test case

> One row per TC per platform. Generated from the result lines in `exec-v2.md` — this is the only place a
> summary table is written.

| TC | Case ID | Title | Platform | Result | Bug |
|---|---|---|---|---|---|
| {TC id} | {case id} | {title} | {label} | ✅ PASSED | — |

---

## Bugs Found

> Candidate defects from this run. **Not filed** — raise them with `report-bug` after review. One row per
> defect, naming every platform it reproduced on; a defect seen on one platform only is still one row.
> **This table is the only place in this file that carries a bug key.**

| TC | Platforms | What is wrong | Repro | Backend | Evidence | Bug |
|---|---|---|---|---|---|---|
| {TC id} | {labels} | {the defect} | {2/2 \| 1/2} | {status and values \| not checked} | {file name} | — |

## Rejected Candidates

> Failures reviewed and judged not to be defects. Omit while none exist.

| TC | Why it is not a defect |
|---|---|

---

## Failed & Blocked

> One entry per failed or blocked TC. This is what `report-bug` classifies from, so it carries every signal
> the run produced and leaves nothing in `exec-v2.md`.

### {TC id} · {Title} — ❌ FAILED on {platform labels}

**Expected** — {the entry from the plan, verbatim}
**Observed** — {label}: {what was seen} · {label}: {what was seen}
**Repro** — {2/2 | 1/2 — intermittent}
**Backend** — {status and compared field values | not checked}
**Signals** — {crash id | console errors | none}
**Evidence** — {file names}
**Reading** — {product defect | environment | data | plan error}, and why

---

## Platform Differences

> Behaviour present on one platform and absent or different on another. A single-platform run writes *None*.

| What | {platform label} | {platform label} | Reading |
|---|---|---|---|

---

## Visual Findings

> Carried from `exec-v2.md` § Visual Findings, plus anything the run's own frame reads turned up. These are
> layout defects, not assertion failures — they have no TC and no result. Omit where none exist.

| Platform | Screen | What is wrong | Evidence |
|---|---|---|---|

---

## AC Coverage

> Carried from `exec-v2.md`. An AC whose only TC failed or blocked on any platform reads **unverified**.

| AC | Requirement | TCs | Result |
|---|---|---|---|

---

## Not Executed

> Skipped at design, and anything deferred. Detail in `exec-v2.md` § Skipped.

| TC | Case ID | Title | Reason |
|---|---|---|---|

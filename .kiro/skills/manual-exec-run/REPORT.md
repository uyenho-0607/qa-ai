# The shape of `report.md`

Phase 3 writes `tasks/{KEY}/report.md` to the shape below, and Phase 4 completes it. Every section is
required; a section with nothing in it reads *None* rather than being dropped.

This file is what `report-bug` and the Testmo write-back read. Neither re-opens `exec.md`.

---

# SIT Execution Report — {Feature} {Build}

## Metadata

- Ticket: {KEY}
- Module: {carried from exec.md § Execution Context}
- Environment: {SIT | UAT}
- **Evidence mode:** {normal | screenshot}
- Executed At: {earliest result timestamp} – {latest result timestamp}
- Exec file: `tasks/{KEY}/exec.md`
- Environment deviations: {carried from exec.md, or "none"}

| Target | Device / URL | OS / viewport | Build |
|---|---|---|---|
| {target} | {identifier or URL} | {version or size} | {build \| unknown} |

> Carried from `exec.md` § Preflight § Targets. `report-bug` names the device or URL and the build per
> target in every bug it files, and takes both from here.

---

## Summary

> One row per target, plus an **All** row counting each TC once, at its worst status across targets.
> Pass rate is `passed / (total − skipped)`.

| Target | Total | Passed | Failed | Blocked | Skipped | Pass rate |
|---|---|---|---|---|---|---|
| {target} | {n} | {n} | {n} | {n} | {n} | {x}% |
| **All** | {n} | {n} | {n} | {n} | {n} | {x}% |

---

## Target Differences

> Every behaviour that differed between targets. A difference is a finding, not a variant.
> *None* — where every target behaved identically, and on a single-target run.

| TC | Checkpoint | {target} observed | {target} observed | Defect? |
|---|---|---|---|---|
| {TC-ID} | c{N} | {what was seen} | {what was seen} | {yes — in Bugs Found \| no — {why}} |

---

## AC Coverage

> Carried from `exec.md`. An AC whose only TC failed or blocked on any target reads `unverified`.

| AC | Requirement | TCs | Result |
|---|---|---|---|
| AC-1 | {text} | {TC-IDs} | verified |
| AC-2 | {text} | {TC-IDs} | unverified — {TC-ID} failed on {target} |

---

## Bugs Found

> Candidate defects from this run. Not filed — raise them with `report-bug` after review. One row per
> defect, naming every target it reproduced on; a defect seen on one target only is still one row.

| TC | Targets | Description | Repro | Backend | Evidence | Bug |
|---|---|---|---|---|---|---|
| {TC-ID} | {targets it reproduced on} | {one-line description} | {2/2 \| 1/2} | {status and compared values \| not checked} | {filename} | {BUG-KEY once filed, or —} |

*None* — if no failure looked like a product defect.

---

## TC Results

> One status column per target, `N/A` where the TC's surface cannot reach it. Evidence is the name derived
> from the plan — never a renamed copy. An Added Coverage TC carries `—` for its Case ID; the Testmo
> write-back asks before creating a case for it.

| TC | Case ID | Title | {target} | {target} | Bug | Evidence |
|---|---|---|---|---|---|---|
| TC-01 | {case id} | {title} | PASSED | PASSED | — | {filename} |
| TC-02 | {case id} | {title} | FAILED | N/A | {BUG-KEY} | {filename} |

---

## Failed & Blocked Details

> One entry per failed or blocked TC. This entry is what `report-bug` classifies from, so it carries every
> signal the run produced and nothing is left in `exec.md`.

### {TC-ID} — {Title} — FAILED on {targets}

**Checkpoint:** c{N} — {assertion text, verbatim}
**Expected:** {expected result from exec.md}
**Actual:** {target}: {what was observed} · {target}: {what was observed}
**Repro:** {2/2 | 1/2 — intermittent}
**Backend:** {status and compared field values | not checked}
**Crash / console:** {crash ID and summary | console error | none}
**Log:** {the lines naming the app under test | none}
**Evidence:** `evidence/{KEY}/{filename}`
**Bug:** {BUG-KEY | not filed | not a defect — {why}}

---

### {TC-ID} — {Title} — BLOCKED on {targets}

**Blocker:** {reason execution could not continue}
**Evidence:** —

---

## Skipped

> Carried from `exec.md` § Skipped.

| TC | Case ID | Title | Reason |
|---|---|---|---|
| {TC-ID} | {case id} | {title} | {reason} |

---

## Rejected Candidates

> Written by Phase 4. Bugs Found rows the user declined to file. *None* until one is declined.

| TC | Description | Reason declined |
|---|---|---|
| {TC-ID} | {one-line description} | {why it was not filed} |

---

## Notes

{Observations that don't fit a specific TC — unexpected behaviour, environment issues, the crash IDs and log
lines collected per wave, evidence files the run could not produce, unaddressable elements the app or FE team
must fix, suggestions.}

# SIT Execution Report — {Feature} {Build}

## Metadata

- Ticket: {KEY}
- Build: {build_number | unknown}
- Environment: SIT
- Executed By: {agent | human}
- Executed At: {YYYY-MM-DD HH:mm} – {YYYY-MM-DD HH:mm}
- Exec file: `tasks/{KEY}/exec.md`
- Environment deviations: {carried from exec.md, or "none"}

---

## Summary

| Total | Passed | Failed | Blocked | Skipped |
|---|---|---|---|---|
| {n} | {n} | {n} | {n} | {n} |

**Pass Rate:** {x}% ({passed}/{total − skipped})

---

## Bugs Found

> Candidate defects from this run. Not filed — raise them with `report-bug` after review.

| TC | Description | Evidence | Bug |
|---|---|---|---|
| {TC-ID} | {one-line description} | {filename} | {BUG-KEY once filed, or —} |

*None* — if no failure looked like a product defect.

---

## TC Results

> Evidence is the group's File from `exec.md` — `TC_{ids}_{slug}.{png|mp4}`, never a renamed copy.

| TC | Case ID | Title | Status | Bug | Evidence |
|---|---|---|---|---|---|
| TC-01 | {case id from exec.md} | {title} | PASSED | — | {filename} |
| TC-02 | {case id from exec.md} | {title} | FAILED | {BUG-KEY} | {filename} |
| TC-03 | {case id from exec.md} | {title} | BLOCKED | — | — |
| TC-04 | {case id from exec.md} | {title} | SKIPPED | — | — |

---

## Failed & Blocked Details

### {TC-ID} — {Title} — FAILED

**Expected:** {expected result from exec file}
**Actual:** {what the agent observed}
**Evidence:** `evidence/{KEY}/{filename}`
**Bug:** {BUG-KEY, or "not filed"}

---

### {TC-ID} — {Title} — BLOCKED

**Blocker:** {reason execution could not continue}
**Evidence:** —

---

## Skipped

| TC | Case ID | Title | Reason |
|---|---|---|---|
| {TC-ID} | {case id from exec.md} | {title} | {reason} |

---

## Notes

{Observations relevant to the feature that don't fit a specific TC — unexpected behaviour, environment issues, suggestions.}

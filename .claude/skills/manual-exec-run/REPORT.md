> Note: Sections marked `(Omit if...)` are omitted entirely when empty. Reference existing `exec.md` data rather than re-copying verbose context.

# SIT Report — {Feature} {Build}

- **Ticket** — {KEY}
- **Executed** — {earliest timestamp} → {latest timestamp}
- **Environment** — {SIT | UAT}
- **Platforms** — {labels} *(Detail in `exec.md` § Preflight)*
- **Plan** — `tasks/{KEY}/exec/exec.md`

---

## Summary

| Platform | Total | ✅ Passed | ❌ Failed | 🚫 Blocked | Skipped |
|---|---|---|---|---|---|
| {platform label} | | | | | |
| **All** | | | | | |

*Verified at recon: {n} TCs · Executed in waves: {n} TCs*

---

## Result by Test Case

| TC | Case ID | Title | Platform | Result | Bug |
|---|---|---|---|---|---|
| TC-{id} | {case id} | {title} | {label} | ✅ PASSED | — |

---

## Bugs Found

> Candidate defects for review. Raise via `report-bug`. Single place where bug keys are assigned.

| TC | Platforms | What is wrong | Repro | Backend | Evidence | Bug |
|---|---|---|---|---|---|---|
| TC-{id} | {labels} | {defect description} | {2/2 \| 1/2} | {status & values \| not checked} | {file} | — |

---

## Rejected Candidates *(Omit if no candidates rejected)*

| TC | Why it is not a defect |
|---|---|
| TC-{id} | {reason} |

---

## Failed & Blocked *(Omit if all passed)*

### TC-{id} · {Title} — {❌ FAILED | 🚫 BLOCKED} on {platform labels}

- **Expected**: {verbatim expected result from plan}
- **Observed**: {platform}: {observed state}
- **Repro**: {2/2 | 1/2 — intermittent}
- **Backend**: {status & compared field values | not checked}
- **Signals**: {crash id | console errors | none}
- **Evidence**: {file names}
- **Reading**: {product defect | environment | data | plan error} — {reasoning}

---

## Platform Differences *(Write "None" for single-platform runs)*

| What | {platform A} | {platform B} | Reading |
|---|---|---|---|

---

## Visual Findings *(Omit if no visual findings)*

| Platform | Screen | What is wrong | Evidence |
|---|---|---|---|

---

## AC Coverage

| AC | Requirement | TCs | Result |
|---|---|---|---|
| AC-{n} | {requirement description} | {TC ids} | {verified | unverified} |

---

## Not Executed *(Omit if none skipped/deferred)*

| TC | Case ID | Title | Reason |
|---|---|---|---|
| TC-{id} | {case id} | {title} | {reason} |

---

## Evidence Audit *(Omit if audit clean)*

Missing: {TC id} — {expected capture that does not exist} · {the plan line that expects it}
Anomalies: {file} — {size or duration out of standard, assertion not visible in frame, wrong section at destination, missing FAILED marker or Actual/Expected lines}
Queue: {clean | {n} failed} · retries run: {files, or "none"}
Verdict: {complete | incomplete — do not report evidence as captured}

NOTE: Sections marked `(Omit if...)` are omitted entirely when empty

`exec.md` runs from the horizontal rule below to the end of `## Test Cases`. `## Field Rules & Constraints` after it defines the fields and **never appears in the generated file** — its example result line would otherwise be picked up by the run's line index.

---

# SIT Execution — {Feature} {Build}

## Execution Context

- **Ticket** — {KEY}
- **Module** — {affected module}
- **Environment** — {SIT | UAT}
- **Platforms** — {label · label}
- **Evidence mode** — {normal | screenshot}
- **Annotations** — {yes | no}
- **Accounts** — {role/platform} — {username} / {password}
- **Sessions** — {a} = {desc} · {b} = {desc} *(Omit if all waves use 1 session)*
- **Environment changes made** — {recon state changes | none}

**Statuses** — ⏳ PENDING · ✅ PASSED · ❌ FAILED · 🚫 BLOCKED

---

## Preflight

### Platforms

| Platform | Device / URL | OS / viewport | Build | Install source |
|---|---|---|---|---|
| {label} | {identifier | URL} | {os | viewport} | {build | unknown} | {source} |

### Data

| Item | Must exist at | TCs |
|---|---|---|
| {account / record / reference} | {location} | {TC ids} |

---

## AC Coverage

Every AC from `jira.md`. A blank TCs cell is a coverage hole, not a formatting gap.

| AC | Requirement | TCs | Status |
|---|---|---|---|
| AC-1 | {text} | {TC ids} | covered |
| AC-2 | {text} | {TC id from Added Coverage} | added |
| AC-3 | {text} | — | out of scope — {owning ticket} |

## Added Coverage *(Omit if every AC was already covered)*

TCs authored because no sheet TC verified the AC, or because a Figma visual state was uncovered. Their ids
continue the same `TC-{id}` sequence as the sheet TCs.

| TC | AC | Why the sheet misses it |
|---|---|---|
| TC-{id} | AC-{n} | {what the sheet leaves unverified} |

---

## Evidence

### Groups — `normal` mode only *(Omit in screenshot mode)*

| Group | TCs | Type | Stem | Why |
|---|---|---|---|---|
| G1 | {TC ids} | {SCREENSHOT | VIDEO} | TC_{ids}_{slug} | {reason} |

### Frames — `screenshot` mode only *(Omit in normal mode)*

| TC | Expected results | Stem | Video needed for |
|---|---|---|---|
| TC-{id} | 1, 2, 3 | TC_{id}_c1c2c3_{slug} | — |

---

## Waves

Only TCs still to execute. Omit Tier-1 TCs verified at recon.

| Wave | TCs | Platforms | Reset | Sessions |
|---|---|---|---|---|
| 1 | {TC ids} | {labels} | {lightest reset action} | {1 | 2} |

---

## Skipped

| TC | Case ID | Title | Reason |
|---|---|---|---|
| TC-{id} | {case id} | {title} | {data constraint | human-executable | unaddressable {element} | needs {platform}} |

---

## Target Inventory

| Platform | Screen | Container | Element | Target | Occ | Source |
|---|---|---|---|---|---|---|
| {label} | {screen} | {container} | {element} | `id=... | desc=... | text=...` | 1 | {live scan | cache — corrected} |

## Unaddressable Elements *(Omit if all elements addressable)*

| Platform | Screen | Element | Blocked TCs | Fix |
|---|---|---|---|---|
| {label} | {screen} | {element} | {TC ids} | {fix stated by pack} |

## Visual Findings *(Omit if visual sweep found no defect)*

| Platform | Screen | What is wrong | Evidence |
|---|---|---|---|
| {label} | {screen} | {defect} | {file} |

---

## Test Cases

### TC-{id} · {Title}

{Case ID} · {platform labels} · {read-only | changes data} · {Tier n}

**Precondition** *(Omit if continuing directly from previous TC)*
{Account and starting screen}

**Test data** *(Omit if no input)*
{field}: `{value}`

**Steps**
1. {Deterministic step using Target Inventory element names}

**Steps on {platform label}** *(Omit if all platforms follow default steps)*
{n}. {Platform-specific override step}

**Expected**
1. {Assertion: [Screen] [Container] [Observable check]}

**Evidence**
{group id OR expected result frame IDs}

**Capture moments** *(VIDEO groups only; omit elsewhere)*
{n} at {moment UI displays assertion}

**Result**
- {platform label} · ⏳ PENDING
<!-- one line per platform; the run rewrites each in place, notes and all -->

**Teardown** *(Omit if no restore needed or matches next precondition)*
{Restore step}

---

## Field Rules & Constraints

- **TC Section Structure**: Included TCs must use `### TC-{id} · {Title}` in wave execution order.
- **Skipped Table Format**: Skipped TCs must reside in `## Skipped` with rows formatted as `| TC-{id} | ... |`.
- **Cross-Platform Flows**: Combine pair labels into one (e.g., `{label A} + {label B}`). Prefix steps, assertions, preconditions, and teardowns with platform names.
- **Result Format**: Exactly one `- {platform label} · {status}` line per assigned platform/pair. Tier-1 recon passes must be formatted inline as `- {platform label} · ✅ PASSED (verified at recon, build {x})`.
- **A Result Line Is One Line.** Content and one-line discipline: `manual-exec-run` Phase 2 step 4. A console error carrying newlines is collapsed to `; `.
- **Single Source of Expected Assertions**: Do not fork Expected section per platform; state observable assertions neutrally. Divergences are logged as bugs.
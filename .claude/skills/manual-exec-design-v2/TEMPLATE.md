# The shape of `exec-v2.md`

Phase 8 writes `tasks/{KEY}/exec/exec-v2.md` to the shape below. Every section is required unless its own note says
when to omit it. `## Test Cases` is last and stays last: `manual-exec-run-v2` reads everything above it as the
header, then slices one TC at a time.

The file runs from the horizontal rule below to the end of `## Test Cases`. `## Field rules` after it defines
the fields and never appears in `exec-v2.md`.

**Written for a human first.** Field names are words, not abbreviations. Result prose sits on real lines. A
lead, a developer on the ticket, or you in three weeks must be able to read this without a glossary.

`manual-exec-run-v2` rewrites exactly one thing: the result lines under each TC's `**Result**`.

---

# SIT Execution — {Feature} {Build}

## Execution Context

- **Ticket** — {KEY}
- **Module** — {the affected module from `jira.md`}
- **Environment** — {SIT | UAT} — SIT unless the user says otherwise
- **Platforms** — {label · label}, from `project-config.md` § Platforms
- **Evidence mode** — {normal | screenshot}
- **Accounts** — {role or platform} — {username} / {password}
- **Sessions** — {a} = {what session a is} · {b} = {what session b is}. Omit where every wave uses one.
- **Environment changes made** — {what recon left changed, or `none`}

**Statuses** — ⏳ PENDING · ✅ PASSED · ❌ FAILED · 🚫 BLOCKED. A skipped TC has no result line at all; it
sits in `## Skipped`.

---

## Preflight

### Platforms

| Platform | Device / URL | OS / viewport | Build | Install source |
|---|---|---|---|---|
| {label} | {identifier or URL} | {version or size} | {build \| unknown} | {where it comes from, or —} |

Plus the rows each pack lists under § Preflight.

### Data

| Item | Must exist at | TCs |
|---|---|---|
| {account / record / reference value} | {where} | {TC ids} |

---

## Evidence

### Groups — `normal` mode only

> The stem names the group; the run appends `_{platform id}` and the extension. A TC that groups with nothing
> still gets its own one-TC row. A VIDEO group is one continuous recording per platform.

| Group | TCs | Type | Stem | Why |
|---|---|---|---|---|
| G1 | {TC ids} | {SCREENSHOT \| VIDEO} | TC_{ids}_{slug} | {reason} |

### Frames — `screenshot` mode only

> One frame per expected result per platform, captured inline. Omit the Groups table entirely.

| TC | Expected results | Stem | Video needed for |
|---|---|---|---|
| {TC id} | 1, 2, 3 | TC_{id}_c1c2c3_{slug} | — |
| {TC id} | 1, 2 | TC_{id}_c1_{slug} | 2 — asserts a toast, a frame cannot prove it |

---

## Waves

> Only TCs still to execute. A Tier-1 TC verified at recon already carries its result and appears in no wave.

| Wave | TCs | Platforms | Reset | Sessions |
|---|---|---|---|---|
| 1 | {TC ids} | {labels} | {the reset, as an action} | {1\|2} |

---

## Skipped

> Covers all skipped TCs: data/env blockers, human-executable, unaddressable elements, and disabled platforms.

| TC | Case ID | Title | Reason |
|---|---|---|---|
| {TC id} | {case id} | {title} | {reason — data constraint \| human-executable \| unaddressable {element} \| needs {platform}} |

---

## Target Inventory

> Elements the TC steps touch. **Only rows recon resolved live, or that match more than one node.** An element
> already correct in `.claude/locator-cache.json` is used from there and not copied here.

| Platform | Screen | Container | Element | Target | Occ | Source |
|---|---|---|---|---|---|---|
| {label} | {screen} | {container} | {element} | `id=… \| desc=… \| text=…` | 1 | {live scan \| cache — corrected} |

`Occ` is how many nodes the target string matches on that screen. Above 1, the row carries a disambiguator or
the target is not usable.

## Unaddressable Elements

> Omit where every element is addressable.

| Platform | Screen | Element | Blocked TCs | Fix |
|---|---|---|---|---|
| {label} | {screen} | {what it is, and where} | {TC ids} | {the fix its pack states} |

## Visual Findings

> From recon's visual sweep — one frame per distinct screen per platform, read for clipping, overlap,
> truncation and misalignment. Omit where the sweep found nothing.

| Platform | Screen | What is wrong | Evidence |
|---|---|---|---|
| {label} | {screen} | {the defect} | {file name} |

---

## Test Cases

> One block per TC, in wave order. Omit a field rather than writing it empty.

### {TC id} · {Title}

{Case ID} · {platform labels} · {read-only | changes data} · {Tier n}

**Precondition**
{the account and the starting screen}

**Test data**
{field}: `{value}` · {field}: `{value}`

**Steps**
1. {step}

**Steps on {platform label}**
2. {the step as it differs there}

**Expected**
1. {separately checkable assertion}
2. {…}

**Evidence**
{group id · or: one frame each — expected 1, 2}

**Capture moments**
{n} at {the moment it must show}

**Result**
- {platform label} · ⏳ PENDING

**Teardown**
{restore step}

---

## Field rules

- **Subtitle line** — case ID, platform labels, whether the TC changes saved data, and its tier. Replaces the
  old `Surf` / `Tgt` / `Mut` fields. A TC that changes nothing reads `read-only`.
- **Platform labels** come from `project-config.md` § Platforms. A cross-platform TC names its pair as one
  label — `{label} + {label}` — because one execution has one outcome.
- **Precondition** — the exact account and starting screen. Omit the whole field where the TC continues from
  the previous one: the omission *is* the continuation.
- **Test data** — every input value, each exactly once. A step names the field; this fixes its value, so a
  step and its value can never drift apart. Omit where the TC has no input.
- **Steps** — numbered, each deterministic, naming elements by the target string Target Inventory or the
  locator cache carries.
- **Steps on {platform}** — an override for that platform only, numbered to match the step it replaces. For
  *the same step done differently*. Omit where every platform does it the same way.
- **Expected** — a numbered list, one entry per separately checkable assertion. The number is the id: evidence
  file names refer to it as `c1`, `c2`. Each entry names its screen, its container, and the observable it is
  read from. State what is checked, not why it matters. **Never fork this per platform** — a divergence is a
  finding, not a variant.
- **Evidence** — `normal`: the group id alone; type and stem live in the Groups table. `screenshot`: which
  expected results get a frame, plus any that need a video instead.
- **Capture moments** — VIDEO groups only. Omit elsewhere.
- **Result** — one line per platform the TC runs on, one per pair for a cross-platform TC. The plan ships each
  as `⏳ PENDING`. Prose the run adds sits on indented lines beneath. A Tier-1 TC verified at recon ships with
  its real result and the note `verified at recon, build {x}`.
- **Teardown** — explicit restore steps. Omit where nothing needs restoring, or where the next TC's
  precondition is exactly the state this TC ends in.

### Cross-platform TCs

Available only where `project-config.md` § Platforms has two or more groups enabled. Where it does not, none
of this appears anywhere in the file.

A cross-platform TC is one flow, executed once per pair, with both sessions open together.

- The subtitle names the pair as one label. One `**Result**` line per pair.
- Every step, precondition clause, expected result and teardown step is prefixed with the platform label it
  happens on. An unprefixed step is an unfinished plan.

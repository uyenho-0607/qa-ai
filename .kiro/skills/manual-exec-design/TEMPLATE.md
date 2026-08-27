# The shape of `exec.md`

Phase 9 writes `tasks/{KEY}/exec.md` to the shape below. Every section is required unless its own note says
when to omit it. `## Test Cases` is last and stays last: `manual-exec-run` reads everything above it as the
header, then slices one TC block at a time.

The file runs from the horizontal rule below to the end of `## Test Cases`. `## Field rules` after it defines
the fields and never appears in `exec.md`.

Added Coverage and Unaddressable Elements are read at the design gate. `manual-exec-run` reads every other
section, and rewrites exactly two: the `**R@…:**` lines, and Results Summary once at Phase 3.

---

# SIT Execution — {Feature} {Build}

## Execution Context

- Ticket: {KEY}
- Module: {the affected module from `jira.md`}
- Environment: {SIT | UAT} — SIT unless the user says otherwise
- **Targets:** {the Phase 1 selection}
- **Evidence mode:** {normal | screenshot}
- Accounts: {role or surface} — {username} / {password}
- Contexts: {a} = {what session a is}, {b} = {what session b is} — omit where every wave uses 1.
  A `bo+app` wave names its two by surface: `@app` = {device or URL}, `@bo` = {browser session and role}.
- Environment deviations: {what recon left changed, or `none`}

**Statuses:** PENDING | PASSED | FAILED | BLOCKED — the four a `**R@…:**` line can carry, plus `N/A` in
Results Summary for a column the TC's surface cannot reach. A skipped TC has neither a result line nor a
Results Summary row; it sits in `## Skipped`.

---

## Preflight

> Checked before Wave 1. A missing item blocks its TCs up front instead of mid-wave.

### Targets

| Target | Device / URL | OS / viewport | Build | Install source |
|---|---|---|---|---|
| {target} | {identifier or URL} | {version or size} | {build \| unknown} | {where it comes from, or —} |

Plus the per-surface rows each pack lists under § Preflight.

### Data

> Every row names the TCs that need it, so a missing item blocks exactly those and no others.

| Item | Must exist at | TCs |
|---|---|---|
| {account / record / reference value} | {where} | {TC-IDs} |

---

## AC Coverage

> Every AC from `jira.md`. A blank TCs cell is a coverage hole, not a formatting gap.

| AC | Requirement | TCs | Status |
|---|---|---|---|
| AC-1 | {text} | {TC-IDs} | covered |
| AC-2 | {text} | {TC-ID from Added Coverage} | added |
| AC-3 | {text} | — | out of scope — {owning ticket} |

---

## Added Coverage

> TCs written because no sheet TC verified the AC. Omit this section where every AC was already covered.
> Their IDs continue the same `TC-NN` sequence as the sheet TCs — `manual-exec-run` indexes the file on `### TC-`.

| TC | AC | Why the sheet misses it |
|---|---|---|
| {TC-ID} | AC-n | {what the sheet leaves unverified} |

---

## Execution Plan

### Evidence Groups — `normal` mode only

> The stem names the group; the run appends `_{target}` and the extension. A TC that groups with nothing
> still gets its own one-TC row. A VIDEO group is one continuous recording per target.

| Group | TCs | Type | Stem | Rationale |
|---|---|---|---|---|
| {G1} | {TC-IDs} | {SCREENSHOT \| VIDEO} | TC_{ids}_{slug} | {reason} |

### Checkpoint Evidence — `screenshot` mode only

> One frame per checkpoint per target, captured inline. Omit the Evidence Groups table entirely.

| TC | Checkpoints | Stem | Frames per target | Escape hatch |
|---|---|---|---|---|
| {TC-ID} | c1, c2, c3 | TC_{id}_c1c2c3_{slug} | 3 | — |
| {TC-ID} | c1, c2 | TC_{id}_c1_{slug} | 1 + VIDEO for c2 | c2 asserts a toast — a frame cannot prove it |

### Waves

| Wave | Groups / TCs | Surface | Targets | Reset | Contexts | Note |
|---|---|---|---|---|---|---|
| Wave 1 | {groups} | {bo \| app} | {targets} | {the reset, as an action} | {1\|2} | {why this order} |
| Wave 2 | {groups} | bo+app | {pairs} | app: {relaunch app} · bo: {fresh context} | 2 | {why this order} |

---

## Results Summary

> The run's status at a glance. The `**R@…:**` lines are authoritative — this table is derived from them,
> written once here as all-`PENDING`, and regenerated once by `manual-exec-run` at Phase 3. Nothing reads it
> to decide what to run, and no bug key is written into it: keys live on the result lines and in `report.md`.
>
> One column per target in Execution Context § Targets, plus one per pair any `bo+app` TC names. A cell reads
> `N/A` where that TC cannot reach that column — a plain TC in a pair column, a paired TC in a single-target
> column, a TC whose surface does not reach that target.

| TC | Case ID | Surface | Title | android | bo | android+bo |
|---|---|---|---|---|---|---|
| TC-01 | {case id} | app | {title} | PENDING | N/A | N/A |
| TC-02 | {case id} | bo | {title} | N/A | PENDING | N/A |
| TC-03 | — | bo+app | {title} | N/A | N/A | PENDING |

Case ID is the ID `tc.md` carries — the Testmo case ID or the sheet TC ID. An Added Coverage TC carries `—`.

---

## Skipped

| TC | Case ID | Title | Reason |
|---|---|---|---|
| {TC-ID} | {case id} | {title} | {human-executable \| unaddressable {element} \| needs {target}} |

---

## Target Inventory

> Every element the TC steps touch, from recon. One column per selected target. No coordinate appears here.

| Surface | Screen | Container | Element | Target | Occ | {target} | {target} | Source |
|---|---|---|---|---|---|---|---|---|
| {bo\|app} | {screen} | {container} | {element} | `id=… \| desc=… \| text=…` | 1 | yes | yes | {locator-cache \| domain file \| live scan} |

`Occ` is how many nodes the target string matches on that screen.

---

## Unaddressable Elements

> The unaddressable elements recon found. Omit this section where every element is addressable.

| Surface | Screen | Element | Targets | Blocked TCs | Fix |
|---|---|---|---|---|---|
| app | {screen} | {what it is, and where} | {all \| named targets} | {TC-IDs} | add a React Native `testID` |
| bo | {screen} | {what it is, and where} | {targets} | {TC-IDs} | add a `data-testid` |

---

## Test Cases

> One block per TC. Every field is a single bolded key on its own line — no `####` headings, no `---`
> separators between blocks. Omit a field rather than writing it empty.

### {TC-ID} — {Title} ({case id from `tc.md`})
**Surf:** {bo | app | bo+app}
**Tgt:** {targets, or pairs when `bo+app`}
**Pre:** {precondition, naming the account and the starting screen}
**Data:** {field}: `{value}`; {field}: `{value}`
**Mut:** {yes|no}
**Steps:**
1. {step}
**Steps@{targets}:** {n}. {the step as it differs on those targets}
**Exp:**
- c1 {separately checkable assertion}
- c2 {…}
**Ev:** {group ID, or `checkpoints c1,c2`}
**Cap:** c{N} at {the moment it must show}
**R@{target}:** PENDING · —
**Teardown:** {restore step}

---

## Field rules

- `**Surf:**` — what the TC exercises. `bo+app` only where one flow must span both surfaces; two TCs that
  happen to sit next to each other are not one paired TC.
- `**Tgt:**` — the targets this TC's surface can reach, minus any target recon blocked. One `**R@…:**` line
  per entry, in the same order. A target the TC cannot reach is simply absent — there is no `N/A` line.
- `**Pre:**` — the exact account and the starting screen. Omit the line where the TC continues from the
  previous one: the omission *is* the continuation.
  Paired form: `@app {member account, starting screen} · @bo {BO account, starting page}`.
- `**Data:**` — every input value the TC needs, each exactly once. A step names the field; this line fixes
  its value, so a step and its value can never drift apart. Omit where the TC has no input.
- `**Mut:**` — `yes` where the steps change persisted state, `no` where they only read. The runner batches
  `no` TCs sharing a screen into one pass.
- `**Steps:**` — numbered, each one deterministic. A step names an element by the target string Target
  Inventory carries for it.
- `**Steps@{targets}:**` — an override for the listed targets only, numbered to match the step it replaces.
  For *the same step done differently* on another target — a tap where a click was. Omit where every target
  does the step the same way.
- `**Exp:**` — one bullet per separately checkable assertion, numbered `c1`, `c2`, … . Both evidence modes
  refer to a checkpoint by that id, and so do `**Cap:**` and the evidence file name. Each assertion names its
  screen, its container, and the observable it is read from — including the endpoint, where the surface pack
  makes it a backend check. State what is checked, not why it matters. Never fork `**Exp:**` per target: a
  divergence in the expected result is a finding, not a variant.
- `**Ev:**` — `normal` mode: the group ID alone; type, stem and path come from the Evidence Groups table and
  are never repeated per TC. `screenshot` mode: the checkpoint list — `**Ev:** checkpoints c1,c2` — plus any
  escape hatch, `+ VIDEO c2`.
- `**Cap:**` — VIDEO groups only: the moment each checkpoint must show. Omit elsewhere.
- `**R@{target}:**` — one per entry in `**Tgt:**`. The plan ships each one as `PENDING · —`;
  `manual-exec-run` owns the grammar it rewrites them to.
- `**Teardown:**` — explicit restore steps. Omit where nothing needs restoring, and where the next TC's
  precondition is exactly the state this TC ends in.

### `bo+app` only

A paired TC is one flow, executed once per pair, with both sessions open together.

- `**Tgt:**` lists **pairs** — `android+bo` — because one paired execution has one outcome, not one per
  surface. Two pairs mean the flow ran twice: `android+bo, ios+bo`.
- `@app` and `@bo` prefix every step, precondition clause, checkpoint and teardown step, saying which surface
  it happens on. An untagged step on a paired TC is an unfinished plan.
- One `**R@{pair}:**` line per pair.

A `bo` or `app` TC carries none of this, however many targets it runs on.

---
name: report-bug
description: Report SIT bug — classify FE/BE, capture evidence, create a SIT Bug subtask under the parent. Use on /bug, /report-bug, or asks to file a bug.
---

## Contract

- **Args:** `{PARENT}` — parent ticket key (required)
- **Writes:** `tasks/{PARENT}/exec/evidence/` · a `SIT Bug` sub-task under `{PARENT}`
- **Returns:** the created `SIT Bug` key

## Pre-Flight
1. Read `.claude/docs/lessons.md`
2. Extract the target list and URLs:
   ```
   awk '/^## /{p=/^## (Platforms|Environment)$/} p' .claude/steering/project-config.md
   ```

## Flow

### 1. Gather Info
- Parent ticket (required)
- Symptom vs expected behavior

**Invoked standalone** → dispatch the `dup-scout` agent with the symptom, the platform, and the parent key before filing anything. A `duplicate of {KEY}` verdict goes to the user with the key, and they decide: comment on the existing bug, or file a new one. No Agent tool in context → grep `tasks/*/exec/report.md` for the symptom and check the parent's existing SIT Bug sub-tasks, then present what you found. **Invoked by `manual-exec-run` Phase 4** → the scan already ran there; skip it.
- **Target** — where the defect was seen, from § Platforms (`bo`, `android`, …). Never infer from the module. Two targets = one bug naming both → load that row's Pack, then the domain section that pack names for the module.

### 2. Plan → GATE
Present and wait for approval:
```
PLAN: Bug under {PARENT}
Title: [{PROJECT_KEY}][{Module}] {symptom summary}
Target: {ids from § Platforms — every one it reproduces on}
Symptom: {what's wrong}
Expected: {correct behavior}
Classification: {API to intercept}
Evidence: {screenshot/video} — {reasoning}
Element: {id=|desc=|text= of the asserted element}
Label: {what is verified}
```

### 3. Execute
1. Reproduce on every target. Web → intercept network BEFORE first navigation. Device → no interception exists; collect the backend check, crash log, device log, repro count
2. Classify FE/BE from what the target produced → GATE: confirm with user
3. Invoke `capture-evidence` skill. Pass `targets={targets}`, `stem={PARENT}_bug_{N}` (`{N}` = next unused index in `dest`), `dest=tasks/{PARENT}/exec/evidence/`, `type={screenshot|video per § Evidence Decision}`, `element={id=|desc=|text= of the asserted element}`, `label={what is verified}`, `annotation=yes` web / `no` device
   **Invoked by `manual-exec-run`** → the evidence exists; take its path from the candidate and skip re-capture unless § Evidence Decision calls for a different `type`.

### 4. Create Bug
Invoke `jira-handler` skill — action: `create_bug`
- summary: `[{PROJECT_KEY}][Module] symptom`
- Name every target the defect reproduced on, with its device identifier or URL
- Bug text: simple English, ≤12 words a sentence, active voice, present tense. State the observed defect; nothing about how it was found.
- assignee: from the confirmed FE/BE classification per `.claude/skills/jira-handler/dev-team.md` § Assignment Rule
- Return the key to the caller.

### 5. Cleanup
- Ask whether to submit the Testmo run result; on yes invoke the `mark-testmo-run` skill.
- Delete the local copy only after the user confirms Jira shows the attachment. `report.md` keeps the path as a record of what was filed.

## FE vs BE Classification

**Intercept network — never guess.**

- **BE**: 5xx error, wrong/missing API payload data, unexpected 4xx, data inconsistency, ignored API params.
- **FE**: API correct but UI wrong, layout/styling/Figma mismatch, JS error, UI-side sort/filter bug.
Ambiguous → ask user.

## Evidence Decision
Rule: "Single frame proves it?" → screenshot. "Action + result?" → video.
- **Screenshot**: Static data/format, missing element, layout/styling, toast.
- **Video**: Sort/filter/search, multi-step workflow, routing, state update.
*API wrong data*: Screenshot + console overlay

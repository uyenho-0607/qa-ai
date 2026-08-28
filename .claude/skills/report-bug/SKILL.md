---
name: report-bug
description: "Report SIT bugs — classify FE/BE, capture evidence, create subtask under parent. Use when user asks to file/report a bug, or says /bug, /report-bug."
---

# Report Bug

## Pre-Flight
1. Read `.claude/docs/lessons.md`
2. Extract Jira constants:
   ```bash
   awk '/^## /{p = /Rovo MCP|Transitions|Bug Assignment/} p' .claude/steering/jira.md
   ```
   Read `project-config.md` for URLs.
3. Extract the target vocabulary, then the section for the target in hand — **one surface, never both**:
   ```bash
   awk '/^## /{p = /Target Vocabulary/} p' .claude/steering/bug-conventions.md
   # then, substituting Web or Device for {S}:
   awk '/^## /{p = /Classify FE vs BE|{S} Targets — Reproduce and Classify|Evidence Rule/} p' \
     .claude/steering/bug-conventions.md
   ```
4. Read the domain file that § Target Vocabulary names for the target in hand, plus
   `.claude/domain/otc-shared.md` for rules spanning both surfaces.

## Flow

### 1. Gather Info
- Parent ticket (required) — bug is "SIT Bug" subtask, never standalone
- Symptom vs expected behavior
- **Target** — where the defect was seen, per § Target Vocabulary. Ask; never infer it from the module name. A defect on
  two targets is one bug naming both.

### 2. Plan → GATE
Present and wait for approval:
```
PLAN: Bug under {PARENT}
Title: [{PROJECT_KEY}][{Module}] {symptom summary}
Target: {bo | bo-mv | ios | android | app-web — every one it reproduces on}
Symptom: {what's wrong}
Expected: {correct behavior}
Classification: {API to intercept — web} | {endpoint to check, crash and log — device}
Evidence: {screenshot/video} × {one per target} — {reasoning}
Duplicate JQL: parent = {PARENT} AND summary ~ "{keyword}"
```

### 3. Execute
1. Duplicate check → if found, ask user before proceeding
2. Reproduce on every target in the plan, per its § Reproduce and Classify section — a web target with interception started
   before the first navigation; a device target collecting the backend check, crashes and the device log,
   with a repro count
3. Classify FE/BE per § Classify FE vs BE, using the signals the target actually produced → GATE: confirm
   with user
4. Invoke the `capture-evidence` skill — never capture manually. Pass `targets` (every target it reproduced
   on), `purpose: bug`, the element and label, and `backend` where a backend check ran

### 4. Create Bug
Invoke the `jira-handler` skill action: `create_bug`
- summary: `[{PROJECT_KEY}][Module] symptom`
- Attach every capture `capture-evidence` returned, and nothing else — never a `.md` beside one
- A native frame shows no device, OS version, build, or statement of what it proves. Write all four into the
  description itself, per capture, so an attachment is never the only place a fact lives
- Name every target the defect reproduced on in the description, with the device identifier or URL and the
  build per target
- If wrong evidence → action: `fix_wrong_evidence`

### 5. Cleanup
- Ask about Testmo link
- Add `@issue` decorator if from test
- Delete local files after upload confirmed

## Classification & Evidence Rules

Already in hand from Pre-Flight step 3 — the shared § Classify FE vs BE, the § for this target's surface, and
§ Evidence Rule. Do not re-extract, and never read the other surface's section.

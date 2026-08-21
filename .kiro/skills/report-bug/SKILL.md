---
name: report-bug
description: "Report SIT bugs — classify FE/BE, capture evidence, create subtask under parent. Use when user asks to file/report a bug, or says /bug, /report-bug."
---

# Report Bug

## Pre-Flight
1. Read `.kiro/domain/manual-task-lessons.md`
2. Read `.kiro/steering/jira.md` (project ids, dev team) + `project-config.md` (URLs)
3. Read relevant domain module file

## Flow

### 1. Gather Info
- Parent ticket (required) — bug is "SIT Bug" subtask, never standalone
- Symptom vs expected behavior
- Evidence source: allure-results (`disclose_context("allure-reader")`) or Playwright browser

### 2. Plan → GATE
Present and wait for approval:
```
PLAN: Bug under {PARENT}
Title: [{PROJECT_KEY}][{Module}] {symptom summary}
App: {OMS/EMS/Backoffice}
Symptom: {what's wrong}
Expected: {correct behavior}
Classification: {API to intercept}
Evidence: {screenshot/video} — {reasoning}
Duplicate JQL: parent = {PARENT} AND summary ~ "{keyword}"
```

### 3. Execute
1. Duplicate check → if found, ask user before proceeding
2. Open browser → reproduce → intercept network (BEFORE navigation)
3. Classify FE/BE from API evidence → GATE: confirm with user
4. `disclose_context("capture-evidence")` — never capture manually

### 4. Create Bug
`disclose_context("jira-handler")` action: `create_bug`
- summary: `[{PROJECT_KEY}][Module] symptom`
- If wrong evidence → action: `fix_wrong_evidence`

### 5. Cleanup
- Ask about Testmo link
- Add `@issue` decorator if from test
- Delete local files after upload confirmed

## FE vs BE Classification

**Intercept network — never guess.**

| BE (assign BE dev) | FE (assign FE dev) |
|--------------------|-------------------|
| 5xx errors | API correct, UI wrong |
| Wrong/missing data in response | Layout/styling issues |
| Unexpected 4xx | UI doesn't match Figma |
| Data inconsistency | Client JS errors |
| Filter/sort param ignored | FE sorts/filters wrong |

Ambiguous → ask user.

## Evidence Decision

| Type | Evidence |
|------|----------|
| Static data/format/missing element | Screenshot |
| Layout/styling | Screenshot |
| API wrong data | Screenshot + console overlay |
| Sorting/filter/search | Video |
| Multi-step workflow | Video |
| Toast/notification | Video |
| Navigation/routing | Video |
| State doesn't update | Video |

Rule: "Single frame proves it?" → screenshot. "Action + result?" → video.

---
name: report-bug
description: "Report SIT bugs — classify FE/BE, capture evidence, create subtask under parent. Use when user asks to file/report a bug, or says /bug, /report-bug."
---

# Report Bug

## Pre-Flight
1. Read `.kiro/docs/lessons.md`
2. Extract Jira constants:
   ```bash
   awk '/^## /{p = /Rovo MCP|Transitions|Bug Assignment/} p' .kiro/steering/jira.md
   ```
   Read `project-config.md` for URLs.
3. Read the domain file for the app under test — `.kiro/domain/otc-bo.md` (Backoffice) or `.kiro/domain/otc-mobile.md` (Android / iOS app) — plus `.kiro/domain/otc-shared.md` for rules spanning both (password policy, OTP, statuses, decimal precision).

## Flow

### 1. Gather Info
- Parent ticket (required) — bug is "SIT Bug" subtask, never standalone
- Symptom vs expected behavior
- Evidence source: Playwright browser

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
4. disclose_context("capture-evidence") — never capture manually

### 4. Create Bug
disclose_context("jira-handler") action: `create_bug`
- summary: `[{PROJECT_KEY}][Module] symptom`
- If wrong evidence → action: `fix_wrong_evidence`

### 5. Cleanup
- Ask about Testmo link
- Add `@issue` decorator if from test
- Delete local files after upload confirmed

## Classification & Evidence Rules

```bash
awk '/^## /{p = /Classify FE vs BE|Evidence Rule/} p' .kiro/steering/bug-conventions.md
```

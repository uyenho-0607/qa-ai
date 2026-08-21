---
name: verify-bug
description: "Verify bug fixes — reproduce STR, capture evidence, post verification comment, transition ticket. Use when user asks to verify a fix, retest, or says /verify-bugs-batch."
---

# Verify Bug

## Pre-Flight
1. Read `.claude/domain/manual-task-lessons.md`
2. Read `.claude/steering/jira.md` (transitions) + `project-config.md` (URLs)
3. Read relevant domain module file

## Flow

### 1. Fetch Bug
- `getJiraIssue` fields: summary, description, attachment, status
- Note status for transition decision
- Match evidence type/count from original bug attachments

### 2. Plan → GATE
Present and wait for approval:
```
PLAN: Verify {KEY}
Status: {status} | App: {OMS/EMS/Backoffice}
STR: {steps}
Pass: {criteria} | Fail: {criteria}
Evidence: {type} x{count}
```

### 3. Execute
1. Open browser → follow STR → observe result
2. Propose finding → GATE: wait for user agreement
3. `Read .claude/skills/capture-evidence/SKILL.md` — never capture manually

### 4. Post Comment
`Read .claude/skills/jira-handler/SKILL.md` action: `post_verification`
- If wrong → action: `fix_wrong_comment`

### 5. Transition

Ready to Test in SIT → SIT in progress (41) → Pass SIT (51) / Reopen (81)
Won't Do (71): bug no longer required

### 6. Cleanup
- Ask about Testmo updates
- Delete local files after upload confirmed

## Rules
- Evidence count must match or exceed original bug
- Before reopening: validate locators against live DOM, check fixtures
- Different issue found → close this bug, file new one

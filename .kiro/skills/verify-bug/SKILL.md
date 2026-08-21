---
name: verify-bug
description: "Verify bug fixes — reproduce STR, capture evidence, post verification comment, transition ticket. Use when user asks to verify a fix, retest, or says /verify-bugs-batch."
---

# Verify Bug

## Pre-Flight
1. Read `.kiro/docs/lessons.md`
2. Extract Jira transitions:
   ```bash
   awk '/^## /{p = /Transitions/} p' .kiro/steering/jira.md
   ```
   Read `project-config.md` for URLs.
3. Read the domain file for the app under test — `.kiro/domain/otc-bo.md` (Backoffice) or `.kiro/domain/otc-mobile.md` (Android / iOS app) — plus `.kiro/domain/otc-shared.md` for rules spanning both (password policy, OTP, statuses, decimal precision).

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
3. disclose_context("capture-evidence") — never capture manually

### 4. Post Comment
disclose_context("jira-handler") action: `post_verification`
- If wrong → action: `fix_wrong_comment`

### 5. Transition

disclose_context("jira-handler") action: `transition`. Ids come from the Pre-Flight extract — never from memory.

Path: `Ready to Test in SIT` → `SIT in Progress` → `Pass SIT` on a pass, `Reopen` on a fail. `Not Required` when the bug is no longer required.

### 6. Cleanup
- Ask about Testmo updates
- Delete local files after upload confirmed
- Verification turned up a reusable lesson — a locator that moved, a fixture that lies, an env quirk that cost a re-run → append one bullet to `.kiro/docs/lessons.md` with the ticket key. Nothing reusable → skip.

## Rules
- Evidence count must match or exceed original bug
- Before reopening: validate locators against live DOM, check fixtures
- Different issue found → close this bug, file new one

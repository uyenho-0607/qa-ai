---
name: verify-bug
description: "Verify bug fixes — reproduce STR, capture evidence, post verification comment, transition ticket. Use when user asks to verify a fix, retest, or says /verify-bugs-batch."
---

# Verify Bug

## Pre-Flight
1. Read `.claude/docs/lessons.md`
2. Extract Jira transitions:
   ```bash
   awk '/^## /{p = /Transitions/} p' .claude/steering/jira.md
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

### 1. Fetch Bug
- `getJiraIssue` fields: summary, description, attachment, status
- Note status for transition decision
- Match evidence type/count from original bug attachments
- **Target** — the one the bug names, per § Target Vocabulary. A bug naming two targets is verified on both, and passes
  only where both pass. A bug naming none: ask — never assume `bo`.

### 2. Plan → GATE
Present and wait for approval:
```
PLAN: Verify {KEY}
Status: {status} | Target: {bo | bo-mv | ios | android | app-web — every one the bug names}
STR: {steps}
Pass: {criteria} | Fail: {criteria}
Evidence: {type} x{count}, one per target
```

### 3. Execute
1. Follow the STR on every target in the plan, per its § Reproduce and Classify section — a browser for a web target, a
   device for `ios` / `android`. On a device target, collect the backend check, crashes and the device log
   before deciding a fail
2. Propose finding → GATE: wait for user agreement. A target-specific result is stated per target, never
   averaged
3. Invoke the `capture-evidence` skill — never capture manually. Pass `targets` (every target verified),
   `purpose: verify`, the element and label

### 4. Post Comment
Invoke the `jira-handler` skill action: `post_verification`
- State the result per target, and name the device identifier or URL and the build for each
- Attach captures only — never a `.md` beside one. State the device, OS version, build and what each capture
  shows in the comment itself
- If wrong → action: `fix_wrong_comment`

### 5. Transition

Invoke the `jira-handler` skill action: `transition`. Ids come from the Pre-Flight extract — never from memory.

Path: `Ready to Test in SIT` → `SIT in Progress` → `Pass SIT` on a pass, `Reopen` on a fail. `Not Required` when the bug is no longer required.

### 6. Cleanup
- Ask about Testmo updates
- Delete local files after upload confirmed
- Verification turned up a reusable lesson — a locator that moved, a fixture that lies, an env quirk that cost a re-run → append one bullet to `.claude/docs/lessons.md` with the ticket key. Nothing reusable → skip.

## Rules
- Evidence count must match or exceed original bug, per target
- Before reopening: validate every element against the live source — the DOM on a web target, the current
  `mobile_list_elements_on_screen` return on a device target — and check fixtures. An element that moved is
  not a reopened bug
- A device target absent: report it unavailable and verify the targets that are present. Never pass a target
  that never ran
- Different issue found → close this bug, file new one

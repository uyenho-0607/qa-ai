---
name: verify-bug
description: Verify a bug fix — reproduce STR, capture evidence, post verification comment, transition. Use on asks to verify or retest, /verify-bug.
---

## Contract

- **Args:** `{KEY}` — bug ticket key (required) [, env: `sit`]
- **Writes:** `tasks/{KEY}/exec/evidence/` · one comment on `{KEY}` · at most one transition

## Pre-Flight
1. Read `.kiro/docs/lessons.md`
2. Extract `.kiro/steering/jira.md` — Transitions section only:
   ```
   awk '/^## /{p=/^## Transitions$/} p' .kiro/steering/jira.md
   ```
3. Extract the target list and URLs:
   ```
   awk '/^## /{p=/^## (Platforms|Environment)$/} p' .kiro/steering/project-config.md
   ```
4. Read the target's pack from § Platforms, then extract the module's section from the domain file the pack points to:
   ```
   awk '/^## /{p=/^## {Module}$/} p' .kiro/domain/{domain file}
   ```

## Flow

### 1. Fetch Bug
- `getJiraIssue` fields: summary, description, attachment, status
- Note status for transition decision
- Match evidence type from original bug attachments, per target
- **Target** — the one the bug names, from § Platforms. Two targets = verify both, passes only if both pass. Names none → ask, never assume

### 2. Plan → GATE
Present and wait for approval:
```
PLAN: Verify {KEY}
Status: {status} | Target: {ids from § Platforms — every one the bug names}
STR: {steps}
Pass: {criteria} | Fail: {criteria}
Evidence: {type} x{count}, one per target
```

### 3. Execute
1. Follow the STR on every target. Web → browser, elements from the live DOM. Device → terminate and relaunch to reach the start state, never tap back through the stack; elements from a current screen inspection, never a coordinate
2. Device has no network interception — before calling a fail, collect the backend check for the implicated endpoint, the crash log and the device log
3. Capture evidence immediately once pass/fail is observed, before proposing the finding — a BO session can expire and a device app gets terminated/relaunched while a gate waits on the user. Invoke `capture-evidence` skill. Pass `targets={targets}`, `stem={KEY}_verify_{N}`, `dest=tasks/{KEY}/exec/evidence/`, `type={type}`, element, label, `annotation=yes` web / `no` device
4. Propose finding → GATE: wait for user agreement, with the evidence file paths already in hand. State the result per target, never averaged

### 4. Post Comment
Invoke `jira-handler` skill — action: `post_verification`. Pass `key={KEY}`, the file paths `capture-evidence` returned, `env={env}`, `verdict={Verified FIXED|Verified NOT FIXED}`, and the per-target result text.
- State the result per target, naming its device identifier or URL and the build

### 5. Transition

Invoke `jira-handler` skill — action: `transition`. Ids come from the Pre-Flight 2 extract, never from memory.

### 6. Cleanup
- Ask about Testmo updates
- Delete the local copy once Jira shows the attachment.

## Rules
- Evidence count must match or exceed original bug, per target
- Before reopening: validate every element and check fixtures. An element that moved is not a reopened bug
- A device absent → report it unavailable and verify the targets present. Never pass a target that never ran
- Different issue found → close this bug, file new one

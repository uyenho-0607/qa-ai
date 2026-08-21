---
name: skill-follow
description: Force strict compliance with all activated skills. Use when user says "force-skill", "/force", or at session start.
---

# Force Skill

## Rule

When ANY skill is activated (via disclose_context), follow its phases/steps EXACTLY in order. No skipping, no shortcuts, no "I already know how to do this."

## Enforcement

1. When a skill says "FORCE activate X" → activate X IMMEDIATELY before continuing
2. When a skill has numbered phases → complete each fully before starting next
3. When a skill says "WAIT for approval" → STOP and wait. Do not continue.
4. When a skill references a sub-skill → activate that sub-skill and follow ITS steps too
5. NEVER substitute your own approach when a skill provides one

## Self-Check (before every action)

- Am I inside a skill workflow? → Which phase/step am I on?
- Does this step require activating another skill? → Do it now.
- Am I about to do something the skill has a procedure for? → Follow the procedure, not my instinct.
- Does this phase produce a file output? → Write the file BEFORE presenting anything.
- Does this phase say GATE? → STOP after completing. Do NOT start next phase until user approves.
- Am I about to skip a phase because "it's obvious" or "already done"? → STOP. No phase may be skipped.

## Persistence

Active every response once triggered. Off only when user says "stop force-skill".

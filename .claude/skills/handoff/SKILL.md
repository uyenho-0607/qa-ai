---
name: handoff
description: Create a handoff document for another AI session to continue work. Use when user says /handoff.
argument-hint: "What will the next session focus on?"
---

# Handoff

Generate a state transfer document — not a conversation summary.

If user provided arguments, tailor handoff to that objective.

## Required Sections

### Objective
Goal + success criteria.

### Current Status
- Completed work
- Work in progress
- Remaining tasks
- Blockers

### Project Context
Only what's needed: architecture, stack, key files, business rules.

### Important Decisions
| Decision | Rationale | Trade-offs |

### Knowledge Gained
- Confirmed/disproven assumptions
- Debugging discoveries
- Implementation insights
- Lessons learned

### Failed Attempts
| Approach | Why Failed | Alternative |

### Constraints
Technical limits, compatibility, standards, policies.

### Relevant Artifacts
Reference existing docs (PRDs, ADRs, PRs, commits) — don't duplicate.

### Remaining Issues
Separate: confirmed issues, suspected issues, open questions.

### Recommended Next Steps
Prioritized execution order.

### Suggested Skills
Only directly relevant skills.

## Before Finalizing
- Remove obsolete/superseded info
- Eliminate contradictions
- Separate facts from assumptions
- Mark uncertainty clearly

## Exclude
- Conversation history
- Unnecessary explanations
- Secrets/keys/passwords/PII

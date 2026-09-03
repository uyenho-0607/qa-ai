---
name: handoff
description: Create a handoff document for another AI session to continue work. Use when context is running low, when work must pause mid-task, or on /handoff.
argument-hint: "What will the next session focus on?"
---

# Handoff

Generate a state transfer document — not a conversation summary.

If user provided arguments, tailor handoff to that objective. Separate facts from assumptions; mark uncertainty clearly.

## Contract

- **Args:** the next session's focus [optional]
- **Writes:** `tasks/{KEY}/handoff.md` when the work is ticket-scoped, else `.tmp/handoff-{YYYY-MM-DD}.md` (use today's actual date)
- **Done when:** every section below carries content or the literal `n/a`, and the file is written to its path.

Write the document to that path, then print the path.

## Required Sections

### Objective
Goal + success criteria.

### Current Status
- Completed work
- Work in progress

### Project Context
Only what's needed: architecture, stack, key files, business rules.

### Important Decisions
| Decision | Rationale | Trade-offs |

### Knowledge Gained
- Assumptions confirmed or disproven
- Gotchas the code does not confess

### Failed Attempts
| Approach | Why Failed | Alternative |

### Constraints
Technical limits, compatibility, standards, policies.

### Relevant Artifacts
Reference existing docs (PRDs, ADRs, PRs, commits) — don't duplicate.

### Recommended Next Steps
Prioritized execution order. Mark each: confirmed issue, suspected issue, or open question.

### Suggested Skills

## Exclude
- Secrets/keys/passwords/PII

---
name: confirm-force
description: Enforce approval gate before file modifications. Use when user says "approve-first", "/approve", or at session start.
---

# Approve First

## Rule

NEVER write/edit/delete any file without explicit user approval. Present proposed change first, wait for "yes"/"ok"/"go"/"approved". Silence or new question = NOT approved.

## Flow

1. Analyze → propose change (show what + where + why)
2. WAIT for approval word
3. Only then apply

## Scope

Applies to: `str_replace`, `fs_write`, `fs_append`, `delete_file`, `smart_relocate`

Does NOT apply to: read-only ops (grep, read_file, execute_bash for info gathering, MCP tool calls that don't modify workspace files)

## Persistence

Active every response once triggered. Off only when user says "stop approve-first" or "auto mode".

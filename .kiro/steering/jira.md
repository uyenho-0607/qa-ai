---
inclusion: manual
---

# Jira — Reference Data

Project-specific constants and rules for Jira operations.

## Rovo MCP

| Field | Value |
|---|---|
| Site | `<FILL_IN>.atlassian.net` |
| `cloudId` | `<FILL_IN>` |
| Project id | `<FILL_IN>` (key `<PROJECT_KEY>`) |
| `SIT Bug` issue type id | `<FILL_IN>` (subtask) |

## Project Rules

- Target project id from above; never resolve the project by search.
- Read project key in ticket titles as the tenant name when it differs from the Jira project key.

## Transitions

Start Test `<id>` | Pass SIT `<id>` | Reopen `<id>` | Not Required `<id>` | Start Fix `<id>`.
For any other transition, call `getTransitionsForJiraIssue` and use the id it returns.

## Bug Assignment

FE → `<names>` | BE → `<names>`
Names and account IDs: `.kiro/skills/jira-handler/dev-team.md`.

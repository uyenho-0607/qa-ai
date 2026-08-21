# Jira — Reference Data

Project-specific constants and rules for Jira operations.

## Rovo MCP

- Site — `aquariux.atlassian.net`
- `cloudId` — `12682e49-4a34-4c8d-a5be-1131ec1b93cc`
- Project id — `10263` (key `AO`, name `AQXPAY-OTC`)
- `SIT Bug` issue type id — `10017` (subtask)
- `QA Preparation` issue type id — `10632` (subtask) — where TC review feedback is left
- `QA Execution` issue type id — `10633` (subtask)

## Project Rules

- Target project id `10263`; never resolve the project by search.
- Project key is `AO` — issue keys follow the format `AO-NNN`.

## Transitions

Reopen `81` | Not Required `71` | Start Fix `11` | SIT in Progress `41` | Pass SIT `51`.
For any other transition, call `getTransitionsForJiraIssue` and use the id it returns.

## Bug Assignment

Names and account IDs: `.claude/skills/jira-handler/dev-team.md`.

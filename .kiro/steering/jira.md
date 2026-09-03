---
inclusion: manual
---

## Rovo MCP

- Site — `aquariux.atlassian.net`
- `cloudId` — `12682e49-4a34-4c8d-a5be-1131ec1b93cc`
- Project id — `10263` (key `AO`, name `AQXPAY-OTC`)
- `SIT Bug` — `10017` (subtask)
- `QA Preparation` — `10632` (subtask) — where TC review feedback is left
- `QA Execution` — `10633` (subtask)

## Project Rules

- Target project id `10263`; never resolve the project by search.
- Issue keys follow the format `{PROJECT_KEY}-NNN` — the key is in `project-config.md` § Environment.

## Transitions

- Reopen `81` | Not Required `71` | SIT in Progress `41` | Pass SIT `51`.
- SIT Bug verify route, from status:
  -  Ready to Test in SIT: -> `41` -> `51` if fixed else `81`
  - Open/Reopen: -> `71` if no longer reproduces; else keep status unchanged
- For any others, call `getTransitionsForJiraIssue`.

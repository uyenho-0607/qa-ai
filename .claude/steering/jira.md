## Rovo MCP

- Site — `aquariux.atlassian.net`
- `cloudId` — `12682e49-4a34-4c8d-a5be-1131ec1b93cc`
- Project id — `10014` (key `WT`, name `Web Trader`)
- `SIT Bug` — `10017` (subtask)
- `Frontend Development` — `10018` (subtask)
- `Backend Development` — `10019` (subtask)
- `Epic` — `10000`

`QAT` (id `10395`, name `QA Team`) is the automation-repo's own work-item project — a task like
"automate WT-1234 TC01-23" goes there, but a bug against the app never does.

## Project Rules

- Target project id `10014`; never resolve the project by search.
- Issue keys follow the format `{PROJECT_KEY}-NNN` — the key is in `project-config.md` § Environment.
- Every bug this team files is a `SIT Bug` (`10017`) subtask under a parent ticket, whatever
  environment the defect turned up in — a prod or UAT finding still gets filed as `SIT Bug`, with
  the environment named in the summary and description instead. The `WT` project's scheme offers
  other bug types from other teams' workflows; picking one of those lands the ticket in a different
  triage queue. If a situation seems to call for a different type, ask rather than deciding.
- Summary format: `[WT][{ENV or Module}] {symptom}` — e.g. `[WT][PROD] TinShing pending orders not
  displaying on member site`. One codebase serves four clients, so name the client whenever the
  defect is client-specific — "Pending orders missing" and "TinShing pending orders missing" send a
  triager to very different places.

## Transitions

- Reopen `81` | Not Required `71` | Start Test `41` | Pass SIT `51` | Start Fix `11`.
- SIT Bug verify route, from status:
  - `Ready to Test in SIT` → `41` → `51` if fixed else `81`
  - `Open`/`Reopened` → `71` if no longer reproduces; else keep status unchanged
- For any others, call `getTransitionsForJiraIssue`.

## Open statuses vs closed

Open: `Ready to Test in SIT`, `SIT in progress`, `Reopened`, `Open`.
Closed: `Done`, `Won't Do`, `Closed`.

## Known gap — `apply-jira-feedback`'s QA Preparation sub-task

`apply-jira-feedback` looks for a `QA Preparation` sub-task under the parent ticket
(`.claude/skills/apply-jira-feedback/SKILL.md:36`). WT's issue-type scheme (above) has no
`QA Preparation` or `QA Execution` type — those were OTC-specific. The skill already degrades
gracefully (reports "no QA Preparation sub-task found" and asks where the feedback lives), so
nothing is broken, but on WT it will likely always take that fallback path until confirmed where
WT actually leaves TC review feedback (a different subtask type, or plain comments on the parent).

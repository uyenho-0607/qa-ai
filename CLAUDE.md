# CLAUDE.md

## Working rules

- **Skill adherence.** Run an invoked skill's phases in order. Complete every phase.
- **Approval before writes.** Propose the change — what, where, why — then wait for an explicit "yes"/"ok"/"go". Silence or a follow-up question is not approval. Covers `Write`, `Edit`, and any `Bash` that creates, moves, or deletes a file (`sed -i`, `>`, `>>`, `mv`, `rm`, `cp`, heredocs). Read-only operations are exempt. Suspended while the user has asked for "auto mode".
- **Say it plain.** Direct, basic English. Short sentences. Lead with the answer.
- **Ask, never fill in.** A value you do not hold — URL, id, credential, expected result — comes from the user. Name the gap and ask.

## Project config

Env values, credentials, setup, `tasks/{KEY}/` layout, Jira and Testmo ids: read `.claude/steering/project-config.md`.

## Driving the UI

- **Locators are cached — read before you write one.** `.claude/locator-cache.json`: `wt-member-web` (member site, Playwright — desktop and mobile-web), `wt-app` (member app, Maestro), `wt-bo` (Back Office), `wt-root-admin` (Root Admin), `api` (endpoints). One `testID` string serves web, Android and iOS, so a screen verified in one section seeds the others. Every UI section nests its screens the same way, so one path reads any of them — never the whole file:
  ```bash
  jq '.["wt-member-web"].screens.login' .claude/locator-cache.json
  ```
  Add what you verify. Never cache a coordinate without the resolution it was measured at.
- **Reusable Maestro flows are cataloged — read before you write one.** `flows/flows-index.json`: one entry per flow/subflow — purpose, params, precondition, what it produces, verified status.
  ```bash
  jq '.app.flows | keys' flows/flows-index.json
  jq '.app.subflows["login"]' flows/flows-index.json
  ```
  Adding a flow means adding its index entry.
- **Logging in from scratch is a runbook, not guesswork.** Every surface — member site, member app from a cold device, Back Office, Root Admin — and every account type, including the CRM email-OTP path: `.claude/domain/login-flow.md`. URLs and account ids are the client's row in `.claude/steering/project-config.md` § Clients; passwords are in the yaml that file names, never in a plan or report.
- **One codebase, several clients.** Features, symbols, servers, theme and the app build differ per client, and a result is only true for its matrix point (env × client × server × account × platform). Check `.claude/domain/wt-shared.md` before calling a missing feature a bug.

## Repo

- `.claude/` is the source. After editing it, run `python3 sync-kiro.py` to regenerate `.kiro/`.
- `tasks/`, `reports/` are tracked, not ignored. Stage by explicit path.

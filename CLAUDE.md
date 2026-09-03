# CLAUDE.md

## Working rules

- **Skill adherence.** Run an invoked skill's phases in order. Complete every phase.
- **Approval before writes.** Propose the change — what, where, why — then wait for an explicit "yes"/"ok"/"go". Silence or a follow-up question is not approval. Covers `Write`, `Edit`, and any `Bash` that creates, moves, or deletes a file (`sed -i`, `>`, `>>`, `mv`, `rm`, `cp`, heredocs). Read-only operations are exempt. Suspended while the user has asked for "auto mode".
- **Say it plain.** Direct, basic English. Short sentences. Lead with the answer.
- **Ask, never fill in.** A value you do not hold — URL, id, credential, expected result — comes from the user. Name the gap and ask.

## Project config

Env values, credentials, setup, `tasks/{KEY}/` layout, Jira and Testmo ids: read `.claude/steering/project-config.md`.

## Driving the UI

- **Locators are cached — read before you write one.** `.claude/locator-cache.json`: `otc-bo` (BO web, Playwright), `bfg-otc-app` (member app, plus `android` commands and taps measured at one resolution), `api` and `memberApi` (endpoints). Both UI sections nest their screens the same way, so one path reads either — never the whole file:
  ```bash
  jq '.["otc-bo"].screens.membersList' .claude/locator-cache.json   # 34 tok, not 8,143
  ```
  Add what you verify. Never cache a coordinate without the resolution it was measured at.
- **Reusable Maestro flows are cataloged — read before you write one.** `flows/flows-index.json`: one entry per flow/subflow — purpose, params, precondition, what it produces, verified status.
  ```bash
  jq '.app.flows | keys' flows/flows-index.json
  jq '.app.subflows["select-network"]' flows/flows-index.json
  ```
  Adding a flow means adding its index entry.
- **Logging in from scratch is a runbook, not guesswork.** Member app from a cold device — boot the AVD, env gate, passcode, email OTP: `.claude/domain/login-flow.md`. BO web is `BO_URL` plus the credentials in `.claude/steering/project-config.md`.

## Repo

- `.claude/` is the source. After editing it, run `python3 sync-kiro.py` to regenerate `.kiro/`.
- `tasks/`, `reports/` are tracked, not ignored. Stage by explicit path.

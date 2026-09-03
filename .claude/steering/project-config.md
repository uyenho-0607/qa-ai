# Project Configuration

## Setting up this project

New machine, a helper failing with `ModuleNotFoundError`, or a missing MCP tool: read `SETUP.md`.
Tell the user to run `./onboarding.sh` themselves — it needs a terminal and refuses to start without one.

## Environment

| Variable | Value |
|----------|-------|
| `PROJECT_KEY` | `AO` |
| `BO_URL` | `https://dashboard.aqxotc-sit.s20ip12.com` — login at `/login` |
| `BO_MAKER` | `maimaker@yopmail.com` |
| `BO_CHECKER` | `maichecker@yopmail.com` |
| `BO_ADMIN` | `maiadmin@yopmail.com` |
| `MEMBER_APP_BUSINESS` | `mth2608@mailinator.com` |
| `SHARED_PASSWORD` | `Te5t1ng!` |
| `APP_PASSCODE` | `111111` — mobile app 6-digit passcode; one-time setup **per device**, not an account credential |
| `APP_ENV_GATE_EMAIL` | `aq@aq.com` — mobile app SIT environment unlock; one-time on a **fresh install** |
| `APP_PACKAGE` | `com.bfgto.sit.app` — mobile app under test, **SIT** build; React Native, same identifier on iOS and Android. Android launch activity `com.bfgtoapp.MainActivity`. |

OTC has one Back Office, not three apps — all three accounts share `BO_URL` and `SHARED_PASSWORD`.
Role capabilities: `.claude/domain/otc-bo.md` § Roles & Permissions.

API credentials (`JIRA_EMAIL`, `JIRA_API`, `GOOGLE_*`) live in `.env` at the repo root

A row still reading `<FILL_IN>` when a skill needs it → ask the user for the value. Never substitute a plausible one.

## Platforms

Every platform the exec skills may plan or run against. **This table is the only place a platform is declared.** A skill reads it, loads the pack for each enabled row, and never names a platform itself.

| Id | Label | Group | Pack | Enabled |
|---|---|---|---|---|
| `bo` | Back Office | web | `.claude/platforms/bo.md` | yes |
| `bo-mv` | Back Office (mobile view) | web | `.claude/platforms/bo.md` | no — not under test this cycle |
| `android` | Member app | device | `.claude/platforms/app.md` | yes |
| `ios` | Member app (iOS) | device | `.claude/platforms/app.md` | no — no iOS build exists |
| `app-web` | Member app (web) | web | `.claude/platforms/app.md` | no — URL not configured |

`Label` is what a human reads in `exec.md`. `Id` is what a file name and a locator cache use.

**Cross-platform flows** — a single test crossing two platforms in one execution — are available only when **two or more groups** are enabled. Pairs available here: `bo` + `android`.

**To disable a platform:** set Enabled to `no` with the reason. Its pack is never loaded and no TC is planned against it. **To add one:** write a pack from `.claude/platforms/TEMPLATE.md` and add a row here.

## Producers

An input file a skill needs but cannot find. The skill stops and names the producer — it never runs one, and never falls back to an MCP call or to chat context.

| Input | Producer |
|---|---|
| `tasks/{KEY}/base/jira.md` | `/jira-retriever {KEY}` with `save` |
| `tasks/{KEY}/base/tc.md` | `/collect-testmo-cases {KEY} save`, or `/collect-gsheet-cases {KEY} {sheet URL}` |

## Folder Structure

```
tasks/{KEY}/  Working files per ticket
  base/
    jira.md       Fetched Jira ticket content
    tc.md         Collected TCs from Testmo or Sheet
    attachments/  Downloaded Jira image attachments
    figma/
      figma-snapshot.md     Frozen Figma design snapshot
      figma-screenshots/    Exported Figma frame PNGs
  exec/
    exec.md    Execution plan
    report.md  Run report
    recon/        Recon screenshots
    evidence/     TC evidence screenshots and videos
    .upload/      Upload queue state and per-wave ledgers — written by `evidence-uploader`
  gen/            Only present when generate-tcs was run
    tc-plan.md    Coverage plan — one row per planned scenario
    manual-tcs.md Generated TCs
    tc-review.md  TC review report — coverage, oracle, repro, form

reports/{KEY}/  Coverage reports — commit if tracking history
```

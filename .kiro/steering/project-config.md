---
inclusion: always
---

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
| `TC_SHEET_ID` | `1vWynEv7nsgF-dTJ8QB2o9M1fUpQamEcr4xd1q_yxLqI` |

OTC has one Back Office, not three apps — all three accounts share `BO_URL` and `SHARED_PASSWORD`.
Role capabilities: `.kiro/domain/otc-bo.md` § Roles & Permissions.

API credentials (`JIRA_EMAIL`, `JIRA_API`, `GOOGLE_*`) live in `.env` at the repo root

A row still reading `<FILL_IN>` when a skill needs it → ask the user for the value. Never substitute a plausible one.

## Platforms

Every platform the exec skills may plan or run against. **This table is the only place a platform is
declared.** A skill reads it, loads the pack for each enabled row, and never names a platform itself.

| Id | Label | Group | Pack | Enabled |
|---|---|---|---|---|
| `bo` | Back Office | web | `.kiro/platforms/bo.md` | yes |
| `bo-mv` | Back Office (mobile view) | web | `.kiro/platforms/bo.md` | no — not under test this cycle |
| `android` | Member app | device | `.kiro/platforms/app.md` | yes |
| `ios` | Member app (iOS) | device | `.kiro/platforms/app.md` | no — no iOS build exists |
| `app-web` | Member app (web) | web | `.kiro/platforms/app.md` | no — URL not configured |

`Label` is what a human reads in `exec.md`. `Id` is what a file name and a locator cache use.

**Cross-platform flows** — a single test crossing two platforms in one execution — are available only when
**two or more groups** are enabled. Pairs available here: `bo` + `android`.

With one group enabled, cross-platform flows do not exist: no pairing, no two-session waves, no paired
results. Nothing needs switching off by hand.

**To disable a platform:** set Enabled to `no` with the reason. Its pack is never loaded and no TC is planned
against it. **To add one:** write a pack from `.kiro/platforms/TEMPLATE.md` and add a row here.

## Producers

An input file a skill needs but cannot find. The skill stops and names the producer — it never runs one, and
never falls back to an MCP call or to chat context.

| Input | Producer |
|---|---|
| `tasks/{KEY}/base/jira.md` | `/fetch-jira {KEY}` with `save` |
| `tasks/{KEY}/base/tc.md` | `/collect-testmo {KEY}` with `save`, or `/collect-gsheet` |

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
    exec-v2.md    Execution plan
    report-v2.md  Run report
    recon/        Recon screenshots
    evidence/     TC evidence screenshots and videos
  gen/            Only present when generate-tcs was run
    tc-plan.md    Coverage plan — one row per planned scenario
    manual-tcs.md Generated TCs
    manual-tcs.csv CSV export
    tc-review.md  TC review report — coverage, oracle, repro, form

reports/{KEY}/  Coverage reports — commit if tracking history

.kiro/platforms/  Platform packs — one per platform, loaded only when enabled
.kiro/domain/  App knowledge base — modules, URLs, UI rules
.kiro/domain/flows.md  `ui-discovery` flow file — behaviour, validation, transitions
.kiro/domain/login-flow.md  Mobile app login runbook — setup, OTP, device driving
.kiro/locator-cache.json  Cached locators — `otc-bo` web, `bfg-otc-app` mobile, `api` endpoints

scripts/  Helpers — run with `.venv/bin/python`
  mailtm_otp.py  Throwaway mail.tm inbox — `new` to create, `otp` to pull the code
  mailinator_otp.py  Public Mailinator inbox — `otp <address>` pulls the code, no setup
```

## Tools
Jira site, `cloudId`, project id, issue-type ids, and transitions: `.kiro/steering/jira.md`
Testmo project, config, and field ids: `.kiro/steering/testmo.md`

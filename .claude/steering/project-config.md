# Project Configuration

## Setting up this project

New machine, a helper failing with `ModuleNotFoundError`, or a missing MCP tool: read `SETUP.md`.
Tell the user to run `./onboarding.sh` themselves — it needs a terminal and refuses to start without one.

## Product

WT 3.0 — Aquariux **WebTrader**. One codebase serves several broker clients. Surfaces: member site
(desktop `/web`, mobile-web `/mobile`), native member app (React Native, iOS + Android), a **Back Office per
client**, one **global Root Admin**. Manual SIT project — no automation code lives here.
Domain: `.claude/domain/wt-shared.md` first, then the surface file the task needs.

## Environment

A result is only true for the **matrix point** it ran on: env × client × server × account × platform.
State all five with every result.

| Variable | Value |
|----------|-------|
| `PROJECT_KEY` | `WT` |
| `ENV` | `sit` — the only env this project tests. Every URL below is SIT |
| `CLIENT` | `transactCloud` — default client. Others in § Clients |
| `SERVER` | `mt5` — default server |
| `ACCOUNT` | `live` — default account type (`live` / `demo` / `crm`) |
| `MEMBER_URL` | `https://transactcloudmt5-mb.webtrader-sit.s20ip12.com` — desktop at `/web`, mobile-web at `/mobile` |
| `BO_URL` | `https://transactcloudmt5-backoffice.webtrader-sit.s20ip12.com` |
| `ROOT_ADMIN_URL` | `https://root.webtrader-sit.s20ip12.com/root` — global, same for every client. The trailing `/root` is what `config/sit.yaml` itself specifies (not a copy artifact); not yet round-tripped against the live server |
| `BO_USER` | `automation` |
| `ROOT_ADMIN_USER` | `automation` — pool `automation`, `automation2`, `automation3` |
| `MEMBER_LIVE` | `998771` — mt5 live account id (default client) |
| `MEMBER_DEMO` | `998771` — mt5 demo account id (default client) |
| `APP_PACKAGE` | `com.aquariux.wt.sit.transactcloudmt5` — SIT build, same id on iOS and Android. **Per env × client** — a different client or env is a different install |
| `MEMBER_PASSWORD` | `Autotest@12345` — every `live`/`demo` member account, every client, SIT |
| `MEMBER_PASSWORD_CRM` | `Auto@12345` — CRM (email-login) accounts, `lirunex` only |
| `BO_PASSWORD` | `Autotest@12345!` — every client's Back Office, SIT |
| `ROOT_ADMIN_PASSWORD` | `Autotest@12345!` |
| `WEB_APP_VIEWPORT` | `430×932` (iPhone 14 Pro Max) — the mobile-web layout |
| `CAPTCHA_SIT` | `123` — BO and Root Admin login captcha on any SIT env |

API credentials (`JIRA_EMAIL`, `JIRA_API`, `GOOGLE_*`) live in `.env` at the repo root.

A row still reading `<FILL_IN>` when a skill needs it → ask the user for the value. Never substitute a plausible one.

### Clients

The client changes URLs, servers, features, theme, and the app build. Pick the row the ticket names.

| Client key | Brand | Servers | Accounts | Member URL (SIT) | BO URL (SIT) | App package (SIT) |
|---|---|---|---|---|---|---|
| `transactCloud` | TransactCloud, **Hantec** (brand runs on this key) | mt5 | live `998771`, demo `998771` | `transactcloudmt5-mb.webtrader-sit.s20ip12.com` | `transactcloudmt5-backoffice.webtrader-sit.s20ip12.com` | `com.aquariux.wt.sit.transactcloudmt5` |
| `lirunex` | Lirunex | mt4, mt5 | mt4 live/demo `2092010247`, crm `mt4_automation40@mailinator.com`; mt5 live/demo `569202036`, crm `mt5_automation45@mailinator.com` | `lirunex-global-mb.webtrader-sit.s20ip12.com` | `lirunex-backoffice.webtrader-sit.s20ip12.com` | `com.aquariux.wt.sit.lirunex` |
| `centroid` | Centroid (**TinShing** on UAT) | mt4, mt5, s1, s2 | mt4/mt5 live/demo `100000088`; s1/s2 `<FILL_IN>` — TODO in source | `centroid-mb.webtrader-sit.s20ip12.com` | `centroid-backoffice.webtrader-sit.s20ip12.com` | `<FILL_IN>` — none on SIT in source |
| `hantec` | — | — | — | no SIT config exists — test the Hantec brand on `transactCloud` | | |

Rules that follow from the row: CRM accounts exist on `lirunex` only. `s1`/`s2` exist on `centroid` only.
Multi-OMS clients = `lirunex`, `centroid`; non-OMS = `transactCloud` (stop-limit orders are non-OMS only).
Details and gates: `.claude/domain/wt-shared.md`.

## Platforms

Every platform the exec skills may plan or run against. **This table is the only place a platform is declared.** A skill reads it, loads the pack for each enabled row, and never names a platform itself.

| Id | Label | Group | Pack | Enabled |
|---|---|---|---|---|
| `web` | Member site (desktop) | web | `.claude/platforms/member-web.md` | yes |
| `web-app` | Member site (mobile web) | web | `.claude/platforms/member-web.md` | yes |
| `android` | Member app (Android) | device | `.claude/platforms/app.md` | yes |
| `ios` | Member app (iOS) | device | `.claude/platforms/app.md` | yes |
| `bo` | Back Office | web | `.claude/platforms/bo.md` | yes |
| `root-admin` | Root Admin | web | `.claude/platforms/root-admin.md` | yes |

`Label` is what a human reads in `exec.md`. `Id` is what a file name and a locator cache use.

Feature availability differs by platform — Price Alert, Copy Trade, Home, Menu exist on `web-app` and the
app only; Quoteboard DOM, Chart panel, Settings dropdown exist on `web` only. The table in
`.claude/domain/wt-member-site.md` § Feature × platform decides which rows a TC gets.

**Cross-platform flows** — a single test crossing two platforms in one execution — are available only when **two or more groups** are enabled. All six rows are enabled, so any `web`-group platform (`web`, `web-app`, `bo`, `root-admin`) can pair with any `device`-group platform (`android`, `ios`). Admin-then-member checks (BO or Root Admin change → member site assert) are the common WT case: `.claude/domain/wt-admin.md` § Cross-surface recipes.

**To disable a platform:** set Enabled to `no` with the reason. Its pack is never loaded and no TC is planned against it. **To add one:** write a pack from `.claude/platforms/TEMPLATE.md` and add a row here.

## Producers

An input file a skill needs but cannot find. The skill stops and names the producer — it never runs one, and never falls back to an MCP call or to chat context.

| Input | Producer |
|---|---|
| `tasks/{KEY}/base/jira.md` | `/jira-retriever {KEY}` with `save` |
| `tasks/{KEY}/base/tc.md` | `/collect-testmo-cases {KEY} save`, or `/collect-gsheet-cases {KEY} {sheet URL}` |

WT Testmo cases do not carry the Jira key in `custom_reqreference` — issue-key lookup returns nothing.
`collect-testmo-cases` resolves by folder and case name, or by the `WT-xxxx_TC-xx` label: `.claude/steering/testmo.md`.

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

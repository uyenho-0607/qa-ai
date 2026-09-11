# WT 3.0 — shared facts

WT 3.0 is Aquariux WebTrader: a white-label trading front end sold per client (tenant). Every other WT doc assumes this file. Trading rules: `.claude/domain/wt-trading.md`. Member-site screens: `.claude/domain/wt-member-site.md`. Back Office and Root Admin: `.claude/domain/wt-admin.md`. TC naming: `.claude/domain/tc-naming-ref.md`. Logging in: `.claude/domain/login-flow.md`.

Sources are cited as `(src: ref-project/qa-automation-wt-3-0/<path>:<line>)`.

## Surfaces

| Surface | Where | Scope | Login |
|---|---|---|---|
| Member site, desktop | `{base_url}/web` | per client | account tab + id + password (src: `src/page_object/member_site/web/base_page.py:74`) |
| Member site, mobile-web | `{base_url}/mobile` at viewport 430×932 ("iPhone 14 Pro Max") | per client | same form, phone layout (src: `web_app/base_page.py:70`, `src/data/consts.py:38`) |
| Native app (iOS + Android) | one install per env × client, e.g. `com.aquariux.wt.sit.lirunex` | per client | same form + ads skip + Remember me (src: `config/sit.yaml:32`) |
| Back Office (BO) | `{client}.back_office.url` | per client | username + password + captcha (src: `src/api/webtrader/back_office/auth.py:44`) |
| Root Admin | `root_admin.url` — one URL for all clients | global | username + password + captcha (src: `config/sit.yaml:5-8`) |
| Centroid bridge (demo_bridge) | `centroid.demo_bridge.url` | Centroid only | bridge admin login, needs `x_forward_client` (src: `src/api/centroid/admin/auth.py:25-33`) |

Prod rule: BO and Root Admin are off limits on prod. The automation refuses to even log in there (src: `src/api/client.py:92,102`). On prod, test the member site only.

Mobile-web is the member site, not the app. Same URL as desktop, different layout — never judge a phone-layout bug from the desktop render.

## The matrix

Every WT fact and every WT result lives at one point of env × client × server × account × platform.

| Axis | Values | Automation default |
|---|---|---|
| env | `sit`, `release_sit`, `uat`, `prod` | `release_sit` (src: `pytest.ini`) |
| client | `lirunex`, `transactCloud`, `centroid`, `hantec` | `transactCloud` |
| server | `mt4`, `mt5`, `s1`, `s2` | `mt5` |
| account | `live`, `demo`, `crm` | `live` |
| platform | `web` (desktop), `web_app` (mobile-web), `ios`, `android` | — |

Which combinations exist:

| Client | Servers | Account types | Login tabs the tenant may show (Root Admin login config) |
|---|---|---|---|
| lirunex | mt4, mt5 | live, demo, crm | COMPANY (CRM) + MT4 live/demo + MT5 live/demo (src: `src/api/webtrader/root_admin/company.py:198-203`) |
| transactCloud | mt5 | live, demo | MT5 live/demo only (src: `company.py:204`) |
| centroid | s1, s2 (mt4/mt5 ids also present in config) | live, demo | CENTROID live/demo only (src: `company.py:205-207`) |
| hantec | mt5 in code | live, demo | `<not in source>` — no Root Admin login config, no yaml block (src: `src/data/enums/system.py:11`) |

- CRM exists only on lirunex. `crm` is "multi-OMS only" (src: `src/data/enums/system.py:51`).
- `s1`/`s2` are Centroid-only. Any other client with s1/s2 is an invalid point (src: `src/data/data_runtime.py:25-29`).
- Server labels in the UI: mt4 → `TS4`, mt5 → `TS5`, s1/s2 → `Centroid` (src: `src/data/enums/system.py:43`, `data_runtime.py:137`).

## SIT per client

Passwords: see `ref-project/qa-automation-wt-3-0/config/sit.yaml` (never copy them into a doc, comment, or report).

| | lirunex | transactCloud | centroid |
|---|---|---|---|
| Member site | `https://lirunex-global-mb.webtrader-sit.s20ip12.com` | `https://transactcloudmt5-mb.webtrader-sit.s20ip12.com` | `https://centroid-mb.webtrader-sit.s20ip12.com` |
| Back Office | `https://lirunex-backoffice.webtrader-sit.s20ip12.com`, user `automation` | `https://transactcloudmt5-backoffice.webtrader-sit.s20ip12.com`, user `automation` | `https://centroid-backoffice.webtrader-sit.s20ip12.com`, user `automation` |
| App package / bundle | `com.aquariux.wt.sit.lirunex` | `com.aquariux.wt.sit.transactcloudmt5` | `<not in source>` — no app on SIT |
| mt4 crm / live / demo | `mt4_automation40@mailinator.com` / `2092010247` / `2092010247` | — | `100000088` / `100000088` (no crm) |
| mt5 crm / live / demo | `mt5_automation45@mailinator.com` / `569202036` / `569202036` | `998771` / `998771` (no crm) | `100000088` / `100000088` (no crm) |
| s1 live / demo | — | — | `<not in source>` — TODO in yaml (src: `config/sit.yaml:79-80`) |
| s2 live / demo | — | — | `<not in source>` — TODO (src: `config/sit.yaml:83-84`) |
| demo_bridge | — | — | url, admin, `x_forward_client` all empty on SIT (src: `config/sit.yaml:62-66`) |

Root Admin on SIT: `https://root.webtrader-sit.s20ip12.com/root`, users `automation`, `automation2`, `automation3` (src: `config/sit.yaml:6-8`). The trailing `/root` exists only on SIT.

SIT gaps, all real: Centroid s1/s2 ids TODO; Centroid demo_bridge empty; no Centroid app on SIT; no Hantec block in any yaml. For Centroid s1/s2 or the bridge, use `release_sit` or `uat` (src: `config/release_sit.yaml`, `config/uat.yaml`).

Other envs: `release_sit` and `uat` hold the full set (ids, serverIds, tenant ids). `prod` has member URLs for lirunex only; BO/Root Admin empty; its app package is still the SIT one — a config bug (src: `config/prod.yaml`).

## Client ↔ brand aliases

Client key is not the brand name. Two known cases:

| Brand seen in tickets / sheets | Config key | Evidence |
|---|---|---|
| Hantec | `transactCloud` | "The sheet names the tenant 'Hantec'; the configs key it transactCloud" (src: `src/data/consts.py:136`); the one Hantec-branded test runs under transactCloud (src: `tests/web_app/assets/insights/styling/test_AST_INS_STL_TC01_positive_ring_chart_styling.py:13`) |
| TinShing | `centroid` on UAT | `https://tinshing-mb.webtrader-uat.s20ip12.com`, bundle `com.aquariux.wt.uat.tinshing`, tenant id 37 (src: `config/uat.yaml:55-59`, `company.py:83`) |

Centroid on UAT also uses a distinct BO account, `aqadmin`, not `automation` (src: `config/uat.yaml:60`). Root Admin tenant ids: lirunex 2; transactCloud 23 (release_sit) / 22 (uat); centroid 65 (release_sit) / 37 (uat) (src: `company.py:80-84`).

## Multi-OMS vs non-OMS

- Multi-OMS clients: lirunex, centroid. Non-OMS: transactCloud, hantec (src: `src/data/consts.py:40`, `data_runtime.py:126`).

| What changes | Multi-OMS (lirunex, centroid) | Non-OMS (transactCloud, hantec) |
|---|---|---|
| Stop Limit order type | absent | offered (MT5 only) (src: `src/data/enums/trading.py:180,191`) |
| Bulk delete "Stop Limit Orders" option | absent | present (src: `trading.py:461`) |
| Cross-server account linking (Manage Account) | possible, non-CRM only | one server, nothing to cross (src: `tests/web_app/menu/manage_account/test_MNU_MGA_TC04_positive_link_account_cross_servers.py:12`) |
| BO config writes | apply to `serverId=0` = all servers | no serverId (src: `src/api/webtrader/back_office/config.py:28-56`) |

Centroid is multi-OMS *and* a different execution model (netting, no SL/TP at placement, Time In Force, Position ID). Those rules live in `.claude/domain/wt-trading.md`.

## Account types

| | live | demo | crm |
|---|---|---|---|
| Login id | numeric account id | numeric account id | email, e.g. `mt4_automation40@mailinator.com` (src: `config/sit.yaml:23`) |
| Password set | `password` | `password` | `password_crm` (src: `data_runtime.py:83-85`) |
| Id placeholder | "Enter your account ID" | same | "Enter your email / username" (src: `src/data/ui_messages.py:12-13`) |
| OTP after login | no | no | yes, 6-digit email OTP (src: `web/pages/crm_otp_page.py:17`) |
| Manage Funds menu | shown | hidden | shown (src: `src/data/enums/ui.py:360`) |
| Open Demo Account menu | shown | hidden | shown (src: `ui.py:374`) |
| Notifications | yes | none — demo gets no notifications (src: `tests/web/trade/settings/test_TRD_SET_TC09_positive_notification_settings.py:7`) | yes |
| Account-type badge on Home/Trade | LIVE | DEMO | LIVE (src: `web_app/pages/home_page.py:150`) |
| Cross-server linking | yes (multi-OMS) | yes | no |

Live and demo often share the same id on SIT (e.g. lirunex mt4 `2092010247` for both). The tab you pick decides the account type.

## Constants a tester checks against

| Fact | Value | Source |
|---|---|---|
| Change-password policy | 12–20 chars, 1 upper, 1 lower, 1 digit, 1 special; not one of the last 5 | `src/data/ui_messages.py:58-59` |
| CRM sign-up password length | "8-12 characters" — differs from change-password | `ui_messages.py:26` |
| OTP resend cooldown | 120 s; timer starts at `02:00`; "An OTP was recently sent to you. Please try again after 2 minutes." | `src/data/consts.py:25`, `ui_messages.py:32` |
| OTP expiry | 300 s; "Your OTP is expired." | `consts.py:26`, `ui_messages.py:34` |
| Wrong OTP | "The code you entered is incorrect, please try again." | `ui_messages.py:30` |
| Wrong login | "Invalid credentials, please try again." | `ui_messages.py:9` |
| Languages (12) | English `en_GB`, 简体中文 `zh_CN`, 繁体中文 `zh_TW`, ภาษาไทย `th_TH`, Tiếng Việt `vi_VN`, Bahasa Indo `id_ID`, Bahasa Melayu `ms_MY`, 日本語 `ja_JP`, 한국어 `ko_KR`, Português `pt_BR`, Español `es_ES`, Arabic `ar_AE` | `src/data/enums/account.py:12-44` |
| Arabic gap | no reference strings for Place Order button, Buy Limit, Sell Limit — expected text `<not in source>` | `account.py:46` |
| Server timezone (pending expiry, trading hours) | lirunex UTC+0; transactCloud UTC+3; hantec UTC+3; centroid UTC+0 ⚠ unverified — source says "recheck for centroid" | `consts.py:43-48` |
| Theme base colour | lirunex `#54a0b6`, centroid `#ff8000`, transactCloud `#4a94c8`, hantec `#f40000` | `consts.py:60` |
| Hidden-balance mask | balance 17 `*`; last price 10 `*`; every other value 8 `*` | `consts.py:148-150` |
| Search history | 5 most recent symbols | `consts.py:154` |
| Bulk delete cap | "Note: A maximum of 30 %s will be deleted." | `ui_messages.py:133` |
| Pinned account-info items | max 3: "You can pin up to 3 items." | `ui_messages.py:144` |

## Rules for every WT result

- **Record the matrix point with every result.** "Broken on transactCloud / mt5 / live / release_sit, Android." A finding without env, client, server, account, platform cannot be reproduced by anyone (src: `.claude/lessons/manual-task-lessons.md`).
- **Reproduce on the client the report names.** Features, symbols, theme, and enabled tabs differ per client. A pass on lirunex says nothing about centroid.
- **Check the client and account type before calling a feature missing.** Stop Limit, CRM, cross-server linking, Manage Funds, notifications, quoteboard cards are each legitimately absent somewhere. Match the tables above first.
- **A missing feature on the app is a build mismatch until the package check says otherwise.** `...sit.lirunex` and `...release.lirunex` are different installs (src: `.claude/docs/appium-rule.md`).
- **Set the phone viewport for mobile-web.** 430×932. Same URL, different UI.
- **Replay the launch ritual on the app.** Skip ads, dismiss "Got it", relaunch. Session and onboarding state survive between launches.
- **Record the observed live price and time.** Market data moves; a price-based expectation is unverifiable without it.
- **Record device model and OS version.** Screen size changes what is scrolled out of view.
- **Same testid string across all four platforms, but the four trees diverge.** An Android answer does not settle a web question.
- **Expected values that vary by client come from the client-keyed table, never a hardcoded one.** Colours, timezone, labels.
- **BO and Root Admin writes leak.** Changing a company or symbol setting hits every tester on that client. Read the current value first, restore it after (src: `.claude/docs/fixture-conventions.md`).
- **Assert the requirement, not the current behaviour.** A wrong value that the app shows today is a bug, not an oracle.
- **Market order is three clicks.** BUY sets direction → Place Order → Confirm.
- **Bugs go to Jira `WT` as `SIT Bug` subtasks, whatever env found them.** Summary `[WT][{ENV or Module}] {symptom}`; name the client when client-specific (src: `.claude/docs/jira.md`).

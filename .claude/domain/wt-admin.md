# WT 3.0 — admin surfaces (Back Office, Root Admin, Centroid bridge)

An admin setting is a **shared lever**: one change hits every tester on that client. Read the value, change it, check the member site, put the value back. Matrix, URLs, tenant ids, per-client login-config sets: `.claude/domain/wt-shared.md`. Member-site screens: `.claude/domain/wt-member-site.md`.

The automation drives BO and Root Admin through the API only. UI paths below are `<UI path not in source — discover on live app>` unless stated. Each capability names the API field so you can confirm the change with a network response or the JSON the member site loads.

## Surfaces

| Surface | Scope | API base | Login |
|---|---|---|---|
| Back Office (BO) | one per client | `{back_office.url}/api/admin` | username + password + image captcha (src: `ref-project/qa-automation-wt-3-0/src/api/webtrader/back_office/auth.py:21,43-52`) |
| Root Admin | one global URL; pick the client by tenant = company id per client × env | `{root_admin.url}/api/root` | same captcha flow (src: `src/api/webtrader/root_admin/auth.py:20,42-52`) |
| Centroid bridge admin | Centroid only; `demo_bridge` — url, admin user and `x_forward_client` all empty on SIT | `{centroid.demo_bridge.url}` | username + password, `auth_step: 1`; every call carries header `x-forward-client` (src: `src/api/centroid/admin/auth.py:25-33`) |

Login and session rules:

- Captcha code is `123` on any env whose name contains `sit` (`sit`, `release_sit`); it is a real image on `uat` (src: `back_office/auth.py:44`, `src/data/data_runtime.py:161-162`). The captcha `cryptograph` is single-use — a failed login needs a fresh captcha (src: `back_office/auth.py:42`).
- Userids are pools (`automation`, `automation2`, …) in `config/{env}.yaml` — any one works. Credentials live in the config, never in a report.
- Session: `POST /auth/v1/session` says whether the token is still valid; when it is not, log in again (src: `back_office/auth.py:61-66`). Expiry duration: `<not in source>`. The bridge has no session check, only re-login (src: `centroid/admin/auth.py:19`).
- Prod: BO and Root Admin are refused outright (src: `src/api/client.py:92,102`). No admin writes on prod, ever.

## Root Admin — company settings

Every write is a read-modify-write of the whole company object (`GET /company/v2/detail?companyId={tenant}` → `PUT /company/v2`, 70+ fields) (src: `src/api/webtrader/root_admin/company.py:88-89,154-164`). The member site reads the result from `GET /api/config/v1/company` (login configs) and `GET /api/config/v1/company/user` (features, flags). After a change: reload the member site; for subscription changes, log out and in again.

| Capability | Field · values | Member-site effect | Verify |
|---|---|---|---|
| Login config tabs | `loginConfigs`: `COMPANY`, `METATRADER4_LIVE`, `METATRADER4_DEMO`, `METATRADER5_LIVE`, `METATRADER5_DEMO`, `CENTROID_LIVE`, `CENTROID_DEMO` (src: `company.py:55-63`). Allowed set per client is in wt-shared. | Account-type tabs on the login screen (live / demo / crm). ⚠ unverified — no test toggles a login config and asserts the tabs. | Login screen tab set; `loginConfigList` in `GET /api/config/v1/company`. |
| Features | `featureList`: `ACCOUNT_CLOSURE`, `CUSTOMER_SERVICE`, `CHANGE_PASSWORD`, `PIE_CHART`, `FORGOT_PASSWORD`, `RESET_PASSWORD`, `TOP_PICK`, `TOP_GAINER`, `TOP_LOSER` (src: `company.py:13-21`). **Destructive: any feature left out of the saved list is disabled** (src: `company.py:241-242`). | `TOP_PICK` / `TOP_GAINER` / `TOP_LOSER` → Market Mover tabs `Top Pick` / `Top Gainer` / `Top Loser` on Markets › Explore and Home. All three off → the Market Mover section is hidden (src: `company.py:30-34`; `tests/web_app/markets/explore/test_MKT_EXP_TC01_positive_display_feature_tabs.py`). Effect of the other six: `<not in source>`. | Reload; count tabs; first enabled tab is selected and painted the theme colour. |
| Supported languages | `supportedLanguages`, 12 locales: `en_GB zh_CN zh_TW th_TH ms_MY id_ID ja_JP ko_KR ar_AE es_ES pt_BR vi_VN` (src: `company.py:41-52`). Same destructive rule (src: `:277-278`). | Language dropdown on the login screen lists only the saved locales; `Sign in` and `Log out` labels translate (src: `tests/web_app/login/test_LGN_TC04_positive_change_language.py`). | Reload login screen; open dropdown; pick one; log in; check Menu › Log out label. |
| Default language | `defaultLanguage`, one of the 12 (src: `company.py:295-309`) | Language shown before the user picks one. ⚠ unverified — no test asserts. | Clear site data, open login screen. |
| Logout URL | `webtraderMemberLogoutUrl`, any URL or empty (src: `company.py:328-341`) | Where the browser goes after Log out. Tests only clear it to keep the CRM OTP flow on-site. ⚠ unverified — no test asserts a redirect. | Log out; note the landing URL. |
| Theme colour | `themeColourCode`, CSS hex. Defaults: lirunex `#54a0b6`, centroid `#ff8000`, transactCloud `#4a94c8`, hantec `#f40000` (src: `src/data/consts.py:60`) | Accent colour — e.g. the selected Market Mover tab background (src: `test_MKT_EXP_TC01…:test_enable_multiple_tabs`). | Reload; inspect the selected tab's background. |
| Market watch | `marketTime`, boolean (src: `company.py:435-439`) | `<not in source>` | — |
| Market timezone | `marketTimeManagement`: `SERVER` or `CLIENT` (src: `company.py:66-69,446-450`) | Symbol spec › Trading Hours › `Time Display`: `SERVER` → `GMT +N` (N = current Europe/Helsinki offset, 2 or 3), Centroid shows `Server Time`; `CLIENT` → `Local Time` and session times in the device zone (src: `src/data/enums/trading.py:133-157`). Open/closed behaviour: ⚠ unverified — fixture exists, no test uses it. | Reload; open a symbol's specification; read the Trading Hours block. |
| Server validation priority | `serverValidationPriority`: ordered list of serverIds (src: `company.py:388-403`); ids per server in `serverResponseList[].serverId` keyed by `mainProductCode` + `account` (src: `:371-386`) | Same account id and same password on two servers → login lands on the first server in the list. Different passwords → the password decides (src: `tests/web_app/login/test_LGN_TC05_positive_server_priority.py`). Also the precondition for cross-server link tests: linking the same account twice → `Account already linked` (src: `tests/web_app/menu/manage_account/test_MNU_MGA_TC06_negative_link_account_errors.py`). | Log in; Home › account name shows the server (test accounts read `MT4 Automation` / `MT5 Automation`). |
| Client ID range | per server `idRangeMin` / `idRangeMax` in `companyServerRequestList`; non-OMS clients also `liveIdRangeMin/Max`, `demoIdRangeMin/Max` at company level (src: `company.py:407-431`). ⚠ unverified — Centroid range cannot be updated (TODO, `:419`). | Account id inside the range → normal login. Outside → expected `Invalid credentials`, but the negative case is disabled "to avoid kicking out active accounts" — ⚠ unverified (src: `tests/web/login/test_LGN_TC07_positive_clientID_range.py:11`). | Reload login; log in; land on Trade (Quote for Centroid). |
| Registration URL | `companyRegistrationUrl` plus per platform/account: `{live\|demo}RegistrationUrl`, `…RegistrationAndroidUrl`, `…RegistrationIosUrl` (src: `company.py:483-491`) | Sign-up link on the login screen opens this URL. | Click Sign up; compare the landing URL. |
| Manage funds URL | `webtraderLivePaymentRedirectUrl` (src: `company.py:496-508`). Neighbouring fields exist but are not written: `webtraderDemoPaymentRedirectUrl`, `fundManagement`, `webtraderPaymentType` (src: `:159`). **The only funding-related setting. No deposit or balance API exists on any surface.** | Menu › Manage Funds redirect target. ⚠ unverified — no test asserts. | Tap Manage Funds; compare URL. Balances cannot be set from admin — use an account that already has funds. |
| Reset / forgot password | `webtraderResetPasswordType` + `webtraderResetPasswordUrl`, `crmForgotPasswordType` + `crmForgotPasswordUrl`, `crmChangePasswordType` (src: `company.py:158-159`); flags `FORGOT_PASSWORD`, `RESET_PASSWORD` in features. Allowed values: `<not in source>`. | Forgot-password link on login. Mapping from type to behaviour: `<not in source>`. | Click Forgot password; note the destination. |
| View-only login | `enableViewOnlyLogin`, boolean; read only in source (src: `company.py:184-195`) | CRM user with no active trading account: `true` → logs in and lands on the Trade page; `false` → message `No active trading account` on the login screen (src: `tests/web_app/login/crm_login/test_LGN_CRM_TC05….py:45-56`). | CRM OTP login with such a user. |
| Copy trade subscription | `companySubscriptionList[productCode=COPY_TRADE].productSubscription`: `FREEMIUM` or `PREMIUM` (src: `company.py:72-75,541-561`) | `FREEMIUM` → Copy Trade page shows the `Express Interest` button; takes effect after log out / log in (src: `tests/web_app/copy_trade/test_CT_TC04_positive_express_interest.py`). `PREMIUM` effect: ⚠ unverified. | Re-login; Menu › Copy Trade. |
| Copy trade config | `copytradeBrokerCode` (e.g. `Pelican`), `copytradeOAuthClientIdWeb`, `copytradeOAuthClientIdMobile`; saving also adds `COPY_TRADE` to `subProductCodeList` and a `PREMIUM` subscription entry if missing (src: `company.py:563-597`) | `copyTradeEnabled` / `COPY_TRADE` in `companyConfigEnabledFlagList` on the member site → Copy Trade menu item and Pelican OAuth login. | `GET /api/config/v1/company/user`; Menu › Copy Trade. |
| Sub products | `subProductCodeList`: `DEALER`, `TRADING_VIEW`, `CALENDAR`, `SIGNAL`, `NEWS`, `EDUCATION`, `QUOTE_BOARD`, `COPY_TRADE` (src: `src/data/enums/ui.py:291-300`) | Menu shortcuts: `CALENDAR` → `Calendar` (More), `SIGNAL` → `Signals` (Trade), `NEWS` → `News` (More), `EDUCATION` → `Learn` (More). `DEALER`, `TRADING_VIEW`, `QUOTE_BOARD`, `COPY_TRADE` render no shortcut through this mapping (src: `ui.py:303-328`). No write wrapper in source. | Menu page; each shortcut opens a page with the same title. |

## Back Office — per-client settings

`serverId` rule for BO calls: `None` for a non-OMS client (transactCloud), `0` = all servers for multi-OMS clients (lirunex, centroid) (src: `src/api/webtrader/back_office/config.py:28,42,50,56`; `src/data/consts.py:40`). Symbol reads and writes use the concrete serverId of the server × account (`SERVER_ID`, release_sit and uat only), except transactCloud which sends none (src: `back_office/configuration.py:16-20`; `consts.py:214-228`).

| Capability | Field · values | Member-site effect | Verify |
|---|---|---|---|
| Pretrade details | `POST /backoffice/config/v1/pretrade` `enablePretradeDetails`, `showEstimatedMarginRequired`; turning pretrade off also turns est. margin off (src: `config.py:18-28`) | Trade form "trade details" section shown/hidden; `Est. Margin Required` row inside the expanded section (src: `tests/web_app/trade/form/test_TRD_FRM_TC02_positive_enable_disable_pretrade_details.py`). Needs a reload. | Open a trade form; expand trade details. |
| One-click trading (company) | `POST /backoffice/config/v1/oct`, multipart field `enableOneClickTrading` `true`/`false`; `GET` reads it per serverId (src: `config.py:35-43`) | Company gate for OCT; the user then switches OCT in their own preference (src: `tests/web_app/trade/form/conftest.py:13-19`). Toggle hidden when off: ⚠ unverified — every test only turns it on. | Menu › OCT / Settings toggle present; OCT trade form places without confirm. |
| Quoteboard config | `GET /backoffice/config/v1/quoteboard` (src: `config.py:53-57`). Write fields: `<not in source>`. | Quote page cards. | — |
| Price alert | `GET/POST /backoffice/config/v1/price-alert` `isEnabled` (src: `config.py:59-73`) | On → bell icon on Trade Analysis opens `Price Alert Management`; `Price Alerts` tab in Notifications. Off → both gone (src: `tests/web_app/price_alert/test_ALR_TC23_positive_bo_price_alert_setting.py`). Needs a reload. | Trade › Analysis; Home › notification bell. |
| Copy trade | `PUT /backoffice/config/v1/copytrade` `isEnabled`, `config.strategyListShowInMemberSite` (default `All`, `EarlierCopied`, `FavouriteSignals`, `TopFreeSignals`), `isCacheStrategyEnabled`, `cacheStrategyConfig.ttl` (src: `config.py:77-99`) | Copy Trade feature and its strategy sections. ⚠ unverified — no test asserts after a toggle. | Menu › Copy Trade sections vs the list saved. |
| Contact info | `GET /config/v2/company/contact`: `email`, `mobile`, `dialCode`, `socialMedia`, `businessHours` — the source of truth (src: `config.py:45-51`). Write path: `<not in source>`. | Menu › Contact Us shows the same values. | Compare field by field. |
| Symbols | `GET/PATCH /configuration/v2/symbols`, per item `isEnable`, `isPopular`, `isEnableQuoteBoard` (with `type`, `symbol`, `account`) (src: `configuration.py:27-63`). **No symbol creation** — only toggles. Centroid symbol names are `FEED\|SYMBOL` (src: `:45-48`). | `isEnable` → symbol listed and tradeable; `isPopular` → `Popular` watchlist tab; `isEnableQuoteBoard` → card on the desktop Quote page (Centroid). | Markets search; watchlist tabs; Quote page. |

## Centroid bridge admin

| Capability | Call | Member-site effect | Verify |
|---|---|---|---|
| Taker symbol config (Takers › TEM) | `GET /v1/node/account/symbol?node_account=` — UAT uses the feed name `SIT_S1`/`SIT_S2`, other envs the account id; `PUT /v1/node/account/symbol_bulk` with `symbol_val`, `min_volume`, `max_volume`, `digits`, each item carrying `old_data` (src: `src/api/centroid/admin/takers.py:11-82`) | Quote page › Default Trade Volume: raising bridge min above a saved default (or max below it) → snack bar `Some symbols have invalid default quantities. UPDATE`, red dot on the Default Trade Volume icon, tooltip `One or more symbol's minimum quantity was updated. Adjust your default quantity.`, error under the symbol (src: `tests/web/quote/default_trade_volume/test_QBD_DTV_TC05….py`) | Wait ~8 s, refresh; sync is slow — up to 5 refreshes. |
| Market watch quotes | `POST /v1/trading/market_data?page=market_watch`, `feed_symbols: ["FEED||SYMBOL"]` (src: `centroid/admin/trading.py:11-21`) | Reference bid/ask for the member Quote board. | Compare against member prices at the same second. |
| Order report (member login) | `POST /v1/report/order` → CSV: `cen_ord_id, party_symbol, side_value, ord_type_value, time_in_force_value, state, price, avg_price, volume_value, fill_volume_value, notional, recv_time_value` (src: `centroid/member/report.py:14-39`) | Bridge-side record of member orders. | Cross-check member order history against the CSV. |

## Cross-surface recipes

Every recipe: read and note the original value → change → reload member site → check → restore the noted value.

| Pattern | Precondition | Admin step | Member-site expectation | Restore |
|---|---|---|---|---|
| Server priority → login | Multi-OMS client; account exists on two servers with the same id and password | Root Admin: move server X first in `serverValidationPriority` | Login lands on server X (account name shows it). Different passwords → password decides. | Original order |
| Feature tabs → Markets / Home | Any client, not prod | Root Admin features: keep only chosen `TOP_*`; keep the other six as they were | Markets › Explore and Home Market Mover show exactly those tabs; none → section hidden; first tab selected in theme colour | Original `featureList` |
| Logout URL + view-only → CRM OTP | lirunex crm; CRM OTP account; note `enableViewOnlyLogin` | Root Admin: `webtraderMemberLogoutUrl` = empty | OTP flow stays on site; after OTP: view-only on → Trade page, off → `No active trading account` | Original URL |
| Languages → login / menu | Any client | Root Admin: save the full 12-locale list | Login dropdown lists all 12; `Sign in` → login → Menu `Log out` both translated | Original list |
| Market timezone → Trading Hours | Any client | Root Admin: `marketTimeManagement` = `CLIENT` | Symbol spec Trading Hours `Time Display` = `Local Time`; `SERVER` → `GMT +N` (Centroid `Server Time`) | Original value |
| Theme colour → styling | Any client | Root Admin: `themeColourCode` = client default | Selected tabs / accents match the hex | Original hex |
| Price alert toggle | Mobile or web_app | BO price alert `isEnabled` off | Bell icon gone from Trade Analysis; `Price Alerts` tab gone from Notifications; on → both back | `true` |
| Pretrade toggle | Any client | BO pretrade off, then on with est. margin off | Trade details section hidden; then visible without `Est. Margin Required` | Both `true` |
| Quoteboard symbol patch | Centroid, desktop web | BO symbols: `isEnableQuoteBoard` false for all current cards | Quote page shows no cards; patch one back → one card | Original card list |

## Rules

- **Restore the original you read, not a default.** Admin writes hit every tester on that client (src: `ref-project/qa-automation-wt-3-0/.claude/docs/fixture-conventions.md`).
- **Log every admin change in the run report**: env, client, tenant id, server/serverId, field, old value, new value, restored at.
- **Never write on prod.** Prod runs are member-site only.
- **Features and languages are whole-list saves.** Start from the current list; add or remove only your item.
- **Reload before you judge.** Company config is read at load; subscription changes need a fresh login.

## Known gaps and drift

- SIT Root Admin URL ends in `/root`; the API base adds `/api/root` on top (`…/root/api/root`). Other envs have no suffix (src: `config/sit.yaml:7`).
- Concrete serverIds and tenant ids exist only for `release_sit` and `uat` (src: `consts.py:214-228`; `company.py:80-84`). On `sit`, read the ids from the Root Admin company detail.
- hantec has no login-config set, tenant id, serverId or yaml block (src: `company.py:198-208`).
- `sit` Centroid bridge is unconfigured; bridge recipes run on `release_sit` / `uat` only (src: `config/sit.yaml:63`).
- Client ID range write always also sets the company-level range because `is_non_oms` is called without `()` (src: `company.py:424`) — expect both to change.

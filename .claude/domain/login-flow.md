# WT login runbook

How to get from a cold surface to a logged-in screen, per surface. URLs, ids, and the matrix are in `.claude/domain/wt-shared.md`; credentials in `ref-project/qa-automation-wt-3-0/config/{env}.yaml`. Sources cited as `(src: ref-project/qa-automation-wt-3-0/<path>:<line>)`.

Facts that hold everywhere:

- Login has **no server picker**. The id alone decides the server; Root Admin "server validation priority" breaks ties when the same id exists on two servers (src: `tests/web/login/test_LGN_TC05_positive_server_priority.py`). A second server's account is attached after login via Manage Account → Link account (below).
- **No passcode, biometric, or env gate screen exists.** Env is the URL (web) or the installed package (app) (src: `src/page_object/` — no such screen in any tree).
- Same testid string on every member-site platform: `data-testid` on web, resource-id on Android (unqualified, e.g. `login-submit`, never `com.aquariux…:id/login-submit`), accessibility id on iOS (src: `.claude/docs/platform-conventions.md`).
- Wrong credentials on any tab: "Invalid credentials, please try again." (src: `src/data/ui_messages.py:9`).

## Member site — desktop

1. Open `{base_url}/web`. Landing path is `/login` (src: `web/base_page.py:74`, `src/data/enums/system.py:65`).
2. Pick the account tab: `tab-login-account-type-live` | `-demo` | `-crm` (div). The selected tab carries class `selected` (src: `web/pages/login_page.py:24,92`).
3. `login-user-id` (input) — account id, or email on the CRM tab (src: `login_page.py:25`).
4. `login-password` (input); eye-mask is the sibling div (src: `login_page.py:26-27`).
5. Optional language: `language-dropdown` (div) → `language-option` whose text is the language name, e.g. `Tiếng Việt` (src: `login_page.py:29-30`).
6. `login-submit` (button). Wait for the loader to clear (src: `login_page.py:28,70`).

Also on the page: `login-account-signup` (Sign up), "Open Demo Account" text link. Not on desktop: Forgot password, Remember me (src: `login_page.py:31-32`).

Tabs shown: `Demo` + `Live` by default; **`Demo` + `CRM` when the tenant is lirunex on MT4** (src: `login_page.py:82-86`).

## Member site — mobile-web

Set viewport **430×932** before the first navigation; the MCP may reset it between calls (src: `src/data/consts.py:38`, `.claude/docs/browser-rule.md`).

1. Open `{base_url}/mobile` (src: `web_app/base_page.py:70`).
2. Account tab — text, not testid. `Demo` = `//div[text()="Demo"]`; **two `Live` divs exist**: the first is the CRM tab, the last is Live (src: `web_app/pages/login_page.py:42-44`).
3. Username field testid is **`login-account-type`** (input), not `login-user-id`. Placeholder "Enter your account ID", or "Enter your email / username" on the CRM tab (src: `login_page.py:33,180-186`, `ui_messages.py:12-13`).
4. `login-password`; reveal `login-password-show-password`, hide `login-password-hide-password` (src: `login_page.py:34-36`).
5. Optional language: `language-dropdown` (button) → option under `language-dropdown-*` with the language text (src: `login_page.py:40-41`).
6. `login-submit`.

Extra on mobile-web: `forgot-password-button`, `login-account-signup`, "Open Demo Account" (src: `login_page.py:38-39,45`). CRM sign-up form lives behind Sign up (src: `web_app/pages/crm_signup_page.py:10`).

## Native app — Android

Pre-steps:

1. Confirm the install matches the matrix point: `adb shell pm list packages | grep aquariux`. Expect exactly one of `com.aquariux.wt.sit.<client>` / `.release.<client>` / `.uat.<client|tinshing>`. Any other package is the wrong build (src: `.claude/docs/appium-rule.md`, `config/*.yaml`).
2. Launch. Tap `ads-skip-button` when it shows; the app may reload once, so expect up to two skips (src: `android/screens/login_screen.py:36,61`).
3. If a previous session survived, you land on Home, not Login. Log out first, or relaunch and re-check (src: `.claude/docs/appium-rule.md`).

Fields (resource-ids):

| Step | Target | Note |
|---|---|---|
| Account tab | content-desc `Demo`; `Live` instance 0 = CRM tab, `Live` instance 1 = Live tab | text-based, same layout as mobile-web (src: `login_screen.py:45-47`) |
| Username | `login-account-type` (EditText) | (src: `:37`) |
| Password | `login-password` (EditText); `login-password-show-password` / `-hide-password` | (src: `:38-40`) |
| Remember me | `login-remember-me-unchecked` ↔ `login-remember-me-checked` — the id flips with state | (src: `:52-53`) |
| Language | `language-dropdown` → scroll to content-desc = language name | (src: `:42-43`) |
| Submit | `login-submit` | (src: `:41`) |
| Also present | `forgot-password-button`, `login-account-signup`, "Open Demo Account", footer `© {Client} {year}. All rights reserved` | (src: `:48-51,253-255`) |

⚠ unverified — Android Live→CRM remap: the Android tree maps "Live" to the **first** `Live` element (the CRM tab) for every client except lirunex; iOS and mobile-web always take the last `Live`. The trees disagree, so which element a non-lirunex Android build calls "Live" must be confirmed on the device (src: `android/screens/login_screen.py:147-148` vs `ios/screens/login_screen.py:165-169`).

After login, Home may show a feature announcement: tap `feature-announcement-modal-got-it-button` until it stops appearing (src: `android/screens/home_screen.py:34,57`).

## Native app — iOS

Pre-steps: `xcrun simctl listapps <udid> | grep -i aquariux` for the bundle; same ads skip (`ads-skip-button`) and session caveat as Android (src: `ios/screens/login_screen.py:32,57`).

Fields (accessibility ids unless noted):

| Step | Target | Note |
|---|---|---|
| Account tab | `Demo`; `Live` — **last** `XCUIElementTypeOther[name == "Live"]` is Live, the first is CRM | (src: `ios/screens/login_screen.py:41-43`) |
| Username | TextField `name == "login-account-type"` | XCUITest also reports a container with the same name — target the text field (src: `:33`, `.claude/docs/appium-rule.md`) |
| Password | `login-password`; `login-password-show-password` / `-hide-password` | (src: `:34-36`) |
| Remember me | `login-remember-me-unchecked` ↔ `login-remember-me-checked` | (src: `:48-49`) |
| Language | Button `language-dropdown` → option = language name | (src: `:38-39`) |
| Submit | `login-submit` | (src: `:37`) |
| Also present | `forgot-password-button`, `login-account-signup`, "Open Demo Account", footer "All rights reserved" | (src: `:44-47`) |

Got-it modal after login: `feature-announcement-modal-got-it-button` (src: `ios/screens/home_screen.py:55`).

## CRM login — email + OTP

Applies only to the CRM tab, so only to lirunex.

1. Username is an **email**, password is the CRM password (`password_crm` in the yaml) (src: `src/data/data_runtime.py:83-85`).
2. Submit. A wrong password stops here with the invalid-credentials error and **no OTP is sent** (src: `tests/web_app/login/crm_login/test_LGN_CRM_TC09*`).
3. OTP screen: title "Enter Code", "Please enter the 6-digits code we sent to your email." (src: `ui_messages.py:37-38`).
   - Web: six `input[maxlength='1']` boxes; submit `sign-up-verification-button`; resend `sign-up-resend-verification`; timer is the span after it; back `otp-back-to-login-button` (src: `web/pages/crm_otp_page.py:24-29`).
   - App: one field `sign-up-verification-pin`, same submit and resend ids (src: `ios/screens/crm_otp_screen.py:24-27`, `android/screens/crm_otp_screen.py:24-27`).
4. Read the 6-digit code from the account's inbox. Test inbox: `mt4@sharklasers.com` (Guerrilla Mail) (src: `src/data/consts.py:193`).
5. Enter the digits and submit.

| Behaviour | Expected |
|---|---|
| Resend timer | starts at `02:00`; Resend disabled until it hits zero (src: `crm_otp_page.py:156`, `test_LGN_CRM_TC01*`) |
| Resend inside cooldown | "An OTP was recently sent to you. Please try again after 2 minutes." (120 s) (src: `ui_messages.py:32`, `consts.py:25`) |
| Code age | expires after 300 s → "Your OTP is expired." (src: `consts.py:26`, `ui_messages.py:34`) |
| Wrong code | "The code you entered is incorrect, please try again." (src: `ui_messages.py:30`) |
| New code requested | previous code is invalid; a used code cannot be reused (src: `test_LGN_CRM_TC05*`, `test_LGN_CRM_TC08*`) |
| Non-numeric input | rejected (src: `test_LGN_CRM_TC07*`) |

Precondition for the "new OTP invalidates previous" and "used OTP" cases: Root Admin logout URL set to empty, restored afterwards (src: `tests/web_app/login/crm_login/test_LGN_CRM_TC05*`, `test_LGN_CRM_TC08*`).

## Back Office

1. Open `{client}.back_office.url` from the yaml. The UI path after the host is `<not in source>` (only the API base `/api/admin` is recorded) (src: `src/api/webtrader/back_office/auth.py:21`).
2. Username from the yaml `userid` list (comma-separated pool; any one works), BO password (src: `auth.py:37`).
3. Captcha: on any `sit` env (sit, release_sit) the code **`123`** is accepted. On uat it is a real image captcha — read it by eye; refresh if unreadable (src: `auth.py:44`, `data_runtime.py:161-162`).
4. Sign in. Sessions expire; the automation re-logs in on a failed session check, so expect to re-login mid-task (src: `auth.py:61`).

Not on prod. Every BO write changes the client for everyone — note the old value, restore it (src: `.claude/docs/fixture-conventions.md`).

## Root Admin

1. Open `root_admin.url` (global; on SIT it ends in `/root`) (src: `config/sit.yaml:7`).
2. No testids. Username = input under label `Username`; password = `input[type=password]`; captcha field = the input whose sibling holds the `<img>`; "new code" link = anchor `Anchor-root`; submit = `button[type=submit]` (src: `src/page_object/root_admin/pages/login_page.py:16-21`).
3. Captcha `123` on sit envs; real image on uat. A login error shows as a `Notification-root` toast — refresh the code and retry (src: `login_page.py:22,45-48`, `root_admin/auth.py:33-66`).
4. Users: `automation`, `automation2`, `automation3` on SIT (src: `config/sit.yaml:8`).

Root Admin edits a whole company object at once. Feature and language saves are **destructive — anything left unticked is disabled** (src: `src/api/webtrader/root_admin/company.py:238,274`). Details in `.claude/domain/wt-admin.md`.

## Attaching a second account — Manage Account → Link account

Mobile-web and app: Menu → Account → Manage Account (`/menu/manage-account`). Desktop: Settings dropdown → linked accounts (src: `src/data/enums/system.py:80`, `tests/web/trade/settings/test_TRD_SET_TC0{5,6,7,8}*`).

1. `manage-account-link-account` (button) (src: `web_app/components/account/manage_account.py:27`).
2. `link-account-form-account-id`, `link-account-form-password` (the linked account's own password), `link-account-form-confirm` (src: `web_app/components/modals/link_account.py:21-27`).
3. Success: "Account linked successfully." on 3.0 mobile ⚠ unverified on web 3.0 — source says "todo: recheck on web 3.0"; older copy is "You have linked your account successfully.\nAccount ID: %s" (src: `ui_messages.py:49-56`).
4. Empty fields: "Account ID is required." / "Password is required."; already linked: "Account already linked" (src: `ui_messages.py:52,64-65`).
5. Switch: tap the linked account → confirm `link-account-modal-ok-button`; "Switch account?\nThis will end your current session…" then "Account switched successfully." Remove: `manage-account-edit` → `manage-account-delete` → confirm (src: `link_account.py:37-40`, `manage_account.py:26-30`, `ui_messages.py:60-62`).
6. Some flows ask the password again: `re-enter-password-form-password` → `re-enter-password-form-confirm` (src: `link_account.py:47-48`).

Cross-server linking (mt4 account onto an mt5 login) works only on multi-OMS tenants (lirunex, centroid) and not from a CRM login (src: `tests/web_app/menu/manage_account/test_MNU_MGA_TC04*:12`). Linked-account rows read `ID: x (USD | 1:leverage)`; Centroid rows read `ID: x` only (src: `src/data/objects/account_info.py:249`).

## Confirming build and env

| Check | How |
|---|---|
| Web env + client | URL host: `{client}-mb.webtrader-{env}.s20ip12.com`; prod is `webtrader.lirunex.com`. TinShing host = centroid on UAT (src: `config/*.yaml`) |
| Web layout | `/web` = desktop; `/mobile` = phone layout. Wrong path → wrong UI |
| App env + client | package name (`adb shell pm list packages` / `xcrun simctl listapps`): `.sit.`, `.release.`, `.uat.` segment + client (src: `.claude/docs/appium-rule.md`) |
| App client on screen | login footer `© {Client} {year}. All rights reserved` (src: `ui_messages.py:17`, `android/screens/login_screen.py:253-255`) |
| Account type after login | Home / Trade badge: LIVE, DEMO; CRM shows LIVE (src: `web_app/pages/home_page.py:150`) |
| Server after login | account-info label `TS4` / `TS5` / `Centroid` (src: `src/data/enums/system.py:43`) |

## Fast checks

| Symptom | Likely cause |
|---|---|
| Feature or menu item missing on the app | wrong build for the env — check the package name first |
| Feature missing on web | wrong client URL or client legitimately lacks it (Stop Limit, CRM, quoteboard…) — see `wt-shared.md` tables |
| Manage Funds / Open Demo Account not in Menu | logged in on a demo account (src: `src/data/enums/ui.py:360,374`) |
| Only Demo + CRM tabs, no Live | lirunex on MT4 — expected (src: `web/pages/login_page.py:85`) |
| Two "Live" tabs when scanning the DOM/tree | first is CRM, last is Live — expected on mobile-web and app |
| Cannot place an order after login; symbols grey | market closed for that symbol; check trading hours and server timezone |
| No notification arrives | demo account — no notifications by design |
| OTP never arrives | wrong password (OTP is not sent), or inside the 120 s cooldown from a previous request |
| OTP rejected as expired | more than 300 s since it was sent |
| BO / Root Admin captcha keeps failing | not on a sit env — `123` only works there; read the image |
| Landed on Home instead of Login on the app | previous session persisted — log out, or relaunch after clearing app data |
| Desktop layout at phone size | viewport not set to 430×932 before navigation |
| Link account says "Account already linked" | that id is already in the linked list — remove it first |
| Cross-server link fails | non-OMS tenant (transactCloud) or a CRM login — not supported |

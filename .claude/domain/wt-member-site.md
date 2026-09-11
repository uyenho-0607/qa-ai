# WT 3.0 — Member site screens

Screen inventory across the four member-facing platforms — `web` (desktop), `web-app` (mobile-web),
`android`, `ios`. This file only answers "does this screen exist here, and what does it do at a
glance" — locators live in `.claude/locator-cache.json`, the one-`testID`-serves-three-platforms
convention is in `.claude/platforms/member-web.md`, login runbooks are in
`.claude/domain/login-flow.md`, and order/position business rules are in `.claude/domain/wt-trading.md`.

Basic pass — confirmed against the reference automation repo's `page_object/member_site/`
directory structure (`web/pages/`, `web_app/pages/`, `android/screens/`, `ios/screens/`) before that
repo was removed from this workspace. Deeper per-component detail (individual fields, modals,
validation rules) was gathered during the port but not folded in here; getting it again means
re-fetching the reference repo, since it's no longer present locally.

## 1. Login, CRM OTP, CRM Sign Up

On all four platforms. Full runbook per platform and account type: `login-flow.md`. Desktop's
username field is `login-user-id`; `web-app`/`android`/`ios` all use `login-account-type` for the
same field (`member-web.md:36`). **CRM Sign Up has no desktop screen** — `web` has no signup page in
source; `web-app` (`crm_signup_page.py`), `android`, `ios` (`signup_screen.py`) all do.

## 2. Quote / Trade

On all four platforms — the order-entry surface. Business rules (order types, fields, calculations,
confirmation flow): `wt-trading.md`. `web` composes a Quoteboard list; `web-app` and `android` both
carry a `components/quoteboard/` widget (a Default Trade Volume sheet, plus a Quote Settings
component that is an empty stub in source on both); **`ios` has no `quoteboard/` component
directory at all** — confirmed by direct file-listing diff against `android`.

## 3. Markets

On all four platforms. Sub-tabs: Watchlist / Market Mover / Explore (mobile), desktop's own
markets listing (`Markets_DS`/`Markets_Mobile` in Testmo's naming — `tc-naming-ref.md`).

## 4. Assets

On all four platforms. Shows Account Information, Open Positions, Pending Orders, Order History —
same tables as the Trade screen's inline assets panel (`wt-trading.md` § Positions and orders).

## 5. Home

**`web-app`, `android`, `ios` only — no desktop equivalent.** Desktop's sidebar IA has no dashboard
screen; `web-app`/app's bottom-nav IA uses Home as the landing screen (`member-web.md`).

## 6. Menu / Settings

**Menu as a dedicated screen exists on `web-app`, `android`, `ios` only.** Desktop has no Menu
screen — Settings is reached through a dropdown instead of a separate screen (already noted in
`project-config.md` § Platforms: "Settings dropdown exist on `web` only").

## 7. Copy Trade

**`web-app`, `android`, `ios` only — no desktop screen in source.** Pre-login state redirects to
Pelican (a separate copy-trade identity provider) in an external browser tab/webview; post-login
shows a strategy list with a Freemium/Premium tier split (`tc-naming-ref.md` § Copy Trade).

## 8. Price Alert

**`web-app`, `android`, `ios` only — no desktop screen in source.** Reached from the Trade/chart
screen's alert icon on mobile; manages per-symbol price alerts.

## 9. Signal

**`web` (desktop) only — no mobile equivalent in source.** The one screen that runs the other
direction from § 5–8.

## Feature × platform

| Screen / Feature | web | web-app | android | ios |
|---|---|---|---|---|
| Login | yes | yes | yes | yes |
| CRM OTP | yes | yes | yes | yes |
| CRM Sign Up | no | yes | yes | yes |
| Quote / Trade | yes | yes | yes | yes |
| Markets | yes | yes | yes | yes |
| Assets | yes | yes | yes | yes |
| Home | no | yes | yes | yes |
| Menu (dedicated screen) | no | yes | yes | yes |
| Settings (dropdown, not a screen) | yes | — | — | — |
| Copy Trade | no | yes | yes | yes |
| Price Alert | no | yes | yes | yes |
| Signal | yes | no | no | no |
| Quoteboard settings widget (stub in source) | unknown — not checked | yes (stub) | yes (stub) | no |

This table decides which platform rows a TC gets (`project-config.md` § Platforms).

# TC Naming Reference — Modules, Sub-modules & Features

Source: live Testmo project `5` (WT) folder tree, sampled via `testmo_list_folders(projectId: 5)`.
`##` is the platform group, `###` are the Modules, `>` carries that group's default Configuration —
`generate-tcs/SKILL.md` § 1.7 and § 3.1 parse this file on those exact heading levels. A Module
folder that itself nests one level deeper becomes the **Sub-module** column of a 3-column table;
one with no further nesting uses the simple 2-column `Feature | Covers` form.

Config ids and the account-type gate (`custom_login_method`) are in `.claude/steering/testmo.md`
§ Configurations, § Case Field IDs — this file only fixes naming, not those ids.

---

## Membersite

> All modules in this section run on the member-facing product — `web`, `web-app`, `android`, `ios`.
> Unlike the two groups below, the **same** Module here can apply to more than one platform; which
> platform(s) a given Module actually covers is in `.claude/domain/wt-member-site.md` § Feature ×
> platform. Default Configuration = the client under test's `{Client}, {platform}` row in
> `testmo.md` § Configurations — e.g. `TransactCloud, Desktop Browser` for this project's default.

### Login Page
_No sub-modules._

| Feature | Covers |
|---------|--------|
| CRM Login | Email + OTP login path (`lirunex` only) |
| Live Login | Account-id login, live account |
| Demo Login | Account-id login, demo account |
| CRM Sign Up | New CRM account creation |
| Demo Account Creation | New demo account creation |
| Remember Me | Persisted-login checkbox |
| AQX Experience Login | Cross-product SSO entry point |

### Trade Page/Home Page
_"Trade Page" on desktop, "Home Page" on mobile._

| Sub-module | Feature | Covers |
|---|---|---|
| _(none)_ | Manage Fund | Manage Funds redirect — the only funding-related surface, no deposit/balance API exists |
| _(none)_ | Search & Time Display | Symbol search, server time display |
| _(none)_ | Announcement | In-page announcement banners |
| _(none)_ | Watchlist | — |
| _(none)_ | Trade Analysis (Mobile) | — |
| _(none)_ | Shortcut Configuration (Mobile) | — |
| _(none)_ | Market Display Config | — |
| Account Information | Mask Account Info | Masked balance/account display |
| Order Placing Window (OPW) | Form | Order entry form fields and validation |

### Post Trade Tables
_"Post Trade table in Trade page and Assets page."_

| Sub-module | Feature | Covers |
|---|---|---|
| _(none)_ | Open Positions | Count display, hide/show others symbol, bulk close, column selection/sort, action buttons, Trade Sharing Card |
| _(none)_ | Pending Orders | Same shape as Open Positions, plus bulk delete |
| Order History | Filter | Date/status filtering on order history |

### Trading Logic
_"Full trading workflow — order events (TP/SL hit, TIF hit, modify, close, delete) and their effect on the order history table; both hedging and netting logic."_

| Sub-module | Feature | Covers |
|---|---|---|
| Hedging Trade | Open Position | Hedge-mode open-position lifecycle |
| Hedging Trade | Pending Order | Hedge-mode pending-order lifecycle |
| Hedging Trade | Order History | Hedge-mode order-history effects |
| Netting Trade | Open Position | Netting-mode open-position lifecycle (Centroid netting: `wt-trading.md` § 6) |
| Netting Trade | Pending Order | Netting-mode pending-order lifecycle |
| Netting Trade | Order History | Netting-mode order-history effects |

### Setting
_No sub-modules._

| Feature | Covers |
|---------|--------|
| Link & Switch | Link/switch member account |
| Language | Language selection |
| Appearance | Theme (light/dark) |
| Notification Setting | Per-category notification toggles |
| Change Password | Password change flow |
| Linked Devices | Device list, revoke |
| Contact Us | Support contact entry point |
| Biometric Login | Biometric enable/disable |
| About | App/build info |
| Logout | Logout flow |
| Manage Accounts | — |
| Market Display Config | — |

### Markets Page
_No sub-modules._

| Feature | Covers |
|---------|--------|
| Markets_DS | Desktop markets listing |
| Markets_Mobile | Mobile markets listing |

### Notification
_No sub-modules._

| Feature | Covers |
|---------|--------|
| Snackbar | Toast/snackbar notifications |

### Chart
_No sub-modules._

| Feature | Covers |
|---------|--------|
| Tracking | — |
| Modify Orders | Modify from chart |
| Chart Display, Timeframe, Data | — |
| Drawing Tools | — |
| Indicators | — |
| Right Click Actions | — |
| Order Placing Window | Place order from chart |
| Trading View | — |

### Assets Page
_"Profile & Account Info, Statistic, My Portfolio."_

| Feature | Covers |
|---------|--------|
| Account Information | Profile and account-info display |
| Open Positions | Assets-page open positions table |
| Pending Orders | Assets-page pending orders table |
| Order History | Assets-page order history table |

### Quoteboard
_No sub-modules._

| Feature | Covers |
|---------|--------|
| Card Display | Quote card layout |
| Default Trade Volume | Default lot/volume on quick-trade |
| Quoteboard OPW | Order placing window launched from the quoteboard |

### Price Alert
_No sub-modules._

| Feature | Covers |
|---------|--------|
| Price Alert Chart | Alert markers on chart |
| Price Alert Modal | Create/edit alert modal |
| Price Alert Notification | Alert-fired notification |

### Copy Trade
_No sub-modules._

| Feature | Covers |
|---------|--------|
| Freemium | Free-tier copy trade |
| Premium | Paid-tier copy trade |

### Trade Sharing Card
_No sub-modules._

| Feature | Covers |
|---------|--------|
| OP_Share Icon_Mobile | Share Open Position card, mobile |
| OP_Share Icon_DS | Share Open Position card, desktop |
| OH_Share Icon_Mobile | Share Order History card, mobile |
| OH_Share Icon_DS | Share Order History card, desktop |
| Card Size Selection | Card size variants |

### Trading Hours & Holiday Setting
_No sub-modules._

| Feature | Covers |
|---------|--------|
| AQXOMS | Trading-hours display, AQXOMS-integrated servers |
| MT4/MT5/Centroid | Trading-hours display, MT4/MT5/Centroid servers |

### Other Membersite Modules — no Feature/Sub-module split sampled

Sampled at Module level only; do not invent a Feature or Sub-module name for these until confirmed
against Testmo:

| Module | Cases | Notes |
|---|---|---|
| Calendar | 70 | |
| Dealer | 20 | |
| Learn | 5 | |
| News | 8 | |
| Signal | 16 | |
| Symbols | 21 | Enabled/Disabled symbol, Market Close, Stay Tuned, Specification, Special Trade Type Config, Off Quote Symbol behavior |
| Read Only Access | 12 | |
| Features Announcement | 0 | |
| StoneInno - KYC View Only | 350 | One ticket's cases (`WT-12234`) — not a stable naming source |

---

## Admin BackOffice

> All modules in this section run in the per-client Back Office. Default Configuration =
> `{Client}, Admin BO` — see `testmo.md` § Configurations.

### Audit Logs
_No sub-modules._

| Feature | Covers |
|---------|--------|
| Trade Sharing Card Config | — |
| Member Login | Login audit trail |
| Market Display Config | — |

### User
_Has sub-modules._

| Sub-module | Feature | Covers |
|---|---|---|
| Roles | Market Display Config | — |
| Roles | Shortcut Configuration Privileges | — |
| _(none)_ | Users | Empty folder — no cases sampled |

### Marketing & Communication
_No sub-modules._

| Feature | Covers |
|---------|--------|
| BO_Trade Sharing Card Config | — |
| Announcement Management | — |
| Masthead Banner Management | — |
| Notification Management | — |
| Feature Shortcut Configuration | — |
| Market Display Config | — |

---

## Root Admin Portal

> Global — one instance shared across every client. Default Configuration = `Root Admin`.

### Config
_No sub-modules._

| Feature | Covers |
|---------|--------|
| View Only | Read-only role/permission view |

### Volume Calculation
_No sub-modules._

| Feature | Covers |
|---------|--------|
| Account Exclusion | Accounts excluded from volume calculation |

### Troubleshoot Platform
_No sub-modules._

| Feature | Covers |
|---------|--------|
| Statement Patch & Regeneration | — |

### Role Management
_No Feature/Sub-module split sampled (3 cases)._

### User Management
_No Feature/Sub-module split sampled (3 cases)._

---

## Legacy — not a current naming source

- **AQX OMS Intergration** (Testmo folder `518`, 271 cases) — ticket-scoped folders
  (`WT-13805 & WT-14991`, `Trade Form Sanity Test`, `WT-13817 Positions Table`, etc.), not a
  Module/Sub-module/Feature tree. Predates the current lirunex/transactCloud/centroid/hantec
  client split — matches the `AQXOMS` config group in `testmo.md`. Do not file new cases here.
- **Backlog** (Testmo folder `2206`, 0 cases) — empty holding folder.

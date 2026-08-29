# Figma Design Snapshot: AO-925

## Metadata

- **Figma File**: OTC Portal [Desktop Web]
- **Section**: `🔎 Add Withdrawal Accounts new tab in Member Mgmt Details page | AO-1054`
- **Figma URL**: https://www.figma.com/file/ACKfmhqMg1qreJjBm1F4Bk?node-id=17516%3A333924&mode=dev
- **File Key**: `ACKfmhqMg1qreJjBm1F4Bk`
- **Node ID**: `17516:333924`
- **Extraction Date**: 2026-08-27
- **Jira Ticket**: AO-925 (design frame also cites AO-1054)
- **Design stamp in frame**: Date 18 August 2026 · Senior Designer: Huiqi · Status `🔎 Ready for review`
- **Screenshots**: `tasks/AO-925/attachments/figma-screenshots/` (55 PNGs)

> Scope note: this snapshot records **rendered UI only**. Designer annotation frames ("Notes") are excluded
> except where a note is the sole source of a rendered string or of a state not drawn as a frame — those are
> marked `(annotation only)`.

---

## Page Structure

### Navigation

- **Side Navigation** (dark, collapsible via a circular chevron button at lower edge): Dashboard, **Members** (active), Balances, OTC, Configuration, Action Required `99+`, Transactions, Reports, Users. Logo "Liverum" top-left.
- **Top Navigation**: page title "Members"; right side `GMT+08:00 · Asia/Singapore` with globe icon; divider; avatar `J` + "John Doe" + chevron.
- **Breadcrumbs**: `Members` (link, cyan) / `Details` (current, non-clickable).

### Member Header (persistent across all tabs)

| Element | Value in design |
|---|---|
| Avatar | Letter avatar, `I` |
| Primary name | Isabella Koh |
| Member type | Personal |
| Email | ops@liverum.com + copy icon |
| Profile ID | `Profile ID: 331239231` + copy icon |
| Status badge | `Active` (green, right-aligned) |

Separators between type / email / profile ID are `|`.
Business-member variant in the same file shows "TechCorp Solutions Inc." · Business · contact@techcorpsolutions.com.

### Tab Navigation

`Overview` · `Verification` · **`Withdrawal Accounts`** · `Recent Actions`

- Underline style, active tab in cyan with a 2px underline.
- **`Withdrawal Accounts` sits third — between `Verification` and `Recent Actions`.**
- `Overview` is the default tab on page load (Personal member shows Date of Birth, ID Number, Created Date).

### Withdrawal Account Type Switcher

A segmented **Button group** directly under the tabs, above the filter row:

- `Bank Accounts` — selected by default (white pill, dark text)
- `Crypto Addresses` — unselected (grey fill, grey text)

---

## Main Page: Withdrawal Accounts — Bank Accounts

_Screenshot: `01-bank-accounts-list.png`_

### Search & Filter

| Control | Type | Detail |
|---|---|---|
| `Created Date` | Dropdown (date condition) | see **Created Date filter** below |
| `Currency` | Dropdown, searchable multi-select | see **Currency filter** below |
| `Status` | Dropdown, checkbox multi-select | `Active`, `Disabled`, `Deleted` |
| Search | Input with magnifier icon, right-aligned | Placeholder: `Bank / Name / Account No.` |

### Table

| # | Column | Sortable | Data type | Sample data |
|---|---|---|---|---|
| 1 | `Bank Name` | No | Text | DBS Bank · HSBC Hong Kong · OCBC Bank · Citibank · Standard Chartered B… · Australia and New Ze… · United Overseas Bank · Maybank |
| 2 | `Account Holder Name` | No | Text (truncates with `…`) | Isabella Koh Mei Ling · Lioncrest Technologie… |
| 3 | `Account Number / IBAN` | No | Masked text | `•••• 7890`, `•••• 7001`, `•••• 5678` — 4 dots + last 4 digits |
| 4 | `Currency` | **Yes** | Flag chips + overflow | `AUD` `CAD` `+10` · `HKD` · `SGD` `USD` · `AUD` `CAD` `+4` |
| 5 | `Status` | No | Badge | `Active` (green) · `Disabled` (red) · `Deleted` (grey) |
| 6 | `Created Date` | **Yes** | Date-time | `04 Apr 2026, 20:39` — `DD MMM YYYY, HH:mm` |
| 7 | *(unlabelled)* | No | Action | `⋯` overflow menu, right-aligned |

- **Currency cell**: shows the first **2** currency chips (flag + code), then `+N` for the remainder. Observed `+2`, `+3`, `+4`, `+10`, `+12`.
- **Sort indicator**: paired up/down chevrons on `Currency` and `Created Date` only.
- **Sorting behaviour** *(annotation only)*: one column sorted at a time; toggles ascending/descending; default sort is system-defined (e.g. Status or Created Date).
- **Row states** *(annotation only)*: hovered row highlights `Gray 50`; selected row highlights `Gray 100`.
- **Observed sort order**: `Active` rows first, then `Disabled`, then `Deleted`.

### Pagination

- **Record count format**: `1 - 10 of 24 records` (bold on the numbers)
- **Style**: `‹` prev · page numbers `1` `2` `3` (active = cyan filled circle) · `›` next
- **Page size selector**: `10 / page` dropdown
- **Jump**: `Go to page` + numeric input (placeholder `11`) + cyan `Go` button

### Action Menu (per row)

_Screenshot: `03-bank-row-actions-menu.png`_

Opens from the `⋯` cell, anchored below-right of the trigger.

| Item | Icon | Destructive |
|---|---|---|
| `View` | Eye outline | No |
| `Disable` | `✕` | Yes (action is destructive in intent; label is not red in the menu) |

Menu contents by row status *(annotation only)*:

| Row status | Menu items |
|---|---|
| `Active` | `View`, `Disable` |
| `Disabled` | `View`, `Enable` |
| `Deleted` | `View` |

> The annotation text spells the second item "Activate" for `Disabled` rows, but every **rendered** control in the
> file reads `Enable`. Rendered copy is `Enable`.

---

## Main Page: Withdrawal Accounts — Crypto Addresses

_Screenshot: `02-crypto-addresses-list.png`_

### Search & Filter

| Control | Type | Detail |
|---|---|---|
| `Created Date` | Dropdown (date condition) | identical to bank |
| `Network` | Dropdown, searchable multi-select | see **Network filter** below |
| `Status` | Dropdown, checkbox multi-select | `Active`, `Disabled`, `Deleted` |
| Search | Input with magnifier icon | Placeholder: `Wallet Address` |

### Table

| # | Column | Sortable | Data type | Sample data |
|---|---|---|---|---|
| 1 | `Network` | No | Text | Ethereum (ERC20) · Bitcoin · TRON (TRC20) · Solana · Polygon · Avalanche C-Chain · BNB Smart Chain (BEP20) · Base · XRP Ledger (XRPL) · Cardano |
| 2 | `Wallet Address` | No | Truncated text | `0x7A9E...A3D2` · `bc1q8m...k7x2` · `TQ8f2k...4mK9` · `7xKp1s...9QmR` · `addr1q...8x4m` — first 6 + `...` + last 4 |
| 3 | `Status` | No | Badge | `Active` · `Disabled` · `Deleted` |
| 4 | `Created Date` | **Yes** | Date-time | `04 Apr 2026, 20:39` |
| 5 | *(unlabelled)* | No | Action | `⋯` overflow menu |

- **Only 4 visible columns + actions. There is no `Asset` column** — network alone identifies the row.
- Sort indicator on `Created Date` only.
- Pagination identical to the bank table (`1 - 10 of 24 records`).

### Action Menu (per row)

_Screenshot: `04-crypto-row-actions-menu.png`_ — identical to the bank menu: `View`, `Disable`.

---

## Drawer: Bank Account Details

_Screenshots: `05-bank-details-drawer.png`, `20-drawer-bank-a.png` (Active), `21-drawer-bank-b.png` (Disabled), `22-drawer-bank-c.png` (Deleted)_

Right-side drawer over a dimmed scrim; the underlying page stays visible. Occupies roughly the right half of a 1440px viewport.

### Header

- **Title**: `Bank Account Details`
- **Actions (top-right)**: status-dependent action button, then a `✕` close icon
- **Record heading** (below header): the record **Label** as an H2 — e.g. `Main Business Account` — followed by the status badge

### Field Groups

**Account**

| Field | Sample |
|---|---|
| `Bank Name` | DBS Bank |
| `Bank Country` | Singapore |
| `Currency` | AUD, CAD, CNY, EUR, GBP, HKD, JPY, MYR, SGD, THB, USD, VND *(full list, comma-separated, wraps)* |
| `Account Type` | Savings |

**Beneficiary**

| Field | Sample | Affordance |
|---|---|---|
| `Account Holder Name` | Isabella Koh Mei Ling | — |
| `Account Number / IBAN` | `•••• 7890` | Copy icon |
| `BIC / SWIFT` | DBSSSGSG | Copy icon |
| `Bank Code / Routing Number` | 7171 | — |
| `Beneficiary Address` | `12 Marina Boulevard` / `Marina Bay Financial Centre Tower 3, #18-01` / `Singapore 018982` | Multi-line, single field |

**Others**

| Field | Sample |
|---|---|
| `Created Date` | 04 Apr 2026, 20:39 |
| `Last Updated` | 04 Apr 2026, 20:39 |

Layout: two columns, label in grey above value in black. `Beneficiary Address` spans the left column across three lines.

### States

| State | Badge | Header action button |
|---|---|---|
| Active | `Active` (green) | `Disable` — red outline, `✕` icon |
| Disabled | `Disabled` (red) | `Enable` — neutral outline, `✓` icon |
| Deleted | `Deleted` (grey) | **none** — close `✕` only |

---

## Drawer: Crypto Address Details

_Screenshots: `06-crypto-details-drawer.png`, `23-drawer-crypto-a.png` (Active), `24-drawer-crypto-b.png` (Disabled), `25-drawer-crypto-c.png` (Deleted), `26-drawer-crypto-d.png` (Active with Memo/Tag)_

Same drawer shell as the bank drawer.

### Header

- **Title**: `Crypto Address Details`
- **Record heading**: the address **Label** as an H2 — e.g. `Binance Wallet` — plus status badge

### Field Groups

**Address**

| Field | Sample | Affordance |
|---|---|---|
| `Network` | Ethereum (ERC20) · XRP Ledger (XRPL) | — |
| `Wallet Address` | `0x4Cbe58c50480A73fC4E5D84F6D7C3c2A4dE6` — **full, unmasked**, wraps to 2 lines | Copy icon |
| `Memo/Tag` | `3904520452` — **rendered only when present** | Copy icon |

**Others**

| Field | Sample |
|---|---|
| `Created Date` | 04 Apr 2026, 20:39 |
| `Last Updated` | 04 Apr 2026, 20:39 |

- **No `Asset` field** on this view.
- The `Memo/Tag` row is absent entirely on the non-memo variants (a, b, c) and present on variant d.

### States

Identical pattern to the bank drawer: `Active` → `Disable`; `Disabled` → `Enable`; `Deleted` → no action button.

---

## Modal: Disable confirmation

_Screenshots: `30-modal-bank-1.png` (bank), `36-modal-crypto-1.png` (crypto)_

| Part | Bank | Crypto |
|---|---|---|
| Icon | Orange `!` in circle | same |
| Title | `Disable Bank Account` | `Disable Crypto Address` |
| Body | `This bank account •••• 7890 will be immediately unavailable for withdrawal, and the member will not be able to add it again while it is disabled.` | `This crypto address 0x7A9E...A3D2 will be immediately unavailable for withdrawal, and the member will not be able to add it again while it is disabled.` |
| Secondary | `Cancel` (white, outlined) | `Cancel` |
| Primary | `Disable` (**red** fill) | `Disable` (**red** fill) |

The masked account number / truncated address is **bold** inside the sentence.

## Modal: Enable confirmation

_Screenshots: `31-modal-bank-2.png`, `37-modal-crypto-2.png`_

| Part | Bank | Crypto |
|---|---|---|
| Title | `Enable Bank Account` | `Enable Crypto Address` |
| Body | `This bank account •••• 7890 will be available for withdrawal again immediately.` | `This crypto address 0x7A9E...A3D2 will be available for withdrawal again immediately.` |
| Secondary | `Cancel` | `Cancel` |
| Primary | `Enable` (**cyan** fill) | `Enable` (**cyan** fill) |

## Modal: Blocking — cannot disable

_Screenshots: `33-modal-bank-4.png`, `40-modal-crypto-5.png`_

| Part | Bank | Crypto |
|---|---|---|
| Title | `Unable to Disable Bank Account` | `Unable to Disable Crypto Address` |
| Body | `This bank account cannot be disabled because it has pending withdrawals. Complete or cancel the pending withdrawals before trying again.` | `This crypto address cannot be disabled because it has pending withdrawals. Complete or cancel the pending withdrawals before trying again.` |
| Buttons | `Close` (cyan) — single button, no Cancel | same |

## Modal: Blocking — cannot enable (active limit)

_Screenshots: `35-modal-bank-6.png`, `41-modal-crypto-6.png`_

| Part | Bank | Crypto |
|---|---|---|
| Title | `Unable to Enable Bank Account` | `Unable to Enable Crypto Address` |
| Body | `This member already has 5 active bank accounts. Disable another record before enabling this one.` | `This member already has 5 active crypto addresses. Disable another record before enabling this one.` |
| Buttons | `Close` (cyan) | same |

---

## Toasts / Snackbars

_Screenshots: `60-snackbar-bank.png`, `61-snackbar-crypto.png`, in context `11-bank-disable-success.png`_

- **Position**: floating near the **top-centre** of the content area, above the drawer scrim.
- **Style**: white pill, drop shadow, green filled `✓` icon on the left.
- **No dismiss control drawn** on the snackbar.

| Message |
|---|
| `Bank account disabled successfully.` |
| `Bank account enabled successfully.` |
| `Crypto address disabled successfully.` |
| `Crypto address enabled successfully.` |

After a successful action the drawer **stays open**: the badge flips (`Active` → `Disabled`) and the header button flips (`Disable` → `Enable`) in place.

Generic failure copy present in the file: `Unable to complete this action. Please try again.`

---

## Empty State (table)

_Screenshots: `81-empty-state-bank-componentset.png`, `82-empty-state-crypto-componentset.png`_

Source of truth: the `State=Empty` variant of the table component sets — `Table/Withdrawal Accounts-bank accounts`
(`17516:348971`) and `Table/Withdrawal Accounts-crypto addresses` (`17552:462516`).

| Property | Value |
|---|---|
| Message — bank | `No bank accounts` |
| Message — crypto | `No crypto addresses` |
| Description line | none |
| CTA | none |
| Illustration | `empty-img-gray` — grey inbox/monitor with a speech bubble, 80px wide × 64px tall |
| Type style | Inter Regular, 14px / 20px line-height, centre-aligned |
| Colour | `Gray/500` — `#858D9D` |
| Layout | Column, centred, 8px gap between illustration and text; block width 352px |
| Placement | Centred in the table body; column headers remain visible above |

The empty state is a **title-only** block — one line of grey text under an illustration. There is no secondary
description, no "Clear filters" action, and no distinct variant separating "this member has none" from
"the filter/search returned nothing" — one string covers both.

> ⚠️ Rendering caveat, recorded so this is not re-litigated: exporting the *table instances* on the board
> (`17552:466461`, `17552:473966`) or the nested instance path `I17552:466461;17516:348971` returns the base
> component defaults — `No results found`, with placeholder `Header` column labels. Those exports do not apply
> the instance overrides and are **not** the design intent. Files `70`, `71`, `79`, `80` in the screenshots
> folder are those unreliable renders; use `81` and `82`.

---

## Filter Components

### Status filter

_Screenshots: `50-filter-status-a.png`, `52-filter-status-c.png`_

- Trigger `Status` + chevron; cyan outline when open.
- Checkbox multi-select: `Active`, `Disabled`, `Deleted`.
- Selected values render as a cyan token inside the trigger, e.g. `Status  Active  ✕  ⌃`, with an `✕` to clear.
- Default: nothing selected (shows all) *(annotation only)*.

### Created Date filter

_Screenshots: `54-filter-date-a.png`, `55-filter-date-expanded.png`_

- Condition dropdown, then condition-specific inputs, then a full-width cyan `Apply` button.
- Conditions: `is in the last` · `is equal to` · `is between`
  - `is in the last` — numeric input (placeholder `7`) + unit dropdown (`days` / `months`)
  - `is equal to` — single date
  - `is between` — start date + end date
- Date inputs use the system date picker *(annotation only)*.
- Validation strings present in the file: `Date range must be within the last 366 days.` · `Maximum range is 366 days.` · `Please select a date within the last 366 days.`
- Sample date values in the file: `04 Nov 2023`, `04 Nov 2023 - 11 Nov 2023`, `04 Nov 2025`.

### Network filter (crypto only)

_Screenshots: `56-filter-network-a.png`, `57-filter-network-b.png`, `72-filter-network-no-results.png`_

- Searchable multi-select: `Search` input at top, then `Select All`, then a scrollable checkbox list.
- Options observed (alphabetical): Avalanche C-Chain, Base, BNB Smart Chain (BEP20), Bitcoin, Bitcoin Cash, Cardano, Ethereum (ERC20), Polygon, Solana, TRON (TRC20), XRP Ledger (XRPL).
- Selected networks show as tokens; clearing removes all *(annotation only)*.
- **No-match state inside the dropdown**: illustration + `No results found`.

### Currency filter (bank only)

_Screenshots: `58-filter-currency-a.png`, `59-filter-currency-b.png`_

- Searchable multi-select with `Search`, `Select All`, scrollable checkbox list, country flag beside each code.
- Options observed (alphabetical): AUD, CAD, CHF, CNH, EUR, GBP, HKD, JPY, NZD, SGD, USD.
- **The isolated component's trigger label reads `From Currency`; on the page the trigger reads `Currency`.**

---

## Component States Summary

| Component | States |
|---|---|
| Tab (`Withdrawal Accounts`) | Active (cyan text + underline) / Inactive (grey) |
| Type switcher | `Bank Accounts` selected / `Crypto Addresses` selected |
| Status badge | `Active` green · `Disabled` red · `Deleted` grey |
| Table row | Default / Hover (Gray 50) / Selected (Gray 100) |
| Table | Populated / Empty (`No results found`) |
| Row action menu | Active → View + Disable · Disabled → View + Enable · Deleted → View |
| Drawer header button | `Disable` (red outline) / `Enable` (neutral outline) / absent (Deleted) |
| Confirmation modal | Disable (red primary) / Enable (cyan primary) |
| Blocking modal | Cannot disable (pending withdrawals) / Cannot enable (active limit) — both single `Close` |
| Snackbar | Success only (green ✓), 4 messages |
| Filter dropdown | Closed / Open / Value selected (token + clear ✕) / No results |
| Sort indicator | Present on `Currency` + `Created Date` (bank), `Created Date` (crypto) |

---

## UI Flow Summary

1. Admin opens **Members** → clicks a member row → **Member Details** opens on the `Overview` tab.
2. Admin selects the **`Withdrawal Accounts`** tab.
3. `Bank Accounts` is selected in the type switcher by default; the bank table loads with `1 - 10 of 24 records`.
4. Admin may filter by `Created Date`, `Currency`, `Status`, or search `Bank / Name / Account No.`.
5. Admin clicks `⋯` on a row → `View` opens the **Bank Account Details** drawer over a dimmed page.
6. From the drawer (or directly from the row menu) admin selects `Disable`.
7. **Disable Bank Account** confirmation modal appears → `Cancel` dismisses; `Disable` (red) commits.
8. On success: snackbar `Bank account disabled successfully.` at top-centre; the drawer stays open with badge `Disabled` and the header button now `Enable`.
9. On block: **Unable to Disable Bank Account** modal — pending withdrawals — `Close` only.
10. To reverse: `Enable` → **Enable Bank Account** modal → `Enable` (cyan) → snackbar `Bank account enabled successfully.`
11. If the member is at the active limit: **Unable to Enable Bank Account** modal — `This member already has 5 active bank accounts.` — `Close` only.
12. Switching to `Crypto Addresses` repeats the same flow with `Network` in place of `Currency` and the **Crypto Address Details** drawer.

---

## Design vs Ticket — Conflicts and Gaps

Raised for TC design; every row is a rendered-design observation against the AO-925 description.

| # | Area | Design shows | Ticket requires | Severity |
|---|---|---|---|---|
| 1 | Disable + pending withdrawal | Blocking modal `Unable to Disable Bank Account / Crypto Address — …cannot be disabled because it has pending withdrawals.` | BR-6: **"Disable is never blocked by an in-flight withdrawal — it is a security action and must succeed."** BR-9 puts the block on the checker's *approve*, not on disable. | **Direct contradiction** |
| 2 | Crypto active limit | `This member already has **5** active crypto addresses.` | BR-6 / AO-922 Req 1: crypto limit is **20** | **High** |
| 3 | Crypto list columns | `Network`, `Wallet Address`, `Status`, `Created Date` | BR-4 requires an **`Asset`** column as well | **High** |
| 4 | Crypto detail fields | `Network`, `Wallet Address`, `Memo/Tag`, `Created Date`, `Last Updated` | BR-5 also requires **`Asset`** | **High** |
| 5 | Bank account number on detail | Masked `•••• 7890` with copy icon; **no reveal/eye control is drawn** in any variant | BR-3: **"The full account number is shown on this view"** (Maker executes the transfer from it). An annotation mentions a visibility icon, but no frame renders one. | **High** |
| 6 | Bank address fields | One multi-line `Beneficiary Address` | BR-3 lists `Address Line 1`, `Address Line 2`, `City`, `Postal Code` as separate fields | Medium |
| 7 | `Date Deleted` | Not present on either list or either drawer | BR-7: a `Deleted` record "remains listed in this tab with its `Date Deleted`" | Medium |
| 8 | Empty-state copy | `No bank accounts` / `No crypto addresses` — title only, no description, no CTA | ERR-9: `This member has no {bank accounts / crypto addresses}.` | Medium |
| 8b | Empty-state coverage | One string serves both "member has none" and "filter/search returned nothing"; the annotation only describes the filter/search case | ERR-9 is written for the member-has-none case. No design exists for a no-filter-match state distinct from it. | Medium |
| 9 | Confirmation modal copy | Title `Disable Bank Account`; body starts `This bank account •••• 7890 will be…` | ERR-1: Header `Disable this bank account?`; body `{Label} will be…` — design keys off the **masked number**, ticket keys off the **Label** | Medium |
| 10 | Success copy | `Bank account disabled successfully.` | ERR-4: `This bank account has been disabled.` | Low |
| 11 | Enable-limit copy | `This member already has 5 active bank accounts. Disable another record before enabling this one.` | ERR-6 — wording matches; only the crypto **number** is wrong (see #2) | Low |
| 12 | Section layout | Bank and crypto are **mutually exclusive tabs** in a segmented switcher | BR-1: "**Bank Accounts** at the top, **Crypto Addresses** below" — i.e. two stacked sections on one view | Medium |
| 13 | Currency filter label | Isolated component trigger reads `From Currency` | Should read `Currency` as on the page | Low |
| 14 | Row-menu wording | Annotation says `Activate` for disabled rows; all rendered controls say `Enable` | Ticket uses `Enable` | Low (doc only) |
| 15 | Bank list sort | Active block runs `04 Apr 20:39`, `27 Mar 11:25`, `20 Mar 13:22`, `18 Mar **18:40**`, `18 Mar **19:05**` — the last two are inverted | BR-2: "Sorted most recently added first" | Low (sample-data slip) |
| 16 | Pagination | `10 / page`, pages 1–3, `1 - 10 of 24 records`, `Go to page` | BR-2/BR-4 never state a page size — design supplies one where the ticket is silent | Info |

Additional design-only behaviour the ticket does not cover: `Currency` is sortable on the bank table; the
`Created Date` filter enforces a 366-day ceiling with three validation strings; both filter dropdowns are
searchable multi-selects with `Select All`.

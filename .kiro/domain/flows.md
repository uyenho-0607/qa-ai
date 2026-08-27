# Withdrawal Accounts (Member Details) — Flow

Source: live observation on OTC BO SIT, 2026-08-26, as Admin / Maker / Checker.
Ticket: AO-925. Build: 0.15.0 - OTC (fixVersion; no build stamp exposed in the UI).

> Everything below is observed live. Where the live app differs from AO-925's requirements, the
> difference is marked **⚠ DEVIATION** — the requirement is quoted, then what the app actually does.

## Navigation

- Login: `{BO_URL}/login` — `#email`, `#password`, `button[type=submit]`. No `data-testid` anywhere in the app.
- Members list: `/members` — Ant table, rows keyed `tr[data-row-key="{email}"]`, `role=button`,
  `aria-label="View details for {name}"`.
- Member Details: `/members/details?memberId={id}`
- Withdrawal Accounts: `/members/details?memberId={id}&tab=withdrawal-accounts`
- Sub-tab: `&subTab=bank-accounts` | `&subTab=crypto-addresses` — both deep-linkable.
- Member Details tab strip, in order: **Overview · Verification · Withdrawal Accounts · Recent Actions**.

## Fields and Behaviour

### Bank Accounts sub-tab

Columns, left to right, as rendered:
`Bank Name` · `Account Holder Name` · `Account Number / IBAN` · `Currency` (sortable) · `Status` ·
`Created Date` (sortable) · unnamed trailing column (presumed row actions)

Matches AO-925 BR-2 exactly.

Controls above the table, **none of which AO-925 specifies**:
- `Created Date` filter dropdown
- `Currency` filter dropdown
- `Status` filter dropdown
- Search box, placeholder `Bank / Name / Account No.`

Empty state: icon + `No bank accounts`

### Crypto Addresses sub-tab

Columns as rendered: `Network` · `Wallet Address` · `Status` · `Created Date` · unnamed trailing column

**⚠ DEVIATION — missing `Asset` column.** BR-4 requires "Columns: `Asset`, `Network`, masked
`Wallet Address` …". The live table has no `Asset` column. TC-161988 step 1 asserts Asset is visible.

Empty state: `No crypto addresses`

### Section layout

**⚠ DEVIATION — sections are a toggle pair, not stacked.** BR-1 requires "two sections — **Bank Accounts**
at the top, **Crypto Addresses** below". Live, they are two `role=tab` BUTTONs in a segmented control
(`div.flex.items-center.gap-0.border-none.w-fit.rounded-lg.bg-gray-200.p-0.5`), `aria-selected` toggling
between them. Only one table is in the DOM at a time. TC-161967 asserts "Crypto Addresses section is
visible **below** Bank Accounts" — not satisfiable as built.

### Empty-state copy

**⚠ DEVIATION — empty-state strings do not match.**

| Required (AO-925 ERR-9) | Live |
|---|---|
| `This member has no bank accounts.` | `No bank accounts` |
| `This member has no crypto addresses.` | `No crypto addresses` |

### Empty optional fields

Member Details → Overview renders unfilled optional fields as `-` (observed on Business Registration
Number and Phone Number). This supports TC-161973's `"-"` expectation, though AO-925 never states it and
the drawer itself could not be reached.

## Validation Rules

None observable. Every validation path in AO-925 (Enable at the 5 / 20 active limit, Disable with a
Pending withdrawal, API failure copy) requires at least one existing record. No record exists — see
State Transitions.

## State Transitions

**Not observable on SIT.** The `Active → Disabled → Active` transitions, both confirmation modals, both
success toasts, the limit-blocked error, and the Deleted read-only state all require a bank account or
crypto address to exist.

Confirmed by exhaustive sweep, 2026-08-26:
- `GET /api/backoffice/backend/bank-account/member/{id}` → `result.total = 0` for **all 459 members**
- `GET /api/backoffice/backend/crypto-address/member/{id}` → `result.total = 0` for **all 459 members**

Re-verified independently the same day by sweeping the profile-id space directly, `1..600` (profile ids
observed top out near 500; member 579 maps to profile 467). Every id returned HTTP 200 with
`result.total = 0` on both endpoints — so the emptiness is real, not a permission or lookup artefact.

On the Crypto Addresses table only `Created Date` carries an `.ant-table-column-sorter`; `Network`,
`Wallet Address` and `Status` are not user-sortable. The AO-925 sort contract (Active → Disabled →
Deleted, each Created-Date-descending) is therefore a *default* server ordering, and unverifiable while
the table is empty.

Records are member-created only (BR-1: "Back Office cannot create, edit or delete a record"), so the
only route to test data is the mobile app Add Bank Account / Add Crypto Address flow (AO-923 / AO-922).

The unnamed trailing column in both tables is presumed to hold the row action menu, but with zero rows
its contents were never rendered — **the existence of `Disable` / `Enable` controls is unverified.**

## Permissions

Withdrawal Accounts tab visibility, verified by logging in as each role:

| Role | Sees Withdrawal Accounts tab | Same columns | Left nav |
|---|---|---|---|
| Admin (`maiadmin@`) | yes | yes | Dashboard, Members, Balances, OTC, Configuration, **Action Required**, Transactions, Reports, User |
| Maker (`maimaker@`) | yes | yes | Dashboard, Members, Balances, OTC, Transactions |
| Checker (`maichecker@`) | yes | yes | Dashboard, Members, Balances, OTC, Transactions |

**⚠ Contradicts `.kiro/domain/otc-bo.md`**, which records Member Management as "Admin: view only" and
Action Required as "Maker + Admin: no access". Live, Admin *does* have Action Required. The live app wins;
`otc-bo.md` § Roles & Permissions is stale on both points.

Whether Disable/Enable is gated by role in the **UI** is still unverified — no record exists to hang an
action menu on. But the **API privilege set settles the intent**, re-verified 2026-08-26 via
`GET /api/backoffice/backend/user/me` for each account:

| Account | `businessRoleCode` | `MEMBER_BANK_ACCOUNT_UPDATE` | `MEMBER_CRYPTO_ADDRESS_UPDATE` |
|---|---|---|---|
| `maiadmin@` | `ADMIN` | yes | yes |
| `maimaker@` | `ADMIN` | yes | yes |
| `maichecker@` | `ADMIN` | yes | yes |

Two consequences:

1. **All three accounts hold the UPDATE privilege** for both destination types. Live intent therefore
   matches AO-925 BR-1 ("available to any Back Office role with Member Details access") and contradicts
   TC-161965 and TC-161966, which assert Maker and Checker must *not* see Disable/Enable. TC-191123
   (Admin CAN see them) is consistent with the live privilege set.
2. **`businessRoleCode` is `ADMIN` for all three accounts.** There is no account on SIT whose role code is
   Maker or Checker. The three are distinguished only by privilege set — `maimaker@` alone has
   `MEMBER_CREATE` + `BALANCE_CREATE`; `maichecker@` alone has `BALANCE_APPROVAL` + `OTC_APPROVAL`.
   TC-161965 / TC-161966 as written ("a Maker-role user", "a Checker-role user") have no matching account.

Full privilege sets observed:
- `maiadmin@` — USER_ACCOUNT_CREATE, MEMBER_CREATE, MEMBER_VIEW, OTC_VIEW, OTC_CREATE, BALANCE_VIEW, TXN_VIEW, BALANCE_STMT_VIEW, BALANCE_APPROVAL, BALANCE_CREATE, USER_ROLE_VIEW, USER_ACCOUNT_VIEW, OTC_APPROVAL, VERIFICATION_VIEW, VERIFICATION_CREATE, VERIFICATION_UPDATE, TRADING_PAIR_VIEW, TRADING_PAIR_CREATE, MARKUP_RULE_VIEW, MARKUP_RULE_CREATE, MEMBER_BANK_ACCOUNT_VIEW, MEMBER_BANK_ACCOUNT_UPDATE, MEMBER_CRYPTO_ADDRESS_VIEW, MEMBER_CRYPTO_ADDRESS_UPDATE
- `maimaker@` — MEMBER_CREATE, MEMBER_VIEW, OTC_VIEW, OTC_CREATE, BALANCE_VIEW, TXN_VIEW, BALANCE_STMT_VIEW, BALANCE_CREATE, VERIFICATION_VIEW, VERIFICATION_CREATE, VERIFICATION_UPDATE, MEMBER_BANK_ACCOUNT_VIEW, MEMBER_BANK_ACCOUNT_UPDATE, MEMBER_CRYPTO_ADDRESS_VIEW, MEMBER_CRYPTO_ADDRESS_UPDATE
- `maichecker@` — MEMBER_VIEW, OTC_VIEW, BALANCE_VIEW, TXN_VIEW, BALANCE_STMT_VIEW, BALANCE_APPROVAL, OTC_APPROVAL, VERIFICATION_VIEW, MEMBER_BANK_ACCOUNT_VIEW, MEMBER_BANK_ACCOUNT_UPDATE, MEMBER_CRYPTO_ADDRESS_VIEW, MEMBER_CRYPTO_ADDRESS_UPDATE

### Action Required submodules (Admin)

`Balance Approvals` → `/approval/balance` · `OTC Approvals` → `/approval/otc` · `Unidentified` → `/approval/unidentified`

Balance Approvals columns: `Type` · `Created Date` · `Member` · `Currency` · `Amount` · `Status` ·
unnamed trailing column holding `button[aria-label="View details"]`.
Pagination footer: `1-10 of 124 records`, page-size selector `10 / page`, `Go to page` + `Go`.

Pending `Withdrawal` rows exist (e.g. `cgmember@yopmail.com` XRP 1.00, USDT 0.10; `popo@yopmail.com` XRP 0.10)
— but every one of those members has zero saved withdrawal accounts, so none can serve the
"Pending withdrawal to a Disabled destination" cases.

**Withdrawal request drawer** — opened via the row's `button[aria-label="View details"]`, calls
`GET /api/report/backend/balance/approval/{txnId}`. Drawer heading `Balance Details`. Sections:
type + amount + status badge · `Timeline` · `Summary` · `Details` · `Others`. Footer buttons `Reject` and
`Approve`, **both `disabled: false`** on a Pending request. Closed via `button[aria-label="Close drawer"]`.

**⚠ Existing Pending withdrawals carry no destination record.** On the sampled request (`txnId 2007`,
cgmember XRP 1.00) the drawer shows `Source Address -` and `Destination Address -`, and the API returns
`"fromAddress": null, "toAddress": null`, `"channel": "MANUAL"`. These requests are not linked to a saved
crypto address or bank account, so disabling a destination cannot affect them. TC-162011 / TC-162012 /
TC-162013 need a withdrawal raised *against a saved destination record* — which requires the mobile
withdrawal flow, not one of these existing rows.

## Capture Points

Reachable today: tab strip render, sub-tab toggle, both empty states, column headers, role-by-role tab
visibility. Everything else waits on test data.

## Locators

No `data-testid` exists in this application. Cached selectors: `.kiro/locator-cache.json`.
Prefer `getByRole('tab', { name: … })` over the generated `#rc-tabs-0-tab-*` ids.

### API

Base `/api/backoffice/backend`. Auth: `Authorization: Bearer ${JSON.parse(localStorage.accessToken)}`
— the token is *not* a cookie, so a bare `fetch` with `credentials:'include'` returns 401.

| Purpose | Endpoint |
|---|---|
| Bank accounts by member | `GET /bank-account/member/{memberId}` |
| Crypto addresses by member | `GET /crypto-address/member/{memberId}` |
| Member list | `GET /member?pageNum=1&pageSize=500` |

Response shape: `{ code, result: { list: [], total, pageNum, pageSize, … } }`.
Note the Withdrawal Accounts page calls `bank-account/member/467` while the URL carries `memberId=579`
— the path parameter is a profile id, not the member id in the URL.

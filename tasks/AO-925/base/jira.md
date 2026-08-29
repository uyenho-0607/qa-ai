# Jira: AO-925

## Title
[OTC][Backoffice] Add Withdrawal Accounts new tab in Member Mgmt Details page

## Status
Ready to Test in SIT | Assignee: Alexis Soo | Reporter: Ming En Leong

Issue type: Story · fixVersion: `0.15.0 - OTC` · Created 2026-07-21 · Updated 2026-08-26
URL: https://aquariux.atlassian.net/browse/AO-925

**Affected module:** Back Office → Member Management → Member Details → **Withdrawal Accounts** (new tab).
Cross-surface impact: member app Withdrawal Accounts (bank + crypto), Fiat Withdrawal, Crypto Withdrawal,
and Back Office → Balance Approvals.

## Description

### Background
Member Details in the Back Office does not display the bank accounts or crypto addresses a member has saved.
Admins handling a member enquiry or a suspected unauthorised destination have no way to see what is on the
account, and no way to stop a destination being used. This enhancement introduces a **Withdrawal Accounts**
tab listing both destination types, with full detail views and admin `Disable` and `Enable` actions.

### User Story
As an admin, I want to see every bank account and crypto address a member has saved and disable any of them,
so that I can support member enquiries and stop a destination the member says they did not add.

### Behaviour Table
| Behaviour | Description |
| --- | --- |
| **As-Is** | Member Details does not display saved bank accounts or crypto addresses. Admins cannot view destination details or disable a destination. |
| **To-Be** | Member Details has a **Withdrawal Accounts** tab listing the member's bank accounts and crypto addresses with status and dates. Admins can open full details, `Disable` any record, and re-enable it later. A disabled record is immediately unusable for withdrawal and cannot be re-added by the member. |

### Back Office Flow: Disable a Withdrawal Account
1. Admin opens **Member Management → Member → Member Details → Withdrawal Accounts**.
2. Admin locates the record in the **Bank Accounts** or **Crypto Addresses** section.
3. Admin opens the record to view full details.
4. Admin selects `Disable` and confirms.
5. The record status becomes `Disabled` and is immediately unavailable for withdrawal in the mobile app.
6. The member can no longer add the same bank account or crypto address.
7. Where a `Pending` withdrawal request exists to that destination, the checker can only reject it.
8. Admin may later select `Enable` to return the record to `Active`.

### Prototype
https://claude.ai/design/p/83dfa170-b3e9-426f-8158-80c26891e257?file=Withdrawal+Account.dc.html&via=share

## Business Requirements

- BR-1: **General Requirements** — A new **Withdrawal Accounts** tab is added under **Member Management → Member → Member Details**, with two sections — **Bank Accounts** at the top, **Crypto Addresses** below — **the "two sections" wording is STALE, superseded by the design.** Live and per the design the two are a `role=tab` toggle pair, one panel at a time. User ruling 2026-08-27; TC-02 c4 passes against it. — both scoped to the member whose page is open. **Records are member-created only** — Back Office cannot create, edit or delete a record. The only admin actions are `Disable` and `Enable`. **No maker-checker** — both actions take effect immediately and are available to any Back Office role with Member Details access.
- BR-2: **Bank Accounts Section** — Lists every bank account belonging to the member, in any status. Columns: `Bank Name`, `Account Holder Name`, masked `Account Number / IBAN` (last 4 digits), `Currency` (the full list held on the account), `Status`, `Created Date`. Sorted most recently added first, with `Disabled` and `Deleted` records after `Active` ones. **Statuses** — `Active` / `Disabled` / `Deleted` (AO-923 Req 1).
- BR-3: **Bank Account Details** — Selecting a record opens a read-only detail drawer view showing **every field captured in AO-923 Req 3** — `Label`, `Bank Country`, `Bank Name`, `Account Holder Name`, `Account Number / IBAN`, `BIC / SWIFT`, `Currency` list, `Address Line 1`, `Address Line 2`, `City`, `Postal Code`, `Bank Code / Routing Number`, `Account Type` — plus `Status`, `Created Date` and `Last Updated Date`. **The full account number is shown on this view**, since the Maker executes the transfer manually from this data (AO-923 Req 8). Every view of this screen is written to the audit log (BR-10).
- BR-4: **Crypto Addresses Section** — Lists every crypto address belonging to the member, in any status. Columns: `Asset`, `Network`, masked `Wallet Address` (first 6 and last 4 characters, per AO-922 Req 2), `Status`, `Created Date`. Same sort order, pagination and status model as BR-2.
- BR-5: **Crypto Address Details** — Selecting a record opens a read-only detail view showing `Label`, `Asset`, `Network`, the full `Wallet Address`, `Memo / Tag` where present, `Status`, `Created Date` and `Last Updated Date`. `Network` is required here because the mobile list does not display it, and the same address on the wrong network is a different destination.
- BR-6: **Disable & Enable Actions** — `Disable` is available on records in `Active` status, from the list row and the detail view, with a confirmation modal. Status becomes `Disabled` and the record is immediately unavailable for withdrawal: in the mobile app it renders in the disabled, non-clickable state (AO-923 Req 2) and is excluded from the withdrawal destination dropdown (AO-881 Req 2). **Disable is never blocked by an in-flight withdrawal** — it is a security action and must succeed even where a `Pending` withdrawal exists to that destination. The pending request is not automatically cancelled (BR-9). `Enable` is available on records in `Disabled` status, with a confirmation modal. Status returns to `Active` and the record is immediately usable again, and the member may add that destination again. **Enable is blocked where the member already holds the maximum number of active records** for that destination type — 5 bank accounts (AO-923 Req 1) or 20 crypto addresses (AO-922 Req 1) — since `Disabled` records do not count toward the limit.
- BR-7: **Deleted Records** — `Deleted` is member-initiated (AO-923 Req 6, AO-922 Req 5). The record is retained, never purged, and remains listed in this tab with its `Date Deleted` so the member's own action stays traceable. **No admin action is available on a deleted record** — it can be neither disabled nor enabled. A `Deleted` record does not prevent the member re-adding the same destination (BR-8).
- BR-8: **Re-add Prevention** — While a record is `Disabled`, the member cannot add the same destination again. **Bank accounts** — the normalised `Account Number / IBAN` plus `BIC / SWIFT` is matched against the member's `Active` and `Disabled` records. **Crypto addresses** — `Asset` + `Network` + `Address` is matched against the member's `Active` and `Disabled` records. `Deleted` records do **not** block re-adding. Member-facing error copy exists in AO-923 and AO-922.
- BR-9: **Impact on Pending Withdrawal Requests** — Where a withdrawal request in `Pending` status is linked to a destination that has since become `Disabled`, the checker **cannot approve it**. Attempting to approve returns a blocking error, and the only available action is `Reject`. On rejection the held amount is returned to the member's available balance (AO-881 Req 6) and the member is notified (AO-917). The request is not auto-rejected — a checker must action it, so the decision stays with a named human.
- BR-10: **Audit Log** *(not shown on UI)* — Record every `Disable` and `Enable` action with the admin, timestamp, record ID, destination type and member ID. Record every view of a Bank Account Details or Crypto Address Details screen, since both expose the destination in full. Member-initiated add and delete events are visible in the tab for reference.

## Acceptance Criteria

The ticket carries no separate Acceptance Criteria section. The ACs below are `derived` — one per numbered
Requirement row, using the same numbering so AC-n maps 1:1 to BR-n.

- AC-1: *(derived from BR-1)* A **Withdrawal Accounts** tab exists under Member Management → Member → Member Details, holding a **Bank Accounts** section above a **Crypto Addresses** section, both scoped to the open member. No create, edit or delete action is offered. `Disable` / `Enable` are the only admin actions, take effect immediately, need no maker-checker, and are available to any Back Office role with Member Details access.
- AC-2: *(derived from BR-2)* The Bank Accounts section lists every bank account of the member in any status, with columns `Bank Name`, `Account Holder Name`, masked `Account Number / IBAN` (last 4), `Currency`, `Status`, `Created Date`; sorted most recently added first with `Disabled` and `Deleted` after `Active`.
- AC-3: *(derived from BR-3)* Clicking a bank account row opens a read-only detail drawer showing every AO-923 Req 3 field plus `Status`, `Created Date`, `Last Updated Date`, with the **full unmasked** account number; the view is written to the audit log.
- AC-4: *(derived from BR-4)* The Crypto Addresses section lists every crypto address of the member in any status, with columns `Asset`, `Network`, masked `Wallet Address` (first 6 / last 4), `Status`, `Created Date`; same sort order, pagination and status model as AC-2.
- AC-5: *(derived from BR-5)* Clicking a crypto address row opens a read-only detail view showing `Label`, `Asset`, `Network`, the **full** `Wallet Address`, `Memo / Tag` where present, `Status`, `Created Date` and `Last Updated Date`.
- AC-6: *(derived from BR-6)* `Disable` is offered on `Active` records from both the list row and the detail view behind a confirmation modal, sets status to `Disabled` immediately, is never blocked by a `Pending` withdrawal, and makes the record non-selectable in the app. `Enable` is offered on `Disabled` records behind a confirmation modal, returns status to `Active`, and is blocked when the member already holds 5 active bank accounts or 20 active crypto addresses.
- AC-7: *(derived from BR-7)* A `Deleted` record stays listed with its date and offers no admin action; it does not prevent the member re-adding the same destination.
- AC-8: *(derived from BR-8)* While `Disabled`, the member cannot re-add the same destination — bank matched on normalised `Account Number / IBAN` + `BIC / SWIFT`, crypto on `Asset` + `Network` + `Address`, both against the member's `Active` and `Disabled` records. `Deleted` records do not block a re-add.
- AC-9: *(derived from BR-9)* A checker cannot approve a `Pending` withdrawal whose destination is now `Disabled` — approval returns a blocking error and only `Reject` succeeds; rejection returns the held amount to available balance and notifies the member. The request is never auto-rejected.
- AC-10: *(derived from BR-10)* Every `Disable`, every `Enable`, and every view of a Bank Account Details or Crypto Address Details screen is written to the audit log with admin, timestamp, record ID, destination type and member ID.

## Error Messages

All strings below are from the **Back Office Messages** table in the description (source: description).

- ERR-1: Header: "Disable this bank account?" Body: "{Label} will be immediately unavailable for withdrawal, and the member will not be able to add it again while it is disabled." CTAs: `Cancel` / `Disable`
- ERR-2: Header: "Disable this crypto address?" Body: "{Label} · will be immediately unavailable for withdrawal, and the member will not be able to add it again while it is disabled." CTAs: `Cancel` / `Disable`
- ERR-3: Header: "Enable this {bank account / crypto address}?" Body: "{Label} · {Masked Number} will be available for withdrawal again immediately." CTAs: `Cancel` / `Enable`
- ERR-4: "This {bank account / crypto address} has been disabled."  (Disable succeeded)
- ERR-5: "This {bank account / crypto address} has been enabled."  (Enable succeeded)
- ERR-6: "This member already has {Limit} active {bank accounts / crypto addresses}. Disable another record before enabling this one."  (Enable blocked by the active limit)
- ERR-7: "This withdrawal destination has been disabled and the request cannot be approved. Reject the request to return the funds to the member's available balance."  (Checker attempts to approve a withdrawal to a disabled destination)
- ERR-8: "Unable to complete this action. Please try again."  (Action failed)
- ERR-9: "This member has no {bank accounts / crypto addresses}."  (Section empty state) — **STALE, superseded by the design.** Live and per the design the empty state reads "No bank accounts" / "No crypto addresses". User ruled the design newer than the ticket text on 2026-08-27; TC-07 and TC-27 pass against it. Raise the wording against the ticket.

## Out of Scope

None stated for the current scope.

⚠️ The two earlier comments by Alexis Soo (2026-07-30, 2026-08-05) carry an **Out of Scope** list, but they
describe a **superseded** scope — "Address Book / Linked Bank Accounts + Action Required → Linked Bank
Account Approval, Maker-Checker". That scope was replaced by Ming En Leong's 2026-08-20 comment, which matches
the current description verbatim. Do not test against the superseded comments. Their Out of Scope list, for
reference only: editing wallet addresses, deleting wallet addresses from Back Office, editing linked bank
accounts, deleting linked bank accounts, bulk approval or rejection, search and filtering enhancements, export
functionality, electronic bank account verification.

## Linked Issues

None (`issuelinks` is empty).

Referenced by requirement text, not by a Jira link:
- AO-923: member-app bank account add / edit / delete, statuses, 5-account limit, full-number display
- AO-922: member-app crypto address add / delete, 20-address limit, masking rule
- AO-881: withdrawal destination dropdown, held-amount return on rejection
- AO-917: member notification on withdrawal rejection

## Sub-tasks

### AO-1032: [OTC][Backoffice] Add Withdrawal Accounts new tab in Member Mgmt Details page
Type: Backend Development · Status: **In SIT** · fixVersion `0.15.0 - OTC`
Comment (Alexis Soo, 2026-08-18): "will complete by today"

### AO-1040: [OTC][Backoffice] Add Withdrawal Accounts new tab in Member Mgmt Details page
Type: Frontend Development · Status: **Pending Merge to SIT** · fixVersion `0.15.0 - OTC`
⚠️ **Not yet merged to SIT.** The BO UI under test may be absent or stale on `BO_URL`. Confirm at Preflight
before executing — this gates every BO-surface TC.

### AO-1054: [OTC][Backoffice] Add Withdrawal Accounts new tab in Member Mgmt Details page
Type: Design Request · Status: Approved

### AO-1087: [AO-925] [OTC][Backoffice] Add Withdrawal Accounts new tab in Member Mgmt Details page
Type: QA Preparation · Status: Done
Description: "suetfun reviewed @ 8/25/2026"
TC breakdown posted by Huyen Mai Thi (2026-08-20, edited 2026-08-25): total 62 cases — 53 under **Members**
(folder 128), 2 under **Fiat Withdrawal** (3597, incl. existing 151523), 3 under **Withdrawal Accounts**
(3595, incl. existing 151419; 162007 also linked to AO-923, 162008 also linked to AO-922), 1 under **Crypto
Withdrawal** (3792), 3 under **Balance Approvals** (374).
Reviewer requests from Suet Fun Ng (2026-08-25) — all three were subsequently added as cases 191123, 191124,
191125:
1. Add test case verifying Admin role CAN see Disable/Enable actions
2. Add test case: member has 4 Active + 2 Disabled bank accounts, Enable succeeds (proves Disabled not counted)
3. Add test case: member deletes bank account, then successfully re-adds same Account Number/IBAN + BIC/SWIFT

### AO-1098: [AO-925] [OTC][Backoffice] Add Withdrawal Accounts new tab in Member Mgmt Details page
Type: QA Execution · Status: To Do — this run's execution sub-task.

## Visual Context

No image attachments. Both attachments are ZIP archives, not downloadable images:
- `Withdrawal account tab design.zip` (1.88 MB, Alexis Soo, 2026-08-18) — `application/zip`
- `Withdrawal account tab design (9f6c229d-86dc-4398-a325-b39d648e4fc6).zip` (1.88 MB, Ming En Leong, 2026-08-20) — `application/zip`

The two `![](blob:...)` markers embedded in the description and in the 2026-08-20 comment resolve to these ZIP
attachments, not to inline screenshots. Design reference is the Prototype link under `## Description`.

## Figma Links

None. The only design link on the ticket is a `claude.ai/design` prototype, not a `figma.com` URL — see
`## Description` → Prototype.

## Open Items from Comments

- **FE not on SIT.** AO-1040 (Frontend Development) is `Pending Merge to SIT` while the parent reads `Ready to
  Test in SIT`. Verify the BO build actually carries the Withdrawal Accounts tab before executing. (status as at 2026-08-27)
- **Superseded scope in comments.** Comments 242956 (Alexis Soo, 2026-07-30) and 243489 (Alexis Soo,
  2026-08-05) describe the Address Book / Linked Bank Accounts / Maker-Checker approval design. Comment 244974
  (Ming En Leong, 2026-08-20) replaced it. No comment confirms the earlier design was formally dropped — it is
  inferred from the description matching the newest comment. Flag if BO shows an "Address Book" tab instead.
- **TC count drift.** AO-1087 records 62 cases; `testmo_find_cases_by_issue` now returns 65 — the three cases
  Suet Fun Ng requested on 2026-08-25 (191123, 191124, 191125) were added after the count was written.
- **Pagination unspecified.** BR-4 says "Same sort order, pagination and status model as Requirement 2", but
  BR-2 never states a page size. No expected result exists for pagination. (by Ming En Leong, 2026-08-20)
- **`Date Deleted` column not in BR-2 / BR-4.** BR-7 requires a `Deleted` record to remain listed "with its
  `Date Deleted`", but neither section's column list includes it. Where it renders is unspecified.
- **QA estimate: 1.5 md** (Suet Fun Ng, 2026-08-26).

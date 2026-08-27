# Jira: AO-925

## Title
[OTC][Backoffice] Add Withdrawal Accounts new tab in Member Mgmt Details page

## Status
Ready to Test in SIT | Assignee: Alexis Soo | Reporter: Ming En Leong

Type: Story | fixVersion: `0.15.0 - OTC` | Components: none | Labels: none
Created: 2026-07-21 | Updated: 2026-08-26
Build number: unknown — no build id stated on the ticket.

## Description

### Background
Member Details in the Back Office does not display the bank accounts or crypto addresses a member has
saved. Admins handling a member enquiry or a suspected unauthorised destination have no way to see what is
on the account, and no way to stop a destination being used. This enhancement introduces a **Withdrawal
Accounts** tab listing both destination types, with full detail views and admin `Disable` / `Enable` actions.

### User Story
As an admin, I want to see every bank account and crypto address a member has saved and disable any of
them, so that I can support member enquiries and stop a destination the member says they did not add.

### Behaviour Table
| Behaviour | Description |
|---|---|
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

- BR-1: **General Requirements** — A new **Withdrawal Accounts** tab is added under **Member Management → Member → Member Details**, with two sections — **Bank Accounts** at the top, **Crypto Addresses** below — both scoped to the member whose page is open. **Records are member-created only** — Back Office cannot create, edit or delete a record. The only admin actions are `Disable` and `Enable`. **No maker-checker** — both actions take effect immediately and are available to any Back Office role with Member Details access.
- BR-2: **Bank Accounts Section** — Lists every bank account belonging to the member, in any status. Columns: `Bank Name`, `Account Holder Name`, masked `Account Number / IBAN` (last 4 digits), `Currency` (the full list held on the account), `Status`, `Created Date`. Sorted most recently added first, with `Disabled` and `Deleted` records after `Active` ones. Statuses — `Active` / `Disabled` / `Deleted` (AO-923 Req 1).
- BR-3: **Bank Account Details** — Selecting a record opens a read-only detail drawer view showing every field captured in AO-923 Req 3 — `Label`, `Bank Country`, `Bank Name`, `Account Holder Name`, `Account Number / IBAN`, `BIC / SWIFT`, `Currency` list, `Address Line 1`, `Address Line 2`, `City`, `Postal Code`, `Bank Code / Routing Number`, `Account Type` — plus `Status`, `Created Date` and `Last Updated Date`. **The full account number is shown on this view**, since the Maker executes the transfer manually from this data (AO-923 Req 8). Every view of this screen is written to the audit log (BR-10).
- BR-4: **Crypto Addresses Section** — Lists every crypto address belonging to the member, in any status. Columns: `Asset`, `Network`, masked `Wallet Address` (first 6 and last 4 characters, per AO-922 Req 2), `Status`, `Created Date`. Same sort order, pagination and status model as BR-2.
- BR-5: **Crypto Address Details** — Selecting a record opens a read-only detail view showing `Label`, `Asset`, `Network`, the full `Wallet Address`, `Memo / Tag` where present, `Status`, `Created Date` and `Last Updated Date`. `Network` is required here because the mobile list does not display it, and the same address on the wrong network is a different destination.
- BR-6: **Disable & Enable Actions** — `Disable` is available on records in `Active` status, from the list row and the detail view, with a confirmation modal. Status becomes `Disabled` and the record is immediately unavailable for withdrawal: in the mobile app it renders in the disabled, non-clickable state (AO-923 Req 2) and is excluded from the withdrawal destination dropdown (AO-881 Req 2). **Disable is never blocked by an in-flight withdrawal** — it is a security action and must succeed even where a `Pending` withdrawal exists to that destination. The pending request is not automatically cancelled (BR-9). `Enable` is available on records in `Disabled` status, with a confirmation modal. Status returns to `Active` and the record is immediately usable again, and the member may add that destination again. **Enable is blocked where the member already holds the maximum number of active records** for that destination type — 5 bank accounts (AO-923 Req 1) or 20 crypto addresses (AO-922 Req 1) — since `Disabled` records do not count toward the limit.
- BR-7: **Deleted Records** — `Deleted` is member-initiated (AO-923 Req 6, AO-922 Req 5). The record is retained, never purged, and remains listed in this tab with its `Date Deleted` so the member's own action stays traceable. **No admin action is available on a deleted record** — it can be neither disabled nor enabled. A `Deleted` record does not prevent the member re-adding the same destination (BR-8).
- BR-8: **Re-add Prevention** — While a record is `Disabled`, the member cannot add the same destination again. **Bank accounts** — the normalised `Account Number / IBAN` plus `BIC / SWIFT` is matched against the member's `Active` and `Disabled` records. **Crypto addresses** — `Asset` + `Network` + `Address` is matched against the member's `Active` and `Disabled` records. `Deleted` records do **not** block re-adding. Member-facing error copy exists in AO-923 and AO-922.
- BR-9: **Impact on Pending Withdrawal Requests** — Where a withdrawal request in `Pending` status is linked to a destination that has since become `Disabled`, the checker **cannot approve it**. Attempting to approve returns a blocking error, and the only available action is `Reject`. On rejection the held amount is returned to the member's available balance (AO-881 Req 6) and the member is notified (AO-917). The request is not auto-rejected — a checker must action it, so the decision stays with a named human.
- BR-10: **Audit Log** *(not shown on UI)* — Record every `Disable` and `Enable` action with the admin, timestamp, record ID, destination type and member ID. Record every view of a Bank Account Details or Crypto Address Details screen, since both expose the destination in full. Member-initiated add and delete events are visible in the tab for reference.

## Acceptance Criteria

*The ticket has no `Acceptance Criteria` section. The criteria below are `derived` from the Requirements
table and the Back Office Flow.*

- AC-1: (derived) A **Withdrawal Accounts** tab exists under Member Management → Member → Member Details, showing a **Bank Accounts** section above a **Crypto Addresses** section, both scoped to the open member.
- AC-2: (derived) Back Office offers no create, edit or delete on either section — only `Disable` and `Enable`.
- AC-3: (derived) `Disable` and `Enable` take effect immediately with no maker-checker step, and are available to any Back Office role with Member Details access.
- AC-4: (derived) Bank Accounts lists every bank account in any status with columns `Bank Name`, `Account Holder Name`, masked `Account Number / IBAN` (last 4), `Currency`, `Status`, `Created Date`.
- AC-5: (derived) Both sections sort most recently added first, with `Disabled` and `Deleted` records after `Active` ones.
- AC-6: (derived) Bank Account Details opens read-only with all 13 AO-923 Req 3 fields plus `Status`, `Created Date`, `Last Updated Date`, and shows the **full** account number.
- AC-7: (derived) Crypto Addresses lists every crypto address in any status with columns `Asset`, `Network`, masked `Wallet Address` (first 6 + last 4), `Status`, `Created Date`.
- AC-8: (derived) Crypto Address Details opens read-only with `Label`, `Asset`, `Network`, full `Wallet Address`, `Memo / Tag` where present, `Status`, `Created Date`, `Last Updated Date`.
- AC-9: (derived) `Disable` is offered only on `Active` records, from both the list row and the detail view, and asks for confirmation before applying.
- AC-10: (derived) After `Disable` the record reads `Disabled`, is non-clickable/disabled in the mobile app, and is absent from the withdrawal destination dropdown.
- AC-11: (derived) `Disable` succeeds even where a `Pending` withdrawal exists to that destination, and does not cancel that request.
- AC-12: (derived) `Enable` is offered only on `Disabled` records, asks for confirmation, and returns the record to `Active` and immediately usable.
- AC-13: (derived) `Enable` is blocked with the active-limit message where the member already holds 5 active bank accounts or 20 active crypto addresses; `Disabled` records do not count toward those limits.
- AC-14: (derived) A `Disabled` record blocks the member re-adding the same destination — bank by normalised `Account Number / IBAN` + `BIC / SWIFT`, crypto by `Asset` + `Network` + `Address`.
- AC-15: (derived) A `Deleted` record stays listed with its `Date Deleted`, offers no admin action, and does not block re-adding the same destination.
- AC-16: (derived) A checker cannot approve a `Pending` withdrawal whose destination is `Disabled` — approval returns a blocking error and only `Reject` proceeds; on rejection the held amount returns to available balance and the member is notified.
- AC-17: (derived) Every `Disable`, `Enable`, and every view of a Bank Account Details or Crypto Address Details screen is written to the audit log with admin, timestamp, record ID, destination type and member ID.
- AC-18: (derived) An empty section shows the empty-state message rather than an empty table.

## Error Messages

*(source: description Back Office Messages table, and the identical table in the comment by Ming En Leong, 2026-08-20)*

- ERR-1: Disable confirmation — bank account. Header: "Disable this bank account?" Body: "{Label} will be immediately unavailable for withdrawal, and the member will not be able to add it again while it is disabled." CTAs: `Cancel` / `Disable`
- ERR-2: Disable confirmation — crypto address. Header: "Disable this crypto address?" Body: "{Label} · will be immediately unavailable for withdrawal, and the member will not be able to add it again while it is disabled." CTAs: `Cancel` / `Disable`
- ERR-3: Enable confirmation. Header: "Enable this {bank account / crypto address}?" Body: "{Label} · {Masked Number} will be available for withdrawal again immediately." CTAs: `Cancel` / `Enable`
- ERR-4: Disable succeeded — "This {bank account / crypto address} has been disabled."
- ERR-5: Enable succeeded — "This {bank account / crypto address} has been enabled."
- ERR-6: Enable blocked by the active limit — "This member already has {Limit} active {bank accounts / crypto addresses}. Disable another record before enabling this one."
- ERR-7: Checker attempts to approve a withdrawal to a disabled destination — "This withdrawal destination has been disabled and the request cannot be approved. Reject the request to return the funds to the member's available balance."
- ERR-8: Action failed — "Unable to complete this action. Please try again."
- ERR-9: Section empty state — "This member has no {bank accounts / crypto addresses}."

## Out of Scope

None — the current description states no Out of Scope section.

*(An earlier superseded revision of this ticket, posted as a comment by Alexis Soo on 2026-07-30 and
2026-08-05, listed: editing wallet addresses; deleting wallet addresses from Back Office; editing linked
bank accounts; deleting linked bank accounts; bulk approval or rejection; search and filtering
enhancements; export functionality; electronic bank account verification. That revision described an
Address Book / Linked Bank Accounts + maker-checker approval design that the 2026-08-20 revision replaced.
Do not test against it.)*

## Linked Issues

None declared in the `issuelinks` field. Referenced by requirement text:
- AO-923: member bank account model — statuses, 5-account limit, detail fields (Req 1, 2, 3, 6, 8)
- AO-922: member crypto address model — masking, 20-address limit, delete (Req 1, 2, 5)
- AO-881: withdrawal request flow — destination dropdown, funds return on reject (Req 2, 6)
- AO-917: member notification on withdrawal rejection

## Sub-tasks

### AO-1032: [OTC][Backoffice] Add Withdrawal Accounts new tab in Member Mgmt Details page
Type: Backend Development | Status: **In SIT** | fixVersion: 0.15.0 - OTC | No description.
Comment (Alexis Soo, 2026-08-18): "will complete by today"

### AO-1040: [OTC][Backoffice] Add Withdrawal Accounts new tab in Member Mgmt Details page
Type: Frontend Development | Status: **Pending Merge to SIT** | fixVersion: 0.15.0 - OTC | No description.
⚠️ Frontend is not yet merged to SIT. Confirm the tab is actually deployed before executing UI cases.

### AO-1054: [OTC][Backoffice] Add Withdrawal Accounts new tab in Member Mgmt Details page
Type: Design Request | Status: Approved | No description.

### AO-1087: [AO-925] [OTC][Backoffice] Add Withdrawal Accounts new tab in Member Mgmt Details page
Type: QA Preparation | Status: Done
Description: "suetfun reviewed @ 8/25/2026"
TC inventory (Huyen Mai Thi, updated 2026-08-25) — total 62 cases:
- 53 under **Members** folder (group 128)
- 2 under **Fiat Withdrawal** folder (group 3597), including existing case 151523
- 3 under **Withdrawal Accounts** folder (group 3595), including existing case 151419; case 162007 linked to AO-923, case 162008 linked to AO-922
- 1 under **Crypto Withdrawal** folder (group 3792)
- 3 under **Balance Approval** folder (group 374)

### AO-1098: [AO-925] [OTC][Backoffice] Add Withdrawal Accounts new tab in Member Mgmt Details page
Type: QA Execution | Status: To Do — this is the sub-task this SIT run reports against.

## Visual Context

No image attachments. Two `.zip` attachments only, neither downloadable as an image:
- `Withdrawal account tab design.zip` (1.79 MB, Alexis Soo, 2026-08-18)
- `Withdrawal account tab design (9f6c229d-86dc-4398-a325-b39d648e4fc6).zip` (1.79 MB, Ming En Leong, 2026-08-20)

The description and the 2026-08-20 comment each embed an inline media blob that the API returns without a
downloadable attachment entry — the design zips above are the same artefact.

## Figma Links

None. The only design reference is a Claude Design prototype:
https://claude.ai/design/p/83dfa170-b3e9-426f-8158-80c26891e257?file=Withdrawal+Account.dc.html&via=share

## Open Items from Comments

- Three TC additions requested by the reviewer and not yet confirmed as applied (Suet Fun Ng, 2026-08-25, on AO-1087): (1) a case verifying the Admin role CAN see Disable/Enable actions; (2) a case where the member holds 4 Active + 2 Disabled bank accounts and Enable succeeds, proving Disabled records are not counted; (3) a case where the member deletes a bank account then successfully re-adds the same Account Number/IBAN + BIC/SWIFT. Check `tc.md` for these three before execution.
- TC count was corrected from 62 to a reviewer-observed 60 and back — Huyen Mai Thi replied 2026-08-25 that some cases were linked while preparing other tickets. Treat the Testmo query as the source of truth, not the comment count.
- QA estimate 1.5 md (Suet Fun Ng, 2026-08-26).
- Frontend sub-task AO-1040 sits at `Pending Merge to SIT` while the parent reads `Ready to Test in SIT` — unresolved contradiction to settle before the run starts.

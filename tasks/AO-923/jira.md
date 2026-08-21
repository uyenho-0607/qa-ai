# Jira: AO-923

## Title
[OTC][MobileApp][Member] Linked Bank Accounts (Manage Bank Accounts) - Add, Edit, Remove

## Status
In Progress | Assignee: Ming En Leong | Reporter: Ming En Leong

---

## Description (latest — comment 244278, 2026-08-13)

### Background
Verified members can submit a bank account from the mobile app via a single generic form, confirmed with Email OTP, selecting one or more currencies. The account is created Active and immediately available for Fiat Withdrawal — no Back Office approval. Members can add or remove currencies on an existing account, or remove the account entirely.

### User Story
As a verified member, I want to register my bank account through the mobile app, so that I can withdraw my fiat balances to an account I control.

### Add Bank Account Flow
1. Member taps **My Account → Withdrawal Accounts → Linked bank accounts → Add Bank Account** (or **Withdrawal → Fiat → Bank Account → Add Bank Account**).
2. Member completes the form and selects one or more Currencies.
3. Member taps Continue; the system validates all mandatory fields and rules.
4. System sends a 6-digit Email OTP; member enters it to confirm.
5. Upon successful verification, the account is created with status `Active` and is immediately available for Fiat Withdrawal.
6. Member is notified by email that a bank account was added.

---

## Business Requirements

### BR-1 — General Requirements
- Only active members with **Approved** verification status can add a bank account.
- Entry points: **My Account → Withdrawal Accounts → Linked bank account → Add bank account** and **Withdrawal → Fiat → Bank Account → Add bank account**.
- Non-verified member clicking "Add bank account" is redirected to verification page (same behaviour as deposit module).
- **Email OTP required on submission** — 6-digit numeric code sent to registered email; must be entered before account is created.
- Bank account statuses: `ACTIVE` / `DISABLED` / `DELETED`.
  - `DISABLED` — set by Back Office, reversible.
  - `DELETED` — set by member, captured in backoffice (AO-925).
- **Account limit** — max **5 Active** bank accounts per member, configurable via system config. Limit counts accounts, not currencies. `DISABLED`/`DELETED` accounts do not count.
- **One record per physical account** — stored as a single record holding a list of currencies.

### BR-2 — Bank Account Listing
- Display list sorted by most recently added, Active accounts before Disabled.
- Search by `Label`, `Bank Name`, masked `Account Number` (last 4 digits displayed).
- `ACTIVE` accounts: clickable → Bank Account Details page.
- `DISABLED` accounts: displayed in disabled (non-clickable) state. Clicking shows error toast: *This bank account has been disabled, contact us for further assistance.*
- **Empty state**: *You haven't added a bank account yet. Add one to withdraw your fiat balances.* with `Add Bank Account` CTA.
- `Add Bank Account` CTA — disabled when member is at account limit of 5, with explanatory toast: *You've reached the maximum of {Limit} bank accounts. Please remove one before adding another.*

### BR-3 — Add Bank Account Details (Generic Form)
**Required fields:** `Label`, `Bank Country`, `Bank Name`, `Account Holder Name`, `Account Number / IBAN`, `BIC / SWIFT`, `Currency`, `Address Line 1`, `City`

**Optional fields:** `Bank Code / Routing Number`, `Account Type`, `Address Line 2`, `Postal Code`

Field rules:
- `Label` — Alphanumeric, max **30** characters. Identifies the bank account.
- `Bank Country` — Single-select from the platform's country list.
- `Bank Name` — Alphanumeric + special chars `& ' . , - ( ) /`, max 100 characters. Regex: `^[\p{L}\p{N}\s&'.,\-()/]+$`
- `Account Holder Name` — Alphanumeric, max 30 characters. Helper text: *Enter the name exactly as it appears on your bank account.*
- `Account Number / IBAN` — Alphanumeric, up to 34 characters. No format validation this sprint.
- `BIC / SWIFT` — 8 or 11 characters per ISO 9362.
- `Bank Code / Routing Number` — Optional free text. Helper text: *If your bank uses a sort code, routing number, BSB or similar, enter it here.*
- `Account Type` — Optional single-select: `Checking` / `Savings` / `Not specified`.
- `Currency` — Multi-select, at least one required. Helper text: *Select the currencies this account can receive.* Member-declared; platform cannot verify.
- `Beneficiary Address` — `Address Line 1`, `Address Line 2` (optional), `City`, `Postal Code` (optional).

### BR-3b — Input Validation (on Continue)
- All required fields in BR-3 completed.
- **(Optional BE)** IBAN checksum — per-country length check then ISO 7064 MOD-97-10.
- **(Optional BE)** BIC format — 8 or 11 characters per ISO 9362.
- **BIC country cross-check** — BIC chars 5–6 encode country. If they disagree with `Bank Country`, show a warning popup (non-blocking, member can "Continue anyway" or "Review Details").
  - Warning: *This SWIFT/BIC code looks like it belongs to a bank in {BIC Country}, but you selected {Bank Country}. Please check before continuing.*
- **Uniqueness** — normalised `Account Number / IBAN` + `BIC / SWIFT` must not match an existing record for the same member.
- Member must be below the limit of 5 active accounts.

### BR-4 — Review Bank Account
- Read-only screen displaying all member input.
- Back button retains all values.
- "Submit" redirects to Email OTP verification.

### BR-5 — Email OTP Verification
- Member must enter correct OTP to add bank account.
- OTP validation follows existing onboarding flow.
- Upon successful verification: account created as `Active`, all selected currencies immediately usable.

### BR-6 — Edit Linked Bank Accounts
- **Edit Label** — editable from Bank Account Details page.
- **Add Currency** — no Email OTP required; currency immediately usable for Fiat Withdrawal.
- **Remove Currency** — no OTP required; blocked if pending withdrawal to that currency.
- **Cannot remove last remaining currency** — "Save changes" button disabled when last currency is deselected (FE dev note: no error message yet — pending PM confirmation).
- **Delete Account** — no Email OTP required. Account immediately unavailable; removed from member listing. Record retained (status `Deleted`, not purged); visible in Backoffice with Date Deleted timestamp.
  - Delete blocked while pending withdrawal associated with the account.
  - Confirmation dialog — Header: *Delete bank account?* | Message: *Removing this bank account will prevent it from being used for future withdrawals. This action won't affect completed transactions.* | CTA: **Delete** / **Cancel**
- **Disabled account** — read-only details; toast on click: *This bank account has been disabled, contact us for further assistance.*

### BR-7 — Notifications
- Email sent to member on every successful bank account addition.
- Adding or removing a currency does **not** trigger a separate notification.

### BR-8 — Back Office Impact (AO-925)
- Bank accounts visible under Member Management → Member → Member Details → Withdrawal Account.
- All fields from BR-3 visible to Maker.
- Currency list per account visible.
- Full `Account Number / IBAN` visible to Maker (unmasked).
- `DELETED` records remain visible with deletion info for audit.

---

## Acceptance Criteria

Note: No formal AC block in the description. Derived from description and requirements.

- AC-1 (derived) — Verified members can add a bank account via My Account → Withdrawal Accounts → Linked Bank Accounts → Add Bank Account.
- AC-2 (derived) — Verified members can add a bank account via Withdrawal → Fiat → Bank Account → Add Bank Account.
- AC-3 (derived) — Non-verified member is redirected to verification flow on tapping Add Bank Account.
- AC-4 (derived) — All required form fields are validated on Continue; errors shown inline.
- AC-5 (derived) — BIC country cross-check warning appears when BIC country code mismatches Bank Country (non-blocking).
- AC-6 (derived) — Duplicate account (same Account Number + BIC/SWIFT) is rejected with error.
- AC-7 (derived) — Email OTP is sent to registered email on Submit; account is created Active after successful OTP.
- AC-8 (derived) — Account limit of 5 Active accounts is enforced; Add Bank Account CTA disabled and toast shown at limit.
- AC-9 (derived) — Listing displays Active accounts before Disabled, sorted most recently added first.
- AC-10 (derived) — Listing search works by Label, Bank Name, masked Account Number (last 4 digits).
- AC-11 (derived) — Disabled account is non-clickable; shows error toast when tapped.
- AC-12 (derived) — Member can edit Label from Bank Account Details page.
- AC-13 (derived) — Member can add a currency without OTP; currency immediately available for Fiat Withdrawal.
- AC-14 (derived) — Member can remove a currency without OTP; blocked if pending withdrawal for that currency.
- AC-15 (derived) — Member cannot remove the last remaining currency (Save changes button disabled).
- AC-16 (derived) — Member can delete a bank account (no OTP); deletion blocked if pending withdrawal.
- AC-17 (derived) — Deleted account is removed from member listing; record retained in Backoffice with status Deleted + Date Deleted.
- AC-18 (derived) — Confirmation email sent on successful account addition; no email on currency add/remove.
- AC-19 (derived) — Backoffice Maker can view all BR-3 fields including unmasked Account Number/IBAN.
- AC-20 (derived) — DISABLED and DELETED accounts do not count toward the 5-account limit.

---

## Error Validation Messages

### From latest description (comment 244278)

| ID | Scenario | Message |
|----|----------|---------|
| ERR-1 | Account Number / IBAN is empty | *Please enter an account number.* |
| ERR-2 | IBAN fails length or checksum validation | *Please check your IBAN and try again.* |
| ERR-3 | BIC / SWIFT is empty | *Please enter your bank's SWIFT/BIC code. Your bank can provide this if you don't have it.* |
| ERR-4 | BIC / SWIFT fails format validation | *Please check the SWIFT/BIC code and try again.* |
| ERR-5 | BIC country does not match Bank Country (warning, confirmable) | *This SWIFT/BIC code looks like it belongs to a bank in {BIC Country}, but you selected {Bank Country}. Please check before continuing.* |
| ERR-6 | Beneficiary address incomplete | *Please complete your address. Your bank needs this to receive transfers.* |
| ERR-7 | No currency selected | *Please select at least one currency.* |
| ERR-8 | Duplicate of an existing non-cancelled account | *You've already added this bank account. You can add more currencies to it instead.* |
| ERR-9 | Duplicate of a Disabled account | *This bank account can't be added. Please contact support for assistance.* |
| ERR-10 | Attempt to remove last remaining currency | *(No error message — Save changes button disabled; pending PM confirmation per dev note)* |
| ERR-11 | Attempt to remove currency with withdrawal in flight | *You have a {Currency} withdrawal in progress to this account. You can remove it once that withdrawal is complete.* |
| ERR-12 | Attempt to add/remove currency on Suspended/Disabled account | *This bank account is suspended. Please contact support for assistance.* |
| ERR-13 | Account limit reached | *You've reached the maximum of {Limit} bank accounts. Please remove one before adding another.* |
| ERR-14 | Removal (delete account) attempted while withdrawal in flight | *You have a withdrawal in progress to this account. You can remove it once that withdrawal is complete.* |
| ERR-15 | Disabled account tapped in listing | *This bank account has been disabled, contact us for further assistance.* |

### From main description body (older, kept for reference)

| ID | Scenario | Message |
|----|----------|---------|
| ERR-D1 | Label is empty | *Please enter a label.* |
| ERR-D2 | Label exceeds 30 characters | *Label cannot exceed 30 characters.* |
| ERR-D3 | Bank Country is not selected | *Please select a bank country.* |
| ERR-D4 | Bank Name is empty | *Please enter a bank name.* |
| ERR-D5 | Bank Name exceeds 100 characters | *Bank name cannot exceed 100 characters.* |
| ERR-D6 | No currency selected | *Please select at least one currency.* |
| ERR-D7 | Account Name is empty | *Please enter the account name.* |
| ERR-D8 | Account Name exceeds 30 characters | *Account name cannot exceed 30 characters.* |
| ERR-D9 | Account Number / IBAN is empty | *Please enter an account number.* |
| ERR-D10 | Account Number / IBAN exceeds 34 characters | *Account number cannot exceed 34 characters.* |
| ERR-D11 | BIC / SWIFT is empty | *Please enter your bank's SWIFT/BIC code.* |
| ERR-D12 | BIC / SWIFT exceeds 11 characters | *SWIFT/BIC code cannot exceed 11 characters.* |
| ERR-D13 | Address Line 1 is empty | *Please enter your address.* |
| ERR-D14 | Address Line 1 exceeds 100 characters | *Address Line 1 cannot exceed 100 characters.* |
| ERR-D15 | Address Line 2 exceeds 100 characters | *Address Line 2 cannot exceed 100 characters.* |
| ERR-D16 | City is empty | *Please enter your city.* |
| ERR-D17 | City exceeds 100 characters | *City cannot exceed 100 characters.* |
| ERR-D18 | Postal Code exceeds 100 characters | *Postal Code cannot exceed 100 characters.* |
| ERR-D19 | Account limit reached | *You've reached the maximum of 5 linked bank accounts. Delete one to add another.* |
| ERR-D20 | Bank code exceeds 100 characters | *Bank code cannot exceed 100 characters.* |

---

## Out of Scope

1. **Freeze Period / holding period** — AO-921, next sprint. *(feature-absence)*
2. **Per-country or per-bank field configuration** — removed by decision 30 Jul 2026. *(feature-absence)*
3. **Corridor-specific fields** (beneficiary tax ID, purpose-of-payment, intermediary bank). *(feature-absence)*
4. **Account holder name matching against KYC name**. *(feature-absence)*
5. **Editing any field other than Label and currencies** — members remove and re-add. *(restricted-capability → negative TC: other fields cannot be edited)*
6. **Verifying that an account accepts a declared currency**. *(feature-absence)*
7. **Electronic bank account verification, Open Banking, micro-deposit, bank-API name checks**. *(feature-absence)*
8. **In-app Inbox and push delivery** — AO-917 and AO-991. Email only this sprint. *(feature-absence)*
9. **Back Office Withdrawal Destination module** — AO-925. *(out of scope for this ticket)*

---

## Linked Issues
- AO-992: [OTC][MobileApp] Consistent Email OTP behaviour (connects to) — Backlog

## Sub-tasks
- AO-981: Design Request — Ready To Review
- AO-982: Backend Development — Pending Review
- AO-983: Frontend Development — Pending Merge to SIT
- AO-1086: QA Preparation — REVIEW DONE (121 cases already in Testmo: 1 Account, 117 Withdrawal Accounts, 3 Members)
- AO-1097: QA Execution — To Do

## Figma
- https://www.figma.com/design/0JJeXQvNYqZfaTzQFPMR4a/OTC-Mobile-App?node-id=7072-149597&t=yeinnEDcSe5CBnuD-1

## Open Items from Comments
- ERR-10 (last currency removal) — error message text pending PM confirmation. FE currently disables Save button.
- ERR-8 (duplicate account) and ERR-4 (BIC/SWIFT format) — error messages confirmed by dev (Dinh Hieu) on 2026-08-20:
  - ERR-8 message from latest requirements stands.
  - ERR-4 FE temporary: "Please check the BIC/SWIFT code and try again" (matches ERR-4 above).

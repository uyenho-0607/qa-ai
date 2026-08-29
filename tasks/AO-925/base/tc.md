# Test Cases — AO-925

**Issue:** [AO-925](https://aquariux.atlassian.net/browse/AO-925)
**Source:** Testmo — project 8 (OTC), `testmo_find_cases_by_issue`
**Fetched:** 2026-08-27
**Total:** 65 cases

## Summary

| Status | Count |
|---|---|
| ✅ Automated (39) | 0 |
| 🔧 Can Automate (37) | 0 |
| 🚧 In Progress (38) | 0 |
| ❌ Not Automatable (40) | 0 |
| ⬜ Unset | 65 |

| Priority | Count |
|---|---|
| High (54) | 0 |
| Medium (55) | 0 |
| Low (56) | 0 |
| ⬜ Unset | 65 |

`custom_priority` and `custom_automation1` are `null` on all 65 cases. Every case carries `state_id: 4`
(`.claude/steering/testmo.md` documents only state `2` = Pending Review — id `4` is unmapped there).

### By Testmo folder

| Folder | id | Cases |
|---|---|---|
| Members | 128 | 55 |
| Balance Approvals | 374 | 3 |
| Withdrawal Accounts | 3595 | 4 |
| Fiat Withdrawal | 3597 | 2 |
| Crypto Withdrawal | 3792 | 1 |

### By surface (derived from case content — confirm at exec design)

| Surface | Cases |
|---|---|
| `bo` — Back Office only | 47 |
| `app` — member app only | 4 |
| `bo+app` — flow crosses both | 14 |

## Case Groups

| Group | Cases | Automated | Can Automate | Pattern |
|---|---|---|---|---|
| Mobile→BO record sync | 3 | 0 | 0 | add / edit / delete on mobile, verified in BO |
| Withdrawal Accounts tab | 2 | 0 | 0 | tab visible, both sections load |
| Role & action availability | 4 | 0 | 0 | no create/edit/delete; Maker, Checker, Admin |
| Bank Accounts list | 3 | 0 | 0 | empty state, columns, sort order |
| Bank Account Details | 4 | 0 | 0 | drawer opens, unmasked number, blanks, Deleted read-only |
| Bank Account Disable | 6 | 0 | 0 | entry points, modal copy, cancel, confirm, pending-withdrawal |
| Bank Account Enable | 7 | 0 | 0 | entry points, modal copy, cancel, confirm, limit block, limit exclusion |
| Crypto Addresses list | 3 | 0 | 0 | empty state, columns, sort order |
| Crypto Address Details | 4 | 0 | 0 | drawer opens, unmasked address, Memo/Tag absent, Deleted read-only |
| Crypto Address Disable | 6 | 0 | 0 | entry points, modal copy, cancel, confirm, pending-withdrawal |
| Crypto Address Enable | 6 | 0 | 0 | entry points, modal copy, cancel, confirm, limit block |
| Audit log | 2 | 0 | 0 | Disable and Enable events written with required fields |
| API failure | 2 | 0 | 0 | Disable and Enable server error, no status change |
| Concurrency | 3 | 0 | 0 | two admins racing at the limit / on the same record |
| Balance Approvals | 3 | 0 | 0 | approve blocked, reject allowed, no auto-reject |
| App — Withdrawal Accounts | 4 | 0 | 0 | disable reflected in app, re-add blocked / allowed |
| App — Fiat Withdrawal | 2 | 0 | 0 | disabled badge non-selectable, re-enabled selectable |
| App — Crypto Withdrawal | 1 | 0 | 0 | disabled crypto address non-clickable |

---

## Full Case Details

### Mobile→BO record sync (3 cases) · folder 128

#### TC-151414 · Members – Details – Withdrawal account record visible in BO after add on mobile
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify a newly added bank account on mobile is reflected in BO

**Prerequisites:**
- Member has successfully added a bank account on the mobile app
- Back Office Maker is on Member Management → Member Details → Withdrawal Account

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Locate the member in BO and open their Withdrawal Account section | 1. Newly added bank account record is visible in BO<br>2. All field values match what was submitted on the mobile form<br>3. Status shows as Active |

**Test Data:** —

---

#### TC-151415 · Members – Details – Withdrawal account record updated in BO after edit on mobile
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify BO reflects the latest data after a member edits their bank account on mobile

**Prerequisites:**
- Member has successfully saved changes on the Edit Bank Account screen
- Back Office Maker is on Member Management → Member Details → Withdrawal Account

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Locate the edited bank account record in BO | 1. Updated label is reflected in BO<br>2. Updated currency list is reflected in BO<br>3. Other fields remain unchanged |

**Test Data:** —

---

#### TC-151416 · Members – Details – Withdrawal account record shows Deleted status after delete on mobile
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify BO reflects Deleted status after a member deletes their bank account on mobile

**Prerequisites:**
- Member has successfully deleted a bank account on the mobile app
- Back Office Maker is on Member Management → Member Details → Withdrawal Account

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Locate the deleted bank account record in BO | 1. Record is still visible in BO (retained for audit)<br>2. Status shows as Deleted<br>3. Date Deleted timestamp is displayed |

**Test Data:** —

---

### Withdrawal Accounts tab (2 cases) · folder 128

#### TC-161963 · Members – Details – Withdrawal Accounts tab visible in Member Details
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify Withdrawal Accounts tab is visible and accessible in Member Details

**Prerequisites:**
- Admin is on the Member Details page of any member

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Observe the tabs available on the Member Details page | 1. A "Withdrawal Accounts" tab is visible alongside other existing tabs<br>2. No errors occur |

**Test Data:** —

---

#### TC-161967 · Members – Details – Withdrawal Accounts tab loads Bank Accounts and Crypto Addresses sections
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify clicking the Withdrawal Accounts tab loads both sections

**Prerequisites:**
- Admin is on the Member Details page
- "Withdrawal Accounts" tab is visible

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Click on the "Withdrawal Accounts" tab | — |
| 2 | 2. Observe the page content | 1. The Withdrawal Accounts page loads successfully<br>2. "Bank Accounts" section is visible at the top<br>3. "Crypto Addresses" section is visible below Bank Accounts<br>4. Each section heading is clearly labelled |

**Test Data:** —

---

### Role & action availability (4 cases) · folder 128

#### TC-161964 · Members – Details – No Create Edit or Delete action available on any withdrawal account record
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify Back Office cannot create, edit or delete a withdrawal account record

**Prerequisites:**
- Admin is on the Withdrawal Accounts tab
- Member has at least one bank account and one crypto address in any status

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Observe the Withdrawal Accounts tab for any Create / Add / New button | 1. No Create, Add, or New button is present on the Withdrawal Accounts tab |
| 2 | 2. Open the action menu and detail drawer for a bank account record and a crypto address record in each status (Active, Disabled, Deleted) | 1. No Edit or Delete action is available in any action menu or detail drawer for any record in any status |

**Test Data:** —

---

#### TC-161965 · Members – Details – Maker role cannot see Disable or Enable actions on withdrawal account records
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify Maker role does not have access to Disable or Enable actions on withdrawal account records

⚠️ **Conflicts with BR-1 / AC-1**, which states Disable and Enable are "available to any Back Office role with
Member Details access". Resolve at exec design before running.

**Prerequisites:**
- A Maker-role user is logged in to Back Office
- Member has at least one Active bank account and one Active crypto address

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Open any member's Withdrawal Accounts tab | — |
| 2 | 2. Open the action menu for an Active bank account record and an Active crypto address record | 1. No Disable or Enable action is available in any action menu for bank account or crypto address records<br>2. The Withdrawal Accounts tab and all records are visible in read-only mode |

**Test Data:** —

---

#### TC-161966 · Members – Details – Checker role cannot see Disable or Enable actions on withdrawal account records
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify Checker role does not have access to Disable or Enable actions on withdrawal account records

⚠️ **Conflicts with BR-1 / AC-1** — same conflict as TC-161965.

**Prerequisites:**
- A Checker-role user is logged in to Back Office
- Member has at least one Active bank account and one Active crypto address

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Open any member's Withdrawal Accounts tab | — |
| 2 | 2. Open the action menu for an Active bank account record and an Active crypto address record | 1. No Disable or Enable action is available in any action menu for bank account or crypto address records<br>2. The Withdrawal Accounts tab and all records are visible in read-only mode |

**Test Data:** —

---

#### TC-191123 · Members – Details – Admin role CAN see Disable and Enable actions on withdrawal account records
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify Admin role has access to Disable and Enable actions on withdrawal account records

Added 2026-08-25 in response to Suet Fun Ng's review request on AO-1087.

**Prerequisites:**
- An Admin-role user is logged in to Back Office
- Member has at least one Active bank account and one Active crypto address
- Member also has at least one Disabled bank account and one Disabled crypto address

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Open any member's Withdrawal Accounts tab | — |
| 2 | 2. Open the action menu for an Active bank account record | 1. A "Disable" action option is visible and clickable |
| 3 | 3. Open the action menu for an Active crypto address record | 1. A "Disable" action option is visible and clickable |
| 4 | 4. Open the action menu for a Disabled bank account record | 1. An "Enable" action option is visible and clickable |
| 5 | 5. Open the action menu for a Disabled crypto address record | 1. An "Enable" action option is visible and clickable |

**Test Data:** —

---

### Bank Accounts list (3 cases) · folder 128

#### TC-161968 · Members – Details – Bank Accounts empty state when member has no bank accounts
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify the empty state message is shown when member has no saved bank accounts

**Prerequisites:**
- Admin is on the Withdrawal Accounts tab
- Member has no saved bank accounts

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Observe the Bank Accounts section | 1. The section displays: "This member has no bank accounts."<br>2. No table rows or loading indicators are shown |

**Test Data:** —

---

#### TC-161969 · Members – Details – Bank Accounts list all required columns displayed
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify Bank Accounts section displays all required columns with correct headers

**Prerequisites:**
- Admin is on the Withdrawal Accounts tab of a member who has at least one bank account

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Observe the Bank Accounts section table columns | 1. The following columns are visible: Bank Name, Account Holder Name, Account Number / IBAN (masked), Currency, Status, Created Date<br>2. Column headers match the specified labels exactly |
| 2 | 2. Observe the Account Number / IBAN column in the Bank Accounts list | 1. Account Number / IBAN is displayed masked — only the last 4 digits are visible (e.g. \*\*\*\* \*\*\*\* \*\*\*\* 1234)<br>2. The full account number is not visible in the list |
| 3 | 3. Observe the Currency column for a bank account linked to multiple currencies | 1. The Currency column displays all currency codes linked to that bank account (e.g. USD, HKD)<br>2. No currencies are truncated or hidden |

**Test Data:** —

---

#### TC-161970 · Members – Details – Bank Accounts sort order Active first then Disabled then Deleted
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify Active bank accounts appear before Disabled and Deleted records in the list

**Prerequisites:**
- Admin is on the Withdrawal Accounts tab
- Member has Active, Disabled, and Deleted bank accounts

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Observe the sort order in the Bank Accounts list | 1. Active records appear at the top, sorted by Created Date descending (most recent first)<br>2. Disabled records appear after all Active records, sorted by Created Date descending<br>3. Deleted records appear last, sorted by Created Date descending |

**Test Data:** —

---

### Bank Account Details (4 cases) · folder 128

#### TC-161971 · Members – Details – Bank Account Details drawer opens on record click
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify clicking a bank account record in the list opens the detail drawer

**Prerequisites:**
- Admin is on the Withdrawal Accounts tab
- Member has at least one bank account

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Click on any bank account record in the list | 1. A read-only detail drawer opens<br>2. The following fields are visible: Label, Bank Country, Bank Name, Account Holder Name, Account Number / IBAN (full unmasked), BIC / SWIFT, Currency list, Address Line 1, Address Line 2, City, Postal Code, Bank Code / Routing Number, Account Type<br>3. Status, Created Date, and Last Updated Date are also displayed<br>4. All field values match the data the member saved |

**Test Data:** —

---

#### TC-161972 · Members – Details – Bank Account Details full account number shown unmasked
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify the full Account Number / IBAN is displayed unmasked in the detail drawer — visible to Maker role only

**Prerequisites:**
- Logged in to Back Office as a Maker role
- Member has at least one linked bank account
- Maker has opened the Bank Account detail drawer

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Observe the Account Number / IBAN field in the detail drawer | 1. The full unmasked Account Number / IBAN is shown<br>2. This is different from the masked format (last 4 digits only) shown in the list view |

**Test Data:** —

---

#### TC-161973 · Members – Details – Bank Account Details optional fields blank when not provided
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify optional fields display correctly as empty when the member did not fill them in

**Prerequisites:**
- Admin has opened the Bank Account detail drawer for an account where Address Line 2, Bank Code / Routing Number, and Account Type were not provided

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Observe optional fields in the detail drawer | 1. Optional fields not filled in by the member show as "-" |

**Test Data:** —

---

#### TC-161986 · Members – Details – Bank Account Details Deleted record opens with no action buttons
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify a Deleted bank account detail drawer is read-only with no Disable or Enable buttons

**Prerequisites:**
- Admin is on the Withdrawal Accounts tab
- Member has at least one Deleted bank account

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Click on a Deleted bank account record in the list | 1. The detail drawer opens successfully<br>2. All fields are visible in read-only mode<br>3. No Disable or Enable buttons are present<br>4. Status field shows "Deleted" |

**Test Data:** —

---

### Bank Account Disable (6 cases) · folder 128

#### TC-161974 · Members – Details – Bank Account Disable option visible on Active record in list
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify the Disable action is available for Active bank account records from the list

**Prerequisites:**
- Admin is on the Withdrawal Accounts tab
- Member has at least one Active bank account

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Locate an Active bank account in the list | — |
| 2 | 2. Open the action menu (e.g. overflow "..." button) for that record | 1. A "Disable" action option is visible |

**Test Data:** —

---

#### TC-161975 · Members – Details – Bank Account Disable button visible in Active record detail drawer
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify the Disable button is available inside the Bank Account detail drawer for Active records

**Prerequisites:**
- Admin has opened the detail drawer of an Active bank account

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Observe the action buttons available in the detail drawer | 1. A "Disable" button is visible and clickable |

**Test Data:** —

---

#### TC-161976 · Members – Details – Bank Account Disable confirmation modal content correct
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify clicking Disable on a bank account shows the confirmation modal with correct copy

**Prerequisites:**
- Admin has clicked Disable on an Active bank account (Label: "My HSBC Account")

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Click the Disable action on an Active bank account | 1. A confirmation modal appears<br>2. Modal header: "Disable this bank account?"<br>3. Modal body: "{Label} will be immediately unavailable for withdrawal, and the member will not be able to add it again while it is disabled." (e.g. "My HSBC Account will be immediately unavailable...")<br>4. Two CTAs are visible: "Cancel" and "Disable" |

**Test Data:** Label "My HSBC Account"

---

#### TC-161977 · Members – Details – Bank Account Disable cancel on modal keeps record Active
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify clicking Cancel on the Disable confirmation modal makes no changes

**Prerequisites:**
- Admin has clicked Disable on an Active bank account and the confirmation modal is open

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Click "Cancel" on the Disable confirmation modal | 1. The modal closes<br>2. The bank account remains in Active status<br>3. No changes are made |

**Test Data:** —

---

#### TC-161978 · Members – Details – Bank Account Disable confirm changes status to Disabled immediately
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify confirming Disable changes the bank account status to Disabled immediately

**Prerequisites:**
- Admin has clicked Disable on an Active bank account (Label: "My HSBC Account") and the confirmation modal is open

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Click "Disable" on the confirmation modal | — |
| 2 | 2. Observe the result in the list and drawer | 1. The modal closes<br>2. Success message shown: "This bank account has been disabled."<br>3. The bank account status changes to "Disabled" immediately<br>4. The record moves to after the Active group in the sorted list<br>5. The Last Updated Date updates to the current timestamp |

**Test Data:** Label "My HSBC Account"

---

#### TC-161979 · Members – Details – Bank Account Disable not blocked by existing Pending withdrawal
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify Disable succeeds even when a Pending withdrawal exists to that bank account

**Prerequisites:**
- Admin is on the Withdrawal Accounts tab
- Member has an Active bank account that has a linked Pending withdrawal request

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Click Disable on the Active bank account that has a linked Pending withdrawal | — |
| 2 | 2. Confirm the Disable action in the modal | — |
| 3 | 3. Observe the bank account status and the Pending withdrawal status in Back Office | 1. The Disable action succeeds without error<br>2. Success message: "This bank account has been disabled."<br>3. The bank account status changes to Disabled<br>4. The linked Pending withdrawal request remains in Pending status — it is not auto-cancelled |

**Test Data:** —

---

### Bank Account Enable (7 cases) · folder 128

#### TC-161980 · Members – Details – Bank Account Enable option visible on Disabled record in list
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify the Enable action is available for Disabled bank account records from the list

**Prerequisites:**
- Admin is on the Withdrawal Accounts tab
- Member has at least one Disabled bank account

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Locate a Disabled bank account in the list | — |
| 2 | 2. Open the action menu for that record | 1. An "Enable" action option is visible |

**Test Data:** —

---

#### TC-161981 · Members – Details – Bank Account Enable button visible in Disabled record detail drawer
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify the Enable button is available inside the Bank Account detail drawer for Disabled records

**Prerequisites:**
- Admin has opened the detail drawer of a Disabled bank account

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Observe the action buttons in the detail drawer | 1. An "Enable" button is visible and clickable |

**Test Data:** —

---

#### TC-161982 · Members – Details – Bank Account Enable confirmation modal content correct
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify clicking Enable on a Disabled bank account shows the modal with correct copy

**Prerequisites:**
- Admin has clicked Enable on a Disabled bank account (Label: "My HSBC Account", masked number: \*\*\*\* 1234)

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Click the Enable action on a Disabled bank account | 1. A confirmation modal appears<br>2. Modal header: "Enable this bank account?"<br>3. Modal body: "{Label} · {Masked Account Number} will be available for withdrawal again immediately." (e.g. "My HSBC Account · \*\*\*\* 1234 will be available for withdrawal again immediately.")<br>4. Two CTAs: "Cancel" and "Enable" |

**Test Data:** Label "My HSBC Account", masked number \*\*\*\* 1234

---

#### TC-161983 · Members – Details – Bank Account Enable cancel on modal keeps record Disabled
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify clicking Cancel on the Enable confirmation modal makes no changes

**Prerequisites:**
- Admin has clicked Enable on a Disabled bank account and the confirmation modal is open

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Click "Cancel" on the modal | 1. The modal closes<br>2. The bank account remains in Disabled status<br>3. No changes are made |

**Test Data:** —

---

#### TC-161984 · Members – Details – Bank Account Enable confirm changes status to Active immediately
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify confirming Enable changes the bank account status to Active immediately

**Prerequisites:**
- Admin has clicked Enable on a Disabled bank account and the confirmation modal is open
- Member has fewer than 5 Active bank accounts

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Click "Enable" on the confirmation modal | — |
| 2 | 2. Observe the result in the list | 1. The modal closes<br>2. Success message: "This bank account has been enabled."<br>3. The bank account status changes to "Active" immediately<br>4. The record moves back to the Active group in the sorted list |

**Test Data:** —

---

#### TC-161985 · Members – Details – Bank Account Enable blocked when member already has 5 Active bank accounts
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify Enable is blocked when member is at the maximum of 5 Active bank accounts

**Prerequisites:**
- Member already has exactly 5 Active bank accounts
- Member has at least 1 Disabled bank account

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Click Enable on a Disabled bank account | — |
| 2 | 2. Observe the result | 1. Enable is blocked<br>2. Error message displayed: "This member already has 5 active bank accounts. Disable another record before enabling this one."<br>3. The Disabled bank account remains in Disabled status |

**Test Data:** Member with exactly 5 Active + ≥1 Disabled bank accounts

---

#### TC-191124 · Members – Details – Bank Account Enable succeeds when member has 4 Active and 2 Disabled accounts (Disabled not counted toward limit)
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify Enable succeeds when member has 4 Active and 2 Disabled bank accounts, confirming that Disabled accounts do not count toward the 5-account active limit

Added 2026-08-25 in response to Suet Fun Ng's review request on AO-1087.

**Prerequisites:**
- An Admin-role user is logged in to Back Office
- Member has exactly 4 Active bank accounts and 2 Disabled bank accounts (6 total)

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Open the member's Withdrawal Accounts tab | 1. Bank Accounts section shows 4 Active records and 2 Disabled records |
| 2 | 2. Click Enable on one of the Disabled bank accounts | 1. Enable confirmation modal appears |
| 3 | 3. Confirm the Enable action in the modal | 1. Success message: "This bank account has been enabled."<br>2. The bank account status changes to Active immediately<br>3. Bank Accounts section now shows 5 Active records and 1 Disabled record<br>4. No limit error is shown — Disabled accounts are NOT counted toward the 5-account limit |

**Test Data:** Member with exactly 4 Active + 2 Disabled bank accounts

---

### Crypto Addresses list (3 cases) · folder 128

#### TC-161987 · Members – Details – Crypto Addresses empty state when member has no crypto addresses
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify the empty state message is shown when member has no saved crypto addresses

**Prerequisites:**
- Admin is on the Withdrawal Accounts tab
- Member has no saved crypto addresses

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Observe the Crypto Addresses section | 1. The section displays: "This member has no crypto addresses."<br>2. No table rows or loading indicators are shown |

**Test Data:** —

---

#### TC-161988 · Members – Details – Crypto Addresses list all required columns displayed
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify Crypto Addresses section displays all required columns with correct headers

**Prerequisites:**
- Admin is on the Withdrawal Accounts tab
- Member has at least one saved crypto address

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Observe the Crypto Addresses section table columns | 1. The following columns are visible: Asset, Network, Wallet Address (masked), Status, Created Date<br>2. Column headers match the specified labels exactly |
| 2 | 2. Observe the Wallet Address column in the Crypto Addresses list | 1. Wallet Address is shown in masked format: first 6 characters + separator + last 4 characters (e.g. 0x1234...5678)<br>2. The characters between first 6 and last 4 are not visible |
| 3 | 3. Observe the Network column in the Crypto Addresses list | 1. The Network column is visible<br>2. Each row shows the correct network for that crypto address (e.g. USDT on ERC20 shows "ERC20", USDT on TRC20 shows "TRC20") |

**Test Data:** —

---

#### TC-161989 · Members – Details – Crypto Addresses sort order Active first then Disabled then Deleted
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify Active crypto addresses appear before Disabled and Deleted records

**Prerequisites:**
- Admin is on the Withdrawal Accounts tab
- Member has Active, Disabled, and Deleted crypto addresses

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Observe the sort order in the Crypto Addresses list | 1. Active records appear at the top, sorted by Created Date descending<br>2. Disabled records appear after all Active records, sorted by Created Date descending<br>3. Deleted records appear last, sorted by Created Date descending |

**Test Data:** —

---

### Crypto Address Details (4 cases) · folder 128

#### TC-161990 · Members – Details – Crypto Address Details drawer opens on record click
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify clicking a crypto address record opens the detail drawer with all required fields

**Prerequisites:**
- Admin is on the Withdrawal Accounts tab
- Member has at least one crypto address with all fields populated (including Memo/Tag)

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Click on any crypto address record in the list | 1. A read-only detail drawer opens<br>2. The following fields are visible: Label, Asset, Network, Wallet Address (full unmasked), Memo / Tag (supported address), Status, Created Date, Last Updated Date<br>3. All values match the data the member saved |

**Test Data:** —

---

#### TC-161991 · Members – Details – Crypto Address Details full wallet address shown unmasked in drawer
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify the full Wallet Address is displayed unmasked in the detail drawer

**Prerequisites:**
- Admin has opened the Crypto Address detail drawer
- The address has a known full wallet address

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Observe the Wallet Address field in the detail drawer | 1. The full unmasked Wallet Address is shown<br>2. This differs from the masked format (first 6 + last 4) shown in the list |

**Test Data:** —

---

#### TC-161992 · Members – Details – Crypto Address Details Memo/Tag hidden when asset/network does not support it
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify Memo/Tag field is absent when the asset/network does not use it

**Prerequisites:**
- Admin has opened the Crypto Address detail drawer for an address that does not support Memo/Tag (e.g. BTC-Bitcoin)

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Observe the Memo / Tag field area in the detail drawer | 1. The Memo / Tag field is not visible |

**Test Data:** BTC-Bitcoin address (no Memo/Tag support)

---

#### TC-162005 · Members – Details – Crypto Address Details Deleted record opens with no action buttons
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify a Deleted crypto address detail drawer is read-only with no Disable or Enable buttons

**Prerequisites:**
- Admin is on the Withdrawal Accounts tab
- Member has at least one Deleted crypto address

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Click on a Deleted crypto address record in the list | 1. The detail drawer opens successfully<br>2. All fields are visible in read-only mode<br>3. No Disable or Enable buttons are present<br>4. Status field shows "Deleted" |

**Test Data:** —

---

### Crypto Address Disable (6 cases) · folder 128

#### TC-161993 · Members – Details – Crypto Address Disable option visible on Active record in list
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify the Disable action is available for Active crypto address records from the list

**Prerequisites:**
- Admin is on the Withdrawal Accounts tab
- Member has at least one Active crypto address

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Locate an Active crypto address in the list | — |
| 2 | 2. Open the action menu for that record | 1. A "Disable" action option is visible |

**Test Data:** —

---

#### TC-161994 · Members – Details – Crypto Address Disable button visible in Active record detail drawer
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify the Disable button is available inside the Crypto Address detail drawer for Active records

**Prerequisites:**
- Admin has opened the detail drawer of an Active crypto address

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Observe the action buttons available in the detail drawer | 1. A "Disable" button is visible and clickable |

**Test Data:** —

---

#### TC-161995 · Members – Details – Crypto Address Disable confirmation modal content correct
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify clicking Disable on a crypto address shows the confirmation modal with correct copy

**Prerequisites:**
- Admin has clicked Disable on an Active crypto address (Label: "My USDT Wallet")

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Click the Disable action on an Active crypto address | 1. A confirmation modal appears<br>2. Modal header: "Disable this crypto address?"<br>3. Modal body: "{Label} · will be immediately unavailable for withdrawal, and the member will not be able to add it again while it is disabled."<br>4. Two CTAs: "Cancel" and "Disable" |

**Test Data:** Label "My USDT Wallet"

---

#### TC-161996 · Members – Details – Crypto Address Disable cancel on modal keeps record Active
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify clicking Cancel on the Disable modal makes no changes

**Prerequisites:**
- Admin has clicked Disable on an Active crypto address and the confirmation modal is open

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Click "Cancel" on the modal | 1. The modal closes<br>2. The crypto address remains in Active status<br>3. No changes are made |

**Test Data:** —

---

#### TC-161997 · Members – Details – Crypto Address Disable confirm changes status to Disabled immediately
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify confirming Disable changes the crypto address status to Disabled immediately

**Prerequisites:**
- Admin has clicked Disable on an Active crypto address (Label: "My USDT Wallet") and the confirmation modal is open

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Click "Disable" on the confirmation modal | — |
| 2 | 2. Observe the result in the list | 1. The modal closes<br>2. Success message: "This crypto address has been disabled."<br>3. The crypto address status changes to "Disabled" immediately<br>4. The record moves to after the Active group in the sorted list<br>5. The Last Updated Date updates to the current timestamp |

**Test Data:** Label "My USDT Wallet"

---

#### TC-161998 · Members – Details – Crypto Address Disable not blocked by existing Pending withdrawal
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify Disable succeeds even when a Pending withdrawal exists to that crypto address

**Prerequisites:**
- Member has an Active crypto address with a linked Pending withdrawal request

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Click Disable on the Active crypto address that has a linked Pending withdrawal | — |
| 2 | 2. Confirm the Disable action in the modal | — |
| 3 | 3. Observe the crypto address status and Pending withdrawal status | 1. The Disable action succeeds<br>2. Success message: "This crypto address has been disabled."<br>3. The crypto address status changes to Disabled<br>4. The linked Pending withdrawal remains in Pending status — not auto-cancelled |

**Test Data:** —

---

### Crypto Address Enable (6 cases) · folder 128

#### TC-161999 · Members – Details – Crypto Address Enable option visible on Disabled record in list
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify the Enable action is available for Disabled crypto address records from the list

**Prerequisites:**
- Admin is on the Withdrawal Accounts tab
- Member has at least one Disabled crypto address

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Locate a Disabled crypto address in the list | — |
| 2 | 2. Open the action menu for that record | 1. An "Enable" action option is visible |

**Test Data:** —

---

#### TC-162000 · Members – Details – Crypto Address Enable button visible in Disabled record detail drawer
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify the Enable button is available inside the Crypto Address detail drawer for Disabled records

**Prerequisites:**
- Admin has opened the detail drawer of a Disabled crypto address

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Observe the action buttons in the detail drawer | 1. An "Enable" button is visible and clickable |

**Test Data:** —

---

#### TC-162001 · Members – Details – Crypto Address Enable confirmation modal content correct
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify clicking Enable on a Disabled crypto address shows the modal with correct copy

**Prerequisites:**
- Admin has clicked Enable on a Disabled crypto address (Label: "My USDT Wallet", masked address: 0x1234...5678)

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Click the Enable action on a Disabled crypto address | 1. A confirmation modal appears<br>2. Modal header: "Enable this crypto address?"<br>3. Modal body: "{Label} · {masked wallet address} will be available for withdrawal again immediately." (e.g. "My USDT Wallet · 0x1234...5678 will be available for withdrawal again immediately.")<br>4. Two CTAs: "Cancel" and "Enable" |

**Test Data:** Label "My USDT Wallet", masked address 0x1234...5678

---

#### TC-162002 · Members – Details – Crypto Address Enable cancel on modal keeps record Disabled
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify clicking Cancel on the Enable modal makes no changes

**Prerequisites:**
- Admin has clicked Enable on a Disabled crypto address and the confirmation modal is open

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Click "Cancel" on the modal | 1. The modal closes<br>2. The crypto address remains in Disabled status<br>3. No changes are made |

**Test Data:** —

---

#### TC-162003 · Members – Details – Crypto Address Enable confirm changes status to Active immediately
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify confirming Enable changes the crypto address status to Active immediately

**Prerequisites:**
- Admin has clicked Enable on a Disabled crypto address and the confirmation modal is open
- Member has fewer than 20 Active crypto addresses

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Click "Enable" on the confirmation modal | — |
| 2 | 2. Observe the result in the list | 1. The modal closes<br>2. Success message: "This crypto address has been enabled."<br>3. The crypto address status changes to "Active" immediately<br>4. The record moves back to the Active group in the sorted list |

**Test Data:** —

---

#### TC-162004 · Members – Details – Crypto Address Enable blocked when member already has 20 Active crypto addresses
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify Enable is blocked when member is at the maximum of 20 Active crypto addresses

**Prerequisites:**
- Member already has exactly 20 Active crypto addresses
- Member has at least 1 Disabled crypto address

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Click Enable on a Disabled crypto address | — |
| 2 | 2. Observe the result | 1. Enable is blocked<br>2. Error message: "This member already has 20 active crypto addresses. Disable another record before enabling this one."<br>3. The Disabled crypto address remains in Disabled status |

**Test Data:** Member with exactly 20 Active + ≥1 Disabled crypto addresses

---

### Audit log (2 cases) · folder 128

#### TC-162014 · Members – Details – Disable action logged in audit log with required fields
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify a Disable action is recorded in the audit log with the correct details

**Prerequisites:**
- Admin has just performed a Disable action on a bank account or crypto address
- Access to the audit log is available via backend/admin tooling

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Admin Disables a withdrawal account record | — |
| 2 | 2. Request BE support to check the audit log for the Disable event | 1. An audit log entry exists for the Disable action<br>2. The entry contains: admin identifier, timestamp, record ID, destination type (bank account / crypto address), and member ID<br>3. The entry is written at the time of the successful Disable (not on Cancel) |

**Test Data:** —

---

#### TC-162015 · Members – Details – Enable action logged in audit log with required fields
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify an Enable action is recorded in the audit log with the correct details

**Prerequisites:**
- Admin has just performed an Enable action on a bank account or crypto address

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Admin Enables a Disabled withdrawal account record | — |
| 2 | 2. Request BE support to check the audit log for the Enable event | 1. An audit log entry exists for the Enable action<br>2. The entry contains: admin identifier, timestamp, record ID, destination type, and member ID<br>3. No audit entry is created for a cancelled action (admin clicked Cancel on the modal) |

**Test Data:** —

---

### API failure (2 cases) · folder 128

#### TC-162016 · Members – Details – Disable action API failure shows error and no status change
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify an API failure on Disable shows an error message and leaves the record unchanged

**Prerequisites:**
- Admin has confirmed the Disable action in the modal
- The server returns an error response (simulated or actual failure)

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Admin confirms Disable in the modal | — |
| 2 | 2. API call returns an error | 1. Error message displayed: "Unable to complete this action. Please try again."<br>2. The record status remains Active (unchanged)<br>3. The modal closes |

**Test Data:** —

---

#### TC-162017 · Members – Details – Enable action API failure shows error and no status change
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify an API failure on Enable shows an error message and leaves the record unchanged

**Prerequisites:**
- Admin has confirmed the Enable action in the modal
- The server returns an error response

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Admin confirms Enable in the modal | — |
| 2 | 2. API call returns an error | 1. Error message displayed: "Unable to complete this action. Please try again."<br>2. The record status remains Disabled (unchanged) |

**Test Data:** —

---

### Concurrency (3 cases) · folder 128

#### TC-162018 · Members – Details – Concurrent Enable bank accounts at limit succeeds for first request only
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify when two admins simultaneously Enable different Disabled bank accounts and member is one below the limit, only the first succeeds

**Prerequisites:**
- Member has exactly 4 Active bank accounts (one below the limit of 5)
- Member has 2 Disabled bank accounts
- Admin A and Admin B both have the Enable confirmation modal open for different Disabled bank accounts at the same time

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Admin A and Admin B both click "Enable" at approximately the same time | — |
| 2 | 2. Observe the result for both admins | 1. One Enable action succeeds — that admin sees: "This bank account has been enabled." and the record becomes Active (member now has 5 Active bank accounts)<br>2. The second Enable action is rejected by the server<br>3. The second admin sees: "This member already has 5 active bank accounts. Disable another record before enabling this one."<br>4. The second Disabled record remains in Disabled status |

**Test Data:** Member with 4 Active + 2 Disabled bank accounts; two concurrent BO sessions

---

#### TC-162019 · Members – Details – Concurrent Enable crypto addresses at limit succeeds for first request only
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify when two admins simultaneously Enable Disabled crypto addresses and member is one below the limit, only the first succeeds

**Prerequisites:**
- Member has exactly 19 Active crypto addresses (one below limit of 20)
- Member has 2 Disabled crypto addresses
- Admin A and Admin B both have the Enable confirmation modal open for different Disabled crypto addresses at the same time

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Admin A and Admin B both click "Enable" at approximately the same time | — |
| 2 | 2. Observe the result for both admins | 1. One Enable action succeeds — record becomes Active (member now has 20 Active crypto addresses)<br>2. The second Enable action is rejected<br>3. The second admin sees: "This member already has 20 active crypto addresses. Disable another record before enabling this one."<br>4. The second Disabled record remains in Disabled status |

**Test Data:** Member with 19 Active + 2 Disabled crypto addresses; two concurrent BO sessions

---

#### TC-162020 · Members – Details – Concurrent Disable of same bank account processed once only
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify two admins simultaneously Disabling the same Active bank account results in one Disable only

**Prerequisites:**
- Member has an Active bank account
- Admin A and Admin B both have the Disable confirmation modal open for the same record at the same time

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Admin A and Admin B both click "Disable" on the same record at approximately the same time | — |
| 2 | 2. Observe the result for both admins and the audit log | 1. The record is Disabled once — the status is Disabled<br>2. One admin sees the success message: "This bank account has been disabled."<br>3. The second admin sees either the same success message (idempotent) or a generic error<br>4. No duplicate audit entries are created for the same event |

**Test Data:** Two concurrent BO sessions on the same record

---

### Balance Approvals (3 cases) · folder 374

#### TC-162011 · Balance Approvals – Logic – Checker cannot approve withdrawal to Disabled destination
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify checker receives a blocking error when approving a Pending withdrawal whose destination is Disabled

**Prerequisites:**
- A member has a Pending withdrawal request to a specific bank account or crypto address
- Admin has since Disabled that destination
- Checker is on the Pending withdrawal request details page in Back Office

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Checker clicks Approve on the Pending withdrawal request | — |
| 2 | 2. Observe the result | 1. The approval is blocked<br>2. A blocking error is displayed: "This withdrawal destination has been disabled and the request cannot be approved. Reject the request to return the funds to the member's available balance."<br>3. The only available action on the request is Reject |

**Test Data:** —

---

#### TC-162012 · Balance Approvals – Logic – Checker can Reject withdrawal to Disabled destination
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify checker can successfully Reject a Pending withdrawal whose destination has been Disabled

**Prerequisites:**
- A Pending withdrawal exists to a Disabled destination
- Checker is on the withdrawal request details page

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Checker clicks Reject on the Pending withdrawal request | — |
| 2 | 2. Checker confirms the rejection | 1. The rejection succeeds<br>2. The withdrawal request status changes from Pending to Rejected<br>3. The held amount is returned to the member's available balance |

**Test Data:** —

---

#### TC-162013 · Balance Approvals – Logic – Pending withdrawal not auto-rejected when destination Disabled
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify a Pending withdrawal is not automatically rejected when admin Disables its destination

**Prerequisites:**
- A Pending withdrawal request exists to an Active bank account or crypto address

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Admin Disables the destination bank account / crypto address used by the Pending withdrawal | — |
| 2 | 2. Observe the Pending withdrawal request status in Back Office | 1. The Disable action on the destination succeeds<br>2. The Pending withdrawal request remains in Pending status — it is NOT automatically rejected or cancelled<br>3. The checker must manually action the request |

**Test Data:** —

---

### App — Withdrawal Accounts (4 cases) · folder 3595

#### TC-151419 · Withdrawal Accounts – Linked bank accounts – BO disables account immediately reflected in app
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify a bank account disabled by Back Office is immediately reflected in the member's app without requiring restart

**Prerequisites:**
- Member has an Active bank account visible in the Linked Bank Accounts listing
- Back Office has just disabled the account

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Without restarting the app, navigate back to the Linked Bank Accounts listing (e.g. pull to refresh or re-open listing) | 1. The account now appears as Disabled in the listing<br>2. Account card shows Disabled status<br>3. Tapping the account shows read-only details with the disabled warning message<br>4. Account is no longer selectable for Fiat Withdrawal |

**Test Data:** —

---

#### TC-162007 · Withdrawal Accounts – Linked bank accounts – Add bank account blocked when matching record is Disabled
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify member gets an error when adding a bank account matching a Disabled record (same Account Number/IBAN + BIC/SWIFT)

Also linked to AO-923 (per AO-1087 comment).

**Prerequisites:**
- Admin has Disabled a bank account with a specific Account Number/IBAN and BIC/SWIFT
- Member is in the mobile app Add Bank Account flow

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Member fills in the Add Bank Account form using the same Account Number/IBAN and BIC/SWIFT as the Disabled record | — |
| 2 | 2. Member submits the form | 1. The system rejects the submission<br>2. An error message is shown to the member<br>3. No new bank account is created |

**Test Data:** —

⚠️ Expected result 2 names no exact error string. BR-8 says "Member-facing error copy exists in AO-923".
The oracle is unresolved — close it at exec design.

---

#### TC-162008 · Withdrawal Accounts – Crypto addresses – Add crypto address blocked when matching record is Disabled
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify member gets an error when adding a crypto address matching a Disabled record (same Asset + Network + Address)

Also linked to AO-922 (per AO-1087 comment).

**Prerequisites:**
- Admin has Disabled a crypto address with a specific Asset, Network, and Wallet Address
- Member is in the mobile app Add Crypto Address flow

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Member fills in the Add Crypto Address form using the same Asset, Network, and Wallet Address as the Disabled record | — |
| 2 | 2. Member submits the form | 1. The system rejects the submission<br>2. An error message is shown to the member<br>3. No new crypto address is created |

**Test Data:** —

⚠️ Expected result 2 names no exact error string. BR-8 says the copy lives in AO-922. Oracle unresolved.

---

#### TC-191125 · Withdrawal Accounts – Linked bank accounts – Add bank account succeeds after Deleted record with same Account Number/IBAN and BIC/SWIFT
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify member can successfully re-add a bank account using the same Account Number/IBAN and BIC/SWIFT after the original record has been deleted

Added 2026-08-25 in response to Suet Fun Ng's review request on AO-1087.

**Prerequisites:**
- Member has previously deleted a bank account (status = Deleted)
- The Account Number/IBAN and BIC/SWIFT of the deleted account are known

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Go to Account > Withdrawal accounts > Linked bank accounts | 1. Linked bank accounts listing is displayed<br>2. The previously deleted account is no longer visible (or shown as Deleted) |
| 2 | 2. Tap "+" or "Add bank account" | 1. Add bank account form is displayed |
| 3 | 3. Fill in all required fields using the same Account Number/IBAN and BIC/SWIFT as the deleted account | — |
| 4 | 4. Tap "Continue" and proceed through the Review screen | 1. No duplicate/blocked error is shown<br>2. Member is navigated to the Review Bank Account screen |
| 5 | 5. Tap "Save bank account" and complete OTP verification | 1. Bank account is created successfully with Active status<br>2. New account appears in the Linked bank accounts listing<br>3. No error indicating the account already exists |

**Test Data:** —

---

### App — Fiat Withdrawal (2 cases) · folder 3597

#### TC-151523 · Withdraw – Fiat – Bank Account – Disabled accounts shown with Disabled badge and not selectable
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify Disabled bank accounts appear in the Bank Account picker with a Disabled badge and cannot be selected

**Prerequisites:**
- Member has at least one Active and at least one Disabled bank account supporting the selected currency
- Member is on the Select bank account screen

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Observe the bank account list | 1. Disabled account is visible in the list, greyed out with a "Disabled" badge |
| 2 | 2. Attempt to tap the Disabled account | 1. Tapping the Disabled account does not select it<br>2. Member remains on the Select bank account screen |

**Test Data:** —

⚠️ TC-151523 says the Disabled account **is visible** in the picker; BR-6 says it "is excluded from the
withdrawal destination dropdown (AO-881 Req 2)". Contradiction — resolve at exec design.

---

#### TC-162006 · Withdrawal – Fiat – Bank Account – Re-enabled bank account selectable again
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify a re-enabled record becomes selectable again in the mobile withdrawal destination list

**Prerequisites:**
- Admin has previously Disabled and then re-Enabled a bank account for a member
- Member is on the withdrawal destination selection screen

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Observe the re-enabled bank account in the destination list | 1. The re-enabled bank account is no longer greyed-out<br>2. The record is clickable and selectable for withdrawal |

**Test Data:** —

---

### App — Crypto Withdrawal (1 case) · folder 3792

#### TC-162010 · Withdrawal – Crypto – CryptoAddressScreen – Disabled crypto address shown non-clickable
**Priority:** Unset | **Automation:** Unset | **State:** 4

**Description:** Verify a Disabled crypto address is shown as non-clickable in the mobile app withdrawal destination list

**Prerequisites:**
- Admin has Disabled a crypto address for a member
- Member is on the crypto withdrawal destination selection screen

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | 1. Observe the previously Active crypto address in the destination list | 1. The disabled crypto address is visible but rendered in a disabled/greyed-out state<br>2. Tapping it does not proceed to withdrawal confirmation<br>3. Other Active crypto addresses remain selectable |

**Test Data:** —

---

## Reconciliation

| Check | Value |
|---|---|
| `testmo_find_cases_by_issue` totalCases | 65 |
| Cases detailed above | 65 |
| Fetch failures | 0 |
| Group total | 3+2+4+3+4+6+7+3+4+6+6+2+2+3+3+4+2+1 = 65 |

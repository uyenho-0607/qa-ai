# Test Cases — AO-923

**Issue:** [AO-923](https://aquariux.atlassian.net/browse/AO-923)
**Fetched:** 2026-08-21
**Total:** 119 cases (115 fetched, 4 not found in project)

## Summary

| Priority | Count |
|---|---|
| High | — |
| Medium | — |
| Low | — |
| Unset | 119 |

## Case Groups

| Group | Cases |
|---|---|
| Account – Withdrawal Accounts | 1 |
| Linked bank accounts – Navigation | 1 |
| Linked bank accounts – Listing | 7 |
| Linked bank accounts – Filter | 4 |
| Add Bank Account – Form UI | 1 |
| Add Bank Account – Label | 3 |
| Add Bank Account – Bank Country | 5 |
| Add Bank Account – Bank Name | 5 |
| Add Bank Account – Supported Currencies | 6 |
| Add Bank Account – Account Type | 4 |
| Add Bank Account – Account Name | 4 |
| Add Bank Account – Account Number/IBAN | 3 |
| Add Bank Account – BIC/SWIFT | 6 |
| Add Bank Account – Duplicate validation | 3 |
| Add Bank Account – Bank Code/Routing Number | 3 |
| Add Bank Account – Address Line 1 | 3 |
| Add Bank Account – Address Line 2 | 3 |
| Add Bank Account – City | 3 |
| Add Bank Account – Postal Code | 3 |
| Add Bank Account – BIC mismatch | 4 |
| Add Bank Account – Review screen | 3 |
| Add Bank Account – Email OTP screen UI | 1 |
| Add Bank Account – OTP flow | 8 |
| Add Bank Account – Full flow E2E | 4 |
| View bank account | 2 |
| Edit bank account | 7 |
| Delete bank account | 4 |
| Error / edge cases | 3 |
| Navigation – Back buttons | 4 |
| App lifecycle – Background | 5 |
| App lifecycle – Kill app | 4 |
| Blocked – Disabled record | 1 |

---

## Full Case Details

### Account – Withdrawal Accounts (1 case)

#### TC-151311 · Account – Withdrawal Accounts – Withdrawal Accounts menu item visible
**Priority:** Unset | **State:** 17

**Description:** Verify Withdrawal Accounts item is visible on the Account screen

**Prerequisites:**
- Member is on the Account screen (Account tab)

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe the Account screen | "Withdrawal accounts" item is visible under the "Your account" section (below "Account details") |

---

### Linked bank accounts – Navigation (1 case)

#### TC-151312 · Withdrawal Accounts – Linked bank accounts – Linked bank accounts option navigates to listing
**Priority:** Unset | **State:** 17

**Description:** Verify tapping Withdrawal Accounts then Linked Bank Accounts navigates to the Linked Bank Accounts listing screen

**Prerequisites:**
- Member is on the Account screen (Account tab)
- "Withdrawal accounts" item is visible

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap on "Withdrawal accounts" | Member is navigated to the Withdrawal accounts screen; "Linked bank accounts" option is visible with description text: "Manage bank accounts for fiat withdrawals" |
| 2 | Tap on "Linked bank accounts" | Member is navigated to the Linked bank accounts listing screen |

---

### Linked bank accounts – Listing (7 cases)

#### TC-151313 · Listing – Empty state displayed when no accounts exist
**Priority:** Unset | **State:** 17

**Description:** Verify Linked Bank Accounts listing displays empty state when no accounts exist

**Prerequisites:**
- Member is on the Linked bank accounts screen
- Member has no linked bank accounts

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe the listing screen | Screen title reads: "Linked bank accounts"; Back button (←) visible top-left; Empty state displayed with: Bank/building icon centered, Heading: "No linked bank accounts", Subtext: "Add a bank account to withdraw fiat.", Orange CTA button: "Add bank account"; Search bar is NOT shown in empty state; No account cards displayed |

---

#### TC-151314 · Listing – Screen UI elements displayed
**Priority:** Unset | **State:** 17

**Description:** Verify Linked Bank Accounts listing screen displays all UI elements correctly

**Prerequisites:**
- Member is on the Linked bank accounts screen
- Member has at least one bank account

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe the listing screen | Screen title reads: "Linked bank accounts"; Back button (←) visible top-left; "+" button visible top-right; Search bar displayed with placeholder: "Search label or bank"; Account cards are displayed below the search bar |

---

#### TC-151315 · Listing – Account card shows label, bank name and masked number
**Priority:** Unset | **State:** 17

**Description:** Verify each account card displays the correct information

**Prerequisites:**
- Member is on the Linked bank accounts screen
- Member has at least one Active and one Disabled bank account

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe the account cards in the listing | Each card displays: Account Label (first line), Bank Name (second line), Masked account number: "•••• XXXX" (last 4 digits, third line); Disabled accounts show an orange "Disabled" badge to the right of the Label |

---

#### TC-151316 · Listing – Active accounts sorted before Disabled
**Priority:** Unset | **State:** 17

**Description:** Verify accounts are sorted with Active accounts before Disabled, most recently added first within each group

**Prerequisites:**
- Member is on the Linked bank accounts screen
- Member has at least 2 Active accounts and 1 Disabled account added at different times

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe the order of account cards in the listing | All Active accounts appear above all Disabled accounts; Within the Active group: accounts sorted by most recently added (newest first); Within the Disabled group: accounts sorted by most recently added (newest first) |

---

#### TC-151317 · Listing – Add button hidden and warning shown at 5-account limit
**Priority:** Unset | **State:** 17

**Description:** Verify Add Bank Account button is not accessible and a warning appears when member has reached 5 Active accounts

**Prerequisites:**
- Member is on the Linked bank accounts screen
- Member has exactly 5 Active bank accounts

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe the listing screen | "+" button is NOT visible (hidden); Inline warning banner displayed below search bar: "You've reached the maximum of 5 linked bank accounts. Delete one to add another."; All 5 Active accounts are listed |

---

#### TC-151318 · Listing – Non-verified member prompted for verification
**Priority:** Unset | **State:** 17

**Description:** Verify non-verified member is prompted to complete verification when tapping Add Bank Account

**Prerequisites:**
- Member is on the Linked Bank Accounts listing screen
- Member's verification status is NOT Approved

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap on "Add bank account" CTA | Verification bottom sheet is displayed (same as tapping the deposit module for a non-verified member); Member is NOT navigated to the Add Bank Account form |

---

#### TC-151323 · Listing – Disabled accounts excluded from 5-account limit
**Priority:** Unset | **State:** 17

**Description:** Verify Disabled accounts do not count toward the 5-account limit

**Prerequisites:**
- Member is on the Linked Bank Accounts listing screen
- Member has 4 Active accounts and 1 Disabled account

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe the "+" (Add bank account) button state | "+" button is enabled (tappable); No limit warning is displayed; Member can proceed to add another account |

---

### Linked bank accounts – Filter (4 cases)

#### TC-151319 · Filter – Search by label returns matching accounts
**Priority:** Unset | **State:** 17

**Description:** Verify member can search bank accounts by Label

**Prerequisites:**
- Member is on the Linked Bank Accounts listing screen
- Member has at least 2 bank accounts with different Labels

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap on the search bar | — |
| 2 | Type part of a known account Label | Results filter in real time as input is typed; Only accounts whose Label matches the search input are displayed; Search is case-insensitive (assumption); Accounts not matching the Label are hidden |

---

#### TC-151320 · Filter – Search by bank name returns matching accounts
**Priority:** Unset | **State:** 17

**Description:** Verify member can search bank accounts by Bank Name

**Prerequisites:**
- Member is on the Linked Bank Accounts listing screen
- Member has at least 2 accounts with different Bank Names

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap on the search bar | — |
| 2 | Type part of a known Bank Name | Results filter to show only accounts whose Bank Name matches the input; Accounts not matching the Bank Name are hidden |

---

#### TC-151321 · Filter – Search returns no results
**Priority:** Unset | **State:** 17

**Description:** Verify search with no matching results shows the correct no-results state

**Prerequisites:**
- Member is on the Linked bank accounts screen
- Member has at least one bank account

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap the search bar | — |
| 2 | Type a value that matches no Label or Bank Name (e.g. "UOB") | No account cards are displayed; Message displayed: "No bank accounts found" |

**Test Data:** UOB

---

#### TC-151322 · Filter – Clearing search restores full list
**Priority:** Unset | **State:** 17

**Description:** Verify clearing the search restores the full account list

**Prerequisites:**
- Member is on the Linked Bank Accounts listing screen
- A search term has been entered and results are filtered

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap the clear [x] on the search bar | Search input is cleared; Full account listing is restored (all Active and Disabled accounts shown) |

---

### Add Bank Account – Form UI (1 case)

#### TC-151324 · Add Bank Account – Form UI elements displayed
**Priority:** Unset | **State:** 17

**Description:** Verify Add Bank Account form displays all required sections and fields

**Prerequisites:**
- Member is on the Linked bank accounts screen
- Member has Approved verification status
- Member has fewer than 5 Active bank accounts

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap the "+" (Add bank account) button | — |
| 2 | Observe the Add Bank Account form | Screen title reads: "Add bank account"; Back button (←) visible top-left; Main sections: "Account", "Beneficiary", "Beneficiary address"; "Continue" CTA button visible at the bottom |
| 3 | Observe the Account section | "Account" section header visible with fields: Label, Bank country, Bank name, Supported currencies (helper text: "Select the currencies this account can receive."), Account type (optional) |
| 4 | Observe the Beneficiary section | "Beneficiary" section header visible with fields: Account name (helper text: "Enter the name exactly as it appears on your bank account."), Account number / IBAN, BIC / SWIFT, Bank code / Routing number (optional) |
| 5 | Observe the Beneficiary address section | "Beneficiary address" section header visible with fields: Address line 1, Address line 2 (optional), City, Postal code (optional) |

---

### Add Bank Account – Label (3 cases)

#### TC-151325 · Add Bank Account – Label field left empty
**Priority:** Unset | **State:** 17

**Description:** Verify inline error shown when Label field is left empty

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap on the Label field, then tap outside without entering any value | Inline error displayed below Label field: "Please enter a label."; "Continue" button remains disabled |

---

#### TC-151326 · Add Bank Account – Label exceeds 30 characters
**Priority:** Unset | **State:** 17

**Description:** Verify inline error shown when Label exceeds 30 characters

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter 31 or more characters into the Label field | Inline error displayed: "Label cannot exceed 30 characters."; "Continue" button remains disabled |

**Test Data:** 31-character string (e.g. "ABCDEFGHIJKLMNOPQRSTUVWXYZ12345")

---

#### TC-151327 · Add Bank Account – Label valid input accepted
**Priority:** Unset | **State:** 17

**Description:** Verify Label field accepts valid alphanumeric input up to 30 characters

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter a valid label of up to 30 characters into the Label field | Label is accepted; No error message displayed |

**Test Data:** My Savings Account 01

---

### Add Bank Account – Bank Country (5 cases)

#### TC-151328 · Add Bank Account – Bank Country modal UI displayed
**Priority:** Unset | **State:** 17

**Description:** Verify Select Bank Country modal displays all UI elements correctly

**Prerequisites:**
- Member is on the Add Bank Account form
- Bank Country dropdown is tapped (Select bank country modal is open)

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe the Select bank country modal | Modal title reads: "Select bank country"; Close button (✕) visible top-left; Search bar displayed with placeholder: "Search country"; Country list sorted alphabetically with section headers (A, B, C...); Each row shows: flag icon + country name; List is scrollable |

---

#### TC-151329 · Add Bank Account – Bank Country not selected
**Priority:** Unset | **State:** 17

**Description:** Verify inline error shown when Bank Country is not selected

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap on the Bank Country dropdown, then close it without selecting any option | Inline error displayed: "Please select a bank country."; "Continue" button remains disabled |

---

#### TC-151330 · Add Bank Account – Bank Country options list correct
**Priority:** Unset | **State:** 17

**Description:** Verify Bank Country dropdown displays the correct list from the platform's country source

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap the Bank Country dropdown | — |
| 2 | Observe the list of countries | Dropdown opens; Countries displayed match the platform's configured country list; Search function is available within the dropdown |

---

#### TC-151331 · Add Bank Account – Bank Country search filters results correctly
**Priority:** Unset | **State:** 17

**Description:** Verify search within Bank Country dropdown filters results correctly

**Prerequisites:**
- Member is on the Add Bank Account form
- Bank Country dropdown is open

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Type a partial country name in the dropdown search (e.g. "Sing") | Dropdown results filter to show only countries containing "Sing" (e.g. Singapore); Countries not matching the keyword are hidden |

**Test Data:** Sing SING SiNg

---

#### TC-151332 · Add Bank Account – Bank Country valid country selected
**Priority:** Unset | **State:** 17

**Description:** Verify Bank Country accepts a valid selection

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap the Bank Country dropdown | — |
| 2 | Select a valid country (e.g. Singapore) | Selected country is displayed in the Bank Country field |

**Test Data:** Singapore

---

### Add Bank Account – Bank Name (5 cases)

#### TC-151333 · Add Bank Account – Bank Name field left empty
**Priority:** Unset | **State:** 17

**Description:** Verify inline error shown when Bank Name field is left empty

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap on the Bank Name field, then tap outside without entering any value | Inline error displayed: "Please enter a bank name."; "Continue" button remains disabled |

---

#### TC-151334 · Add Bank Account – Bank Name exceeds 100 characters
**Priority:** Unset | **State:** 17

**Description:** Verify inline error shown when Bank Name exceeds 100 characters

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter 101 or more characters into the Bank Name field | Inline error displayed: "Bank name cannot exceed 100 characters."; "Continue" button remains disabled |

**Test Data:** 101-character string (e.g. 101 x "A")

---

#### TC-151335 · Add Bank Account – Bank Name allowed special characters accepted
**Priority:** Unset | **State:** 17

**Description:** Verify Bank Name accepts the allowed special characters: & ' . , - ( ) /

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter a bank name containing allowed special characters: & ' . , - ( ) / | Input is accepted and displayed correctly in the Bank Name field; No error message displayed |

**Test Data:** DBS Bank (S'pore) & Co., Ltd / Trust

---

#### TC-151336 · Add Bank Account – Bank Name unallowed special characters rejected
**Priority:** Unset | **State:** 17

**Description:** Verify Bank Name does not accept special characters outside the allowed set

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter a bank name containing unallowed special characters (e.g. @, #, $, %, ^, *, !, ~) | Inline error is displayed; "Continue" button remains disabled; Only allowed characters (alphanumeric and & ' . , - ( ) /) are accepted |

**Test Data:** DBS@Bank#2024

---

#### TC-151337 · Add Bank Account – Bank Name valid input accepted
**Priority:** Unset | **State:** 17

**Description:** Verify Bank Name accepts valid alphanumeric free-text input

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter a valid bank name up to 100 characters | Bank Name is accepted; No error message displayed |

**Test Data:** OCBC Bank

---

### Add Bank Account – Supported Currencies (6 cases)

#### TC-151338 · Add Bank Account – Supported Currencies modal UI displayed
**Priority:** Unset | **State:** 17

**Description:** Verify Select Currencies modal displays all UI elements correctly

**Prerequisites:**
- Member is on the Add Bank Account form
- Supported Currencies dropdown is tapped (Select currencies modal is open)

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe the Select currencies modal | Modal title reads: "Select currencies"; Close button (✕) visible top-left; Search bar displayed with placeholder: "Search currency"; Currency list shows each row with: flag icon + currency code + full currency name; Checkbox visible on the right of each row; "Done" CTA button visible at the bottom |

---

#### TC-151339 · Add Bank Account – Supported Currencies no currency selected
**Priority:** Unset | **State:** 17

**Description:** Verify inline error shown when no currency is selected

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap on the Supported Currencies dropdown, then close it without selecting any option | Inline error displayed: "Please select at least one currency."; "Continue" button remains disabled |

---

#### TC-151340 · Add Bank Account – Supported Currencies options list correct
**Priority:** Unset | **State:** 17

**Description:** Verify Supported Currencies multi-select displays the correct list of fiat currencies

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap the Supported Currencies field | — |
| 2 | Observe the list of options | Multi-select dropdown opens; Available currencies match the platform's configured supported fiat currencies list; Helper text visible: "Select the currencies this account can receive." |

---

#### TC-151341 · Add Bank Account – Supported Currencies single currency selected
**Priority:** Unset | **State:** 17

**Description:** Verify a single currency can be selected

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap the Supported Currencies field | — |
| 2 | Select one currency (e.g. SGD) | SGD is selected and displayed in the field; No error message displayed |

**Test Data:** SGD

---

#### TC-151342 · Add Bank Account – Supported Currencies search filters correctly
**Priority:** Unset | **State:** 17

**Description:** Verify search within the Select Currencies modal filters the list correctly

**Prerequisites:**
- Member is on the Add Bank Account form
- Select currencies modal is open

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Type a partial currency code or name in the search bar (e.g. "HK") | List filters to show only currencies matching "HK" (e.g. HKD — Hong Kong Dollar); Non-matching currencies are hidden |
| 2 | Clear the search input | Full currency list is restored |

**Test Data:** HK Hong Kong hkd

---

#### TC-151343 · Add Bank Account – Supported Currencies multiple currencies selected
**Priority:** Unset | **State:** 17

**Description:** Verify multiple currencies can be selected

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap the Supported Currencies field | — |
| 2 | Select more than one currency (e.g. SGD, HKD, USD) | All selected currencies are shown in the field; No error message displayed |

**Test Data:** SGD, HKD, USD

---

### Add Bank Account – Account Type (4 cases)

#### TC-151344 · Add Bank Account – Account Type bottom sheet UI displayed
**Priority:** Unset | **State:** 17

**Description:** Verify Select Account Type bottom sheet displays all UI elements correctly

**Prerequisites:**
- Member is on the Add Bank Account form
- Account Type (optional) dropdown is tapped

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe the Select account type bottom sheet | Bottom sheet title reads: "Select account type"; Close button (✕) visible top-left; Exactly 2 options displayed: Checking, Savings; No search bar displayed |

---

#### TC-151345 · Add Bank Account – Account Type Checking selected
**Priority:** Unset | **State:** 17

**Description:** Verify Account Type accepts Checking option

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap the Account Type dropdown | — |
| 2 | Select "Checking" | "Checking" is displayed in the Account Type field |

**Test Data:** Checking

---

#### TC-151346 · Add Bank Account – Account Type Savings selected
**Priority:** Unset | **State:** 17

**Description:** Verify Account Type accepts Savings option

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap the Account Type dropdown | — |
| 2 | Select "Savings" | "Savings" is displayed in the Account Type field |

**Test Data:** Savings

---

#### TC-151347 · Add Bank Account – Account Type optional field left empty
**Priority:** Unset | **State:** 17

**Description:** Verify Account Type is optional and can be left without selection

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Leave Account Type without any selection | — |
| 2 | Fill all other mandatory fields with valid values | — |
| 3 | Tap "Continue" | No error message displayed for Account Type; Form proceeds past validation |

**Test Data:** (no selection)

---

### Add Bank Account – Account Name (4 cases)

#### TC-151348 · Add Bank Account – Account Name field left empty
**Priority:** Unset | **State:** 17

**Description:** Verify inline error shown when Account Name field is left empty

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap on the Account Name field, then tap outside without entering any value | Inline error displayed: "Please enter the account name."; "Continue" button remains disabled |

---

#### TC-151349 · Add Bank Account – Account Name exceeds 30 characters
**Priority:** Unset | **State:** 17

**Description:** Verify inline error shown when Account Name exceeds 30 characters

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter 31 or more characters into the Account Name field | Inline error displayed: "Account name cannot exceed 30 characters."; "Continue" button remains disabled |

**Test Data:** 31-character string (e.g. "ABCDEFGHIJKLMNOPQRSTUVWXYZ12345")

---

#### TC-151350 · Add Bank Account – Account Name special characters rejected
**Priority:** Unset | **State:** 17

**Description:** Verify Account Name does not accept special characters (alphanumeric only)

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter special characters into the Account Name field (e.g. @, #, $, %, ^, *, !) | Inline error is displayed; "Continue" button remains disabled; Only alphanumeric characters are accepted |

**Test Data:** @John#Doe!

---

#### TC-151351 · Add Bank Account – Account Name valid input accepted
**Priority:** Unset | **State:** 17

**Description:** Verify Account Name accepts valid alphanumeric input up to 30 characters

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter a valid account name into the Account Name field | Account Name is accepted; Helper text visible: "Enter the name exactly as it appears on your bank account." |

**Test Data:** John Doe

---

### Add Bank Account – Account Number/IBAN (3 cases)

#### TC-151352 · Add Bank Account – Account Number/IBAN field left empty
**Priority:** Unset | **State:** 17

**Description:** Verify inline error shown when Account Number / IBAN field is left empty

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap on the Account Number / IBAN field, then tap outside without entering any value | Inline error displayed: "Please enter an account number."; "Continue" button remains disabled |

---

#### TC-151353 · Add Bank Account – Account Number/IBAN exceeds 34 characters
**Priority:** Unset | **State:** 17

**Description:** Verify inline error shown when Account Number / IBAN exceeds 34 characters

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter 35 or more characters into the Account Number / IBAN field | Inline error displayed: "Account number cannot exceed 34 characters."; "Continue" button remains disabled |

**Test Data:** 35-character string

---

#### TC-151354 · Add Bank Account – Account Number/IBAN valid input accepted
**Priority:** Unset | **State:** 17

**Description:** Verify Account Number / IBAN accepts valid alphanumeric input up to 34 characters

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter a valid account number into the Account Number / IBAN field | Account Number / IBAN is accepted; No error message displayed |

**Test Data:** GB82WEST12345698765432

---

### Add Bank Account – BIC/SWIFT (6 cases)

#### TC-151355 · Add Bank Account – BIC/SWIFT field left empty
**Priority:** Unset | **State:** 17

**Description:** Verify inline error shown when BIC / SWIFT field is left empty

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap on the BIC / SWIFT field, then tap outside without entering any value | Inline error displayed: "Please enter your bank's SWIFT/BIC code."; "Continue" button remains disabled |

---

#### TC-151356 · Add Bank Account – BIC/SWIFT exceeds 11 characters
**Priority:** Unset | **State:** 17

**Description:** Verify inline error shown when BIC / SWIFT exceeds 11 characters

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter 12 or more characters into the BIC / SWIFT field | Inline error displayed: "SWIFT/BIC code cannot exceed 11 characters."; "Continue" button remains disabled |

**Test Data:** DEUTDEFF123X (12 chars)

---

#### TC-151357 · Add Bank Account – BIC/SWIFT below 8-character minimum
**Priority:** Unset | **State:** 17

**Description:** Verify inline error shown when BIC / SWIFT is less than 8 characters

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter fewer than 8 characters into the BIC / SWIFT field | Inline error displayed (assumption: "SWIFT/BIC code must be 8 or 11 characters."); "Continue" button remains disabled |

**Test Data:** DEUT5 (5 chars)

---

#### TC-151358 · Add Bank Account – BIC/SWIFT invalid length 9 or 10 characters
**Priority:** Unset | **State:** 17

**Description:** Verify inline error shown when BIC / SWIFT is 9 or 10 characters

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter exactly 9 characters into the BIC / SWIFT field | Inline error displayed (assumption: "SWIFT/BIC code must be 8 or 11 characters."); "Continue" button remains disabled |

**Test Data:** DEUTDEFF1 (9 chars)

---

#### TC-151359 · Add Bank Account – BIC/SWIFT valid 8-character input
**Priority:** Unset | **State:** 17

**Description:** Verify BIC / SWIFT accepts valid 8-character input

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter a valid 8-character BIC / SWIFT code | BIC / SWIFT is accepted; No error message displayed |

**Test Data:** DEUTDEFF

---

#### TC-151360 · Add Bank Account – BIC/SWIFT valid 11-character input
**Priority:** Unset | **State:** 17

**Description:** Verify BIC / SWIFT accepts valid 11-character input

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter a valid 11-character BIC / SWIFT code | BIC / SWIFT is accepted; No error message displayed |

**Test Data:** DEUTDEFFE10

---

### Add Bank Account – Duplicate validation (3 cases)

#### TC-151361 · Add Bank Account – Account Number/IBAN duplicate rejected for same member
**Priority:** Unset | **State:** 17

**Description:** Verify validation error when Account Number/IBAN + BIC/SWIFT combination already exists for same member

**Prerequisites:**
- Member is on the Add Bank Account form
- Member already has an active bank account with Account Number "GB82WEST12345698765432" and BIC "DEUTDEFF"

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter the same Account Number / IBAN: "GB82WEST12345698765432" | — |
| 2 | Enter the same BIC / SWIFT: "DEUTDEFF" | — |
| 3 | Fill all other mandatory fields with valid values | — |
| 4 | Tap "Continue" | Validation error is displayed indicating the account already exists (assumption: error message such as "This bank account has already been added.") |

**Test Data:** Account Number: GB82WEST12345698765432 / BIC: DEUTDEFF

---

#### TC-151362 · Add Bank Account – Same Account Number different BIC allowed
**Priority:** Unset | **State:** 17

**Description:** Verify adding an account with the same Account Number / IBAN but a different BIC / SWIFT is allowed (not treated as duplicate)

**Prerequisites:**
- Member is on the Add Bank Account form
- Member already has an existing bank account with Account Number: GB82WEST12345698765432 and BIC: DEUTDEFF

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter the same Account Number / IBAN: "GB82WEST12345698765432" | — |
| 2 | Enter a different BIC / SWIFT: "HSBCHKHHHKH" | — |
| 3 | Fill all other mandatory fields with valid values | — |
| 4 | Tap "Continue" | No duplicate validation error displayed; Member proceeds to the Review Bank Account screen |

**Test Data:** Account Number: GB82WEST12345698765432 / BIC: HSBCHKHHHKH (different)

---

#### TC-151363 · Add Bank Account – Different Account Number same BIC allowed
**Priority:** Unset | **State:** 17

**Description:** Verify adding an account with a different Account Number / IBAN but the same BIC / SWIFT is allowed (not treated as duplicate)

**Prerequisites:**
- Member is on the Add Bank Account form
- Member already has an existing bank account with Account Number: GB82WEST12345698765432 and BIC: DEUTDEFF

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter a different Account Number / IBAN: "DE89370400440532013000" | — |
| 2 | Enter the same BIC / SWIFT: "DEUTDEFF" | — |
| 3 | Fill all other mandatory fields with valid values | — |
| 4 | Tap "Continue" | No duplicate validation error displayed; Member proceeds to the Review Bank Account screen |

**Test Data:** Account Number: DE89370400440532013000 (different) / BIC: DEUTDEFF (same)

---

### Add Bank Account – Bank Code/Routing Number (3 cases)

#### TC-151364 · Add Bank Account – Bank Code/Routing Number exceeds 100 characters
**Priority:** Unset | **State:** 17

**Description:** Verify inline error shown when Bank Code / Routing Number exceeds 100 characters

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter 101 or more characters into the Bank Code / Routing Number field | Inline error displayed: "Bank code cannot exceed 100 characters."; "Continue" button remains disabled |

**Test Data:** 101-character string

---

#### TC-151365 · Add Bank Account – Bank Code/Routing Number accepts all free-text types
**Priority:** Unset | **State:** 17

**Description:** Verify Bank Code / Routing Number accepts numeric, alphabetic, and special character input (free-text field)

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter each test data value into the Bank Code / Routing Number field and observe the result | All test data variants are accepted and displayed correctly in the field; No error message displayed for any variant; (Assumption: field is free-text — accepts all character types) |

**Test Data:** 026009593 (numeric) / 20-47-12 (sort code with hyphens) / ABCDEF (alphabet only) / 062-ABC-000 (mixed alphanumeric with hyphens)

---

#### TC-151366 · Add Bank Account – Bank Code/Routing Number optional field left empty
**Priority:** Unset | **State:** 17

**Description:** Verify Bank Code / Routing Number is optional and can be left empty

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Leave Bank Code / Routing Number empty | — |
| 2 | Fill all other mandatory fields with valid values | — |
| 3 | Tap "Continue" | No error displayed for Bank Code / Routing Number; Form proceeds past validation |

**Test Data:** (empty)

---

### Add Bank Account – Address Line 1 (3 cases)

#### TC-151367 · Add Bank Account – Address Line 1 field left empty
**Priority:** Unset | **State:** 17

**Description:** Verify inline error shown when Address Line 1 field is left empty

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap on the Address Line 1 field, then tap outside without entering any value | Inline error displayed: "Please enter your address."; "Continue" button remains disabled |

---

#### TC-151368 · Add Bank Account – Address Line 1 exceeds 100 characters
**Priority:** Unset | **State:** 17

**Description:** Verify inline error shown when Address Line 1 exceeds 100 characters

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter 101 or more characters into the Address Line 1 field | Inline error displayed: "Address Line 1 cannot exceed 100 characters."; "Continue" button remains disabled |

**Test Data:** 101-character string

---

#### TC-151369 · Add Bank Account – Address Line 1 valid input accepted
**Priority:** Unset | **State:** 17

**Description:** Verify Address Line 1 accepts valid free-text input

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter a valid street address into Address Line 1 | Address Line 1 is accepted; No error message displayed |

**Test Data:** 123 Orchard Road

---

### Add Bank Account – Address Line 2 (3 cases)

#### TC-151370 · Add Bank Account – Address Line 2 optional field left empty
**Priority:** Unset | **State:** 17

**Description:** Verify Address Line 2 is optional and can be left empty

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Leave Address Line 2 empty | — |
| 2 | Fill all other mandatory fields with valid values | — |
| 3 | Tap "Continue" | No error displayed for Address Line 2; Form proceeds past validation |

**Test Data:** (empty)

---

#### TC-151371 · Add Bank Account – Address Line 2 exceeds 100 characters
**Priority:** Unset | **State:** 17

**Description:** Verify inline error shown when Address Line 2 exceeds 100 characters

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter 101 or more characters into the Address Line 2 field | Inline error displayed: "Address Line 2 cannot exceed 100 characters."; "Continue" button remains disabled |

**Test Data:** 101-character string

---

#### TC-151372 · Add Bank Account – Address Line 2 valid input accepted
**Priority:** Unset | **State:** 17

**Description:** Verify Address Line 2 accepts valid free-text input

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter a valid value into Address Line 2 | Address Line 2 is accepted; No error message displayed |

**Test Data:** #10-01 Orchard Tower

---

### Add Bank Account – City (3 cases)

#### TC-151373 · Add Bank Account – City field left empty
**Priority:** Unset | **State:** 17

**Description:** Verify inline error shown when City field is left empty

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap on the City field, then tap outside without entering any value | Inline error displayed: "Please enter your city."; "Continue" button remains disabled |

---

#### TC-151374 · Add Bank Account – City exceeds 100 characters
**Priority:** Unset | **State:** 17

**Description:** Verify inline error shown when City exceeds 100 characters

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter 101 or more characters into the City field | Inline error displayed: "City cannot exceed 100 characters."; "Continue" button remains disabled |

**Test Data:** 101-character string

---

#### TC-151375 · Add Bank Account – City valid input accepted
**Priority:** Unset | **State:** 17

**Description:** Verify City accepts valid free-text input

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter a valid city name into the City field | City is accepted; No error message displayed |

**Test Data:** Singapore

---

### Add Bank Account – Postal Code (3 cases)

#### TC-151376 · Add Bank Account – Postal Code optional field left empty
**Priority:** Unset | **State:** 17

**Description:** Verify Postal Code is optional and can be left empty

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Leave Postal Code empty | — |
| 2 | Fill all other mandatory fields with valid values | — |
| 3 | Tap "Continue" | No error displayed for Postal Code; Form proceeds past validation |

**Test Data:** (empty)

---

#### TC-151377 · Add Bank Account – Postal Code exceeds 100 characters
**Priority:** Unset | **State:** 17

**Description:** Verify inline error shown when Postal Code exceeds 100 characters

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter 101 or more characters into the Postal Code field | Inline error displayed: "Postal Code cannot exceed 100 characters."; "Continue" button remains disabled |

**Test Data:** 101-character string

---

#### TC-151378 · Add Bank Account – Postal Code valid input accepted
**Priority:** Unset | **State:** 17

**Description:** Verify Postal Code accepts valid free-text input

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter a valid postal code into the Postal Code field | Postal Code is accepted; No error message displayed |

**Test Data:** 238859

---

### Add Bank Account – BIC mismatch (4 cases)

#### TC-151379 · Add Bank Account – All fields valid and BIC country matches proceeds to Review
**Priority:** Unset | **State:** — | ⚠️ NOT FOUND in project

> Case 151379 was listed in the issue link but could not be fetched from project 8.

---

#### TC-151380 · Add Bank Account – BIC country mismatch warning shown
**Priority:** Unset | **State:** — | ⚠️ NOT FOUND in project

> Case 151380 was listed in the issue link but could not be fetched from project 8.

---

#### TC-151381 · Add Bank Account – BIC mismatch Review Details returns to form
**Priority:** Unset | **State:** 17

**Description:** Verify tapping Review Details on the BIC mismatch warning returns member to the Add Bank Account form

**Prerequisites:**
- Member is on the BIC country mismatch warning dialog

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap "Review Details" | Warning dialog is dismissed; Member is returned to the Add Bank Account form; Previously entered values are retained in all fields |

---

#### TC-151382 · Add Bank Account – BIC mismatch Continue anyway proceeds to Review
**Priority:** Unset | **State:** 17

**Description:** Verify tapping Continue anyway on the BIC mismatch warning navigates to the Review Bank Account screen

**Prerequisites:**
- Member is on the BIC country mismatch warning dialog

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap "Continue anyway" | Warning dialog is dismissed; Member is navigated to the Review Bank Account screen; All entered values are displayed on the Review screen |

---

### Add Bank Account – Review screen (3 cases)

#### TC-151383 · Add Bank Account – Review screen UI all fields displayed
**Priority:** Unset | **State:** 17

**Description:** Verify Review Bank Account screen displays all entered values in read-only format

**Prerequisites:**
- Member has completed the Add Bank Account form with all fields filled
- Member is on the Review Bank Account screen

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe the Review Bank Account screen | All values entered in the form are displayed correctly in read-only mode; All sections visible: Account, Beneficiary, Beneficiary Address; "Save bank account" CTA is visible; Back button is available |

---

#### TC-151384 · Add Bank Account – Review screen Back button retains form data
**Priority:** Unset | **State:** 17

**Description:** Verify tapping Back on the Review screen returns to the form with all values retained

**Prerequisites:**
- Member is on the Review Bank Account screen

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap the Back button on the Review Bank Account screen | Member is returned to the Add Bank Account form; All previously entered values are retained in their respective fields; No data is lost or reset |

---

#### TC-151385 · Add Bank Account – Review screen Save bank account triggers OTP
**Priority:** Unset | **State:** 17

**Description:** Verify tapping Save bank account initiates the Email OTP verification flow

**Prerequisites:**
- Member is on the Review Bank Account screen

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap "Save bank account" | Member is navigated to the Email OTP verification screen; OTP input prompt is displayed |

---

### Add Bank Account – Email OTP screen UI (1 case)

#### TC-151386 · Add Bank Account – Email OTP screen UI elements displayed
**Priority:** Unset | **State:** 17

**Description:** Verify Email OTP screen displays correctly after tapping Save bank account

**Prerequisites:**
- Member has tapped "Save bank account" on the Review Bank Account screen

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe the Email OTP screen | Screen title reads: "Verify your email"; Back button (←) visible top-left; Subtitle: "Enter the 6-digit verification code sent to [masked email]"; 6 individual OTP input boxes displayed; Resend text: "Didn't receive the code? Resend in 00:59" with orange countdown timer; Numeric keypad displayed (not standard keyboard) |

---

### Add Bank Account – OTP flow (8 cases)

#### TC-151387 · Add Bank Account – OTP email received on initial trigger
**Priority:** Unset | **State:** 17

**Description:** Verify member receives the OTP email in their inbox when the OTP flow is first triggered

**Prerequisites:**
- Member has tapped "Save bank account" on the Review Bank Account screen
- Member is now on the Email OTP screen

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Check the member's registered email inbox | OTP email is received in the member's registered email inbox; Email contains the 6-digit verification code |

---

#### TC-151388 · Add Bank Account – Incorrect OTP shows error and clears boxes
**Priority:** Unset | **State:** 17

**Description:** Verify error is shown when an incorrect OTP is entered

**Prerequisites:**
- Member is on the Email OTP screen
- A valid OTP has been sent to the member's registered email

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter an incorrect 6-digit OTP using the numeric keypad | OTP is auto-submitted after the 6th digit is entered; Inline error displayed: "Your verification code is incorrect, please try again."; All 6 OTP input boxes are cleared; Member remains on the OTP screen |

**Test Data:** 000000 (incorrect OTP)

---

#### TC-151389 · Add Bank Account – Expired OTP shows error
**Priority:** Unset | **State:** 17

**Description:** Verify error is shown when an expired OTP is submitted

**Prerequisites:**
- Member is on the Email OTP screen
- The OTP has expired

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Wait for the OTP to expire | — |
| 2 | Enter the expired OTP and submit | Error displayed: "Your verification code has expired, please request a new code."; Member remains on the OTP screen; All 6 OTP input boxes are cleared |

**Test Data:** Expired OTP

---

#### TC-151390 · Add Bank Account – Max incorrect OTP attempts reached blocks flow
**Priority:** Unset | **State:** 17

**Description:** Verify member is blocked from the OTP flow after reaching the maximum number of incorrect OTP attempts (10 times)

**Prerequisites:**
- Member is on the Email OTP screen
- A valid OTP has been sent to the member's registered email

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter an incorrect 6-digit OTP 9 times consecutively | Each incorrect attempt shows inline error and clears OTP boxes |
| 2 | Enter an incorrect OTP for the 10th time | Member is blocked from further OTP attempts; Error message: "You have reached the maximum number of incorrect verification code attempts. Please request a new code." |

**Test Data:** Incorrect OTP entered 9 times (e.g. 000000 each time)

---

#### TC-151391 · Add Bank Account – Resend OTP available after countdown
**Priority:** Unset | **State:** 17

**Description:** Verify member can resend the OTP after the countdown timer expires

**Prerequisites:**
- Member is on the Email OTP screen
- Countdown timer has reached 00:00 (Resend link is now active)

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe the Resend link state when countdown is active (e.g. 00:59) | "Resend" link is greyed out / not tappable while countdown timer is running |
| 2 | Wait for countdown to reach 00:00, then tap "Resend" | New OTP is sent to the member's registered email; Countdown timer resets and starts again; OTP input boxes are cleared |

---

#### TC-151392 · Add Bank Account – New OTP email received after Resend
**Priority:** Unset | **State:** 17

**Description:** Verify member receives a new OTP email in their inbox after tapping Resend

**Prerequisites:**
- Member is on the Email OTP screen
- Countdown timer has reached 00:00
- Resend link is now active

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap "Resend" | — |
| 2 | Check the member's registered email inbox | A new OTP email is received in the member's registered email inbox; New email contains a new 6-digit verification code |

---

#### TC-151393 · Add Bank Account – Previous OTP rejected after Resend
**Priority:** Unset | **State:** 17

**Description:** Verify the previous OTP code is no longer valid after member taps Resend

**Prerequisites:**
- Member is on the Email OTP screen
- Member has received the initial OTP (noted the code)
- Member has tapped Resend and a new OTP has been sent

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter the previous (old) OTP code using the numeric keypad | OTP is rejected; Inline error displayed: "Your verification code is incorrect, please try again."; OTP input boxes are cleared; Bank account is NOT created |

**Test Data:** Old OTP code (from before Resend was tapped)

---

#### TC-151394 · Add Bank Account – Correct OTP creates bank account with Active status
**Priority:** Unset | **State:** 17

**Description:** Verify bank account is created with Active status after correct OTP is entered

**Prerequisites:**
- Member is on the Email OTP screen
- A valid OTP has been sent to the member's registered email

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter the correct 6-digit OTP using the numeric keypad | OTP is auto-submitted after the 6th digit is entered; Member is navigated back to the Linked bank accounts listing screen; Success toast displayed at the top: "Bank account added" |
| 2 | Observe the current Linked bank accounts listing | Newly added account appears in the listing with status Active; Account is listed at the top of the Active accounts group (most recently added) |

**Test Data:** Correct OTP

---

### Add Bank Account – Full flow E2E (4 cases)

#### TC-151395 · Add Bank Account – Confirmation email sent after successful addition
**Priority:** Unset | **State:** 17

**Description:** Verify a confirmation email is sent to the member's registered email address after successful bank account addition

**Prerequisites:**
- Member has successfully completed OTP verification
- Bank account has been created with Active status

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Check the member's registered email inbox | A confirmation email is received; Email subject and content confirm the bank account was successfully added |

---

#### TC-151396 · Add Bank Account – Full add flow succeeds with single currency via My Account
**Priority:** Unset | **State:** 17

**Description:** Verify full Add Bank Account flow succeeds via My Account path with single currency and no optional fields

**Prerequisites:**
- Member is on the My Account screen
- Member has Approved verification status
- Member has fewer than 5 Active bank accounts

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap "Withdrawal Accounts" from the Account screen | — |
| 2 | Tap "Linked Bank Accounts" | — |
| 3 | Tap "+" (Add bank account) | — |
| 4 | Fill in all mandatory fields (Label, Bank Country, Bank Name, one currency, Account Name, Account Number/IBAN, BIC/SWIFT, Address Line 1, City). Leave all optional fields empty. | — |
| 5 | Tap "Continue" | — |
| 6 | Verify all entered values on Review screen, then tap "Save bank account" | — |
| 7 | Enter the correct OTP received at registered email | OTP verified successfully; New account appears in Linked Bank Accounts listing with status Active; Account is immediately available for Fiat Withdrawal; Confirmation email received at registered email address |

**Test Data:** Label: My SGD Account / Bank Country: Singapore / Bank Name: DBS Bank / Currency: SGD / Account Name: John Doe / Account Number: 0123456789 / BIC: DBSSSGSG / Address Line 1: 12 Marina Blvd / City: Singapore

---

#### TC-151397 · Add Bank Account – Full add flow succeeds with multiple currencies and optional fields via Fiat Withdrawal
**Priority:** Unset | **State:** 17

**Description:** Verify full Add Bank Account flow succeeds via Fiat Withdrawal path with multiple currencies and all optional fields filled

**Prerequisites:**
- Member is on the Withdrawal screen
- Member has Approved verification status
- Member has fewer than 5 Active bank accounts

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Navigate to Withdrawal > Fiat > Bank Account | — |
| 2 | Tap "Add bank account" | — |
| 3 | Fill in all fields including optional ones | — |
| 4 | Tap "Continue" and verify Review screen, then tap "Save bank account" | — |
| 5 | Enter the correct OTP | Bank account created with status Active; Account appears in listing showing HKD and USD currencies; Confirmation email received |

**Test Data:** Label: My HKD USD Account / Bank Country: Hong Kong / Bank Name: HSBC Hong Kong / Currencies: HKD, USD / Account Type: Savings / Account Name: Jane Smith / Account Number: HK12HSBC345678901234 / BIC: HSBCHKHHHKH / Bank Code: 004 / Addr1: 1 Queen's Road Central / City: Hong Kong / Postal Code: 999077

---

#### TC-151398 · Add Bank Account – Full add flow succeeds after choosing Continue anyway on BIC mismatch warning
**Priority:** Unset | **State:** 17

**Description:** Verify full flow succeeds when member chooses Continue anyway on BIC country mismatch warning

**Prerequisites:**
- Member is on the Add Bank Account form
- All mandatory fields filled with valid values
- BIC/SWIFT country code does NOT match selected Bank Country

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Fill in Bank Country = Singapore, BIC = DEUTDEFF (country mismatch) | — |
| 2 | Fill all other mandatory fields with valid values | — |
| 3 | Tap "Continue" | — |
| 4 | On the BIC mismatch warning dialog, tap "Continue anyway" | — |
| 5 | Verify all values on Review screen, then tap "Save bank account" | — |
| 6 | Enter the correct OTP | Bank account created with Active status despite BIC/country mismatch; Account appears in listing |

**Test Data:** Bank Country: Singapore / BIC: DEUTDEFF

---

#### TC-151399 · Add Bank Account – Full add flow succeeds when adding the 5th account at limit boundary
**Priority:** Unset | **State:** 17

**Description:** Verify a member with 4 Active accounts can still add one more (5th) account successfully

**Prerequisites:**
- Member is on the Linked Bank Accounts listing screen
- Member currently has exactly 4 Active bank accounts

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap "+" (Add bank account) | — |
| 2 | Complete the Add Bank Account form with valid data | — |
| 3 | Complete OTP verification | — |
| 4 | Observe the listing screen after success | New account created with Active status; Listing now shows 5 Active accounts; "+" button is now disabled with message: "You've reached the maximum of 5 linked bank accounts. Delete one to add another." |

**Test Data:** All valid data for a new account

---

### View bank account (2 cases)

#### TC-151400 · View Active bank account opens Edit Bank Account screen
**Priority:** Unset | **State:** — | ⚠️ NOT FOUND in project

> Case 151400 was listed in the issue link but could not be fetched from project 8.

---

#### TC-151401 · View Disabled bank account opens read-only details with warning
**Priority:** Unset | **State:** 17

**Description:** Verify tapping a Disabled bank account opens the read-only Bank Account Details screen with disabled warning

**Prerequisites:**
- Member is on the Linked bank accounts screen
- Member has at least one Disabled bank account

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap on a Disabled bank account card | Screen title reads: "Bank account details"; Orange warning banner: "This bank account has been disabled by an administrator. It can't be used for withdrawals."; All fields displayed as read-only; Account number / IBAN is masked (•••• XXXX); "Contact support" CTA button visible at the bottom |

---

### Edit bank account (7 cases)

#### TC-151402 · Edit – Label updated with valid new value
**Priority:** Unset | **State:** 17

**Description:** Verify member can update the Label field with a new valid value

**Prerequisites:**
- Member is on the Edit Bank Account screen for an Active bank account
- Current label is "My SGD Account"

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Clear the existing label and enter a new valid label | New label is accepted and displayed in the Label field; No error message displayed |

**Test Data:** New label: "Primary SGD Account"

---

#### TC-151403 · Edit – Label cleared shows empty field error
**Priority:** Unset | **State:** 17

**Description:** Verify validation error when label is cleared and saved empty

**Prerequisites:**
- Member is on the Edit Bank Account screen for an Active bank account

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Clear the existing label to make it empty | Inline error displayed: "Please enter a label."; "Save changes" button remains disabled |

**Test Data:** (empty)

---

#### TC-151404 · Edit – Label exceeds 30 characters rejected
**Priority:** Unset | **State:** 17

**Description:** Verify validation error when edited label exceeds 30 characters

**Prerequisites:**
- Member is on the Edit Bank Account screen for an Active bank account

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter a label of 31 or more characters into the Label field | Inline error displayed: "Label cannot exceed 30 characters."; "Save changes" button remains disabled |

**Test Data:** 31-character string

---

#### TC-151405 · Edit – New currency selectable in Supported Currencies
**Priority:** Unset | **State:** 17

**Description:** Verify member can select a new currency in the Supported currencies dropdown

**Prerequisites:**
- Member is on the Edit Bank Account screen for an Active bank account
- Account currently supports SGD only

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap the Supported currencies dropdown and select a new currency (e.g. USD) | USD is selected and displayed in the Supported currencies field; No error message displayed |

**Test Data:** New currency: USD

---

#### TC-151406 · Edit – Existing currency deselectable from Supported Currencies
**Priority:** Unset | **State:** 17

**Description:** Verify member can deselect an existing currency in the Supported currencies dropdown

**Prerequisites:**
- Member is on the Edit Bank Account screen for an Active bank account
- Account supports SGD and USD
- No pending withdrawals exist for this account

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap the Supported currencies dropdown and deselect USD | USD is deselected and removed from the Supported currencies field; No error message displayed |

**Test Data:** Currency to remove: USD

---

#### TC-151407 · Edit – Last remaining currency cannot be removed
**Priority:** Unset | **State:** 17

**Description:** Verify member cannot remove the last remaining currency from an account

**Prerequisites:**
- Member is on the Edit Bank Account screen for an Active bank account
- Account supports only one currency (e.g. SGD)

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Attempt to deselect SGD (the only currency on the account) | Removal is blocked; Error message displayed (assumption: "At least one currency must remain on the account."); SGD remains on the account |

---

#### TC-151408 · Edit – Save changes reflects updated label and currencies
**Priority:** Unset | **State:** 17

**Description:** Verify changes to Label and Supported currencies are saved and reflected after tapping Save changes

**Prerequisites:**
- Member is on the Edit Bank Account screen for an Active bank account
- Current label is "My SGD Account"
- Account currently supports SGD only

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Update the Label field to a new value | — |
| 2 | Update the Supported currencies | — |
| 3 | Tap "Save changes" | Member is navigated back to the Linked bank accounts listing screen; Success toast displayed: "Bank account updated" |
| 4 | Observe the account card in the listing | Account card shows the updated label |
| 5 | Tap on the updated account card to open it | Edit Bank Account screen opens; Supported currencies field shows updated currencies |

**Test Data:** New label: "Primary SGD Account" / Select new currency / Deselect existing currency

---

### Delete bank account (4 cases)

#### TC-151409 · Delete – Confirmation dialog shown
**Priority:** Unset | **State:** 17

**Description:** Verify Delete Bank Account confirmation dialog is displayed when tapping Delete bank account

**Prerequisites:**
- Member is on the Edit Bank Account screen for an Active bank account
- No pending withdrawals exist for this account

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap "Delete bank account" | Confirmation dialog is displayed; Dialog header: "Delete bank account?"; Message: "Removing this bank account will prevent it from being used for future withdrawals. This action won't affect completed transactions."; Two CTAs visible: "Delete" and "Cancel" |

---

#### TC-151410 · Delete – Cancel keeps account unchanged
**Priority:** Unset | **State:** — | ⚠️ NOT FOUND in project

> Case 151410 was listed in the issue link but could not be fetched from project 8.

---

#### TC-151411 · Delete – Confirmed account removed from listing
**Priority:** Unset | **State:** 17

**Description:** Verify bank account is removed after deletion is confirmed

**Prerequisites:**
- Member is on the Delete Bank Account confirmation dialog
- No pending withdrawals exist for this account

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap "Delete" | Member is navigated back to the Linked bank accounts listing screen; Success toast displayed: "Bank account deleted"; Deleted account is no longer visible in the listing |

---

#### TC-151412 · Delete – Blocked when pending withdrawal exists
**Priority:** Unset | **State:** 17

**Description:** Verify a bottom sheet is shown blocking deletion when a pending withdrawal exists

**Prerequisites:**
- Member is on the Edit Bank Account screen for an Active bank account
- A pending Fiat Withdrawal exists for this bank account

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap "Delete bank account" | Bottom sheet displayed with title: "Unable to delete bank account"; Message: "This bank account can't be deleted because it has pending withdrawals. Try again after all pending withdrawals are completed or cancelled."; CTA: "Close" button; Account is NOT deleted |

---

#### TC-151413 · Delete – Close blocked dialog returns to Edit screen
**Priority:** Unset | **State:** 17

**Description:** Verify tapping Close on the Unable to Delete bottom sheet dismisses it and returns to the Edit Bank Account screen

**Prerequisites:**
- Member is on the "Unable to delete bank account" bottom sheet
- Deletion was blocked due to pending withdrawal

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap "Close" | Bottom sheet is dismissed; Member returns to the Edit Bank Account screen; Account is NOT deleted; Account data remains unchanged |

---

### Error / edge cases (3 cases)

#### TC-151417 · Add Bank Account – Network interruption during OTP submission
**Priority:** Unset | **State:** 17

**Description:** Verify app behavior when network is interrupted at the moment OTP is submitted

**Prerequisites:**
- Member is on the Email OTP screen
- Network connection is active

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter the correct OTP | — |
| 2 | Disable network connection immediately before or during submission | App displays an appropriate error or timeout message; Bank account is NOT created; Member remains on or is returned to the OTP screen; Member can retry once connection is restored |

**Test Data:** Correct OTP + network off

---

#### TC-151418 · Add Bank Account – Session timeout during form fill
**Priority:** Unset | **State:** 17

**Description:** Verify app behavior when member's session expires while filling in the Add Bank Account form

**Prerequisites:**
- Member has started filling in the Add Bank Account form
- Member's session token expires (due to inactivity or token TTL)

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Leave the app idle until the session expires | — |
| 2 | Attempt to tap "Continue" to submit the form | Member is prompted to re-authenticate (redirected to login screen or session-expired prompt); Bank account is NOT created |

**Test Data:** All mandatory fields filled

---

#### TC-151419 · BO disables account immediately reflected in app
**Priority:** Unset | **State:** 17

**Description:** Verify a bank account disabled by Back Office is immediately reflected in the member's app without requiring restart

**Prerequisites:**
- Member has an Active bank account visible in the Linked Bank Accounts listing
- Back Office has just disabled the account

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Without restarting the app, navigate back to the Linked Bank Accounts listing (e.g. pull to refresh or re-open listing) | The account now appears as Disabled in the listing; Account card shows Disabled status; Tapping the account shows read-only details with the disabled warning message; Account is no longer selectable for Fiat Withdrawal |

---

### Navigation – Back buttons (4 cases)

#### TC-151420 · Add Bank Account – Back button returns to Withdrawal Accounts screen
**Priority:** Unset | **State:** 17

**Description:** Verify tapping Back on the Add Bank Account form navigates back to the Withdrawal Accounts screen

**Prerequisites:**
- Member is on the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap the Back button (←) | Member is navigated back to the Withdrawal Accounts screen; Bank account is NOT created; No error is triggered |

---

#### TC-151421 · Add Bank Account – Review screen Back button returns to form with data
**Priority:** Unset | **State:** 17

**Description:** Verify tapping Back on the Review Bank Account screen returns to the form with all values retained

**Prerequisites:**
- Member is on the Review Bank Account screen
- All form fields were filled before proceeding

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap the Back button (←) | Member is returned to the Add Bank Account form; All previously entered values are retained in their fields |

---

#### TC-151422 · Add Bank Account – OTP screen Back button returns to Review screen
**Priority:** Unset | **State:** 17

**Description:** Verify tapping Back on the OTP screen returns to the Review Bank Account screen with data retained

**Prerequisites:**
- Member is on the Email OTP screen

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap the Back button (←) | Member is returned to the Review Bank Account screen; All entered values are still displayed; Bank account is NOT created |

---

#### TC-151423 · Edit – Back button returns to listing without saving
**Priority:** Unset | **State:** 17

**Description:** Verify tapping Back on the Edit Bank Account screen returns to the Linked Bank Accounts listing

**Prerequisites:**
- Member is on the Edit Bank Account screen

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap the Back button (←) | Member is returned to the Linked bank accounts listing screen; No changes are saved if Back is tapped without tapping Save changes |

---

### App lifecycle – Background (5 cases)

#### TC-151424 · Add Bank Account – Background app during form fill retains data on resume
**Priority:** Unset | **State:** 17

**Description:** Verify form data is retained when member backgrounds the app during form fill and returns

**Prerequisites:**
- Member has partially filled the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Background the app (press Home) | — |
| 2 | Return to the app | Add Bank Account form is shown on resume; All previously entered field values are retained; Member can continue filling the form |

---

#### TC-151425 · Add Bank Account – Background app during OTP resumes with valid OTP
**Priority:** Unset | **State:** 17

**Description:** Verify OTP remains valid when member backgrounds the app and returns before expiry

**Prerequisites:**
- Member is on the Email OTP screen
- OTP has been sent and countdown timer is active

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Background the app (press Home) | — |
| 2 | Return to the app before the countdown expires | OTP screen is shown on resume; Countdown timer continues from where it left off; Member can still enter the OTP successfully |

---

#### TC-151427 · Add Bank Account – Background app on Review screen retains data on resume
**Priority:** Unset | **State:** 17

**Description:** Verify Review Bank Account screen data is retained when member backgrounds the app and returns

**Prerequisites:**
- Member is on the Review Bank Account screen

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Background the app (press Home) | — |
| 2 | Return to the app | Review Bank Account screen is shown on resume; All entered values are still displayed; Member can proceed to tap "Save bank account" |

---

#### TC-151431 · Edit – Background app retains unsaved changes on resume
**Priority:** Unset | **State:** 17

**Description:** Verify unsaved changes are retained when member backgrounds the Edit Bank Account screen and returns

**Prerequisites:**
- Member is on the Edit Bank Account screen
- Member has changed Label or currencies but NOT tapped Save changes

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Background the app (press Home) | — |
| 2 | Return to the app | Edit Bank Account screen is shown on resume; Unsaved changes (label/currencies) are still visible in the fields; Member can continue editing or tap Save changes |

---

### App lifecycle – Kill app (4 cases)

#### TC-151426 · Add Bank Account – Kill app on Review screen does not create account
**Priority:** Unset | **State:** 17

**Description:** Verify bank account is not created when app is killed on the Review Bank Account screen

**Prerequisites:**
- Member is on the Review Bank Account screen

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Force close (kill) the app | — |
| 2 | Reopen the app and navigate to Linked bank accounts | Bank account is NOT created; Linked bank accounts listing shows no new account; Member must restart the Add Bank Account flow |

---

#### TC-151428 · Add Bank Account – Kill app during form fill clears form on reopen
**Priority:** Unset | **State:** 17

**Description:** Verify form data is cleared when app is killed during Add Bank Account form fill

**Prerequisites:**
- Member has partially filled the Add Bank Account form

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Force close (kill) the app | — |
| 2 | Reopen the app and navigate to Add Bank Account | Form is empty / cleared (assumption: no draft saved); Member must re-enter all fields |

---

#### TC-151429 · Add Bank Account – Kill app during OTP does not create account
**Priority:** Unset | **State:** 17

**Description:** Verify bank account is not created when app is killed during OTP entry

**Prerequisites:**
- Member is on the Email OTP screen
- OTP has been sent but not yet submitted

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Force close (kill) the app | — |
| 2 | Reopen the app | Member is returned to the app home or login screen (not OTP screen); Bank account is NOT created; Member must restart the Add Bank Account flow to try again |

---

#### TC-151430 · Edit – Kill app discards unsaved changes
**Priority:** Unset | **State:** 17

**Description:** Verify unsaved changes are discarded when app is killed on the Edit Bank Account screen

**Prerequisites:**
- Member is on the Edit Bank Account screen
- Member has changed Label or Supported currencies but NOT tapped Save changes

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Force close (kill) the app | — |
| 2 | Reopen the app and navigate to the bank account | Bank account data is unchanged (original label and currencies retained); Unsaved edits are discarded |

---

### Blocked – Disabled record (1 case)

#### TC-162007 · Add bank account blocked when matching record is Disabled
**Priority:** Unset | **State:** 2 (Review)

**Description:** Verify member gets an error when adding a bank account matching a Disabled record (same Account Number/IBAN + BIC/SWIFT)

**Prerequisites:**
- Admin has Disabled a bank account with a specific Account Number/IBAN and BIC/SWIFT
- Member is in the mobile app Add Bank Account flow

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Member fills in the Add Bank Account form using the same Account Number/IBAN and BIC/SWIFT as the Disabled record | — |
| 2 | Member submits the form | The system rejects the submission; An error message is shown to the member; No new bank account is created |

---

> **Note:** 4 cases were listed in the Testmo issue link but returned "not found" when fetched from project 8:
> - TC-151379 — All fields valid and BIC country matches proceeds to Review
> - TC-151380 — BIC country mismatch warning shown
> - TC-151400 — View Active bank account opens Edit Bank Account screen
> - TC-151410 — Delete – Cancel keeps account unchanged

# Manual Test Cases — AO-923
# [OTC][MobileApp][Member] Linked Bank Accounts — Add, Edit, Remove
# Module: Withdrawal Accounts

---

## AO-923_TC-01
**Name:** Withdrawal Accounts - Linked Bank Accounts - Access via My Account entry point - Listing screen displayed
**Test Scenario:** Verify that a verified Active member can access the Linked Bank Accounts listing via My Account → Withdrawal Accounts → Linked Bank Accounts.
**Test Case Type:** Happy Path
**Pre-requisites:** Logged in as a verified member with Approved verification status and Active account status.
**Steps:**
1. From the home screen, navigate to My Account.
2. Tap Withdrawal Accounts.
3. Tap Linked Bank Accounts.
4. Observe the screen displayed.
**Test Data:** —
**Expected Result:** The Linked Bank Accounts listing screen is displayed. If the member has no accounts, the empty state message "You haven't added a bank account yet. Add one to withdraw your fiat balances." is shown; if accounts exist, the account list is displayed.
**Priority:** High
**Requirement Reference:** AC-1; BR-1
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-02
**Name:** Withdrawal Accounts - Linked Bank Accounts - Access via Withdrawal Fiat entry point - Listing screen displayed
**Test Scenario:** Verify that a verified Active member can access the Add Bank Account screen via Withdrawal → Fiat → Bank Account → Add Bank Account.
**Test Case Type:** Happy Path
**Pre-requisites:** Logged in as a verified member with Approved verification status and Active account status.
**Steps:**
1. From the home screen, tap Withdrawal.
2. Select Fiat.
3. Tap Bank Account.
4. Tap Add Bank Account.
5. Observe the screen displayed.
**Test Data:** —
**Expected Result:** The Add Bank Account form screen is displayed.
**Priority:** High
**Requirement Reference:** AC-2; BR-1
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-03
**Name:** Withdrawal Accounts - Linked Bank Accounts - Non-verified member Add Bank Account - Redirected to verification flow
**Test Scenario:** Verify that a non-verified member who attempts to add a bank account is redirected to the verification flow, and a verified member is not redirected.
**Test Case Type:** Permission / Role
**Pre-requisites:** Two test accounts available: (1) member with non-verified status; (2) verified member with Approved status.
**Steps:**
1. Log in as the non-verified member.
2. Navigate to My Account → Withdrawal Accounts → Linked Bank Accounts.
3. Tap Add Bank Account.
4. Observe the screen displayed.
**Test Data:** —
**Expected Result:** The verification flow bottom sheet is displayed (same behaviour as tapping the deposit module entry point).
**Priority:** High
**Requirement Reference:** AC-3; BR-1
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-04
**Name:** Withdrawal Accounts - Linked Bank Accounts - Non-Active member Add Bank Account - Blocked
**Test Scenario:** Verify that a non-Active member (e.g. suspended) is blocked from adding a bank account and is redirected to the verification flow.
**Test Case Type:** Permission / Role
**Pre-requisites:** Test account with non-Active status (e.g. suspended) but Approved verification status available.
**Steps:**
1. Log in as the non-Active member.
2. Navigate to My Account → Withdrawal Accounts → Linked Bank Accounts.
3. Tap Add Bank Account.
4. Observe the screen displayed.
**Test Data:** —
**Expected Result:** Member is blocked from adding a bank account; redirected to verification flow (same gate as non-verified member).
**Priority:** Medium
**Requirement Reference:** BR-1
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**


---

## AO-923_TC-05
**Name:** Withdrawal Accounts - Linked Bank Accounts - Listing sort order - Active before Disabled, newest first
**Test Scenario:** Verify that the bank account listing displays Active accounts before Disabled accounts, sorted by most recently added first within each group.
**Test Case Type:** Happy Path
**Pre-requisites:** Logged in as a verified Active member with at least two Active and one Disabled bank accounts present, added at different times.
**Steps:**
1. Navigate to My Account → Withdrawal Accounts → Linked Bank Accounts.
2. Observe the order of accounts in the listing.
**Test Data:** —
**Expected Result:** Active accounts are listed first (sorted newest added first), followed by Disabled accounts (sorted newest added first).
**Priority:** Medium
**Requirement Reference:** AC-9; BR-2
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-06
**Name:** Withdrawal Accounts - Linked Bank Accounts - Newly added account - Appears at top of listing
**Test Scenario:** Verify that a newly added bank account appears at the top of the Active accounts list immediately after successful addition.
**Test Case Type:** Happy Path
**Pre-requisites:** Logged in as a verified Active member with at least one existing Active bank account.
**Steps:**
1. Navigate to My Account → Withdrawal Accounts → Linked Bank Accounts.
2. Note the current top account in the listing.
3. Add a new bank account and complete OTP verification.
4. Return to the Linked Bank Accounts listing.
5. Observe the position of the newly added account.
**Test Data:** —
**Expected Result:** The newly added account appears at the top of the Active accounts section.
**Priority:** Medium
**Requirement Reference:** AC-9; BR-2
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-07
**Name:** Withdrawal Accounts - Linked Bank Accounts - Empty state - Correct message and CTA displayed
**Test Scenario:** Verify that the correct empty state message and Add Bank Account CTA are displayed when the member has no linked bank accounts.
**Test Case Type:** Empty / No Data
**Pre-requisites:** Logged in as a verified Active member with no bank accounts added.
**Steps:**
1. Navigate to My Account → Withdrawal Accounts → Linked Bank Accounts.
2. Observe the screen content.
**Test Data:** —
**Expected Result:** Empty state is displayed with message "You haven't added a bank account yet. Add one to withdraw your fiat balances." and an Add Bank Account CTA.
**Priority:** Medium
**Requirement Reference:** BR-2
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-08
**Name:** Withdrawal Accounts - Linked Bank Accounts - Search by Label - Matching accounts returned
**Test Scenario:** Verify that searching by Label returns only accounts whose Label matches the search term.
**Test Case Type:** Happy Path
**Pre-requisites:** Logged in as a verified Active member with at least two bank accounts with distinct Labels (one labelled `My OCBC SGD`, another with a different label).
**Steps:**
1. Navigate to My Account → Withdrawal Accounts → Linked Bank Accounts.
2. Tap the search field.
3. Enter the Label of one of the existing accounts.
4. Observe the results.
**Test Data:** `My OCBC SGD`
**Expected Result:** Only the account whose Label matches the search term is displayed in the results.
**Priority:** Medium
**Requirement Reference:** AC-10; BR-2
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-09
**Name:** Withdrawal Accounts - Linked Bank Accounts - Search by Bank Name - Matching accounts returned
**Test Scenario:** Verify that searching by Bank Name returns only accounts whose Bank Name matches the search term.
**Test Case Type:** Happy Path
**Pre-requisites:** Logged in as a verified Active member with at least two bank accounts with distinct Bank Names (one with Bank Name `OCBC`, another with a different name).
**Steps:**
1. Navigate to My Account → Withdrawal Accounts → Linked Bank Accounts.
2. Tap the search field.
3. Enter the Bank Name of one of the existing accounts.
4. Observe the results.
**Test Data:** `OCBC`
**Expected Result:** Only the account whose Bank Name matches the search term is displayed.
**Priority:** Medium
**Requirement Reference:** AC-10; BR-2
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**


---

## AO-923_TC-10
**Name:** Withdrawal Accounts - Linked Bank Accounts - Search by masked Account Number - Matching accounts returned
**Test Scenario:** Verify that searching by the last 4 digits of the Account Number returns only accounts whose Account Number ends with those digits.
**Test Case Type:** Happy Path
**Pre-requisites:** Logged in as a verified Active member with at least two bank accounts with different Account Numbers (one ending in `6819`, another ending in different digits).
**Steps:**
1. Navigate to My Account → Withdrawal Accounts → Linked Bank Accounts.
2. Tap the search field.
3. Enter the last 4 digits of one account's Account Number.
4. Observe the results.
**Test Data:** `6819`
**Expected Result:** Only the account whose Account Number ends with the entered 4 digits is displayed.
**Priority:** Medium
**Requirement Reference:** AC-10; BR-2
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-11
**Name:** Withdrawal Accounts - Linked Bank Accounts - Search no match - Empty search state displayed
**Test Scenario:** Verify that searching with a term that matches no bank accounts displays an empty/no-results state.
**Test Case Type:** Empty / No Data
**Pre-requisites:** Logged in as a verified Active member with at least one bank account.
**Steps:**
1. Navigate to My Account → Withdrawal Accounts → Linked Bank Accounts.
2. Tap the search field.
3. Enter a search term that does not match any Label, Bank Name, or Account Number.
4. Observe the results.
**Test Data:** `ZZZNOMATCH999`
**Expected Result:** No accounts are displayed; a no-results state is shown (no rows visible in the search results area).
**Priority:** Low
**Requirement Reference:** BR-2
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-12
**Name:** Withdrawal Accounts - Linked Bank Accounts - Disabled account - Displayed as non-clickable
**Test Scenario:** Verify that a Disabled bank account row appears visually disabled (greyed out or non-interactive) in the listing.
**Test Case Type:** Status Transition
**Pre-requisites:** Logged in as a verified Active member with at least one Disabled bank account.
**Steps:**
1. Navigate to My Account → Withdrawal Accounts → Linked Bank Accounts.
2. Locate the Disabled account row.
3. Observe the visual state of the row.
**Test Data:** —
**Expected Result:** The Disabled account row is displayed in a visually disabled state (non-interactive appearance).
**Priority:** Medium
**Requirement Reference:** AC-11; BR-2
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-13
**Name:** Withdrawal Accounts - Linked Bank Accounts - Disabled account tap - Error toast displayed
**Test Scenario:** Verify that tapping a Disabled bank account row displays the correct error toast message.
**Test Case Type:** Negative
**Pre-requisites:** Logged in as a verified Active member with at least one Disabled bank account.
**Steps:**
1. Navigate to My Account → Withdrawal Accounts → Linked Bank Accounts.
2. Tap the Disabled account row.
3. Observe the message displayed.
**Test Data:** —
**Expected Result:** Error toast displayed: "This bank account has been disabled, contact us for further assistance."
**Priority:** Medium
**Requirement Reference:** AC-11; BR-2; ERR-15
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-14
**Name:** Withdrawal Accounts - Linked Bank Accounts - Account limit reached - Add Bank Account CTA disabled
**Test Scenario:** Verify that the Add Bank Account CTA is disabled when the member has exactly 5 Active bank accounts.
**Test Case Type:** Boundary
**Pre-requisites:** Logged in as a verified Active member with exactly 5 Active bank accounts.
**Steps:**
1. Navigate to My Account → Withdrawal Accounts → Linked Bank Accounts.
2. Observe the state of the Add Bank Account CTA.
**Test Data:** —
**Expected Result:** The Add Bank Account CTA is disabled (non-interactive).
**Priority:** High
**Requirement Reference:** AC-8; BR-2; BR-1
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-15
**Name:** Withdrawal Accounts - Linked Bank Accounts - Account limit reached - Toast message displayed
**Test Scenario:** Verify that tapping the disabled Add Bank Account CTA when at the 5-account limit shows the correct toast message with the limit value rendered.
**Test Case Type:** Boundary
**Pre-requisites:** Logged in as a verified Active member with exactly 5 Active bank accounts.
**Steps:**
1. Navigate to My Account → Withdrawal Accounts → Linked Bank Accounts.
2. Tap the disabled Add Bank Account CTA.
3. Observe the message displayed.
**Test Data:** —
**Expected Result:** Toast displayed: "You've reached the maximum of 5 bank accounts. Please remove one before adding another." (the value "5" is rendered, not a placeholder).
**Priority:** High
**Requirement Reference:** AC-8; BR-2; ERR-13
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**


---

## AO-923_TC-16
**Name:** Withdrawal Accounts - Linked Bank Accounts - Below account limit - Add Bank Account CTA enabled
**Test Scenario:** Verify that the Add Bank Account CTA is enabled when the member has fewer than 5 Active bank accounts.
**Test Case Type:** Boundary
**Pre-requisites:** Logged in as a verified Active member with 4 or fewer Active bank accounts.
**Steps:**
1. Navigate to My Account → Withdrawal Accounts → Linked Bank Accounts.
2. Observe the state of the Add Bank Account CTA.
**Test Data:** —
**Expected Result:** The Add Bank Account CTA is enabled and interactive.
**Priority:** High
**Requirement Reference:** BR-2; BR-1
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-17
**Name:** Withdrawal Accounts - Linked Bank Accounts - Disabled accounts not counted toward limit
**Test Scenario:** Verify that Disabled bank accounts are not counted toward the 5-account Active limit.
**Test Case Type:** Boundary
**Pre-requisites:** Logged in as a verified Active member with 4 Active and 1 Disabled bank accounts.
**Steps:**
1. Navigate to My Account → Withdrawal Accounts → Linked Bank Accounts.
2. Observe the state of the Add Bank Account CTA.
**Test Data:** —
**Expected Result:** The Add Bank Account CTA is enabled (Disabled account does not count toward the limit; total Active count is 4).
**Priority:** High
**Requirement Reference:** AC-20; BR-1
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-18
**Name:** Withdrawal Accounts - Linked Bank Accounts - Deleted accounts not counted toward limit
**Test Scenario:** Verify that Deleted bank accounts are not counted toward the 5-account Active limit.
**Test Case Type:** Boundary
**Pre-requisites:** Logged in as a verified Active member with 4 Active and 1 Deleted bank account (Deleted record exists in system).
**Steps:**
1. Navigate to My Account → Withdrawal Accounts → Linked Bank Accounts.
2. Observe the state of the Add Bank Account CTA.
**Test Data:** —
**Expected Result:** The Add Bank Account CTA is enabled (Deleted account does not count; total Active count is 4).
**Priority:** High
**Requirement Reference:** AC-20; BR-1
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-19
**Name:** Withdrawal Accounts - Linked Bank Accounts - Active account tap - Bank Account Details page opened
**Test Scenario:** Verify that tapping an Active bank account row opens the Bank Account Details page for that account.
**Test Case Type:** Navigation / Screen Flow
**Pre-requisites:** Logged in as a verified Active member with at least one Active bank account.
**Steps:**
1. Navigate to My Account → Withdrawal Accounts → Linked Bank Accounts.
2. Tap an Active account row.
3. Observe the screen displayed.
**Test Data:** —
**Expected Result:** The Bank Account Details page for the tapped account is displayed.
**Priority:** High
**Requirement Reference:** BR-2
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-20
**Name:** Withdrawal Accounts - Add Bank Account - Required and optional fields displayed with correct labels
**Test Scenario:** Verify that all required and optional fields are displayed with correct labels and helper texts on the Add Bank Account form.
**Test Case Type:** Display / UI
**Pre-requisites:** Logged in as a verified Active member with fewer than 5 Active bank accounts.
**Steps:**
1. Navigate to My Account → Withdrawal Accounts → Linked Bank Accounts.
2. Tap Add Bank Account.
3. Observe all fields displayed on the form.
**Test Data:** —
**Expected Result:** Required fields present: Label, Bank Country, Bank Name, Account Holder Name, Account Number / IBAN, BIC / SWIFT, Currency, Address Line 1, City. Optional fields present: Bank Code / Routing Number, Account Type, Address Line 2, Postal Code. All helper texts match the specification (e.g. Currency: "Select the currencies this account can receive."; Account Holder Name: "Enter the name exactly as it appears on your bank account.").
**Priority:** Medium
**Requirement Reference:** AC-4; BR-3
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**


---

## AO-923_TC-21
**Name:** Withdrawal Accounts - Add Bank Account - Optional fields visible on form
**Test Scenario:** Verify that optional fields (Bank Code / Routing Number, Account Type, Address Line 2, Postal Code) are visible on the Add Bank Account form.
**Test Case Type:** Display / UI
**Pre-requisites:** Logged in as a verified Active member with fewer than 5 Active bank accounts.
**Steps:**
1. Navigate to My Account → Withdrawal Accounts → Linked Bank Accounts.
2. Tap Add Bank Account.
3. Observe all fields present on the screen.
**Test Data:** —
**Expected Result:** Bank Code / Routing Number, Account Type, Address Line 2, and Postal Code fields are visible on the form.
**Priority:** Low
**Requirement Reference:** AC-4; BR-3
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-22
**Name:** Withdrawal Accounts - Add Bank Account - Label - Valid input accepted
**Test Scenario:** Verify that a valid alphanumeric Label of up to 30 characters is accepted in the Label field.
**Test Case Type:** Happy Path
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Enter a valid Label.
3. Tap Continue.
4. Observe that no validation error appears for the Label field.
**Test Data:** `My OCBC Account`
**Expected Result:** No validation error is shown for the Label field.
**Priority:** High
**Requirement Reference:** AC-4; BR-3
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-23
**Name:** Withdrawal Accounts - Add Bank Account - Label - Empty field error
**Test Scenario:** Verify that the Label field validation error is displayed when the Label field is empty on form submission.
**Test Case Type:** Validation
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Leave the Label field empty.
3. Fill in all other required fields with valid data.
4. Tap Continue.
5. Observe the error displayed for the Label field.
**Test Data:** Label: (empty)
**Expected Result:** Validation error displayed: "Please enter a label."
**Priority:** High
**Requirement Reference:** BR-3; ERR-D1
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-24
**Name:** Withdrawal Accounts - Add Bank Account - Label - Exceeds 30 characters error
**Test Scenario:** Verify that the Label field validation error is displayed when the Label exceeds 30 characters.
**Test Case Type:** Boundary
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Enter a 31-character string in the Label field.
3. Fill in all other required fields with valid data.
4. Tap Continue.
5. Observe the error displayed for the Label field.
**Test Data:** `AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA` (31 characters)
**Expected Result:** Validation error displayed: "Label cannot exceed 30 characters."
**Priority:** Medium
**Requirement Reference:** BR-3; ERR-D2
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-25
**Name:** Withdrawal Accounts - Add Bank Account - Bank Country - Options match platform country list
**Test Scenario:** Verify that the Bank Country dropdown options match the OTC platform's configured country list.
**Test Case Type:** Selection / Reference List
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Tap the Bank Country field.
3. Observe the list of available country options.
**Test Data:** —
**Expected Result:** The countries listed match the OTC platform's configured country list (reference: OTC country list spreadsheet).
**Priority:** Medium
**Requirement Reference:** BR-3
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-26
**Name:** Withdrawal Accounts - Add Bank Account - Bank Country - Not selected error
**Test Scenario:** Verify that the Bank Country field validation error is displayed when no country is selected on form submission.
**Test Case Type:** Validation
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Leave Bank Country unselected.
3. Fill in all other required fields with valid data.
4. Tap Continue.
5. Observe the error displayed for the Bank Country field.
**Test Data:** Bank Country: (not selected)
**Expected Result:** Validation error displayed: "Please select a bank country."
**Priority:** High
**Requirement Reference:** BR-3; ERR-D3
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**


---

## AO-923_TC-27
**Name:** Withdrawal Accounts - Add Bank Account - Bank Name - Valid alphanumeric and special characters accepted
**Test Scenario:** Verify that a Bank Name containing alphanumeric characters and the allowed special characters is accepted.
**Test Case Type:** Happy Path
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Enter a Bank Name containing letters, numbers, and the characters `& ' . , - ( ) /`.
3. Fill in all other required fields with valid data.
4. Tap Continue.
5. Observe that no validation error appears for the Bank Name field.
**Test Data:** `OCBC Bank (S'pore) Ltd & Co.`
**Expected Result:** No validation error is shown for the Bank Name field.
**Priority:** High
**Requirement Reference:** BR-3
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-28
**Name:** Withdrawal Accounts - Add Bank Account - Bank Name - Empty field error
**Test Scenario:** Verify that the Bank Name field validation error is displayed when the field is empty on form submission.
**Test Case Type:** Validation
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Leave the Bank Name field empty.
3. Fill in all other required fields with valid data.
4. Tap Continue.
5. Observe the error for the Bank Name field.
**Test Data:** Bank Name: (empty)
**Expected Result:** Validation error displayed: "Please enter a bank name."
**Priority:** High
**Requirement Reference:** BR-3; ERR-D4
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-29
**Name:** Withdrawal Accounts - Add Bank Account - Bank Name - Exceeds 100 characters error
**Test Scenario:** Verify that the Bank Name field validation error is displayed when the Bank Name exceeds 100 characters.
**Test Case Type:** Boundary
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Enter a 101-character string in the Bank Name field.
3. Fill in all other required fields with valid data.
4. Tap Continue.
5. Observe the error for the Bank Name field.
**Test Data:** `AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA` (101 characters)
**Expected Result:** Validation error displayed: "Bank name cannot exceed 100 characters."
**Priority:** Medium
**Requirement Reference:** BR-3; ERR-D5
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-30
**Name:** Withdrawal Accounts - Add Bank Account - Bank Name - Invalid special characters rejected
**Test Scenario:** Verify that the Bank Name field validation error is displayed when the field contains a disallowed special character, and that the allowed special characters are accepted without error.
**Test Case Type:** Validation
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Enter a Bank Name containing `@` character (e.g. `Bank@Name`).
3. Fill in all other required fields with valid data.
4. Tap Continue.
5. Observe the error for the Bank Name field.
**Test Data:** `Bank@Name`
**Expected Result:** A validation error is displayed for the Bank Name field indicating the entered character is not allowed.
**Priority:** Medium
**Requirement Reference:** BR-3
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-31
**Name:** Withdrawal Accounts - Add Bank Account - Account Holder Name - Valid input accepted
**Test Scenario:** Verify that a valid alphanumeric Account Holder Name of up to 30 characters is accepted.
**Test Case Type:** Happy Path
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Enter a valid Account Holder Name.
3. Fill in all other required fields with valid data.
4. Tap Continue.
5. Observe that no validation error appears for the Account Holder Name field.
**Test Data:** `John Smith`
**Expected Result:** No validation error is shown for the Account Holder Name field.
**Priority:** High
**Requirement Reference:** BR-3
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**


---

## AO-923_TC-32
**Name:** Withdrawal Accounts - Add Bank Account - Account Holder Name - Empty field error
**Test Scenario:** Verify that the Account Holder Name field validation error is displayed when the field is empty on form submission.
**Test Case Type:** Validation
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Leave Account Holder Name empty.
3. Fill in all other required fields with valid data.
4. Tap Continue.
5. Observe the error for Account Holder Name.
**Test Data:** Account Holder Name: (empty)
**Expected Result:** Validation error displayed: "Please enter the account name."
**Priority:** High
**Requirement Reference:** BR-3; ERR-D7
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-33
**Name:** Withdrawal Accounts - Add Bank Account - Account Holder Name - Exceeds 30 characters error
**Test Scenario:** Verify that the Account Holder Name field validation error is displayed when the name exceeds 30 characters.
**Test Case Type:** Boundary
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Enter a 31-character string in Account Holder Name.
3. Fill in all other required fields with valid data.
4. Tap Continue.
5. Observe the error for Account Holder Name.
**Test Data:** `AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA` (31 characters)
**Expected Result:** Validation error displayed: "Account name cannot exceed 30 characters."
**Priority:** Medium
**Requirement Reference:** BR-3; ERR-D8
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-34
**Name:** Withdrawal Accounts - Add Bank Account - Account Number IBAN - Valid input accepted
**Test Scenario:** Verify that a valid alphanumeric Account Number / IBAN of up to 34 characters is accepted.
**Test Case Type:** Happy Path
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Enter a valid Account Number / IBAN.
3. Fill in all other required fields with valid data.
4. Tap Continue.
5. Observe that no validation error appears for Account Number / IBAN.
**Test Data:** `GB29NWBK60161331926819`
**Expected Result:** No validation error is shown for Account Number / IBAN.
**Priority:** High
**Requirement Reference:** BR-3
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-35
**Name:** Withdrawal Accounts - Add Bank Account - Account Number IBAN - Empty field error
**Test Scenario:** Verify that the Account Number / IBAN field validation error is displayed when the field is empty on form submission.
**Test Case Type:** Validation
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Leave Account Number / IBAN empty.
3. Fill in all other required fields with valid data.
4. Tap Continue.
5. Observe the error for Account Number / IBAN.
**Test Data:** Account Number / IBAN: (empty)
**Expected Result:** Validation error displayed: "Please enter an account number."
**Priority:** High
**Requirement Reference:** BR-3; ERR-1
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-36
**Name:** Withdrawal Accounts - Add Bank Account - Account Number IBAN - Exceeds 34 characters error
**Test Scenario:** Verify that the Account Number / IBAN field validation error is displayed when the value exceeds 34 characters.
**Test Case Type:** Boundary
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Enter a 35-character alphanumeric string in Account Number / IBAN.
3. Fill in all other required fields with valid data.
4. Tap Continue.
5. Observe the error for Account Number / IBAN.
**Test Data:** `AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA` (35 characters)
**Expected Result:** Validation error displayed: "Account number cannot exceed 34 characters."
**Priority:** Medium
**Requirement Reference:** BR-3; ERR-D10
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**


---

## AO-923_TC-37
**Name:** Withdrawal Accounts - Add Bank Account - BIC SWIFT - 8-character code accepted
**Test Scenario:** Verify that a valid 8-character BIC / SWIFT code is accepted.
**Test Case Type:** Happy Path
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Enter an 8-character BIC / SWIFT code.
3. Fill in all other required fields with valid data.
4. Tap Continue.
5. Observe that no validation error appears for BIC / SWIFT.
**Test Data:** `OCBCSGSG` (8 characters)
**Expected Result:** No validation error is shown for BIC / SWIFT.
**Priority:** High
**Requirement Reference:** BR-3
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-38
**Name:** Withdrawal Accounts - Add Bank Account - BIC SWIFT - 11-character code accepted
**Test Scenario:** Verify that a valid 11-character BIC / SWIFT code is accepted.
**Test Case Type:** Happy Path
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Enter an 11-character BIC / SWIFT code.
3. Fill in all other required fields with valid data.
4. Tap Continue.
5. Observe that no validation error appears for BIC / SWIFT.
**Test Data:** `OCBCSGSGXXX` (11 characters)
**Expected Result:** No validation error is shown for BIC / SWIFT.
**Priority:** High
**Requirement Reference:** BR-3
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-39
**Name:** Withdrawal Accounts - Add Bank Account - BIC SWIFT - Empty field error
**Test Scenario:** Verify that the BIC / SWIFT field validation error is displayed when the field is empty on form submission.
**Test Case Type:** Validation
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Leave BIC / SWIFT empty.
3. Fill in all other required fields with valid data.
4. Tap Continue.
5. Observe the error for BIC / SWIFT.
**Test Data:** BIC / SWIFT: (empty)
**Expected Result:** Validation error displayed: "Please enter your bank's SWIFT/BIC code. Your bank can provide this if you don't have it."
**Priority:** High
**Requirement Reference:** BR-3; ERR-3
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-40
**Name:** Withdrawal Accounts - Add Bank Account - BIC SWIFT - Invalid format error
**Test Scenario:** Verify that the BIC / SWIFT field validation error is displayed when the value is not 8 or 11 characters.
**Test Case Type:** Validation
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Enter a BIC / SWIFT code that is 9 characters (invalid length).
3. Fill in all other required fields with valid data.
4. Tap Continue.
5. Observe the error for BIC / SWIFT.
6. Repeat steps 2–5 with a 10-character BIC / SWIFT code.
**Test Data:** 9-character: `OCBCSGSGX`; 10-character: `OCBCSGSGXX`
**Expected Result:** Validation error displayed: "Please check the SWIFT/BIC code and try again."
**Priority:** High
**Requirement Reference:** BR-3; ERR-4
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-41
**Name:** Withdrawal Accounts - Add Bank Account - Currency - Options match platform fiat currency list
**Test Scenario:** Verify that the Currency multi-select options match all fiat currencies supported by the platform.
**Test Case Type:** Selection / Reference List
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Tap the Currency field.
3. Observe the list of available currency options.
**Test Data:** —
**Expected Result:** The currencies listed match the platform's configured fiat currency list.
**Priority:** High
**Requirement Reference:** BR-3
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-42
**Name:** Withdrawal Accounts - Add Bank Account - Currency - No currency selected error
**Test Scenario:** Verify that the Currency field validation error is displayed when no currency is selected on form submission.
**Test Case Type:** Validation
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Leave Currency unselected.
3. Fill in all other required fields with valid data.
4. Tap Continue.
5. Observe the error for Currency.
**Test Data:** Currency: (none selected)
**Expected Result:** Validation error displayed: "Please select at least one currency."
**Priority:** High
**Requirement Reference:** BR-3; ERR-7
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**


---

## AO-923_TC-43
**Name:** Withdrawal Accounts - Add Bank Account - Currency - Multiple currencies selectable
**Test Scenario:** Verify that multiple currencies can be selected simultaneously in the Currency field.
**Test Case Type:** Happy Path
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Tap the Currency field.
3. Select two or more currencies.
4. Fill in all other required fields with valid data.
5. Tap Continue.
6. Observe that no validation error appears for Currency and all selected currencies are shown.
**Test Data:** Select currencies: SGD, USD
**Expected Result:** Both SGD and USD are selected and shown; no validation error for Currency.
**Priority:** High
**Requirement Reference:** BR-3
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-44
**Name:** Withdrawal Accounts - Add Bank Account - Account Type - Options available
**Test Scenario:** Verify that the Account Type optional field displays Checking, Savings, and Not specified as options.
**Test Case Type:** Selection / Reference List
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Tap the Account Type field.
3. Observe the available options.
**Test Data:** —
**Expected Result:** Options displayed: Checking, Savings, Not specified.
**Priority:** Low
**Requirement Reference:** BR-3
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-45
**Name:** Withdrawal Accounts - Add Bank Account - Bank Code Routing Number - Optional free text accepted
**Test Scenario:** Verify that the Bank Code / Routing Number optional field accepts free text input of up to 100 characters.
**Test Case Type:** Happy Path
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Enter a value in the Bank Code / Routing Number field.
3. Fill in all other required fields with valid data.
4. Tap Continue.
5. Observe that no validation error appears for Bank Code / Routing Number.
**Test Data:** `082-000`
**Expected Result:** No validation error for Bank Code / Routing Number.
**Priority:** Low
**Requirement Reference:** BR-3
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-46
**Name:** Withdrawal Accounts - Add Bank Account - Bank Code Routing Number - Exceeds 100 characters error
**Test Scenario:** Verify that the Bank Code / Routing Number field validation error is displayed when the value exceeds 100 characters.
**Test Case Type:** Boundary
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Enter a 101-character string in Bank Code / Routing Number.
3. Fill in all other required fields with valid data.
4. Tap Continue.
5. Observe the error for Bank Code / Routing Number.
**Test Data:** `AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA` (101 characters)
**Expected Result:** Validation error displayed: "Bank code cannot exceed 100 characters."
**Priority:** Low
**Requirement Reference:** BR-3; ERR-D20
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-47
**Name:** Withdrawal Accounts - Add Bank Account - Address Line 1 - Valid input accepted
**Test Scenario:** Verify that a valid Address Line 1 of up to 100 characters is accepted.
**Test Case Type:** Happy Path
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Enter a valid value in Address Line 1.
3. Fill in all other required fields with valid data.
4. Tap Continue.
5. Observe that no validation error appears for Address Line 1.
**Test Data:** `123 Orchard Road`
**Expected Result:** No validation error for Address Line 1.
**Priority:** High
**Requirement Reference:** BR-3
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-48
**Name:** Withdrawal Accounts - Add Bank Account - Address Line 1 - Empty field error
**Test Scenario:** Verify that the Address Line 1 field validation error is displayed when the field is empty on form submission.
**Test Case Type:** Validation
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Leave Address Line 1 empty.
3. Fill in all other required fields with valid data.
4. Tap Continue.
5. Observe the error for Address Line 1.
**Test Data:** Address Line 1: (empty)
**Expected Result:** Validation error displayed: "Please enter your address."
**Priority:** High
**Requirement Reference:** BR-3; ERR-D13
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**


---

## AO-923_TC-49
**Name:** Withdrawal Accounts - Add Bank Account - Address Line 1 - Exceeds 100 characters error
**Test Scenario:** Verify that the Address Line 1 field validation error is displayed when the value exceeds 100 characters.
**Test Case Type:** Boundary
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Enter a 101-character string in Address Line 1.
3. Fill in all other required fields with valid data.
4. Tap Continue.
5. Observe the error for Address Line 1.
**Test Data:** `AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA` (101 characters)
**Expected Result:** Validation error displayed: "Address Line 1 cannot exceed 100 characters."
**Priority:** Medium
**Requirement Reference:** BR-3; ERR-D14
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-50
**Name:** Withdrawal Accounts - Add Bank Account - Address Line 2 - Optional exceeds 100 characters error
**Test Scenario:** Verify that the Address Line 2 field validation error is displayed when the optional value exceeds 100 characters.
**Test Case Type:** Boundary
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Enter a 101-character string in Address Line 2.
3. Fill in all other required fields with valid data.
4. Tap Continue.
5. Observe the error for Address Line 2.
**Test Data:** `AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA` (101 characters)
**Expected Result:** Validation error displayed: "Address Line 2 cannot exceed 100 characters."
**Priority:** Low
**Requirement Reference:** BR-3; ERR-D15
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-51
**Name:** Withdrawal Accounts - Add Bank Account - City - Valid input accepted
**Test Scenario:** Verify that a valid City value of up to 100 characters is accepted.
**Test Case Type:** Happy Path
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Enter a valid value in City.
3. Fill in all other required fields with valid data.
4. Tap Continue.
5. Observe that no validation error appears for City.
**Test Data:** `Singapore`
**Expected Result:** No validation error for City.
**Priority:** High
**Requirement Reference:** BR-3
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-52
**Name:** Withdrawal Accounts - Add Bank Account - City - Empty field error
**Test Scenario:** Verify that the City field validation error is displayed when the field is empty on form submission.
**Test Case Type:** Validation
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Leave City empty.
3. Fill in all other required fields with valid data.
4. Tap Continue.
5. Observe the error for City.
**Test Data:** City: (empty)
**Expected Result:** Validation error displayed: "Please enter your city."
**Priority:** High
**Requirement Reference:** BR-3; ERR-D16
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-53
**Name:** Withdrawal Accounts - Add Bank Account - City - Exceeds 100 characters error
**Test Scenario:** Verify that the City field validation error is displayed when the value exceeds 100 characters.
**Test Case Type:** Boundary
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Enter a 101-character string in City.
3. Fill in all other required fields with valid data.
4. Tap Continue.
5. Observe the error for City.
**Test Data:** `AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA` (101 characters)
**Expected Result:** Validation error displayed: "City cannot exceed 100 characters."
**Priority:** Medium
**Requirement Reference:** BR-3; ERR-D17
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-54
**Name:** Withdrawal Accounts - Add Bank Account - Postal Code - Optional exceeds 100 characters error
**Test Scenario:** Verify that the Postal Code field validation error is displayed when the optional value exceeds 100 characters.
**Test Case Type:** Boundary
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Enter a 101-character string in Postal Code.
3. Fill in all other required fields with valid data.
4. Tap Continue.
5. Observe the error for Postal Code.
**Test Data:** `AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA` (101 characters)
**Expected Result:** Validation error displayed: "Postal Code cannot exceed 100 characters."
**Priority:** Low
**Requirement Reference:** BR-3; ERR-D18
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**


---

## AO-923_TC-55
**Name:** Withdrawal Accounts - Add Bank Account - Continue CTA - Disabled until all required fields filled
**Test Scenario:** Verify that the Continue CTA is disabled when required fields are incomplete and enabled only when all required fields are filled.
**Test Case Type:** Navigation / Screen Flow
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Leave all fields empty and observe the Continue CTA state.
3. Fill in all required fields one by one.
4. After filling the last required field, observe the Continue CTA state.
**Test Data:** —
**Expected Result:** Continue CTA is disabled when any required field is empty; becomes enabled only when all required fields are filled.
**Priority:** Medium
**Requirement Reference:** BR-3; BR-3b
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-56
**Name:** Withdrawal Accounts - Add Bank Account - BIC country cross-check - Match - No warning shown
**Test Scenario:** Verify that no BIC country warning popup is shown when the BIC country code matches the selected Bank Country.
**Test Case Type:** Happy Path
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Select Bank Country: Singapore.
3. Enter a BIC / SWIFT code whose 5th–6th characters are "SG" (e.g. OCBCSGSG).
4. Fill in all other required fields with valid data.
5. Tap Continue.
6. Observe whether a warning popup appears.
**Test Data:** Bank Country: Singapore; BIC / SWIFT: `OCBCSGSG`
**Expected Result:** No BIC country mismatch warning popup is displayed; form proceeds to Review Bank Account screen.
**Priority:** High
**Requirement Reference:** AC-5; BR-3b
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-57
**Name:** Withdrawal Accounts - Add Bank Account - BIC country cross-check - Mismatch - Warning popup displayed with country names
**Test Scenario:** Verify that the BIC country mismatch warning popup is displayed with actual country names rendered when the BIC country code does not match the selected Bank Country.
**Test Case Type:** Validation
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Select Bank Country: Singapore.
3. Enter a BIC / SWIFT code whose 5th–6th characters are "DE" (e.g. DEUTDEFF).
4. Fill in all other required fields with valid data.
5. Tap Continue.
6. Observe the popup displayed.
**Test Data:** Bank Country: Singapore; BIC / SWIFT: `DEUTDEFF`
**Expected Result:** Warning popup displayed with message: "This SWIFT/BIC code looks like it belongs to a bank in Germany, but you selected Singapore. Please check before continuing." (actual country names rendered, not placeholders).
**Priority:** High
**Requirement Reference:** AC-5; BR-3b; ERR-5
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-58
**Name:** Withdrawal Accounts - Add Bank Account - BIC country mismatch warning - Review Details returns to form
**Test Scenario:** Verify that the BIC country mismatch warning popup is dismissed and the Add Bank Account form is displayed when Review Details is selected.
**Test Case Type:** Navigation / Screen Flow
**Pre-requisites:** Logged in as a verified Active member; BIC country mismatch warning popup is displayed (see TC-57 setup).
**Steps:**
1. Trigger the BIC country mismatch warning popup (Bank Country: Singapore; BIC: DEUTDEFF).
2. Tap Review Details on the popup.
3. Observe the screen displayed.
**Test Data:** Bank Country: Singapore; BIC / SWIFT: `DEUTDEFF`
**Expected Result:** The popup is dismissed and the Add Bank Account form is displayed with all previously entered values retained.
**Priority:** High
**Requirement Reference:** AC-5; BR-3b
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-59
**Name:** Withdrawal Accounts - Add Bank Account - BIC country mismatch warning - Continue anyway proceeds to Review
**Test Scenario:** Verify that the Review Bank Account screen is displayed when Continue anyway is selected on the BIC country mismatch warning popup.
**Test Case Type:** Navigation / Screen Flow
**Pre-requisites:** Logged in as a verified Active member; BIC country mismatch warning popup is displayed.
**Steps:**
1. Trigger the BIC country mismatch warning popup (Bank Country: Singapore; BIC: DEUTDEFF).
2. Tap Continue anyway on the popup.
3. Observe the screen displayed.
**Test Data:** Bank Country: Singapore; BIC / SWIFT: `DEUTDEFF`
**Expected Result:** The Review Bank Account screen is displayed with all entered values shown.
**Priority:** High
**Requirement Reference:** AC-5; BR-3b
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**


---

## AO-923_TC-60
**Name:** Withdrawal Accounts - Add Bank Account - Duplicate account - Error message and banner displayed
**Test Scenario:** Verify that submitting a bank account with the same Account Number / IBAN and BIC / SWIFT as an existing Active account for the same member displays the correct duplicate rejection error banner.
**Test Case Type:** Negative
**Pre-requisites:** Logged in as a verified Active member with an existing Active bank account with Account Number `GB29NWBK60161331926819` and BIC / SWIFT `OCBCSGSG`.
**Steps:**
1. Navigate to Add Bank Account form.
2. Enter the same Account Number / IBAN and BIC / SWIFT as the existing Active account.
3. Fill in all other required fields with valid data.
4. Tap Continue.
5. Observe the error displayed.
**Test Data:** Account Number / IBAN: `GB29NWBK60161331926819`; BIC / SWIFT: `OCBCSGSG`
**Expected Result:** Error banner displayed: "You've already added this bank account. You can add more currencies to it instead."
**Priority:** High
**Requirement Reference:** AC-6; BR-3b; ERR-8
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-61
**Name:** Withdrawal Accounts - Add Bank Account - Duplicate account fields highlighted red with auto-scroll
**Test Scenario:** Verify that when a duplicate account is detected, the Account Number / IBAN and BIC / SWIFT fields are highlighted in red and the page auto-scrolls to those fields.
**Test Case Type:** Negative
**Pre-requisites:** Logged in as a verified Active member with an existing Active bank account with Account Number `GB29NWBK60161331926819` and BIC / SWIFT `OCBCSGSG`.
**Steps:**
1. Navigate to Add Bank Account form.
2. Enter the same Account Number / IBAN and BIC / SWIFT as the existing Active account.
3. Fill in all other required fields with valid data.
4. Tap Continue.
5. Observe the field highlighting and scroll position.
**Test Data:** Account Number / IBAN: `GB29NWBK60161331926819`; BIC / SWIFT: `OCBCSGSG`
**Expected Result:** The Account Number / IBAN and BIC / SWIFT fields are highlighted in red; the form auto-scrolls to bring those fields into view.
**Priority:** Medium
**Requirement Reference:** AC-6; BR-3b
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-62
**Name:** Withdrawal Accounts - Add Bank Account - Duplicate of Disabled account - Error displayed
**Test Scenario:** Verify that submitting an account matching a Disabled bank account for the same member shows the correct error.
**Test Case Type:** Negative
**Pre-requisites:** Logged in as a verified Active member with an existing Disabled bank account with Account Number `GB29NWBK60161331926820` and BIC / SWIFT `OCBCSGSG`.
**Steps:**
1. Navigate to Add Bank Account form.
2. Enter the same Account Number / IBAN and BIC / SWIFT as the Disabled account.
3. Fill in all other required fields with valid data.
4. Tap Continue.
5. Observe the error displayed.
**Test Data:** Account Number / IBAN: `GB29NWBK60161331926820`; BIC / SWIFT: `OCBCSGSG`
**Expected Result:** Error displayed: "This bank account can't be added. Please contact support for assistance."
**Priority:** High
**Requirement Reference:** BR-3b; ERR-9
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-63
**Name:** Withdrawal Accounts - Add Bank Account - Account limit reached - Cannot submit
**Test Scenario:** Verify that a member who has reached the 5-account limit cannot submit a new bank account.
**Test Case Type:** Boundary
**Pre-requisites:** Logged in as a verified Active member with exactly 5 Active bank accounts.
**Steps:**
1. Navigate to Add Bank Account form (access via URL or deep link if CTA is disabled).
2. Fill in all required fields with valid data.
3. Tap Continue.
4. Observe the behavior.
**Test Data:** —
**Expected Result:** The Continue CTA does not advance the flow; submission is blocked and a message indicating the 5-account limit is shown.
**Priority:** High
**Requirement Reference:** AC-8; BR-3b; ERR-13
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-64
**Name:** Withdrawal Accounts - Review Bank Account - All values displayed correctly
**Test Scenario:** Verify that all values entered in the Add Bank Account form are displayed correctly on the Review Bank Account screen in read-only format.
**Test Case Type:** Display / UI
**Pre-requisites:** Logged in as a verified Active member; all required fields filled on the Add Bank Account form; Continue tapped successfully.
**Steps:**
1. Fill in all required fields on the Add Bank Account form with specific test data.
2. Tap Continue.
3. On the Review Bank Account screen, observe all displayed values.
**Test Data:** Label: `My OCBC SGD`; Bank Country: Singapore; Bank Name: `OCBC`; Account Holder Name: `John Smith`; Account Number: `GB29NWBK60161331926819`; BIC: `OCBCSGSG`; Currency: SGD; Address Line 1: `123 Orchard Road`; City: `Singapore`
**Expected Result:** All entered values are displayed exactly as entered on the Review screen in a read-only format.
**Priority:** High
**Requirement Reference:** BR-4
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-65
**Name:** Withdrawal Accounts - Review Bank Account - Back button - Returns to form with values retained
**Test Scenario:** Verify that tapping Back on the Review Bank Account screen returns to the Add Bank Account form with all previously entered values retained.
**Test Case Type:** Navigation / Screen Flow
**Pre-requisites:** Logged in as a verified Active member on the Review Bank Account screen.
**Steps:**
1. Fill in all required fields on the Add Bank Account form.
2. Tap Continue to reach the Review Bank Account screen.
3. Tap Back.
4. Observe the Add Bank Account form and its field values.
**Test Data:** Label: `Test Retention`; Bank Country: Singapore; Bank Name: `Test Bank`; Account Holder Name: `Jane Doe`; Account Number: `SG12TEST12345`; BIC: `OCBCSGSG`; Currency: SGD; Address Line 1: `1 Test Street`; City: `Singapore`
**Expected Result:** The Add Bank Account form is displayed with all previously entered values intact.
**Priority:** High
**Requirement Reference:** BR-4
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**


---

## AO-923_TC-66
**Name:** Withdrawal Accounts - Review Bank Account - Submit - Email OTP flow initiated
**Test Scenario:** Verify that the Email OTP verification screen is displayed after Submit is confirmed on the Review Bank Account screen.
**Test Case Type:** Navigation / Screen Flow
**Pre-requisites:** Logged in as a verified Active member on the Review Bank Account screen.
**Steps:**
1. Complete the Add Bank Account form and reach the Review screen.
2. Tap Submit.
3. Observe the screen displayed and whether an OTP email is triggered.
**Test Data:** —
**Expected Result:** The Email OTP verification screen is displayed.
**Priority:** High
**Requirement Reference:** BR-4
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-67
**Name:** Withdrawal Accounts - Email OTP - OTP sent to registered email on Submit
**Test Scenario:** Verify that a 6-digit OTP email is sent to the member's registered email address when Submit is tapped on the Review screen.
**Test Case Type:** Happy Path
**Pre-requisites:** Logged in as a verified Active member; access to the registered test email inbox.
**Steps:**
1. Complete the Add Bank Account form and tap Submit on Review screen.
2. Check the member's registered email inbox.
3. Observe whether an OTP email has been received.
**Test Data:** —
**Expected Result:** A 6-digit OTP email is received in the member's registered email inbox.
**Priority:** High
**Requirement Reference:** AC-7; BR-5; BR-7
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-68
**Name:** Withdrawal Accounts - Email OTP - Correct OTP - Account created Active and immediately usable
**Test Scenario:** Verify that entering the correct OTP creates the bank account with Active status, the account appears in the listing, and all selected currencies are immediately available for Fiat Withdrawal.
**Test Case Type:** Happy Path
**Pre-requisites:** Logged in as a verified Active member; OTP email received in registered inbox.
**Steps:**
1. Complete the Add Bank Account form (select currencies: SGD, USD) and reach OTP screen.
2. Enter the correct 6-digit OTP from the registered email.
3. Observe the screen after OTP submission.
4. Navigate to My Account → Withdrawal Accounts → Linked Bank Accounts.
5. Observe the new account in the listing.
6. Navigate to Withdrawal → Fiat → Bank Account and observe available accounts.
**Test Data:** Correct OTP from registered email; Currencies: SGD, USD
**Expected Result:** The bank account is created with Active status, is visible in the listing with Active status, and all selected currencies (SGD, USD) are immediately available in the Fiat Withdrawal destination list.
**Priority:** High
**Requirement Reference:** AC-7; BR-5
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-69
**Name:** Withdrawal Accounts - Email OTP - Incorrect OTP - Error shown, retry allowed
**Test Scenario:** Verify that entering an incorrect OTP displays an error and allows the member to retry.
**Test Case Type:** Negative
**Pre-requisites:** Logged in as a verified Active member on the OTP verification screen.
**Steps:**
1. Complete the Add Bank Account form and reach the OTP screen.
2. Enter an incorrect OTP.
3. Observe the error displayed and whether the OTP field allows another attempt.
**Test Data:** Incorrect OTP: `000000`
**Expected Result:** An error message is displayed indicating the OTP is incorrect; the OTP input field remains active for another attempt.
**Priority:** High
**Requirement Reference:** BR-5
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-70
**Name:** Withdrawal Accounts - Email OTP - Expired OTP - Member must request new OTP
**Test Scenario:** Verify that an expired OTP is rejected and the member must request a new OTP to proceed.
**Test Case Type:** Negative
**Pre-requisites:** Logged in as a verified Active member on the OTP verification screen; wait for the OTP to expire before entering it.
**Steps:**
1. Complete the Add Bank Account form and reach the OTP screen.
2. Wait until the OTP expiry indicator on screen shows the OTP has expired (do not enter the OTP before this point).
3. Enter the expired OTP.
4. Observe the error displayed.
**Test Data:** Expired OTP (obtained from the registered email, entered after expiry)
**Expected Result:** Error is displayed indicating the OTP has expired; member is prompted to request a new OTP.
**Priority:** High
**Requirement Reference:** BR-5
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-71
**Name:** Withdrawal Accounts - Email OTP - Multiple incorrect attempts - OTP invalidated after limit
**Test Scenario:** Verify that the OTP is invalidated after the maximum number of incorrect attempts is reached and the member must request a new OTP.
**Test Case Type:** Boundary
**Pre-requisites:** Logged in as a verified Active member on the OTP verification screen.
**Steps:**
1. Complete the Add Bank Account form and reach the OTP screen.
2. Enter an incorrect OTP repeatedly until the maximum attempt limit is reached.
3. Observe the behavior after the final incorrect attempt.
**Test Data:** Incorrect OTP: `000000` (repeat until locked out)
**Expected Result:** After reaching the attempt limit, the current OTP is invalidated; member is prompted to request a new OTP and cannot use the invalidated OTP.
**Priority:** High
**Requirement Reference:** BR-5
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**


---

## AO-923_TC-72
**Name:** Withdrawal Accounts - Email OTP - Resend OTP - New OTP sent, old OTP invalidated
**Test Scenario:** Verify that requesting a new OTP sends a fresh OTP and invalidates the previously issued OTP.
**Test Case Type:** Negative
**Pre-requisites:** Logged in as a verified Active member on the OTP verification screen; original OTP received in email inbox.
**Steps:**
1. Complete the Add Bank Account form and reach the OTP screen.
2. Note the original OTP from the registered email.
3. Tap the Resend OTP CTA.
4. Enter the original OTP.
5. Observe whether the original OTP is accepted.
**Test Data:** Original OTP (from first email, entered after resend)
**Expected Result:** The original OTP is rejected; a new OTP has been sent to the registered email and only the new OTP is valid.
**Priority:** High
**Requirement Reference:** BR-5
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-73
**Name:** Withdrawal Accounts - Email OTP - OTP screen UI elements displayed correctly
**Test Scenario:** Verify that the OTP verification screen displays the correct UI elements.
**Test Case Type:** Display / UI
**Pre-requisites:** Logged in as a verified Active member; Add Bank Account form completed; on OTP verification screen.
**Steps:**
1. Complete the Add Bank Account form and reach the OTP screen.
2. Observe all UI elements present on the screen.
**Test Data:** —
**Expected Result:** OTP verification screen displays: OTP input field, Resend OTP CTA, and expiry indicator (timer or expiry notice).
**Priority:** Medium
**Requirement Reference:** BR-5
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-74
**Name:** Withdrawal Accounts - Email OTP - Back button - Returns to Review screen with values retained
**Test Scenario:** Verify that tapping Back on the OTP verification screen returns to the Review Bank Account screen with all values retained.
**Test Case Type:** Navigation / Screen Flow
**Pre-requisites:** Logged in as a verified Active member on the OTP verification screen.
**Steps:**
1. Complete the Add Bank Account form, pass Review, and reach the OTP screen.
2. Tap Back.
3. Observe the screen displayed and field values.
**Test Data:** —
**Expected Result:** The Review Bank Account screen is displayed with all previously entered values intact.
**Priority:** High
**Requirement Reference:** BR-5
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-75
**Name:** Withdrawal Accounts - Post-Add - New account appears in listing as Active
**Test Scenario:** Verify that the newly added bank account appears in the Linked Bank Accounts listing with Active status immediately after successful OTP verification.
**Test Case Type:** Happy Path
**Pre-requisites:** Logged in as a verified Active member; OTP verification completed successfully.
**Steps:**
1. Complete the Add Bank Account flow including OTP verification.
2. Navigate to My Account → Withdrawal Accounts → Linked Bank Accounts.
3. Observe the listing.
**Test Data:** —
**Expected Result:** The newly added account appears at the top of the listing with Active status.
**Priority:** High
**Requirement Reference:** AC-7; BR-5; BR-2
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-76
**Name:** Withdrawal Accounts - Notifications - Confirmation email sent after bank account addition
**Test Scenario:** Verify that a confirmation email is sent to the member's registered email address after successfully adding a bank account.
**Test Case Type:** Happy Path
**Pre-requisites:** Logged in as a verified Active member; access to registered test email inbox.
**Steps:**
1. Complete the Add Bank Account flow including OTP verification.
2. Check the registered email inbox.
3. Observe whether a bank account confirmation email has been received.
**Test Data:** —
**Expected Result:** A confirmation email is received in the registered email inbox confirming the bank account was added.
**Priority:** High
**Requirement Reference:** AC-18; BR-7
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**


---

## AO-923_TC-77
**Name:** Withdrawal Accounts - Notifications - No email sent when currency added to existing account
**Test Scenario:** Verify that no email notification is sent when a currency is added to an existing bank account.
**Test Case Type:** Negative
**Pre-requisites:** Logged in as a verified Active member with at least one Active bank account; access to registered email inbox.
**Steps:**
1. Navigate to Bank Account Details for an existing Active account.
2. Add a new currency to the account.
3. Save the change.
4. Check the registered email inbox.
5. Observe whether a notification email was sent.
**Test Data:** —
**Expected Result:** No email notification is received for the currency addition.
**Priority:** Medium
**Requirement Reference:** AC-18; BR-7
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-78
**Name:** Withdrawal Accounts - Notifications - No email sent when currency removed from existing account
**Test Scenario:** Verify that no email notification is sent when a currency is removed from an existing bank account.
**Test Case Type:** Negative
**Pre-requisites:** Logged in as a verified Active member with an Active bank account containing at least two currencies; access to registered email inbox.
**Steps:**
1. Navigate to Bank Account Details for an Active account with two or more currencies.
2. Remove one currency and save.
3. Check the registered email inbox.
4. Observe whether a notification email was sent.
**Test Data:** —
**Expected Result:** No email notification is received for the currency removal.
**Priority:** Medium
**Requirement Reference:** AC-18; BR-7
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-79
**Name:** Withdrawal Accounts - Bank Account Details - Full Account Number IBAN displayed unmasked
**Test Scenario:** Verify that the Bank Account Details page for an Active account displays the full (unmasked) Account Number / IBAN.
**Test Case Type:** Display / UI
**Pre-requisites:** Logged in as a verified Active member; Active bank account with a known Account Number / IBAN.
**Steps:**
1. Navigate to My Account → Withdrawal Accounts → Linked Bank Accounts.
2. Tap an Active account.
3. Observe the Account Number / IBAN displayed on the Details page.
**Test Data:** `GB29NWBK60161331926819`
**Expected Result:** The full Account Number / IBAN is displayed without masking.
**Priority:** High
**Requirement Reference:** BR-2
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-80
**Name:** Withdrawal Accounts - Bank Account Details - Active account - Edit CTAs visible
**Test Scenario:** Verify that the Bank Account Details page for an Active account displays the correct screen title and all available edit CTAs (Edit Label, Add/Remove Currency, Delete).
**Test Case Type:** Display / UI
**Pre-requisites:** Logged in as a verified Active member with at least one Active bank account.
**Steps:**
1. Navigate to My Account → Withdrawal Accounts → Linked Bank Accounts.
2. Tap an Active account.
3. Observe the screen title and available CTAs.
**Test Data:** —
**Expected Result:** Bank Account Details page displays the account details and edit CTAs for Edit Label, currency management, and Delete Bank Account.
**Priority:** Medium
**Requirement Reference:** BR-2
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-81
**Name:** Withdrawal Accounts - Edit Label - Valid new label saved successfully
**Test Scenario:** Verify that a member can edit the Label of an existing Active bank account and the new label is saved successfully.
**Test Case Type:** Happy Path
**Pre-requisites:** Logged in as a verified Active member on the Bank Account Details page of an Active account.
**Steps:**
1. Navigate to Bank Account Details of an Active account.
2. Tap Edit Label (or the Label field).
3. Clear the existing Label and enter a new valid label.
4. Save the change.
5. Observe the Label displayed on the Details page.
**Test Data:** New Label: `Updated Label`
**Expected Result:** The Label is updated to "Updated Label" and the new value is displayed on the Bank Account Details page.
**Priority:** High
**Requirement Reference:** AC-12; BR-6
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-82
**Name:** Withdrawal Accounts - Edit Label - Empty label error
**Test Scenario:** Verify that the Label field validation error is displayed when the Label is empty on the Edit Label screen.
**Test Case Type:** Validation
**Pre-requisites:** Logged in as a verified Active member on the Edit Label screen.
**Steps:**
1. Navigate to Edit Label for an Active account.
2. Clear the Label field.
3. Tap Save.
4. Observe the error displayed.
**Test Data:** Label: (empty)
**Expected Result:** Validation error displayed: "Please enter a label."
**Priority:** High
**Requirement Reference:** BR-6; ERR-D1
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-83
**Name:** Withdrawal Accounts - Edit Label - Label exceeds 30 characters error
**Test Scenario:** Verify that the Label field validation error is displayed when the Label exceeds 30 characters on the Edit Label screen.
**Test Case Type:** Boundary
**Pre-requisites:** Logged in as a verified Active member on the Edit Label screen.
**Steps:**
1. Navigate to Edit Label for an Active account.
2. Enter a 31-character string in the Label field.
3. Tap Save.
4. Observe the error displayed.
**Test Data:** `AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA` (31 characters)
**Expected Result:** Validation error displayed: "Label cannot exceed 30 characters."
**Priority:** Medium
**Requirement Reference:** BR-6; ERR-D2
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**


---

## AO-923_TC-84
**Name:** Withdrawal Accounts - Add Currency - Currency added without OTP and immediately usable
**Test Scenario:** Verify that a member can add a new currency to an existing Active bank account without Email OTP, and the currency is immediately available for Fiat Withdrawal.
**Test Case Type:** Happy Path
**Pre-requisites:** Logged in as a verified Active member with an Active bank account that does not yet have USD as a currency.
**Steps:**
1. Navigate to Bank Account Details of an Active account.
2. Add USD as a new currency.
3. Save the change (no OTP required).
4. Navigate to Withdrawal → Fiat → Bank Account.
5. Select the updated account and observe available currencies.
**Test Data:** Currency to add: USD
**Expected Result:** USD is added to the account with no OTP required; USD is immediately available as a withdrawal currency for this account.
**Priority:** High
**Requirement Reference:** AC-13; BR-6
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-85
**Name:** Withdrawal Accounts - Add Currency - Newly added currency visible in Bank Account Details
**Test Scenario:** Verify that a newly added currency appears in the currency list on the Bank Account Details page immediately after saving.
**Test Case Type:** Happy Path
**Pre-requisites:** Logged in as a verified Active member; Active bank account without EUR currency.
**Steps:**
1. Navigate to Bank Account Details of an Active account.
2. Add EUR as a new currency and save.
3. Observe the currency list on the Bank Account Details page.
**Test Data:** Currency to add: EUR
**Expected Result:** EUR is displayed in the currency list on the Bank Account Details page.
**Priority:** Medium
**Requirement Reference:** AC-13; BR-6
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-86
**Name:** Withdrawal Accounts - Remove Currency - Currency removed without OTP
**Test Scenario:** Verify that a member can remove a currency from an Active bank account without Email OTP and the currency is no longer available for withdrawal.
**Test Case Type:** Happy Path
**Pre-requisites:** Logged in as a verified Active member with an Active bank account containing at least two currencies (SGD and USD), no pending withdrawals for the currency to be removed.
**Steps:**
1. Navigate to Bank Account Details of an Active account with SGD and USD.
2. Remove USD from the currency list.
3. Save the change.
4. Navigate to Withdrawal → Fiat → Bank Account and select this account.
5. Observe available currencies.
**Test Data:** Currency to remove: USD
**Expected Result:** USD is removed from the account without OTP; USD is no longer available as a withdrawal currency for this account.
**Priority:** High
**Requirement Reference:** AC-14; BR-6
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-87
**Name:** Withdrawal Accounts - Remove Currency - Blocked when pending withdrawal for that currency
**Test Scenario:** Verify that currency removal is blocked when there is a pending withdrawal associated with that currency and bank account.
**Test Case Type:** Negative
**Pre-requisites:** Logged in as a verified Active member with an Active bank account that has a pending withdrawal for USD.
**Steps:**
1. Navigate to Bank Account Details of the Active account with pending USD withdrawal.
2. Attempt to remove USD from the currency list.
3. Tap Save.
4. Observe the error displayed.
**Test Data:** Currency: USD (with pending withdrawal)
**Expected Result:** Error displayed: "You have a USD withdrawal in progress to this account. You can remove it once that withdrawal is complete."
**Priority:** High
**Requirement Reference:** AC-14; BR-6; ERR-11
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-88
**Name:** Withdrawal Accounts - Remove Currency - Save button disabled when last currency deselected
**Test Scenario:** Verify that the Save changes button is disabled when the member deselects the last remaining currency on a bank account.
**Test Case Type:** Negative
**Pre-requisites:** Logged in as a verified Active member with an Active bank account containing exactly one currency (SGD).
**Steps:**
1. Navigate to Bank Account Details of an Active account with only SGD.
2. Deselect SGD (attempt to remove the last currency).
3. Observe the state of the Save changes button.
**Test Data:** Account with single currency: SGD
**Expected Result:** The Save changes button is disabled; the member cannot save with zero currencies selected.
**Priority:** High
**Requirement Reference:** AC-15; BR-6
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-89
**Name:** Withdrawal Accounts - Remove Currency - Add remove currency blocked on Disabled account
**Test Scenario:** Verify that attempting to add or remove a currency on a Disabled bank account displays the correct error.
**Test Case Type:** Negative
**Pre-requisites:** Logged in as a verified Active member with a Disabled bank account.
**Steps:**
1. Navigate to the Disabled account's details page. (Note: BR-2 states Disabled rows are non-clickable in the listing; confirm with the team whether the details page is accessible via a different entry path — e.g. direct URL or admin toggle — before executing this TC.)
2. Attempt to modify the currency list.
3. Observe the error displayed.
**Test Data:** —
**Expected Result:** Error displayed: "This bank account is suspended. Please contact support for assistance."
**Priority:** Medium
**Requirement Reference:** BR-6; ERR-12
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**


---

## AO-923_TC-90
**Name:** Withdrawal Accounts - Delete Bank Account - Confirmation dialog content correct
**Test Scenario:** Verify that tapping Delete Bank Account displays the confirmation dialog with the correct header, message, and CTAs.
**Test Case Type:** Display / UI
**Pre-requisites:** Logged in as a verified Active member on the Bank Account Details page of an Active account with no pending withdrawals.
**Steps:**
1. Navigate to Bank Account Details of an Active account.
2. Tap Delete Bank Account.
3. Observe the dialog displayed.
**Test Data:** —
**Expected Result:** Confirmation dialog displayed with: Header "Delete bank account?"; Message "Removing this bank account will prevent it from being used for future withdrawals. This action won't affect completed transactions."; CTAs: Delete and Cancel.
**Priority:** High
**Requirement Reference:** AC-16; BR-6
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-91
**Name:** Withdrawal Accounts - Delete Bank Account - Cancel - Account not deleted
**Test Scenario:** Verify that the delete confirmation dialog is dismissed and the account remains Active when Cancel is selected.
**Test Case Type:** Negative
**Pre-requisites:** Logged in as a verified Active member; delete confirmation dialog is displayed.
**Steps:**
1. Navigate to Bank Account Details of an Active account.
2. Tap Delete Bank Account to display the confirmation dialog.
3. Tap Cancel.
4. Observe the screen and account status.
**Test Data:** —
**Expected Result:** The dialog is dismissed; the account remains in Active status and is still visible in the listing.
**Priority:** High
**Requirement Reference:** AC-16; BR-6
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-92
**Name:** Withdrawal Accounts - Delete Bank Account - Delete confirmed - Account removed from listing and unavailable for withdrawal
**Test Scenario:** Verify that confirming Delete removes the account from the member's listing, makes it immediately unavailable for Fiat Withdrawal, and requires no Email OTP.
**Test Case Type:** Happy Path
**Pre-requisites:** Logged in as a verified Active member with an Active bank account; no pending withdrawals for this account.
**Steps:**
1. Navigate to Bank Account Details of an Active account.
2. Tap Delete Bank Account and confirm by tapping Delete.
3. Observe whether OTP is required.
4. Navigate to My Account → Withdrawal Accounts → Linked Bank Accounts.
5. Observe the listing.
6. Navigate to Withdrawal → Fiat → Bank Account.
7. Observe the available destination accounts.
**Test Data:** —
**Expected Result:** The account is deleted without OTP; it is absent from the Linked Bank Accounts listing and from the Fiat Withdrawal destination list.
**Priority:** High
**Requirement Reference:** AC-16; BR-6
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-93
**Name:** Withdrawal Accounts - Delete Bank Account - Blocked when pending withdrawal exists
**Test Scenario:** Verify that deleting a bank account is blocked when there is a pending withdrawal associated with that account.
**Test Case Type:** Negative
**Pre-requisites:** Logged in as a verified Active member with an Active bank account that has a pending withdrawal.
**Steps:**
1. Navigate to Bank Account Details of an Active account with a pending withdrawal.
2. Tap Delete Bank Account.
3. Confirm the deletion by tapping Delete in the dialog.
4. Observe the error displayed.
**Test Data:** Active account with a pending withdrawal.
**Expected Result:** Error displayed: "You have a withdrawal in progress to this account. You can remove it once that withdrawal is complete."
**Priority:** High
**Requirement Reference:** AC-16; BR-6; ERR-14
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-95
**Name:** Withdrawal Accounts - Delete Bank Account - Deleted account not visible in member listing
**Test Scenario:** Verify that a deleted bank account is no longer visible in the member's Linked Bank Accounts listing.
**Test Case Type:** Status Transition
**Pre-requisites:** Logged in as a verified Active member; a bank account has just been successfully deleted.
**Steps:**
1. Delete an Active bank account (confirm via dialog).
2. Navigate to My Account → Withdrawal Accounts → Linked Bank Accounts.
3. Observe the listing.
**Test Data:** —
**Expected Result:** The deleted account does not appear in the listing.
**Priority:** High
**Requirement Reference:** AC-17; BR-6
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-96
**Name:** Withdrawal Accounts - Delete Bank Account - Deleted record visible in Backoffice with Deleted status and Date Deleted
**Test Scenario:** Verify that a bank account deleted by the member remains visible in Backoffice under Withdrawal Account with status Deleted and a Date Deleted timestamp.
**Test Case Type:** Cross-System Sync
**Pre-requisites:** Logged in as a verified Active member (mobile app) and as a Maker in Backoffice; a bank account has been deleted by the member.
**Steps:**
1. Member deletes an Active bank account from the mobile app.
2. Log in to Backoffice as Maker.
3. Navigate to Member Management → Member → Member Details → Withdrawal Account.
4. Locate the deleted account record.
5. Observe the status and deletion information.
**Test Data:** —
**Expected Result:** The deleted account record is visible in Backoffice with status "Deleted" and a Date Deleted timestamp present and accurate.
**Priority:** High
**Requirement Reference:** AC-17; BR-6; BR-8
**Configuration:** OTC Mobile App / Backoffice
**Login Method:** Mobile App (member) + Backoffice (Maker)
**Story:** AO-923
**Automation:**

---

## AO-923_TC-97
**Name:** Withdrawal Accounts - Disabled Account - Visible in listing
**Test Scenario:** Verify that a Disabled bank account is visible (not hidden) in the member's Linked Bank Accounts listing.
**Test Case Type:** Status Transition
**Pre-requisites:** Logged in as a verified Active member with at least one Disabled bank account (set by Backoffice).
**Steps:**
1. Navigate to My Account → Withdrawal Accounts → Linked Bank Accounts.
2. Observe the listing.
**Test Data:** —
**Expected Result:** The Disabled account is visible in the listing, displayed after Active accounts.
**Priority:** Medium
**Requirement Reference:** AC-11; BR-2
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-99
**Name:** Withdrawal Accounts - Disabled Account - Cannot be used for Fiat Withdrawal
**Test Scenario:** Verify that a Disabled bank account is not available as a destination in the Fiat Withdrawal flow.
**Test Case Type:** Negative
**Pre-requisites:** Logged in as a verified Active member with a Disabled bank account and at least one Active bank account.
**Steps:**
1. Navigate to Withdrawal → Fiat → Bank Account.
2. Observe the list of available destination accounts.
**Test Data:** —
**Expected Result:** The Disabled bank account does not appear as a selectable destination in the Fiat Withdrawal flow.
**Priority:** High
**Requirement Reference:** BR-1
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-100
**Name:** Withdrawal Accounts - Edit - Non-Label non-currency fields cannot be edited
**Test Scenario:** Verify that fields other than Label and Currencies (e.g. Bank Name, Account Number, BIC) cannot be edited from the Bank Account Details page.
**Test Case Type:** Negative
**Pre-requisites:** Logged in as a verified Active member on the Bank Account Details page of an Active account.
**Steps:**
1. Navigate to Bank Account Details of an Active account.
2. Observe whether edit controls (input field, edit icon, or edit CTA) are present for fields such as Bank Name, Account Number / IBAN, BIC / SWIFT, Address Line 1.
**Test Data:** —
**Expected Result:** No edit controls are present for any field other than Label and Currencies; those fields are read-only.
**Priority:** High
**Requirement Reference:** OOS-5
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**


---

## AO-923_TC-101
**Name:** Withdrawal Accounts - Backoffice - Maker can view all bank account fields
**Test Scenario:** Verify that a Maker in Backoffice can view all required bank account fields under Member Details → Withdrawal Account.
**Test Case Type:** Cross-System Sync
**Pre-requisites:** An Active bank account exists for a member; logged in as Maker in Backoffice.
**Steps:**
1. Log in to Backoffice as Maker.
2. Navigate to Member Management → Member → Member Details → Withdrawal Account.
3. Locate the member's Active bank account.
4. Observe all fields displayed.
**Test Data:** —
**Expected Result:** All BR-3 fields are visible: Label, Bank Country, Bank Name, Account Holder Name, Account Number / IBAN, BIC / SWIFT, Bank Code / Routing Number, Account Type, Currency list, Address Line 1, Address Line 2, City, Postal Code.
**Priority:** High
**Requirement Reference:** AC-19; BR-8
**Configuration:** Backoffice
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-102
**Name:** Withdrawal Accounts - Backoffice - Full Account Number IBAN unmasked for Maker
**Test Scenario:** Verify that the full (unmasked) Account Number / IBAN is visible to Maker in Backoffice.
**Test Case Type:** Cross-System Sync
**Pre-requisites:** An Active bank account with a known Account Number exists; logged in as Maker in Backoffice.
**Steps:**
1. Log in to Backoffice as Maker.
2. Navigate to Member Management → Member → Member Details → Withdrawal Account.
3. Locate the bank account record.
4. Observe the Account Number / IBAN displayed.
**Test Data:** Account Number / IBAN: `GB29NWBK60161331926819`
**Expected Result:** The full Account Number / IBAN `GB29NWBK60161331926819` is displayed without masking.
**Priority:** High
**Requirement Reference:** AC-19; BR-8
**Configuration:** Backoffice
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-103
**Name:** Withdrawal Accounts - Backoffice - Currency list per account visible
**Test Scenario:** Verify that the currency list associated with a bank account is visible to Maker in Backoffice.
**Test Case Type:** Cross-System Sync
**Pre-requisites:** An Active bank account with multiple currencies (SGD, USD) exists; logged in as Maker in Backoffice.
**Steps:**
1. Log in to Backoffice as Maker.
2. Navigate to Member Management → Member → Member Details → Withdrawal Account.
3. Locate the bank account with SGD and USD.
4. Observe the currency list displayed.
**Test Data:** Account with currencies: SGD, USD
**Expected Result:** Both SGD and USD are listed under the bank account record in Backoffice.
**Priority:** High
**Requirement Reference:** BR-8
**Configuration:** Backoffice
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-104
**Name:** Withdrawal Accounts - Backoffice - Active Disabled and Deleted records all visible
**Test Scenario:** Verify that Active, Disabled, and Deleted bank account records are all visible to Maker in Backoffice under Withdrawal Account.
**Test Case Type:** Cross-System Sync
**Pre-requisites:** A member with one Active, one Disabled, and one Deleted bank account exists; logged in as Maker in Backoffice.
**Steps:**
1. Log in to Backoffice as Maker.
2. Navigate to Member Management → Member → Member Details → Withdrawal Account.
3. Observe the records listed.
**Test Data:** —
**Expected Result:** All three records are visible: one Active, one Disabled, one Deleted — each with its correct status shown.
**Priority:** High
**Requirement Reference:** BR-8
**Configuration:** Backoffice
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-107
**Name:** Withdrawal Accounts - Add Bank Account - Back from form returns to listing
**Test Scenario:** Verify that tapping Back on the Add Bank Account form returns the member to the Linked Bank Accounts listing screen.
**Test Case Type:** Navigation / Screen Flow
**Pre-requisites:** Logged in as a verified Active member on the Add Bank Account form.
**Steps:**
1. Navigate to Add Bank Account form.
2. Partially fill in some fields.
3. Tap Back.
4. Observe the screen displayed.
**Test Data:** —
**Expected Result:** The Linked Bank Accounts listing screen is displayed.
**Priority:** Medium
**Requirement Reference:** BR-3
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-108
**Name:** Withdrawal Accounts - Review Bank Account - Back preserves all form values
**Test Scenario:** Verify that tapping Back on the Review Bank Account screen returns to the Add Bank Account form with all values retained.
**Test Case Type:** Navigation / Screen Flow
**Pre-requisites:** Logged in as a verified Active member on the Review Bank Account screen.
**Steps:**
1. Fill in all required fields on the Add Bank Account form with specific test data.
2. Tap Continue to reach the Review screen.
3. Tap Back.
4. Observe the Add Bank Account form and all field values.
**Test Data:** Label: `Test Label`; Bank Country: Singapore; Bank Name: `Test Bank`; Account Holder Name: `Jane Doe`; Account Number: `SG12TEST12345`; BIC: `OCBCSGSG`; Currency: SGD; Address Line 1: `1 Test Street`; City: `Singapore`
**Expected Result:** The Add Bank Account form is displayed with all entered values exactly as entered before navigating to Review.
**Priority:** High
**Requirement Reference:** BR-4
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-109
**Name:** Withdrawal Accounts - OTP - Back returns to Review screen with values retained
**Test Scenario:** Verify that tapping Back on the OTP verification screen returns to the Review Bank Account screen with all values retained.
**Test Case Type:** Navigation / Screen Flow
**Pre-requisites:** Logged in as a verified Active member on the OTP verification screen.
**Steps:**
1. Complete the Add Bank Account form and Review screen to reach the OTP screen.
2. Tap Back on the OTP screen.
3. Observe the screen displayed and the values shown.
**Test Data:** —
**Expected Result:** The Review Bank Account screen is displayed with all previously entered values intact.
**Priority:** High
**Requirement Reference:** BR-5
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-110
**Name:** Withdrawal Accounts - Mobile Lifecycle - Background during form fill - Data retained on resume
**Test Scenario:** Verify that backgrounding the app during Add Bank Account form fill retains all entered data when the app is resumed.
**Test Case Type:** Mobile App Lifecycle
**Pre-requisites:** Logged in as a verified Active member; Add Bank Account form partially filled.
**Steps:**
1. Navigate to Add Bank Account form and fill in several fields with test data.
2. Background the app (press home button).
3. Wait 30 seconds.
4. Reopen the app and navigate back to the Add Bank Account form.
5. Observe the field values.
**Test Data:** Label: `My Bank`; Bank Country: Singapore; Bank Name: `OCBC`
**Expected Result:** All previously entered field values are retained after resuming from background.
**Priority:** Medium
**Requirement Reference:** BR-3
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-111
**Name:** Withdrawal Accounts - Mobile Lifecycle - Kill app during form fill - Form cleared on reopen
**Test Scenario:** Verify that force-closing the app during Add Bank Account form fill clears the form when the app is reopened.
**Test Case Type:** Mobile App Lifecycle
**Pre-requisites:** Logged in as a verified Active member; Add Bank Account form partially filled.
**Steps:**
1. Navigate to Add Bank Account form and fill in several fields.
2. Force-kill the app.
3. Reopen the app and navigate to Add Bank Account.
4. Observe the field values.
**Test Data:** —
**Expected Result:** The Add Bank Account form is empty (reset); no previously entered data is retained after a force-kill.
**Priority:** Medium
**Requirement Reference:** BR-3
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-112
**Name:** Withdrawal Accounts - Mobile Lifecycle - Background during OTP - Timer continues server-side
**Test Scenario:** Verify that backgrounding the app during OTP verification does not reset the OTP timer; the OTP remains valid on resume if still within its validity window, and is expired if the window has passed.
**Test Case Type:** Mobile App Lifecycle
**Pre-requisites:** Logged in as a verified Active member on the OTP verification screen; OTP received in registered email inbox.
**Steps:**
1. Reach the OTP verification screen.
2. Background the app immediately after the OTP is received.
3. Resume the app within the OTP validity window.
4. Enter the OTP.
5. Observe the result.
6. Repeat: background app until OTP expires, then re-enter.
**Test Data:** —
**Expected Result:** (1) When resumed within the validity window: OTP is accepted and account is created. (2) When resumed after the window has expired: OTP is rejected with an expiry error; member must request a new OTP.
**Priority:** High
**Requirement Reference:** BR-5
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**


---

## AO-923_TC-113
**Name:** Withdrawal Accounts - Mobile Lifecycle - Kill app on Review screen - No account created
**Test Scenario:** Verify that force-closing the app on the Review Bank Account screen does not create a bank account record.
**Test Case Type:** Mobile App Lifecycle
**Pre-requisites:** Logged in as a verified Active member on the Review Bank Account screen.
**Steps:**
1. Complete the Add Bank Account form and reach the Review screen.
2. Force-kill the app without tapping Submit.
3. Reopen the app.
4. Navigate to My Account → Withdrawal Accounts → Linked Bank Accounts.
5. Observe the listing.
**Test Data:** —
**Expected Result:** No new bank account record has been created; the listing is unchanged from before.
**Priority:** High
**Requirement Reference:** BR-4
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-114
**Name:** Withdrawal Accounts - Mobile Lifecycle - Kill app during edit - Unsaved changes discarded
**Test Scenario:** Verify that force-closing the app during an edit (Label or currency change) discards unsaved changes.
**Test Case Type:** Mobile App Lifecycle
**Pre-requisites:** Logged in as a verified Active member; unsaved edit in progress on Bank Account Details.
**Steps:**
1. Navigate to Bank Account Details of an Active account.
2. Change the Label to a new value but do not save.
3. Force-kill the app.
4. Reopen the app and navigate back to the Bank Account Details.
5. Observe the Label value.
**Test Data:** Unsaved new Label: `Unsaved Edit`
**Expected Result:** The Label retains its original value; the unsaved change is discarded.
**Priority:** Medium
**Requirement Reference:** BR-6
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-115
**Name:** Withdrawal Accounts - Mobile Lifecycle - Network interruption during OTP submission - Graceful error, no duplicate account
**Test Scenario:** Verify that a network interruption during OTP submission shows a graceful error and does not create a duplicate bank account record.
**Test Case Type:** Mobile App Lifecycle
**Pre-requisites:** Logged in as a verified Active member on the OTP verification screen; ability to simulate network interruption.
**Steps:**
1. Reach the OTP verification screen.
2. Enter the correct OTP.
3. Simulate a network interruption at the moment of submission (e.g. toggle airplane mode immediately after tapping confirm).
4. Restore network connectivity.
5. Observe the error displayed.
6. Navigate to My Account → Withdrawal Accounts → Linked Bank Accounts.
7. Observe the listing.
**Test Data:** —
**Expected Result:** A graceful error message is displayed indicating the submission failed; only one bank account record exists (no duplicate created).
**Priority:** High
**Requirement Reference:** BR-5
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-116
**Name:** Withdrawal Accounts - Account Limit - 4 accounts can add a 5th successfully
**Test Scenario:** Verify that a member with 4 Active bank accounts can successfully add a 5th account.
**Test Case Type:** Boundary
**Pre-requisites:** Logged in as a verified Active member with exactly 4 Active bank accounts.
**Steps:**
1. Navigate to My Account → Withdrawal Accounts → Linked Bank Accounts.
2. Tap Add Bank Account.
3. Complete the Add Bank Account flow including OTP verification.
4. Navigate back to the listing.
5. Observe the number of Active accounts.
**Test Data:** Label: `Account 5`; Bank Country: Singapore; Bank Name: `DBS`; Account Holder Name: `John Smith`; Account Number: `SG99DBS0000012345`; BIC: `DBSSSGSG`; Currency: SGD; Address Line 1: `1 Marina Blvd`; City: `Singapore`
**Expected Result:** The 5th bank account is created successfully with Active status; listing shows 5 Active accounts.
**Priority:** High
**Requirement Reference:** AC-8; BR-1
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-117
**Name:** Withdrawal Accounts - Account Limit - 5 accounts cannot add a 6th
**Test Scenario:** Verify that a member with 5 Active bank accounts cannot add a 6th account.
**Test Case Type:** Boundary
**Pre-requisites:** Logged in as a verified Active member with exactly 5 Active bank accounts.
**Steps:**
1. Navigate to My Account → Withdrawal Accounts → Linked Bank Accounts.
2. Observe the Add Bank Account CTA state.
3. Attempt to tap the Add Bank Account CTA.
**Test Data:** —
**Expected Result:** The Add Bank Account CTA is disabled; tapping it shows the toast: "You've reached the maximum of 5 bank accounts. Please remove one before adding another."
**Priority:** High
**Requirement Reference:** AC-8; BR-1
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**


---

## AO-923_TC-118
**Name:** Withdrawal Accounts - Account Limit - 5 Active plus 1 Disabled - Limit counted as 5
**Test Scenario:** Verify that a member with 5 Active and 1 Disabled bank account is counted at the limit of 5 (Disabled does not count), and the Add Bank Account CTA is disabled.
**Test Case Type:** Boundary
**Pre-requisites:** Logged in as a verified Active member with exactly 5 Active and 1 Disabled bank accounts.
**Steps:**
1. Navigate to My Account → Withdrawal Accounts → Linked Bank Accounts.
2. Observe the Add Bank Account CTA state.
**Test Data:** —
**Expected Result:** The Add Bank Account CTA is disabled (Active count = 5; Disabled account not counted toward limit).
**Priority:** High
**Requirement Reference:** AC-20; BR-1
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-119
**Name:** Withdrawal Accounts - Account Limit - 5 Active plus 1 Deleted - Limit counted as 5
**Test Scenario:** Verify that a member with 5 Active and 1 Deleted bank account is counted at the limit of 5 (Deleted does not count), and the Add Bank Account CTA is disabled.
**Test Case Type:** Boundary
**Pre-requisites:** Logged in as a verified Active member with exactly 5 Active bank accounts and 1 previously deleted account.
**Steps:**
1. Navigate to My Account → Withdrawal Accounts → Linked Bank Accounts.
2. Observe the Add Bank Account CTA state.
**Test Data:** —
**Expected Result:** The Add Bank Account CTA is disabled (Active count = 5; Deleted account not counted toward limit).
**Priority:** High
**Requirement Reference:** AC-20; BR-1
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-120
**Name:** Withdrawal Accounts - Account Limit - Delete frees limit slot immediately
**Test Scenario:** Verify that deleting one of 5 Active bank accounts immediately allows the member to add a new account.
**Test Case Type:** Boundary
**Pre-requisites:** Logged in as a verified Active member with exactly 5 Active bank accounts; no pending withdrawals on the account to be deleted.
**Steps:**
1. Navigate to My Account → Withdrawal Accounts → Linked Bank Accounts.
2. Verify the Add Bank Account CTA is disabled (5 accounts).
3. Delete one Active account (confirm via dialog).
4. Observe the Add Bank Account CTA state after deletion.
**Test Data:** —
**Expected Result:** After deletion, the Add Bank Account CTA is immediately enabled (Active count = 4).
**Priority:** High
**Requirement Reference:** BR-1
**Configuration:** OTC Mobile App
**Login Method:**
**Story:** AO-923
**Automation:**

---

## AO-923_TC-121
**Name:** Withdrawal Accounts - Backoffice - Deleted account visible with Deleted status and Date Deleted timestamp
**Test Scenario:** Verify that a bank account deleted by the member is visible in Backoffice with status Deleted and both the Deleted status label and Date Deleted timestamp are displayed correctly.
**Test Case Type:** Cross-System Sync
**Pre-requisites:** A member has deleted a bank account; logged in as Maker in Backoffice.
**Steps:**
1. Member deletes a bank account from the mobile app and notes the deletion date/time.
2. Log in to Backoffice as Maker.
3. Navigate to Member Management → Member → Member Details → Withdrawal Account.
4. Locate the deleted record.
5. Observe the status and Date Deleted fields.
**Test Data:** —
**Expected Result:** The record is visible with status "Deleted" and the Date Deleted timestamp matches the time of deletion.
**Priority:** High
**Requirement Reference:** AC-17; BR-8
**Configuration:** OTC Mobile App / Backoffice
**Login Method:** Mobile App (member) + Backoffice (Maker)
**Story:** AO-923
**Automation:**

---

## AO-923_TC-122
**Name:** Withdrawal Accounts - Disabled Account - BO re-enables account - Account restored to Active in app
**Test Scenario:** Verify that when Backoffice re-enables a Disabled bank account, the account is restored to Active status in the member's app, becomes clickable in the listing, and is available for Fiat Withdrawal.
**Test Case Type:** Status Transition
**Pre-requisites:** Logged in as a verified Active member with at least one Disabled bank account; logged in as Maker/Admin in Backoffice with ability to re-enable bank accounts.
**Steps:**
1. Confirm the Disabled account is non-clickable in the member's Linked Bank Accounts listing.
2. In Backoffice, navigate to the member's Withdrawal Account section and re-enable the Disabled account.
3. In the mobile app, navigate to My Account → Withdrawal Accounts → Linked Bank Accounts.
4. Locate the previously Disabled account and observe its status and interactivity.
5. Navigate to Withdrawal → Fiat → Bank Account and observe available destinations.
**Test Data:** —
**Expected Result:** The previously Disabled account is displayed as Active, is clickable in the listing, and appears as an available destination in the Fiat Withdrawal flow.
**Priority:** High
**Requirement Reference:** BR-1; BR-2
**Configuration:** OTC Mobile App / Backoffice
**Login Method:** Mobile App (member) + Backoffice (Maker)
**Story:** AO-923
**Automation:**

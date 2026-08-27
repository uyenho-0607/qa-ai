# Test Cases — AO-306

**Total:** 29

---

## AO-306_TC-01 — Sign Up – Personal Onboarding – Account Type – Personal Account option displayed

- **Module:** Sign Up
- **Scenario:** Verify that the Personal Account option is available for selection alongside the Business Account option on the Account Type screen.
- **Type:** Happy Path
- **Priority:** High
- **Automation:** Not set
- **Pre-requisites:** - App installed
- Not yet registered (new member)
- Onboarding flow started from the app launch screen. On the Account Type Selection screen (Step 2).
- **Requirement Ref:** BR-1

**Steps:**
1. Observe the Account Type screen.

**Expected Result:**
- [1] "Personal" account type option is visible on screen.
- [1] "Business" account type option is also visible on screen.
- [1] Both "Personal" and "Business" options respond to tap (highlight or selection state changes).

---

## AO-306_TC-02 — Sign Up – Personal Onboarding – Account Type – Selecting Personal navigates to Personal Details

- **Module:** Sign Up
- **Scenario:** Verify that selecting Personal Account navigates the member to the Personal Details screen.
- **Type:** Navigation / Screen Flow
- **Priority:** High
- **Automation:** Not set
- **Pre-requisites:** - On the Account Type Selection screen (Step 2).
- **Requirement Ref:** BR-1

**Steps:**
1. Tap the "Personal" account type option.

**Expected Result:**
- [1] The Personal Details screen is displayed.
- [1] Screen heading reads "Tell us about yourself".
- [1] Step 3 progress indicator is visible (progress bar advanced past Step 2).

---

## AO-306_TC-03 — Sign Up – Personal Onboarding – Personal Details – Screen UI and mandatory fields displayed

- **Module:** Sign Up
- **Scenario:** Verify that the Personal Details screen displays the required fields and a Continue CTA.
- **Type:** Display / UI
- **Priority:** Medium
- **Automation:** Not set
- **Pre-requisites:** - On the Personal Details screen (Step 3 of onboarding flow) with no fields filled.
- **Requirement Ref:** BR-2

**Steps:**
1. Observe the Personal Details screen.

**Expected Result:**
- [1] Screen heading: "Tell us about yourself".
- [1] Subheading: "Help us verify your identity and comply with regulatory requirements."
- [1] "Country of residence" field is present with placeholder "Select country".
- [1] "Date of birth" field is present with placeholder "DD/MM/YYYY".
- [1] Both fields are labelled as required (mandatory).
- [1] "Continue" CTA is visible at the bottom of the screen.

---

## AO-306_TC-04 — Sign Up – Personal Onboarding – Country of Residence – Tapping field opens country side sheet

- **Module:** Sign Up
- **Scenario:** Verify that the Country of Residence field opens a country selection side sheet.
- **Type:** Navigation / Screen Flow
- **Priority:** High
- **Automation:** Not set
- **Pre-requisites:** - On the Personal Details screen (Step 3 of onboarding flow).
- **Requirement Ref:** BR-2

**Steps:**
1. Tap anywhere on the "Country of residence" field.

**Expected Result:**
- [1] A full-height side sheet slides in with the title "Country of residence".
- [1] A search bar is displayed at the top of the side sheet.
- [1] Countries are listed alphabetically (A–Z) with country flag on the left and country name as primary text.
- [1] The list is scrollable.
- [1] The field on the main form is read-only (keyboard does not open on the main form).

---

## AO-306_TC-05 — Sign Up – Personal Onboarding – Country of Residence – Search filters results in real-time

- **Module:** Sign Up
- **Scenario:** Verify that partial input in the country search bar filters the country list in real-time from the first character.
- **Type:** Selection or Reference List
- **Priority:** Medium
- **Automation:** Not set
- **Pre-requisites:** - On the Personal Details screen (Step 3 of onboarding flow)
- Country of Residence side sheet is open.
- **Test Data:** Partial search: Sin | Full search: Singapore
- **Requirement Ref:** BR-2

**Steps:**
1. Tap the search bar on the country side sheet.
2. Type Sin.
3. Observe the filtered results.
4. Continue typing to Singapore.
5. Observe the filtered results.

**Expected Result:**
- [3] Results update immediately showing countries matching "Sin" (e.g. Singapore, Sint Maarten).
- [5] Only "Singapore" is shown.
- [5] Results update in real-time after each character.

---

## AO-306_TC-06 — Sign Up – Personal Onboarding – Country of Residence – Search with no match shows "No countries found"

- **Module:** Sign Up
- **Scenario:** Verify that searching for a term with no matching country shows the "No countries found" empty state.
- **Type:** Empty / No Data
- **Priority:** Low
- **Automation:** Not set
- **Pre-requisites:** - On the Personal Details screen (Step 3 of onboarding flow)
- Country of Residence side sheet is open.
- **Test Data:** Search term: Singpore
- **Requirement Ref:** BR-2

**Steps:**
1. Tap the search bar on the country side sheet.
2. Type Singpore.
3. Observe the results area.

**Expected Result:**
- [3] No country items are shown in the list.
- [3] Empty state message displayed: "No countries found".

---

## AO-306_TC-07 — Sign Up – Personal Onboarding – Country of Residence – Clearing search restores full country list

- **Module:** Sign Up
- **Scenario:** Verify that the country side sheet restores the full alphabetical country list when the search input is cleared.
- **Type:** Selection or Reference List
- **Priority:** Low
- **Automation:** Not set
- **Pre-requisites:** - On the Personal Details screen (Step 3 of onboarding flow)
- Country of Residence side sheet is open with a search term entered (e.g. `Singapore`).
- **Requirement Ref:** BR-2

**Steps:**
1. Type Singapore in the search bar.
2. Tap the clear (×) button on the search bar.
3. Observe the country list.

**Expected Result:**
- [2] Search input is cleared.
- [3] Full alphabetical country list is restored, starting from A (e.g. Afghanistan).
- [3] No filter is applied.

---

## AO-306_TC-08 — Sign Up – Personal Onboarding – Country of Residence – Back without selecting does not save selection

- **Module:** Sign Up
- **Scenario:** Verify that back navigation from the country side sheet without a selection does not save any value to the Country of Residence field.
- **Type:** Navigation / Screen Flow
- **Priority:** Medium
- **Automation:** Not set
- **Pre-requisites:** - On the Personal Details screen (Step 3 of onboarding flow)
- Country of Residence side sheet is open
- No country has been tapped/selected.
- **Requirement Ref:** BR-2

**Steps:**
1. Tap the back arrow (←) on the side sheet header without selecting any country.

**Expected Result:**
- [1] Side sheet closes.
- [1] Member is returned to the Personal Details screen.
- [1] "Country of residence" field still shows placeholder "Select country" (no value populated).

---

## AO-306_TC-09 — Sign Up – Personal Onboarding – Country of Residence – Selecting country populates field and closes side sheet

- **Module:** Sign Up
- **Scenario:** Verify that a country selection from the side sheet closes the sheet and populates the Country of Residence field with the chosen country name.
- **Type:** Happy Path
- **Priority:** High
- **Automation:** Not set
- **Pre-requisites:** - On the Personal Details screen (Step 3 of onboarding flow)
- Country of Residence side sheet is open.
- **Test Data:** Country: Singapore
- **Requirement Ref:** BR-2

**Steps:**
1. Scroll or search to find Singapore.
2. Tap Singapore.

**Expected Result:**
- [2] Side sheet closes immediately.
- [2] Member is returned to the Personal Details screen.
- [2] "Country of residence" field displays "Singapore".

---

## AO-306_TC-10 — Sign Up – Personal Onboarding – Country of Residence – Unavailable country shows inline error

- **Module:** Sign Up
- **Scenario:** Verify that selecting a country unavailable for registration displays the inline error "Sorry, registration is currently unavailable for this country."
- **Type:** Negative
- **Priority:** High
- **Automation:** Not set
- **Pre-requisites:** - On the Personal Details screen (Step 3 of onboarding flow)
- Country of Residence side sheet is open.
- **Test Data:** Country: Afghanistan
- **Requirement Ref:** BR-2

**Steps:**
1. Select Afghanistan from the country list.
2. Observe the Personal Details screen.

**Expected Result:**
- [1] Side sheet closes.
- [2] "Afghanistan" is displayed in the Country of Residence field.
- [2] Inline error message shown below the field: "Sorry, registration is currently unavailable for this country."
- [2] "Continue" CTA remains disabled.

---

## AO-306_TC-11 — Sign Up – Personal Onboarding – Personal Details – Continue disabled until both fields are filled

- **Module:** Sign Up
- **Scenario:** Verify that the Continue CTA is disabled when one or both mandatory fields have no valid value, and becomes enabled only when both contain valid values.
- **Type:** Navigation / Screen Flow
- **Priority:** High
- **Automation:** Not set
- **Pre-requisites:** - On the Personal Details screen (Step 3 of onboarding flow) with no fields filled.
- **Test Data:** Country: Singapore | DOB: 23/04/1995
- **Requirement Ref:** BR-2

**Steps:**
1. Observe Continue CTA — both fields empty.
2. Select Singapore as the Country of Residence.
3. Observe Continue CTA — country filled, DOB empty.
4. Select DOB 23/04/1995.
5. Observe Continue CTA — both fields filled.

**Expected Result:**
- [1] Continue CTA is disabled (greyed out / not tappable).
- [3] Continue CTA remains disabled.
- [5] Continue CTA becomes enabled (active, tappable).

---

## AO-306_TC-12 — Sign Up – Personal Onboarding – Date of Birth – Tapping field opens wheel date picker bottom sheet

- **Module:** Sign Up
- **Scenario:** Verify that the Date of Birth field opens a floating bottom sheet with a wheel date picker and a Done button.
- **Type:** Happy Path
- **Priority:** High
- **Automation:** Not set
- **Pre-requisites:** - On the Personal Details screen (Step 3 of onboarding flow)
- Country of Residence already filled with a valid country.
- **Requirement Ref:** BR-2

**Steps:**
1. Tap the "Date of birth" field.
2. Scroll the wheel picker to select a valid adult date (e.g. 23/04/1995).
3. Tap "Done".

**Expected Result:**
- [1] A floating bottom sheet titled "Date of birth" opens with a wheel picker (Month / Day / Year columns).
- [1] "Done" button is displayed on the bottom sheet.
- [3] Bottom sheet closes.
- [3] Selected date is displayed in the DOB field in DD/MM/YYYY format (e.g. "23/04/1995").
- [3] Continue CTA becomes active (both fields now filled with valid values).

---

## AO-306_TC-13 — Sign Up – Personal Onboarding – Date of Birth – Missing DOB shows "Please select your date of birth."

- **Module:** Sign Up
- **Scenario:** Verify that the error "Please select your date of birth." is displayed when Continue is tapped without a Date of Birth selection.
- **Type:** Validation
- **Priority:** High
- **Automation:** Not set
- **Pre-requisites:** - On the Personal Details screen (Step 3 of onboarding flow)
- Country of Residence filled with a valid available country
- DOB field empty.
- **Requirement Ref:** BR-2; ERR-1

**Steps:**
1. Select Singapore as the Country of Residence.
2. Tap the "Date of birth" field.
3. Dismiss the date picker bottom sheet by tapping the dim overlay behind it (do not select a date).

**Expected Result:**
- [3] Inline validation error shown below the DOB field: "Please select your date of birth."
- [3] Continue CTA is disabled; member cannot proceed.

---

## AO-306_TC-14 — Sign Up – Personal Onboarding – Date of Birth – Under-18 DOB shows "You must be at least 18 years old to register for an account."

- **Module:** Sign Up
- **Scenario:** Verify that selecting a DOB resulting in age exactly 17 displays the under-18 error and blocks continuation.
- **Type:** Boundary
- **Priority:** High
- **Automation:** Not set
- **Pre-requisites:** - On the Personal Details screen (Step 3 of onboarding flow)
- Country of Residence filled with a valid available country.
- **Test Data:** DOB: 22/08/2008 (under-18 boundary as of 2026-08-21; update before each run to: today's date − 18 years + 1 day)
- **Requirement Ref:** BR-2

**Steps:**
1. Select a valid available country (e.g. Singapore).
2. Tap the DOB field.
3. Set the wheel picker to 22/08/2008.
4. Tap "Done".

**Expected Result:**
- [4] DOB field displays "22/08/2008".
- [4] Inline error displayed below the DOB field: "You must be at least 18 years old to register for an account."
- [4] Continue CTA remains disabled.

---

## AO-306_TC-15 — Sign Up – Personal Onboarding – Date of Birth – Exactly 18 years old allows continuation

- **Module:** Sign Up
- **Scenario:** Verify that selecting a DOB resulting in age exactly 18 shows no validation error and enables the Continue CTA.
- **Type:** Boundary
- **Priority:** High
- **Automation:** Not set
- **Pre-requisites:** - On the Personal Details screen (Step 3 of onboarding flow)
- Country of Residence filled with a valid available country.
- **Test Data:** DOB: 21/08/2008 (exact 18-year boundary as of 2026-08-21; update before each run to: today's date − 18 years)
- **Requirement Ref:** BR-2

**Steps:**
1. Select a valid available country (e.g. Singapore).
2. Tap the DOB field.
3. Set the wheel picker to 21/08/2008.
4. Tap "Done".

**Expected Result:**
- [4] DOB field displays "21/08/2008".
- [4] No error message shown below the DOB field.
- [4] Continue CTA becomes enabled (active, tappable).

---

## AO-306_TC-16 — Sign Up – Personal Onboarding – Date of Birth – Future date treated as under-18 and blocked

- **Module:** Sign Up
- **Scenario:** Verify that a future date in the Date of Birth field triggers the under-18 validation error and blocks continuation.
- **Type:** Negative
- **Priority:** High
- **Automation:** Not set
- **Pre-requisites:** - On the Personal Details screen (Step 3 of onboarding flow)
- Country of Residence filled with a valid available country.
- **Test Data:** DOB: 01/01/2028
- **Requirement Ref:** BR-2

**Steps:**
1. Select a valid available country (e.g. Singapore).
2. Tap the DOB field.
3. Scroll the wheel picker to a future date: 01/01/2028.
4. Tap "Done".

**Expected Result:**
- [3] Future date is selectable on the wheel picker (not blocked at picker level).
- [4] DOB field shows the future date.
- [4] Inline error displayed: "You must be at least 18 years old to register for an account."
- [4] Continue CTA remains disabled.

---

## AO-306_TC-17 — Sign Up – Personal Onboarding – Personal Details – Back navigation returns to Account Type with inputs retained

- **Module:** Sign Up
- **Scenario:** Verify that back navigation on the Personal Details screen returns to the Account Type Selection screen while preserving any previously entered values.
- **Type:** Navigation / Screen Flow
- **Priority:** Medium
- **Automation:** Not set
- **Pre-requisites:** - On the Personal Details screen (Step 3 of onboarding flow) with at least one field filled (e.g. Country = Singapore).
- **Requirement Ref:** BR-1

**Steps:**
1. Fill Country of Residence with "Singapore".
2. Tap the back arrow (←).
3. Observe the screen shown.
4. Tap 'Personal' on the Account Type Selection screen to navigate forward to the Personal Details screen.

**Expected Result:**
- [2] Member is returned to the Account Type Selection screen (Step 2).
- [4] "Singapore" is still shown in the Country of Residence field (inputs retained).

---

## AO-306_TC-18 — Sign Up – Personal Onboarding – Steps 4–7 – Valid personal details proceeds to Setup Email

- **Module:** Sign Up
- **Scenario:** Verify that submitting valid personal details navigates the member to the Setup Email step (Step 4).
- **Type:** Navigation / Screen Flow
- **Priority:** High
- **Automation:** Not set
- **Pre-requisites:** - On the Personal Details screen (Step 3 of onboarding flow)
- Valid Country of Residence selected (available country)
- Valid DOB selected (age ≥ 18).
- **Requirement Ref:** BR-1

**Steps:**
1. Select an available country (e.g. Singapore).
2. Select a valid DOB (age ≥ 18).
3. Tap "Continue".

**Expected Result:**
- [3] Member is navigated to the Setup Email screen (Step 4).
- [3] Email setup screen is displayed.
- [3] Progress bar advances to Step 4 indicator.

---

## AO-306_TC-19 — Sign Up – Personal Onboarding – Account Created – Account type is Personal

- **Module:** Sign Up
- **Scenario:** Verify that upon successful completion of the full Personal onboarding flow, the created account type is displayed as Personal.
- **Type:** Happy Path
- **Priority:** High
- **Automation:** Not set
- **Pre-requisites:** - On the Account Created screen
- A Personal account has been fully registered through all onboarding steps (Name → Personal Account → Personal Details → Email → Password → Phone).
- **Requirement Ref:** BR-3

**Steps:**
1. Observe the Account Created confirmation screen.
2. Tap the CTA on the Account Created confirmation screen to proceed to the next screen; observe the account type label.

**Expected Result:**
- [1] Account Created screen is displayed upon successful completion.
- [2] Account type is identified as "Personal" (not "Business").

---

## AO-306_TC-20 — Sign Up – Personal Onboarding – Account Created – KYC verification journey triggered

- **Module:** Sign Up
- **Scenario:** Verify that after successful Personal account creation, the KYC (not KYB) verification journey is triggered.
- **Type:** Happy Path
- **Priority:** High
- **Automation:** Not set
- **Pre-requisites:** - On the Account Created screen
- Personal account onboarding completed.
- **Requirement Ref:** BR-3

**Steps:**
1. Observe the post-account-creation screen for a verification prompt.
2. Tap the KYC verification CTA displayed on the post-account-creation screen.

**Expected Result:**
- [1] KYC verification journey is triggered (not KYB).
- [1] Verification prompt or KYC flow entry point is displayed to the member.
- [2] No KYB flow is initiated.

---

## AO-306_TC-21 — Sign Up – Personal Onboarding – Backoffice – Country of Residence shown in Member Details

- **Module:** Sign Up
- **Scenario:** Verify that the Country of Residence entered during Personal onboarding is displayed in the Backoffice Member Details page.
- **Type:** Cross-System Sync
- **Priority:** High
- **Automation:** Not set
- **Pre-requisites:** - On the Member Details page (Backoffice)
- A Personal account has been successfully created with Country of Residence = Singapore
- Logged in to the Backoffice as an admin user.
- **Requirement Ref:** BR-4

**Steps:**
1. Navigate to the Member Details page for the newly created Personal account member.
2. Observe the Country of Residence field.

**Expected Result:**
- [2] Member Details page displays the "Country of Residence" field.
- [2] Value shown matches what was entered during onboarding: "Singapore".

---

## AO-306_TC-22 — Sign Up – Personal Onboarding – Backoffice – Create Member flow has no Country of Residence field

- **Module:** Sign Up
- **Scenario:** Verify that the Backoffice Create Member flow does not include a Country of Residence field.
- **Type:** Negative
- **Priority:** Medium
- **Automation:** Not set
- **Pre-requisites:** - On the Backoffice
- Logged in as an admin user with member creation permissions.
- **Requirement Ref:** BR-4

**Steps:**
1. Navigate to the Backoffice Create Member flow.
2. Review all fields available in the Create Member form.

**Expected Result:**
- [2] No "Country of Residence" field is present in the Backoffice Create Member form.
- [2] The Create Member flow is unchanged from its existing implementation.

---

## AO-306_TC-23 — Sign Up – Personal Onboarding – Personal Details – App backgrounded retains form data on resume

- **Module:** Sign Up
- **Scenario:** Verify that backgrounding the app during Personal Details form fill retains entered data when the app is resumed.
- **Type:** Mobile App Lifecycle
- **Priority:** Medium
- **Automation:** Not set
- **Pre-requisites:** - On the Personal Details screen (Step 3 of onboarding flow)
- Country of Residence filled with "Singapore"
- DOB field not yet filled.
- **Requirement Ref:** BR-2

**Steps:**
1. Fill Country of Residence with "Singapore".
2. Send the app to background (press Home).
3. Wait 30 seconds.
4. Resume the app.

**Expected Result:**
- [4] App resumes on the Personal Details screen.
- [4] Country of Residence field still shows "Singapore".
- [4] DOB field still shows its previous state (empty).
- [4] No data loss on resume.

---

## AO-306_TC-24 — Sign Up – Personal Onboarding – Personal Details – App killed clears form on reopen

- **Module:** Sign Up
- **Scenario:** Verify that force-killing the app during Personal Details form fill results in an empty form when the app is reopened.
- **Type:** Mobile App Lifecycle
- **Priority:** Medium
- **Automation:** Not set
- **Pre-requisites:** - On the Personal Details screen (Step 3 of onboarding flow)
- Country of Residence filled with "Singapore".
- **Requirement Ref:** BR-2

**Steps:**
1. Fill Country of Residence with "Singapore".
2. Force-kill the app.
3. Relaunch the app.
4. From the app launch screen, restart onboarding: enter name → select Personal Account → reach the Personal Details screen.

**Expected Result:**
- [3] App reopens to the start of the onboarding flow (or login screen).
- [4] Country of Residence and Date of Birth fields are empty.
- [4] Previously entered "Singapore" is not retained.

---

## AO-306_TC-25 — Sign Up – Personal Onboarding – Personal Details – User inputs retained when navigating back from later step

- **Module:** Sign Up
- **Scenario:** Verify that back navigation from the Setup Email step to the Personal Details screen retains previously entered Country of Residence and Date of Birth values.
- **Type:** Navigation / Screen Flow
- **Priority:** Medium
- **Automation:** Not set
- **Pre-requisites:** - On the Setup Email screen (Step 4 of onboarding flow)
- Personal Details already completed with Country: Singapore, DOB: 23/04/1995.
- **Test Data:** Country: Singapore | DOB: 23/04/1995
- **Requirement Ref:** BR-2

**Steps:**
1. From the Setup Email screen (Step 4), tap the back arrow (←).
2. Observe the Personal Details screen.

**Expected Result:**
- [1] Member is returned to the Personal Details screen.
- [2] "Country of residence" field displays "Singapore".
- [2] "Date of birth" field displays "23/04/1995".
- [2] No values are cleared or reset.
- [2] Continue CTA is enabled (both fields still valid).

---

## AO-306_TC-26 — Sign Up – Personal Onboarding – ID Number – Empty ID Number shows validation error

- **Module:** Sign Up
- **Scenario:** Verify that submitting the Personal Details form with an empty ID Number field displays the error "Please enter your ID number."
- **Type:** Validation
- **Priority:** High
- **Automation:** Not set
- **Pre-requisites:** - On the Personal Details screen (Step 3 of onboarding flow)
- Country of Residence and Date of Birth filled with valid values
- ID Number field present and empty.
- **Requirement Ref:** ERR-3

**Steps:**
1. Leave the ID Number field empty.
2. Tap "Continue".

**Expected Result:**
- [2] ⚠️ OPEN QUESTION (COV-02 / ORA): Confirm whether the ID Number field is in scope for AO-306 and which screen it appears on. If in scope — inline error shown below the ID Number field: "Please enter your ID number." Continue CTA is disabled.

---

## AO-306_TC-27 — Sign Up – Personal Onboarding – ID Number – ID Number exceeds maximum length shows validation error

- **Module:** Sign Up
- **Scenario:** Verify that entering more than 100 characters in the ID Number field displays the error "Maximum 100 characters allowed."
- **Type:** Boundary
- **Priority:** High
- **Automation:** Not set
- **Pre-requisites:** - On the Personal Details screen (Step 3 of onboarding flow)
- Country of Residence and Date of Birth filled with valid values
- ID Number field present.
- **Test Data:** ID Number: AAAAAAAAAABBBBBBBBBBCCCCCCCCCCDDDDDDDDDDEEEEEEEEEEAAAAAAAAAABBBBBBBBBBCCCCCCCCCCDDDDDDDDDDE1 (101 characters)
- **Requirement Ref:** ERR-4

**Steps:**
1. Enter a 101-character string in the ID Number field.
2. Tap "Continue" or observe inline validation.

**Expected Result:**
- [1] ⚠️ OPEN QUESTION (COV-02 / ORA): Confirm whether the ID Number field is in scope for AO-306 and which screen it appears on. If in scope — input is capped at 100 characters or inline error shown: "Maximum 100 characters allowed." after 101 characters are entered.

---

## AO-306_TC-28 — Sign Up – Personal Onboarding – Personal Details – Network interruption during submission shows graceful error

- **Module:** Sign Up
- **Scenario:** Verify that a network interruption during Personal Details form submission shows a graceful error and does not create a duplicate submission.
- **Type:** Mobile App Lifecycle
- **Priority:** Medium
- **Automation:** Not set
- **Pre-requisites:** - On the Personal Details screen (Step 3 of onboarding flow)
- Country of Residence and Date of Birth filled with valid values
- Device network connection available.
- **Test Data:** Country: Singapore | DOB: 21/08/2008
- **Requirement Ref:** BR-2

**Steps:**
1. Fill Country of Residence with a valid country and DOB with a valid date (age ≥ 18).
2. Disable the device network connection (airplane mode or Wi-Fi off).
3. Tap "Continue".
4. Re-enable the network connection.

**Expected Result:**
- [3] ⚠️ OPEN QUESTION (COV-03): Error message text on network failure is not specified in the ticket. Confirm the expected error message and whether retry is automatic or manual. If specified — a graceful error is displayed and no duplicate record is created on retry.

---

## AO-306_TC-29 — Sign Up – Personal Onboarding – Country of Residence – Re-opening side sheet after selection shows previous selection

- **Module:** Sign Up
- **Scenario:** Verify that re-opening the Country of Residence side sheet after a country was already selected displays the previously selected country in the list.
- **Type:** Selection or Reference List
- **Priority:** Medium
- **Automation:** Not set
- **Pre-requisites:** - On the Personal Details screen (Step 3 of onboarding flow)
- Country of Residence field already populated with "Singapore".
- **Test Data:** Previously selected country: Singapore
- **Requirement Ref:** BR-2

**Steps:**
1. Tap the "Country of residence" field to re-open the side sheet.
2. Observe the country list on re-open.

**Expected Result:**
- [2] ⚠️ OPEN QUESTION (COV-04): The expected state on re-open is not specified in the ticket. Confirm whether "Singapore" is pre-highlighted/pre-selected in the list, whether the list scrolls to "Singapore" automatically, and whether the search bar is cleared or retains previous input.

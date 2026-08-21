# Manual Test Cases — AO-306
**Story:** AO-306  **Configuration:** Android app; iOS app

---

## AO-306_TC-01
**Name:** Sign Up – Personal Onboarding – Account Type – Personal Account option displayed
**Test Scenario:** Verify that both Personal and Business account type options are available on the Account Type screen.
**Test Case Type:** Happy Path
**Pre-requisites:** App installed; not yet registered (new member); onboarding flow started from the app launch screen. On the Account Type Selection screen (Step 2).
**Steps:**
1. Observe the Account Type screen.
**Expected Result:**
- [1] "Personal" account type option is visible on screen with its description label (e.g. "For individual traders").
- [1] "Business" account type option is visible on screen with its description label (e.g. "For companies and organisations").
- [1] Both "Personal" and "Business" options respond to tap (highlight or selection state changes).
**Priority:** High
**Requirement Reference:** BR-1

---

## AO-306_TC-03
**Name:** Sign Up – Personal Onboarding – Personal Details – Screen UI and mandatory fields displayed
**Test Scenario:** Verify that the Personal Details screen displays the required fields and a Continue CTA.
**Test Case Type:** Display / UI
**Pre-requisites:** On the Personal Details screen (Step 3 of onboarding flow) with no fields filled.
**Steps:**
1. Observe the Personal Details screen.
**Expected Result:**
- [1] Screen heading: "Tell us about yourself".
- [1] Subheading: "Help us verify your identity and comply with regulatory requirements."
- [1] "Country of residence" field is present with placeholder "Select country".
- [1] "Date of birth" field is present with placeholder "DD/MM/YYYY".
- [1] Both fields are labelled as required (mandatory).
- [1] "Continue" CTA is visible at the bottom of the screen.
**Priority:** Medium
**Requirement Reference:** BR-2

---

## AO-306_TC-04
**Name:** Sign Up – Personal Onboarding – Country of Residence – Tapping field opens country side sheet
**Test Scenario:** Verify that the Country of Residence field opens a country selection side sheet.
**Test Case Type:** Navigation / Screen Flow
**Pre-requisites:** On the Personal Details screen (Step 3 of onboarding flow).
**Steps:**
1. Tap anywhere on the "Country of residence" field.
**Expected Result:**
- [1] A full-height side sheet slides in with the title "Country of residence".
- [1] A search bar is displayed at the top of the side sheet.
- [1] Countries are listed alphabetically (A–Z) with country flag on the left and country name as primary text.
- [1] The list is scrollable.
- [1] The field on the main form is read-only (keyboard does not open on the main form).
**Priority:** High
**Requirement Reference:** BR-2

---

## AO-306_TC-05
**Name:** Sign Up – Personal Onboarding – Country of Residence – Search filters by keyword and shows empty state for no match
**Test Scenario:** Verify that the country search bar filters results by keyword and shows an empty state when no country matches.
**Test Case Type:** Selection or Reference List
**Pre-requisites:** On the Personal Details screen (Step 3 of onboarding flow); Country of Residence side sheet is open.
**Steps:**
1. Tap the search bar on the country side sheet.
2. Type a valid country keyword (`Sin` / `SingGaPore` / `singapore`).
3. Clear the search input.
4. Type a keyword that matches no country (`XYZ`).
**Test Data:** Valid keyword: `Sin` / `SingGaPore` / `singapore` | No-match keyword: `XYZ`
**Expected Result:**
- [2] Country list is filtered to show only countries matching the keyword (case-insensitive).
- [3] Full alphabetical country list is restored.
- [4] No countries are shown.
- [4] Empty state message displayed: "No countries found".
**Priority:** Medium
**Requirement Reference:** BR-2

---

## AO-306_TC-07
**Name:** Sign Up – Personal Onboarding – Country of Residence – Clearing search restores full country list
**Test Scenario:** Verify that the country side sheet restores the full alphabetical country list when the search input is empty.
**Test Case Type:** Selection or Reference List
**Pre-requisites:** On the Personal Details screen (Step 3 of onboarding flow); Country of Residence side sheet is open with a search term entered (e.g. `Singapore`).
**Steps:**
1. Type `Singapore` in the search bar.
2. Tap the clear (×) button on the search bar.
3. Observe the country list.
**Expected Result:**
- [2] Search input is cleared.
- [3] Full alphabetical country list is restored, starting from A (e.g. Afghanistan).
- [3] No filter is applied.
**Priority:** Low
**Requirement Reference:** BR-2

---

## AO-306_TC-08
**Name:** Sign Up – Personal Onboarding – Country of Residence – Back without selecting does not save selection
**Test Scenario:** Verify that closing the country side sheet without a selection leaves the Country of Residence field unchanged.
**Test Case Type:** Navigation / Screen Flow
**Pre-requisites:** On the Personal Details screen (Step 3 of onboarding flow); Country of Residence side sheet is open; no country has been tapped/selected.
**Steps:**
1. Tap the back arrow (←) on the side sheet header without selecting any country.
**Expected Result:**
- [1] Side sheet closes.
- [1] Member is returned to the Personal Details screen.
- [1] "Country of residence" field still shows placeholder "Select country" (no value populated).
**Priority:** Medium
**Requirement Reference:** BR-2

---

## AO-306_TC-09
**Name:** Sign Up – Personal Onboarding – Country of Residence – Selecting country populates field and closes side sheet
**Test Scenario:** Verify that a country selection closes the side sheet and populates the Country of Residence field.
**Test Case Type:** Happy Path
**Pre-requisites:** On the Personal Details screen (Step 3 of onboarding flow); Country of Residence side sheet is open.
**Steps:**
1. Scroll or search to find Singapore.
2. Tap Singapore.
**Test Data:** Country: `Singapore`
**Expected Result:**
- [2] Side sheet closes immediately.
- [2] Member is returned to the Personal Details screen.
- [2] "Country of residence" field displays "Singapore".
**Priority:** High
**Requirement Reference:** BR-2

---

## AO-306_TC-10
**Name:** Sign Up – Personal Onboarding – Country of Residence – Unavailable country shows inline error
**Test Scenario:** Verify that a country unavailable for registration shows an inline error and blocks continuation.
**Test Case Type:** Negative
**Pre-requisites:** On the Personal Details screen (Step 3 of onboarding flow); Country of Residence side sheet is open.
**Steps:**
1. Select Afghanistan from the country list.
2. Observe the Personal Details screen.
**Test Data:** Country: `Afghanistan`
**Expected Result:**
- [1] Side sheet closes.
- [2] "Afghanistan" is displayed in the Country of Residence field.
- [2] Inline error message shown below the field: "Sorry, registration is currently unavailable for this country."
- [2] "Continue" CTA remains disabled.
**Priority:** High
**Requirement Reference:** BR-2

---

## AO-306_TC-11
**Name:** Sign Up – Personal Onboarding – Personal Details – Continue disabled until both fields are filled
**Test Scenario:** Verify that the Continue CTA is enabled only when all mandatory fields are valid.
**Test Case Type:** Navigation / Screen Flow
**Pre-requisites:** On the Personal Details screen (Step 3 of onboarding flow) with no fields filled.
**Steps:**
1. Observe Continue CTA — both fields empty.
2. Select Singapore as the Country of Residence.
3. Observe Continue CTA — country filled, DOB empty.
4. Select DOB 23/04/1995.
5. Observe Continue CTA — both fields filled.
**Test Data:** Country: `Singapore` | DOB: `23/04/1995`
**Expected Result:**
- [1] Continue CTA is disabled (greyed out / not tappable).
- [3] Continue CTA remains disabled.
- [5] Continue CTA becomes enabled (active, tappable).
**Priority:** High
**Requirement Reference:** BR-2

---

## AO-306_TC-12
**Name:** Sign Up – Personal Onboarding – Date of Birth – Tapping field opens wheel date picker bottom sheet
**Test Scenario:** Verify that the Date of Birth field opens a date picker.
**Test Case Type:** Happy Path
**Pre-requisites:** On the Personal Details screen (Step 3 of onboarding flow); Country of Residence already filled with a valid country.
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
**Priority:** High
**Requirement Reference:** BR-2

---

## AO-306_TC-13
**Name:** Sign Up – Personal Onboarding – Date of Birth – Missing DOB shows "Please select your date of birth."
**Test Scenario:** Verify that the DOB validation error is displayed when the Date of Birth field is empty.
**Test Case Type:** Validation
**Pre-requisites:** On the Personal Details screen (Step 3 of onboarding flow); Country of Residence filled with a valid available country; DOB field empty.
**Steps:**
1. Select Singapore as the Country of Residence.
2. Tap the "Date of birth" field.
3. Dismiss the date picker bottom sheet by tapping the dim overlay behind it (do not select a date).
**Expected Result:**
- [3] Inline validation error shown below the DOB field: "Please select your date of birth."
- [3] Continue CTA is disabled; member cannot proceed.
**Priority:** High
**Requirement Reference:** BR-2; ERR-1

---

## AO-306_TC-14
**Name:** Sign Up – Personal Onboarding – Date of Birth – Under-18 DOB shows "You must be at least 18 years old to register for an account."
**Test Scenario:** Verify that an under-18 DOB blocks continuation with an age requirement error.
**Test Case Type:** Boundary
**Pre-requisites:** On the Personal Details screen (Step 3 of onboarding flow); Country of Residence filled with a valid available country.
**Steps:**
1. Select a valid available country (e.g. Singapore).
2. Tap the DOB field.
3. Set the wheel picker to `22/08/2008`.
4. Tap "Done".
**Test Data:** DOB: `22/08/2008`
**Expected Result:**
- [4] DOB field displays "22/08/2008".
- [4] Inline error displayed below the DOB field: "You must be at least 18 years old to register for an account."
- [4] Continue CTA remains disabled.
**Priority:** High
**Requirement Reference:** BR-2

---

## AO-306_TC-15
**Name:** Sign Up – Personal Onboarding – Date of Birth – Exactly 18 years old allows continuation
**Test Scenario:** Verify that a DOB of exactly 18 years old passes the age requirement and enables continuation.
**Test Case Type:** Boundary
**Pre-requisites:** On the Personal Details screen (Step 3 of onboarding flow); Country of Residence filled with a valid available country.
**Steps:**
1. Select a valid available country (e.g. Singapore).
2. Tap the DOB field.
3. Set the wheel picker to `21/08/2008`.
4. Tap "Done".
**Test Data:** DOB: `21/08/2008`
**Expected Result:**
- [4] DOB field displays "21/08/2008".
- [4] No error message shown below the DOB field.
- [4] Continue CTA becomes enabled (active, tappable).
**Priority:** High
**Requirement Reference:** BR-2

---

## AO-306_TC-16
**Name:** Sign Up – Personal Onboarding – Date of Birth – Future date shows "Please select a valid date of birth."
**Test Scenario:** Verify that a future date in the Date of Birth field triggers a validation error and blocks continuation.
**Test Case Type:** Negative
**Pre-requisites:** On the Personal Details screen (Step 3 of onboarding flow); Country of Residence filled with a valid available country.
**Steps:**
1. Select a valid available country (e.g. Singapore).
2. Tap the DOB field.
3. Scroll the wheel picker to a future date: `01/01/2028`.
4. Tap "Done".
**Test Data:** DOB: `01/01/2028`
**Expected Result:**
- [3] Future date is selectable on the wheel picker (not blocked at picker level).
- [4] DOB field shows the future date.
- [4] Inline error displayed: "Please select a valid date of birth."
- [4] Continue CTA remains disabled.
**Priority:** High
**Requirement Reference:** BR-2; ERR-2

---

## AO-306_TC-17
**Name:** Sign Up – Personal Onboarding – Personal Details – Back navigation returns to Account Type with inputs retained
**Test Scenario:** Verify that back navigation on the Personal Details screen returns to the Account Type Selection screen while preserving any previously entered values.
**Test Case Type:** Navigation / Screen Flow
**Pre-requisites:** On the Personal Details screen (Step 3 of onboarding flow) with at least one field filled (e.g. Country = Singapore).
**Steps:**
1. Fill Country of Residence with "Singapore".
2. Tap the back arrow (←).
3. Observe the screen shown.
4. Tap 'Personal' on the Account Type Selection screen to navigate forward to the Personal Details screen.
**Expected Result:**
- [2] Member is returned to the Account Type Selection screen (Step 2).
- [4] "Singapore" is still shown in the Country of Residence field (inputs retained).
**Priority:** Medium
**Requirement Reference:** BR-1

---

## AO-306_TC-18
**Name:** Sign Up – Personal Onboarding – Steps 4–7 – Valid personal details proceeds to Setup Email
**Test Scenario:** Verify that valid personal details on Continue navigates the member to the Setup Email step.
**Test Case Type:** Navigation / Screen Flow
**Pre-requisites:** On the Personal Details screen (Step 3 of onboarding flow); valid Country of Residence selected (available country); valid DOB selected (age ≥ 18).
**Steps:**
1. Select an available country (e.g. Singapore).
2. Select a valid DOB (age ≥ 18).
3. Tap "Continue".
**Expected Result:**
- [3] Member is navigated to the Setup Email screen (Step 4).
- [3] Email setup screen is displayed.
- [3] Progress bar advances to Step 4 indicator.
**Priority:** High
**Requirement Reference:** BR-1

---

## AO-306_TC-19
**Name:** Sign Up – Personal Onboarding – Account Created – Account created successfully after completing Personal onboarding
**Test Scenario:** Verify that the Account Created screen is displayed after completing all Personal onboarding steps.
**Test Case Type:** Happy Path
**Pre-requisites:** On the Phone Number OTP Verification screen (Step 6 of onboarding flow); Personal account onboarding steps 1–6 completed (Name → Personal Account → Personal Details → Email OTP → Password → Phone OTP).
**Steps:**
1. Enter the correct 6-digit phone OTP.
2. Observe the Account Created confirmation screen.
**Expected Result:**
- [2] Account Created screen is displayed upon successful completion.
- [2] Screen header reads "Account Successfully Created".
- [2] "Done" CTA button is visible.
**Priority:** High
**Requirement Reference:** BR-3

---

## AO-306_TC-20
**Name:** Sign Up – Personal Onboarding – Account Created – KYC popup shown on Home after Personal account creation
**Test Scenario:** Verify that a KYC verification popup is shown on the Home screen after Personal account creation.
**Test Case Type:** Happy Path
**Pre-requisites:** On the Account Created screen; Personal account onboarding completed.
**Steps:**
1. Tap the "Done" button on the Account Created screen.
2. Observe the Home screen.
**Expected Result:**
- [1] Member is navigated to the Home screen.
- [2] A popup is displayed on the Home screen prompting the member to start the KYC verification journey.
- [2] The popup can be skipped (skip/dismiss option is present).
**Priority:** High
**Requirement Reference:** BR-3

---

## AO-306_TC-21
**Name:** Members – Personal Onboarding – Country of Residence shown in Member Details
**Test Scenario:** Verify that the Country of Residence is shown in the Backoffice Member Details page.
**Test Case Type:** Cross-System Sync
**Pre-requisites:** On the Member Details screen (Backoffice); a Personal account has been successfully created with Country of Residence = Singapore; logged in to the Backoffice as an admin user.
**Steps:**
1. Navigate to the Member Details page for the newly created Personal account member.
2. Observe the Country of Residence field.
**Expected Result:**
- [2] Member Details page displays the "Country of Residence" field.
- [2] Value shown matches what was entered during onboarding: "Singapore".
**Priority:** High
**Requirement Reference:** BR-4

---

## AO-306_TC-22
**Name:** Members – Personal Onboarding – Backoffice – Create Member flow has no Country of Residence field
**Test Scenario:** Verify that the Backoffice Create Member flow does not include a Country of Residence field.
**Test Case Type:** Negative
**Pre-requisites:** On the Create Member screen (Backoffice); logged in as an admin user with member creation permissions.
**Steps:**
1. Navigate to the Backoffice Create Member flow.
2. Review all fields available in the Create Member form.
**Expected Result:**
- [2] No "Country of Residence" field is present in the Backoffice Create Member form.
- [2] The Create Member flow is unchanged from its existing implementation.
**Priority:** Medium
**Requirement Reference:** BR-4

---

## AO-306_TC-23
**Name:** Sign Up – Personal Onboarding – Personal Details – App backgrounded retains form data on resume
**Test Scenario:** Verify that backgrounding the app during Personal Details form fill retains entered data when the app is resumed.
**Test Case Type:** Mobile App Lifecycle
**Pre-requisites:** On the Personal Details screen (Step 3 of onboarding flow); Country of Residence filled with "Singapore"; DOB field not yet filled.
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
**Priority:** Medium
**Requirement Reference:** BR-2

---

## AO-306_TC-24
**Name:** Sign Up – Personal Onboarding – Personal Details – App killed clears form on reopen
**Test Scenario:** Verify that force-killing the app during Personal Details form fill results in an empty form when the app is reopened.
**Test Case Type:** Mobile App Lifecycle
**Pre-requisites:** On the Personal Details screen (Step 3 of onboarding flow); Country of Residence filled with "Singapore".
**Steps:**
1. Fill Country of Residence with "Singapore".
2. Force-kill the app.
3. Relaunch the app.
4. From the app launch screen, restart onboarding: enter name → select Personal Account → reach the Personal Details screen.
**Expected Result:**
- [3] App reopens to the start of the onboarding flow (or login screen).
- [4] Country of Residence and Date of Birth fields are empty.
- [4] Previously entered "Singapore" is not retained.
**Priority:** Medium
**Requirement Reference:** BR-2

---

## AO-306_TC-25
**Name:** Sign Up – Personal Onboarding – Personal Details – User inputs retained when navigating back from later step
**Test Scenario:** Verify that back navigation from Setup Email to Personal Details retains previously entered values.
**Test Case Type:** Navigation / Screen Flow
**Pre-requisites:** On the Setup Email screen (Step 4 of onboarding flow); Personal Details already completed with Country: Singapore, DOB: 23/04/1995.
**Steps:**
1. From the Setup Email screen (Step 4), tap the back arrow (←).
2. Observe the Personal Details screen.
**Test Data:** Country: `Singapore` | DOB: `23/04/1995`
**Expected Result:**
- [1] Member is returned to the Personal Details screen.
- [2] "Country of residence" field displays "Singapore".
- [2] "Date of birth" field displays "23/04/1995".
- [2] No values are cleared or reset.
- [2] Continue CTA is enabled (both fields still valid).
**Priority:** Medium
**Requirement Reference:** BR-2

---

## AO-306_TC-28
**Name:** Sign Up – Personal Onboarding – Personal Details – Network interruption during submission shows graceful error
**Test Scenario:** Verify that a network interruption during form submission shows an error without creating a duplicate.
**Test Case Type:** Mobile App Lifecycle
**Pre-requisites:** On the Personal Details screen (Step 3 of onboarding flow); Country of Residence and Date of Birth filled with valid values; device network connection available.
**Steps:**
1. Fill Country of Residence with a valid country and DOB with a valid date (age ≥ 18).
2. Disable the device network connection (airplane mode or Wi-Fi off).
3. Tap "Continue".
4. Re-enable the network connection.
**Test Data:** Country: `Singapore` | DOB: `23/04/1995`
**Expected Result:**
- [3] ⚠️ OPEN QUESTION: Error message text on network failure is not specified in the ticket. Confirm the expected error message and whether retry is automatic or manual. If specified — a graceful error is displayed and no duplicate record is created on retry.
**Priority:** Medium
**Requirement Reference:** BR-2

---

## AO-306_TC-29
**Name:** Sign Up – Personal Onboarding – Country of Residence – Re-opening side sheet after selection shows previous selection
**Test Scenario:** Verify that re-opening the country side sheet shows the previously selected country.
**Test Case Type:** Selection or Reference List
**Pre-requisites:** On the Personal Details screen (Step 3 of onboarding flow); Country of Residence field already populated with "Singapore".
**Steps:**
1. Tap the "Country of residence" field to re-open the side sheet.
2. Observe the country list on re-open.
**Test Data:** Previously selected country: `Singapore`
**Expected Result:**
- [2] Previously selected country "Singapore" is shown with a checkmark (✓) in the list.
**Priority:** Medium
**Requirement Reference:** BR-2


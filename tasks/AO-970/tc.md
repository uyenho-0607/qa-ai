# Test Cases — AO-970

**Issue:** [AO-970](https://aquariux.atlassian.net/browse/AO-970)
**Fetched:** 2026-08-27
**Total:** 6 cases

## Summary

| Status | Count |
|---|---|
| ✅ Automated (39) | 0 |
| 🔧 Can Automate (37) | 0 |
| 🚧 In Progress (38) | 0 |
| ❌ Not Automatable (40) | 0 |
| ⬜ Unset | 6 |

| Priority | Count |
|---|---|
| High (54) | 0 |
| Medium (55) | 0 |
| Low (56) | 0 |
| Unset | 6 |

## Case Groups

| Group | Cases | Automated | Can Automate | Pattern |
|---|---|---|---|---|
| Sign Up - Routing - Existing BO Member - Validation prompt | 2 | 0 | 0 | Business vs Personal member |
| Login – Authentication – Backoffice Member Login | 1 | 0 | 0 | solo |
| Login – Passcode – UI Display | 1 | 0 | 0 | solo |
| Login – Rounding – Backoffice Created Member | 2 | 0 | 0 | Business vs Personal member |

---

## Full Case Details

### Sign Up - Routing - Existing BO Member - Validation prompt (2 cases)

#### TC-178548 · Sign Up - Routing - Existing BO Member (Business) - Validation prompt
**Priority:** Unset | **Automation:** Unset | **State:** Done
**Folder:** 2315 Sign Up

**Description:** Verify that a backoffice-created Business member who attempts to register via the Sign Up flow sees a custom error directing them to Forgot Password instead of the generic "email already registered" message.

**Prerequisites:**
A backoffice-created Business account member exists (email registered, no password ever set). Member is on the Registration – Setup Email screen.

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter the backoffice-created Business member's registered email in the email field | — |
| 2 | Observe the error message shown | Error displayed: "Please go to Forgot Password page to reset your password". Member remains on Setup Email screen. The generic error "This email address is already registered. Please log in or use a different email address to proceed." is not shown. |

**Test Data:** —

---

#### TC-191117 · Sign Up - Routing - Existing BO Member (Personal) - Validation prompt
**Priority:** Unset | **Automation:** Unset | **State:** Done
**Folder:** 2315 Sign Up

**Description:** Verify that a backoffice-created Personal member who attempts to register via the Sign Up flow sees a custom error directing them to Forgot Password instead of the generic "email already registered" message.

**Prerequisites:**
A backoffice-created Personal account member exists (email registered, no password ever set). Member is on the Registration – Setup Email screen.

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Enter the backoffice-created Personal member's registered email in the email field | — |
| 2 | Observe the error message shown | Error displayed: "Please go to Forgot Password page to reset your password". Member remains on Setup Email screen. The generic error "This email address is already registered. Please log in or use a different email address to proceed." is not shown. |

**Test Data:** —

---

### Login – Authentication – Backoffice Member Login (1 case)

#### TC-178546 · Login – Authentication – Backoffice Member Login – Suspended error shown when no password set
**Priority:** Unset | **Automation:** Unset | **State:** Done
**Folder:** 2317 LoginApp

**Description:** Verify backoffice-created member sees suspended error when attempting login before setting a password.

**Prerequisites:**
A backoffice-created member account exists (no password has ever been set). Member has downloaded and launched the OTC Mobile App.

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | On the Login screen, enter the backoffice-created member's registered email and a random password, then tap "Log in" | Login fails. Error displayed: "Account Suspended — Your account has been suspended. Please go to Forgot Password to retain your account." "Forgot Password" link/button remains visible and tappable. |

**Test Data:** —

---

### Login – Passcode – UI Display (1 case)

#### TC-178547 · Login – Passcode – UI Display – Passcode setup screen shown on backoffice member first login
**Priority:** Unset | **Automation:** Unset | **State:** Done
**Folder:** 2317 LoginApp

**Description:** Verify Passcode Setup screen is shown immediately after backoffice-created member's first successful login.

**Prerequisites:**
- Backoffice-created member account exists (no password set)
- Member has completed Forgot Password flow and reset their password
- Member has tapped "Log in" on Password Updated screen and entered new credentials on Login screen
- Member has tapped "Log in" and authentication succeeded

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe the screen displayed immediately after successful login | Passcode Setup screen is displayed: title indicating passcode creation; 6-digit input field (dots/circles); numeric keypad (0–9); no Back/Skip button available. |

**Test Data:** —

---

### Login – Rounding – Backoffice Created Member (2 cases)

#### TC-191116 · Login – Rounding – Backoffice Created Member (Business) – successful login after passcode and biometric setup
**Priority:** Unset | **Automation:** Unset | **State:** Done
**Folder:** 2317 LoginApp

**Description:** Verify the complete end-to-end onboarding journey for a Business member created by a backoffice admin.

**Prerequisites:**
- A backoffice admin has created a Business member account (email registered, no password ever set).
- The member has downloaded and launched the OTC Mobile App.
- Member has completed Forgot Password flow and reset their password.

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | On the Login screen, member entered new credentials and tap Log In | Authentication succeeds. User is NOT taken to the home screen yet. |
| 2 | Observe the screen displayed immediately after successful login | Passcode Setup screen is displayed: title indicating passcode creation; 6-digit input field (dots/circles); numeric keypad (0–9); no Back/Skip button. |
| 3 | Enter a 6-digit passcode, then re-enter it to confirm | Passcode is accepted. App proceeds to the next setup step (Biometric setup screen). |
| 4 | On the Biometric Setup screen, agree to enable biometric authentication (Face ID / Fingerprint) when prompted. Note: this step may be skipped because device without hardware or hardware but none enrolled | Biometric is enabled successfully. |
| 5 | Observe the app | The member is navigated to the app Home screen, fully authenticated and onboarded. |

**Test Data:** —

---

#### TC-191118 · Login – Rounding – Backoffice Created Member (Personal) – successful login after passcode and biometric setup
**Priority:** Unset | **Automation:** Unset | **State:** Done
**Folder:** 2317 LoginApp

**Description:** Verify the complete end-to-end onboarding journey for a Personal member created by a backoffice admin.

**Prerequisites:**
- A backoffice admin has created a Personal member account (email registered, no password ever set).
- The member has downloaded and launched the OTC Mobile App.
- Member has completed Forgot Password flow and reset their password.

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | On the Login screen, member entered new credentials and tap Log In | Authentication succeeds. User is NOT taken to the home screen yet. |
| 2 | Observe the screen displayed immediately after successful login | Passcode Setup screen is displayed: title indicating passcode creation; 6-digit input field (dots/circles); numeric keypad (0–9); no Back/Skip button. |
| 3 | Enter a 6-digit passcode, then re-enter it to confirm | Passcode is accepted. App proceeds to the next setup step (Biometric setup screen). |
| 4 | On the Biometric Setup screen, agree to enable biometric authentication (Face ID / Fingerprint) when prompted. Note: this step may be skipped because device without hardware or hardware but none enrolled | Biometric is enabled successfully. |
| 5 | Observe the app | The member is navigated to the app Home screen, fully authenticated and onboarded. |

**Test Data:** —

---

# Jira: AO-306

## Title
[OTC][MobileApp] Personal Onboarding

## Status
In Progress | Assignee: Ming En Leong | Reporter: Alexis Soo

---

## Description

### Background
Currently, the mobile application only supports Business account onboarding. This enhancement introduces Personal account onboarding, allowing new members to register a Personal account through the mobile application. The existing onboarding flow for _Email Verification, Password Setup, Phone Verification and Account Creation_ shall be reused. A new Personal Details screen is introduced to capture information required for Personal accounts before continuing to the existing onboarding flow.

### User Story
As a new member, I want to register a Personal account so that I can create my own account through the mobile application.

### Behaviour Table

| Behaviour | Description |
|---|---|
| As-Is | Only Business account onboarding is supported. |
| To-Be | Members can select Personal Account, complete the required personal details, and continue through the existing onboarding flow. |

### User Flow
1. Member selects _Personal Account_ during onboarding.
2. System displays the _Personal Details_ screen.
3. Member enters:
   - Country of Residence
   - DOB
4. Member taps _Continue CTA_.
5. System validates all mandatory fields.
6. Member proceeds to the existing onboarding flow:
   - Setup Email & Verify Email
   - Setup Password
   - Phone Number & Verify Phone Number
   - Account Created

---

## Business Requirements

| # | Requirement | Description |
|---|---|---|
| 1 | General Requirements | User path: Step 1: Enter Name → Step 2: Select Personal → **Step 3: Enter Personal Details - Country of Residence, Date Of Birth.** Personal onboarding shall reuse the existing Business onboarding flow for steps 4–7: Step 4: Setup Email & OTP Verification (AO-298), Step 5: Setup Password (AO-299), Step 6: Setup Phone Number & OTP Verification (AO-297), Step 7: Account Created (AO-300). Note: Error messages for Email Verification, Password, Phone Number and OTP shall follow the existing Business onboarding implementation. |
| 2 | Step 3: Personal Details | The Personal Details screen shall contain mandatory fields `Country of Residence` & `Date Of Birth`. Country of Residence uses the same country master list configured for Country of Registration. Date of Birth — date picker; future dates are not allowed; minimum age requirement applies. If the member is under 18, prevent continuation and display: _You must be at least 18 years old to register for an account._ |
| 3 | Member Verification | Upon successful account creation, the account type shall be **Personal** and the member shall follow the **KYC** verification journey. |
| 4 | Backoffice Impact | The Member Details page shall display the member's `Country of Residence`. No changes are required to the Back Office Create Member flow. |

---

## Acceptance Criteria
_(Derived from description, BRs, and comment — no explicit AC list in ticket)_

- AC-1 *(derived)*: A new "Personal Account" option is available for selection during onboarding (Step 2).
- AC-2 *(derived)*: Selecting Personal Account navigates the user to the Personal Details screen (Step 3).
- AC-3 *(derived)*: Personal Details screen contains mandatory fields: Country of Residence and Date of Birth.
- AC-4 *(derived)*: Country of Residence uses the same country master list as Business Country of Registration.
- AC-5 *(derived)*: Date of Birth uses a date picker; future dates cannot be selected.
- AC-6 *(derived)*: If user is under 18 years old, continuation is blocked.
- AC-7 *(derived)*: After valid personal details are entered and Continue is tapped, the user proceeds to the existing onboarding flow (Steps 4–7: Email, Password, Phone, Account Created).
- AC-8 *(derived)*: Upon successful account creation, account type is Personal and the KYC (not KYB) verification journey is triggered.
- AC-9 *(derived)*: Backoffice Member Details page displays the member's Country of Residence.
- AC-10 *(derived)*: The Backoffice Create Member flow requires no changes.

---

## Error Messages (from comment by Ming En Leong, 2026-07-29)

| # | Scenario | Message |
|---|---|---|
| ERR-1 | Date of Birth not selected | _Please select your date of birth._ |
| ERR-2 | Date of Birth is in the future | _Please select a valid date of birth._ |
| ERR-3 | ID Number is empty | _Please enter your ID number._ |
| ERR-4 | ID Number exceeds maximum length | _Maximum 100 characters allowed._ |

> **Note:** ERR-3 and ERR-4 reference an "ID Number" field. The main ticket description (BR-2) and user flow do not list ID Number as part of Step 3 (only Country of Residence + DOB are mentioned). This may be a future field or a carry-over from a different version. Flagged for clarification.

---

## Linked Issues

- AO-992: [OTC][MobileApp] Consistent Email OTP behaviour (connects to) — Backlog

### Referenced Issues (in BR-1, reuse existing flow)
- AO-298: Setup Email & OTP Verification
- AO-299: Setup Password
- AO-297: Setup Phone Number & OTP Verification
- AO-300: Account Created

---

## Sub-tasks

| Key | Summary | Type | Status |
|---|---|---|---|
| AO-984 | [OTC][MobileApp] Individual Onboarding | Design Request | Ready To Review |
| AO-985 | [OTC][MobileApp] Individual Onboarding | Backend Development | Pending Merge to SIT |
| AO-986 | [OTC][MobileApp] Individual Onboarding | Frontend Development | Pending Review |
| AO-1081 | [AO-306] [OTC][MobileApp] Personal Onboarding | QA Execution | To Do |
| AO-1082 | [AO-306][OTC][MobileApp] Personal Onboarding | QA Preparation | To Do |

_Sub-tasks AO-984, AO-985, AO-986 have no description or ACs (implementation tickets only)._

---

## Visual Context
No attachments on this ticket.

## Figma Links
No Figma links found in description or comments.

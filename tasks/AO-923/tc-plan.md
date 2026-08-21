# TC Plan — AO-923
# [OTC][MobileApp][Member] Linked Bank Accounts — Add, Edit, Remove
# Module: Withdrawal Accounts (OTC Mobile App)

## Screens Swept
1. Bank Account Listing screen
2. Add Bank Account form screen
3. Review Bank Account screen
4. Email OTP Verification screen
5. Bank Account Details screen (Active)
6. Bank Account Details screen (Disabled — read-only)
7. Edit Label screen
8. Add/Remove Currency screen
9. Delete Account confirmation dialog

---

| #  | Refs | Screen | Scenario | Type | Expected-value source | Status |
|----|------|--------|----------|------|-----------------------|--------|

## SECTION 1 — General Requirements / Entry Points

| #  | Refs | Screen | Scenario | Type | Expected-value source | Status |
|----|------|--------|----------|------|-----------------------|--------|
| 1  | AC-1, BR-1 | Listing | Verified Active member can access Linked Bank Accounts via My Account → Withdrawal Accounts → Linked Bank Accounts | Happy Path | BR-1 entry point | new |
| 2  | AC-2, BR-1 | Listing | Verified Active member can access Add Bank Account via Withdrawal → Fiat → Bank Account → Add Bank Account | Happy Path | BR-1 entry point | new |
| 3  | AC-3, BR-1 | Listing | Non-verified member tapping Add Bank Account is redirected to verification flow (same behaviour as deposit module entry point); verified member is NOT redirected | Permission / Role | BR-1: "same behaviour as clicking deposit module" | new |
| 4  | BR-1 | Listing | Non-Active member (e.g. suspended) clicking Add Bank Account is blocked — redirected to verification flow (same gate as non-verified member per BR-1 "active members with Approved verification status") | Permission / Role | BR-1: access gate requires active + Approved verification status | new |

## SECTION 2 — Bank Account Listing

| #  | Refs | Screen | Scenario | Type | Expected-value source | Status |
|----|------|--------|----------|------|-----------------------|--------|
| 5  | AC-9, BR-2 | Listing | Listing displays Active accounts before Disabled accounts, sorted most recently added first | Happy Path | BR-2 sort rule | new |
| 6  | AC-9, BR-2 | Listing | Newly added account appears at top of listing | Happy Path | BR-2 sort rule | new |
| 7  | BR-2 | Listing | Empty state shown when member has no bank accounts | Empty / No Data | BR-2: "You haven't added a bank account yet. Add one to withdraw your fiat balances." | new |
| 8  | AC-10, BR-2 | Listing | Search by Label returns matching accounts | Happy Path | BR-2 search | new |
| 9  | AC-10, BR-2 | Listing | Search by Bank Name returns matching accounts | Happy Path | BR-2 search | new |
| 10 | AC-10, BR-2 | Listing | Search by masked Account Number (last 4 digits) returns matching accounts | Happy Path | BR-2 masked search | new |
| 11 | BR-2 | Listing | Search with no match displays no results / empty search state | Empty / No Data | BR-2 search | new |
| 12 | AC-11, BR-2 | Listing | Disabled account row is non-clickable (visually disabled) | Status Transition | BR-2 | new |
| 13 | AC-11, BR-2 | Listing | Tapping a Disabled account shows error toast: "This bank account has been disabled, contact us for further assistance." | Negative | ERR-15 | new |
| 14 | AC-8, BR-2 | Listing | Add Bank Account CTA is disabled when member has 5 Active accounts | Boundary | BR-1 limit = 5; BR-2 | new |
| 15 | AC-8, BR-2 | Listing | Toast shown when member at limit taps disabled Add Bank Account CTA: "You've reached the maximum of 5 bank accounts. Please remove one before adding another." (assert "5" rendered, not template literal) | Boundary | ERR-13; BR-1 config limit = 5 | new |
| 16 | BR-2 | Listing | Add Bank Account CTA is enabled when member has fewer than 5 Active accounts | Boundary | BR-1 limit = 5 | new |
| 17 | AC-20, BR-1 | Listing | Disabled accounts do not count toward the 5-account limit | Boundary | BR-1 | new |
| 18 | AC-20, BR-1 | Listing | Deleted accounts do not count toward the 5-account limit | Boundary | BR-1 | new |
| 19 | BR-2 | Navigation | Tapping Active account row opens Bank Account Details page | Navigation / Screen Flow | BR-2 | new |

## SECTION 3 — Add Bank Account Form

| #  | Refs | Screen | Scenario | Type | Expected-value source | Status |
|----|------|--------|----------|------|-----------------------|--------|
| 20 | AC-4, BR-3 | Add form | All required fields visible and displayed with correct labels and helper texts | Display / UI | BR-3 field list | new |
| 21 | AC-4, BR-3 | Add form | Optional fields visible (Bank Code, Account Type, Address Line 2, Postal Code) | Display / UI | BR-3 optional fields | new |
| 22 | AC-4, BR-3 | Add form | Label — valid alphanumeric input accepted (max 30 chars) | Happy Path | BR-3 Label rule | new |
| 23 | BR-3, ERR-D1 | Add form | Label — empty field shows error: "Please enter a label." | Validation | ERR-D1 | new |
| 24 | BR-3, ERR-D2 | Add form | Label — 31 characters shows error: "Label cannot exceed 30 characters." | Boundary | ERR-D2 | new |
| 25 | BR-3 | Add form | Bank Country — single-select options match OTC platform country list | Selection / Reference List | BR-3 | new |
| 26 | BR-3, ERR-D3 | Add form | Bank Country — not selected shows error: "Please select a bank country." | Validation | ERR-D3 | new |
| 27 | BR-3 | Add form | Bank Name — valid alphanumeric + special chars `& ' . , - ( ) /` accepted (max 100 chars) | Happy Path | BR-3 Bank Name rule | new |
| 28 | BR-3, ERR-D4 | Add form | Bank Name — empty shows error: "Please enter a bank name." | Validation | ERR-D4 | new |
| 29 | BR-3, ERR-D5 | Add form | Bank Name — 101 characters shows error: "Bank name cannot exceed 100 characters." | Boundary | ERR-D5 | new |
| 30 | BR-3 | Add form | Bank Name — invalid special characters (@, #, $) rejected; valid chars (& ' . , - ( ) /) accepted in same field | Validation | BR-3 regex `^[\p{L}\p{N}\s&'.,\-()/]+$` | new |
| 31 | BR-3 | Add form | Account Holder Name — valid alphanumeric input accepted (max 30 chars) | Happy Path | BR-3 | new |
| 32 | BR-3, ERR-D7 | Add form | Account Holder Name — empty shows error: "Please enter the account name." | Validation | ERR-D7 | new |
| 33 | BR-3, ERR-D8 | Add form | Account Holder Name — 31 characters shows error: "Account name cannot exceed 30 characters." | Boundary | ERR-D8 | new |
| 34 | BR-3 | Add form | Account Number / IBAN — valid alphanumeric input accepted (max 34 chars) | Happy Path | BR-3 | new |
| 35 | BR-3, ERR-1 | Add form | Account Number / IBAN — empty shows error: "Please enter an account number." | Validation | ERR-1 | new |
| 36 | BR-3, ERR-D10 | Add form | Account Number / IBAN — 35 characters shows error: "Account number cannot exceed 34 characters." | Boundary | ERR-D10 | new |
| 37 | BR-3 | Add form | BIC / SWIFT — 8-character code accepted | Happy Path | BR-3 ISO 9362 | new |
| 38 | BR-3 | Add form | BIC / SWIFT — 11-character code accepted | Happy Path | BR-3 ISO 9362 | new |
| 39 | BR-3, ERR-3 | Add form | BIC / SWIFT — empty shows error: "Please enter your bank's SWIFT/BIC code. Your bank can provide this if you don't have it." | Validation | ERR-3 | new |
| 40 | BR-3, ERR-4 | Add form | BIC / SWIFT — invalid format (not 8 or 11 chars) shows error: "Please check the SWIFT/BIC code and try again." | Validation | ERR-4 | new |
| 41 | BR-3 | Add form | Currency — multi-select options match platform fiat currency list | Selection / Reference List | BR-3 | new |
| 42 | BR-3, ERR-7 | Add form | Currency — no currency selected shows error: "Please select at least one currency." | Validation | ERR-7 | new |
| 43 | BR-3 | Add form | Currency — multiple currencies can be selected simultaneously | Happy Path | BR-3 multi-select | new |
| 44 | BR-3 | Add form | Account Type — optional single-select; Checking / Savings / Not specified options available | Selection / Reference List | BR-3 | new |
| 45 | BR-3 | Add form | Bank Code / Routing Number — optional; accepts free text (max 100 chars) | Happy Path | BR-3 | new |
| 46 | BR-3, ERR-D20 | Add form | Bank Code / Routing Number — 101 characters shows error: "Bank code cannot exceed 100 characters." | Boundary | ERR-D20 | new |
| 47 | BR-3 | Add form | Address Line 1 — valid free text accepted (max 100 chars) | Happy Path | BR-3 | new |
| 48 | BR-3, ERR-D13 | Add form | Address Line 1 — empty shows error: "Please enter your address." | Validation | ERR-D13 | new |
| 49 | BR-3, ERR-D14 | Add form | Address Line 1 — 101 characters shows error: "Address Line 1 cannot exceed 100 characters." | Boundary | ERR-D14 | new |
| 50 | BR-3, ERR-D15 | Add form | Address Line 2 — optional; 101 characters shows error: "Address Line 2 cannot exceed 100 characters." | Boundary | ERR-D15 | new |
| 51 | BR-3 | Add form | City — valid free text accepted (max 100 chars) | Happy Path | BR-3 | new |
| 52 | BR-3, ERR-D16 | Add form | City — empty shows error: "Please enter your city." | Validation | ERR-D16 | new |
| 53 | BR-3, ERR-D17 | Add form | City — 101 characters shows error: "City cannot exceed 100 characters." | Boundary | ERR-D17 | new |
| 54 | BR-3, ERR-D18 | Add form | Postal Code — optional; 101 characters shows error: "Postal Code cannot exceed 100 characters." | Boundary | ERR-D18 | new |
| 55 | BR-3, BR-3b | Add form | Continue CTA is disabled until all required fields are filled | Navigation / Screen Flow | BR-3b validation on Continue | new |

## SECTION 4 — Input Validation (Cross-field & Business Rules)

| #  | Refs | Screen | Scenario | Type | Expected-value source | Status |
|----|------|--------|----------|------|-----------------------|--------|
| 56 | AC-5, BR-3b | Add form | BIC country cross-check — BIC country matches Bank Country, no warning shown | Happy Path | BR-3b | new |
| 57 | AC-5, BR-3b, ERR-5 | Add form | BIC country cross-check — BIC country mismatches Bank Country shows warning popup with message "This SWIFT/BIC code looks like it belongs to a bank in {BIC Country}, but you selected {Bank Country}. Please check before continuing." — assert actual country names render (e.g. BIC=DEUTDEFF → "Germany"; Bank Country="Singapore") | Validation | ERR-5; comment 244280 | new |
| 58 | AC-5, BR-3b | Add form | BIC country mismatch warning — tapping "Review Details" dismisses popup and returns to form | Navigation / Screen Flow | comment 244280 | new |
| 59 | AC-5, BR-3b | Add form | BIC country mismatch warning — tapping "Continue anyway" proceeds to Review Bank Account | Navigation / Screen Flow | comment 244280 | new |
| 60 | AC-6, BR-3b, ERR-8 | Add form | Duplicate account (same Account Number + BIC/SWIFT already Active for same member) rejected: "You've already added this bank account. You can add more currencies to it instead." — assert error message appears as banner | Negative | ERR-8 | new |
| 121 | AC-6, BR-3b | Add form | Duplicate account rejection — Account Number and BIC/SWIFT fields highlighted in red; page auto-scrolls to those fields (per dev comment 244968 + Figma) | Negative | dev comment 244968; Figma node 7327-326619 | new |
| 61 | BR-3b, ERR-9 | Add form | Duplicate of a Disabled account shows error: "This bank account can't be added. Please contact support for assistance." | Negative | ERR-9 | new |
| 62 | AC-8, BR-3b | Add form | Member at 5-account limit cannot submit new bank account (CTA disabled or error shown) | Boundary | BR-1, ERR-13 | new |

## SECTION 5 — Review Bank Account Screen

| #  | Refs | Screen | Scenario | Type | Expected-value source | Status |
|----|------|--------|----------|------|-----------------------|--------|
| 63 | BR-4 | Review | All entered field values displayed correctly on Review screen (read-only) | Display / UI | BR-4 | new |
| 64 | BR-4 | Review | Tapping Back on Review screen returns to Add form with all values retained | Navigation / Screen Flow | BR-4 back-nav data retention | new |
| 65 | BR-4 | Review | Tapping "Submit" on Review screen initiates Email OTP flow | Navigation / Screen Flow | BR-4 | new |

## SECTION 6 — Email OTP Verification

| #  | Refs | Screen | Scenario | Type | Expected-value source | Status |
|----|------|--------|----------|------|-----------------------|--------|
| 66 | AC-7, BR-5 | OTP | OTP email is sent to member's registered email address on Submit | Happy Path | BR-5, BR-7 | new |
| 67 | AC-7, BR-5 | OTP | Correct OTP entered — account created as Active; (1) account appears in listing with Active badge; (2) account is selectable as destination in Fiat Withdrawal flow; (3) all selected currencies immediately usable | Happy Path | BR-5 | new |
| 68 | BR-5 | OTP | Incorrect OTP entered — error shown, member can retry | Negative | BR-5 existing onboarding validation | new |
| 69 | BR-5 | OTP | Expired OTP — member must request a new OTP; existing onboarding OTP has expiry (AO-992 standardises the window; current behaviour asserted without pinning the exact duration) | Negative | BR-5 "follows existing onboarding validation"; AO-992 informational | new |
| 70 | BR-5 | OTP | Multiple incorrect OTP attempts — OTP is invalidated after reaching the attempt limit; member must request a new one (exact threshold is AO-992-governed; assert the lock-out behaviour without pinning to 5) | Boundary | BR-5 "follows existing onboarding validation"; AO-992 informational | new |
| 71 | BR-5 | OTP | Resend OTP — new OTP is sent, previously issued OTP is invalidated; entering the old OTP after a resend returns an error | Negative | BR-5 "follows existing onboarding validation"; AO-992: reissuing OTP does not reset counter but old OTP becomes invalid | new |
| 72 | BR-5 | OTP | OTP screen displays correct UI elements (input field, resend CTA, timer if applicable) | Display / UI | BR-5 / existing onboarding OTP screen | new |
| 73 | BR-5 | Navigation | Tapping Back on OTP screen returns to Review Bank Account screen with all values retained (inferred: OTP is step after Review "Submit"; Review is the logical back-nav target per BR-4/BR-5 flow) | Navigation / Screen Flow | BR-4 back-nav retention + BR-5 flow order | new |

## SECTION 7 — Post-Add Success

| #  | Refs | Screen | Scenario | Type | Expected-value source | Status |
|----|------|--------|----------|------|-----------------------|--------|
| 74 | AC-7, BR-5 | Post-OTP | Newly created account appears in listing with Active status immediately after OTP verification | Happy Path | BR-5, BR-2 | new |
| 75 | AC-18, BR-7 | Post-OTP | Confirmation email received in member's registered test email inbox after successful bank account addition (note: requires test email inbox access to verify) | Happy Path | BR-7 | new |
| 76 | AC-18, BR-7 | Post-OTP | No email notification sent when currency is added to existing account | Negative | BR-7 "Adding or removing a currency does not trigger a separate notification." | new |
| 77 | AC-18, BR-7 | Post-OTP | No email notification sent when currency is removed from existing account | Negative | BR-7 | new |

## SECTION 8 — Bank Account Details (Active)

| #  | Refs | Screen | Scenario | Type | Expected-value source | Status |
|----|------|--------|----------|------|-----------------------|--------|
| 78 | BR-2 | Details (Active) | Bank Account Details page displays all stored fields including full (unmasked) Account Number / IBAN | Display / UI | BR-2: "Bank Account Details page displays full Account Number / IBAN (not masked)" | new |
| 79 | BR-2 | Details (Active) | Correct screen title and all edit CTAs visible for Active account | Display / UI | BR-2 | new |

## SECTION 9 — Edit Label

| #  | Refs | Screen | Scenario | Type | Expected-value source | Status |
|----|------|--------|----------|------|-----------------------|--------|
| 80 | AC-12, BR-6 | Edit Label | Member can edit Label — valid new label saved successfully | Happy Path | BR-6 Edit Label | new |
| 81 | BR-6, ERR-D1 | Edit Label | Label — empty shows error: "Please enter a label." | Validation | ERR-D1 | new |
| 82 | BR-6, ERR-D2 | Edit Label | Label — 31 characters shows error: "Label cannot exceed 30 characters." | Boundary | ERR-D2 | new |

## SECTION 10 — Add Currency

| #  | Refs | Screen | Scenario | Type | Expected-value source | Status |
|----|------|--------|----------|------|-----------------------|--------|
| 83 | AC-13, BR-6 | Add Currency | Member can add a new currency without Email OTP; currency immediately available for Fiat Withdrawal | Happy Path | BR-6 Add Currency | new |
| 84 | AC-13, BR-6 | Add Currency | Newly added currency appears in currency list on Bank Account Details page | Happy Path | BR-6 | new |

## SECTION 11 — Remove Currency

| #  | Refs | Screen | Scenario | Type | Expected-value source | Status |
|----|------|--------|----------|------|-----------------------|--------|
| 85 | AC-14, BR-6 | Remove Currency | Member can remove a currency without Email OTP | Happy Path | BR-6 Remove Currency | new |
| 86 | AC-14, BR-6, ERR-11 | Remove Currency | Remove currency blocked when pending withdrawal for that currency: "You have a {Currency} withdrawal in progress to this account. You can remove it once that withdrawal is complete." | Negative | ERR-11 | new |
| 87 | AC-15, BR-6 | Remove Currency | Save changes button is disabled when member deselects last remaining currency — member cannot save with zero currencies | Negative | BR-6 + dev comment 244968 (button disabled; no error message text confirmed yet) | new |
| 88 | BR-6, ERR-12 | Remove Currency | Attempt to add/remove currency on Disabled account shows error: "This bank account is suspended. Please contact support for assistance." | Negative | ERR-12 | new |

## SECTION 12 — Delete Bank Account

| #  | Refs | Screen | Scenario | Type | Expected-value source | Status |
|----|------|--------|----------|------|-----------------------|--------|
| 89 | AC-16, BR-6 | Delete | Delete confirmation dialog shown with correct content: Header "Delete bank account?" / Message "Removing this bank account will prevent it from being used for future withdrawals. This action won't affect completed transactions." / CTAs Delete + Cancel | Display / UI | BR-6 delete dialog | new |
| 90 | AC-16, BR-6 | Delete | Tapping Cancel on delete dialog dismisses dialog; account remains | Negative | BR-6 | new |
| 91 | AC-16, BR-6 | Delete | Tapping Delete removes account from member listing; account immediately unavailable for Fiat Withdrawal (assert: (1) account absent from listing, (2) account absent from Fiat Withdrawal destination list) | Happy Path | BR-6 | new |
| 92 | AC-16, BR-6, ERR-14 | Delete | Delete blocked when pending withdrawal associated with account: "You have a withdrawal in progress to this account. You can remove it once that withdrawal is complete." | Negative | ERR-14 | new |
| 93 | AC-16, BR-6 | Delete | Deletion requires no Email OTP | Happy Path | BR-6 | new |

## SECTION 13 — Post-Delete State

| #  | Refs | Screen | Scenario | Type | Expected-value source | Status |
|----|------|--------|----------|------|-----------------------|--------|
| 94 | AC-17, BR-6 | Listing | Deleted account not visible in member's bank account listing | Status Transition | BR-6 | new |
| 95 | AC-17 | Post-delete | Deleted account visible in BO under Withdrawal Account with status "Deleted" and Date Deleted timestamp both present and correct | Cross-System Sync | AC-17, BR-6 audit retention; BR-8 | new |

## SECTION 14 — Disabled Account Behaviour

| #  | Refs | Screen | Scenario | Type | Expected-value source | Status |
|----|------|--------|----------|------|-----------------------|--------|
| 96 | AC-11, BR-2 | Listing | Disabled account visible in listing (not hidden) | Status Transition | BR-2 | new |
| 97 | AC-11, BR-2 | Details (Disabled) | Tapping Disabled account row shows error toast (non-clickable behaviour) | Status Transition | BR-2 + ERR-15 | new |
| 98 | BR-1 | Disabled | Disabled account cannot be used for Fiat Withdrawal | Negative | BR-1 DISABLED status definition | new |

## SECTION 15 — Out-of-Scope Constraint (Restricted-Capability)

| #  | Refs | Screen | Scenario | Type | Expected-value source | Status |
|----|------|--------|----------|------|-----------------------|--------|
| 99 | OOS-5 | Details (Active) | Fields other than Label and Currencies cannot be edited (no edit CTA for other fields) | Negative | OOS-5: "Editing any field other than Label and currencies — members remove and re-add." | new |

## SECTION 16 — Back Office Impact

| #  | Refs | Screen | Scenario | Type | Expected-value source | Status |
|----|------|--------|----------|------|-----------------------|--------|
| 100 | AC-19, BR-8 | BO — Withdrawal Account | Maker can view all BR-3 fields in BO under Member Details → Withdrawal Account | Cross-System Sync | BR-8 | new |
| 101 | AC-19, BR-8 | BO — Withdrawal Account | Full (unmasked) Account Number / IBAN visible to Maker in BO | Cross-System Sync | BR-8 | new |
| 102 | BR-8 | BO — Withdrawal Account | Currency list per account visible in BO | Cross-System Sync | BR-8 | new |
| 103 | AC-17, BR-8 | BO — Withdrawal Account | Deleted account visible in BO with Deleted status and Date Deleted | Cross-System Sync | BR-8 audit | new |
| 104 | BR-8 | BO — Withdrawal Account | Active, Disabled and Deleted records all visible in BO | Cross-System Sync | BR-8 | new |

## SECTION 17 — Navigation / Screen Flow

| #  | Refs | Screen | Scenario | Type | Expected-value source | Status |
|----|------|--------|----------|------|-----------------------|--------|
| 105 | BR-1 | Navigation | Add Bank Account entry point via My Account → Withdrawal Accounts → Linked Bank Accounts navigates to listing | Navigation / Screen Flow | BR-1 | new |
| 106 | BR-1 | Navigation | Add Bank Account entry point via Withdrawal → Fiat → Bank Account navigates to listing | Navigation / Screen Flow | BR-1 | new |
| 107 | BR-3 | Navigation | Tapping Back on Add Bank Account form returns to listing | Navigation / Screen Flow | BR-3 | new |
| 108 | BR-4 | Navigation | Tapping Back on Review screen preserves all form values | Navigation / Screen Flow | BR-4 | new |
| 109 | BR-5 | Navigation | Tapping Back on OTP screen returns to Review Bank Account screen with all values retained (inferred from flow order: OTP follows Review "Submit"; Review is the logical back-nav target) | Navigation / Screen Flow | BR-4 data retention + BR-5 flow order | new |

## SECTION 18 — Mobile App Lifecycle

| #  | Refs | Screen | Scenario | Type | Expected-value source | Status |
|----|------|--------|----------|------|-----------------------|--------|
| 110 | BR-3 | Add form | Backgrounding app during form fill — data retained on resume | Mobile App Lifecycle | tc-scenario-guide Mobile App Lifecycle | new |
| 111 | BR-3 | Add form | Kill app during form fill — form cleared/reset on reopen | Mobile App Lifecycle | tc-scenario-guide Mobile App Lifecycle | new |
| 112 | BR-5 | OTP | Background app during OTP flow — OTP timer is server-side and is NOT reset by backgrounding; OTP is valid on resume if still within its validity window; expired if window has passed | Mobile App Lifecycle | AO-992: "Leaving/re-entering the screen / Restarting the application / Switching devices shall not reset the request counter"; server-side timer | new |
| 113 | BR-4 | Review | Kill app on Review screen — no bank account record created | Mobile App Lifecycle | tc-scenario-guide Mobile App Lifecycle | new |
| 114 | BR-6 | Edit | Kill app during edit (label/currency) — unsaved changes discarded | Mobile App Lifecycle | tc-scenario-guide Mobile App Lifecycle | new |
| 115 | BR-5 | OTP | Network interruption during OTP submission — graceful error shown, no duplicate account created | Mobile App Lifecycle | tc-scenario-guide Mobile App Lifecycle | new |

## SECTION 19 — Account Limit Boundary

| #  | Refs | Screen | Scenario | Type | Expected-value source | Status |
|----|------|--------|----------|------|-----------------------|--------|
| 116 | AC-8, BR-1 | Listing | Member with 4 Active accounts can add a 5th account successfully | Boundary | BR-1 limit = 5 | new |
| 117 | AC-8, BR-1 | Listing | Member with 5 Active accounts cannot add a 6th account | Boundary | BR-1 limit = 5 | new |
| 118 | AC-20, BR-1 | Listing | Member with 5 Active + 1 Disabled accounts: limit counted as 5 (Disabled not counted) | Boundary | BR-1 | new |
| 119 | AC-20, BR-1 | Listing | Member with 5 Active + 1 Deleted accounts: limit counted as 5 (Deleted not counted) | Boundary | BR-1 | new |
| 120 | BR-1 | Listing | Member deletes 1 of 5 Active accounts — can immediately add a new account (limit freed) | Boundary | BR-1 | new |

---

## Needs Clarification Summary

All previously flagged items resolved using AO-992 content and ticket logic. No remaining needs-clarification rows.

## Gap Summary

No uncovered AC/BR/ERR IDs. All items appear in at least one row.

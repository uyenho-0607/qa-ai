# TC Plan — AO-306
# [OTC][MobileApp] Personal Onboarding

Generated: 2026-08-21
Updated: 2026-08-21 (Figma review applied)

## Scope Summary

| Items | Count |
|---|---|
| ACs (derived) | 10 (AC-1 – AC-10) |
| BRs | 4 (BR-1 – BR-4) |
| ERRs | 2 in scope (ERR-1, ERR-2); ERR-3/ERR-4 dropped — ID Number not in design |
| Out of scope | AO-992 OTP rate-limiting controls (Backlog) |
| Out of scope | Backoffice Create Member flow (BR-4: no changes required) |
| Out of scope | ERR-3, ERR-4 — ID Number field not in Figma designs or BR-2; confirmed absent |

### Figma Findings Applied

| Finding | Impact |
|---|---|
| Row 6: No "Country not selected" error — CTA disabled until selection made | Row 6 changed from Validation to Navigation/Screen Flow (CTA state) |
| Row 10: Future date not blocked at picker; under-18 validation fires inline | Row 10 updated — wheel picker allows future dates, inline error shown after Done |
| Rows 19/20: ID Number absent from all Figma screens | Dropped — out of scope |
| Row 21: Back → Account Type screen, inputs retained | Resolved — source: Figma Navigation notes |
| New: Country unavailable for registration → inline error | Row 6b added |
| New: Country search no-results state "No countries found" | Row 5b added |
| Progress bar at Step 3 = 30% | Row 3b added |
| Screen title "Tell us about yourself" | Added to row 3 |

---

## Coverage Plan

| # | Refs | Screen | Scenario | Type | Expected-value source | Status |
|---|---|---|---|---|---|---|
| 1 | AC-1, BR-1 | Step 2 — Account Type Selection | Personal Account option is available alongside Business Account | Happy Path | AC-1 (derived from BR-1 user flow) | new |
| 2 | AC-1, AC-2, BR-1 | Step 2 — Account Type Selection | Selecting Personal Account navigates to the Personal Details screen | Navigation / Screen Flow | AC-2, BR-1; Figma Navigation note | new |
| 3 | AC-3, BR-2 | Step 3 — Personal Details | Personal Details screen displays "Tell us about yourself" heading, Country of Residence and Date of Birth as mandatory fields with correct placeholders | Display / UI | AC-3, BR-2; Figma screen title, placeholder "Select country", "DD/MM/YYYY" | new |
| 3b | AC-3, BR-1 | Step 3 — Personal Details | Progress bar shows 30% on Personal Details screen | Display / UI | Figma Progress Bar notes (Step 3 → 30%) | new |
| 4 | AC-4, BR-2 | Step 3 — Country of Residence | Tapping Country of Residence field opens a side sheet with alphabetical country list and search bar | Selection or Reference List | AC-4, BR-2; Figma Country Selection field notes | new |
| 5 | AC-4, BR-2 | Step 3 — Country of Residence | Searching by partial name (e.g. "Sin") filters results in real-time; full match (e.g. "Singapore") shows single result | Selection or Reference List | Figma Search Behavior notes | new |
| 5b | AC-4, BR-2 | Step 3 — Country of Residence | Search with no matching term shows "No countries found" empty state | Empty / No Data | Figma: "No countries found" text | new |
| 5c | AC-4, BR-2 | Step 3 — Country of Residence | Clearing search input restores the full alphabetical country list | Selection or Reference List | Figma Country Selection notes | new |
| 5d | AC-4, BR-2 | Step 3 — Country of Residence | Back button on country side sheet closes sheet and returns to Personal Details without saving any selection | Navigation / Screen Flow | Figma Back Navigation note: "Does not save any selection" | new |
| 6 | AC-3, BR-2 | Step 3 — Personal Details | Continue CTA remains disabled until both Country of Residence and Date of Birth are filled | Navigation / Screen Flow | Figma Validation & Behavior: CTA disabled if any field invalid/unfilled | new |
| 6b | AC-4, BR-2 | Step 3 — Country of Residence | Selecting a country unavailable for registration shows inline error "Sorry, registration is currently unavailable for this country." | Negative | Figma Validation screen — error text visible under Afghanistan selection | new |
| 7 | AC-5, AC-6, BR-2 | Step 3 — Date of Birth | Tapping DOB field opens floating bottom sheet with wheel date picker; tapping Done applies the selected date in DD/MM/YYYY format | Happy Path | AC-5, BR-2; Figma DOB Bottom Sheet notes | new |
| 8 | AC-5, BR-2, ERR-1 | Step 3 — Date of Birth | Continue tapped without selecting DOB → inline error "Please select your date of birth." | Validation | ERR-1 exact message | new |
| 9 | AC-5, BR-2, ERR-2 | Step 3 — Date of Birth | DOB wheel picker allows selecting future dates; after tapping Done with a future date → inline error "You must be at least 18 years old to register for an account." | Negative / Boundary | Figma Validation screen; BR-2 under-18 message | new |
| 10 | AC-6, BR-2 | Step 3 — Date of Birth | DOB resulting in age exactly 17 (e.g. DOB = today − 17 years) → inline error "You must be at least 18 years old to register for an account." and Continue disabled | Boundary | BR-2 exact message; Figma Validation screen | new |
| 11 | AC-6, BR-2 | Step 3 — Date of Birth | DOB resulting in age exactly 18 → no error shown, Continue enabled | Boundary | BR-2 (min age = 18); AC-6 | new |
| 12 | AC-3, BR-2 | Step 3 — Personal Details | User inputs retained when navigating back from later step to Personal Details | Navigation / Screen Flow | Figma notes: "User inputs are retained if they navigate back to the previous step" | new |
| 13 | AC-1, AC-2, BR-1 | Step 3 — Personal Details | Back from Personal Details returns to Account Type Selection screen, inputs retained | Navigation / Screen Flow | Figma Navigation: "Back: Returns to the Account Type screen while preserving any entered information" | new |
| 14 | AC-7, BR-1 | Steps 4–7 — Existing Flow | After valid Personal Details submitted, member proceeds to Setup Email step | Navigation / Screen Flow | AC-7, BR-1 | new |
| 15 | AC-8, BR-3 | Account Created | Upon successful account creation, account type is displayed as Personal | Happy Path | AC-8, BR-3 | new |
| 16 | AC-8, BR-3 | Account Created | Upon successful account creation, KYC (not KYB) verification journey is triggered | Happy Path / Cross-System Sync | AC-8, BR-3 | new |
| 17 | AC-9, BR-4 | Backoffice — Member Details | Country of Residence is displayed in Backoffice Member Details page after Personal account creation | Cross-System Sync | AC-9, BR-4 | new |
| 18 | AC-10, BR-4 | Backoffice — Create Member | Backoffice Create Member flow contains no Country of Residence field | Negative | AC-10, BR-4 | new |
| 19 | AC-5, BR-2 | Step 3 — Personal Details | App backgrounded during Personal Details form fill — data retained on resume | Mobile App Lifecycle | Figma: "User inputs are retained"; standard mobile lifecycle | new |
| 20 | AC-5, BR-2 | Step 3 — Personal Details | App killed during Personal Details form fill — form cleared on reopen | Mobile App Lifecycle | Standard mobile lifecycle behaviour | new |

---

## Coverage Trace

| Scope Item | Covered by rows |
|---|---|
| AC-1 | 1, 2 |
| AC-2 | 2, 13 |
| AC-3 | 3, 3b, 6, 8, 12 |
| AC-4 | 4, 5, 5b, 5c, 5d, 6b |
| AC-5 | 7, 8, 9, 19, 20 |
| AC-6 | 9, 10, 11 |
| AC-7 | 14 |
| AC-8 | 15, 16 |
| AC-9 | 17 |
| AC-10 | 18 |
| BR-1 | 1, 2, 13, 14 |
| BR-2 | 3, 4, 5, 5b, 5c, 5d, 6, 6b, 7, 8, 9, 10, 11, 12, 19, 20 |
| BR-3 | 15, 16 |
| BR-4 | 17, 18 |
| ERR-1 | 8 |
| ERR-2 | 9, 10 |
| ERR-3, ERR-4 | dropped — ID Number not in scope |

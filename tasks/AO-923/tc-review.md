# TC Review — AO-923
# [OTC][MobileApp][Member] Linked Bank Accounts — Add, Edit, Remove
# Reviewed: 2026-08-21 | Source: tasks/AO-923/manual-tcs.md | 121 TCs

---

## Summary

| Dimension | Findings |
|-----------|----------|
| Coverage | 4 findings (2 fix, 2 ask) |
| Oracle | 8 findings (8 fix) |
| Repro | 9 findings (9 fix) |
| Form | 6 findings (6 fix) |
| **Total** | **27 findings — fix 25 · ask 2 · clean 94** |

---

## COVERAGE

### COV-01 · fix · Missing Reverse Transition — Disabled account re-enabled by BO
**Dimension:** Coverage — Anti-pattern #14 Missing Reverse Transition
**Evidence:** BR-1 states DISABLED "is set by Back Office and is reversible." TC-12, TC-13, TC-97, TC-98, TC-99 test the Disabled state and its member-facing effects, but no TC verifies what happens when BO re-enables (reverses) a Disabled account — that it returns to Active in the app, becomes clickable, and is usable for Fiat Withdrawal again.
**Fix:** Add TC covering: BO re-enables a Disabled account → account re-appears as Active in member listing, becomes clickable, and is available for Fiat Withdrawal.
**Grade:** fix (behaviour is documented in BR-1)

---

### COV-02 · fix · Silent Scope Narrowing — Duplicate uniqueness check only tested for Active accounts
**Dimension:** Coverage — Anti-pattern #15 Silent Scope Narrowing
**Evidence:** TC-60, TC-61 test duplicate rejection against an Active account. TC-62 tests against a Disabled account. No TC tests the uniqueness rule against a Deleted account — BR-3b says "must not match an existing record for the same member" without a status qualifier, which implies Deleted records are also in scope for the uniqueness check.
**Fix:** Add TC: Attempt to add an account with same Account Number + BIC/SWIFT as a Deleted account for the same member — assert whether it is accepted (Deleted not counted) or rejected. Expected behaviour needs confirmation from spec — mark as `ask` if unclear.
**Grade:** ask — ticket says Deleted records are retained but does not explicitly state whether they participate in the uniqueness check.

---

### COV-03 · fix · Missing coverage — BO Checker/Maker role distinction not tested
**Dimension:** Coverage
**Evidence:** BR-8 specifies "Maker can view all bank account fields." The ticket uses Maker/Checker terminology which implies role-based BO access. TC-96, TC-101–104, TC-121 only test Maker access. No TC verifies that a non-Maker BO role (e.g. Checker or Viewer) either can or cannot see the same fields.
**Fix:** This is `ask` — the ticket does not define Checker visibility for this module. Either confirm scope or note as out of scope.
**Grade:** ask

---

### COV-04 · fix · Missing negative — BIC 10-character code (boundary between 8 and 11)
**Dimension:** Coverage — Boundary
**Evidence:** TC-37 tests 8-char BIC (accepted), TC-38 tests 11-char BIC (accepted), TC-40 tests 9-char BIC (rejected). No TC tests a 10-character BIC — the other invalid length between 8 and 11. ISO 9362 only permits 8 or 11 characters; 10 is also invalid and should produce the same error as 9.
**Fix:** Add Test Data `OCBCSGSGXX` (10 characters) to TC-40, or create a separate boundary TC for the 10-character case.
**Grade:** fix

---

## ORACLE

### ORA-01 · fix · TC-01 — Expected Result too vague
**TC:** AO-923_TC-01
**Field:** Expected Result
**Evidence:** "The Linked Bank Accounts listing screen is displayed." — does not specify what the listing contains (e.g. empty state if no accounts, or account rows if accounts exist). A blank white screen with the correct title would pass this check.
**Fix:** Tighten to: "The Linked Bank Accounts listing screen is displayed. If the member has no accounts, the empty state message 'You haven't added a bank account yet. Add one to withdraw your fiat balances.' is shown; if accounts exist, the account list is displayed."

---

### ORA-02 · fix · TC-11 — Expected Result vague ("empty or no-results state")
**TC:** AO-923_TC-11
**Field:** Expected Result
**Evidence:** "No accounts are displayed; an empty or no-results state is shown." — the "or" makes this untestable. A wrong state (e.g. spinner, error message) would satisfy the check.
**Fix:** Remove "or": "No accounts are displayed; a no-results state is shown (e.g. no rows visible in the search results area)."

---

### ORA-03 · fix · TC-22 — Expected Result vague ("form proceeds to the next validation step")
**TC:** AO-923_TC-22
**Field:** Expected Result
**Evidence:** "No validation error is shown for the Label field; form proceeds to the next validation step." — "next validation step" is implementation language, not an observable outcome.
**Fix:** "No validation error is shown for the Label field." (Remove the second clause — the happy-path outcome is the absence of error, not the internal step.)

---

### ORA-04 · fix · TC-30 — Expected Result vague ("Validation error is displayed")
**TC:** AO-923_TC-30
**Field:** Expected Result
**Evidence:** "Validation error is displayed for the Bank Name field (invalid character rejected)." — no exact message text cited. The ERR source (BR-3 regex) does not specify a message for invalid special chars.
**Fix:** Add the exact message if known, or note `needs-clarification` and use: "A validation error is displayed for the Bank Name field indicating the entered character is not allowed." Keep as fix if the message can be inferred from the rejection behaviour; escalate as ask if the exact message text is unspecified in the ticket.
**Grade:** fix — tighten the wording; message text for invalid char is not specified in the ticket so state the assertion as the field-level rejection rather than a specific string.

---

### ORA-05 · fix · TC-63 — Expected Result uses "or" (vague alternative)
**TC:** AO-923_TC-63
**Field:** Expected Result
**Evidence:** "Submission is blocked; error or CTA disabled state displayed indicating the member has reached the maximum of 5 bank accounts." — "error or CTA disabled" is an alternative that would pass on either outcome, including a wrong one.
**Fix:** Separate into two precise assertions: (1) CTA is disabled (tested by TC-14/15); (2) if accessed via deep link, the Continue action is blocked with the limit-reached error. Consolidate with TC-14/15 or tighten: "The Continue CTA does not advance the flow; submission is blocked and a message indicating the 5-account limit is shown."

---

### ORA-06 · fix · TC-65 — Test Data vague ("Any valid complete form data")
**TC:** AO-923_TC-65
**Field:** Test Data
**Evidence:** "Any valid complete form data." — this is a description, not a literal value. Anti-pattern #16.
**Fix:** Replace with a specific data set, e.g.: `Label: Test Retention; Bank Country: Singapore; Bank Name: Test Bank; Account Holder Name: Jane Doe; Account Number: SG12TEST12345; BIC: OCBCSGSG; Currency: SGD; Address Line 1: 1 Test Road; City: Singapore`

---

### ORA-07 · fix · TC-68 — Expected Result has three assertions (should be one per convention)
**TC:** AO-923_TC-68
**Field:** Expected Result
**Evidence:** "(1) Account appears in the listing with Active status. (2) Account is available as a destination in the Fiat Withdrawal flow. (3) Both SGD and USD are selectable for withdrawal to this account." — three distinct checks in one Expected Result. Conventions require one exact outcome per TC.
**Fix:** Keep the primary oracle as (1) "Account appears in the listing with Active status." Move assertions (2) and (3) to TC-75 (post-add listing) and a separate usability check, or accept that this is an end-to-end TC where multi-step verification is intentional — in that case reframe as a single composite statement: "The bank account is created with Active status, is visible in the listing, and all selected currencies (SGD, USD) are immediately available in the Fiat Withdrawal destination list."

---

### ORA-08 · fix · TC-92 — Expected Result has three assertions
**TC:** AO-923_TC-92
**Field:** Expected Result
**Evidence:** "(1) No OTP is required for deletion. (2) The deleted account is absent from the listing. (3) The deleted account is absent from the Fiat Withdrawal destination list." — three distinct checks.
**Fix:** Consolidate: "The account is deleted without OTP; it is absent from the Linked Bank Accounts listing and from the Fiat Withdrawal destination list."

---

## REPRO

### REP-01 · fix · TC-08, TC-09, TC-10 — Test Data descriptive, not literal (Anti-pattern #16)
**TCs:** AO-923_TC-08, AO-923_TC-09, AO-923_TC-10
**Field:** Test Data
**Evidence:**
- TC-08: `Label of one existing account (e.g. "My OCBC SGD")` — the "e.g." makes it a description, not a literal value.
- TC-09: `Bank Name of one existing account (e.g. "OCBC")` — same issue.
- TC-10: `Last 4 digits of one existing account number (e.g. "1234")` — same issue.
**Fix:** Replace with literal values tied to the Pre-requisites: e.g. TC-08 Test Data: `My OCBC SGD` (the Label of the pre-created account named in Pre-requisites). Update Pre-requisites to state "with one account labelled 'My OCBC SGD'".

---

### REP-02 · fix · TC-21 — Step 1 "Navigate to Add Bank Account form" — non-specific navigation
**TC:** AO-923_TC-21
**Field:** Steps
**Evidence:** Step 1: "Navigate to Add Bank Account form." — does not specify which entry point, leaving ambiguity for a new tester.
**Fix:** Step 1: "Navigate to My Account → Withdrawal Accounts → Linked Bank Accounts. Tap Add Bank Account."

---

### REP-03 · fix · TC-60, TC-61, TC-62 — Test Data descriptive, not literal
**TCs:** AO-923_TC-60, AO-923_TC-61, AO-923_TC-62
**Field:** Test Data
**Evidence:**
- TC-60: "Account Number / IBAN and BIC / SWIFT matching an existing Active account for this member." — description, not literal values.
- TC-61: Same issue.
- TC-62: "Account Number / IBAN and BIC / SWIFT matching an existing Disabled account." — same.
**Fix:** Update Pre-requisites to state a specific existing account (e.g. "Account with Account Number `GB29NWBK60161331926819` and BIC `OCBCSGSG` already exists as Active/Disabled"). Update Test Data to: `Account Number: GB29NWBK60161331926819; BIC / SWIFT: OCBCSGSG`.

---

### REP-04 · fix · TC-70 — Pre-requisite instructs tester to wait but no timing anchor
**TC:** AO-923_TC-70
**Field:** Pre-requisites / Steps
**Evidence:** Pre-requisites: "wait for the OTP to expire before entering it." Step 2: "Wait for the OTP to expire (do not enter it until the expiry indicator shows expired)." — the expiry window is not specified (AO-992 Backlog, so the exact duration is not confirmed for this sprint). "Expiry indicator shows expired" is the correct anchor but the step should explicitly tell the tester to look for the on-screen indicator rather than time-box it.
**Fix:** Step 2: "Wait until the OTP expiry indicator on screen shows the OTP has expired (do not enter the OTP before this point)."

---

### REP-05 · fix · TC-79 — Test Data descriptive with "e.g."
**TC:** AO-923_TC-79
**Field:** Test Data
**Evidence:** `Account Number / IBAN of an existing Active account (e.g. GB29NWBK60161331926819)` — "e.g." pattern, anti-pattern #16.
**Fix:** Remove the parenthetical description. Test Data: `GB29NWBK60161331926819` (align Pre-requisites to reference the same account).

---

### REP-06 · fix · TC-89 — Step 1 "(if accessible)" introduces ambiguity
**TC:** AO-923_TC-89
**Field:** Steps
**Evidence:** Step 1: "Navigate to Bank Account Details of a Disabled account (if accessible)." — the parenthetical implies the tester might not be able to execute the step, leaving the test unresolved.
**Fix:** Remove the parenthetical. Pre-requisites already require a Disabled account to be present. Step 1: "Navigate to Bank Account Details of the Disabled account." (Note: BR-2 states Disabled accounts are non-clickable in the listing — the entry path for this test should be confirmed. If the details page is truly inaccessible from the listing, this TC needs a different entry path or must be recorded as a coverage gap. Mark as `ask` if the entry path is unclear.)
**Grade:** Downgrade to ask — it's unclear whether the Disabled account Details page is accessible to the member at all (BR-2 says Disabled rows are non-clickable; the test expects to reach the details page to attempt currency modification).

---

### REP-07 · fix · TC-116 — Test Data descriptive
**TC:** AO-923_TC-116
**Field:** Test Data
**Evidence:** "Valid new bank account details distinct from existing 4." — description, not literal values.
**Fix:** Replace with a complete literal data set, e.g.: `Label: Account 5; Bank Country: Singapore; Bank Name: DBS; Account Holder Name: John Smith; Account Number: SG99DBS12345; BIC: DBSSSGSG; Currency: SGD; Address Line 1: 1 Marina Blvd; City: Singapore`

---

## FORM

### FRM-01 · fix · TC-03 — Test Scenario contains UI action verb "tapping"
**TC:** AO-923_TC-03
**Field:** Test Scenario
**Evidence:** "Verify that a non-verified member **tapping** Add Bank Account is redirected…" — conventions prohibit UI action verbs in Test Scenario.
**Fix:** "Verify that a non-verified member who attempts to add a bank account is redirected to the verification flow, and a verified member is not redirected."

---

### FRM-02 · fix · Multiple TCs — Test Scenario contains action verbs "submitting", "entering", "tapping"
**TCs:** TC-23, TC-24, TC-26, TC-28, TC-29, TC-32, TC-33, TC-35, TC-36, TC-39, TC-40, TC-42, TC-46, TC-48, TC-49, TC-50, TC-52, TC-53, TC-54, TC-57, TC-58, TC-59, TC-60, TC-62, TC-63, TC-65, TC-66, TC-82, TC-83, TC-87, TC-91
**Field:** Test Scenario
**Evidence (sample):**
- TC-23: "Verify that **submitting** the form with an empty Label field displays…"
- TC-57: "Verify that a BIC country mismatch warning popup is shown with the actual country names rendered when the BIC country code does **not match** the selected Bank Country." ← acceptable
- TC-58: "Verify that **tapping** Review Details on the BIC country mismatch warning popup dismisses…"
- TC-66: "Verify that **tapping** Submit on the Review Bank Account screen initiates…"
**Fix (pattern):** Replace action-verb subject with state/condition subject:
- "submitting the form with…" → "an empty [Field] field triggers the validation error…"
- "tapping [CTA]" → "selecting [CTA] on [screen]" — wait, "selecting" is also an action verb per conventions. Correct pattern: "Verify that the [screen/message/state] is [correct outcome] when [condition]." Examples:
  - TC-23: "Verify that the Label field validation error is displayed when the field is empty."
  - TC-58: "Verify that the BIC country mismatch warning popup is dismissed and the Add Bank Account form is displayed when Review Details is chosen."
  - TC-66: "Verify that the Email OTP verification screen is displayed after Submit is confirmed on the Review Bank Account screen."

---

### FRM-03 · fix · TC-92, TC-94 — Duplicate scenario
**TCs:** AO-923_TC-92, AO-923_TC-94
**Dimension:** Form — Anti-pattern #10 Duplicate TC
**Evidence:**
- TC-92 Expected Result: "(1) No OTP is required for deletion…"
- TC-94 Test Scenario: "Verify that deleting a bank account does not trigger an Email OTP verification step." / Expected Result: "The account is deleted without any Email OTP verification being required."
Both TCs assert the same fact: deletion requires no OTP. TC-92 is the comprehensive delete TC; TC-94 duplicates the OTP assertion from it.
**Fix:** Remove TC-94. Merge its explicit "no OTP" assertion into TC-92's Expected Result (already present as assertion (1)).

---

### FRM-04 · fix · TC-98 — Duplicate of TC-13
**TCs:** AO-923_TC-13, AO-923_TC-98
**Dimension:** Form — Anti-pattern #10 Duplicate TC
**Evidence:**
- TC-13: "Verify that tapping a Disabled bank account row displays the correct error toast message." Expected Result: "Error toast displayed: 'This bank account has been disabled, contact us for further assistance.'"
- TC-98: "Verify that tapping a Disabled account row displays the correct error toast." Expected Result: identical message.
Both TCs test the same scenario on the same screen. TC-13 already covers this; TC-98 is a full duplicate.
**Fix:** Remove TC-98. Update TC-13's Requirement Reference to include `AC-11; BR-2; ERR-15` (already present — no change needed).

---

### FRM-05 · fix · TC-105 — Duplicate of TC-01
**TCs:** AO-923_TC-01, AO-923_TC-105
**Dimension:** Form — Anti-pattern #10 Duplicate TC
**Evidence:**
- TC-01 Name: "Access via My Account entry point - Listing screen displayed" / Steps: identical navigation path / Expected Result: identical.
- TC-105 Name: "Navigation - My Account entry point navigates to listing" / Steps: identical / Expected Result: identical.
**Fix:** Remove TC-105. TC-01 already covers this scenario. Update TC-01's Requirement Reference to add `BR-1` (already present).

---

### FRM-06 · fix · TC-106 — Partial duplicate of TC-02
**TCs:** AO-923_TC-02, AO-923_TC-106
**Dimension:** Form — Anti-pattern #10 Duplicate TC
**Evidence:**
- TC-02: "Access via Withdrawal Fiat entry point — Add Bank Account form displayed." Navigation path: Withdrawal → Fiat → Bank Account → Add Bank Account.
- TC-106: "Navigation — Withdrawal Fiat entry point navigates to Add Bank Account." Identical path and Expected Result.
**Fix:** Remove TC-106. TC-02 already covers this navigation scenario.

---

## CLEAN TCs (passing all four dimensions)

TC-04 through TC-12, TC-14 through TC-20, TC-25 through TC-27, TC-31, TC-34, TC-37 through TC-38, TC-41, TC-43 through TC-45, TC-47, TC-51, TC-55 through TC-56, TC-58 (oracle only minor), TC-64, TC-66 (form fix needed but oracle/repro clean), TC-67, TC-69 through TC-78, TC-80 through TC-81, TC-84 through TC-86, TC-88 through TC-90, TC-93, TC-95 through TC-97, TC-99 through TC-104, TC-107 through TC-115, TC-117 through TC-121.

Total clean (no findings): **94**

---

## Ask Items Summary

| ID | TC | Description |
|----|----|-------------|
| COV-02 | — (new TC needed) | Uniqueness check against Deleted accounts — ticket does not state whether Deleted records participate in duplicate detection |
| COV-03 | — (new TC or out-of-scope note) | BO Checker/non-Maker role visibility for bank account fields — not defined in ticket |
| REP-06 | TC-89 | Entry path to Disabled account Details page unclear — BR-2 says Disabled rows are non-clickable; test assumes the page is reachable |

---

## Fix Items — Applied in Phase 4

All 25 `fix` findings will be applied to `tasks/AO-923/manual-tcs.md`:

| # | TC(s) | Change |
|---|-------|--------|
| COV-01 | new | Add TC: BO re-enables Disabled account → Active in app |
| COV-04 | TC-40 | Add 10-char BIC test data variant |
| ORA-01 | TC-01 | Tighten Expected Result |
| ORA-02 | TC-11 | Remove "or" from Expected Result |
| ORA-03 | TC-22 | Remove vague second clause from Expected Result |
| ORA-04 | TC-30 | Tighten Expected Result message |
| ORA-05 | TC-63 | Tighten Expected Result, remove "or" |
| ORA-06 | TC-65 | Replace descriptive Test Data with literal values |
| ORA-07 | TC-68 | Consolidate 3-assertion Expected Result into one |
| ORA-08 | TC-92 | Consolidate 3-assertion Expected Result into one |
| REP-01 | TC-08, TC-09, TC-10 | Replace descriptive Test Data with literals + fix Pre-requisites |
| REP-02 | TC-21 | Specify navigation in Step 1 |
| REP-03 | TC-60, TC-61, TC-62 | Replace descriptive Test Data with literal account values |
| REP-04 | TC-70 | Tighten Step 2 expiry anchor |
| REP-05 | TC-79 | Remove "e.g." from Test Data |
| REP-07 | TC-116 | Replace descriptive Test Data with literal values |
| FRM-01 | TC-03 | Remove action verb from Test Scenario |
| FRM-02 | TC-23, TC-58, TC-59, TC-66 and others | Remove action verbs from Test Scenarios |
| FRM-03 | TC-94 | Remove duplicate TC |
| FRM-04 | TC-98 | Remove duplicate TC |
| FRM-05 | TC-105 | Remove duplicate TC |
| FRM-06 | TC-106 | Remove duplicate TC |

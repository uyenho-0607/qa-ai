# TC Naming Reference — Predefined Modules, Sub-modules & Features

Source: https://docs.google.com/spreadsheets/d/16R1Aov9dDdl9j9LNxvr0LeMcxslas_KoAQUyFLP9SMI/edit?gid=841145538

---

## Desktop (Backoffice)

> All modules in this section run in the Backoffice. Default Configuration = **`Admin BO`**.

### Login
_No sub-modules._

| Feature | Covers |
|---------|--------|
| Input | Email field, password field |
| Authentication | Credential check, unauthorized, account suspension (failed attempts → locked) |
| Session | Multi-session, session expiry, session token |
| 2FA | All 2FA-related flows |

### Members
_No sub-modules. Configuration = `Admin BO` (this module lives in the Backoffice, not the mobile app)._

| Feature | Covers |
|---------|--------|
| Listing | Pagination, data display, table header, empty state |
| Filter | Filters, search, sorting |
| Creation | Creation modal required fields, email field |
| Details | Member profile, recent actions, verification tab, withdrawal accounts |
| Edit | Edit, Edit Verification Status, Edit Sumsub ID, Edit Remarks modals |
| Permission | Page permission, add/update/delete/view permission |
| Actions | Resend verification, status update |
| Webhook | KYC/KYB webhook events |

### Balances
_No sub-modules._

| Feature | Covers |
|---------|--------|
| Listing | Pagination, data display, table header, empty state |
| Filter | Filters, search, sorting |
| Create Balance | Creation modal/drawer checks, field validation |
| Export | Export file, export data |
| Permission | Page permission, add/update/delete/view permission |
| Logic | Balance update, pending balance logic, total balance sum calculation |

### OTC
_No sub-modules._

| Feature | Covers |
|---------|--------|
| Listing | Pagination, data display, table header, empty state |
| Filter | Filters, search, sorting |
| Creation | Required fields, sell currency required field |
| Edit | Edit sell amount, upload attachment |
| Details | Top section: Type, Amount, Currency, Status; Timeline |
| Logic | Calculation logic, ID assignment, status transition flow |
| Permission | Page permission, add/update/delete/view permission |
| Export | Export file, export data |

### Transactions
_No sub-modules._

| Feature | Covers |
|---------|--------|
| Listing | Pagination, data display, table header, empty state |
| Filter | Filters, search, sorting |
| Details | Top section: Type, Amount, Currency, Status; Timeline |
| Export | Export file, export data |
| Logic | Status transition flows |

### Users
_No sub-modules._

| Feature | Covers |
|---------|--------|
| Creation | Required selection, duplicate username |
| Listing | Pagination, data display, table header, empty state |
| Filter | Filters, search, sorting |
| Actions | Edit email, reset password, deactivate user |
| Permission | Page permission, add/update/delete/view permission |

### Action Required

| Sub-module | Feature | Covers |
|------------|---------|--------|
| Balance Approvals | Permission | Page permission, add/update/delete/view permission |
| Balance Approvals | Details | Top section: Type, Amount, Currency, Status; Timeline |
| Balance Approvals | Logic | Status-based visibility rules |
| OTC Approvals | Logic | Pending status display, reject balance returned |
| OTC Approvals | Permission | Page permission, add/update/delete/view permission |
| Unidentified | Permission | Page permission, add/update/delete/view permission |

### Reports

| Sub-module | Feature | Covers |
|------------|---------|--------|
| Balance Statement | Listing | Pagination, data display, table header, empty state |
| Balance Statement | Filter | Filters, search, sorting |
| Balance Statement | Export | Export file, export data |
| Balance Statement | Logic | Balance calculation, transacted amount updates |

### Configuration

| Sub-module | Feature | Covers |
|------------|---------|--------|
| Currency Pairs | Listing | Pagination, data display, table header, empty state |
| Currency Pairs | Filter | Filters, search, sorting |
| Currency Pairs | Creation | Base currency required selection, pairs preview |
| Currency Pairs | Actions | Deactivate, activate, confirmation modal |
| Currency Pairs | Logic | Inactive impact, pending convert reject-only |
| Currency Pairs | Permission | Page permission, add/update/delete/view permission |
| Markup Rules | Listing | Pagination, data display, table header, empty state |
| Markup Rules | Filter | Filters, search, sorting |
| Markup Rules | Creation | — |
| Markup Rules | Details | View active/inactive rule, system default rule |
| Markup Rules | Edit | Pre-filled form, Rule Name, Buy/Sell Markup, Currency Pair |
| Markup Rules | Action | Activate, deactivate |
| Markup Rules | Permission | Page permission, add/update/delete/view permission |
| Markup Rules | Session | Edit drawer expiry popup |
| Markup Rules | Logic | Buy/Sell Markup full calculation, zero markup no spread profit |

---

## App (Mobile)

> All modules in this section run on the mobile app. Default Configuration = **`Android app; iOS app`** (or split if platform-specific).

### Sign Up
_No sub-modules._

| Feature | Covers |
|---------|--------|
| Passcode | Passcode setup, entry validation, masking, toggle visibility |
| Biometric | Biometric setup, enable/disable, fallback to passcode |
| Member Name | Screen display, First/Last Name field validation, navigation |
| MemberProfileSelection | Screen display, Personal/Business type selection, navigation |
| Personal Detail | Screen display, field validation, navigation |
| Business Detail | Screen display, field validation, navigation |
| Setup Email | Screen display, email field validation, navigation |
| Email OTP Validation | OTP auto-validation, navigation |
| Setup Password | Screen display, password policy validation, toggle visibility, Confirm Password match, Continue button |
| Setup Phone Number | Screen display, phone field validation, Send Code button |
| Phone Number OTP Validation | OTP auto-validation, Continue button |
| PostSubmission | Account created screen display, BO member reflection, navigation to Home |

### Splash Screen
_No sub-modules._

| Feature | Covers |
|---------|--------|
| Display | Visual, duration, orientation, non-interactive, triggers, transitions |
| Routing | Auth routing and end-to-end flows |
| Compatibility | Device/OS testing |

### Home
_No sub-modules._

| Feature | Covers |
|---------|--------|
| Verification | Sumsub verification, KYB/KYC SDK |

### Convert
_No sub-modules._

| Feature | Covers |
|---------|--------|
| Input | Form fields: Amount, Currency chips, Rate Display, Review Button, Bottom Sheet, Keyboard state, display precision |
| ReviewScreen | Confirmation screen display, navigation |
| PostSubmission | Success/Failure screens, BO check for txn success on mobile |
| App Lifecycle | Foreground, background, and terminated states |
| Logic | Rate refresh, rate precision, calculation, rounding |

### Withdrawal

| Sub-module | Feature | Covers |
|------------|---------|--------|
| Crypto | CryptoAddressesScreen | Account list: Active, Disabled, unsupported currency |
| Crypto | Input | Amount input: Amount, currency chip, balance display, Continue button |
| Crypto | ReviewScreen | Withdrawal details display, navigation |
| Crypto | PostSubmission | OTP verification, Success/Failure screens, confirmation email, BO check, Recent Transactions |
| Crypto | App Lifecycle | Foreground, background, and terminated states |
| Crypto | Logic | Rounding |
| Fiat | Input | Amount input: Amount, currency chip, balance display, Continue button |
| Fiat | BankAccountScreen | Account list: Active, Disabled, unsupported currency |
| Fiat | ReviewScreen | Withdrawal details display, navigation |
| Fiat | PostSubmission | OTP verification, Success/Failure screens, confirmation email, BO check, Recent Transactions |
| Fiat | App Lifecycle | Foreground, background, and terminated states |
| Fiat | Logic | Rounding |

### Activity
_No sub-modules._

| Feature | Covers |
|---------|--------|
| Listing | Pagination, data display, table header, empty state |
| Filter | Filters, search, sorting |
| Display | Amount format, color, icons, titles, decimal display rules, no-transactions state |
| Transaction Details | Transaction types, display |

### Wallet
_No sub-modules._

| Feature | Covers |
|---------|--------|
| Listing | Pagination, data display, table header, empty state |
| Filter | Filters, search, sorting |
| Add Currency | — |
| Logic | Calculation, balance updated |
| Refresh | Balance refresh, page refresh, rate refresh |

### Account

| Sub-module | Feature | Covers |
|------------|---------|--------|
| _(none)_ | Logout | Logout, access token |
| Security & Privacy | Biometric & Passcode | Login validation, credential check, unauthorized, disabled/suspended account login |
| Security & Privacy | Password | Change password flow, current password validation, new password confirmation |
| Withdrawal Accounts | Crypto addresses | Listing, add crypto address (form validation, review, Email OTP), view/edit/delete |
| Withdrawal Accounts | Linked bank accounts | Listing, add bank account (form validation, review, Email OTP), view/edit/delete |

### Login
_No sub-modules._

| Feature | Covers |
|---------|--------|
| Input | Email field, password field |
| Passcode | Passcode field, entry, validation, failure counter, session rules |
| Biometric | FaceID/Fingerprint unlock — auto-prompt, fallback, failure threshold |
| Authentication | Login validation, credential check, unauthorized, disabled/suspended account, suspension mechanism, session logout, counter reset on recovery |
| Forgot Password | Email input, OTP verification, password reset, OTP validity & resend cooldown, password policy, account recovery |
| Failed Attempt Counter | Attempt 1–4 warnings, attempt 5 lockout, counter reset, independent per account |
| Device Lock | 10 attempts within 15 min, 30 min cooldown, message priority |

# OTC Shared Rules — Domain Knowledge

Cross-platform rules shared between Back Office and Mobile App.
Search syntax: grep `#tag keyword` to pull only relevant entries.
Tags: `#rule` `#error` `#field` `#integration` `#status` `#scope`

---

## Password Policy (all platforms)

#rule    Password min length | 8 characters
#rule    Password requirements | at least 1 uppercase (A–Z), 1 lowercase (a–z), 1 number (0–9), 1 special character
#rule    Password max length | 100 characters
#error   Password — weak/common | "Your password is not strong enough. To secure your account, avoid common words, names, dates and repeating characters."
#error   Password — empty | "Please enter your password." (mobile) | "Please enter your password." (BO)
#error   Password — max length exceeded | "Maximum 100 characters allowed."
#error   Confirm password — mismatch | "Password does not match."

---

## OTP Rules (shared across Email OTP and Phone OTP flows)

#rule    OTP length | 6 digits, numeric only
#rule    OTP validity | 5 minutes from time sent
#rule    OTP resend cooldown | 1 minute between resend requests
#rule    OTP max incorrect attempts | 10 consecutive incorrect → invalidated, must request new code
#rule    OTP resend invalidates previous | old OTP no longer valid after resend
#rule    OTP partial input | does not trigger validation (system waits for 6th digit)
#rule    OTP max send limit | 500 OTPs per session (email) | 500 OTPs per session (SMS) — configurable
#error   OTP — incorrect | "Your verification code is incorrect, please try again."
#error   OTP — expired | "Your verification code has expired, please request a new code."
#error   OTP — max attempts | "You have reached the maximum number of incorrect verification code attempts. Please request a new code."
#error   OTP — non-numeric input | not accepted, does not appear in field

---

## Email Field Rules (shared)

#rule    Email max length | 100 characters
#rule    Email uniqueness | unique per platform (BO users and Mobile members share uniqueness check)
#error   Email — empty | "Please enter an email." (BO create member/user) | "Please enter your email." (mobile login/forgot password)
#error   Email — invalid format | "Please enter a valid email to proceed."
#error   Email — duplicate (member) | "This email address is already registered. Please log in to your existing account."
#error   Email — duplicate (BO create) | "This email already exists."
#error   Email — max length | "Maximum 100 characters allowed."

---

## Member / Account Statuses (shared)

#status  Active | normal operating state | can log in, can be selected in BO dropdowns
#status  Disabled (BO) | admin action | cannot log in | cannot recover via Forgot Password | shown as Disabled in BO
#status  Suspended (Mobile) | caused by max failed login attempts | cannot log in | recoverable via Forgot Password | shown as Suspended in BO Member Details
#rule    Suspended vs Disabled | Suspended = max login failures (recoverable) | Disabled = admin action (not recoverable via app)
#rule    BO Maker can activate Suspended member | via "Activate" action button in Member Details

---

## Third-Party Integrations

#integration  Sumsub | KYC verification (Personal accounts) + KYB verification (Business accounts) | third-party, do not test internal Sumsub flow details
#integration  Sumsub | entry point only: popup on Home after account creation, skippable | Sumsub config drives the journey
#integration  Twilio | SMS OTP delivery for phone verification | country support varies — see country master list; unsupported countries → Country Code pre-fill is empty
#integration  UTGL | external OTC system | generates Reference ID for OTC Credit/Debit/Commission transactions
#integration  Fireblocks | crypto wallet custody | generates deposit addresses + memo/tag | returns Fireblocks Transaction ID, Source Address, Transaction Hash on withdrawal
#integration  Fireblocks | deposit/withdrawal currency-network availability | a pair must be active in BFG AND enabled in Fireblocks to appear in the app
#integration  CMC (CoinMarketCap) | reference rate source for currency conversion | configured pair direction determines the rate shown to members
#scope   Sumsub | KYC/KYB journey details out of scope | only assert entry point and integration trigger
#scope   Twilio | country availability out of scope | only assert pre-fill behaviour based on Twilio support
#scope   Fireblocks | address generation internals out of scope | assert only the address/memo returned and its stability per member + currency-network pair
#scope   CMC | rate feed accuracy out of scope | assert only that the configured pair direction drives the displayed rate

---

## Country List Rules

#rule    Country master list | same list used for Country of Registration (Business) and Country of Residence (Personal) | configured per environment
#rule    Country of Registration | used in Business onboarding Step 3 | pre-fills Phone Country Code in Step 6
#rule    Country of Residence | used in Personal onboarding Step 3 | pre-fills Phone Country Code in Step 6
#rule    Country availability | some countries blocked for registration | inline error shown when selected in Personal Details or Business Details
#rule    Country search | partial match, case-insensitive | "Sin" matches Singapore and Sint Maarten
#rule    Country not found | empty state shown when no match

---

## File Attachment Rules (shared)

#rule    Attachment max size | 5MB
#rule    Attachment accepted formats | PDF, PNG, JPG
#rule    Attachment max count | 1 file per submission
#error   Attachment — no file | "Please attach a file."
#error   Attachment — file too large | "File size exceeds the maximum limit of 5MB"

---

## Export Rules (BO modules)

#rule    Export formats | CSV (.csv) and Excel (.xlsx)
#rule    Export applies current filters | exported data matches what is shown on screen
#error   Export — success | snackbar: "File exported successfully." (Transactions, Balance) | "Balance statement exported successfully." (Reports)
#error   Export — failed | "Export failed. Please try again." (Transactions) | "Failed to export balance statement. Please try again." (Reports)

---

## Decimal Precision Rules

#rule    Fiat amounts | max 2 decimal places
#rule    Crypto amounts | max 8 decimal places
#rule    OTC rates (Cost Rate, Execution Rate, Spread) | max 8 decimal places
#rule    Per-currency precision | currency-specific, not a flat rule | authority: https://aquariux.atlassian.net/wiki/spaces/OTC/pages/1732280322/Precision+Reference
#rule    Crypto amount over 8 decimals | auto-truncated to 8 decimal places, no error

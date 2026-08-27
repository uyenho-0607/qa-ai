---
inclusion: manual
---

# OTC Mobile App — Domain Knowledge

Search syntax: grep `#tag keyword` to pull only relevant entries.
Tags: `#screen` `#field` `#error` `#rule` `#flow` `#reuse` `#bo` `#module` `#status` `#scope` `#runbook`

---

## Sign Up — Onboarding

#flow    Business onboarding | steps: Name → Account Type → Business Details → Email OTP → Password → Phone OTP → Account Created → Passcode → Biometric → Home
#flow    Personal onboarding | steps: Name → Account Type → Personal Details (CoR + DOB) → Email OTP → Password → Phone OTP → Account Created → Passcode → Biometric → Home | ticket: AO-306
#reuse   Steps 4–7 (Email OTP / Password / Phone OTP / Account Created) | shared by Personal and Business onboarding | source: AO-298 (Email OTP), AO-299 (Password), AO-297 (Phone OTP), AO-300 (Account Created)
#screen  Account Type Selection | step: 2 | options: Personal, Business
#screen  Personal Details | step: 3 (Personal onboarding only) | fields: Country of Residence (mandatory), Date of Birth (mandatory) | heading: "Tell us about yourself" | subheading: "Help us verify your identity and comply with regulatory requirements."
#screen  Setup Email | step: 4 | field: Email | CTA: Send Code (disabled until valid email) → navigates to Verify Email
#screen  Verify Email | step: 4b | field: 6-digit OTP | timer: 60s countdown | Resend disabled during countdown
#screen  Setup Password | step: 5 | fields: Password, Confirm Password | CTA: Continue (disabled until both fields valid)
#screen  Setup Phone Number | step: 6 | fields: Country Code (pre-filled from CoR/CoReg if Twilio-supported), Mobile Number, Delivery Method (WhatsApp default / SMS) | CTA: Send Code
#screen  Verify Phone Number | step: 6b | field: 6-digit OTP | CTA: Skip (optional)
#screen  Account Created | step: 7 | header: "Account Successfully Created" | CTA: Done → navigates to Passcode Setup
#screen  Passcode Setup | post account creation | 6-digit numeric | cannot skip | confirm entry required
#screen  Biometric Offer | post passcode setup | shown if device supports biometric | options: Enable, Not Now | ticket: AO-864
#field   Country of Residence | screen: Personal Details | type: side sheet | list: same as Country of Registration master list | searchable, alphabetical, flag + name
#field   Date of Birth | screen: Personal Details | type: wheel picker (Month/Day/Year) | format: DD/MM/YYYY | future dates: selectable on picker but rejected on Done
#field   Country Code | screen: Setup Phone Number | pre-fill: from CoR or CoReg if country is Twilio-supported; empty if not supported
#rule    Min age | 18 years | screen: Personal Details | enforced after DOB picker Done tapped
#rule    Country unavailable | some countries not available for registration | screen: Personal Details | enforced after country selected from side sheet
#rule    KYC journey | triggered after Personal account creation | entry: popup on Home screen, skippable | third-party: Sumsub | do not test KYC flow details
#rule    KYB journey | triggered after Business account creation | third-party: Sumsub | do not test KYB flow details
#rule    Passcode | 6-digit numeric | mandatory after account creation | cannot be turned off | stored on-device only (iOS: Secure Enclave, Android: Keystore)
#rule    Biometric | optional after passcode setup | device-native (Face ID / fingerprint) | not stored server-side | iOS: OS permission required first time; Android: no separate consent dialog
#error   DOB empty | "Please select your date of birth."
#error   DOB future | "Please select a valid date of birth."
#error   DOB under-18 | "You must be at least 18 years old to register for an account."
#error   Country unavailable | "Sorry, registration is currently unavailable for this country."
#error   Country search no match | "No countries found"
#bo      Country of Residence | shown in: Member Details > Overview tab | added for Personal account type | not in Create Member flow (no change)
#module  Sign Up > Step N | app-side screens | BO-facing TCs → Members module

---

## Login

#runbook Login — device operations | env gate, app passcode, OTP fetch, device driving, gotchas | `.kiro/domain/login-flow.md` | read when a login must actually be driven, not for spec facts
#flow    Login | app launch → Splash Screen → Biometric/Passcode unlock (if session exists) OR Email+Password login (no session / session expired) → Home | tickets: AO-304, AO-305, AO-778
#flow    Forgot Password | Login screen → Email input → OTP verify → Reset Password → Account Recovery → Login screen | ticket: AO-777
#flow    Logout | Account > Settings → Log Out → confirmation prompt → session ended → Login screen | ticket: AO-865
#screen  Login | fields: Email, Password (masked, show/hide toggle) | CTA: Login | link: Forgot Password
#screen  Splash Screen | shown on app launch | auto-routes to Biometric/Passcode (session exists) or Login (no session) | ticket: AO-313
#screen  Biometric/Passcode Unlock | shown when valid session exists on device | biometric auto-prompted if enabled; passcode always available as fallback
#screen  Forgot Password — Email Input | field: Email | CTA: Next → always shows "Kindly check your email for verification code." regardless of whether email is registered
#screen  Forgot Password — Verify Email | 6-digit OTP | same OTP rules as onboarding (AO-298) | 5 consecutive incorrect → invalidate, request new code
#screen  Forgot Password — Reset Password | fields: New Password, Confirm Password | same password policy as onboarding
#rule    Login method | Email + Password (fallback / primary) | Passcode (day-to-day, local) | Biometric (day-to-day, local, optional)
#rule    Failed login limit | 5 consecutive incorrect attempts → account Suspended | counter resets on successful login or successful Forgot Password
#rule    Passcode failure limit | 5 consecutive incorrect passcode attempts → device session invalidated → full Email+Password login required | account NOT locked (device only)
#rule    Biometric failure | 3 failures → auto-fallback to Passcode | OS manages retry/lockout
#rule    Session TTL | 60 days
#rule    Account switch on device | logging in as different account → previous account session + biometric/passcode enrollment removed → new account goes through Passcode+Biometric Setup fresh
#rule    Password change (AO-779) | current device session reissued (biometric/passcode unaffected) | all other devices' sessions revoked
#rule    Logout | session token revoked | biometric/passcode enrollment stays configured | next login with same account resumes biometric/passcode automatically (no re-setup)
#rule    Suspended status | caused by: max failed login attempts | recovery: Forgot Password flow only | cannot log in while Suspended
#rule    Disabled status | caused by: admin action | cannot recover via Forgot Password | cannot log in
#rule    Forgot Password — unregistered email | system sends nothing but does NOT reveal email is unregistered; same UI shown as registered email
#error   Login — empty email | "Please enter your email."
#error   Login — invalid email format | "Please enter a valid email to proceed."
#error   Login — empty password | "Please enter your password."
#error   Login — wrong credentials | "Email or password is incorrect."
#error   Login — account locked | "Your account has been locked due to multiple failed login attempts. Please reset your password to regain access."
#error   Forgot Password — empty email | "Please enter your email."
#error   Forgot Password — invalid email format | "Please enter a valid email to proceed."
#error   Forgot Password — OTP expired | "Your verification code has expired, please request a new code."
#error   Forgot Password — OTP incorrect | "Your verification code is incorrect, please try again."
#error   Forgot Password — OTP max attempts | "You have reached the maximum number of incorrect verification code attempts. Please request a new code."
#error   Forgot Password — weak password | "Your password is not strong enough. To secure your account, avoid common words, names, dates and repeating characters."
#error   Forgot Password — same as current password | "The new password shall not be the same as the current password."
#error   Forgot Password — passwords don't match | "Password does not match."
#error   Passcode change — wrong current passcode (attempt 4) | "Incorrect passcode. You have 1 attempt remaining before you'll need to sign in with your email and password."
#status  Active | normal account state | can log in
#status  Suspended | max failed login attempts reached | cannot log in | recoverable via Forgot Password
#status  Disabled | admin action | cannot log in | cannot recover via Forgot Password
#bo      Suspended status | shown in Member Details (BO) | Maker or Admin can activate via "Activate" action button | ticket: AO-778
#module  Login screens | module: Login | BO status changes → Members module
#scope   Login — out of scope (phase 1) | SSO (Google/Apple) | OTP login | 2FA | magic link | CAPTCHA | Remember me
#scope   New Device Verification | AO-307 — Backlog, not yet implemented | no spec available yet

---

## Deposit — Crypto

#flow    Crypto deposit | Home → Deposit icon → Choose Deposit Type (bottom sheet) → Crypto → Select Currency → Select Network → [system validates pair + KYC + member status] → Deposit Details → Done → Home | tickets: AO-433 (type sheet), AO-426 (crypto deposit)
#screen  Choose Deposit Type | bottom sheet | trigger: any Deposit icon | title: "Choose Deposit Type" | close: "X" top-left | no option pre-selected | fresh state on every open
#screen  Choose Deposit Type — options | Crypto: "Deposit using a blockchain network (USDC, BTC, etc.)" | Fiat: "Deposit using bank transfer (SGD, USD, etc.)" | each with next ">" | mutually exclusive
#rule    Choose Deposit Type — selection | tap option → sheet closes immediately → navigates to that deposit flow
#rule    Choose Deposit Type — dismiss | tap "X" | swipe down | tap outside (dimmed overlay) | none trigger a deposit flow
#screen  Select Currency (deposit) | header: "Select Currency" | search placeholder: "Search currency", filters real-time | each row shows balance | tap a currency → Select Network
#rule    Select Currency (deposit) — list source | OTC Default Currency List – [Deposit] Crypto | only pairs active in BFG AND enabled in Fireblocks
#rule    Select Currency (deposit) — sorting | balance descending | zero-balance currencies alphabetical after them
#rule    Select Currency (deposit) — no data | error shown from Mobile Masterlist
#screen  Select Network (deposit) | header: "Select <currency> network" | tag-style list, alphabetical A→Z | no default selection | tap a network → system validates → Deposit Details or error
#rule    Select Network (deposit) — changing currency | network list must refresh for the newly selected currency
#rule    Select Network (deposit) — no data | error shown from Mobile Masterlist
#rule    Deposit validation on network tap | 1) currency-network pair still active in BFG + enabled in Fireblocks | 2) member Verification (KYC/KYB) status = Approved | 3) member status = Active
#error   Deposit — verification status changed | popup: "Your account verification status has changed and no longer meets deposit requirements."
#error   Deposit — member status changed (disabled) | popup: "Your account status has changed and no longer meets deposit requirements."
#error   Deposit — address retrieval API failure/timeout | "Please contact support for assistance."
#screen  Deposit Details | read-only | header: "Deposit address" | shows "<Currency> on <Network>" matching selections | QR code (FE-generated from the address) | Deposit Address + Copy | Save QR Code | Memo/Tag (conditional) | warning message | Done → Home
#rule    Deposit Details — Save QR Code | downloads the QR as .png | success toast: "Image saved to photo library"
#rule    Deposit Details — Copy address | copies to clipboard | success toast: "Address copied"
#rule    Deposit Details — Memo/Tag visibility | shown only for pairs whose Address Type is Account-based with Memo/Tag (e.g. XRP-XRPL) | value from Fireblocks
#error   Deposit warning — no memo/tag | "Only send <Currency> on the <Network> to this address. Sending other assets may result in permanent loss."
#error   Deposit warning — with memo/tag | "Only send <Currency> on the <Network> to this address. Sending other assets may result in permanent loss. Please ensure that you include the memo/tag provided when making the deposit."

### Deposit Address Types

#rule    Address stability | address does NOT change when the screen is closed and the same currency-network pair is requested again within the same member profile
#rule    Address type — Account-based (EVM) | e.g. ETH-ERC20, USDC-ERC20, POL-Polygon | one address shared by all assets on the EVM chain within the same member profile | no memo/tag
#rule    Address type — Account-based (Tron) | e.g. TRX-TRC20, USDT-TRC20 | one address shared by all assets on Tron within the same member profile | no memo/tag
#rule    Address type — Account-based (Solana) | e.g. SOL-Solana | dedicated address for the Solana network | no memo/tag
#rule    Address type — UTXO | e.g. ADA-Cardano | sub-address issued by Fireblocks | no memo/tag
#rule    Address type — Account-based with Memo/Tag | e.g. XRP-XRPL | address plus memo/tag, both from Fireblocks | memo/tag required for the sender
#rule    Deposit test data matrix | Business: USDC-ERC20 (EVM), POL-Polygon (EVM), SOL-Solana, XRP-XRPL (memo) | Personal: TRX-TRC20 (Tron), USDT-TRC20 (Tron), ADA-Cardano (UTXO)

---

## Withdrawal — Crypto

#flow    Crypto withdrawal | Home → Withdraw → Crypto → Select Currency → Select Network → Input Details → Next → Confirm Withdrawal → Confirm → Success (Pending) or Failure → Done → Home | ticket: AO-427
#rule    Select Currency (withdrawal) | only currencies with balance > 0 | sorted by balance descending
#rule    Select Network (withdrawal) | alphabetical | no default selection | changing currency refreshes the network list
#screen  Input Details (withdrawal) | fields: Amount, Destination Address, Memo/Tag (conditional) | Available Balance shown top-right | warning: "Ensure the destination wallet supports the selected network before proceeding." | CTA: Next | Back → Select Network
#field   Amount (withdrawal) | numeric, placeholder "$0.00" | disabled until Currency + Network chosen | precision is currency-specific — see otc-shared.md § Decimal Precision Rules
#field   Max button (withdrawal) | enabled when the Amount field is enabled | tap → fills Amount with the Available Balance
#field   Available Balance (withdrawal) | displayed as "Available Balance <Amount><Currency>" | shows "-" until both Currency and Network are selected
#field   Destination Address (withdrawal) | alphanumeric | disabled by default | format validated against the selected network
#field   Memo/Tag (withdrawal) | optional, numeric only | hidden by default | shown only for pairs that support it (e.g. XRP)
#rule    Next button (withdrawal) | ALWAYS enabled | tap → validates mandatory fields → shows errors if invalid, navigates to Confirm Withdrawal if valid
#rule    Changing currency-network pair (withdrawal) | resets every input field back to empty
#error   Withdrawal amount — empty | "Please enter an amount."
#error   Withdrawal amount — letters or special characters | not accepted, does not appear in the field
#error   Withdrawal amount — mixed input (123abc) | only the numeric part is accepted
#error   Withdrawal amount — zero | "Amount has to be greater than or equal to 0.00000001 {{currency}}"
#error   Withdrawal amount — exceeds available balance | "Insufficient balance to complete withdrawal."
#error   Withdrawal amount — over 12 integer digits | "Amount has to be less than or equal to 999,999,999,999.99999999 {{currency}}."
#rule    Withdrawal amount — over 8 decimal places | auto-truncated to 8 decimals, no error
#error   Withdrawal address — empty | "Please enter a withdrawal address."
#error   Withdrawal address — invalid format | "Please enter a valid Destination Address."
#error   Withdrawal address — valid format but wrong network | "Please enter a valid Destination Address."
#screen  Confirm Withdrawal | read-only | shows Amount, Currency, Network, Transaction ID (OTC-generated), Destination Address as entered | after processing adds: Fireblocks Transaction ID, Source Address, Transaction Hash (hyperlink to blockchain explorer)
#rule    Withdrawal BO progression | Transaction Created (Pending) → Checker approves → In Progress → Fireblocks → Success
#rule    Withdrawal balance — after submit (Pending) | Total unchanged | Available = A - amount | Pending = P + amount
#rule    Withdrawal balance — after approved and processed (Success) | Total = X - amount | Available = A - amount | Pending = P (back to prior)
#rule    Withdrawal test data matrix | cover one pair without memo/tag (e.g. USDC-ERC20) and one with (e.g. XRP-XRPL) across Business and Personal profiles
#module  Deposit / Withdraw screens | app-side modules | BO-facing assertions (transaction records, balances) → Transactions or Balance module

---

## Error Handling (app-wide)

#flow    Error handling | connection lost on loaded screen → snackbar | app launch + offline → full screen | API error (online) → full screen | connection restored → snackbar | ticket: AO-946
#screen  No Internet Connection (full screen) | shown: app launch + offline | header: "No internet connection" | description: "Please check your internet connection and try again." | CTA: Retry
#screen  General Error (full screen) | shown: API/backend error while online | header: "Something went wrong" | description: "We couldn't complete your request. Please try again later." | CTA: Back to home → navigates to Home
#screen  Device Security (full screen) | shown: jailbroken/rooted device | header: "Device security issue detected" | description: "This device doesn't meet our security requirements. To help protect your account, this app can't be used on this device." | CTA: Close App
#error   Connection lost on screen | snackbar: "No internet connection"
#error   Connection restored | snackbar: "You're back online"
#rule    Error handling scope | technical/system errors only | feature-specific validation errors unchanged | session not terminated by connectivity or general error
#scope   Error handling — out of scope | session timeout | force update | scheduled maintenance | backend error logging | device security detection mechanism internals

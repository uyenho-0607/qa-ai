
# OTC Back Office — Domain Knowledge

Search syntax: grep `#tag keyword` to pull only relevant entries.
Tags: `#screen` `#field` `#error` `#rule` `#role` `#module` `#status` `#flow` `#permission` `#scope`

---

## Roles & Permissions

#role    Admin | access: all modules | actions: create users, reset password, disable 2FA, view all
#role    Maker | access: Member Management, Balance, OTC, Reports | actions: create members, create balance requests, create OTC requests, activate/disable members
#role    Checker | access: Action Required, Balance (view), OTC (view), Transactions (view), Reports | actions: approve/reject balance and OTC requests
#permission  Dashboard | all roles
#permission  Member Management | Maker: create + edit status + view | Checker: view only | Admin: view only
#permission  Balance | Maker: create + view | Checker: view only
#permission  OTC | Maker: create + view | Checker: view only
#permission  Action Required | Checker: full access | Maker + Admin: no access | approve/reject never available to the request's own creator
#permission  Transactions | all roles: view + export only
#permission  Reports — Balance Statement | all roles: view + export
#permission  User Management | Admin only: create + reset password + disable 2FA | Maker + Checker: no access

---

## Login (BO)

#flow    BO Login | Email + Password → 2FA check → if 2FA enabled: 2FA screen → Dashboard | if 2FA disabled: Dashboard
#rule    2FA | optional per user | default: disabled for new users | Admin can disable 2FA for any user via User Management
#rule    Account lock | account Disabled when locked for security reasons | Admin can re-activate via User Management
#error   BO login — no email | "Please enter your email."
#error   BO login — wrong credentials | "Email or password is incorrect."
#error   BO login — no password | "Please enter your password."
#error   BO 2FA — invalid OTP | "Please enter a valid code."
#error   BO 2FA — limit reached / account disabled | "Your account has been disabled. Please contact your admin to unlock your account."
#rule    No Forgot Password for BO | Admin resets passwords for sub-admins via User Management
#status  Active | can log in
#status  Disabled | cannot log in | Admin can re-activate

---

## Members Module

#screen  Members list | columns: Member (name + email), Member Type, Verification Status, Status, Created Date, Action (...) | source: BO + Mobile app registrations
#screen  Member Details — Overview | fields: First Name, Last Name, Business Registration (Business), Country of Registration (Business) or Country of Residence (Personal), Phone Number, Created Date
#screen  Member Details — Verification tab | linked to Sumsub verification record
#screen  Create Member (BO) | breadcrumb: Members / Create Member | sections: Profile Type, Member Information, Verification Setup | CTA: Cancel, Create
#screen  Create Member — Profile Type | card-style segmented buttons (not radio) | options: Individual (default, "Personal account for a single verified user"), Business ("Business entity requiring KYB verification")
#screen  Create Member — Individual fields | Email (mandatory), First Name (mandatory), Last Name (mandatory), Date of Birth (optional), ID Number (optional) | no Country of Residence field
#screen  Create Member — Business fields | Business Name (mandatory), Business Email (mandatory), First Name (mandatory), Last Name (mandatory), Country of Registration (mandatory), Business Registration Number (optional), Phone Number (optional)
#screen  Create Member — Verification Setup | option 1 (default): Create new Sumsub applicant | option 2: Link existing Sumsub applicant
#field   Verification Level | screen: Create Member (Create new applicant) | mandatory dropdown | options from Sumsub, sorted alphabetically | Individual profile → Individual levels | Business profile → Company levels
#field   Send verification email | screen: Create Member (Create new applicant) | checkbox, default: checked | if enabled: verification invitation email sent after creation
#field   Sumsub Applicant ID | screen: Create Member (Link existing applicant) | mandatory text, max 100 characters | must match profile type (Individual ↔ Individual, Business ↔ Company)
#field   Phone Number (BO create) | optional, numeric only | Country Code auto-populates from Country of Registration | no Country of Registration selected → Country Code blank
#field   Date of Birth (BO create) | optional date picker | future dates cannot be selected (blocked at picker)
#rule    Create Member — Cancel | closes form, no member created | re-opening shows empty fields, no saved draft
#rule    Create Member — verification status after creation | Create new applicant: "Not Started" → "Documents requested" | Link existing: retrieved from Sumsub
#error   Members — create: country of registration not selected | "Please select a country of registration"
#error   Members — create: verification level not selected | "Please select a verification level."
#error   Members — create: Sumsub applicant ID not found | "Unable to link Sumsub Applicant ID. Please contact support for assistance."
#error   Members — create: Sumsub applicant ID already linked | "Sumsub Applicant ID is already linked to another member. Please use a different Sumsub Applicant ID."
#error   Members — create: Sumsub applicant type mismatch | "Sumsub Applicant type does not match member profile type. Please check and try again."
#rule    Member created via BO | default status: Active | no Country of Residence field in BO Create Member flow
#rule    Member created via Mobile (Business) | Member Type: Business | Verification Status: Not Started → Documents requested after account created
#rule    Member created via Mobile (Personal) | Member Type: Personal | Verification Status: Not Started | KYC journey triggered post-creation
#rule    Maker cannot disable member if | available balance > 0 OR pending balance > 0 OR pending deposit/withdrawal/OTC transactions exist
#rule    Member statuses | Active: normal | Disabled: admin action or max failed login (Suspended on mobile = Disabled on BO)
#error   Members — cannot disable (has balance) | "This member cannot be disabled as they have available or pending balances. Please clear all balances before disabling the member."
#error   Members — cannot disable (pending requests) | "This member cannot be disabled as they currently have pending requests. Please resolve all pending requests before disabling."
#error   Members — create: email empty | "Please enter an email."
#error   Members — create: invalid email | "Please enter a valid email to proceed."
#error   Members — create: duplicate email | "This email already exists."
#error   Members — create: email max length | "Maximum 100 characters allowed."
#error   Members — create: first name empty | "Please enter first name."
#error   Members — create: last name empty | "Please enter last name."
#error   Members — create: name max length | "Maximum 100 characters allowed."
#module  Members | BO module for all member record checks | app-side TCs that verify BO impact → use Members module

---

## Balance Module

#screen  Balance listing | columns: Member, Currency, Total Balance, Available Balance, Pending Balance | default: sorted by Total Balance desc, only rows with at least one balance > 0
#rule    Total Balance = Available Balance + Pending Balance
#rule    Available Balance | used for OTC sell and withdrawals | debit must not exceed available balance
#rule    Pending Balance | sell amount from pending OTC requests + pending withdrawals
#rule    Balance request flow | Maker creates → Pending → Checker approves/rejects in Action Required
#rule    Withdrawal validation | amount cannot exceed member's available balance
#error   Balance — create failed | "Failed to create new balance. Please try again."
#error   Balance — created ok | snackbar: "New balance has been created successfully."

---

## OTC Module

#screen  OTC listing | columns: Created Date, Member, Sell Amount, Sell Currency, Buy Amount, Buy Currency, OTC ID, Status, Action | default: latest Created Date first
#rule    OTC ID format | OTC-20251110210000630196 (OTC- prefix + timestamp-based numeric)
#rule    Sell Amount | deducted from member's available balance at creation | checked only on form submission
#rule    Buy Amount | credited to member's balance on Checker approval
#rule    Commission | credited to Treasury (platform), not member | creates separate transaction entry
#rule    OTC request states | Pending → Approved or Rejected
#error   OTC — insufficient balance | "Member has insufficient balance."
#error   OTC — created ok | snackbar: "OTC request created successfully."
#error   OTC — member not selected | "Please select a member."
#error   OTC — amount empty | "Please enter an amount." or "Please enter a valid amount."
#error   OTC — zero amount | "Please enter a valid amount."
#error   OTC — currency not selected | "Please select a currency."
#error   OTC — cost rate empty | "Please enter a valid cost rate."
#error   OTC — execution rate empty | "Please enter a valid execution rate."
#error   OTC — spread empty | "Please enter a valid spread."
#error   OTC — reference ID empty | "Please enter a reference id."
#error   OTC — no attachment | "Please attach a file."
#error   OTC — file too large | "File size exceeds the maximum limit of 5MB"

---

## Transactions Module

#screen  Transactions listing | columns: Type, Created Date, Member, Amount, Currency, Status, Action | default: latest first
#rule    Transaction types | Deposit, Withdrawal, OTC Credit, OTC Debit, Commission
#rule    Transaction statuses | Approved, Pending, Rejected
#rule    OTC Credit + OTC Debit + Commission | grouped by same OTC ID and Reference ID
#rule    Transaction ID | Liverum-OTC system-generated | used for Deposit/Withdrawal entries
#rule    Reference ID | from counterparty via UTGL (external OTC system) | used for OTC Credit/Debit/Commission

---

## Action Required Module

#screen  Action Required — Balance | pending balance requests for Checker to approve/reject
#screen  Action Required — OTC | pending OTC requests for Checker to approve/reject
#rule    Approve balance | deducts sell amount, adds buy amount, updates transaction status to Approved
#rule    Reject balance | reverts sell amount to member balance, updates transaction status to Rejected, Remarks mandatory
#rule    Approve OTC | same balance impact as balance approval
#rule    Reject OTC | same reversal as balance rejection, Remarks mandatory
#rule    Remarks | mandatory on reject | optional on approve | max 255 characters | input stops at 255, counter shown as 0/255
#rule    Self-approval blocked | a user cannot approve a request they created themselves | applies to Admin too
#rule    Self-rejection allowed | a user CAN reject a request they created themselves
#rule    Approve/Reject buttons | visible to Checker (and Admin) only | Maker never sees them
#rule    Action Required listing | every record is Pending — no Status filter | no Export button | no Search bar, filters only
#rule    Approve/Reject actions | located in the record detail drawer, not inline on the listing row
#rule    Sidebar pending badge | shows pending count | must match total records in the queue | decreases after approve or reject
#rule    Post-action effects | record removed from approval list | badge decremented | balance updated (approve deposit → Available ↑; reject withdrawal → Available ↑) | transaction record created with matching status
#error   Reject without remarks | blocked — error shown, request remains Pending
#error   Balance approved | snackbar: "Balance request approved successfully."
#error   Balance rejected | snackbar: "Balance request rejected successfully."
#error   OTC approved | snackbar: "OTC request approved successfully."
#error   OTC rejected | snackbar: "OTC request rejected successfully."

---

## Configuration — Currency Pairs

#permission  Configuration > Currency Pairs | Admin only | Maker + Checker: cannot view the module
#rule    Currency Pairs — no approval flow | Admin-only changes take effect immediately | no maker/checker cycle
#rule    Currency pairs are directional | BTC/USD and USD/BTC are inverse | only ONE direction can be Active at any time
#rule    Rate derivation | reference rate source and direction rule: otc-shared.md § Third-Party Integrations (CMC)
#rule    Currency Pairs dependency | controls Mobile App Convert module only | does NOT affect Back Office OTC
#rule    Bulk creation | one Base + multiple Quote currencies → creates one pair per Quote
#rule    Markup Rule assigned at creation | default: "System Default" | changeable per pair
#screen  Currency Pairs listing | tabs: Currency Pairs (active) | Markup Rules | buttons: Export, Create Currency Pair | columns: Currency Pair, Buy Markup, Sell Markup, Status, Last Updated, Updated By, '...' action
#screen  Currency Pairs listing | default sort: Last Updated descending | date format: DD MMM YYYY, HH:mm | pagination: "1-10 of [total] records", 10/page, Go to page
#screen  Currency Pairs filters | left: Base Currency, Quote Currency, Status, Last Updated (all multi-select) | right: search, placeholder "Base / Quote Currency"
#screen  Create Currency Pair | breadcrumb: Configuration / Create Currency Pair | sections: Currency Pair, Pairs to be created, Set default configuration | CTA: Cancel, Create
#field   Base Currency | screen: Create Currency Pair | single-select dropdown | crypto only, alphabetical
#field   Quote Currencies | screen: Create Currency Pair | multi-select, disabled until Base selected | Crypto + Fiat shown separated | Base excluded | already-configured pairs shown disabled
#rule    Pairs to be created table | always visible | empty state: "Select base and quote currencies to view currency pairs" | columns: Currency Pair, Status, Markup Rule Applied | all default to Active + System Default
#rule    Remove a pending pair | via chip [x] only | no trash icon in the table
#rule    Markup Rule dropdown | lists Active markup rules only, Inactive hidden | each shows Name + Buy % · Sell %
#rule    Apply to All | does NOT auto-apply to pairs added afterwards — those get System Default | must click Apply to All again to include them
#rule    Create button | disabled until at least one Quote selected AND no inverse conflict
#rule    Inverse conflict | inverse pair already Active → inline error shown, Create disabled
#rule    Search — non-directional | "BTC" returns all pairs where BTC is base OR quote
#rule    Search — directional | "BTC/" returns BTC as base only | "/BTC" returns BTC as quote only | apply: Enter key | clear: [x] on input
#rule    Filter then search | left filters CLEARED, search applies alone
#rule    Search then filter | both RETAINED, combined with AND logic
#rule    Clear filters button | hidden by default | appears when any filter or search is applied | clears ALL
#rule    Status action menu | Active pair shows "✕ Deactivate" | Inactive pair shows "✓ Activate"
#screen  Update Currency Pair Status modal | header: "Update Currency Pair Status" | description: "Updating the currency pair status will take effect immediately and may impact conversion in mobile app. Are you sure you want to proceed?" | CTA: Cancel, Confirm
#status  Currency pair Inactive | immediately hidden from Mobile App Convert (From/To fields) | pending Convert transactions: Approve CTA disabled, Checker can only reject | past OTC transactions unaffected | assigned Markup Rule not deleted
#status  Currency pair reactivated | available again in Mobile App Convert immediately
#scope   Currency Pairs logs | backend only, not visible on UI | captures Updated By + Last Updated on Create and Status Update | verify via BE support
#module  Currency Pairs | module: Configuration | sub-module: Currency Pairs | ticket: AO-395

---

## User Management Module

#screen  User Management | columns: User (name + email), Role, Status, 2FA Status, Action (Reset Password / Disable / Activate / Disable 2FA)
#rule    New user | default 2FA: disabled | Admin assigns role at creation
#rule    BO roles | Admin, Maker, Checker
#rule    Reset password | does NOT reset/disable 2FA
#error   User — email empty | "Please enter an email."
#error   User — invalid email | "Please enter a valid email to proceed."
#error   User — duplicate email | "This email already exists."
#error   User — email max length | "Maximum 100 characters allowed."
#error   User — first name empty | "Please enter first name."
#error   User — last name empty | "Please enter last name."
#error   User — name max length | "Maximum 100 characters allowed."
#error   User — password empty | "Please enter your password."
#error   User — password max length | "Maximum 100 characters allowed."
#error   User — password format | "Password does not meet the required format."
#error   User — role not selected | "Please select a role."

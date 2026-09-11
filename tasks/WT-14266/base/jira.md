# Jira: WT-14266

## Title
[WT][ROOT][Centroid] Support Upload Missing Statement Data and Regenerate Patched Daily Statements

## Status
SIT in progress | Assignee: Lim Jing Ting | Reporter: Chin Yee Heng

## Requirement Changes
The ticket description/requirement table is kept current via an in-body "change log" table, and it already reflects every dated revision through **9 Sep 2026** (requirement #8 revised, requirement #27 added). One clarification, however, was decided only in a comment and is **not** written into the requirement table text — downstream test design must use this, not the silent description:

- **Comma-formatted numeric values (comment by Chin Yee Heng, 2026-08-19, and Quoc Binh Nguyen, 2026-08-19):** Final decision — the uploaded **CSV must not contain commas** in numeric fields (plain numeric only), but once uploaded/queried, the **Statement Data Table (UI) shall display the numeric columns with comma thousand-separators** (e.g. CSV value `1000` displays as `1,000.00` in the table). This formatting rule does not appear anywhere in the requirement table or CSV validation rows.
- This decision is directly relevant to sub-task **WT-15818** ("Open Price accepts comma-formatted text without validation error on CSV upload"), where the assignee (Le Ngoc Loan Anh, 2026-09-09) is still asking Chin Yee Heng to confirm whether a comma-formatted value inside the **uploaded CSV itself** (e.g. `1,330.65`) should be rejected. As of the last comment on that sub-task, **no reply has been given** — this is an open question, not yet resolved into the spec or the requirement table.

See "Open Items from Comments" below for two further unresolved threads.

## Description
**Internal Doc:** https://aquariux.atlassian.net/wiki/spaces/WT/pages/1874296899/Root+Admin+-+Upload+Missing+Statement+Data+Patch+and+Regenerate+Statements

**User Story:** As an AQ internal user, I want to upload missing Centroid statement data into Root Admin, so that the system can patch the missing data and regenerate the affected trader statement for Root Admin & Membersite download.

**Current Behaviour:** When Centroid API fails or returns incomplete data, AQXTrader may generate the statement with missing data. Current Root Admin does not have a manual way to upload missing Centroid data and regenerate the affected statement.

**Expected Behaviour (Core Flow):**
1. System alert will be triggered by BE health check.
2. L1 will retrieve the missing data manually from Centroid.
3. L1 will prepare the missing data in CSV format based on the relevant statement table template.
4. L1 / PM will create a new patch in Root Admin.
5. Root Admin user selects the tenant/client first.
6. Root Admin user uploads the missing data CSV for the selected statement table type.
7. BE validates and stores the uploaded file/data for patching.
8. Root Admin user selects the statement date/month to patch and regenerate.
9. Root Admin user may optionally preview one account statement before patching.
10. Root Admin user triggers Patch and Regenerate.
11. When Root Admin user clicks Patch: BE patches the missing data to DB.
12. When Root Admin user clicks Regenerate: BE regenerates the affected statement PDF(s).
13. When Root Admin user clicks Download: System allows downloading the generated PDF(s) to user device in a ZIP file.
14. Patch job is displayed in Patch History.
15. No statement email should be sent after manual upload / patch / regeneration.

**Core Flow Reference (as stated in ticket):**
- Query & Update Data: `Query DB → Statement Data Table → Edit/Delete → Patch DB → Generate Patched Dataset → Preview → Regenerate → Download`
- Upload CSV: `Upload CSV → Statement Data Table → Edit/Delete → Patch DB → Patched Dataset → Preview → Regenerate → Download`
- Preview Statement: `Select Statement Type, Select Statement Date, Select Account ID → Click Preview Statement`
- Regenerate: `View Patch History → click Regenerate PDF → Download ZIP File`

**Statement Table / CSV Template / Data Validation mapping** (per Statement Table type — see requirement table for full column lists):
- **Executed Orders:** no CSV upload (fetched live from Centroid API); AppID defaults `WEB` if empty, Trigger defaults `MANUAL` if empty; not editable: Account ID, Item, Order Date, Order Time, Order Ref, Exchange Rate.
- **Settled Position:** CSV columns Account ID, Date, Item, Open Ref, Open Date, Open Price, Close Ref, Close Date, Close Lot(s), Close Price, Exchange Rate, Interest, Commission, Profit/Loss, IsDeleted. Open Date/Close Date must be valid `yyyy-mm-dd` or `--`; numeric fields per column (see requirement table row "Settled Position").
- **Open Position:** CSV columns Account ID, Date, Order Ref, Item, Net Volume, Average Price, Closing Price, Exchange Rate, Unrealised Interest, Daily Interest, Commission, Floating Profit/Loss, Notional, IsDeleted.
- **Deposit/Withdrawal:** CSV columns Account ID, Date, Order Ref, Description, Type, Amount, IsDeleted. Type accepts only `DEPOSIT`, `WITHDRAWAL`, `CREDIT`, `OTHERS`.
- **Statement Summary:** CSV columns Account ID, Date, New balance, Equity, Call Margin, Currency, Buy Exchange Rate, Sell Exchange Rate, IsDeleted (BE calculates remaining columns). Data source is DB backup/CSV only (BE cannot fetch prior-date balance from API).
- **Interest Rate:** CSV columns Account ID, Date, Taker Feed, Limit Symbol Group, Symbol, Sell Rate, Buy Rate, IsDeleted. CSV stores numeric only; FE displays `%`.

**Data source consolidation (per BE, comment 2026-08-18):**
- Executed Orders → Centroid API (Broker) only — no CSV upload flow.
- Settled positions → Centroid API (Trader) < Database backup < CSV data.
- Transactions (Deposit/Withdrawal) → Centroid API (Trader) < Database backup < CSV data.
- Open positions → Database backup < CSV data.
- Statement summary → Database backup < CSV data.
- Interest rate → Database backup < CSV data.

**Patch History table columns:** Name (Tenant name), Short Code, Patched Dataset (CSV), Range (Daily/Monthly), Patch Execution Date, Patched By, Remarks (system appends error message on job failure, persists even after a later successful retry), Status (PROCESSING/COMPLETED/FAILED, auto-refreshes), Action (Download Patched Dataset, Regenerate PDF, Download Regenerated Statement — Regenerate PDF hidden while PROCESSING/FAILED, shown when COMPLETED; shows loading icon while regenerating, Download icon on success, FAILED tag + Retry icon on failure).

## Business Requirements
- BR-1: Root Admin Privilege and Access — Add privileges "View Patch and Regenerate Statement Page" and "Patch and Regenerate Statement". Only authorised users access the page. View-only users: page loads with all 4 sections visible; Section 1 (tenant select) enabled; Sections 2 and 3 disabled; Section 4 displayed with Refresh + Download (patched dataset & PDF) enabled but no Regenerate/Retry.
- BR-2: Add Statement Patch and Regeneration Page — New page under Root Admin > Troubleshoot Platform, named "Statement Patch & Regeneration", with 4 sections: Select Tenant and Action, Statement Data Query & Patch, Statement Preview, Patch History and Regeneration.
- BR-3: Select Client — dropdown lists all tenants in current Root Admin as `Tenant Name (Short Code)`; default placeholder "Select client"; user must select a tenant before proceeding; all fields disabled except Patch History section until a tenant is selected.
- BR-4: Select Statement Table — dropdown options in order: Executed Orders, Settled Position, Open Position, Deposit/Withdrawal, Statement Summary, Interest Rate; default "Executed Orders"; selection determines the Statement Data Table columns.
- BR-5: Select Statement Type — options Daily, Monthly; default "Daily"; determines applicable query filters and table structure.
- BR-6: Statement Table Template — "Download template here" link shown per selected Statement Table/Type, EXCEPT when Statement Table = Executed Orders (no CSV upload for that table).
- BR-7: Upload CSV — "Choose File" button; shows "No file chosen" by default, then `[file name].csv` after selection; not displayed when Statement Table = Executed Orders.
- BR-8 *(revised 2026-09-09)*: CSV Validation and Error Handling — file must be `.csv`, non-empty, ≤5MB, contain required columns for the selected table, Account ID/Symbol must belong to selected tenant, FE-level field validation applied; system shows a specific snackbar per failure type (see Error Messages).
- BR-9: CSV Upload Behaviour — once validated, system auto-populates the Statement Data Query & Patch table; all query filters, Search and Export Data are disabled while a CSV is uploaded; uploading replaces existing table data; user may view/edit/delete uploaded records before Patch; DB is updated only after Patch.
- BR-10: Statement Data Table — columns depend on selected Statement Table/Type; acts as single source of truth for the working dataset before Patch; Search/Fetch/Upload populate it; loading another dataset replaces existing working data; Edit/Delete affect only the working table until Patch.
- BR-11: Query & Update Data - Daily — mandatory filters Account ID, Start Datetime (UTC), End Datetime (UTC); Search enabled only when all filled; Search retrieves DB data into the table; Export Data disabled when table empty, enabled when records exist.
- BR-12: Query & Update Data - Monthly — mandatory filters Account ID, Select Month; same Search/Export Data behaviour as Daily.
- BR-13: AccountID — LIVE Account IDs only (DEMO out of scope), scoped to selected tenant, dropdown has search, single selection, sorted numerical ascending, default placeholder "Select Account ID"; Account ID / Start Datetime / End Datetime / Select Month are retained when the user changes Statement Table.
- BR-14: Start Datetime (UTC) — date picker in `yyyy-mm-dd hh:mm:ss` UTC format, shown when Statement Type = Daily; value retained across Statement Table changes.
- BR-15: End Datetime (UTC) — same as Start Datetime; value retained across Statement Table changes.
- BR-16: Start Datetime and End Datetime (Patch period rules, per Daylight Saving state):
  - Daily, DST ON: previous calendar day 22:00:00 UTC → today 21:00:00 UTC. DST OFF: previous day 23:00:00 UTC → today 22:00:00 UTC.
  - Monthly, DST ON: previous day of 1st of selected month 22:00:00 UTC → last day of month 21:00:00 UTC. DST OFF: previous day 23:00:00 UTC → last day of month 22:00:00 UTC.
- BR-17: Edit Table Record — Edit action on editable rows; some fields non-editable per table type; other fields follow field-level validation; changes affect working table only until Patch.
- BR-18: Delete Table Record — Delete action shows confirmation modal; confirmed record is removed from the displayed table (no snackbar); working table only until Patch; FE passes a flag/column so BE removes the record in DB when user clicks Patch.
- BR-19: Daylight Saving Toggle — shown for Daily and Monthly, positioned after the Statement Data Table, before Remarks/Patch; auto ON/OFF based on today's date vs. DST period; applies on Search/Patch click; turning OFF shifts Start/End Datetime by +1 hour on UI (22:00:00→23:00:00, 21:00:00→22:00:00) and vice-versa; FE sends the final converted Start/End Datetime + DST setting to BE; DST conversion does not alter records already displayed in the table.
- BR-20: Remarks — optional free-text field after the Statement Data table, left of Patch button; placeholder "Enter your remarks".
- BR-21: Patch Statement Data — Patch button enabled only when the table has data; clicking submits the final working dataset to BE; BE updates DB per the final table data and delete-indicators; Patch triggers DB update only (no regeneration); creates a Patch History record with the Patched Dataset.
- BR-22: Patch History — one record per Patch action, latest first, 5 records/page pagination; columns per the Patch History table (see Description); status auto-refreshes; Refresh action provided.
- BR-23: Patched Dataset — FE consolidates the final working dataset and submits on Patch; BE retains it for audit; represents table state immediately before Patch (not necessarily the original uploaded CSV); edited records show final values; deleted records remain with an added **IsDeleted** column (`TRUE`/`FALSE`); downloadable as CSV from Patch History.
- BR-24: Preview Statement — independent of Search/Fetch/Upload/Patch; requires Statement Type, Statement Date (auto today for Daily / current month for Monthly), Account ID — all mandatory; button disabled until all 3 are filled; generates the statement from the latest DB data for the selected account/period; PDF displayed in a scrollable popup modal with a close (X) control; preview does not replace the existing statement; user may return to Section 2 to edit/Patch again before Regenerate.
- BR-25: Regenerate Statement — final action; regenerates and replaces the applicable existing statement(s) using the latest Patched Dataset (not the uploaded CSV); only 1 Regenerate job at a time (loading icon shown, other Regenerate buttons blocked while running); on completion the button becomes an enabled Download (ZIP of PDFs); regenerated statement replaces the existing Membersite statement; no statement email sent.
- BR-26: Store Statement Data for those using Trader API — store Closed Positions and Transaction data in DB; BE data-source hierarchy per table as listed under Description.
- BR-27 *(added 2026-09-09)*: Restrict Patching Data to July 2026 Onwards — system only allows patching statement data dated 1 July 2026 onwards. Applies to: date pickers (Start/End Datetime, Select Month, Statement Date — disable dates before 1 July 2026); Query/Search/Preview Statement (FE blocks the action if the resolved date/range falls before 1 July 2026, however set); CSV Upload (FE validates the CSV's date column and rejects upload with "File is not supported" if any record predates 1 July 2026). Reason (per comment): some data has not been stored in DB prior to July.

## Acceptance Criteria
*(All items below are `derived` from the description's numbered "Expected Behaviour" flow — the ticket has no separate "Acceptance Criteria" heading.)*
- AC-1 (derived): A system alert is triggered by BE health check when Centroid data is missing.
- AC-2 (derived): L1 can retrieve the missing data manually from Centroid and prepare it as CSV per the relevant statement table template.
- AC-3 (derived): L1/PM can create a new patch in Root Admin.
- AC-4 (derived): Root Admin user must select the tenant/client before any other action.
- AC-5 (derived): Root Admin user can upload the missing-data CSV for the selected statement table type.
- AC-6 (derived): BE validates and stores the uploaded file/data for patching.
- AC-7 (derived): Root Admin user can select the statement date/month to patch and regenerate.
- AC-8 (derived): Root Admin user can optionally preview one account statement before patching.
- AC-9 (derived): Root Admin user can trigger Patch and Regenerate.
- AC-10 (derived): Clicking Patch causes BE to patch the missing data to DB (DB update only, no regeneration).
- AC-11 (derived): Clicking Regenerate causes BE to regenerate the affected statement PDF(s) from the Patched Dataset.
- AC-12 (derived): Clicking Download allows the user to download the generated PDF(s) as a ZIP file.
- AC-13 (derived): Every Patch job is displayed in Patch History.
- AC-14 (derived): No statement email is sent after manual upload / patch / regeneration.
- AC-15 (derived): Regenerated statements replace the corresponding existing Membersite statement, and the new PDF overrides the old one (BE does not need to retain the old PDF) — per product review comment 2026-08-06.

## Error Messages
*(Upload CSV File Validation and Snackbar Mapping — source: description, revised via comment by Chin Yee Heng, 2026-09-09)*
- ERR-1: "Invalid file format. Upload a .csv file." (File is not .csv)
- ERR-2: "File is empty." (File is empty)
- ERR-3: "File exceeds 5MB limit." (File exceeds 5MB)
- ERR-4: "Missing required column." (Missing required columns)
- ERR-5: "Account ID does not belong to this tenant." (Account ID not belonging to selected tenant)
- ERR-6: "Symbol does not belong to this tenant." (Symbol not belonging to selected tenant)
- ERR-7: "File contains invalid data." (FE-level field validation failed)
- ERR-8: "[Date Column Name] must be in yyyy-mm-dd format." (Date or Open Date not in correct format)
- ERR-9: "Close Date must be in -- or yyyy-mm-dd format." (Close Date not in correct format)
- ERR-10: "File contains data before 1 Jul 2026." (Record dated before 1 July 2026 — supports BR-27)

## Out of Scope
- DEMO Account IDs — the AccountID field displays LIVE Account IDs only; DEMO accounts are explicitly out of scope (per BR-13).

## Linked Issues
- WT-10203: [WT][CENTROID][BE] Store Exchange Rate in Open Position and Statement Summary (relates to)

## Sub-tasks
### WT-15428: [WT-14266] [WT][ROOT][Centroid] Support Upload Missing Statement Data and Regenerate Patched Daily Statements
- Type: QA Preparation | Status: REVIEW DONE
- Notes: TC sheet reviewed 2026-08-22 by Vong Thuy Thuy Trang with extensive coverage feedback (Role Management, Select Tenant, Section 2/3/4, cross-section integration, edge cases); actioned/dismissed responses logged 2026-08-24 by Ngoc Nam Phuong Truong.

### WT-15439: [WT][ROOT][Centroid] Support Upload Missing Statement Data and Regenerate Patched Daily Statements
- Type: Backend Development | Status: In SIT

### WT-15440: [WT][ROOT][Centroid] Support Upload Missing Statement Data and Regenerate Patched Daily Statements
- Type: Frontend Development | Status: In SIT

### WT-15651: [WT-14266] [WT][ROOT][Centroid] Support Upload Missing Statement Data and Regenerate Patched Daily Statements
- Type: QA Execution | Status: In Progress
- Notes: Testmo Run ID 301, Config "Root Admin".

### WT-15782: [WT][RAP][Centroid] Privileges – Patch and Regenerate Statement privileges displayed in wrong order, and "Page" missing from the View privilege label
- Type: SIT Bug | Status: Ready to Test in SIT

### WT-15786: [WT][RAP][Centroid] Statement Patch & Regeneration – Whole page turns blank after clicking Search in Statement Data Query & Patch section
- Type: SIT Bug | Status: Ready to Test in SIT

### WT-15789: [WT][RAP][Centroid] Statement Patch & Regeneration – Clicking Preview Statement auto-downloads the PDF
- Type: SIT Bug | Status: Ready to Test in SIT

### WT-15790: [WT][RAP][Centroid] Statement Patch & Regeneration – Preview modal displays double scrollbar
- Type: SIT Bug | Status: Ready to Test in SIT

### WT-15791: [WT][RAP][Centroid] Statement Patch & Regeneration – Search and Export Data buttons not displayed in default disabled state
- Type: SIT Bug | Status: Won't Do (confirmed not-a-bug: Executed Orders is default table, uses "Fetch from Centroid" only, no Search/Export Data by design)

### WT-15792: [WT][RAP][Centroid] Statement Patch & Regeneration – Patch History (Section 4) not accessible before selecting a client
- Type: SIT Bug | Status: Ready to Test in SIT
- Notes: PM clarified Patch History must show all tenants' patch records as an activity log, unfiltered by tenant selection.

### WT-15794: [WT][RAP][Centroid] Statement Patch & Regeneration – Patch History table columns do not match the designed column set
- Type: SIT Bug | Status: Ready to Test in SIT

### WT-15795: [WT][RAP][Centroid] Statement Patch & Regeneration – Select Client dropdown does not display all tenants available in current RAP
- Type: SIT Bug | Status: Ready to Test in SIT
- Notes: dropdown currently limited to tenants on a LIVE server; team agreed to test with demo brokers temporarily.

### WT-15796: [WT][RAP][Centroid] Statement Patch & Regeneration – Upload CSV button and "Download template here" link do not appear after selecting a tenant
- Type: SIT Bug | Status: Won't Do (confirmed not-a-bug: Executed Orders has no CSV template/upload by design)

### WT-15798: [WT][RAP][Centroid] Statement Patch & Regeneration – Working state is not reset when navigating away and returning to the page
- Type: SIT Bug | Status: Ready to Test in SIT

### WT-15802: [WT][RAP][Centroid] Statement Patch & Regeneration – Upload CSV field still displays the file name after upload is rejected as "not supported"
- Type: SIT Bug | Status: Ready to Test in SIT

### WT-15803: [WT][RAP][Centroid] Statement Patch & Regeneration – Statement Summary data table columns display does not match the defined
- Type: SIT Bug | Status: Ready to Test in SIT

### WT-15807: [WT][RAP][Centroid] Statement Patch & Regeneration – Statement Summary backup CSV contains extra columns not in the defined CSV template
- Type: SIT Bug | Status: Won't Do (PM confirmed Credit / Buy Exchange Rate / Sell Exchange Rate are intentional additions per WT-10199, not yet reflected in the ticket's CSV template text at filing time)

### WT-15808: [WT][RAP][Centroid] Statement Patch & Regeneration – Statement Data Query table still returns data when filtering a month the account has no data for
- Type: SIT Bug | Status: Dev in Progress

### WT-15809: [WT][RAP][Centroid] Statement Patch & Regeneration – "End Datetime must not exceed 1 day from Start Datetime" error still shows when the range does not exceed 1 day
- Type: SIT Bug | Status: Ready to Test in SIT

### WT-15810: [WT][RAP][Centroid] Statement Patch & Regeneration – Start/End Datetime datepicker UI does not match the design mockup
- Type: SIT Bug | Status: Won't Do (team agreed to keep the Mantine date-time-picker library UI instead of matching the mockup exactly)

### WT-15811: [WT][RAP][Centroid] Statement Patch & Regeneration – Account ID and date range are not retained when changing the Statement Table option
- Type: SIT Bug | Status: Ready to Test in SIT
- Notes: PM confirmed 2026-09-09 — Account ID, Start/End Datetime, Select Month must be retained across Statement Table changes (now reflected in BR-13).

### WT-15812: [WT][RAP][Centroid] Statement Patch & Regeneration – Uploaded CSV file is not reset when changing Statement Type (Daily > Monthly)
- Type: SIT Bug | Status: Ready to Test in SIT

### WT-15813: [WT][RAP][Centroid] Statement Patch & Regeneration – Patch data from uploaded CSV does not update to DB
- Type: SIT Bug | Status: Open

### WT-15814: [WT][RAP][Centroid] Statement Patch & Regeneration – Cannot generate Preview Statement after patching
- Type: SIT Bug | Status: Open

### WT-15815: [WT][RAP][Centroid] Statement Patch & Regeneration – Statement Table and Statement Type fields get narrowed when the uploaded CSV has a long file name
- Type: SIT Bug | Status: Ready to Test in SIT

### WT-15818: [WT][RAP][Centroid] Statement Patch & Regeneration – Open Price accepts comma-formatted text (non-numeric) without validation error on CSV upload
- Type: SIT Bug | Status: Pending
- Notes: unresolved — see "Requirement Changes" and "Open Items from Comments"; PM confirmation on comma-in-CSV handling still outstanding.

### WT-15819: [WT][RAP][Centroid] Statement Patch & Regeneration – Account ID dropdown does not sort Account IDs in numerical ascending order
- Type: SIT Bug | Status: Ready to Test in SIT

### WT-15820: [WT][RAP][Centroid] Statement Patch & Regeneration – Export Data button is not disabled when a CSV file is uploaded
- Type: SIT Bug | Status: Ready to Test in SIT

## Figma Links
None. No `figma.com` URL appears anywhere in the parent ticket (description or 37 comments) or in any of the 28 sub-tasks (description/comments). One comment (Chin Yee Heng, 2026-08-26) states "Figma is updated" but supplies no link. Per the skill's non-interactive default for a ticket with no discoverable Figma link, this was recorded as "no Figma links found" and the run continued without invoking `figma-retriever`.

## Visual Context
- `aae9b2ab-213e-435d-a05e-0f9e2ca323cf.png` (parent, undated attachment): full-page mockup of an **earlier** design — shows only 3 visible action sections (1 Select Tenant, 2 Upload Statement Data, 3 Patch & Regenerate Statement) plus Patch History, a combined "Patch Range" dropdown, and a single "Patch & Regenerate" button. This does not match the final 4-section / separate-Search-Preview-Regenerate spec in the current description — it is superseded by the 8/18 and 8/20 "changed whole mockup" revisions noted in the change log.
- `image-20260624-080642.png` (parent, referenced explicitly by WT-15810): the Start Datetime design mockup — shows year-jump (`«`) and month-jump (`‹›`) calendar controls plus three separate HH/MM/SS spinner fields with up/down arrows. Confirms WT-15810's Expected Result description is accurate; current build instead uses the Mantine library's single text-input time picker (team agreed to keep as-is, ticket marked Won't Do).
- `image-20260909-040650.png` (parent, 2026-09-09): "Upload CSV File Validation and Snackbar Mapping" table screenshot — content matches the Error Messages section exactly (10 validation rows), confirming the description text is current as of the latest revision.
- Given the volume of attached evidence (33 parent images + 24 sub-task attachments, including 11 bug-repro screen-recordings expanded to 587 total video frames under `*-frames/` folders, plus 3 PDF statement samples on WT-15813), the remaining files were downloaded to `tasks/WT-14266/base/attachments/` but not individually described here — each SIT Bug sub-task's Steps/Expected/Actual text above already documents what its accompanying screenshot/video shows; open the corresponding file(s) directly if visual confirmation is needed for a specific bug.

## Figma Discrepancies
None — no Figma link was found for this ticket (see Figma Links).

## Open Items from Comments
- Comma-formatted CSV values: PM confirmation on whether `1,000`-style values inside an **uploaded CSV** should be rejected as invalid numeric data is still outstanding as of the last comment on WT-15818 (Le Ngoc Loan Anh, 2026-09-09) — see "Requirement Changes" above.
- Statement Summary calculation source: Quoc Binh Nguyen asked (2026-08-12) whether Statement Summary should also be treated as an "overload"/calculation table, and whether any statement exists with full data across all tables for test purposes — no direct reply is recorded in the thread (later comments on data-source consolidation, 2026-08-18, may partially answer this but do not address it explicitly).
- Historical regenerate scope across Daily/Monthly: Quoc Binh Nguyen raised (2026-09-08) that patching one Executed Order date affects both the Daily statement for that date and the Monthly statement for that month, requiring two regenerations, and asked how this should be represented at the UI level (and whether it also applies to the other 5 statement tables) — no reply is recorded in the thread as of the last comment fetched.

# Test Cases — WT-14266

**Issue:** [WT-14266](https://aquariux.atlassian.net/browse/WT-14266)
**Fetched:** 2026-09-09
**Total:** 120 cases (TC-220320 re-fetched 2026-09-09, initial fetch had failed)

## Summary

| Status | Count |
|---|---|
| ✅ Automated | 0 |
| 🔧 Can Automate | 0 |
| 🚧 In Progress | 0 |
| ❌ Not Automatable | 0 |
| ⬜ Unset | 120 |

| Priority | Count |
|---|---|
| High | 120 |
| Medium | 0 |
| Low | 0 |

## Case Groups

| Group | Cases | Automated | Can Automate | Folders |
|---|---|---|---|---|
| Statement Patch & Regeneration | 114 | 0 | 0 | 4829 |
| Role Management | 3 | 0 | 0 | 4830 |
| User Management | 3 | 0 | 0 | 4831 |

---

## Full Case Details

### Statement Patch & Regeneration (113 cases)

#### TC-220239 · Statement Patch & Regeneration - Form - Select Client - verify default state and placeholder
**Priority:** High | **Automation:** Unset

**Description:** Verify that Select Client dropdown displays placeholder 'Select client' by default and all other fields in Section 1 are disabled until client is selected

**Prerequisites:**
- User has full privileges
- Page loaded fresh (no prior selection)

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Navigate to Troubleshoot Platform > Statement Patch & Regeneration | Loading |
| 2 | Observe Select Client dropdown | 1. Dropdown displays placeholder text: 'Select client' 2. No tenant pre-selected |
| 3 | Observe Statement Table dropdown | 1. Field is disabled / not clickable 2. Shows default 'Executed Orders' but cannot be changed |
| 4 | Observe Statement Type dropdown | 1. Field is disabled / not clickable 2. Shows default 'Daily' but cannot be changed |
| 5 | Observe Upload CSV area (Choose file button) | 1. [Choose file] button is NOT displayed |
| 6 | Observe Section 2 (Statement Data Query & Patch) — all fields | 1. Account ID dropdown: disabled, shows placeholder 'Select Account ID' 2. Start Datetime (UTC) field: disabled 3. End Datetime (UTC) field: disabled 4. [Search] button: disabled 5. [Export data] button: disabled 6. Statement Data Table: empty, shows 'No items available' 7. Daylight Saving toggle: disabled 8. Remarks field: disabled 9. [Patch] button: disabled |
| 7 | Observe Section 3 (Preview Statement) | 1. Statement Type dropdown: shows 'Daily' (default) 2. Select Date field: shows date 3. Account ID: shows placeholder 'Select Account ID' 4. [Preview Statement] button: disabled |
| 8 | Observe Section 4 (Patch History) | 1. Patch History section is ACCESSIBLE regardless of client selection 2. Table displays, [Refresh] button enabled 3. Pagination functional |

**Test Data:** None

---

#### TC-220240 · Statement Patch & Regeneration - Form - Select Client - verify dropdown options format and content
**Priority:** High | **Automation:** Unset

**Description:** Verify that Select Client dropdown displays all tenants in 'Tenant Name (Short Code)' format

**Prerequisites:**
- User has full privileges
- Multiple tenants exist in Root Admin system

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Click on Select Client dropdown to expand | Dropdown opens |
| 2 | Observe dropdown options | 1. All tenants available in Root Admin are listed, sort is not required 2. Format per option: 'Tenant Name (Short Code)' Example: 'Tin Shing International Precious Metals Limited (tinshing)' 3. No empty or malformed entries |
| 3 | Scroll through the list if more than visible area | 1. All tenants accessible via scroll 2. No duplicate entries |

**Test Data:** None

---

#### TC-220241 · Statement Patch & Regeneration - Form - Select Client - verify selecting tenant enables all Section 1 and Section 2 fields
**Priority:** High | **Automation:** Unset

**Description:** Verify that after selecting a tenant, all Section 1 fields (Statement Table, Statement Type, Upload CSV) and Section 2 fields become enabled and interactive

**Prerequisites:**
- User has full privileges
- At least one tenant exists

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Select a tenant from dropdown (e.g. 'Tin Shing International Precious Metals Limited (tinshing)') | Selection confirmed |
| 2 | Observe Select Client dropdown after selection | 1. Dropdown displays selected tenant: 'Tin Shing International Precious Metals Limited (tinshing)' 2. Selection persists (not reverting to placeholder) |
| 3 | Observe Statement Table dropdown | 1. Field becomes enabled / clickable 2. Default selected: 'Executed Orders' |
| 4 | Observe Statement Type dropdown | 1. Field becomes enabled / clickable 2. Default selected: 'Daily' |
| 5 | Observe Upload CSV area | 1. [Choose file] button becomes enabled / clickable 2. Text remains 'No file chosen' until user selects file |
| 6 | Observe 'Download template here' link | 1. Link is displayed (visible and clickable) when Statement Table ≠ Executed Orders 2. If Statement Table = Executed Orders (current default), 'Download template here' may not display |
| 7 | Observe Section 2 (Statement Data Query & Patch) | 1. Account ID dropdown: enabled, shows 'Select Account ID' placeholder 2. Start Datetime (UTC): enabled, shows date format placeholder 3. End Datetime (UTC): enabled, shows date format placeholder 4. [Search] button: remains disabled until all mandatory filters filled 5. [Export data] button: disabled (table still empty) 6. [Patch] button: disabled (table still empty) |
| 8 | Observe Section 3 (Preview Statement) | 1. Statement Type: enabled 2. Select Date: enabled 3. Account ID: enabled 4. [Preview Statement] button: disabled until all 3 fields are filled |

**Test Data:** Selected: Tin Shing International Precious Metals Limited (tinshing) Statement Table ≠ Executed Orders

---

#### TC-220242 · Statement Patch & Regeneration - Form - Select Client - verify switching tenant resets all working state
**Priority:** High | **Automation:** Unset

**Description:** Verify that changing selected tenant clears/resets all data in Section 1 (Statement Table, Statement Type, uploaded file) and Section 2 (query filters, table data, remarks) back to default

**Prerequisites:**
- User has full privileges
- Tenant A currently selected
- Section 2 has data: query performed, table populated, remarks entered
- Tenant B exists

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | With Tenant A selected, populate working state: - Statement Table = Settled Position - Statement Type = Monthly - Upload a CSV file - Query data so table has records - Enter remarks: 'Test remark' | State populated |
| 2 | Switch Select Client to Tenant B | Switch completed |
| 3 | Observe Statement Table dropdown | 1. Reset to default: 'Executed Orders' |
| 4 | Observe Statement Type dropdown | 1. Reset to default: 'Daily' |
| 5 | Observe Upload CSV area | 1. Reset to 'No file chosen' 2. Previously uploaded file reference cleared |
| 6 | Observe Section 2 — query filters | 1. Account ID: reset to placeholder 'Select Account ID' 2. Start Datetime: cleared 3. End Datetime: cleared |
| 7 | Observe Section 2 — Statement Data Table | 1. Table is empty / shows 'No items available' 2. All previously loaded data cleared |
| 8 | Observe Remarks field | 1. Remarks field cleared (shows placeholder 'Enter your remarks') |
| 9 | Observe [Patch] button | 1. [Patch] button disabled (table empty) |
| 10 | Observe Section 3 — Preview Statement fields | 1. Account ID reset to placeholder 2. [Preview Statement] button disabled |

**Test Data:** Tenant A: tinshing Statement Table: Settled Position Statement Type: Monthly Remarks: Test remark Tenant B: (another available tenant)

---

#### TC-220243 · Statement Patch & Regeneration - State - Working state reset - verify page refresh (F5 / browser refresh) clears all working data
**Priority:** High | **Automation:** Unset

**Description:** Verify that refreshing the page (F5 or browser refresh button) clears all working state: uploaded CSV, table data, query filters, Remarks — page returns to initial state

**Prerequisites:**
- Tenant selected: tinshing
- Statement Table = Open Position
- CSV uploaded with data
- Remarks filled
- Working state fully populated

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe current working state before refresh | 1. Select Client: 'tinshing' selected 2. Statement Table: 'Open Position' 3. Upload area: shows CSV filename 4. Statement Data Table: has data 5. Remarks: has text |
| 2 | Press F5 key to refresh page | 1. Page reloads completely 2. No warning modal or 'unsaved changes' prompt |
| 3 | Observe Select Client dropdown | 1. Reset to placeholder: 'Select client' 2. No tenant pre-selected |
| 4 | Observe Statement Table and Statement Type | 1. Statement Table: disabled (no tenant selected) 2. Statement Type: disabled 3. Default values shown but not interactive |
| 5 | Observe Upload CSV area | 1. Hidden (no tenant selected) OR shows 'No file chosen' if visible 2. Previously uploaded CSV completely gone |
| 6 | Observe Statement Data Table | 1. Table empty: 'No items available' 2. All working data cleared |
| 7 | Observe Remarks field | 1. Remarks cleared — shows placeholder |
| 8 | Click browser refresh button (circular arrow in address bar) | 1. Same behavior as F5 2. Page returns to initial state 3. All working data cleared |

**Test Data:** None

---

#### TC-220244 · Statement Patch & Regeneration - State - Working state reset - verify navigating away and returning clears all working data
**Priority:** High | **Automation:** Unset

**Description:** Verify that navigating to another page then returning to Statement Patch & Regeneration clears all working state — unsaved work is silently discarded

**Prerequisites:**
- Tenant selected: tinshing
- Statement Table = Deposit/Withdrawal
- CSV uploaded with 3 rows
- Some rows edited
- Remarks: 'Navigation test'
- [Patch] NOT clicked (unsaved work)

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe current working state | 1. Tenant: tinshing selected 2. Table: 3 data rows (some edited) 3. Remarks: 'Navigation test' 4. Unsaved changes exist |
| 2 | Navigate to another page (e.g. click 'Dashboard' or 'Role Management' in sidebar) | 1. Page navigates away 2. NO warning modal about unsaved changes 3. Unsaved work silently discarded |
| 3 | Navigate back to Troubleshoot Platform > Statement Patch & Regeneration | 1. Page loads fresh |
| 4 | Observe Select Client dropdown | 1. Reset to placeholder: 'Select client' 2. Previous tenant selection NOT retained |
| 5 | Observe all Section 1 fields | 1. Statement Table: disabled, default 'Executed Orders' 2. Statement Type: disabled, default 'Daily' 3. Upload CSV: hidden or disabled |
| 6 | Observe Statement Data Table | 1. Table empty: 'No items available' 2. Previously uploaded/edited data completely gone 3. Edits NOT preserved |
| 7 | Observe Remarks field | 1. Remarks cleared 2. 'Navigation test' text NOT retained |
| 8 | Observe Patch History section | 1. Patch History still accessible 2. Shows all tenants' patch records (not filtered) 3. Previous COMPLETED patches still visible (persisted in DB) [Only working/unsaved state is lost; committed patches remain] |

**Test Data:** None

---

#### TC-220245 · Statement Patch & Regeneration - Form - Select Client - verify Patch History section remains unfiltered regardless of tenant selection
**Priority:** High | **Automation:** Unset

**Description:** Verify that Patch History table displays ALL tenants' records and is NOT affected by Select Client selection — consistent with 'EXCEPT Patch History section' behavior

**Prerequisites:**
- User has full privileges
- Multiple tenants have patch history records (e.g., Tenant A: tinshing, Tenant B: demo_tenant)
- Patch History has records from different tenants

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Before selecting any tenant, observe Patch History table | 1. Patch History table displays records from ALL tenants 2. Name column shows different tenant names 3. Short Code column shows different tenant short codes [This confirms Patch History is accessible without tenant selection] |
| 2 | Select Tenant A (tinshing) | 1. Patch History table STILL displays records from ALL tenants 2. Table is NOT filtered to show only Tenant A 3. Records from Tenant B and other tenants remain visible [Patch History is independent of Select Client — 'EXCEPT Patch History section'] |
| 3 | Switch to Tenant B | Action confirmed |
| 4 | Observe Patch History table | 1. Patch History table STILL displays records from ALL tenants 2. No filtering applied based on tenant selection 3. Name and Short Code columns continue to show multi-tenant data [Confirms: Patch History behavior is consistent regardless of tenant selection] |

**Test Data:** None

---

#### TC-220246 · Statement Patch & Regeneration - Form - Select Client - verify Account ID dropdown in Section 2 shows only accounts belonging to selected tenant
**Priority:** High | **Automation:** Unset

**Description:** Verify that after selecting a tenant, the Account ID dropdown in Section 2 shows ONLY LIVE accounts belonging to that specific tenant — not all accounts in system

**Prerequisites:**
- User has full privileges
- Tenant A (tinshing) has LIVE accounts: 710001, 710002, 710003
- Tenant A also has DEMO accounts: 810001
- Tenant B has different accounts: 990001, 990002

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Select Tenant A (tinshing) | Selection confirmed |
| 2 | Click Account ID dropdown in Section 2 | 1. Dropdown shows only accounts belonging to Tenant A Example: 710001, 710002, 710003 2. DEMO account 810001 is NOT listed (LIVE only) 3. Tenant B accounts (990001, 990002) are NOT listed |
| 3 | Switch to Tenant B | Switch confirmed |
| 4 | Click Account ID dropdown in Section 2 | 1. Dropdown now shows only Tenant B accounts Example: 990001, 990002 2. Tenant A accounts no longer visible 3. Only LIVE accounts listed |

**Test Data:** None

---

#### TC-220247 · Statement Patch & Regeneration - Form - Select Client - verify Account ID in Section 3 (Preview) also filters by selected tenant
**Priority:** High | **Automation:** Unset

**Description:** Verify that Account ID dropdown in Preview Statement section (Section 3) also shows only LIVE accounts for the selected tenant

**Prerequisites:**
- User has full privileges
- Tenant A selected (has LIVE accounts 710001, 710002)
- Tenant A has DEMO account 810001

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Select Tenant A | Selection confirmed |
| 2 | Click Account ID dropdown in Section 3 (Preview Statement) | 1. Dropdown shows only LIVE accounts for Tenant A: 710001, 710002 2. DEMO account 810001 NOT listed 3. Accounts from other tenants NOT listed |

**Test Data:** None

---

#### TC-220248 · Statement Patch & Regeneration - Form - Statement Table dropdown - verify options, order, and default
**Priority:** High | **Automation:** Unset

**Description:** Verify Statement Table dropdown displays 6 options in correct sequence with 'Executed Orders' as default

**Prerequisites:**
- Tenant selected
- Statement Table dropdown enabled

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe Statement Table dropdown default value | 1. Default selected: 'Executed Orders' |
| 2 | Click dropdown to expand and observe options | 1. Options in exact sequence: 1) Executed Orders 2) Settled Position 3) Open Position 4) Deposit/Withdrawal 5) Statement Summary 6) Interest Rate 2. No other options present 3. Single selection only |

**Test Data:** None

---

#### TC-220249 · Statement Patch & Regeneration - Form - Statement Type dropdown - verify options, order, and default
**Priority:** High | **Automation:** Unset

**Description:** Verify Statement Type dropdown displays Daily and Monthly options with 'Daily' as default

**Prerequisites:**
- Tenant selected
- Statement Type dropdown enabled

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe Statement Type dropdown default value | 1. Default selected: 'Daily' |
| 2 | Click dropdown to expand and observe options | 1. Options: 1) Daily 2) Monthly 2. No other options 3. Single selection only |

**Test Data:** None

---

#### TC-220250 · Statement Patch & Regeneration - Form - Statement Table = Executed Orders - verify Upload CSV and Download template hidden
**Priority:** High | **Automation:** Unset

**Description:** Verify that when Statement Table = 'Executed Orders', the Upload CSV area and 'Download template here' link are NOT displayed (Executed Orders does not support CSV upload; data is queried from Centroid API only)

**Prerequisites:**
- Tenant selected
- Statement Table = Executed Orders (default)

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe the page with Statement Table = 'Executed Orders' selected | Observation setup |
| 2 | Look for 'Download template here' link | 1. 'Download template here' link is NOT displayed / hidden |
| 3 | Look for Upload CSV area ([Choose file] + 'No file chosen') | 1. Upload CSV area ([Choose file] button + text) is NOT displayed / hidden [Note: Executed Orders data is pulled from Centroid API — no manual CSV upload] |
| 4 | Switch Statement Table to 'Settled Position' | Switch confirmed |
| 5 | Observe 'Download template here' and Upload CSV area | 1. 'Download template here' link now VISIBLE and clickable 2. Upload CSV area now VISIBLE: [Choose file] button enabled + 'No file chosen' text |
| 6 | Switch Statement Table back to 'Executed Orders' | Switch confirmed |
| 7 | Verification | 1. 'Download template here' link hidden again 2. Upload CSV area hidden again |

**Test Data:** None

---

#### TC-220251 · Statement Patch & Regeneration - Form - Statement Table change - verify table columns in Section 2 update accordingly
**Priority:** High | **Automation:** Unset

**Description:** Verify that changing Statement Table selection updates the Statement Data Table column headers in Section 2 to match the selected table type

**Prerequisites:**
- Tenant selected
- Statement Table dropdown enabled

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Select Statement Table = 'Executed Orders', observe table columns | 1. Table columns (Section 2): Account ID, Item, Order Date, Order Time, Order Ref, Bought Lot(s), Sold Lot(s), New/Liq., Exchange Rate, Executed Price, Action |
| 2 | Select Statement Table = 'Settled Position', observe table columns | 1. Table columns: Account ID, Date, Item, Open Ref, Open Date, Open Price, Close Ref, Close Date, Close Lot(s), Close Price, Exchange Rate, Interest, Commission, Profit/Loss, Actions |
| 3 | Select Statement Table = 'Open Position', Statement Type = Daily, observe table columns | 1. Table columns: Account ID, Date, Order Ref, Item, Net Volume, Average Price, Closing Price, Exchange Rate, Unrealised Interest, Daily Interest, Commission, Floating Profit/Loss, Notional, Actions |
| 5 | Select Statement Table = 'Deposit/Withdrawal', observe table columns | 1. Table columns: Account ID, Date, Order Ref, Description, Type, Amount,Actions |
| 6 | Select Statement Table = 'Statement Summary', Statement Type = Daily, observe table columns | 1. Table columns: Account ID, Date, Margin In, Monthly Profit/Loss, Margin Out, New Balance, Adjustment, Floating Profit/Loss, Unrealised Interest, Equity, Realised Interest, Margin Requirement, Commission, Call Margin, Credit 信用额度, Actions |
| 8 | Select Statement Table = 'Interest Rate', observe table columns | 1. Table columns: Account ID, Date, Taker Feed, Limit Symbol Group, Symbol, Sell Rate, Buy Rate, Actions |

**Test Data:** None

---

#### TC-220252 · Statement Patch & Regeneration - Toggle/Button - Download template here - verify correct CSV template downloaded per Statement Table + Type combination
**Priority:** High | **Automation:** Unset

**Description:** Verify clicking 'Download template here' downloads correct CSV template with matching column headers for each Statement Table + Statement Type combination

**Prerequisites:**
- Tenant selected
- Statement Table ≠ Executed Orders

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Select Statement Table = 'Settled Position', Statement Type = 'Daily'/'Monthly' | - |
| 2 | Click 'Download template here' | 1. CSV file downloads 2. Filename indicates table type (e.g. contains 'settled_position') 3. CSV headers match: Account ID, Date, Item, Open Ref, Open Date, Open Price, Close Ref, Close Date, Close Lot(s), Close Price, Exchange Rate, Interest, Commission, Profit/Loss, IsDeleted 4. File is empty (template only — no data rows) |
| 3 | Select Statement Table = 'Open Position', Statement Type = 'Daily'/'Monthly' | - |
| 4 | Click 'Download template here' | 1. CSV headers match: Account ID, Date, Order Ref, Item, Net Volume, Average Price, Closing Price, Exchange Rate, Unrealised Interest, Daily Interest, Commission, Floating Profit/Loss, Notional, IsDeleted |
| 5 | Select Statement Table = 'Deposit/Withdrawal' | - |
| 6 | Click 'Download template here' | 1. CSV headers match: Account ID, Date, Order Ref, Description, Type, Amount, IsDeleted |
| 7 | Select Statement Table = 'Statement Summary', Statement Type = 'Daily'/'Monthly' | - |
| 8 | Click 'Download template here' | 1. CSV headers match: Account ID, Date, New Balance, Equity, Call Margin, Currency, IsDeleted |
| 9 | Select Statement Table = 'Interest Rate', Statement Type = 'Daily'/'Monthly' | - |
| 10 | Click 'Download template here' | 1. CSV headers match: Account ID, Date, Taker Feed, Limit Symbol Group, Symbol, Sell Rate, Buy Rate, IsDeleted |

**Test Data:** None

---

#### TC-220253 · Statement Patch & Regeneration - Form - Statement Table change - verify switching table type resets Section 2 data
**Priority:** High | **Automation:** Unset

**Description:** Verify that changing the Statement Table selection clears/resets any previously loaded data in Statement Data Table, query filters retain Account ID but datetime resets where applicable

**Prerequisites:**
- Tenant selected
- Statement Table = Settled Position, table has data from previous query/upload

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | With Settled Position selected and table containing data, switch Statement Table to 'Open Position' | - |
| 2 | Observe Statement Data Table | 1. Table is cleared / shows 'No items available' 2. Column headers update to Open Position columns 3. Previously loaded Settled Position data is gone |
| 3 | Observe query filters | 1. Account ID: retained (same tenant scope) 2. Start/End Datetime: retained 3. [Search] button state reflects current filter completeness |
| 4 | With Statement Table = Open Position, upload a valid CSV file | 1. Upload area shows filename: 'open_position_data.csv' 2. Statement Data Table populates with CSV data 3. Query filters become DISABLED (CSV mode) |
| 5 | Switch Statement Table to 'Executed Orders' | 1. Upload CSV area becomes HIDDEN (Executed Orders does not support CSV upload) 2. Statement Data Table clears — shows 'No items available' 3. 'Download template here' link hidden |
| 6 | Switch Statement Table back to 'Open Position' | 1. Upload CSV area re-appears (visible again) 2. Filename shows: 'No file chosen' — CSV is CLEARED, not just hidden 3. Statement Data Table: empty ('No items available') 4. Previous CSV data NOT restored 5. Query filters re-enabled (no longer in CSV mode) [Confirms: state is truly CLEARED when switching tables, not just visually hidden] |
| 7 | Attempt to click [Patch] button | 1. [Patch] button: DISABLED (table empty) [No residual state from previous CSV upload] |

**Test Data:** File: open_position_data.csv

---

#### TC-220254 · Statement Patch & Regeneration - Form - Statement Type change - verify switching between Daily and Monthly updates query filter UI
**Priority:** High | **Automation:** Unset

**Description:** Verify that switching Statement Type between Daily and Monthly changes the query filter fields in Section 2 accordingly

**Prerequisites:**
- Tenant selected
- Statement Type = Daily (default)

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe Section 2 query filters with Statement Type = Daily | 1. Filter fields shown: Account ID * (dropdown), Start Datetime (UTC) * (date-time picker, format: yyyy-mm-dd hh:mm:ss), End Datetime (UTC) * (date-time picker, format: yyyy-mm-dd hh:mm:ss), [Search] button, [Export data] button |
| 2 | Switch Statement Type to 'Monthly' | - |
| 3 | Observe Section 2 query filters | 1. Filter fields change to: Account ID * (dropdown), Select Month * (month picker), [Search] button, [Export data] button 2. Start/End Datetime fields replaced by Select Month field |
| 4 | Switch Statement Type back to 'Daily' | 1. Filters revert to: Account ID + Start Datetime + End Datetime 2. Select Month field replaced by datetime fields |

**Test Data:** None

---

#### TC-220255 · Statement Patch & Regeneration - State - Working state reset - verify Statement Type change silently clears uploaded CSV and working data
**Priority:** High | **Automation:** Unset

**Description:** Verify that changing Statement Type (Daily ↔ Monthly) silently clears: uploaded CSV filename, Statement Data Table, query filters, Remarks — no warning modal

**Prerequisites:**
- Tenant selected
- Statement Table = Settled Position (not Executed Orders)
- CSV uploaded: filename shows 'test_data.csv'
- Statement Data Table has data from CSV
- Remarks filled: 'Test remark'

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe current state before changing Statement Type | 1. Upload area shows: 'test_data.csv' 2. Statement Data Table: has data rows 3. Remarks: 'Test remark' 4. Statement Type: 'Daily' |
| 2 | Change Statement Type from 'Daily' to 'Monthly' | 1. NO warning modal appears (silent clear) 2. Statement Type changes to 'Monthly' |
| 3 | Observe Upload CSV area | 1. Filename reset to: 'No file chosen' 2. Previously uploaded CSV reference cleared |
| 4 | Observe Statement Data Table | 1. Table cleared — shows 'No items available' 2. All data rows from CSV are gone |
| 5 | Observe query filter fields | 1. Account ID: reset to placeholder 'Select Account ID' 2. Date/Month picker: reset to default 3. Query filters re-enabled (no longer disabled by CSV upload) |
| 6 | Observe Remarks field | 1. Remarks cleared — shows placeholder 'Enter your remarks' |
| 7 | Observe [Patch] and [Export data] buttons | 1. [Patch] button: DISABLED (table empty) 2. [Export data] button: DISABLED (table empty) |
| 8 | Switch Statement Type back to 'Daily' | 1. Same reset behavior — no data restored 2. Working state remains cleared |

**Test Data:** None

---

#### TC-220256 · Statement Patch & Regeneration - Form - Upload CSV - verify default state and file selection flow
**Priority:** High | **Automation:** Unset

**Description:** Verify Upload CSV area: default shows [Choose file] + 'No file chosen', after selecting file shows filename.csv

**Prerequisites:**
- Tenant selected
- Statement Table ≠ Executed Orders (e.g. Settled Position)
- Upload CSV area visible

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe Upload CSV area before selecting any file | 1. [Choose file] button displayed and enabled 2. Text next to button shows: 'No file chosen' |
| 2 | Click [Choose file] button | 1. OS file picker dialog opens |
| 3 | Select a valid .csv file (e.g. 'settled_position_patch_20260816.csv') | 1. File picker closes 2. Text next to [Choose file] updates to show selected filename: 'settled_position_patch_20260816.csv' 3. File is not yet uploaded to server at this point (pending validation) |
| 4 | Click [Choose file] again and select a different file | 1. Previously displayed filename replaced with new filename: 'another_file.csv' 2. Only 1 file can be selected at a time (no multi-file) |

**Test Data:** File: settled_position_patch_20260816.csv; File: another_file.csv

---

#### TC-220257 · Statement Patch & Regeneration - Validation - Upload CSV - verify .csv file extension required
**Priority:** High | **Automation:** Unset

**Description:** Verify that only files with .csv extension are accepted; non-.csv files are rejected with snackbar error

**Prerequisites:**
- Tenant selected
- Statement Table = Settled Position
- Upload CSV area visible

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Click [Choose file] and select a .xlsx file | 1. Snackbar error displays: 'File is not supported' 2. File is NOT loaded into Statement Data Table 3. Upload area reverts to 'No file chosen' or retains previous state |
| 2 | Click [Choose file] and select a .pdf file | 1. Snackbar error: 'File is not supported' |
| 3 | Click [Choose file] and select a .txt file | 1. Snackbar error: 'File is not supported' |
| 4 | Click [Choose file] and select a file with no extension | 1. Snackbar error: 'File is not supported' |
| 5 | Click [Choose file] and select a .CSV file (uppercase extension) | 1. File accepted (case-insensitive extension check) |
| 6 | Click [Choose file] and select a valid .csv file | 1. File accepted 2. No error snackbar 3. Data auto-populates Statement Data Table |

**Test Data:** File: data.xlsx; File: report.pdf; File: data.txt; File: datafile (no extension); File: DATA.CSV; File: valid_data.csv

---

#### TC-220258 · Statement Patch & Regeneration - Validation - Upload CSV - verify empty file rejected
**Priority:** High | **Automation:** Unset

**Description:** Verify that empty CSV file (0 bytes or headers only with no data rows) is rejected with snackbar error

**Prerequisites:**
- Tenant selected
- Statement Table = Settled Position

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Prepare a CSV file with 0 bytes (completely empty) | - |
| 2 | Click [Choose file] and select the 0-byte file | 1. Snackbar error: 'File is not supported' 2. Statement Data Table remains empty |
| 3 | Prepare a CSV file with header row only (no data rows) | - |
| 4 | Click [Choose file] and select the headers-only file | 1. Snackbar error: 'File is not supported' 2. Statement Data Table remains empty |

**Test Data:** File: empty_0bytes.csv (0 KB); File: headers_only.csv (headers but 0 data rows)

---

#### TC-220259 · Statement Patch & Regeneration - Validation - Upload CSV - verify 5MB file size limit
**Priority:** High | **Automation:** Unset

**Description:** Verify that CSV file exceeding 5MB is rejected; file exactly 5MB is accepted (boundary test)

**Prerequisites:**
- Tenant selected
- Statement Table = Settled Position

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Prepare CSV file exactly 5MB (5,242,880 bytes) with valid content | - |
| 2 | Click [Choose file] and select the 5MB file | 1. File accepted (boundary: equal to limit passes) 2. Data populates Statement Data Table 3. No error snackbar |
| 3 | Prepare CSV file slightly over 5MB (e.g. 5,242,881 bytes) | - |
| 4 | Click [Choose file] and select the over-5MB file | 1. Snackbar error: 'File is not supported' 2. Statement Data Table remains unchanged 3. File NOT loaded |

**Test Data:** File: exactly_5mb.csv (5.00 MB); File: over_5mb.csv (5.00+ MB)

---

#### TC-220260 · Statement Patch & Regeneration - Validation - Upload CSV - verify required columns check per Statement Table type
**Priority:** High | **Automation:** Unset

**Description:** Verify that CSV missing required columns for the selected Statement Table is rejected with snackbar error

**Prerequisites:**
- Tenant selected
- Statement Table = Settled Position
- Required columns: Account ID, Date, Item, Open Ref, Open Date, Open Price, Close Ref, Close Date, Close Lot(s), Close Price, Interest, Commission, Profit/Loss

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Prepare CSV missing 'Account ID' column (all other columns present) | - |
| 2 | Click [Choose file] and select the file | 1. Snackbar error: 'File is not supported' 2. Table not populated |
| 3 | Prepare CSV missing 'Profit/Loss' column | - |
| 4 | Click [Choose file] and select the file | 1. Snackbar error: 'File is not supported' |
| 5 | Prepare CSV with ALL required columns present but with extra columns added | - |
| 6 | Click [Choose file] and select the file with extra columns | 1. File accepted — extra columns ignored 2. Statement Data Table shows only the required columns |
| 7 | Prepare CSV with correct columns but in DIFFERENT order than template | - |
| 8 | Click [Choose file] and select the reordered file | 1. File accepted — system maps by column header name regardless of order 2. Data populates correctly in table |

**Test Data:** File: missing_accountid.csv (no Account ID); File: missing_profitloss.csv (no Profit/Loss); File: extra_columns.csv (all required + 'Notes', 'Custom1'); File: reordered_columns.csv (different column order)

---

#### TC-220261 · Statement Patch & Regeneration - Validation - Upload CSV - verify Account ID and Item must belong to selected tenant
**Priority:** High | **Automation:** Unset

**Description:** Verify that CSV containing Account ID(s) or Item (symbol) not belonging to the currently selected tenant is rejected

**Prerequisites:**
- Tenant A (tinshing) selected — has LIVE accounts: 710001, 710002, 710003

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Prepare CSV with Account ID = 999999 (does not exist in any tenant) | - |
| 2 | Click [Choose file] and select the file | 1. Snackbar error: 'File is not supported' 2. Table not populated |
| 3 | Prepare CSV with Account ID = 990001 (belongs to Tenant B, NOT Tenant A) | - |
| 4 | Click [Choose file] and select the file | 1. Snackbar error: 'File is not supported' 2. Table not populated [Account exists in system but does NOT belong to selected tenant] |
| 5 | Prepare CSV with Account ID = 710001 (valid, belongs to Tenant A) | - |
| 6 | Click [Choose file] and select the file | 1. File accepted 2. Data populates Statement Data Table |
| 7 | Prepare CSV with mixed Account IDs: 710001 (valid) + 999999 (invalid) | - |
| 8 | Click [Choose file] and select the mixed file | 1. Snackbar error: 'File is not supported' 2. Entire file rejected (not partial import) |
| 9 | Prepare CSV with Item = 'XYZINVALID' (symbol does not exist / does not belong to tenant), valid Account ID | - |
| 10 | Click [Choose file] and select file | 1. Snackbar error: 'File is not supported' 2. Statement Data Table not populated [Item must be valid symbol configured for selected tenant] |
| 11 | Prepare CSV with Item = 'XAUUSD' (valid, belongs to tenant tinshing) | - |
| 12 | Click [Choose file] and select file | 1. File accepted 2. Data populates correctly in Statement Data Table 3. Item column displays 'XAUUSD' |

**Test Data:** File: nonexistent_account.csv (Account ID 999999); File: wrong_tenant_account.csv (Account ID 990001, Tenant B); File: correct_account.csv (Account ID 710001); File: mixed_accounts.csv (710001 + 999999); File: invalid_item.csv (Account 710001, Item XYZINVALID); File: valid_item.csv (Account 710001, Item XAUUSD)

---

#### TC-220262 · Statement Patch & Regeneration - Validation - Upload CSV - verify Open Position Item must belong to selected tenant
**Priority:** High | **Automation:** Unset

**Description:** Verify that CSV for Open Position containing Item (symbol) not belonging to the selected tenant is rejected

**Prerequisites:**
- Tenant selected (tinshing) — has symbols: XAUUSD, XAGUSD
- Statement Table = Open Position (Daily)

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Prepare Open Position CSV with Item = 'XYZINVALID' (symbol does not exist / does not belong to tenant), valid Account ID | - |
| 2 | Click [Choose file] and select file | 1. Snackbar error: 'File is not supported' 2. Statement Data Table not populated [Item must be valid symbol configured for selected tenant] |
| 3 | Prepare Open Position CSV with Item = 'XAUUSD' (valid, belongs to tenant) | - |
| 4 | Click [Choose file] and select file | 1. File accepted 2. Data populates correctly in Statement Data Table 3. Item column displays 'XAUUSD' |
| 5 | Switch Statement Type to Monthly, prepare CSV with invalid Item | - |
| 6 | Click [Choose file] and select file | 1. Snackbar error: 'File is not supported' 2. Table not populated [Same validation applies for Monthly Statement Type] |
| 7 | Prepare CSV with valid Item for Monthly | - |
| 8 | Click [Choose file] and select file | 1. File accepted 2. Data populates correctly [Confirms: Open Position Item validation works for both Daily and Monthly Statement Types] |

**Test Data:** File: invalid_item_op.csv (Account 710001, Item XYZINVALID); File: valid_item_op.csv (Account 710001, Item XAUUSD); Statement Type: Monthly, File: invalid_item_op_monthly.csv (Item BTCUSD); File: valid_item_op_monthly.csv (Item XAGUSD)

---

#### TC-220263 · Statement Patch & Regeneration - Validation - Upload CSV - verify Symbol must belong to selected tenant
**Priority:** High | **Automation:** Unset

**Description:** Verify that CSV containing Symbol not belonging to the selected tenant is rejected (applicable for Interest Rate and other tables with Symbol column)

**Prerequisites:**
- Tenant A (tinshing) selected — has symbols: XAUUSD, XAGUSD
- Statement Table = Interest Rate

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Prepare Interest Rate CSV with Symbol = 'XAUUSD' (valid for tenant) | - |
| 2 | Click [Choose file] and select the file | 1. File accepted 2. Data populates table with Symbol = XAUUSD |
| 3 | Prepare Interest Rate CSV with Symbol = 'BTCUSD' (not configured for this tenant) | - |
| 4 | Click [Choose file] and select the file | 1. Snackbar error: 'File is not supported' 2. Table not populated |

**Test Data:** File: valid_symbol.csv (Symbol XAUUSD); File: invalid_symbol.csv (Symbol BTCUSD)

---

#### TC-220264 · Statement Patch & Regeneration - Validation - Upload CSV - verify corrupted/binary file renamed to .csv is rejected
**Priority:** High | **Automation:** Unset

**Description:** Verify that a non-text file (e.g. PNG, PDF) renamed with .csv extension is rejected during validation

**Prerequisites:**
- Tenant selected
- Statement Table = Settled Position

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Take a PNG image file and rename extension to .csv (e.g. image.png → image.csv) | - |
| 2 | Click [Choose file] and select the corrupted .csv file | 1. Snackbar error: 'File is not supported' 2. Table not populated [System should detect file content is not valid CSV format despite .csv extension] |

**Test Data:** File: image.csv (actually a PNG binary)

---

#### TC-220265 · Statement Patch & Regeneration - Validation - Upload CSV - verify wrong template columns rejected (mismatched Statement Table)
**Priority:** High | **Automation:** Unset

**Description:** Verify that CSV using columns from a different Statement Table type than the one currently selected is rejected

**Prerequisites:**
- Tenant selected
- Statement Table = Open Position (Daily) selected

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Prepare CSV using Settled Position template columns (Account ID, Date, Item, Open Ref, Open Date, Open Price, Close Ref, Close Date, Close Lot(s), Close Price, Interest, Commission, Profit/Loss, IsDeleted) | - |
| 2 | Click [Choose file] and select this mismatched CSV | 1. Snackbar error: 'File is not supported' 2. Table not populated [System detects columns don't match expected Open Position schema] |
| 3 | Prepare CSV using correct Open Position (Daily) columns | - |
| 4 | Click [Choose file] and select the correct template CSV | 1. File accepted 2. Data populates table correctly |

**Test Data:** File: settled_template_for_open.csv (Settled Position columns); File: correct_open_position.csv (correct Open Position columns)

---
#### TC-220266 · Statement Patch & Regeneration - Integration - Upload CSV - verify auto-populate Statement Data Table on successful upload
**Priority:** High | **Automation:** Unset

**Description:** Verify that once CSV passes all validations, system automatically retrieves data from the file and displays it in the Statement Data Table

**Prerequisites:**
- Tenant selected
- Statement Table = Settled Position
- Valid CSV file with 5 data rows prepared

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Click [Choose file] and select valid Settled Position CSV with 5 records | - |
| 2 | Observe Statement Data Table immediately after file selection | 1. Table auto-populates with 5 data rows from CSV 2. Each column maps correctly: Account ID matches CSV, Item matches CSV, Open Ref/Open Date/Open Price etc. all populated 3. Actions column shows Edit (pencil icon) and Delete (trash icon) for each row 4. 'No items available' message disappears 5. [Export data] button becomes enabled 6. [Patch] button becomes enabled (table now has data) |

**Test Data:** File: settled_5records.csv (5 rows with valid Account ID, Item, dates, numeric values)

---

#### TC-220267 · Statement Patch & Regeneration - State - Upload CSV - verify uploading new CSV replaces existing table data
**Priority:** High | **Automation:** Unset

**Description:** Verify that if Statement Data Table already contains data (from previous query or upload), uploading a new CSV replaces ALL existing table data with the new CSV content

**Prerequisites:**
- Tenant selected
- Statement Table = Settled Position
- Table currently shows 3 rows from previous Search query
- New CSV file with 5 different rows prepared

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe current Statement Data Table: 3 rows from previous query | - |
| 2 | Click [Choose file] and select new CSV with 5 different records | - |
| 3 | Observe Statement Data Table after upload | 1. Table now shows 5 rows (from new CSV) 2. Previous 3 rows (ORD001, ORD002, ORD003) are completely gone 3. New rows (ORD010-ORD014) displayed 4. Data is REPLACED, not appended |

**Test Data:** Current: 3 rows (ORD001, ORD002, ORD003); File: new_5records.csv (ORD010, ORD011, ORD012, ORD013, ORD014)

---

#### TC-220268 · Statement Patch & Regeneration - State - Upload CSV - verify uploaded data is working table only, DB not updated until Patch
**Priority:** High | **Automation:** Unset

**Description:** Verify that uploading CSV only populates the working table for editing; database is NOT updated until user explicitly clicks [Patch]

**Prerequisites:**
- Tenant selected
- Statement Table = Settled Position
- Valid CSV uploaded with new records (ORD-NEW1, ORD-NEW2)

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Upload valid CSV with new records not currently in DB | - |
| 2 | Observe Statement Data Table shows uploaded records | 1. Table shows ORD-NEW1 and ORD-NEW2 |
| 3 | Open a new browser tab, navigate to same page, same tenant, query the same account/date range via [Search] | 1. In new tab: queried data does NOT contain ORD-NEW1, ORD-NEW2 2. Confirms DB has not been updated yet [Upload only affects working table in current session, not DB] |
| 4 | Return to original tab and click [Patch] | 1. Data submitted to BE 2. DB now updated with ORD-NEW1, ORD-NEW2 |
| 5 | In second tab, click [Search] again | 1. Queried data now includes ORD-NEW1, ORD-NEW2 2. Confirms DB was only updated after Patch |

**Test Data:** File: new_records.csv (ORD-NEW1, ORD-NEW2)

---

#### TC-220269 · Statement Patch & Regeneration - Form - Upload CSV - verify user can Edit and Delete uploaded records before Patch
**Priority:** High | **Automation:** Unset

**Description:** Verify that after CSV uploads into working table, user can Edit row values and Delete rows before clicking Patch (changes are to working table only)

**Prerequisites:**
- Valid CSV uploaded into Statement Data Table
- Table shows 3 rows
- User has full privileges

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe Actions column for each row in table | 1. Each row has: Edit icon (pencil) — clickable, Delete icon (trash) — clickable |
| 2 | Click Edit icon on row 1 (ORD001) | 1. Row enters edit mode 2. Editable fields become input fields (per Statement Table edit rules) 3. Non-editable fields remain read-only (greyed out) |
| 3 | Modify an editable field value (e.g. Change Profit/Loss from 500.00 to 750.00) | 1. Field accepts new value: 750.00 2. Change visible in table cell |
| 4 | Save/confirm the edit (click checkmark or press Enter) | 1. Row exits edit mode 2. Updated value (750.00) persists in table 3. This is working table change only — not yet in DB |
| 5 | Click Delete icon on row 2 (ORD002) | 1. Confirmation modal appears: Message asking to confirm deletion, [Confirm] and [Cancel] buttons |
| 6 | Click [Confirm] in deletion modal | 1. Row 2 (ORD002) removed from table 2. Table now shows 2 rows (row 1 edited + row 3 unchanged) 3. No snackbar required after successful removal 4. Working table updated but DB unchanged |
| 7 | Click [Cancel] in deletion modal (test cancellation) | 1. Modal closes 2. Row remains in table (not deleted) 3. No changes made |

**Test Data:** Profit/Loss: 500.00 → 750.00

---

#### TC-220270 · Statement Patch & Regeneration - Validation - Upload CSV - verify FE validates date format in CSV (Date columns must be valid yyyy-mm-dd)
**Priority:** High | **Automation:** Unset

**Description:** Verify that CSV with invalid date format in date columns is rejected

**Prerequisites:**
- Tenant selected
- Statement Table = Settled Position (has Date, Open Date, Close Date columns)

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Prepare CSV with invalid Open Date format (e.g. '24-06-2026' instead of '2026-06-24') | - |
| 2 | Click [Choose file] and select the file | 1. Snackbar error: "Open Date must be in yyyy-mm-dd format." |
| 3 | Prepare CSV with Open Date = 'invalid-text' | - |
| 4 | Click [Choose file] and select the file | 1. Snackbar error: "Open Date must be in yyyy-mm-dd format." 2. Non-date text in date column must be rejected |
| 5 | Prepare CSV with valid date: Date = '2026-06-24' | - |
| 6 | Click [Choose file] and select the valid file | 1. File accepted 2. Date displays correctly in table |
| 7 | Prepare CSV with valid date: Open Date = '2026-06-24' | - |
| 8 | Click [Choose file] and select the valid file | 1. File accepted 2. Date displays correctly in table |
| 9 | Prepare CSV with Close Date = '--' (allowed per Settled Position validation: 'Close Date = valid yyyy-mm-dd or --') | - |
| 10 | Click [Choose file] and select the file | 1. File accepted 2. Close Date column shows '--' in table [Per requirement: Settled Position Close Date accepts '--' as valid value] |

**Test Data:** File: invalid_date_format.csv (Open Date 24-06-2026, dd-mm-yyyy); File: text_in_date.csv (Open Date 'abc-def-ghij'); File: valid_date.csv (Open Date 2026-06-24); File: dash_closedate.csv (Close Date '--')

---

#### TC-220271 · Statement Patch & Regeneration - Validation - Upload CSV - verify FE validates numeric fields reject negative where not allowed
**Priority:** High | **Automation:** Unset

**Description:** Verify that numeric columns that disallow negative values (Open Price, Close Lot(s), Close Price for Settled Position) reject negative numbers in CSV

**Prerequisites:**
- Tenant selected
- Statement Table = Settled Position
- Validation rule: Open Price, Close Lot(s), Close Price: 'negative not allowed'

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Prepare CSV with Open Price = -100.50 (negative) | - |
| 2 | Click [Choose file] and select the file | 1. Snackbar error: "File contains invalid data." |
| 3 | Prepare CSV with Interest = -5.50 (negative ALLOWED for Interest per requirement) | - |
| 4 | Click [Choose file] and select the file | 1. File accepted 2. Interest column shows -5.50 in table [Per requirement: Interest, Commission, Profit/Loss allow negative values] |
| 5 | Prepare CSV with numeric field containing alphabet characters (e.g. Open Price = 'abc') | - |
| 6 | Click [Choose file] and select the file | 1. Snackbar error: 'File contains invalid data.' [Alphabet characters in numeric columns must be rejected] |

**Test Data:** File: negative_price.csv (Open Price -100.50); File: negative_interest.csv (Interest -5.50); File: alpha_in_numeric.csv (Open Price 'abc')

---

#### TC-220272 · Statement Patch & Regeneration - Validation - Upload CSV - verify Deposit/Withdrawal Type column only accepts DEPOSIT, WITHDRAWAL, CREDIT, OTHERS
**Priority:** High | **Automation:** Unset

**Description:** Verify that CSV for Deposit/Withdrawal table with invalid Type value is rejected; only DEPOSIT, WITHDRAWAL, CREDIT, OTHERS are valid

**Prerequisites:**
- Tenant selected
- Statement Table = Deposit/Withdrawal

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Prepare CSV with Type = 'DEPOSIT' (valid) | - |
| 2 | Click [Choose file] and select the file | 1. File accepted 2. Type column shows 'DEPOSIT' in table |
| 3 | Prepare CSV with Type = 'TRANSFER' (invalid — not in allowed list) | - |
| 4 | Click [Choose file] and select the file | 1. Snackbar error: 'File contains invalid data.' [Only DEPOSIT, WITHDRAWAL, CREDIT, OTHERS are valid] |
| 5 | Prepare CSV with Type = 'deposit' (lowercase) | - |
| 6 | Click [Choose file] and select the file | 1. File accepted (case-insensitive match) |
| 7 | Prepare CSV with Type = '' (empty) | - |
| 8 | Click [Choose file] and select the file | 1. Snackbar error: 'File contains invalid data.' [Type is a required field — cannot be empty] |

**Test Data:** File: valid_type.csv (Type DEPOSIT); File: invalid_type.csv (Type TRANSFER); File: lowercase_type.csv (Type deposit); File: empty_type.csv (Type empty)

---

#### TC-220273 · Statement Patch & Regeneration - Validation - Upload CSV - verify Open Position numeric fields validation (Average Price, Closing Price, Net Volume)
**Priority:** High | **Automation:** Unset

**Description:** Verify CSV validation for Open Position numeric fields: Average Price and Closing Price reject negative; Net Volume allows negative

**Prerequisites:**
- Tenant selected
- Statement Table = Open Position (Daily)

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Prepare CSV with Average Price = '-1800.50' (negative) | - |
| 2 | Upload file | 1. Snackbar error: 'File contains invalid data.' [Average Price does not allow negative values] |
| 3 | Prepare CSV with Closing Price = '-1750.00' (negative) | - |
| 4 | Upload file | 1. Snackbar error: 'File contains invalid data.' [Closing Price does not allow negative values] |
| 5 | Prepare CSV with Net Volume = '-5.00' (negative, allowed) | - |
| 6 | Upload file | 1. File accepted 2. Net Volume displays '-5.00' in table [Net Volume allows negative values — SELL direction] |
| 7 | Prepare CSV with Average Price = '1800.50' and Closing Price = '1750.00' (valid) | - |
| 8 | Upload file | 1. File accepted 2. Data populates correctly: Average Price 1,800.50, Closing Price 1,750.00 [Confirms CSV validation parity with Edit validation for Open Position numeric fields] |

**Test Data:** File: negative_avgprice.csv (Average Price -1800.50); File: negative_closeprice.csv (Closing Price -1750.00); File: negative_netvolume.csv (Net Volume -5.00); File: valid_prices.csv (Average Price 1800.50, Closing Price 1750.00)

---

#### TC-220274 · Statement Patch & Regeneration - Validation - Upload CSV - verify Open Position Commission empty defaults to '--'
**Priority:** High | **Automation:** Unset

**Description:** Verify that CSV for Open Position with Commission field empty defaults to '--' in table display

**Prerequisites:**
- Tenant selected
- Statement Table = Open Position (Daily)

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Prepare CSV with Commission = '' (empty) | - |
| 2 | Click [Choose file] and select the file | 1. File accepted 2. Commission shows '--' in table [Per requirement: Commission defaults to '--' if empty] |
| 3 | Prepare CSV with Commission = '-2.50' (valid negative numeric) | - |
| 4 | Click [Choose file] and select the file | 1. File accepted 2. Commission shows '-2.50' in table [Commission allows negative values] |

**Test Data:** File: empty_commission.csv (Commission empty); File: negative_commission.csv (Commission -2.50)

---

#### TC-220275 · Statement Patch & Regeneration - Validation - Upload CSV - verify Interest Rate: Sell Rate and Buy Rate accept numeric including negative, FE displays '%'
**Priority:** High | **Automation:** Unset

**Description:** Verify that Interest Rate CSV: Sell Rate and Buy Rate are stored as numeric in CSV but displayed with '%' in FE table

**Prerequisites:**
- Tenant selected
- Statement Table = Interest Rate

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Prepare CSV with Sell Rate = 0.05, Buy Rate = -0.03 | - |
| 2 | Click [Choose file] and select the file | 1. File accepted 2. Table displays: Sell Rate '0.05%' (with % symbol), Buy Rate '-0.03%' (with % symbol) 3. CSV stores numeric value only; FE appends '%' for display |
| 3 | Prepare CSV with Sell Rate = 'abc' (non-numeric) | - |
| 4 | Click [Choose file] and select the file | 1. Snackbar error: 'File is not supported' [Sell Rate / Buy Rate must be numeric] |

**Test Data:** File: interest_rates.csv (Sell Rate 0.05, Buy Rate -0.03); File: invalid_rate.csv (Sell Rate abc)

---

#### TC-220276 · Statement Patch & Regeneration - Validation - Upload CSV - Statement Summary - verify positive-only vs allow-negative fields in CSV template
**Priority:** High | **Automation:** Unset

**Description:** Verify CSV validation for Statement Summary editable fields

**Prerequisites:**
- Tenant selected
- Statement Table = Statement Summary
- Statement Type = Daily or Monthly

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Prepare CSV with Equity = -2000 (negative) | 1. Snackbar error: 'File is not supported' [Equity: positive only — negative not allowed] |
| 2 | Prepare CSV with Call Margin = -300 (negative) | 1. Snackbar error: 'File is not supported' [Call Margin: positive only — negative not allowed] |
| 3 | Prepare CSV with New Balance = -1000 (negative) | 1. File accepted 2. New Balance shows '-1,000.00' in table [New Balance: allows negative values] |
| 4 | Prepare CSV with Currency = USD (TBC w PM) | 1. File accepted |

**Test Data:** File: negative_equity.csv (Equity -2000); File: negative_call_margin.csv (Call Margin -300); File: negative_new_balance.csv (New Balance -1000)

---

#### TC-220277 · Statement Patch & Regeneration - Display - Preview PDF - Statement Summary - verify BE-calculated fields display negative values correctly
**Priority:** High | **Automation:** Unset

**Description:** Verify that BE-calculated fields in Statement Summary section of Preview PDF can display negative values correctly

**Prerequisites:**
- Tenant selected
- Account has statement data with: negative P/L from Settled Position, negative Floating P/L from Open Position, negative Commission values

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Query or Patch data that results in negative calculated values for Statement Summary | 1. Patch completes successfully |
| 2 | Click [Preview Statement] for the patched account/date | 1. Preview PDF opens 2. STATEMENT SUMMARY section displays: Margin In (positive, ≥0), Margin Out (positive, ≥0), Margin Requirement (positive, ≥0), Profit/Loss (negative if calculated negative, e.g. '-350.50'), Adjustment (negative if applicable), Floating P/L (negative if Open Position has loss), Unrealised Interest (negative if applicable), Realised Interest (negative if applicable), Commission (negative if applicable) [Confirms: BE-calculated negative values display correctly in PDF] |
| 3 | Verify negative values format in PDF | 1. Negative values show with minus sign: '-1,000.00' 2. Format consistent with positive values (same decimal places) 3. No display corruption or missing minus signs |

**Test Data:** None

---

#### TC-220278 · Statement Patch & Regeneration - Validation - Upload CSV - verify IsDeleted column accepts TRUE/FALSE values
**Priority:** High | **Automation:** Unset

**Description:** Verify that CSV upload validates IsDeleted column: accepts TRUE/FALSE (case-insensitive), handles empty values, rejects invalid values

**Prerequisites:**
- Tenant selected
- Statement Table = Settled Position
- Multiple CSV files prepared with different IsDeleted values

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Prepare CSV with IsDeleted = 'TRUE' (uppercase) | 1. File accepted 2. Data loads into table |
| 2 | Prepare CSV with IsDeleted = 'FALSE' (uppercase) | 1. File accepted 2. Data loads into table |
| 3 | Prepare CSV with IsDeleted = 'true' (lowercase) | 1. File accepted (case-insensitive) 2. Data loads into table |
| 4 | Prepare CSV with IsDeleted = '' (empty/blank) | 1. Verify behavior: if accepted, defaults to FALSE (row kept); if rejected, snackbar error message [Document actual behavior] |
| 5 | Prepare CSV with IsDeleted = 'yes' (invalid value) | 1. File REJECTED with validation error 2. Snackbar shows error: invalid IsDeleted value [Only TRUE/FALSE accepted] |
| 6 | Prepare CSV with IsDeleted = '1' (numeric instead of boolean) | 1. Verify behavior: if accepted, '1' treated as TRUE; if rejected, validation error [Document actual behavior] |
| 7 | Prepare CSV with mixed IsDeleted values in same file (Row 1 TRUE, Row 2 FALSE, Row 3 TRUE) | 1. File accepted 2. All 3 rows load into table 3. After Patch: Row 1 and Row 3 deleted, Row 2 kept |
| 8 | Upload the file | 1. File accepted 2. Monthly Profit/Loss shows '-800.00' [Monthly Profit/Loss allows negative] |

**Test Data:** File: isdeleted_true.csv; File: isdeleted_false.csv; File: isdeleted_lowercase.csv; File: isdeleted_empty.csv; File: isdeleted_invalid_yes.csv; File: isdeleted_numeric.csv; File: isdeleted_mixed.csv

---

#### TC-220279 · Statement Patch & Regeneration - Validation - Upload CSV - verify comma inside numeric value causes parse error
**Priority:** High | **Automation:** Unset

**Description:** Verify CSV with comma in numeric (e.g. '1,000') is rejected or corrupts data since comma is CSV delimiter; only raw numbers accepted

**Prerequisites:**
- Tenant selected
- Statement Table = Settled Position

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Prepare CSV with comma in numeric: Open Price = '1,000' | - |
| 2 | Upload the file | 1. Snackbar: 'File is not supported' (column count mismatch) |
| 3 | Prepare CSV with raw number: Open Price = '1000' (no comma) | - |
| 4 | Upload the raw number file | 1. File accepted 2. Table displays '1,000.00' (FE auto-formats with thousand separator) 3. Columns correctly mapped |
| 5 | Prepare CSV with decimal value: Open Price = '1.00' | - |
| 6 | Upload the decimal file | 1. File accepted 2. Table displays '1.00' (decimal preserved) 3. No thousand separator needed for values < 1,000 |

**Test Data:** File: comma_in_number.csv; File: raw_number.csv (Open Price 1000); File: decimal.csv (Open Price 1.00)

---

#### TC-220280 · Statement Patch & Regeneration - Form - Query Daily - verify mandatory filters and Search button enablement
**Priority:** High | **Automation:** Unset

**Description:** Verify that Daily query requires Account ID + Start Datetime + End Datetime; Search button only enables when all 3 are filled

**Prerequisites:**
- Tenant selected
- Statement Table = any (e.g. Executed Orders)
- Statement Type = Daily

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe query filter area with all fields empty | 1. Fields displayed: Account ID * (dropdown, placeholder 'Select Account ID'), Start Datetime (UTC) * (format: yyyy-mm-dd hh:mm:ss), End Datetime (UTC) * (format: yyyy-mm-dd hh:mm:ss) 2. [Search] button: disabled 3. [Export data] button: disabled |
| 2 | Select Account ID only (leave datetime fields empty) | 1. [Search] button: still disabled (not all mandatory filled) |
| 3 | Fill Start Datetime only (Account ID + Start filled, End empty) | 1. [Search] button: still disabled |
| 4 | Fill End Datetime (all 3 mandatory fields now filled) | 1. [Search] button: ENABLED 2. [Export data] button: still disabled (table still empty) |
| 5 | Clear Account ID (remove selection) | 1. [Search] button: disabled again (mandatory field missing) |
| 6 | Select invalid Start Datetime & End Datetime: End Time before Start Datetime | 1. [Search] button: disable - show error message |
| 7 | Update valid Start Datetime & End Datetime | 1. [Search] button: enable |

**Test Data:** Account ID: 710001; Start: 2026-08-15 22:00:00; End: 2026-08-16 21:00:00; (invalid: Start 2026-08-16 21:00 / End 2026-08-15 22:00)

---
#### TC-220281 · Statement Patch & Regeneration - Validation - Daily date range - verify End Datetime must not exceed 1 day from Start Datetime
**Priority:** High | **Automation:** Unset

**Description:** Verify that when Statement Type = Daily, selecting End Datetime more than 1 day from Start Datetime shows validation error and disables Search button

**Prerequisites:**
- Tenant selected
- Statement Type = Daily
- Account ID filled

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Fill Start Datetime = 2026-08-25 17:00:00 | 1. Start Datetime field shows: 2026-08-25 17:00:00 |
| 2 | Fill End Datetime = 2026-08-27 00:00:00 (more than 1 day from Start) | 1. End Datetime field highlighted in RED (error state) 2. Error message displays below field: 'End Datetime must not exceed 1 day from Start Datetime.' 3. [Search] button: DISABLED 4. [Export] button: DISABLED |
| 3 | Change End Datetime to 2026-08-26 17:00:00 (exactly 1 day) | 1. Error message disappears 2. End Datetime field returns to normal state (no red highlight) 3. [Search] button: ENABLED |
| 4 | Change End Datetime to 2026-08-26 16:59:59 (less than 1 day) | 1. No error message 2. [Search] button: ENABLED [Confirms: boundary validation - exactly 1 day is allowed, more than 1 day is rejected] |
| 5 | Switch Statement Type to 'Monthly', observe date range validation | 1. Date range validation no longer applies (Monthly uses month picker instead) 2. No '1 day' restriction for Monthly [Daily-specific validation only] |

**Test Data:** Start: 2026-08-25 17:00:00; End: 2026-08-27 00:00:00 / 2026-08-26 17:00:00 / 2026-08-26 16:59:59

---

#### TC-220282 · Statement Patch & Regeneration - Form - Query Monthly - verify mandatory filters and Search button enablement
**Priority:** High | **Automation:** Unset

**Description:** Verify that Monthly query requires Account ID + Select Month; Search button only enables when both are filled

**Prerequisites:**
- Tenant selected
- Statement Type = Monthly

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Switch Statement Type to 'Monthly' | 1. Query filter area changes: Account ID * (dropdown), Select Month * (month picker) 2. Start/End Datetime fields disappear 3. [Search] button: disabled |
| 2 | Select Account ID only | 1. [Search] button: still disabled (month not selected) |
| 3 | Select month (e.g. July 2026) | 1. [Search] button: ENABLED |
| 4 | Clear the Select Month field (remove month selection) | 1. [Search] button becomes disabled again (mandatory field missing) |
| 5 | Clear Account ID selection (with month still selected) | 1. [Search] button disabled (both fields must be filled) |
| 6 | Click [Search] with valid Account ID and Month selection | 1. Statement Data Table populates with Monthly data 2. [Export Data] button: ENABLED [Monthly: Export Data enabled when table has data] |
| 7 | Delete all rows in the table (or clear table data) | 1. Statement Data Table becomes empty 2. [Export Data] button: DISABLED [Monthly: Export Data disabled when no data to export] |

**Test Data:** Account ID: 710001; Month: July 2026

---

#### TC-220283 · Statement Patch & Regeneration - Form - Account ID dropdown - verify LIVE only, search function, sorted ascending, single selection
**Priority:** High | **Automation:** Unset

**Description:** Verify Account ID dropdown: shows LIVE accounts only, has search function, sorted numerically ascending, single selection

**Prerequisites:**
- Tenant selected (tinshing)
- Tenant has LIVE accounts: 710001, 710002, 710003, 710010
- Tenant has DEMO accounts: 810001, 810002

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Click Account ID dropdown | 1. Dropdown opens 2. Search input field available at top of dropdown |
| 2 | Observe listed accounts | 1. Only LIVE accounts listed: 710001, 710002, 710003, 710010 2. DEMO accounts (810001, 810002) NOT present 3. Sorted numerically ascending |
| 3 | Type '710' in search input | 1. Filtered results show only accounts containing '710' 2. Non-matching accounts hidden |
| 4 | Type '810' in search input | 1. No results (DEMO accounts excluded) |
| 5 | Select account 710001 | 1. Dropdown closes 2. Field shows '710001' 3. Only 1 account selected (single selection — no multi-select) |

**Test Data:** Search: 710; Search: 810

---

#### TC-220284 · Statement Patch & Regeneration - Integration - Search button - verify queries DB data and populates table
**Priority:** High | **Automation:** Unset

**Description:** Verify clicking Search retrieves existing data from BE (consolidated from Centroid API/DB) and populates Statement Data Table

**Prerequisites:**
- Tenant selected
- Statement Table = Executed Orders, Statement Type = Daily
- All query filters filled
- Account has existing Executed Orders data in DB for the date range

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Fill all filters: Account ID = 710001, Start = 2026-08-15 22:00:00, End = 2026-08-16 21:00:00 | - |
| 2 | Click [Search] | 1. Loading indicator shown while fetching 2. Statement Data Table populates with data rows from BE 3. Columns match Executed Orders schema: Account ID, Item, Order Date, Order Time, Order Ref, Bought Lot(s), Sold Lot(s), New/Liq., Exchange Rate, Executed Price, Action 4. Data reflects BE consolidated result for the queried account/period 5. [Export data] button becomes ENABLED 6. 'No items available' message disappears 7. Exchange Rate: USD symbol shows 1, non-USD shows +ve values 5dp round up, rejected orders show -- |
| 3 | Observe Actions column | 1. Each row has Edit (pencil) and Delete (trash) icons in Actions column [Note: For Executed Orders, edit rules apply per validation table] |

**Test Data:** Account: 710001; Start: 2026-08-15 22:00:00; End: 2026-08-16 21:00:00

---

#### TC-220285 · Statement Patch & Regeneration - Integration - Search - verify query returns data for all Statement Table types (excluding Executed Orders)
**Priority:** High | **Automation:** Unset

**Description:** Verify Search retrieves data from BE for all Statement Tables: Settled Position, Open Position (Daily/Monthly), Deposit/Withdrawal, Statement Summary (Daily/Monthly)

**Prerequisites:**
- Tenant selected (tinshing)
- Account 710001 has existing data in DB for all Statement Table types
- User has full privileges

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Select Statement Table = 'Settled Position', Statement Type = 'Daily/Monthly', fill Account ID and date range, click [Search] | 1. Table populates with Settled Position data 2. Columns match: Account ID, Date, Item, Open Ref, Open Date, Open Price, Close Ref, Close Date, Close Lot(s), Close Price, Exchange Rate, Interest, Commission, Profit/Loss, Actions 3. Exchange Rate: USD shows 1, non-USD shows +ve values 5dp round up, rejected shows -- [Data source: Database backup] |
| 2 | Select Statement Table = 'Open Position', Statement Type = 'Daily/Monthly', fill filters, click [Search] | 1. Table populates with Open Position Daily data 2. Columns include 'Daily Interest' column 3. Columns match: Account ID, Date, Order Ref, Item, Net Volume, Average Price, Closing Price, Exchange Rate, Unrealised Interest, Daily Interest, Commission, Floating Profit/Loss, PL Conv Rate, Notional, Actions 4. Exchange Rate same rule as above |
| 3 | Select Statement Table = 'Deposit/Withdrawal', Statement Type = 'Daily/Monthly', fill filters, click [Search] | 1. Table populates with Deposit/Withdrawal data 2. Columns match: Account ID, Date, Order Ref, Description, Type, Amount, Actions |
| 4 | Select Statement Table = 'Statement Summary', Statement Type = 'Daily/Monthly', fill filters, click [Search] | 1. Table populates with Statement Summary Daily data 2. Columns include: Account ID, Date, Margin In, Monthly Profit/Loss, Margin Out, New Balance, Adjustment, Floating Profit/Loss, Unrealised Interest, Equity, Realised Interest, Margin Requirement, Commission, Call Margin, Credit, Actions |
| 5 | Select Statement Table = 'Interest Rate', fill filters, click [Search] | 1. Table populates with Interest Rate data 2. Columns match: Account ID, Date, Taker Feed, Limit Symbol Group, Symbol, Sell Rate, Buy Rate, Actions 3. Sell Rate and Buy Rate display with '%' suffix |
| 6 | For each table above, verify [Export data] button enables after Search | 1. [Export data] button: ENABLED for all tables after successful Search 2. Exported CSV contains queried data |
| 7 | For each table above, verify Edit and Delete icons appear in Actions column | 1. Each row has Edit (pencil) and Delete (trash) icons 2. Icons are clickable [Confirms: Search functionality works consistently across all Statement Tables, regardless of data source] |

**Test Data:** Account: 710001; Start: 2026-08-15 22:00:00; End: 2026-08-16 21:00:00

---

#### TC-220286 · Statement Patch & Regeneration - Integration - Search - verify querying again replaces existing table data
**Priority:** High | **Automation:** Unset

**Description:** Verify that performing a second Search (same or different filters) replaces the current table data entirely

**Prerequisites:**
- Table currently shows data from previous query (Account 710001, 3 rows)
- User changes filters

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Change Account ID to 710002 (different account) | - |
| 2 | Click [Search] | 1. Previous data (710001, 3 rows) completely replaced 2. Table now shows data for 710002 3. No data from 710001 remains |
| 3 | Change date range and click [Search] again with same account | 1. Table data replaced with new query result for updated date range |

**Test Data:** Account: 710002; Start: 2026-07-15 22:00:00; End: 2026-07-16 21:00:00

---

#### TC-220287 · Statement Patch & Regeneration - State - Upload CSV disables query filters
**Priority:** High | **Automation:** Unset

**Description:** Verify that after uploading a valid CSV, the query filter fields (Account ID, Start/End Datetime or Month) become disabled

**Prerequisites:**
- Tenant selected
- Statement Table = Settled Position
- Query filters currently enabled
- Valid CSV file ready

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe query filters before upload: all enabled | 1. Account ID dropdown: enabled 2. Start/End Datetime fields: enabled 3. [Search] button: state depends on filter completeness |
| 2 | Upload valid CSV via [Choose file] | 1. CSV data loads into Statement Data Table 2. Query filters become DISABLED: Account ID dropdown disabled/greyed out, Start Datetime disabled, End Datetime disabled, [Search] button disabled 3. [Export data] button: disabled (req: All query filters, Search button and Export Data button shall be disabled when a csv file is uploaded) |

**Test Data:** File: settled_position_patch.csv

---

#### TC-220288 · Statement Patch & Regeneration - State - Upload CSV multi-account - verify table shows all accounts and query filter disabled
**Priority:** High | **Automation:** Unset

**Description:** Verify that after uploading CSV with multiple Account IDs, table displays ALL accounts from CSV (not filtered to 1), and Account ID query filter is disabled

**Prerequisites:**
- Tenant selected
- Statement Table = Settled Position
- CSV contains data for 3 accounts: 710001, 710002, 710003 (2 rows each = 6 total rows)

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Upload CSV with 3 different Account IDs (6 rows total) | - |
| 2 | Observe Statement Data Table | 1. Table shows ALL 6 rows 2. Rows contain mixed Account IDs: 710001, 710002, 710003 3. Table is NOT filtered to single account |
| 3 | Observe Account ID dropdown in query filter area | 1. Account ID dropdown: DISABLED (greyed out) 2. User cannot filter table by single account [Upload CSV = show all data as-is, no filtering] |
| 4 | Return to Query mode to compare (via the available reset action — e.g. change Statement Table then switch back, or re-select tenant), then select Account ID = 710001 and click [Search] | 1. Query filters re-enabled after reset 2. After Search: table shows ONLY rows for 710001 3. 710002 and 710003 rows NOT visible [Query = filtered to 1 account; Upload CSV = all accounts shown] |

**Test Data:** File: multi_account.csv (Rows 1-2: 710001, Rows 3-4: 710002, Rows 5-6: 710003)

---

#### TC-220289 · Statement Patch & Regeneration - Toggle/Button - Export Data - verify export current table dataset as CSV
**Priority:** High | **Automation:** Unset

**Description:** Verify Export Data button: disabled when table empty, enabled when records exist, exports current displayed dataset as CSV

**Prerequisites:**
- Tenant selected
- Statement Table = Settled Position
- Table has data (from Query or Upload)

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe [Export data] button when table is empty (before query/upload) | 1. [Export data] button: DISABLED |
| 2 | Query or upload data to populate table (e.g. 5 rows) | 1. [Export data] button becomes ENABLED |
| 3 | Click [Export data] | 1. CSV file downloads to device 2. CSV contains the current dataset as displayed in table 3. Columns match Statement Data Table columns 4. Number of data rows matches table row count (5 rows) |
| 4 | Edit a row in table (change Profit/Loss from 500 to 750), then click [Export data] again | 1. Exported CSV contains the EDITED value (750), not original (500) [Export reflects working table state including edits] |
| 5 | Delete a row in table, then click [Export data] | 1. Exported CSV does NOT contain the deleted row [Export reflects current table state after deletion] |

**Test Data:** Edited: Profit/Loss 500 → 750

---

#### TC-220290 · Statement Patch & Regeneration - Display - Thousand separator in table - verify FE auto-formats numeric values with comma
**Priority:** High | **Automation:** Unset

**Description:** Verify that when CSV data or queried data loads into table, FE auto-displays numeric values with thousand separator (e.g. 1000 → 1,000.00); CSV/export retains raw number

**Prerequisites:**
- Tenant selected
- Statement Table = Settled Position
- CSV contains raw numeric: Open Price = 1000, Profit/Loss = 50000.5

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Upload CSV with raw numeric values (no commas in file) | - |
| 2 | Observe Statement Data Table display | 1. Open Price displays: '1,000.00' (thousand separator + decimal) 2. Profit/Loss displays: '50,000.50' 3. FE auto-applies thousand separator for display only |
| 3 | Click [Edit] on the row — observe field value in edit mode | 1. User can type raw number without comma 2. Showing the raw value in edit mode (e.g. 1000, not 1,000.00), then reformatting with comma/decimal display once the user exits edit mode |
| 4 | Click [Export data] — open exported CSV | 1. Exported CSV contains RAW numeric values: 1000, 50000.5 2. NO thousand separator (comma) in CSV file [Per comment 19/8: comma only for FE table display, not in CSV] |
| 5 | After Patch, download Patched Dataset CSV from Patch History | 1. Patched Dataset CSV also stores raw numbers (no comma) [Consistent: all CSV files = raw numeric; only UI table has formatting] |

**Test Data:** CSV contains: Open Price 1000, Profit/Loss 50000.5

---

#### TC-220291 · Statement Patch & Regeneration - Form - Edit Settled Position - verify editable vs non-editable fields
**Priority:** High | **Automation:** Unset

**Description:** Verify that for Settled Position table: Account ID, Item, Open Ref, Open Date, Close Ref, Close Date are NOT editable; other fields are editable

**Prerequisites:**
- Statement Table = Settled Position
- Table has data (from Query or Upload)
- User has full privileges

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Click Edit icon (pencil) on a Settled Position row | 1. Row enters edit mode 2. Non-editable fields (greyed out / read-only): Account ID, Item, Open Ref, Open Date, Close Ref, Close Date, Exchange Rate 3. Editable fields (become input fields): Open Price, Close Lot(s), Close Price, Interest, Commission, Profit/Loss, Date column enables date picker |
| 2 | Attempt to click/type in Account ID field | 1. Field does not respond to click/keyboard 2. No cursor appears 3. Value cannot be changed |
| 3 | Attempt to click/type in Open Price field | 1. Field becomes active / cursor appears 2. User can modify value |
| 4 | Type alphabet 'abc' into Open Price field (numeric column) | 1. Alphabet characters BLOCKED — field does not accept letters [Per requirement: Block user keyboard inserting alphabet data into numeric columns] |
| 5 | Type '1234.56' into Open Price field | 1. Value accepted (numeric with decimal allowed) |
| 6 | Type '-100' into field that does not allow negative (Open Price, Close Lot(s), Close Price) | 1. Value REJECTED — negative not allowed for Open Price |
| 7 | Type '-50.25' into field that allows negative (Interest, Commission, Profit/Loss all allow negative for Settled Position) | 1. All three values ACCEPTED |
| 8 | Click on a Date column (Open Date) while in edit mode | 1. Date picker appears (not free-text input) [Per requirement: Date Column shall enable date picker] |

**Test Data:** Input: 1234.56; Input: -100; Interest: -50.25; Commission: -2.50; Profit/Loss: -100.00

---

#### TC-220292 · Statement Patch & Regeneration - Form - Edit Executed Orders - verify editable vs non-editable fields
**Priority:** High | **Automation:** Unset

**Description:** Verify Executed Orders edit rules: Account ID, Item, Order Date, Order Time, Order Ref are non-editable; Bought Lot(s), Sold Lot(s), New/Liq., Executed Price are editable

**Prerequisites:**
- Statement Table = Executed Orders
- Table has data (from Query/Search)
- User has full privileges

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Click Edit icon on an Executed Orders row | 1. Non-editable fields (greyed out): Account ID, Item, Order Date, Order Time, Order Ref, Exchange Rate 2. Editable fields: Bought Lot(s), Sold Lot(s), New/Liq., Executed Price |
| 2 | Type 'abc' into Bought Lot(s) field (numeric column) | 1. Alphabet BLOCKED [Per requirement: Block alphabet in numeric columns] |
| 3 | Type '10.00' into Bought Lot(s) field | 1. Value accepted (numeric with decimal) |
| 4 | Type '-5.00' into Sold Lot(s) field | 1. Value REJECTED — Bought/Sold Lot(s) should not accept negative (lot quantity always positive; direction expressed by column Bought vs Sold) [Note: unlike Open Position Net Volume which allows negative for SELL direction, Executed Orders separates Buy/Sell into distinct columns] |
| 5 | Click on Order Date field (non-editable date column) | 1. Field does NOT respond 2. No date picker opens [Order Date is non-editable for Executed Orders] |

**Test Data:** Input: abc; Input: 10.00; Input: -5.00

---

#### TC-220293 · Statement Patch & Regeneration - Form - Edit Open Position (Daily) - verify editable vs non-editable fields
**Priority:** High | **Automation:** Unset

**Description:** Verify that for Open Position: Account ID, Date, Order Ref, Item are NOT editable; other numeric fields are editable with correct sign rules

**Prerequisites:**
- Statement Table = Open Position
- Table has data

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Click Edit icon on an Open Position row | 1. Non-editable fields: Account ID, Date, Order Ref, Item 2. Editable fields: Net Volume, Average Price, Closing Price, Unrealised Interest, Daily Interest, Commission, Floating Profit/Loss, Exchange Rate, Notional |
| 2 | Type '-5.00' into Net Volume (negative allowed) | 1. Value ACCEPTED [Net Volume allows negative per validation] |
| 3 | Type '-100' into Average Price (negative NOT allowed) | 1. Value REJECTED [Average Price, Closing Price: negative not allowed] |
| 4 | Type 'abc' into Closing Price | 1. Alphabet BLOCKED |
| 5 | Type '-2.50' into Commission, then clear it (leave empty) | 1. Commission accepts '-2.50' (negative allowed) 2. Commission empty → will default to '--' on Patch [Per validation: Commission and Storage both allow negative; Commission empty defaults to '--'; Storage removed 27 Aug] |
| 6 | Type '-10.50' into Unrealised Interest field (negative) | 1. Value ACCEPTED [Per validation: Unrealised Interest allows negative] |
| 7 | Type '-2.25' into Daily Interest field (negative) | 1. Value ACCEPTED [Per validation: Daily Interest allows negative] |
| 8 | Type '-500.00' into Floating Profit/Loss field (negative) | 1. Value ACCEPTED [Per validation: Floating Profit/Loss allows negative] |

**Test Data:** Input: -5.00; -100; abc; Commission: -2.50; -10.50; -2.25; -500.00

---

#### TC-220294 · Statement Patch & Regeneration - Form - Edit Deposit/Withdrawal - verify editable vs non-editable fields and Type validation
**Priority:** High | **Automation:** Unset

**Description:** Verify Deposit/Withdrawal edit rules: Account ID, Date, Order Ref are non-editable; Description, Type, Amount are editable; Type only accepts DEPOSIT/WITHDRAWAL/CREDIT/OTHERS

**Prerequisites:**
- Statement Table = Deposit/Withdrawal
- Table has data

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Click Edit icon on a Deposit/Withdrawal row | 1. Non-editable fields: Account ID, Date, Order Ref 2. Editable fields: Description (text/alphanumeric), Type, Amount (numeric) |
| 2 | Type 'Client bank transfer' into Description field | 1. Value ACCEPTED (text/alphanumeric allowed) |
| 3 | Change Type to 'CREDIT' | 1. Value ACCEPTED (valid option) |
| 4 | Change Type to 'TRANSFER' | 1. Value REJECTED — only DEPOSIT, WITHDRAWAL, CREDIT, OTHERS allowed |
| 5 | Type 'abc' into Amount field | 1. Alphabet BLOCKED (numeric column) |
| 6 | Type value into Amount field: positive number, then negative number | 1. Value ACCEPTED when inputting positive number, REJECTED when inputting negative number |
| 7 | Clear the Type field (leave empty) and attempt to save | 1. Value REJECTED / validation error [Type is required and only accepts DEPOSIT, WITHDRAWAL, CREDIT, OTHERS — empty not allowed] |
| 8 | Type 'deposit' (lowercase) into Type field | 1. Value ACCEPTED (case-insensitive match) 2. Field normalises to 'DEPOSIT' when user exits edit mode |

**Test Data:** Input: Client bank transfer; CREDIT; TRANSFER; abc; 5000.00; (empty); deposit

---

#### TC-220295 · Statement Patch & Regeneration - Form - Edit Interest Rate - verify non-editable fields and Sell/Buy Rate allow negative
**Priority:** High | **Automation:** Unset

**Description:** Verify Interest Rate edit rules: Account ID, Date, Taker Feed, Limit Symbol Group, Symbol are non-editable; Sell Rate, Buy Rate are editable and allow negative

**Prerequisites:**
- Statement Table = Interest Rate
- Table has data

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Click Edit icon on an Interest Rate row | 1. Non-editable fields: Account ID, Date, Taker Feed, Limit Symbol Group, Symbol 2. Editable fields: Sell Rate, Buy Rate |
| 2 | Type '-0.03' into Buy Rate | 1. Value ACCEPTED (negative allowed for Sell/Buy Rate) |
| 3 | Type 'abc' into Sell Rate | 1. Alphabet BLOCKED |
| 4 | Edit Sell Rate to '0.05' and save the row | 1. After saving, table displays Sell Rate as '0.05%' (FE appends % symbol) [Per requirement: CSV stores numeric only; FE displays %] |

**Test Data:** Input: -0.03; abc; 0.05

---

#### TC-220296 · Statement Patch & Regeneration - Form - Edit Statement Summary - verify non-editable fields and sign rules per column
**Priority:** High | **Automation:** Unset

**Description:** Verify Statement Summary edit: many fields are non-editable (calculated by BE); only New Balance, Adjustment, Equity, Call Margin are editable; numeric fields have specific positive-only vs allow-negative rules

**Prerequisites:**
- Statement Table = Statement Summary
- Table has data

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Click Edit icon on a Statement Summary row | 1. Non-editable fields (greyed out / disabled): Account ID, Date, Margin In, Monthly Profit/Loss, Margin Out, Floating Profit/Loss, Unrealised Interest, Realised Interest, Margin Requirement, Commission, Credit 2. Editable fields: New Balance, Adjustment, Equity, Call Margin [Per updated requirement 2026-08-26: most fields are now non-editable as BE calculates them] |
| 2 | Type '-100' into Equity field (negative not allowed) | 1. Value REJECTED — Equity does not allow negative [Equity, Margin Requirement, Call Margin: negative not allowed] |
| 3 | Type '-50.25' into Adjustment field (negative allowed) | 1. Value ACCEPTED — Adjustment allows negative |
| 4 | Type '-200' into New Balance field (negative allowed) | 1. Value ACCEPTED — New Balance allows negative |
| 5 | Type '500.50' into Call Margin field (positive only) | 1. Value ACCEPTED — Call Margin accepts positive values 2. Negative not allowed for Call Margin |
| 6 | Attempt to click/edit a non-editable field (e.g., Margin In) | 1. Field is not clickable / not editable 2. No input cursor appears [Confirms: Non-editable fields cannot be modified] |
| 7 | Attempt to click/edit Credit field | 1. Credit field is NOT clickable / NOT editable 2. No input cursor appears 3. Credit is read-only (non-editable field) [Confirms: Credit cannot be modified in Statement Summary edit mode] |
| 8 | Verify Credit displays current value from DB | 1. Credit field shows value from database 2. Format: numeric with appropriate decimal places 3. Value unchanged regardless of other edits in the row |

**Test Data:** Input: -100; -50.25; -200; 500.50

---

#### TC-220297 · Statement Patch & Regeneration - Form - Delete table record - verify confirmation modal, removal from table, and cancel option
**Priority:** High | **Automation:** Unset

**Description:** Verify Delete action: shows confirmation modal, [Confirm] removes row from working table, [Cancel] keeps row; no snackbar after deletion; DB unchanged until Patch

**Prerequisites:**
- Table has at least 3 rows
- User has full privileges

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Click Delete icon (trash) on row 2 | 1. Confirmation modal appears with: Title 'Delete Confirmation', message 'Are you sure you want to delete this record?', [Delete] button, [Cancel] button |
| 2 | Click [Cancel] | 1. Modal closes 2. Row 2 remains in table (unchanged) 3. No deletion occurs |
| 3 | Click Delete icon on row 2 again | 1. Confirmation modal appears again |
| 4 | Click [Delete] | 1. Modal closes 2. Row 2 removed from Statement Data Table 3. Table now shows 2 rows (row 1 + row 3) 4. No snackbar message displayed 5. DB NOT updated (working table change only) |
| 5 | Click [Export data] after deletion | 1. Exported CSV contains only remaining 2 rows 2. Deleted row NOT in export |

**Test Data:** None

---

#### TC-220298 · Statement Patch & Regeneration - Form - Remarks field - verify optional, placeholder, and accepts free text
**Priority:** High | **Automation:** Unset

**Description:** Verify Remarks field: optional (not mandatory), shows placeholder 'Enter your remarks', accepts free text input

**Prerequisites:**
- Tenant selected
- Table has data

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe Remarks field | 1. Field displayed with placeholder: 'Enter your remarks' 2. Field is empty by default 3. No asterisk (*) — field is optional |
| 2 | Leave Remarks empty and observe [Patch] button | 1. [Patch] button enabled regardless (Remarks not mandatory) [Patch can proceed without Remarks] |
| 3 | Type remarks text | 1. Text accepted and displayed in field |

**Test Data:** Input: 'Centroid API data missing for 2026-08-16'

---

#### TC-220299 · Statement Patch & Regeneration - Toggle/Button - Patch button - verify enabled/disabled states and submission behavior
**Priority:** High | **Automation:** Unset

**Description:** Verify Patch button: disabled when table empty, enabled when table has data, click submits working dataset to BE, creates Patch History record, does NOT regenerate statement

**Prerequisites:**
- Tenant selected
- Statement Table = Settled Position

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe [Patch] button with empty table (no query/upload done) | 1. [Patch] button: DISABLED |
| 2 | Populate table (via Query or Upload CSV) | 1. [Patch] button becomes ENABLED |
| 3 | Delete all rows from table one by one | 1. When last row deleted → table empty again 2. [Patch] button returns to DISABLED |
| 4 | Re-populate table and click [Patch] | 1. Loading/processing indicator shown 2. Patch submitted to BE 3. New record appears in Patch History (Section 4): Name (tenant name), Short Code (tenant short code), Patched Dataset (downloadable CSV link), Range ('Daily'/'Monthly'), Patch Execution Date (current datetime), Patched By (current user), Remarks (value entered or '-' if empty), Status ('PROCESSING' then 'COMPLETED') 4. Statement NOT regenerated (no PDF created yet) 5. [Patch] button may reset/disable after successful patch |

**Test Data:** None

---
#### TC-220300 · Statement Patch & Regeneration - Form - Daylight Saving toggle - verify default state based on today's DST period
**Priority:** High | **Automation:** Unset

**Description:** Verify DST toggle default = ON or OFF based on whether today's date falls within the Daylight Saving period (not always OFF)

**Prerequisites:**
- Tenant selected
- Table has data
- Know the current DST period dates for the tenant's timezone

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Navigate to page on a date WITHIN DST period (e.g. summer) | 1. Toggle displays as ON by default [DST default is determined by whether today is within DST period] |
| 2 | Navigate to page on a date OUTSIDE DST period (e.g. winter) | 1. Toggle displays as OFF by default [Default reflects current real-world DST status] |

**Test Data:** None

---

#### TC-220301 · Statement Patch & Regeneration - Form - Daylight Saving toggle - verify toggling OFF adds +1 hour to Start/End Datetime on UI
**Priority:** High | **Automation:** Unset

**Description:** Verify that when user turns DST toggle OFF, FE adjusts displayed Start/End Datetime by +1 hour (22:00→23:00, 21:00→22:00); toggling ON reverts

**Prerequisites:**
- Statement Type = Daily
- DST toggle currently ON (default during DST period)
- Start Datetime shows: 2026-08-15 22:00:00
- End Datetime shows: 2026-08-16 21:00:00

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe Start/End Datetime with DST = ON | 1. Start Datetime: 2026-08-15 22:00:00 2. End Datetime: 2026-08-16 21:00:00 |
| 2 | Toggle DST to OFF | 1. Start Datetime changes to: 2026-08-15 23:00:00 (+1 hour) 2. End Datetime changes to: 2026-08-16 22:00:00 (+1 hour) [Per comment 20/8: turning OFF DST = FE +1 hour on Start and End] |
| 3 | Toggle DST back to ON | 1. Start Datetime reverts to: 2026-08-15 22:00:00 2. End Datetime reverts to: 2026-08-16 21:00:00 [Toggle ON = revert to DST-period times] |

**Test Data:** None

---

#### TC-220302 · Statement Patch & Regeneration - Form - Daylight Saving toggle - verify DST now AFFECTS query fromTime/toTime
**Priority:** High | **Automation:** Unset

**Description:** Verify that DST toggle state affects the query filter Start/End Datetime values used for Search (changed from original requirement where DST didn't affect query)

**Prerequisites:**
- Statement Type = Daily
- DST toggle ON
- Account ID filled

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | With DST = ON, observe Start/End Datetime values | 1. Start: 2026-08-15 22:00:00 2. End: 2026-08-16 21:00:00 |
| 2 | Click [Search] | 1. Query uses Start=22:00:00, End=21:00:00 to fetch data from BE 2. Table populates with data matching DST ON time range |
| 3 | Toggle DST to OFF (Start becomes 23:00:00, End becomes 22:00:00) | 1. Start changes to 23:00:00, End changes to 22:00:00 |
| 4 | Click [Search] again | 1. Query now uses Start=23:00:00, End=22:00:00 2. Table may show different data (narrower/shifted time window) [Per comment 20/8: DST toggle SHALL affect query fromTime/toTime — contradicts original requirement] |

**Test Data:** None

---

#### TC-220303 · Statement Patch & Regeneration - Calculation - Patch with DST ON (Daily) - verify FE sends correct datetime to BE
**Priority:** High | **Automation:** Unset

**Description:** Verify that when Patch triggered with DST = ON, FE sends Start: prev day 22:00:00, End: selected day 21:00:00 to BE

**Prerequisites:**
- Statement Type = Daily
- DST = ON
- Date context: 2026-08-16
- Table has data

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Ensure DST = ON, query shows 22:00/21:00 times | - |
| 2 | Click [Patch] | 1. FE sends to BE: Start 2026-08-15 22:00:00 UTC, End 2026-08-16 21:00:00 UTC, DST: ON |

**Test Data:** None

---

#### TC-220304 · Statement Patch & Regeneration - Calculation - Patch with DST OFF (Daily) - verify FE sends +1 hour datetime to BE
**Priority:** High | **Automation:** Unset

**Description:** Verify that when Patch triggered with DST = OFF, FE sends Start: prev day 23:00:00, End: selected day 22:00:00 to BE

**Prerequisites:**
- Statement Type = Daily
- DST = OFF
- Date context: 2026-08-16
- Table has data

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Toggle DST OFF, confirm times show 23:00/22:00 | 1. UI displays: Start 2026-08-15 23:00:00, End 2026-08-16 22:00:00 |
| 2 | Click [Patch] | 1. FE sends to BE: Start 2026-08-15 23:00:00 UTC, End 2026-08-16 22:00:00 UTC, DST: OFF |

**Test Data:** None

---

#### TC-220305 · Statement Patch & Regeneration - Calculation - Patch with DST ON (Monthly, July 2026) - verify full month range
**Priority:** High | **Automation:** Unset

**Description:** Verify Monthly + DST ON: Start = June 30 22:00:00, End = July 31 21:00:00 UTC

**Prerequisites:**
- Statement Type = Monthly
- DST = ON
- Month: July 2026
- Table has data

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Set Monthly, select July 2026, DST ON | - |
| 2 | Click [Patch] | 1. FE sends to BE: Start 2026-06-30 22:00:00 UTC, End 2026-07-31 21:00:00 UTC |

**Test Data:** Month: July 2026

---

#### TC-220306 · Statement Patch & Regeneration - Calculation - Patch with DST OFF (Monthly, July 2026) - verify +1 hour on month range
**Priority:** High | **Automation:** Unset

**Description:** Verify Monthly + DST OFF: Start = June 30 23:00:00, End = July 31 22:00:00 UTC

**Prerequisites:**
- Statement Type = Monthly
- DST = OFF
- Month: July 2026
- Table has data

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Set Monthly, select July 2026, toggle DST OFF | - |
| 2 | Click [Patch] | 1. FE sends to BE: Start 2026-06-30 23:00:00 UTC, End 2026-07-31 22:00:00 UTC |

**Test Data:** Month: July 2026

---

#### TC-220307 · Statement Patch & Regeneration - Form - DST toggle does NOT modify table data records
**Priority:** High | **Automation:** Unset

**Description:** Verify that toggling DST ON/OFF only changes Start/End Datetime display — does NOT modify any data records in Statement Data Table

**Prerequisites:**
- Table populated with data (e.g. 3 rows)
- DST currently ON

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Note table data values (e.g. row 1: Open Price = 1800.50, Date = 2026-08-16) | - |
| 2 | Toggle DST OFF | 1. Start/End Datetime fields change (+1 hour) 2. Table data rows remain UNCHANGED: Row 1 Open Price still 1800.50, Row 1 Date still 2026-08-16, all values identical [DST affects time range only, not record content] |
| 3 | Toggle DST ON again | 1. Start/End revert 2. Table data still unchanged |

**Test Data:** None

---

#### TC-220308 · Statement Patch & Regeneration - Form - Preview Statement - verify independent of Query/Upload/Patch, all fields mandatory
**Priority:** High | **Automation:** Unset

**Description:** Verify Preview Statement: independent section, does NOT require prior Query/Upload/Patch; requires Statement Type + Statement Date + Account ID; button disabled until all filled

**Prerequisites:**
- Tenant selected
- NO query or upload performed in Section 2

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe Preview Statement section with no fields filled | 1. Fields displayed: Statement Type * (dropdown, default 'Daily'), Select Date * (date picker), Account ID * (dropdown, placeholder 'Select Account ID') 2. [Preview Statement] button: DISABLED |
| 2 | With Statement Type = Daily (default), observe Statement Date field type and default value | 1. Statement Date is a DATE picker 2. Auto-selects today's date (e.g. 2026-08-16) |
| 3 | Select Account ID | 1. All 3 mandatory fields now filled (Statement Type + Date + Account ID) 2. [Preview Statement] button becomes ENABLED |
| 4 | Clear Account ID (deselect) | 1. [Preview Statement] button returns to DISABLED (a mandatory field is now empty) |
| 5 | Switch Statement Type to 'Monthly' and observe the Statement Date field | 1. Statement Date field changes from DATE picker to MONTH picker 2. Auto-selected value updates to current month (e.g. Aug 2026) [Section 3 field type + auto-selected date must update on Statement Type change, independent of Section 2] |
| 6 | Switch Statement Type back to 'Daily' and observe the Statement Date field | 1. Statement Date field reverts from MONTH picker to DATE picker 2. Auto-selected value updates back to today's date (e.g. 2026-08-16) |

**Test Data:** Account ID: 710001

---

#### TC-220309 · Statement Patch & Regeneration - UI / Layout / Styling - Preview popup modal - verify PDF display, scrollable, X close, view-only
**Priority:** High | **Automation:** Unset

**Description:** Verify clicking Preview Statement generates PDF using latest DB data, shown in popup modal within Root Admin: scrollable, X to close, no download option

**Prerequisites:**
- All 3 Preview fields filled
- [Preview Statement] button enabled

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Click [Preview Statement] | 1. Loading indicator while generating PDF 2. Popup modal appears WITHIN Root Admin page (not new tab) 3. PDF displayed inside modal 4. X button visible at top-right of modal |
| 2 | Scroll within the PDF modal | 1. NO download button available 2. NO right-click save option (or disabled) 3. Preview is VIEW ONLY 4. Preview does NOT trigger regeneration — existing Membersite statement for same account/date remains UNCHANGED (verify by downloading Membersite statement before and after Preview; both identical) [Per requirement: Preview is view only and shall not replace the existing statement] |
| 3 | Look for download button/save option in modal | 1. NO download button available 2. NO right-click save option (or disabled) 3. Preview is VIEW ONLY [Per requirement: Preview is view only and shall not replace the existing statement] |
| 4 | Click X button at top-right | 1. Modal closes 2. Page returns to normal state 3. All form data (Section 1, 2) retained (not reset by Preview) |

**Test Data:** None

---

#### TC-220310 · Statement Patch & Regeneration - Integration - Preview - verify uses latest DB data including just-patched data
**Priority:** High | **Automation:** Unset

**Description:** Verify that Preview generates statement using LATEST available data in DB — if user just patched data, Preview should reflect the patched values

**Prerequisites:**
- User has full privileges
- Account 710001, Date 2026-08-16
- Original DB: Settled Position = 'No records'
- User just completed Patch with new Settled Position data (ORD-NEW, P/L = 500)

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | After completing Patch (Section 2), navigate to Preview Statement | - |
| 2 | Select Statement Type = Daily, Date = 2026-08-16, Account = 710001 | - |
| 3 | Click [Preview Statement] | 1. Preview PDF shows the PATCHED data: SETTLED POSITION section now contains ORD-NEW record (P/L = 500), previously showed 'No records' 2. STATEMENT SUMMARY recalculated to include P/L = 500 [Preview uses latest DB data — reflects just-patched changes] |

**Test Data:** None

---

#### TC-220311 · Statement Patch & Regeneration - Integration - Preview PDF - verify Exchange Rate column appears in Executed Orders section
**Priority:** High | **Automation:** Unset

**Description:** Verify that Preview PDF for Executed Orders table includes Exchange Rate column with correct position and data format (per Q15.4: Executed Orders has Exchange Rate in PDF)

**Prerequisites:**
- User has full privileges
- Tenant selected
- Account has Executed Orders data with: USD pair order (XAUUSD), non-USD pair order (XAUEUR), rejected order

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | In Section 2: Statement Table = Executed Orders, Type = Daily, query account data | - |
| 2 | Click [Preview Statement] in Section 3 | 1. Preview PDF opens 2. EXECUTED ORDERS section displays Exchange Rate column: positioned between 'New/Liq.' and 'Executed Price'; USD pair shows '1'; non-USD pair shows 5 decimal places (e.g. 1.08765); rejected order shows '--' [Confirms: Exchange Rate appears in Executed Orders PDF per Q15.4] |

**Test Data:** None

---

#### TC-220312 · Statement Patch & Regeneration - Integration - Preview PDF - verify Exchange Rate column appears in Settled Position section
**Priority:** High | **Automation:** Unset

**Description:** Verify that Preview PDF for Settled Position table includes Exchange Rate column with correct position and data format (per Q15.4: Settled Position has Exchange Rate in PDF)

**Prerequisites:**
- User has full privileges
- Tenant selected
- Account has Settled Position data with: USD pair position (XAUUSD), non-USD pair position (XAUEUR)

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | In Section 2: Statement Table = Settled Position, Type = Daily, query account data | - |
| 2 | Click [Preview Statement] in Section 3 | 1. Preview PDF opens 2. SETTLED POSITION section displays Exchange Rate column: positioned between 'Close Price' and 'Interest'; USD pair shows '1'; non-USD pair shows 5 decimal places, rounded up [Confirms: Exchange Rate appears in Settled Position PDF per Q15.4] |

**Test Data:** None

---

#### TC-220313 · Statement Patch & Regeneration - Integration - Preview PDF - verify Exchange Rate column does NOT appear in Open Position section
**Priority:** High | **Automation:** Unset

**Description:** Verify that Preview PDF for Open Position table does NOT include Exchange Rate column (per Q15.4: Open Position has Exchange Rate in CSV/UI only, NOT in PDF)

**Prerequisites:**
- User has full privileges
- Tenant selected
- Account has Open Position data
- Statement Data Table (UI) shows Exchange Rate column

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | In Section 2: Statement Table = Open Position, Type = Daily, query account data | 1. Statement Data Table displays Exchange Rate column in UI |
| 2 | Click [Preview Statement] in Section 3 | 1. Preview PDF opens 2. OPEN POSITION section does NOT display Exchange Rate column: columns go directly from 'Close Price' to 'Unrealised Interest'; Exchange Rate column is ABSENT from PDF [Confirms: Open Position Exchange Rate is UI/CSV only, NOT in PDF per Q15.4] |

**Test Data:** None

---

#### TC-220314 · Statement Patch & Regeneration - Integration - Regenerate PDF - verify Exchange Rate column in downloaded PDF for Executed Orders
**Priority:** High | **Automation:** Unset

**Description:** Verify that Regenerated PDF ZIP for Executed Orders includes Exchange Rate column in the downloaded statement

**Prerequisites:**
- User has full privileges
- Patch completed for Executed Orders table
- Patch History shows COMPLETED status

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | In Patch History, click [Regenerate PDF] for Executed Orders patch record | - |
| 2 | Wait for regeneration to complete, click Download | 1. ZIP downloads |
| 3 | Extract ZIP and open PDF statement | 1. PDF EXECUTED ORDERS section includes Exchange Rate column 2. Column values match what was shown in UI: USD = 1, Non-USD = 5dp, Rejected = '--' [Regenerated PDF matches Preview — Exchange Rate present] |

**Test Data:** None

---

#### TC-220315 · Statement Patch & Regeneration - Integration - Regenerate PDF - verify Exchange Rate column in downloaded PDF for Settled Position
**Priority:** High | **Automation:** Unset

**Description:** Verify that Regenerated PDF ZIP for Settled Position includes Exchange Rate column in the downloaded statement

**Prerequisites:**
- User has full privileges
- Patch completed for Settled Position table
- Patch History shows COMPLETED status

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | In Patch History, click [Regenerate PDF] for Settled Position patch record | - |
| 2 | Wait for regeneration to complete, click Download | 1. ZIP downloads |
| 3 | Extract ZIP and open PDF statement | 1. PDF SETTLED POSITION section includes Exchange Rate column 2. Column positioned between 'Close Price' and 'Interest' 3. Values: USD=1, Non-USD=5dp rounded up [Regenerated PDF matches Preview — Exchange Rate present] |

**Test Data:** None

---

#### TC-220316 · Statement Patch & Regeneration - Integration - Regenerate PDF - verify Exchange Rate column does NOT appear in downloaded PDF for Open Position
**Priority:** High | **Automation:** Unset

**Description:** Verify that Regenerated PDF ZIP for Open Position does NOT include Exchange Rate column (per Q15.4 scope limitation)

**Prerequisites:**
- User has full privileges
- Patch completed for Open Position table
- Patch History shows COMPLETED status
- UI Statement Data Table showed Exchange Rate column

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | In Patch History, click [Regenerate PDF] for Open Position patch record | - |
| 2 | Wait for regeneration to complete, click Download | 1. ZIP downloads |
| 3 | Extract ZIP and open PDF statement | 1. PDF OPEN POSITION section does NOT include Exchange Rate column 2. Columns: Close Price → Unrealised Interest (Exchange Rate absent) 3. Matches Q15.4 scope: Open Position Exchange Rate = CSV + UI only, NOT PDF [Confirms: PDF scope correctly excludes Exchange Rate for Open Position] |

**Test Data:** None

---

#### TC-220317 · Statement Patch & Regeneration - Listing - Patch History table - verify all columns, sorting, and pagination
**Priority:** High | **Automation:** Unset

**Description:** Verify Patch History table: displays all required columns, sorted latest first, pagination = 5 records per page

**Prerequisites:**
- User has full privileges
- At least 6 Patch records exist (to test pagination)

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe Patch History table header columns | 1. Columns displayed: Name ↑ (sortable), Short Code ↑ (sortable), Patched Dataset (downloadable link), Range ↑ (Daily or Monthly), Patch Execution Date ↑ (sortable), Patched By ↑ (sortable), Remarks, Status ↑ (sortable), Action |
| 2 | Observe row ordering | 1. Latest Patch Execution Date appears FIRST (descending order) 2. Most recent patch at top of table |
| 3 | Count visible rows | 1. Maximum 5 records per page 2. Pagination indicator shows: '1–5 of X' (total count) |
| 4 | Click next page arrow (>) | 1. Page 2 loads with next set of records (6th onwards) 2. Records are older than page 1 |

**Test Data:** None

---

#### TC-220318 · Statement Patch & Regeneration - Listing - Patch History Range column - verify displays Daily or Monthly based on Statement Type
**Priority:** High | **Automation:** Unset

**Description:** Verify Patch History Range column: shows 'Daily' when patched with Statement Type = Daily, 'Monthly' when patched with Statement Type = Monthly

**Prerequisites:**
- User has full privileges
- Multiple patch records exist from different flows

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Patch using Statement Table = Settled Position, Statement Type = Daily | - |
| 2 | Observe new Patch History record — check Range column | 1. Range column displays: 'Daily' |
| 3 | Patch using Statement Table = Open Position, Statement Type = Monthly | - |
| 4 | Observe new Patch History record — check Range column | 1. Range column displays: 'Monthly' |

**Test Data:** None

---

#### TC-220319 · Statement Patch & Regeneration - Listing - Patched Dataset - verify downloadable CSV contains final working state with deleted records marked
**Priority:** High | **Automation:** Unset

**Description:** Verify Patched Dataset CSV: contains final table state at time of Patch, edited records have final values, deleted records present with Remarks = 'Deleted'

**Prerequisites:**
- Patch completed where: Row 1 edited (P/L changed 500 → 750), Row 2 deleted, Row 3 unchanged

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | In Patch History, click Patched Dataset download link (e.g. 'settled_position_patch_20260816.csv') | 1. CSV file downloads to device |
| 2 | Open CSV and verify edited record (row 1) | 1. Row 1 shows FINAL edited value: Profit/Loss = 750 (not original 500) [Patched Dataset reflects final working table state] |
| 3 | Verify deleted record (row 2) in CSV | 1. Row 2 IS PRESENT in CSV (not removed) 2. Additional 'Remarks' column at end = 'Deleted' && isDeleted = 'TRUE' [Per requirement: Deleted records remain in Patched Dataset with Remarks column = 'Deleted'] |
| 4 | Verify unchanged record (row 3) in CSV | 1. Row 3 present with original values unchanged 2. Remarks column empty or absent for this row && isDeleted = 'FALSE' |

**Test Data:** None

---

#### TC-220320 · Statement Patch & Regeneration - Listing - Patched Dataset link - verify clickable, downloads correct CSV, filename format per record
**Priority:** High | **Automation:** Unset

**Description:** Verify Patched Dataset column in Patch History: displayed as clickable link (purple underline), clicking downloads the CSV file, filename reflects table type and date, each record has its own unique file

**Prerequisites:**
- Multiple Patch History records exist from different patches

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe Patched Dataset column in Patch History table | 1. Each record shows a filename displayed as clickable link (purple underlined text) 2. Filename format indicates content (e.g. 'settled_position_patch_20260816.csv' or similar) |
| 2 | Click on Patched Dataset link for record 1 (e.g. Settled Position patch) | 1. CSV file downloads to device 2. Downloaded filename matches the displayed link text 3. File opens as valid CSV with correct data |
| 3 | Click on Patched Dataset link for record 2 (different patch) | 1. Different CSV file downloads 2. Content matches that specific patch's working dataset (not record 1's data) [Each record has its own independent Patched Dataset file] |
| 4 | Verify record with no uploaded file (Fetch from Centroid / Query only patch) | 1. Patched Dataset link still present and downloadable [Patched Dataset = final table state at time of Patch, regardless of data source] |

**Test Data:** None

---
#### TC-220321 · Statement Patch & Regeneration - State - Patch History Status - verify auto-refresh from PROCESSING to COMPLETED
**Priority:** High | **Automation:** Unset

**Description:** Verify Status column auto-refreshes without manual page reload: PROCESSING → COMPLETED

**Prerequisites:**
- Patch just triggered
- Status shows 'PROCESSING'

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | After clicking [Patch], observe Status column in Patch History | 1. Status shows 'PROCESSING' (grey badge) |
| 2 | Do NOT refresh page manually. Wait. | 1. Status auto-refreshes to 'COMPLETED' (green badge) 2. No manual action required for status update |

**Test Data:** None

---

#### TC-220322 · Statement Patch & Regeneration - State - Patch Status FAILED - verify failed state with no retry button
**Priority:** High | **Automation:** Unset

**Description:** Verify that when Patch job fails (due to invalid data bypassing FE validation via API), Status changes to FAILED and no retry button is available

**Prerequisites:**
- Tenant selected
- Statement Table = Settled Position
- Invalid CSV data prepared (will fail BE validation)
- Postman or API tool available to bypass FE validation

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Using Postman/API, upload CSV data that passes FE validation but contains invalid data that will fail BE processing (e.g. malformed date format, invalid Account ID format) | - |
| 2 | Trigger Patch via API or observe FE after API upload | 1. Patch History record created 2. Status shows 'PROCESSING' |
| 3 | Wait for BE processing to complete/fail | 1. Status auto refresh from PROCESSING → FAILED (red badge) 2. Action column: NO retry button displayed 3. BE appends the applicable error message after the user-entered remarks |

**Test Data:** API upload: invalid_data.csv (bypasses FE validation)

---

#### TC-220323 · Statement Patch & Regeneration - State - Patch Failed - verify user can re-attempt Patch after API-triggered failure
**Priority:** High | **Automation:** Unset

**Description:** Verify after Patch failure (triggered via API): user can re-query/upload data and Patch again; Patch History appends new record (old FAILED record preserved)

**Prerequisites:**
- User has full privileges
- Previous Patch failed via API call (simulated BE failure)
- FAILED record visible in Patch History
- Working table may be empty (page refresh after failure)

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | [Pre-condition] Trigger Patch failure via API call to simulate BE error (S3/DB/infra issue) | 1. Patch History shows new record with Status = FAILED 2. No Retry button available (per Confluence Q1) 3. Remarks may contain error message from BE |
| 2 | Observe Section 2 (Statement Data Query & Patch) state | 1. Working table may be empty or retain previous data (depends on page state) 2. Query filters and Upload CSV still functional 3. [Patch] button visible |
| 3 | Re-query data: fill filters (same Account ID, Date range) and click [Search] OR Upload corrected CSV file | - |
| 4 | Make any necessary edits to fix the data issue | 1. Edit modal works normally 2. Changes saved to working table |
| 5 | Click [Patch] button | 1. New Patch job initiated |
| 6 | Observe Patch History section | 1. NEW record appears at top of Patch History 2. New record Status: PROCESSING → COMPLETED 3. Old FAILED record STILL EXISTS (not overwritten) 4. Total records in history increased by 1 [Confirms: Patch History is append-only] |
| 7 | Verify both records in Patch History | 1. New COMPLETED record: Patched Dataset downloadable, Regenerate PDF available 2. Old FAILED record: Status unchanged FAILED, original timestamp preserved, no Retry button, Remarks preserved [Confirms: Historical records immutable, audit trail intact] |

**Test Data:** API: POST /patch with invalid payload or mock failure response

---

#### TC-220324 · Statement Patch & Regeneration - Toggle/Button - Regenerate PDF - verify appears only when Status = COMPLETED, one job at a time
**Priority:** High | **Automation:** Unset

**Description:** Verify Regenerate PDF button: only shown when Status = COMPLETED; not shown for PROCESSING; only 1 Regenerate job at a time; other buttons disabled during processing

**Prerequisites:**
- Patch History has records with different statuses

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe Action column for record with Status = 'PROCESSING' | 1. NO Regenerate button visible [Per requirement: When Status = Processing, no Regenerate button displayed] |
| 2 | Observe Action column and Remark column for record with Status = 'FAILED' | 1. NO Regenerate button visible 2. NO Download button visible [Patch failed = no statement data to regenerate] 3. BE appends the applicable error message after the user-entered remarks |
| 3 | Observe Action column for record with Status = 'COMPLETED' | 1. [Regenerate PDF] button visible and enabled |
| 4 | Click [Regenerate PDF] on a COMPLETED record | 1. Loading icon appears WITHIN the button (replacing text) 2. All OTHER [Regenerate PDF] buttons in table become DISABLED [Per requirement: Only 1 Regenerate job at a time] |
| 5 | Wait for regeneration to complete | 1. Loading icon disappears 2. Button changes to Download icon 3. Other Regenerate buttons re-enabled |

**Test Data:** None

---

#### TC-220325 · Statement Patch & Regeneration - State - Regenerate Status FAILED - verify failed state with retry button
**Priority:** High | **Automation:** Unset

**Description:** Verify that when Regenerate job fails (S3/infra error), a retry button appears in Action column allowing user to retry regeneration

**Prerequisites:**
- Patch completed successfully (Status = COMPLETED)
- Regenerate will fail (simulate infra/S3 error — may need BE support)

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Click [Regenerate PDF] on a COMPLETED Patch record | 1. Loading icon appears in button 2. Regeneration job starts |
| 2 | Wait for Regenerate to fail (or simulate failure via BE) | 1. Status/indicator shows failure state 2. Retry button appears in Action column (replacing Download icon) [PM confirmed: Regenerate failure = retry button available] |
| 3 | Click Retry button | 1. Regeneration re-triggered 2. Loading icon reappears 3. If successful this time: Download icon appears 4. If fails again: Retry button remains |

**Test Data:** None

---

#### TC-220326 · Statement Patch & Regeneration - State - Regenerate - verify navigate away and return while job processing
**Priority:** High | **Automation:** Unset

**Description:** Verify that if user navigates away from the page while Regenerate is processing, then returns, the job status is correctly reflected (still processing or completed with Download button)

**Prerequisites:**
- Regenerate job triggered
- Loading icon shown in button
- Job is processing

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Click [Regenerate PDF] on a Completed record — observe loading icon | 1. Loading icon appears in button 2. Other Regenerate buttons disabled |
| 2 | Navigate away from the page (e.g. click 'Dashboard' or another menu item) | 1. Page changes to different section |
| 3 | Navigate back to Troubleshoot Platform > Statement Patch & Regeneration | 1. Page loads 2. Patch History displays |
| 4 | Observe the record that was being regenerated | 1. IF still processing: loading icon visible in button, other Regenerate buttons still disabled 2. IF completed: Download icon shown (button changed from Regenerate to Download) 3. If regeneration FAILED: FAILED tag + Retry icon displayed in Action column [Job continues server-side regardless of navigation; UI reflects current state on return] |

**Test Data:** None

---

#### TC-220327 · Statement Patch & Regeneration - Export - Download regenerated ZIP - verify contains correct PDFs
**Priority:** High | **Automation:** Unset

**Description:** Verify clicking Download icon downloads ZIP file containing regenerated statement PDF(s) for all affected accounts in the patch

**Prerequisites:**
- Regeneration completed
- Download icon visible in Action column

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Click Download icon | 1. ZIP file downloads to user's device 2. File has .zip extension |
| 2 | Extract ZIP and examine contents | 1. ZIP contains PDF file(s) 2. PDF filename indicates account + date (e.g. account_710001_20260816.pdf) 3. If patch contained multiple Account IDs: multiple PDFs in ZIP (one per account per date) |
| 3 | Open a PDF and verify format matches standard Daily Statement structure | 1. PDF structure matches standard statement format: Header (Logo, 'Daily Statement', date), Account Info, EXECUTED ORDERS, SETTLED POSITION, OPEN POSITION, Deposit/Withdrawal, STATEMENT SUMMARY, Interest Rate 2. Patched data appears in relevant section |

**Test Data:** None

---

#### TC-220328 · Statement Patch & Regeneration - State - Regenerated PDF replaces Membersite statement, NO email sent to trader
**Priority:** High | **Automation:** Unset

**Description:** Verify: regenerated PDF overwrites existing Membersite statement for affected account/date; NO statement email sent to trader (silent update)

**Prerequisites:**
- Regeneration completed successfully for Account 710001, date 2026-08-16
- Trader's email inbox accessible
- Membersite accessible for account 710001

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | After successful Regeneration, check trader's email inbox | 1. NO new statement email received by trader 2. No notification of any kind sent to trader [Per requirement: No statement email shall be sent] |
| 2 | Login to Membersite as trader (account 710001) | - |
| 3 | Navigate to statement download for date 2026-08-16 | 1. Statement is available for download 2. Downloaded PDF contains the PATCHED data (updated/added records) 3. PDF matches the regenerated version from ZIP [Regenerated statement REPLACES the old one on Membersite] |

**Test Data:** None

---

#### TC-220329 · Statement Patch & Regeneration - Toggle/Button - Refresh icon - verify manual refresh of Patch History
**Priority:** High | **Automation:** Unset

**Description:** Verify [Refresh] icon in Patch History manually refreshes the list to show latest records

**Prerequisites:**
- Patch History visible
- New patch created from another browser tab/session

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe Refresh button (top-right of Patch History) | 1. Refresh button visible and clickable |
| 2 | In a second browser tab, complete a Patch job for same tenant | - |
| 3 | Return to first tab — observe Patch History (without clicking Refresh) | 1. New record from tab 2 may NOT appear yet (depending on auto-refresh interval) |
| 4 | Click [Refresh] button in the top right corner of Section 4 | 1. Table reloads 2. New record from tab 2 now visible in Patch History 3. List sorted correctly (latest first) |

**Test Data:** None

---

#### TC-220330 · Statement Patch & Regeneration - Sort - Patch History table - verify sortable columns respond to click
**Priority:** High | **Automation:** Unset

**Description:** Verify that columns with sort indicator (↑) in Patch History table can be sorted ascending/descending by clicking column header

**Prerequisites:**
- Multiple Patch History records exist with different values across columns
- At least 3+ records for meaningful sort verification

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Observe default sort order (Patch Execution Date descending — latest first) | 1. Records ordered by Patch Execution Date, newest at top |
| 2 | Click 'Patch Execution Date' column header | 1. Sort toggles to ascending (oldest first) 2. Arrow indicator changes direction |
| 3 | Click 'Patch Execution Date' column header again | 1. Sort toggles back to descending (newest first) |
| 4 | Click 'Name' column header | 1. Table re-sorts alphabetically by tenant Name 2. Sort indicator moves to Name column |
| 5 | Click 'Range' column header | 1. Table re-sorts by Range value (Daily/Monthly) |
| 6 | Click 'Status' column header | 1. Table re-sorts by Status (COMPLETED/PROCESSING/FAILED grouping) |
| 7 | Click 'Patched By' column header | 1. Table re-sorts alphabetically by user name |
| 8 | Click 'Short Code' column header | 1. Table re-sorts alphabetically by Short Code |

**Test Data:** None

---

#### TC-220331 · Statement Patch & Regeneration - Integration - E2E Query flow: Query > Edit > Delete > Patch > Verify Patched Dataset > Preview > Regenerate > Download > Membersite
**Priority:** High | **Automation:** Unset

**Description:** Verify complete happy path: Query DB data → Edit row → Delete row → Patch → Download Patched Dataset → Preview shows updated data → Regenerate → Download ZIP → Membersite updated

**Prerequisites:**
- User has full privileges
- Tenant: tinshing
- Statement Table: Settled Position, Type: Daily
- Account 710001 has existing data in DB (3 rows: ORD001, ORD002, ORD003)
- ORD001 P/L = 500, ORD002 P/L = 300, ORD003 P/L = 200

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Select tenant tinshing, Statement Table = Settled Position, Type = Daily | - |
| 2 | Fill Account ID = 710001, Start = 2026-08-15 22:00:00, End = 2026-08-16 21:00:00 | - |
| 3 | Click [Search] — verify table populates with 3 rows | 1. Table shows 3 rows: ORD001, ORD002, ORD003 |
| 4 | Edit ORD001: change Profit/Loss from 500 to 850 | 1. Working table shows ORD001 P/L = 850 |
| 5 | Delete ORD002 (click Delete → Confirm) | 1. Table now shows 2 rows: ORD001 (edited), ORD003 (unchanged) |
| 6 | Enter Remarks: 'Patch missing settled position data' | - |
| 7 | Click [Patch] | 1. Patch History new record created 2. Status: PROCESSING → COMPLETED |
| 8 | Download Patched Dataset CSV from Patch History | 1. CSV contains: ORD001 with P/L = 850 (edited value), ORD002 with Remarks = 'Deleted' && isDeleted = TRUE, ORD003 with original values |
| 9 | Preview Statement: Statement Type = Daily, Date = 2026-08-16, Account = 710001, click [Preview Statement] | 1. PDF shows: SETTLED POSITION ORD001 (P/L=850), ORD003 (P/L=200); ORD002 NOT present (deleted); STATEMENT SUMMARY recalculated |
| 10 | Click [Regenerate PDF] in Patch History | 1. Loading icon → completes → Download icon appears |
| 11 | Click Download, extract ZIP, open PDF | 1. PDF matches Preview content 2. SETTLED POSITION: ORD001 (850), ORD003 (200), no ORD002 |
| 12 | Login to Membersite as trader (710001), download statement for 2026-08-16 in Assets Page | 1. Membersite PDF matches regenerated PDF 2. Patched data reflected (ORD001=850, no ORD002) |

**Test Data:** P/L: 500 → 850; Remarks: Patch missing settled position data

---

#### TC-220332 · Statement Patch & Regeneration - Integration - E2E Upload CSV flow: Upload > Edit > Patch > Regenerate > Download > Membersite
**Priority:** High | **Automation:** Unset

**Description:** Verify complete happy path via CSV upload: Upload CSV with multiple accounts → Edit row → Patch → Regenerate → Download ZIP with multiple PDFs → Membersite updated for all accounts

**Prerequisites:**
- User has full privileges
- Tenant: tinshing
- Statement Table: Deposit/Withdrawal, Type: Daily
- CSV prepared with 2 Account IDs: 710001 (1 deposit record) and 710002 (1 withdrawal record)
- Original statements show 'No records' in Deposit/Withdrawal section

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Select tenant, Statement Table = Deposit/Withdrawal, Type = Daily | - |
| 2 | Upload CSV with records for 710001 and 710002 | 1. Table shows 2 rows (mixed accounts and date) 2. Query filters DISABLED (CSV uploaded) |
| 3 | Edit row 2: change Amount from 2000.00 to 2500.00 | 1. Working table updated |
| 4 | Click [Patch] (with DST OFF) | 1. Patch History record created with Status COMPLETED 2. Patched Dataset contains both rows (row 2 with edited amount 2500) |
| 5 | Click [Regenerate PDF] | 1. Regeneration processes 2. Download icon appears when complete |
| 6 | Download ZIP and extract | 1. ZIP contains 2 PDF files (one per account): PDF for 710001, PDF for 710002 |
| 7 | Open PDF for 710001 — check Deposit/Withdrawal section | 1. Shows: DEP001, DEPOSIT, 5000.00 [Previous 'No records' now filled] |
| 8 | Open PDF for 710002 — check Deposit/Withdrawal section | 1. Shows: WD001, WITHDRAWAL, 2500.00 (edited value) [Amount reflects the edit made before Patch] |
| 9 | Login to Membersite as trader 710001 — download statement in Assets page | 1. Statement shows Deposit/Withdrawal with DEP001 record |
| 10 | Login to Membersite as trader 710002 — download statement in Assets Page | 1. Statement shows Deposit/Withdrawal with WD001 (amount 2500) |

**Test Data:** File: deposit_withdrawal_multi.csv (Row 1: 710001, 2026-08-16, DEP001, Client deposit, DEPOSIT, 5000.00; Row 2: 710002, 2026-08-17, WD001, Client withdrawal, WITHDRAWAL, 2000.00); Amount: 2000 → 2500

---
#### TC-220333 · Statement Patch & Regeneration - Integration - E2E Monthly flow: Query > Edit > Delete > Patch > Verify Patched Dataset > Preview > Regenerate > Download > Membersite
**Priority:** High | **Automation:** Unset

**Description:** End-to-end test for Monthly Statement Type flow — verifies full workflow with Monthly-specific behaviors: month selector, Monthly columns (no Daily Interest), full month datetime range

**Prerequisites:**
- Tenant: tinshing
- Account 710001 has existing Monthly data in DB
- Statement Type = Monthly
- Month: July 2026

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Select tenant 'tinshing', Statement Table = 'Open Position', Statement Type = 'Monthly' | 1. Month selector appears (replaces date picker) 2. Columns no change to when change to Monthly |
| 2 | Select Month = July 2026, Account ID = 710001, click [Search] | 1. Query executes with full month range: Start 2026-06-30 22:00:00 (DST ON), End 2026-07-31 21:00:00 2. Table populates with Open Position Monthly data |
| 3 | Click Edit icon on row 1, modify Floating Profit/Loss value | 1. Edit modal opens 2. 'Daily Interest' field NOT present (Monthly) 3. After save: row updates to 750.00 |
| 4 | Click Delete icon on row 2, confirm deletion | 1. Confirmation modal appears 2. After confirm: row removed from table 3. Row count decreases by 1 |
| 5 | Enter Remarks, click [Patch] | 1. Snackbar: 'Statement patch success!' 2. Patch History shows new record: Range 'Monthly', Status PROCESSING → COMPLETED |
| 6 | Click Patched Dataset download link | 1. CSV downloads 2. Row 1 shows edited value (750.00) 3. Filename includes 'monthly' identifier |
| 7 | In Preview Statement section: Statement Type = Monthly, select July 2026, Account 710001, click [Preview Statement] | 1. Preview modal opens with PDF 2. OPEN POSITION section shows patched data: Row 1 750.00 (edited), Row 2 NOT displayed (deleted) 3. Monthly format columns (no Daily Interest) |
| 8 | Close Preview, click [Regenerate PDF] button on Patch History record | 1. Status changes: COMPLETED → PROCESSING 2. After completion: Status = COMPLETED 3. Download link appears |
| 9 | Click Download link for regenerated ZIP | 1. ZIP file downloads 2. Contains Monthly statement PDF for July 2026 3. PDF shows patched data with Monthly format |
| 10 | Login to Membersite as trader 710001, navigate to Statements > July 2026 | 1. Monthly statement available for download 2. PDF matches regenerated content 3. Open Position section shows patched values [Confirms: Full Monthly E2E workflow from Query → Membersite delivery] |

**Test Data:** Month: July 2026; Account: 710001; Original: 500.00; New: 750.00; Remarks: 'Monthly E2E test - July 2026'

---

#### TC-220334 · Statement Patch & Regeneration - Integration - E2E Upload CSV Monthly flow: Upload > Edit > Delete > Patch > Regenerate > Download > Membersite
**Priority:** High | **Automation:** Unset

**Description:** Verify complete E2E flow for Monthly statement via CSV upload: Upload CSV → Edit row → Delete row → Patch → Download Patched Dataset → Preview Monthly → Regenerate → Download ZIP → Membersite Monthly statement updated

**Prerequisites:**
- User has full privileges
- Tenant: tinshing
- Statement Table: Open Position, Type: Monthly
- CSV prepared for July 2026 with Account 710001, 3 rows: ORD001 (Net Volume 1.5), ORD002 (Net Volume 2.0), ORD003 (Net Volume 3.0)
- Original Monthly statement shows different or no data

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Select tenant tinshing, Statement Table = Open Position, Type = Monthly | 1. Statement Table = Open Position selected 2. Statement Type dropdown shows: Monthly 3. Select Month dropdown appears (instead of Start/End datetime) |
| 2 | Upload CSV file with Open Position data for July 2026 | 1. CSV accepted (valid format, columns match Open Position schema) 2. Table shows rows: ORD001, ORD002, ORD003 3. Query filters (Account ID, Select Month) become DISABLED 4. Monthly columns displayed (no Daily Interest column) |
| 3 | Edit ORD001: change Net Volume from 1.5 to 3.0 | 1. Edit mode: raw value shown 2. Working table updated: ORD001 Net Volume = 3.0 |
| 4 | Delete ORD002 (click Delete → Confirm) | 1. Confirmation modal appears 2. After confirm: table shows ORD001, ORD003 3. ORD002 removed from working table |
| 5 | Enter Remarks, click [Patch] | 1. Snackbar: 'Statement patch success!' 2. Patch History shows new record: Range 'Monthly', Status PROCESSING → COMPLETED, Remarks 'Monthly E2E CSV upload test - July 2026' |
| 6 | Download Patched Dataset CSV from Patch History | 1. CSV downloads 2. Contains: ORD001 Net Volume = 3.0 (edited value), ORD002 with IsDeleted = TRUE (deleted record), ORD003 Net Volume retained 3. Filename includes 'monthly' or month identifier |
| 7 | Preview Statement: Statement Type = Monthly, Month = July 2026, Account = 710001, click [Preview Statement] | 1. Preview modal opens with Monthly PDF 2. OPEN POSITION section shows: ORD001 Net Volume = 3.0 (patched), ORD002 NOT displayed (deleted), ORD003 (patched) 3. Monthly format (no Daily Interest column) |
| 8 | Click [Regenerate PDF] in Patch History | 1. Status: COMPLETED → PROCESSING 2. After completion: Download icon appears 3. Status returns to COMPLETED |
| 9 | Download ZIP, extract, open Monthly PDF | 1. ZIP contains Monthly statement PDF 2. PDF shows: Open Position ORD001 with Net Volume = 3.0, ORD002 NOT present, ORD003 patched, Monthly format columns |
| 10 | Login to Membersite as trader 710001, navigate to Assets > Statements > July 2026 Monthly | 1. Monthly statement available for July 2026 2. PDF content matches regenerated version 3. Open Position shows patched data (ORD001 & ORD003, no ORD002) [Confirms: Full E2E Monthly CSV Upload workflow from Upload → Membersite delivery] |

**Test Data:** File: open_position_monthly.csv (Row 1: 710001, 2026-07-15, ORD001, XAUUSD, 1.5, ...; Row 2: 710001, 2026-07-17, ORD002, EURUSD, 2.0, ...; Row 3: 710001, 2026-07-18, ORD003, EURUSD, 2.0, ...); Net Volume: 1.5 → 3.0; Remarks: 'Monthly E2E CSV upload test - July 2026'

---

#### TC-220335 · Statement Patch & Regeneration - Column - IsDeleted - verify present in Export Data CSV
**Priority:** High | **Automation:** Unset

**Description:** Verify that Export Data CSV includes IsDeleted column with FALSE value for all visible (non-deleted) rows

**Prerequisites:**
- Tenant selected
- Statement Table = Settled Position
- Table has data (from Query or Upload)

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Query or upload data to populate table | 1. Table displays data |
| 2 | Click [Export data] | 1. CSV file downloads 2. CSV includes IsDeleted column 3. All rows show IsDeleted=FALSE |

**Test Data:** None

---

#### TC-220336 · Statement Patch & Regeneration - Form - Bulk Delete via CSV - verify IsDeleted=TRUE marks rows for deletion
**Priority:** High | **Automation:** Unset

**Description:** Verify that uploading CSV with IsDeleted=TRUE for specific rows marks those rows for deletion; after Patch, deleted rows are removed from DB

**Prerequisites:**
- Tenant selected (tinshing)
- Statement Table = Settled Position
- Account 710001 has existing data: ORD001, ORD002, ORD003
- CSV prepared with: ORD001 IsDeleted=TRUE (to delete), ORD002 IsDeleted=FALSE (to keep), ORD003 IsDeleted=TRUE (to delete)

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Export current data via [Export data] to get CSV with IsDeleted column | 1. CSV downloads with IsDeleted column 2. All rows show IsDeleted=FALSE |
| 2 | Edit exported CSV: set IsDeleted=TRUE for ORD001 and ORD003, keep ORD002 as IsDeleted=FALSE | - |
| 3 | Upload the modified CSV via [Choose file] | 1. CSV validated and accepted 2. Statement Data Table shows all 3 rows |
| 4 | Click [Patch] | 1. Patch processes successfully 2. Snackbar confirms success |
| 5 | Query same account/date range via [Search] | 1. Statement Data Table shows ONLY ORD002 2. ORD001 and ORD003 are DELETED from DB 3. Bulk delete via IsDeleted=TRUE confirmed working |

**Test Data:** Modified CSV: ORD001 IsDeleted=TRUE; ORD002 IsDeleted=FALSE; ORD003 IsDeleted=TRUE

---

#### TC-220337 · Statement Patch & Regeneration - State - Double-click Patch - verify no duplicate patch jobs
**Priority:** High | **Automation:** Unset

**Description:** Verify rapidly clicking Patch does not create duplicate records in Patch History

**Prerequisites:**
- Table has data
- [Patch] button enabled

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Rapidly double-click [Patch] button | 1. Only 1 Patch History record created (no duplicates) 2. Button disables immediately after first click to prevent double submission |

**Test Data:** None

---

#### TC-220338 · Statement Patch & Regeneration - State - Patch same account/date/table twice - verify second overwrites first
**Priority:** High | **Automation:** Unset

**Description:** Verify that patching same scope (account + date + table type) a second time overwrites previous patch data in DB

**Prerequisites:**
- First Patch completed: Account 710001, Settled Position, 2026-08-16, ORD001 P/L = 500
- Second CSV prepared: same scope but ORD001 P/L = 900

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Complete first Patch (P/L = 500) | - |
| 2 | Upload new CSV with ORD001 P/L = 900 for same account/date | - |
| 3 | Click [Patch] again | 1. Second Patch History record created |
| 4 | Regenerate from second patch record, download PDF | 1. PDF shows ORD001 P/L = 900 (second patch wins) [Same Order Ref = overwrite per requirement] |

**Test Data:** Second CSV: ORD001 P/L = 900

---

#### TC-220339 · Statement Patch & Regeneration - State - Browser refresh during Patch processing - verify job continues server-side
**Priority:** High | **Automation:** Unset

**Description:** Verify that Patch job continues processing on BE even if user refreshes browser mid-processing

**Prerequisites:**
- Patch triggered, Status = PROCESSING

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Click [Patch] — observe Status = PROCESSING in Patch History | - |
| 2 | Immediately refresh browser (F5) | 1. Page reloads |
| 3 | Navigate back to Statement Patch & Regeneration, observe Patch History | 1. Patch record exists 2. Status either still PROCESSING or already COMPLETED 3. Job was NOT cancelled by browser refresh [BE processing continues independently of FE session] |

**Test Data:** None

---

#### TC-220340 · Statement Patch & Regeneration - State - Order Ref logic - same Ref overwrites, new Ref adds
**Priority:** High | **Automation:** Unset

**Description:** Verify: uploaded data with EXISTING Order Ref = overwrite that record in DB; NEW Order Ref = insert as new record; other existing records unaffected

**Prerequisites:**
- Account 710001 has existing Settled Position in DB: ORD001 (P/L = 500), ORD002 (P/L = 300)
- ORD999 does NOT exist in DB

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Preview original statement for 710001 — note SETTLED POSITION: ORD001=500, ORD002=300, no ORD999 | - |
| 2 | Upload CSV with: ORD001 P/L = 800 (existing → overwrite) and ORD999 P/L = 350 (new → insert) | - |
| 3 | Click [Patch], then Regenerate and download | 1. Regenerated PDF SETTLED POSITION section shows: ORD001 P/L = 800 (overwritten, was 500), ORD002 P/L = 300 (UNCHANGED — not in upload, not affected), ORD999 P/L = 350 (newly added) [Same Order Ref = overwrite; New Order Ref = add; Unmentioned records = unchanged] |

**Test Data:** CSV: ORD001 P/L = 800; ORD999 P/L = 350

---

#### TC-220341 · Statement Patch & Regeneration - Calculation - STATEMENT SUMMARY recalculated after patching missing data
**Priority:** High | **Automation:** Unset

**Description:** Verify that BE recalculates STATEMENT SUMMARY values (Profit/Loss, New Balance, Equity) when Settled Position or other financial data is patched

**Prerequisites:**
- Account 710001, Date 2026-08-16
- Original: SETTLED POSITION = 'No records', Statement Summary P/L = 0, New Balance = 49,926.96
- Upload Settled Position with P/L = 500

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Preview original statement — note Statement Summary: Profit/Loss = 0.000, New Balance = 49,926.960 | - |
| 2 | Upload Settled Position CSV (ORD-NEW, P/L = 500.00) | - |
| 3 | Patch and Regenerate, download PDF | 1. SETTLED POSITION section now shows ORD-NEW record 2. STATEMENT SUMMARY recalculated: Profit/Loss now includes +500.00, New Balance adjusted (previous + P/L), Equity recalculated |

**Test Data:** CSV: ORD-NEW, P/L = 500.00

---

#### TC-220342 · Statement Patch & Regeneration - State - Patch scope isolation - patching Account A does not affect Account B
**Priority:** High | **Automation:** Unset

**Description:** Verify that patching data for Account A does not modify Account B's statement on Membersite, even if both are in same tenant

**Prerequisites:**
- Tenant: tinshing
- Account A (710001) and Account B (710002) both have statements for 2026-08-16
- Upload CSV only for Account A

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Download Account B (710002) statement from Membersite (baseline) | - |
| 2 | Upload CSV with data for Account A (710001) only, Patch and Regenerate | - |
| 3 | Download Account B (710002) statement from Membersite again | 1. Account B's statement IDENTICAL to baseline 2. No data modified in Account B's PDF [Patching Account A does NOT affect Account B] |

**Test Data:** CSV: Account 710001 only

---

#### TC-220343 · Statement Patch & Regeneration - Integration - Sequential patching multiple table types for same account
**Priority:** High | **Automation:** Unset

**Description:** Verify user can patch different Statement Tables in sequence for same account/date; final Regenerate produces PDF reflecting ALL patches

**Prerequisites:**
- Account 710001, Date 2026-08-16
- Need to patch both Settled Position and Deposit/Withdrawal
- Original has 'No records' in both sections

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Select Statement Table = Settled Position, upload CSV (ORD-NEW, P/L = 500) | - |
| 2 | Click [Patch] — observe Patch History record created | 1. Patch History: Record 1 (Settled Position) |
| 3 | Select Statement Table = Deposit/Withdrawal, upload CSV (DEP001, DEPOSIT, 5000) | - |
| 4 | Click [Patch] — observe second Patch History record | 1. Patch History: Record 2 (Deposit/Withdrawal) |
| 5 | Click [Regenerate PDF] on the LATEST record (Record 2) | 1. Regeneration produces PDF using ALL latest DB data for the account |
| 6 | Download ZIP, open PDF | 1. PDF shows: SETTLED POSITION ORD-NEW (P/L = 500) — from Patch 1; DEPOSIT/WITHDRAWAL DEP001 (DEPOSIT, 5000) — from Patch 2; both sections populated (no longer 'No records') [Regenerate uses latest DB state which includes all previous patches] |

**Test Data:** Job 1: Settled Position; Job 2: Deposit/Withdrawal

---

#### TC-220344 · Statement Patch & Regeneration - Integration - Search - verify empty state when no data exists for filters
**Priority:** High | **Automation:** Unset

**Description:** Verify that querying a valid Account ID + date range that has NO existing data in DB shows the empty state ('No items available')

**Prerequisites:**
- Tenant selected
- Statement Table = Settled Position, Type = Daily
- Account ID has NO statement data for the selected date range

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Fill Account ID + Start/End Datetime for a range known to have no data | - |
| 2 | Click [Search] | 1. Loading indicator shown, then completes 2. Statement Data Table shows empty state: 'No items available' 3. [Export data] button: disabled (no records) 4. [Patch] button: disabled (no records) 5. No error snackbar (empty result is valid, not an error) |

**Test Data:** Account: 710001 (no data for this period); Start: 2026-07-10 22:00:00; End: 2026-07-11 21:00:00

---

#### TC-220345 · Statement Patch & Regeneration - Calculation - Patch Monthly for January - verify cross-year datetime range
**Priority:** High | **Automation:** Unset

**Description:** Verify Monthly patch for January correctly calculates cross-year Start Datetime (previous day of Jan 1 = Dec 31 of previous year)

**Prerequisites:**
- Statement Type = Monthly
- Selected Month: January 2027
- Table has data

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Set Statement Type = Monthly, select January 2027, DST OFF | - |
| 2 | Click [Patch] | 1. FE sends to BE (DST OFF): Start 2026-12-31 23:00:00 UTC (Dec 31 of PREVIOUS year), End 2027-01-31 22:00:00 UTC [Cross-year boundary: prev day of Jan 1 correctly rolls back to Dec 31 of prior year] |
| 3 | Repeat with DST ON | 1. FE sends to BE (DST ON): Start 2026-12-31 22:00:00 UTC, End 2027-01-31 21:00:00 UTC |

**Test Data:** Month: January 2027

---

#### TC-220346 · Statement Patch & Regeneration - Calculation - Monthly February - verify correct last day (28 vs 29 leap year)
**Priority:** High | **Automation:** Unset

**Description:** Verify Monthly patch for February correctly determines the last day: 28 for non-leap year, 29 for leap year

**Prerequisites:**
- Statement Type = Monthly
- Table has data

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Select February 2027 (non-leap year), DST OFF, click [Patch] | 1. End Datetime = 2027-02-28 22:00:00 UTC (Feb has 28 days in 2027) |
| 2 | Select February 2028 (leap year), DST OFF, click [Patch] | 1. End Datetime = 2028-02-29 22:00:00 UTC (Feb has 29 days in leap year 2028) |

**Test Data:** Month: February 2027; Month: February 2028

---

#### TC-220347 · Statement Patch & Regeneration - State - Search after unsaved edits - verify edits discarded silently
**Priority:** High | **Automation:** Unset

**Description:** Verify that unsaved edits in working table are discarded silently (no warning) when user performs a new Search before Patch

**Prerequisites:**
- Statement Table has queried data
- User edited 1+ rows (not yet Patched)

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Query data, then Edit a row (change a value, e.g. P/L 500 → 750) but do NOT Patch | - |
| 2 | Change Account ID or date filter and click [Search] again | 1. Unsaved edits discarded silently — NO warning modal 2. Table replaced with new query results 3. Previous edited data (P/L = 750) is lost [PM confirmed: silent discard, no prompt] |

**Test Data:** Edit: P/L 500 → 750

---

#### TC-220348 · Statement Patch & Regeneration - Integration - Preview Statement when no data exists - verify PDF shows empty sections
**Priority:** High | **Automation:** Unset

**Description:** Verify Preview Statement output when the selected Account ID + date has no statement data in DB — PDF generated with all sections showing 'No records'

**Prerequisites:**
- Tenant selected
- Account ID + date with NO data in DB

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | In Preview section, select Statement Type, Date, Account ID with no data | - |
| 2 | Click [Preview Statement] | 1. PDF generated successfully 2. All sections display with standard headers 3. All data tables show 'No records' or equivalent empty state 4. PDF structure same as normal statement (not blank/error) [PM confirmed: PDF with 'no records' display] |

**Test Data:** Account: 710001 (no statement data for this date); Date: 2026-07-10

---

#### TC-220349 · Statement Patch & Regeneration - Validation - Upload CSV - verify Date format validation across remaining Statement Tables
**Priority:** High | **Automation:** Unset

**Description:** Verify Date columns reject invalid format (must be yyyy-mm-dd) for Open Position, Deposit/Withdrawal, Statement Summary, Interest Rate — supplements TC which only tested Settled Position

**Prerequisites:**
- Tenant selected
- User has full privileges

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Select Statement Table = 'Open Position', prepare CSV with Date = '16-08-2026' (invalid format dd-mm-yyyy) | - |
| 2 | Click [Choose file] and select file | 1. Snackbar error: 'File is not supported' 2. Table not populated [Date must be yyyy-mm-dd format] |
| 3 | Fix Date = '2026-08-16' (correct format), upload again | 1. File accepted 2. Date displays correctly in table |
| 4 | Select Statement Table = 'Deposit/Withdrawal', prepare CSV with invalid Date format | - |
| 5 | Upload file | 1. Snackbar error: 'File is not supported' [Deposit/Withdrawal Date validation consistent] |
| 6 | Select Statement Table = 'Statement Summary' (Daily), prepare CSV with invalid Date format | - |
| 7 | Upload file | 1. Snackbar error: 'File is not supported' [Statement Summary Date validation consistent] |
| 8 | Select Statement Table = 'Interest Rate', prepare CSV with invalid Date format | - |
| 9 | Upload file | 1. Snackbar error: 'File is not supported' [Interest Rate Date validation consistent] [Confirms: Date format validation (yyyy-mm-dd) is enforced across ALL Statement Tables that support CSV upload] |

**Test Data:** File: invalid_date_op.csv (Date 16-08-2026); File: valid_date_op.csv (Date 2026-08-16); File: invalid_date_dw.csv (Date 08/16/2026); File: invalid_date_ss.csv (Date 2026/08/16); File: invalid_date_ir.csv (Date August 16, 2026)

---

#### TC-220350 · Statement Patch & Regeneration - Validation - Upload CSV - verify duplicate rows in same file rejected (same Account ID + Order Ref)
**Priority:** High | **Automation:** Unset

**Description:** Verify CSV file with duplicate rows (same Account ID + Order Ref appearing twice in the SAME file) is rejected with appropriate error message

**Prerequisites:**
- Tenant selected (tinshing)
- Statement Table = Settled Position

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Prepare CSV file with 2 identical rows: Row 1 Account ID 710001/Order Ref ORD-001/Item XAUUSD; Row 2 exact duplicate | - |
| 2 | Click [Choose file] and select the duplicate CSV file | 1. Snackbar error: 'File is not supported' 2. Statement Data Table NOT populated 3. File rejected — user must fix duplicates before re-uploading |
| 3 | Prepare CSV with 2 rows having same Account ID + Order Ref but DIFFERENT other fields (Row 1 P/L=500, Row 2 P/L=750, same key) | - |
| 4 | Click [Choose file] and select this file | 1. Snackbar error: 'File is not supported' 2. Table NOT populated [Duplicate key = duplicate row, regardless of other field values] |
| 5 | Prepare valid CSV with unique Account ID + Order Ref combinations (710001/ORD-001, 710001/ORD-002, 710002/ORD-001) | - |
| 6 | Click [Choose file] and select valid file | 1. File accepted 2. Table populates with 3 rows 3. All data displayed correctly [Same Account ID with different Order Ref = valid; Same Order Ref with different Account ID = valid] |
| 7 | Test with Open Position/other tables — prepare CSV with duplicate Account ID + Order Ref | 1. Same behavior: Snackbar error, file rejected [Duplicate key validation applies across all Statement Tables that use Order Ref] |

**Test Data:** File: duplicate_rows.csv; File: duplicate_key_diff_values.csv; File: unique_keys.csv; File: duplicate_op.csv (Open Position)

---

#### TC-220351 · Statement Patch & Regeneration - Calculation - CSV Upload dates exactly on DST transition boundary
**Priority:** High | **Automation:** Unset

**Description:** Verify behavior when CSV contains a record dated exactly on DST transition day (e.g. 2026-03-08 in US where clocks spring forward at 2 AM)

**Prerequisites:**
- Tenant selected
- Statement Table = Settled Position, Type = Daily
- DST transition day: 2026-03-08 (US) where 2:00 AM becomes 3:00 AM
- CSV prepared with Date = 2026-03-08

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Upload CSV with Date = 2026-03-08 (DST transition day) | 1. File accepted, table shows record 2. No error about ambiguous/invalid date [System must handle DST transition day gracefully] |
| 2 | With DST toggle ON, click [Patch] | 1. Patch processes successfully 2. No error about 'non-existent time' or 'ambiguous time' [Note: DST transition day has 23 hours (spring forward) — system must handle correctly] |
| 3 | Regenerate and download PDF for 2026-03-08 | 1. PDF generated successfully 2. Statement covers the correct 23-hour trading day 3. No data loss or duplicate due to clock skip |

**Test Data:** File: dst_boundary.csv (Date: 2026-03-08, DST transition day)

---

#### TC-220352 · Statement Patch & Regeneration - Filter - Datetime Range - verify Search accepts very short range (few hours within same day)
**Priority:** High | **Automation:** Unset

**Description:** Verify that Search accepts datetime range significantly shorter than 1 day (e.g., 3 hours) — no minimum range enforced. Confirm: Search returns only records within narrow window; Patch does not delete data outside range; Regenerate PDF still includes full day data

**Prerequisites:**
- Tenant selected
- Statement Table = Settled Position (Daily)
- Account has records throughout the day: 01:00, 05:00, 09:00, 12:00, 15:00, 20:00
- DST toggle set appropriately

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Set Start Datetime = 2026-08-26 09:00:00 | 1. Start datetime accepted 2. No minimum range validation error |
| 2 | Set End Datetime = 2026-08-26 12:00:00 (only 3 hours range) | 1. End datetime accepted 2. Range = 3 hours (09:00 → 12:00) 3. [Search] button: ENABLED 4. No 'range too short' validation error |
| 3 | Click [Search] | 1. Search executes successfully 2. Statement Data Table shows ONLY records within 09:00-12:00 window: 09:00 visible, 12:00 visible (boundary), 01:00/05:00/15:00/20:00 NOT visible 3. Table may show fewer records than full-day query 4. [Export data] button: ENABLED |
| 4 | Edit one record in the narrow result set | 1. Edit mode works normally 2. Changes saved to working table |
| 5 | Click [Patch] | 1. Patch executes for records in narrow range only 2. Records OUTSIDE 09:00-12:00 (01:00, 05:00, 15:00, 20:00) are NOT affected in DB 3. Patch mechanism: update by Order Ref (not bulk delete/insert by range) 4. Patch History shows new entry |
| 6 | Query full day range (22:00 prev day → 21:00 same day) to verify data integrity | 1. Full day query returns ALL records: 01:00/05:00 original values (untouched), 09:00/12:00 patched values (edited), 15:00/20:00 original values (untouched) 2. No data loss from narrow-range Patch [Confirms: Patch by Order Ref, not by date range deletion] |
| 7 | Click [Regenerate] from Patch History for the narrow-range patch entry | 1. Regenerate uses FULL DAY data from DB (not limited to 09:00-12:00 patch range) 2. Generated PDF includes all records for the statement date 3. PDF reflects: original values for records outside patch range, updated values for records within patch range [Confirms: Regenerate scope = full day/month, independent of Search range] |

**Test Data:** Account: 710001; Change Close Price value; Start: 2026-08-25 22:00:00; End: 2026-08-26 21:00:00

---

### Role Management (3 cases)

#### TC-191126 · Role Management - Permissions - Statement Patch privileges - verify checkboxes display in New/Edit Role form
**Priority:** High | **Automation:** Unset

**Description:** Verify that Statement Patch privilege checkboxes display correctly under Troubleshoot Platform section in New/Edit Role form

**Prerequisites:**
- User logged in as Root Admin

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Navigate to Role Management > Click [New Role] or [Edit] on existing role | Navigation complete |
| 2 | Scroll to 'Troubleshoot Platform' section in privilege list | Section found |
| 3 | Observe the privilege checkboxes | 1. 'Troubleshoot Platform' section displays in privilege list 2. Two checkboxes display: - 'View Patch and Regenerate Statement Page' — unchecked by default - 'Patch and Regenerate Statement' — unchecked by default |

**Test Data:** None

---

#### TC-191127 · Role Management - Permissions - View privilege - verify enabling and saving role
**Priority:** High | **Automation:** Unset

**Description:** Verify that Root Admin can enable 'View Patch and Regenerate Statement Page' privilege and save role successfully

**Prerequisites:**
- User logged in as Root Admin

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Navigate to Role Management > Click [New Role] | Navigation complete |
| 2 | Fill in Role Name: 'Statement Patch View Only Role', Description: 'View only access' | Form filled |
| 3 | Check 'View Patch and Regenerate Statement Page' checkbox only (NOT 'Patch and Regenerate Statement') | Checkbox checked |
| 4 | Click [SAVE] button | Save triggered |
| 5 | Observe result and verify role in listing | 1. Role saved successfully 2. Role created with 'View Patch and Regenerate Statement Page' enabled 3. Role appears in Role listing |

**Test Data:** Role Name: Statement Patch View Only Role

---

#### TC-191128 · Role Management - Permissions - Full Access privilege - verify enabling and saving role
**Priority:** High | **Automation:** Unset

**Description:** Verify that Root Admin can enable 'Patch and Regenerate Statement' privilege (full access) and save role successfully

**Prerequisites:**
- User logged in as Root Admin

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Navigate to Role Management > Click [New Role] | Navigation complete |
| 2 | Fill in Role Name: 'Statement Patch Full Access Role', Description: 'Full access to patch and regenerate' | Form filled |
| 3 | Check 'Patch and Regenerate Statement' checkboxes | 1. both 'View Patch and Regenerate Statement Page' AND 'Patch and Regenerate Statement' checkboxes are selected |
| 4 | Uncheck 'View Patch and Regenerate Statement Page' checkboxes | 1. both 'View Patch and Regenerate Statement Page' AND 'Patch and Regenerate Statement' checkboxes are DEselected |
| 5 | Check 'Patch and Regenerate Statement' checkboxes | 1. both 'View Patch and Regenerate Statement Page' AND 'Patch and Regenerate Statement' checkboxes are selected |
| 6 | Click [SAVE] button | Save triggered |
| 7 | Observe result and verify role in listing | 1. Role saved successfully 2. Role created with both privileges enabled 3. Role appears in Role listing |

**Test Data:** Role Name: Statement Patch Full Access Role

---

### User Management (3 cases)

#### TC-191129 · User Management - Permissions - View Only user - verify page access and restricted actions
**Priority:** High | **Automation:** Unset

**Description:** Verify that user with only 'View' privilege can access page but cannot perform patch actions

**Prerequisites:**
- User 'viewonlyuser' exists
- Role with only 'View Patch and Regenerate Statement Page' assigned

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Login as 'viewonlyuser' | Login complete |
| 2 | Navigate to Troubleshoot Platform > Statement Patch & Regeneration | Navigation complete |
| 3 | Observe page access and all interactive elements | 1. Page loads successfully with all 4 sections visible 2. Section 1 (Select Tenant): Dropdown selectable to user download file in Section 4 3. Section 2 (Statement Data Query & Patch): disable 4. Section 3 (Preview Statement): disable 5. Section 4 (Patch History): Table displays (read-only), [Refresh] and [Download] enabled |

**Test Data:** None

---

#### TC-191130 · User Management - Permissions - Full Access user - verify all actions enabled
**Priority:** High | **Automation:** Unset

**Description:** Verify that user with 'Patch and Regenerate Statement' privilege can perform all actions

**Prerequisites:**
- User 'fullaccessuser' exists
- Role with both 'View' and 'Patch and Regenerate Statement' privileges assigned

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Login as 'fullaccessuser' | Login complete |
| 2 | Navigate to Troubleshoot Platform > Statement Patch & Regeneration | Navigation complete |
| 3 | Observe all interactive elements are enabled | 1. Page loads with all sections 2. Section 1: Dropdown enabled 3. Section 2: [Choose File], [Upload], Delete icons all enabled 4. Section 3: [Preview], [Patch & Regenerate] all enabled 5. Section 4: Full access to table, filters, refresh |

**Test Data:** None

---

#### TC-191131 · User Management - Permissions - No privilege user - verify page inaccessible
**Priority:** High | **Automation:** Unset

**Description:** Verify that user without any Statement Patch privilege cannot access the page

**Prerequisites:**
- User 'nopermuser' exists
- No Statement Patch privileges assigned

**Steps:**

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Login as 'nopermuser' | Login complete |
| 2 | Observe navigation menu for 'Troubleshoot Platform' | 1. 'Statement Patch & Regeneration' sub-menu is hidden |
| 3 | Attempt to access page via direct URL | 1. Page content not accessible |

**Test Data:** None

---

## Collection Notes

- **Total cases collected:** 120
- **Total cases failed:** 0 (TC-220320 initial fetch failed, re-fetched 2026-09-09)
- **Folders queried:** 3 (4829, 4830, 4831)
- **Groups identified:** 3
- **All cases state:** Review, Approved, or Deprecated
- **All cases priority:** High
- **Automation status:** All Unset (100%)

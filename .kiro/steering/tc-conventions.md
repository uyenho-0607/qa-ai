---
inclusion: manual
---

# Test Case Conventions

## Name Test Cases

Format: `[Module] – [Sub-module] – [Feature] – [Field/Action] – [Condition]`

Approved Module, Sub-module, and Feature names: `.kiro/domain/tc-naming-ref.md`. Copy them verbatim — that file is the authority for spelling.

```bash
awk -v m="{Module}" '/^#/{p = ($0 == "### " m)} p' .kiro/domain/tc-naming-ref.md
```

- Include Module and Condition in every name.
- Include Sub-module when the reference lists sub-modules for that Module (e.g. Action Required > Balance Approvals, Configuration > Currency Pairs). Omit when it lists none (e.g. Login, OTC, Members).
- Omit Feature and Field/Action when not applicable.
- Write Field/Action free-form, specific to the TC.
- Separate segments with an en dash (`–`).
- Use no abbreviations unless commonly understood in the project.
- Reflect the expected outcome in the name.

## Write Test Scenarios

Start every Test Scenario with "Verify that". Omit all UI action verbs (base and gerund form): tap, click, enter, type, select, fill, submit, scroll, open, clear, navigate. Use state nouns instead: "an empty field", "a future date", "a country unavailable for registration".

Keep scenarios to one condition and one outcome. Put exact error strings, field values, and label text in Expected Result.

```
✔ Verify that deposit with a valid amount is processed successfully.
✔ Verify that the minimum deposit validation is enforced.
✔ Verify that the Country of Residence field opens a country selection side sheet.
✗ Users can navigate to Funds > Deposit and enter an amount and click Submit.
✗ Verify login and deposit flow works end to end.
✗ Verify that the Country of Residence field opens a full-height side sheet with an alphabetical country list and a search bar.
```

## Write Steps

Exclude login from Steps. Exception: include login only when the TC requires logging into multiple platforms.

Never write a standalone observation step. The Expected Result column *is* the observation — a step that only looks at the outcome adds nothing.

```
✔ 3. Tap the "Continue" button.
✗ 3. Tap the "Continue" button.
  4. Observe the result.
```

Merge/split decisions, step atomicity, and step scope: `tc-design-guide.md`.

## Write Expected Results

State all verifiable checkpoints as a bullet list. Each bullet names an exact message, value, or state change — one checkpoint per bullet. Write each checkpoint in its own bullet rather than joining them with semicolons, commas, or "and". Omit vague outcomes, implementation details, and alternatives joined by "or".


For a field whose form gates its submit CTA, an empty-required or invalid-input TC asserts **both** halves: the inline error message *and* that the CTA remains disabled. Both are observable, so both belong in the oracle. Because validation fires inline, such a TC has no "Tap [CTA]" step — the last step is entering the value.

```
✔ - "Please enter an email." is displayed below the Email field.
  - The "Continue" button remains disabled.
✗ - "Please enter an email." is displayed below the Email field.
```

For selection screens, the ER names each option's descriptive text, subtitle, or caption alongside its label — visibility alone is not an assertion. Spec silent on the text → mark `needs-clarification`.

```
✔ "Personal" account type option is visible with its description label (e.g. "For individual traders").
✗ "Personal" account type option is visible on screen.
```

## Write Pre-requisites

The first item must be a screen/location anchor: `On the [Screen Name] screen`. Include flow context in parentheses when the screen is part of a named flow or step sequence. Anchor selection rules: `tc-design-guide.md`.

Sub-states (side sheets, modals, overlays) go after the parent screen anchor, separated by `;`.

```
✔ On the Personal Details screen (3rd step of onboarding flow).
✔ On the Personal Details screen (3rd step of onboarding flow); Country of Residence side sheet is open; no country has been tapped/selected.
✗ Country of Residence side sheet is open; no country has been tapped/selected.
```

## Avoid Duplicates

Before writing a TC, check the plan's `covered by` column and any existing TCs in scope. Merge rules: `tc-design-guide.md`.

## Assign Platform and Role

- Place platform in **Configuration** — must match an existing Testmo config name. OTC configs: `Admin BO`, `Android app`, `iOS app`. For other projects, fetch via `testmo_list_configs`.
- **Configuration = where the Expected Results (assertions) are checked**, not where the setup or trigger steps happen. If a TC sets up data on mobile but all assertions are verified in the Backoffice, use `Admin BO` only.
- When assertions span multiple platforms within the same TC, list all applicable configs (e.g. `Android app; iOS app; Admin BO`).
- Place user role in **Pre-requisites** (e.g. "Logged in as Admin").
- Name the role without listing credentials.

## Consolidate Cross-Platform TCs

Consolidate TCs with identical scenarios on Desktop and Mobile into one TC. State platform-specific expected results within the same TC.

## Output Format

Block format, field set, file header, ER bullet prefixes, and block separator: `.kiro/skills/generate-tcs/TEMPLATE.md`.

## Order Export Columns

Column order for every export — CSV, Google Sheet, Testmo — is the `COLUMNS` list in `scripts/format_tc_sheet.py`:

```bash
sed -n '/^COLUMNS = \[/,/^]/p' scripts/format_tc_sheet.py
```

Test ID format: `{KEY}_TC-[nn]` — `{KEY}` is the ticket key, taken from the file's `**Story:**` header. `scripts/format_tc_sheet.py` matches any project key; it warns when a block's key differs from the `**Story:**` key.

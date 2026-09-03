# TC Design Guide

Structural decisions: merge/split, step scope, pre-req anchoring, shared flows, modules.
Format → `tc-conventions.md`. What to test → `tc-scenario-guide.md`.

## Merge or Split TCs

- Merge scenarios sharing the same steps that differ only in assertion.
- Merge a scenario whose assertion a later scenario already passes through.
- Merge a linear progression (type → clear → type again) into one TC with inline test-data variants.
- Split when a distinct business rule drives the outcome.
- Cover same-rule input variants in one TC carrying multiple test-data values.
- Merge identical scenarios across configs into one TC, config-specific results stated in the ER (e.g. `Android app; iOS app`).

```
✔ Split: DOB under-18 (age rule) vs DOB in future (date-validity rule).
✗ Split: `Sin` vs `SingGaPore` — same rule, same outcome.
```

## Scope Steps

- Trace one action sequence to one outcome per TC.
- Write one action per step.
- List a repeated-value step once, variants in Test Data.
- Name the action only; leave screen names, validation rules, and setup to Pre-requisites and Test Data.

```
✔ 1. Tap the DOB field.  2. Set the wheel picker to 22/08/2008.  3. Tap "Done".
✗ 1. Open the date picker and set a date and tap Done.
✔ 3. Enter Country of Residence and Date of Birth. Tap "Continue".
✗ 3. On the Personal Details screen, select a valid Country of Residence (e.g. Singapore)…
```

## Anchor Pre-requisites

- Anchor to the screen the tester occupies before step 1.
- Verify flow order against the AC/BR list in `tasks/{KEY}/base/jira.md` before writing the anchor.
- State prior field values, selections, and completed steps in Pre-requisites.

```
✔ On the Email OTP Verification screen (Step 4); Send Code has been tapped.
✗ On the Account Created screen   (Account Created is Step 7)
```

## Reuse Shared Flows

- Reference existing TCs by id with status `covered by [existing TC name]` when the ticket marks steps as reusing an existing flow — name the source ticket in the Refs column, not Status.
- Import existing TCs as-is from the source when absent from the target sheet or Testmo.
- Write shared-flow TCs generically — no account-type or path-specific language.
- State both account-type variants in the ER for BO TCs citing account-specific fields.

```
✔ On the Setup Email Address screen (Step 4 of onboarding flow).
✗ On the Setup Email Address screen (Step 4 of Personal onboarding flow).
✔ Member Type matches the onboarding path (Personal or Business).
```

## Assign Modules

- Assign a TC to the module of the screen it verifies, not the ticket's feature area.
- Assign BO-facing TCs to the BO module (e.g. `Members`), regardless of triggering flow.

---
name: learn-domain
description: >
  Self-learning domain knowledge updater. Browses live app or reads codebase/tickets
  to discover new locators, business rules, or UI patterns, then updates the
  .claude/domain/ knowledge base files. Use when user says "learn domain",
  "/learn-domain", "update domain knowledge", or "capture learnings".
---

## Behavior

When invoked:

1. **Determine scope:**
   - If user specifies a topic (e.g., "learn domain for Funds page"), focus ONLY on that area
   - If no topic specified, capture learnings from the CURRENT conversation session — what new info was discovered during work that isn't yet in `.claude/domain/`

2. **Discovery methods (pick based on scope):**
   - **Browse live app:** Navigate to the relevant page, take snapshot, extract locators/form fields/table columns
   - **Read codebase:** Search POM files, API modules, enum definitions for the area
   - **Fetch Jira ticket:** If a specific ticket has business rules not yet captured
   - **From session context:** Review what was learned during current bug verification, test writing, or browser interaction

3. **Update knowledge base:**
   - Read the existing relevant `.claude/domain/` file first
   - Append or correct ONLY what's new — never delete existing correct info
   - If a file doesn't exist for the area, create one following the existing format
   - Every update must include WHAT was added and WHY (source: "learned from OMS-XXX" or "captured from live DOM 2026-07-03")

4. **Report:**
   - List exactly what files were updated
   - Show the diff (what was added/changed)
   - Confirm no existing correct info was lost

## Rules

- NEVER overwrite correct existing data
- ALWAYS read the target file before writing
- If uncertain whether info is correct, ASK the user before writing
- Prefer specificity: exact locator selectors > generic descriptions
- For locators: capture element type, placeholder/text, enabled/disabled state, parent context
- For business rules: include the source ticket ID
- For flows: include step-by-step with expected outcomes

## Target Files

| What was learned           | Write to                                                                                                                           |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| New form field locators    | `locators-symbols.md`, `locators-market.md`, or `locators-accounts.md`                                                             |
| New page discovered        | Create `locators-{page}.md`                                                                                                        |
| Business rule / validation | `market-module.md`, `accounts-module.md`, `order-lifecycle.md`, `positions.md`, `risk-and-margin.md`, or `settings-auth-module.md` |
| API endpoint               | `api-map.md`                                                                                                                       |
| Interaction flow recipe    | `flows.md`                                                                                                                         |
| New module/page URL        | `modules.md`                                                                                                                       |
| EMS behavior               | `ems-trader.md`                                                                                                                    |

## Examples

User: "learn domain for the Funds page"
→ Browse /admin/accounts/funds, capture Deposit/Withdrawal modal locators, update `locators-accounts.md`

User: "learn domain" (after verifying OMS-1112)
→ Check what was discovered: CP Closed Volume field shows "3.0/5.0" format after fix. Update `positions.md` if the rule wasn't already captured.

User: "learn domain for Reports"
→ Browse /admin/reports/account-statements, capture filter locators + table structure, create `locators-reports.md` if it doesn't exist.

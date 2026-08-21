# UI Discovery Rules

What must be discovered, and what the output must contain. Consulted during Phase 2 to verify completeness.

---

## What to Discover

### Workflow
- Business capability provided by the page
- Complete user journey: entry point → all termination points
- Every meaningful business action (create, update, delete, approve, reject, deposit, withdraw, open, modify, close)
- Every business state for each entity (account, order, position, etc.)
- Every state transition and its trigger
- Navigational actions only if they affect business state

### Business Information
- Every business value displayed to the user
- Every location where each value appears (checkpoint map)
- How values change across the workflow (data relationships)
- Conditional visibility: when each value appears, disappears, or is disabled
- Dynamic content that updates without user action (live prices, profit, notifications)
- Refresh behaviour: automatic, manual, real-time, requires navigation
- Empty states where no business data exists

### Rules and Constraints
- All validation rules: required fields, min/max, format restrictions, business restrictions
- All error states and how the UI communicates them (toast, dialog, inline message, banner)
- All business rules visible through the UI: trading restrictions, market state, balance limits
- Negative paths: what must NOT exist or must NOT be accessible per role and state

### Permissions and Platforms
- Controls and information that are visible, hidden, disabled, or restricted per user role
- Permission differences across all applicable roles
- Behaviour differences across supported platforms
- Platform differences documented — never assumed consistent

---

## Completeness Checklist

Before marking a page as complete:

- [ ] Business capability is identified
- [ ] Complete user workflow is mapped
- [ ] All business values are in the Checkpoint Map
- [ ] All business actions are documented
- [ ] All business states and transitions are identified
- [ ] Conditional visibility rules are observed
- [ ] All validation rules are recorded
- [ ] All error behaviours are documented
- [ ] Empty states are identified
- [ ] Negative paths are documented per role and state
- [ ] Cross-module relationships are mapped
- [ ] Permission differences are documented
- [ ] Screenshot exists for each distinct page state

---

## Flow File Quality Rules

- Every field listed must have observed constraints — not assumed from the label
- Validation rules must come from live observation — not inferred from requirements
- Capture Points must list every action that triggers UI state change
- Locators must be verified from the live DOM — not copied from memory or guessed

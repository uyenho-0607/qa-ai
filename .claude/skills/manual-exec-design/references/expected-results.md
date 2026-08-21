# Expected Result Strengthening

**Shallow checking is the default failure. A TC's written expected result is the floor, not the target — if it changed on screen, verify it. Strengthen every expected result before it enters the exec file.**

---

## Depth levels

Design depth in here — the run asserts exactly what the exec file states, and nothing more.

Assign every TC the levels it needs. Most TCs need 1 + 2.

**Level 1 — Primary outcome** (the thing the TC is named after)
- Toast/notification with the exact message text
- Modal opened / closed
- Element enabled, disabled, visible, or removed

**Level 2 — Everything else that changed on the same screen**
- Table → row added/removed/updated, row count, sort position, cell values
- Form → fields cleared or retained, buttons re-enabled, validation messages gone
- Status → badge text and colour, dependent columns
- Counters, totals, timestamps → recalculated to the expected value
- The return destination — did it stay on the modal or go back to the table?

**Level 3 — Ripple beyond the screen**
- Audit log entry written, with correct actor and action
- Change on page A reflected on page B
- Another session or role sees the correct state
- Network: the expected API call fired — or, on invalid input, fired **not at all**

---

## Ask of every TC

1. Does it verify all specified behaviour, or only the happy path?
2. Are implicit constraints checked? A list of allowed items implies no others are allowed.
3. Is every assertion tied to an objective DOM fact — testid, attribute, text, API status — rather
   than a visual assumption?
4. What else on this screen changed that the TC does not mention?

Treat a one-bullet expected result as shallow unless the TC verifies a single static state.

---

## Common gaps

**Example — Admin Users → Reset Password (OMS-1120):**

| TC kind | Shallow (as written) | Deep (strengthened) |
|---------|---------------------|---------------------|
| Menu / list | "Reset Password option is present" | Action menu contains **exactly 3** items in order: View → Reset Password → Delete |
| Form state | "Password field is greyed out" | Field carries `readonly`, shows the masked value, and cannot be focused for edit |
| Validation | "Error message appears" | Error text matches exactly **and** no `PUT /admin-users/{id}/password` call fires |
| Success | "Success toast shows" | Toast text matches, Edit modal stays open, password field still `readonly`, table row unchanged |
| Negative | "Modal closes on Cancel" | Modal removed from DOM, no API call, table still shows the original row |
| Session | "User is not logged out" | Primary session still authenticated after reset, second context unaffected, no redirect to login |
| Audit | "Reset is logged" | Audit Log has a new row: correct actor, action `Reset Password`, timestamp within the run window |

---

## Priority

- Requirement beats test case on all conflicts.
- Live app beats domain file on all UI facts.
- Send a TC back to classification when its assertion cannot be tied to a DOM fact.
- Never weaken an expected result to make it assertable.

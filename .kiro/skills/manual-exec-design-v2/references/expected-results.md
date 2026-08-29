# Expected Result Strengthening

**Shallow checking is the default failure. A TC's written expected result is the floor, not the target — if it
changed on screen, verify it.** Design the depth here: the run asserts exactly what `exec-v2.md` states, and
nothing more.

Applies to **Tier 2 and Tier 3** TCs, and to any Tier-1 TC recon had to defer. A Tier-1 TC already verified at
recon is finished.

## Source the oracle before deriving it

Where `.kiro/domain/flows.md` or the platform's domain file already records the observed value — the exact
error text, the validation rule, the column set, the state transition — **quote it and cite the file.** Those
were captured live by `ui-discovery`, which is required to record *"observed constraints, not assumed from the
label"* and *"validation rules from live observation, not inferred from requirements"*.

Derive from scratch only what no file records. That is the difference between writing an expected result and
inventing one.

## Depth levels

Assign every TC the levels it needs, each as its own numbered expected result. Most need 1 + 2.

**Level 1 — Primary outcome** (the thing the TC is named after)
- Toast / notification with the exact message text
- Modal opened or closed
- Element enabled, disabled, visible, or removed

**Level 2 — Everything else that changed on the same screen**
- Table → row added / removed / updated, row count, sort position, cell values
- Form → fields cleared or retained, buttons re-enabled, validation messages gone
- Status → badge text and colour, dependent columns
- Counters, totals, timestamps → recalculated to the expected value
- The return destination — did it stay on the modal or go back to the table?

**Level 3 — Ripple beyond the screen**
- Audit log entry written, with the correct actor and action
- A change on screen A reflected on screen B
- Another session or role sees the correct state
- Network: the expected call fired — or, on invalid input, fired **not at all**

A Level 3 network assertion is directly observable only where the platform pack lists network among its
§ Observables. Where it does not, the pack states what the assertion becomes there.

## Ask of every TC

1. Does it verify all specified behaviour, or only the happy path?
2. Are implicit constraints checked? A list of allowed items implies no others are allowed.
3. Is every assertion tied to an observable its pack lists, rather than to a visual assumption?
4. What else on this screen changed that the TC does not mention?

Treat a single expected result as shallow unless the TC verifies a single static state.

## Shallow against deep

| TC kind | Shallow, as written | Deep, strengthened |
|---------|---------------------|--------------------|
| Menu / list | "Reset Password option is present" | Action menu contains **exactly 3** items in order: View → Reset Password → Delete |
| Validation | "Error message appears" | Error text matches exactly **and** no `PUT /admin-users/{id}/password` call fires |
| Success | "Success toast shows" | Toast text matches, Edit modal stays open, password field still `readonly`, table row unchanged |
| Negative | "Modal closes on Cancel" | Modal removed from DOM, no API call, table still shows the original row |
| Audit | "Reset is logged" | Audit Log has a new row: correct actor, action `Reset Password`, timestamp within the run window |

## Where an assertion will not hold

- Send a TC back to classification when its assertion cannot be tied to an observable its platform produces.
- Never weaken an expected result to make it assertable.

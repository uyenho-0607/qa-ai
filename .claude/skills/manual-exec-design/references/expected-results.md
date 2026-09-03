# Expected Result Strengthening

## Domain Oracle Sourcing

- Check `.claude/domain/flows.md` or platform domain files **before** writing expected results.
- Quote and cite domain files directly for live-observed error text, validation rules, column sets, and state transitions.
- Derive assertions from scratch **only** if no domain file records the observed value.

## Depth levels

Assign every TC the levels it needs, each as its own numbered expected result. Most need 1 + 2.

**Level 1 — Primary outcome**
- Toast / notification with the exact message text
- Modal opened or closed
- Element enabled, disabled, visible, or removed

**Level 2 — On-Screen Side Effects**
- Table → row added / removed / updated, row count, sort position, cell values
- Form → fields cleared or retained, buttons re-enabled, validation messages gone
- Status → badge text and colour, dependent columns
- Counters, totals, timestamps → recalculated to the expected value
- The return destination — did it stay on the modal or go back to the table?

**Level 3 — System & Ripple Effects**
- Audit log entry written, with the correct actor and action
- A change on screen A reflected on screen B
- Another session or role sees the correct state
- Network: the expected call fired — or, on invalid input, fired **not at all**
  - *Note*: Network call assertions require network support under pack § Observables.

## Evaluation Checklist
Before finalizing, ask:
1. Are negative flows and implicit constraints checked (e.g., explicit list implies others are forbidden)?
2. Is every assertion bound directly to a pack observable?
3. Are all secondary on-screen state changes captured?
*Rule: A single expected result is considered shallow unless the TC verifies a single static state*

## Shallow vs. Deep Guidance

| Scenario | Shallow (Do Not Use) | Deep (Required Standard) |
|---|---|---|
| **Menu / List** | "Reset Password option is present" | Action menu contains **exactly 3** items in order: `View` → `Reset Password` → `Delete` |
| **Validation** | "Error message appears" | Exact error text matches **AND** no `PUT /admin-users/{id}/password` call fires |
| **Success** | "Success toast shows" | Toast text matches, modal stays open, password field remains `readonly`, table row unchanged |
| **Negative** | "Modal closes on Cancel" | Modal removed from DOM, no API call fired, table retains original row state |
| **Audit** | "Reset is logged" | Audit Log adds row: correct actor, action `Reset Password`, valid timestamp |

## Non-Assertable Handling

- If an assertion cannot be tied to a pack observable, send the TC back to Phase 2 classification (Skipped or dropped platform).
- **NEVER** weaken an expected result to make it assertable.

---
name: ui-discovery
description: Map business behaviour of a live web application — workflows, values, validation rules, permissions, state transitions — then save findings as a Checkpoint Map and domain flow file. Use when user says "explore this page", "discover the UI", "map this feature", "build checkpoint map".
---

# UI Discovery

Outputs: **Checkpoint Map** (where values appear) + **flow file** (behaviour, validation, transitions).

Rules: `.kiro/steering/playwright-rule.md`, `.kiro/skills/ui-discovery/rules.md`, `.kiro/steering/reasoning-standards.md`

## Hard Rule
**Every phase is mandatory. No phase may be skipped, shortened, or rationalized away.** Even if POM exists or pages seem familiar — always discover live state.

## Inputs
- Target feature/capability
- Target app: OTC Back Office (`BO_URL`) — roles: Maker / Checker / Admin
- Flow file path (default: `.kiro/domain/flows.md`)
- Read `project-config.md` for URLs/credentials

## Flow

### Phase 1 — Page Identification → GATE
List all pages/tabs/panels/modals where feature data appears.
For each: app name, navigation path, expected business value.

### Phase 2 — Live Exploration → GATE
For each page:

**2.1 Navigate & capture**
Navigate → waitForLoadState + waitForTimeout(500) → extract data-testids + values → screenshot

**2.2 Map business values (Checkpoint Map)**
| # | App | Page | Navigation | Field Label | data-testid | Live Value | Format |

**2.3 Map interactions**
Perform actions → capture state after each → record: what changed, new fields, validation

**2.4 Map validation**
Test boundaries (min, max, empty, invalid) → capture error messages, enable/disable, constraints

**2.5 Map permissions**
If multiple roles: switch and repeat 2.1-2.2

### Phase 3 — Cross-App Consistency → GATE
Verify same value across all apps. Flag inconsistencies.

### Phase 4 — Outputs
1. **Checkpoint Map** — consolidated table
2. **Flow file** — save to path:
   ```
   # {Feature} — Flow
   ## Navigation
   ## Fields and Behaviour
   ## Validation Rules
   ## State Transitions
   ## Capture Points
   ## Locators
   ```
3. **Locator cache** — update `.kiro/locator-cache.json`
4. **Confidence Report** — one row per dimension:

   ```
   Discovery — {Feature}    [n] pages · [n] checkpoints · [n] validation rules

   | Dimension | Observed | Confidence | Gap |
   |---|---|---|---|
   | Page coverage | [n]/[n] pages from Phase 1 explored | high/med/low | [what was not reached] |
   | Checkpoint map | [n] values across [n] locations | | |
   | Validation rules | [n] rules observed live | | |
   | Permission mapping | [n]/[n] roles exercised | | |
   | Cross-app consistency | [n] values compared, [n] mismatches | | |
   ```

   Confidence is `high` only where every row came from a live observation. Anything inferred from a label, a requirement, or a previous session is `low` — name it in Gap.

   `.kiro/domain/flows.md` and `.kiro/locator-cache.json` do not exist until this phase writes them; create them rather than reporting them missing.

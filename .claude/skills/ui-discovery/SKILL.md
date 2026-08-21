---
name: ui-discovery
description: Map business behaviour of a live web application — workflows, values, validation rules, permissions, state transitions — then save findings as a Checkpoint Map and domain flow file. Use when user says "explore this page", "discover the UI", "map this feature", "build checkpoint map".
---

# UI Discovery

Outputs: **Checkpoint Map** (where values appear) + **flow file** (behaviour, validation, transitions).

Rules: `.claude/steering/playwright-rule.md`, `.claude/skills/ui-discovery/rules.md`, `.claude/steering/reasoning-standards.md`, `.claude/steering/deliverable-reporting.md`

## Hard Rule
**Every phase is mandatory. No phase may be skipped, shortened, or rationalized away.** Even if POM exists or pages seem familiar — always discover live state.

## Inputs
- Target feature/capability
- Target apps: OMS Admin / EMS Trader / EMS Backoffice
- Flow file path (default: `.claude/domain/flows.md`)
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
3. **Locator cache** — update `.claude/locator-cache.json`
4. **Confidence Report** — dimensions: page coverage, checkpoint map, validation rules, permission mapping, cross-app consistency

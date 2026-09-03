---
name: ui-discovery
description: Map a live web app's business behaviour into a Checkpoint Map and domain flow file. Use on "map this feature", "discover the UI".
---

# UI Discovery

Outputs: **Checkpoint Map** (where values appear) + **flow file** (behaviour, validation, transitions).

## Hard Rule
Even if POM exists or pages seem familiar — always discover live state.

## Phase 0 — Load rules
Read `.kiro/steering/playwright-rule.md` and `.kiro/skills/ui-discovery/rules.md` before the first navigation.
Read the pack named by the target's row in `project-config.md` § Platforms (§ Targets, § Cached locators,
§ Stack quirks). For the `bo` target this resolves to `.kiro/platforms/bo.md`.

## Inputs
- Target feature/capability
- Target app: the platform under discovery — its row in `project-config.md` § Platforms names the pack; the
  pack names its domain file and roles. **Name no app here.**
- Flow file path (default: `.kiro/domain/flows.md`)
- URLs, credentials and roles: `project-config.md` § Environment and § Platforms — extract, never whole:
  `awk '/^## /{p=/^## (Environment|Platforms)$/} p' .kiro/steering/project-config.md`

## Flow

### Phase 1 — Page Identification → GATE
List all pages/tabs/panels/modals where feature data appears.
For each: app name (omit when fewer than two web-group platforms are enabled per project-config.md §
Platforms), navigation path, expected business value.

### Phase 2 — Live Exploration → GATE
For each page:

**2.1 Navigate & capture**
Navigate → settle per `.kiro/steering/playwright-rule.md` § Timeouts → scan data-testids per § DOM-First Rule → extract
values → capture screenshot via the `capture-evidence` skill (`dest: reports/discovery/{feature}/`, `stem:`
page/state name)

**2.2 Map business values (Checkpoint Map)**
Per `rules.md` § Business Information.

| # | App | Page | Navigation | Field Label | data-testid | Live Value | Format |

App column applies only when more than one platform is in scope (see Phase 1) — omit otherwise.

**2.3 Map interactions**
Per `rules.md` § Workflow.

**2.4 Map validation**
Per `rules.md` § Rules and Constraints.

**2.5 Map permissions**
Per `rules.md` § Permissions and Platforms. If multiple roles: switch and repeat 2.1-2.4.

### Phase 3 — Cross-App Consistency → GATE
Skip when fewer than two web-group platforms are enabled (project-config.md § Platforms). Otherwise: verify
same value across all apps; flag inconsistencies.

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
4. **Screenshots** — file paths returned by `capture-evidence` in step 2.1, under `reports/discovery/{feature}/`
5. **Confidence Report** — one row per dimension:

   ```
   Discovery — {Feature}    [n] pages · [n] checkpoints · [n] validation rules

   | Dimension | Observed | Confidence | Gap |
   |---|---|---|---|
   | Page coverage | [n]/[n] pages from Phase 1 explored | high/med/low | [what was not reached] |
   | Checkpoint map | [n] values across [n] locations | high/med/low | [gap] |
   | Validation rules | [n] rules observed live | high/med/low | [gap] |
   | Permission mapping | [n]/[n] roles exercised | high/med/low | [gap] |
   | Cross-app consistency (only when >1 platform in scope) | [n] values compared, [n] mismatches | high/med/low | [gap] |
   ```

   Confidence is `high` only where every row came from a live observation. Anything inferred from a label, a requirement, or a previous session is `low` — name it in Gap.

   Merge findings into the flow file and the locator cache — never overwrite either; create a file only when it genuinely does not exist.

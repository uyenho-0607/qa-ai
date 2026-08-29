---
name: manual-exec-design
description: Build exec.md, the manual SIT execution plan, from jira.md and tc.md — coverage, triage, recon, expected results, evidence, waves. Use on "design exec plan", /manual-exec-design, or when manual-exec-run finds no exec.md.
---

## Contract

TASK: `tasks/{KEY}/`

- **Args:** `{KEY}` [, `platforms={ids}`] [, `evidence={normal|screenshot}`] [, `annotations={yes|no}`] [, `no-gate`] — ids from `project-config.md` § Platforms
- **Reads:** 
  `.kiro/steering/project-config.md` § Environment, § Platforms, § Producers — extract, never whole:
  `awk '/^## /{p=/^## (Environment|Platforms|Producers)$/} p' .kiro/steering/project-config.md`
  the platform packs § Platforms names — § Targets, § Observables and § Stack quirks by heading
  `.kiro/steering/tc-exec-classify.md`
  `.kiro/locator-cache.json`
  `.kiro/domain/flows.md` or the platform domain files
  `TASK/base/jira.md`
  `TASK/base/tc.md`
  `TASK/base/figma/figma-snapshot.md`
  `TASK/base/figma/figma-screenshots/*.png`
- **Writes:** 
  `TASK/exec/exec.md`
  Recon screenshots to `TASK/exec/recon/`
  Tier-1 evidence to `TASK/exec/evidence/`
  Verified locators to `.kiro/locator-cache.json`
  `TASK/exec/report.md` — deleted when overwriting an existing `exec.md`
- **Guardrails:** Execute all phases strictly in sequence. Name no platform directly; derive all platform facts from `project-config.md` § Platforms. If `exec.md` exists, ask to overwrite or abort.

## Phase 1 — Input & Cover ACs

- Read enabled platforms (id, label, group, pack) from `project-config.md` § Platforms. Do not load packs yet.
- `jira.md` or `tc.md` missing → STOP and name the producer per `project-config.md` § Producers (`/jira-retriever {KEY}` with `save`, or `/collect-testmo-cases {KEY}` with `save` / `/collect-gsheet-cases`). This skill never runs a producer itself.
- Read:
   - `TASK/base/jira.md`: Extract module and number criteria (`AC-1`, `AC-2`, …).
   - `TASK/base/tc.md`: Load TCs (case IDs, titles, steps, expected results).
   - `TASK/base/figma/figma-snapshot.md` & `figma-screenshots/`: if not exists and `jira.md` carries a `## Figma Links` entry → dispatch the `figma-fetcher` agent with that URL and `{KEY}`. No Agent tool in context → disclose_context("figma-retriever") FULLY instead. Then recheck and extract exact button labels, field placeholders, and visible text strings.

- Cross-reference Figma against TCs:
  - Labels/copy differ from `jira.md` → use Figma as truth; log discrepancy for the Phase 7 gate.
  - Visual states (empty, disabled, error, loading) not covered by any TC → author Added TC.

- Map every AC to its covering TCs.
  - Covered → record covering TCs.
  - Uncovered → author an Added Coverage TC (no case ID).
  - Out of scope → record the owning ticket.

Done when: ACs are numbered (`AC-1`+), sheet TCs cataloged, Figma states cross-referenced, 100% of ACs are mapped to a TC or out-of-scope ticket, and the cross-platform flag is recorded (enabled only if ≥2 groups are active).

## Phase 2 — Classify

Read `.kiro/steering/tc-exec-classify.md` and apply it. Move non-addressable TCs to Skipped with reasons. For remaining TCs:
- **Platforms:** Find active platforms capable of executing the TC (or apply `platforms=` override). Skip TCs with zero enabled platforms. Assign platform pairs for cross-platform flows.
- **Tiers:**
  - **Tier 1:** Static UI facts (presence, labels, column ordering of settled screens). Verified at Phase 3. When in doubt, Tier 2.
  - **Tier 2:** Dynamic behaviors, actions, transitions, and state validations.
  - **Tier 3:** Cross-screen, cross-session, or cross-platform ripple changes.
- **Preflight Data:** Derive the Preflight Data list — accounts, records, references each included TC requires — from TC preconditions.

Done when: Every TC has a status (Skipped/Included), Tier (1–3), and platform or pair assigned. Preflight Data list is derived. Active platform set for recon is stated (platforms in play and any excluded, with reason).

## Phase 3 — Recon & Verify Tier 1

- Prompt for `evidence` (`normal` | `screenshot`, default: `normal`) and `annotations` (`yes` | `no`, default: `no`) via `AskUserQuestion` unless set in args.
- Load active platform packs.
- Verify the Phase 2 Preflight Data items against the live env. Create missing items using active platform domain knowledge (confirm if creation steps unclear).
- Record state changes under `Environment changes made`. Log failed creation as gate blockers.
- **Delegate the live-UI pass.** Dispatch one `recon-scout` agent per active platform, **in sequence** — one browser and one device mean two scouts on the same target fight over the session. Pass `{KEY}`, that platform's id, and the Tier-1 TC ids to verify. Each scout follows `references/recon.md` and returns its full Return block.
- No Agent tool in context → follow `references/recon.md` yourself, per platform, and produce the same Return block.
- Act on what comes back:
   - Record platform identities and build versions from each scout's `Build` line (`fixVersion`, app footer/about menu, or `unknown`).
   - Take each scout's `Verified` lines as the Tier-1 results, with the screenshot paths it names.
   - Merge every returned locator patch into `.kiro/locator-cache.json` yourself.
   - Move `Unverified` items with an unresolved target to `Unaddressable Elements` (or reclassify to `Skipped`). Defer unreachable Tier-1 TCs to execution waves.
   - Merge the scout's `Visual findings` into `## Visual Findings` and its `Environment changes made` into `## Execution Context` — not just the locator patch.

Done when: Parameters are set, preflight data/builds are logged, reachable Tier-1 TCs are visually verified, and unaddressable elements are handled.

## Phase 4 — Strengthen Expected Results & Plan Evidence

- Follow `references/expected-results.md` for Tier 2/3 and deferred Tier 1 TCs. Tie every assertion to pack observables. Record platform differences for the final gate. Process in batches of 10 if TCs > 20.
- Plan capture paths per `references/evidence.md` for all remaining included TCs based on the evidence mode and annotations resolved in Phase 3.

Done when: Tier 2/3 TCs have multi-depth, numbered expected results tied to pack observables. Evidence mode/annotations stored and capture paths planned per TC/platform.

## Phase 5 — Order the Waves

Group remaining TCs into execution waves:
- Place dependent TCs immediately after prerequisites. Separate TCs modifying the same data into distinct waves.
- Limit each wave to 1 platform group (or 1 pair for cross-platform) and max 1 VIDEO group.
- Define `Platforms`, `Reset` (lightest required reset), and `Sessions` (≥2 for cross-platform) per wave.

Done when: All remaining TCs are assigned to waves with `Platforms`, `Reset`, and `Sessions`.

## Phase 6 — Write `exec.md`

- Generate `TASK/exec/exec.md` using `TEMPLATE.md`.
- Overwriting an existing `exec.md` → delete any existing `TASK/exec/report.md`; it belongs to the plan being replaced.
- Write `evidence` mode and `annotations` setting into `exec.md` § Execution Context.
- Embed Phase 3 Tier-1 results inline (omit summary tables).
- Ask user whether passed Tier-1 TCs should be re-verified; if yes, move selected items to Wave 1 as `⏳ PENDING`.

Done when: `exec.md` matches `TEMPLATE.md`, Tier-1 results and evidence context are written, and re-verification prompt is sent.

## Phase 7 — Check, then GATE

- Run:

```bash
# Count included TC blocks
grep -c '^### TC-' tasks/{KEY}/exec/exec.md
# Count Skipped TCs (Skipped section only)
awk '/^## Skipped/{p=1;next} /^## /{p=0} p' tasks/{KEY}/exec/exec.md | grep -c '^| TC-'
# Count Added Coverage TCs (Added Coverage section only)
awk '/^## Added Coverage/{p=1;next} /^## /{p=0} p' tasks/{KEY}/exec/exec.md | grep -c '^| TC-'
# Verify header entries and expected result lines per TC
grep -n '^### TC-\|^- .* · [⏳✅❌🚫]' tasks/{KEY}/exec/exec.md
```
- Verify every tc.md TC appears exactly once as included or Skipped: (### TC- count) + (Skipped count) − (Added count) = tc.md total.
- Verify every included TC has exactly one result line per final platform/pair.
- Present:
 1. Blockers
 2. Tier-1 results
 3. Added Coverage
 4. Differences
 5. Open questions
 
Stop for user approval. `no-gate`: auto-approve.
Done when: Count check passes ((### TC-) + Skipped − Added = tc.md total) and user approves gate summary.

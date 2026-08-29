# Recon & Tier-1 Verification

Executed in Phase 3. Strictly scoped to screens, sheets, and modals named in included TC steps. **Recon confirms and verifies; it does not explore.**

---

## 1. Targeted Context Loading

- Locators: `jq '.["{section}"].screens.{screen}' .kiro/locator-cache.json`, one screen at a time —
  `{section}` is the pack's `Cached locators:` value, above its first heading.
- Read only the relevant sections of `.kiro/domain/flows.md` or platform domain files.

---

## 2. Recon & Target Validation Rules

- **Cache Delta Handling**: Visit each screen once per platform. If live target matches cache, reuse it. If live target differs, update `.kiro/locator-cache.json` and add to Target Inventory. Live app beats domain file on all UI facts.
- **Rule 1 — Disambiguation**: Target strings matching `Occ > 1` on a screen MUST include a container and row index disambiguator.
- **Rule 2 — Scroll Rule**: Scroll each container to its bottom before declaring any element absent or unaddressable.
- **Rule 3 — Container Naming**: Every inventory row and assertion must specify its `Screen` and `Container`.
- **Unaddressable Elements**: If an element has no `id=`, `desc=`, or unique `text=`, record it under `Unaddressable Elements` with blocking TCs and pack fix.

---

## 3. Tier-1 Verification Procedure

For every reachable Tier-1 TC:

1. **Capture Screenshot First**: Capture screen state prior to any DOM interaction.
2. **Read Back the Frame**: Confirm every expected result is visible in the captured frame, then confirm the DOM attributes agree. The frame is what passes Tier 1; the DOM corroborates.
3. **Save Evidence**: Invoke `/capture-evidence targets={platform} type=screenshot stem={stem} dest=tasks/{KEY}/exec/evidence/ annotation={annotations}`.
4. **Record Status**:
   - ✅ **PASSED**: Write the result line per `../TEMPLATE.md` § Field Rules → Result Format. Exclude from execution waves.
   - ❌ **FAILED**: Record failure finding. Retain TC in wave for run repro count (`2/2` or `1/2`).
   - ⏳ **DEFERRED**: If screen is unreachable, mark deferred with reason and schedule into execution wave.

---

## 4. Visual Defect Sweep

- Capture 1 frame per distinct visual state (default view, opened drawer/modal, empty state). Shared states share 1 frame.
- Inspect for clipping, overlap, text truncation, misalignment, or broken layout.
- Log defect findings to `## Visual Findings`.

---

## 5. Output Captures, Discrepancies & State Logging

- **Recon Screenshots**: Save to `tasks/{KEY}/exec/recon/{screen}_{platform_id}.png` **ONLY** if screen contradicts cache, shows a new state, or fails a TC.
- **Cross-Platform Discrepancies**: Log any element, column, or behavior present on one platform but absent on another.
- **TC vs. Live Disagreements**: Log any mismatch between a TC's written expected result and what the live UI displays (e.g., changed label, missing field).
- **State Changes**: Record all environment data/state changes caused by recon in `## Execution Context` under `Environment changes made` (or write `none`).

---

## Done When

- Every screen named in TC steps is visited on every active platform; every reachable Tier-1 TC is visually
  verified and DOM-corroborated with evidence; every unreachable one is deferred with a reason.
- Every rule in §§ 1–5 above is applied and its outputs recorded.
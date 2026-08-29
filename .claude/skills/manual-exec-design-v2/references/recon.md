# Recon

Two jobs in one pass over the screens the plan needs:

1. **Confirm the plan is executable** — every element addressable, every target string unambiguous.
2. **Verify every reachable Tier-1 TC** — and capture its evidence on the spot.

Scoped to the screens, tabs, sheets and modals the included TCs' steps name, on every platform in play, and no
others. Add a screen only where a TC step reaches it.

Recon **confirms and verifies; it does not explore.** It never tests boundaries it was not given a TC for,
never switches roles to look around, and never changes data it does not have to. To learn a feature nobody has
mapped yet, run `ui-discovery` first and let recon read its output.

Follow the pack for each platform in play.

## Order

1. **Read what is already known**, scoped to the screens in hand — **never a file in full**:
   `jq '.["{cache key}"].screens.{screen}' .claude/locator-cache.json` one key at a time, then **only the
   sections** of `.claude/domain/flows.md` and the platform's domain file that name those screens. Reading a
   whole domain file is a bug: they run to 19 KB each.

2. **Confirm the deltas only.** Visit each screen once per platform. A cached target the live screen returns
   needs no rescan and no inventory row — it is used from the cache. A cached target the screen contradicts is
   a stale-cache finding: correct `.claude/locator-cache.json`, add the row, carry it to the gate.

3. **Verify every Tier-1 TC whose screen is now settled.** For each TC:

   a. **Take a screenshot first.** Before touching the DOM, capture the screen as it stands.
   b. **Read the image back.** Look at the screenshot — not the DOM tree — and confirm every expected result
      is visible in the frame. What the human eye sees in the image is the verification. The DOM then
      provides the objective fact the result line carries; it corroborates the image, it does not replace it.
   c. A DOM assertion that cannot be corroborated by what is visible in the screenshot is not a Tier-1 pass.
      Reclassify the TC to Tier-2 or defer it — never write a pass based on DOM alone.
   d. **Capture the screenshot as evidence** under the stem `references/evidence.md` § Stem defines.
   e. **Write the result:** `verified at recon, build {x}` — the screenshot is what verified it, the DOM
      confirmed it.

   Outcomes:
   - ✅ passed → **final.** The run does not re-execute it.
   - ❌ failed → record it, and leave the TC in a wave so the run can produce a repro count. A bug needs
     `2/2` or `1/2`, and one observation cannot give it.
   - screen not reachable — the data does not exist yet → mark the TC deferred with the reason and plan it
     into a wave like any Tier-2 TC. Never guess the result.

4. **Sweep each distinct UI state per platform for visual defects.** One frame per distinct visual state on
   that screen — the default list view, each drawer opened, each modal opened, each empty state. Several TCs
   that share the same visual state share one sweep frame; a screen with no openable panels needs one frame.
   Read each frame for clipping, overlap, truncation, misalignment and broken layout. Findings go to Visual
   Findings and are raised at the gate.

5. **Record the elements the TC steps touch** — but only the rows recon resolved live, or that match more than
   one node. An element the cache already has correct is used from there, not copied into the plan. An element
   with no `id=`, no `desc=` and no unique `text=` goes to Unaddressable Elements with the TCs it blocks and
   the fix its pack states.

6. **Screenshot the deltas.** Save to `tasks/{KEY}/exec/recon/{screen}_{platform id}.png` only where the screen
   contradicted the cache, showed something new, or disagreed with a TC. A screen that matched what was
   already known needs no recon screenshot — the sweep frame from step 4 already covers it.

7. **Compare every TC expected result against what the screen shows.** Record each disagreement.

8. **Record any state recon changed.**

## The three rules that decide whether the plan is safe

1. **Occurrences.** Record how many nodes each target string matches on its screen. Above 1, the row carries a
   disambiguator — the container plus a row index — or the target is not usable. A target matching many nodes
   is how a run passes against the wrong element.
2. **Scroll before declaring absence.** Scroll each container to its end before recording an element as absent
   or unaddressable. A viewport listing is not a screen inventory.
3. **Name the container.** Every inventory row, and every assertion built on it, names its screen and the
   container the element lives in.

## Done when

- Every screen an included TC's steps name has been visited on every platform in play.
- Every Tier-1 TC is verified, or deferred with the reason its screen was unreachable.
- Every verified Tier-1 TC carries evidence and a result noting the build it was verified against.
- Every Tier-1 TC's screenshot has been read back and visually confirmed before the result was written.
- Every distinct screen has been swept once per platform, and findings recorded.
- Every element those steps touch is addressable from the cache or carries an inventory row.
- Every target string with occurrences above 1 carries a disambiguator.
- Every container was scrolled to its end before any absence was recorded.
- Every unaddressable element lists the TCs it blocks and its fix.
- Every element or behaviour present on one platform and absent on another is recorded.
- Every TC-expected-vs-live disagreement is recorded.
- Every stale cache entry is corrected in `.claude/locator-cache.json`.
- The state recon changed is recorded, or recorded as `none`.

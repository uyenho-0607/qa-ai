# Recon

Scoped verification of what the plan needs: the screens, tabs, sheets and modals the included TCs' steps name,
on every selected target, and no others. Add a screen only where a TC step reaches it.

Recon confirms and records; it does not explore. It never tests boundaries, never switches roles to look
around, and never mutates data it does not have to. To learn a feature nobody has mapped yet, run
`ui-discovery` first and let recon read its output.

Follow the surface pack for each surface in play.

## Order

1. **Read what is already known**, scoped to the screens in hand — never a file in full:
   `jq '.["{surface key}"].screens.{screen}' .claude/locator-cache.json` one key at a time, then the sections
   of `.claude/domain/flows.md` and the surface's domain file that name those screens. Most are already
   recorded.
2. **Confirm the deltas only.** Visit each screen once per target. A cached target the live screen returns
   needs no rescan — its source is `locator-cache`. A cached target the screen contradicts is a stale-cache
   finding: correct the entry in `.claude/locator-cache.json`, and carry it to the gate.
3. **Screenshot each screen per target**, to `tasks/{KEY}/exec/recon/{screen}_{target}.png`.
4. **Record every element the TC steps touch** into Target Inventory — screen, container, element, target
   string, occurrences, per-target presence, source. An element with no `id=`, no `desc=` and no unique
   `text=` goes to Unaddressable Elements instead, with the TCs it blocks and the fix its pack states.
5. **Compare every TC expected result against what the screen shows.** Record each disagreement.
6. **Record any state the recon changed.**

## The three rules that decide whether the plan is safe

1. **Occurrences.** Record how many nodes each target string matches on its screen. Above 1, the Target
   Inventory cell carries a disambiguator — the container plus a row index — or the target is not usable. A
   target matching many nodes is how a run passes against the wrong element.
2. **Scroll before declaring absence.** Scroll each container to its end before recording an element as absent
   or unaddressable. A viewport listing is not a screen inventory.
3. **Name the container.** Every inventory row, and every assertion built on it, names its screen and the
   container the element lives in.

## Done when

- Every screen an included TC's steps name has been visited and screenshotted on every selected target.
- Every element those steps touch carries a target string, an occurrences count, and a per-target mark.
- Every target string with occurrences above 1 carries a disambiguator.
- Every container was scrolled to its end before any absence was recorded.
- Every unaddressable element lists the TCs it blocks and its fix.
- Every element or behaviour present on one target and absent on another is recorded.
- Every TC-expected-vs-live disagreement is recorded.
- Every stale cache entry is corrected in `.claude/locator-cache.json`.
- The state recon changed is recorded, or recorded as `none`.

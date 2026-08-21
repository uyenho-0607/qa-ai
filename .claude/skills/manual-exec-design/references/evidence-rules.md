# Evidence Rules

**VIDEO is the default. SCREENSHOT is the exception.**

---

## Evidence type

Assign SCREENSHOT **only when ALL hold:**

- The assertion is a single static state, visible in one frame
- Nothing appears, disappears, or changes during the assertion
- No timing, ordering, or "nothing happened" claim is involved
- One frame proves the expected result on its own

Assign VIDEO **whenever ANY holds:**

- A toast, banner, or transient element appears
- An element disappears — modal closes, row removed, error clears
- The flow spans steps: menu → click → modal → submit
- Validation updates live as the user types
- A toggle changes rendered content (eye icon, expand, switch)
- The assertion is negative — "no X happened", "session not kicked", "no API call"
- Behaviour spans two contexts or sessions

Capture cost is never a reason to assign SCREENSHOT.

---

## Grouping

**Group into one recording when ALL hold:**

- Same precondition and starting state
- Sequential with no teardown between them
- Each assertion moment is visually distinct within the recording
- Failure in one TC does not make another's assertion ambiguous

**Group into one frame when ALL hold:**

- Every checkpoint is visible at the same instant, without scrolling
- All checkpoints hold in the same state, on the same page
- The labels do not cover the elements they mark

Prefer a frame over a recording wherever both qualify.

**Split when ANY holds:**

- Different preconditions or starting state
- Teardown required between TCs
- Failure in one TC would corrupt shared evidence for another

---

## Naming

All paths under `evidence/{KEY}/`. One grammar, no variants:

```
TC_{id}_{id}…_{slug}[_f{N}][_primary|_session].{png|mp4}
```

- `{id}` — every member's case ID, in group order, zero-padded, without the `TC-` prefix.
- List every member ID; never collapse a range, never use the group ID.
- Source each ID from `tc.md`.
- `{slug}` — 2–4 words, snake_case, taken from the group's Rationale.
- `_f{N}` — frame index, and only where a SCREENSHOT group needs more than one frame.
- `_primary` / `_session` — multi-context capture, one file per context.
- Extension follows the evidence type: `.png` for SCREENSHOT, `.mp4` for VIDEO.
- Maximum 100 characters. Shorten the slug, never the ID list.

| Group | File |
|---|---|
| G2 = TC-06..TC-09, SCREENSHOT | `TC_06_07_08_09_filter_options.png` |
| Solo TC-12, VIDEO, two contexts | `TC_12_session_not_kicked_primary.mp4`, `TC_12_session_not_kicked_session.mp4` |
| G1 = TC-01, TC-02, SCREENSHOT, 2 frames | `TC_01_02_action_menu_f1.png`, `TC_01_02_action_menu_f2.png` |

---

## Labels

Every screenshot, and every assertion moment in a video, carries a label overlay.

Format: `{TC-ID} | {what is being verified}`

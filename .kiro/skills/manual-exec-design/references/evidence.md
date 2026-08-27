# Evidence — planning

Design decides what evidence exists and what each file is called; `manual-exec-run` captures it, per
`.kiro/steering/capture-mechanics.md`. Nothing here is read at run time.

| Mode | What it produces |
|---|---|
| `normal` | VIDEO or SCREENSHOT per group, the type decided from what the scenario needs |
| `screenshot` | one frame per checkpoint, no grouping |

## Stem

The plan carries the **stem**. The run appends `_{target}` and the extension, one file per entry in the TC's
`**Tgt:**`, so a plan table never grows a column per target.

```
recording:   TC_{ids}_{slug}
frame:       TC_{ids}_c{N}[_c{M}…]_{slug}
```

- `{ids}` — the plan's `TC-NN` numbers, zero-padded, without the `TC-` prefix, in group order, joined by `_`.
  List every member; never collapse a range, never substitute the group ID.
- `{slug}` — 2–4 words, snake_case, from the group's Rationale or the checkpoint's assertion.
- `c{N}` — the checkpoint id from the TC's `**Exp:**` bullet. A shared frame lists every checkpoint it proves.

Keep the whole name inside 100 characters once the run has added `_{target}` and the extension — shorten the
slug, never the ids.

---

# `normal` mode

## Evidence type

**VIDEO is the default. SCREENSHOT is the exception.** Any VIDEO trigger outranks every SCREENSHOT condition.

Assign SCREENSHOT only when ALL hold:

- The assertion is a single static state, visible in one frame
- Nothing appears, disappears, or changes during the assertion
- No timing, ordering, or "nothing happened" claim is involved
- One frame proves the expected result on its own

Assign VIDEO whenever ANY holds:

- A toast, snackbar, banner, or transient element appears
- An element disappears — modal or sheet closes, row removed, error clears
- The flow spans steps: menu → click → modal → submit
- Validation updates live as the user types
- A toggle changes rendered content
- The assertion is negative — "no X happened", "session not dropped"
- The flow crosses a screen transition or a navigation push
- Behaviour spans two contexts or sessions

Capture cost is never a reason to assign SCREENSHOT.

## Grouping

Group into one recording when ALL hold:

- Same surface, same precondition, same starting screen
- Sequential with no teardown between them
- Each assertion moment is distinct within the recording
- Failure in one TC does not make another's assertion ambiguous

Split when ANY holds:

- Different precondition or starting screen
- Teardown required between TCs
- Failure in one TC would corrupt shared evidence for another

Prefer a frame over a recording wherever both qualify. A TC that groups with nothing still gets its own
one-TC group row — there is no separate solo grammar.

**A `bo+app` group captures once per surface**, into files distinguished by their target suffix: the pair
produces `…_android` and `…_bo`, both evidence for the same TC. `**Cap:**` names the moment on each side, and
the two captures must show the hand-off in order. A paired TC is the one case where a surface change is not a
group split.

## Sharing a frame

One frame may prove several checkpoints, of one TC or of several. Share it when ALL hold:

- Every checkpoint it covers is visible at the same instant, without scrolling
- All of them hold in the same state, on the same screen
- Each is attributable from the capture — the in-frame label where the target's pack declares the overlay
  available, the sidecar where it does not
- Failure in one does not make another's assertion ambiguous

Split into separate frames when any of those fails.

## What the plan carries

The Evidence Groups table — group, TCs, type, stem, rationale.

---

# `screenshot` mode

Everything is a frame: enough of them to prove every `**Exp:**` checkpoint, per entry in the TC's `**Tgt:**`
— one each where their states differ, one shared per § Sharing a frame where they hold at the same instant.

## What a frame cannot prove

A frame cannot show a transient element, a disappearance, an ordering, or a negative. List every checkpoint
of those kinds as a **video escape hatch**: that TC gets a VIDEO per § Evidence type above, or the gate
accepts the weaker frame explicitly. An unprovable checkpoint captured as a frame, unflagged, is a false pass.

## What the plan carries

The Checkpoint Evidence table — checkpoint ids, stem, frame count per target, and any escape hatch. No
Evidence Groups table.

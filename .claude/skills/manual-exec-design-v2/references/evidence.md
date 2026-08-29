# Evidence — planning

Design decides what evidence exists and what each file is called; `manual-exec-run-v2` captures it, per
`.claude/steering/capture-mechanics.md`. Nothing here is read at run time.

A Tier-1 TC verified at recon already has its evidence, captured at the moment it was asserted. Plan nothing
further for it.

| Mode | What it produces |
|---|---|
| `normal` | VIDEO or SCREENSHOT per group, the type decided from what the scenario needs |
| `screenshot` | one frame per expected result, no grouping |

**The modes differ in cost far more than they look.** A `normal` recording is verified with one `ffprobe`
call. A `screenshot` frame is verified against a file check, and only read back where it matters — see
`manual-exec-run-v2` § Verifying a capture. Quantify both at Phase 6 before asking.

## Stem

The plan carries the **stem**. The run appends `_{platform id}` and the extension, one file per platform the
TC runs on, so a plan table never grows a column per platform.

```
recording:   TC_{ids}_{slug}
frame:       TC_{ids}_c{N}[_c{M}…]_{slug}
```

- `{ids}` — the plan's `TC-NN` numbers, zero-padded, without the `TC-` prefix, in group order, joined by `_`.
  List every member; never collapse a range, never substitute the group id.
- `{slug}` — 2–4 words, snake_case, from the group's reason or the assertion.
- `c{N}` — the number of the entry in the TC's **Expected** list. A shared frame lists every entry it proves.

Keep the whole name inside 100 characters once the run has added `_{platform id}` and the extension — shorten
the slug, never the ids.

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
- Behaviour spans two sessions

Capture cost is never a reason to assign SCREENSHOT.

## Grouping

Group into one recording when ALL hold:

- Same platform, same precondition, same starting screen
- Sequential with no teardown between them
- Each assertion moment is distinct within the recording
- Failure in one TC does not make another's assertion ambiguous

Split when ANY holds:

- Different precondition or starting screen
- Teardown required between TCs
- Failure in one TC would corrupt shared evidence for another

Prefer a frame over a recording wherever both qualify. A TC that groups with nothing still gets its own
one-TC group row — there is no separate solo grammar.

*Cross-platform:* a paired group captures once per side, into files distinguished by their platform suffix.
Both are evidence for the same TC, the capture moments name the moment on each side, and the two must show the
hand-off in order. A paired TC is the one case where a platform change is not a group split.

## Sharing a frame

One frame may prove several expected results, of one TC or of several. Share it when ALL hold:

- Every entry it covers is visible at the same instant, without scrolling
- All of them hold in the same state, on the same screen
- Each is attributable from the capture — the in-frame label where the platform's pack declares the overlay
  available, the file name where it does not
- Failure in one does not make another's assertion ambiguous

Split into separate frames when any of those fails.

## What the plan carries

The Evidence § Groups table — group, TCs, type, stem, why.

---

# `screenshot` mode

Everything is a frame: enough to prove every entry in each TC's **Expected** list, per platform — one each
where their states differ, one shared per § Sharing a frame where they hold at the same instant.

## What a frame cannot prove

A frame cannot show a transient element, a disappearance, an ordering, or a negative. List every such entry
in the `Video needed for` column: that TC gets a VIDEO per § Evidence type above, or the gate accepts the
weaker frame explicitly. An unprovable expected result captured as a frame, unflagged, is a false pass.

This column is not a formality. It is what keeps the run's cheap frame verification safe — a frame that could
never prove its assertion is caught here, at design, not by reading every image later.

## What the plan carries

The Evidence § Frames table — expected-result numbers, stem, frame count per platform, and what needs video.
No Groups table.

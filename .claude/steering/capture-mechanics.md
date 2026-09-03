# Capture Mechanics

Audience: every skill that captures evidence — `manual-exec-run` during a wave, `capture-evidence` for a
one-off bug or verification, `evidence-auditor` when it audits a run's captures. This file owns the rules that
hold for **every** capture. The caller owns the stem of the file name.

Each target's **Group** comes from § Platforms in the caller's own extract — never re-read it here. Load this
file plus the row for that group, and no other row:

| Group | Driver rule | Capture mechanics |
|---|---|---|
| `web` | `.claude/steering/playwright-rule.md` | `.claude/steering/capture-web.md` |
| `device` | `.claude/steering/maestro-rule.md` | `.claude/steering/capture-device.md` |

Substitute `{KEY}`, `{stem}`, `{target}`, `{dest}`, `{N}` and `{name}` with real values before running any
snippet — they are placeholders, not code.

## Invariants

- A capture never decides a result. One that failed is recorded; the result stands on its assertion.
- A name is derived, never invented, and never changed afterwards. A file showing the wrong thing is
  re-captured, never renamed.
- A capture is verified against its assertion before the caller moves on.
- Never capture the same state twice. Two identical frames under two names is duplicated evidence, not
  coverage.

## File name

Everything lands under `tasks/{KEY}/exec/evidence/`. Never the repo root, never a bare filename — a bare name
resolves against the MCP server's own working directory.

```
{stem}_{target}.{png|mp4}
```

- `{stem}` — the caller's. An exec run takes it from the plan, per
  `.claude/skills/manual-exec-design/references/evidence.md` § File Naming (Stem); `report-bug` passes
  `{KEY}_bug_{N}` and `verify-bug` passes `{KEY}_verify_{N}`.
- `{target}` — the platform `Id`, verbatim from § Platforms. Always present, so a multi-target capture is never
  ambiguous. One file per target, including the two sides of a cross-platform pair.
- `.png` for a frame, `.mp4` for a recording.
- Maximum 100 characters. Shorten the stem's words, never its ids.

## When to capture

| Evidence mode | When the capture happens |
|---|---|
| `normal` | a replay pass after the group has been tested — test first, record second |
| `screenshot` | inline, at the assertion moment |

**A recording is a replay, not the test.** Test the group first, then replay every step inside one recording
context at a steady pace. Restore the starting precondition only where the test changed state; a read-only flow
replays as-is. Enter the recording knowing every step and every target string — resolving anything inside a
recording context puts the agent's own latency into the video, and that reads as a slow app.

## Label

`{TC-ID} | c{N} | {what is being verified}` — a one-off capture uses the caller's label instead.

Whether the label goes in the frame is the target's own answer — read § Label overlay in its platform pack.
**Available**: the label is injected into the frame, clear of the elements it marks, and one frame may carry
several labelled checkpoints. **Not available**: the capture is attributed by its file name alone.

## No sidecars

**Never write a `.md` beside a capture.** `tasks/{KEY}/exec/evidence/` holds `.png` and `.mp4` files and nothing else.

Never let a fact reach only a capture. The file name attributes it; the caller's own result note is the record
— assertion text, what was observed, the backend check, the elapsed second a failure lands on in a recording.

## Verify

**Frame** — for transient elements (toast, snackbar, banner, notification — anything that disappears after a
few seconds), read the `.png` back immediately after saving and confirm the element is visible in it. A
transient element may have cleared by the time the file is saved; the read-back catches a blank or
already-dismissed frame before it reaches the report.

For stable, settled screen states (a list row, a drawer field, a status badge), a file-exists and non-zero
check is sufficient — the agent already observed the element before capturing.

**Recording** — confirm the duration covers the whole replay rather than truncating at `timeLimit`, and that
the file is larger than 0 bytes:

```bash
ffprobe -v error -show_entries format=duration,size -of default=nw=1 "tasks/{KEY}/exec/evidence/{name}.mp4"
```

**Per capture type** — the standards an evidence audit applies:

| Capture type | Verification standard |
|---|---|
| Recording | `ffprobe` duration and size check (above). |
| Settled state on a screen already captured this wave | File existence, non-zero size. |
| Every other frame — first view, first frame of a wave, any failed frame or size anomaly | Read the image back: confirm the assertion is visible. |

A capture failing either check is re-captured once. One that still fails is recorded in the caller's notes —
it never changes the result.

---
inclusion: manual
---

# Capture Mechanics

Audience: every skill that captures evidence — `manual-exec-run` during a wave, `capture-evidence` for a
one-off bug or verification. This file owns the rules that hold for **every** capture. The caller owns the
stem of the file name; the driver file owns the calls.

Load this file plus the row for each target in hand, and no other row:

| Target | Driver rule | Capture mechanics |
|---|---|---|
| `bo`, `bo-mv`, `app-web` | `.kiro/steering/playwright-rule.md` | `.kiro/steering/capture-web.md` |
| `ios`, `android` | `.kiro/steering/mobile-mcp-rule.md` | `.kiro/steering/capture-device.md` |

Substitute `{KEY}`, `{stem}`, `{target}`, `{N}` and `{name}` with real values before running any snippet —
they are placeholders, not code.

## Invariants

- A capture never decides a result. One that failed is recorded; the result stands on its assertion.
- A name is derived, never invented, and never changed afterwards. A file showing the wrong thing is
  re-captured, never renamed.
- A capture is verified against its assertion before the caller moves on.
- Never capture the same state twice. Two identical frames under two names is duplicated evidence, not
  coverage.

## File name

Everything lands under `evidence/{KEY}/`. Never the repo root, never a bare filename — a bare name resolves
against the MCP server's own working directory.

```
{stem}_{target}[_f{N}][_a|_b].{png|mp4}
```

- `{stem}` — the caller's. An exec run takes it from the plan; a one-off capture derives it per
  `.kiro/skills/capture-evidence/SKILL.md` § File Naming.
- `{target}` — `bo`, `bo-mv`, `ios`, `android`, `app-web`. Always present, so a multi-target capture is never
  ambiguous. One file per target.
- `_f{N}` — frame index, only where one planned capture needs more than one frame.
- `_a` / `_b` — the two sessions of a two-context capture, in the order the caller names them.
- `.png` for a frame, `.mp4` for a recording.
- Maximum 100 characters. Shorten the stem's words, never its ids.

## When to capture

| Evidence mode | When the capture happens |
|---|---|
| `normal` | a replay pass after the group has been tested — test first, record second |
| `screenshot` | inline, at the assertion moment |

Enter a recording knowing every step and every target string. Resolving anything inside a recording context
puts the agent's own latency into the video.

## Label

`{TC-ID} | c{N} | {what is being verified}` — a one-off capture uses the caller's label instead.

`bo`, `bo-mv` and `app-web` are a DOM and take an injected overlay: the label goes in the frame, clear of the
elements it marks. `ios` and `android` are a native screen and take none: the sidecar carries the same text.

## Sidecar

A `.md` beside the capture, same basename, naming what the capture shows. **Required** for every capture on
`ios` or `android`, and for every capture in `screenshot` mode. Optional elsewhere. Write it immediately
after the capture.

```
Target: {target} · {device identifier or URL} · {OS version} · build {build}
c1 | 00:00–00:07 | {assertion text, verbatim} | observed: {what was seen}
c2 | 00:07–00:14 | {assertion text, verbatim} | observed: {what was seen}
Backend: {METHOD path → status, compared values}
```

- A frame's lines carry no timestamps. A recording's carry one elapsed range per moment, read off the
  recording and never off the plan.
- An exec run keys each line by its checkpoint id. A one-off capture keys it by the caller's label, one line.
- `Backend:` appears only where a backend check ran.

## Verify

**Frame** — read the `.png` back and confirm the asserted element is visible in it.

**Recording** — confirm the duration covers the whole replay rather than truncating at `timeLimit`, and that
the file is larger than 0 bytes:

```bash
ffprobe -v error -show_entries format=duration,size -of default=nw=1 "evidence/{KEY}/{name}.mp4"
```

Both device recorders write H.264 mp4 directly; no conversion runs. Web recordings are `.webm` and are
converted.

A capture failing either check is re-captured once. One that still fails is recorded in the caller's notes —
it never changes the result.

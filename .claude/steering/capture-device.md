# Capture — Device Targets

Mobile mechanics for `capture-mechanics.md`. Driver: `.claude/steering/maestro-rule.md`.

**This file names capabilities, never tools.** Take the tool that provides each one from your own tool list,
and its signature from that tool's own schema.

Two capture capabilities are **not** interchangeable:

| Capability | Use |
|---|---|
| saves a frame **to a path** you give it | evidence |
| returns a frame **inline** to you | perception only — never attach it to a bug, a report, or a Jira comment |

## Screenshot

1. Bring the asserted element into the listing — swipe the container where it is off-screen.
2. Confirm it is in a **current** screen listing, per the driver rule.
3. Save the frame to the absolute path of `{dest}{stem}_{target}.png` — a relative name fails, per
   `maestro-rule.md` § Driver.

## Video — one replay pass per group per target

Replay-pass rule: `capture-mechanics.md` § When to capture. Mobile mechanics for it:

1. **Check for a zombie recording first.** On an Android target, `adb shell pgrep screenrecord` — if a PID is
   returned, a prior recording is still active (e.g. left running after a crash). Kill it with
   `adb shell kill {PID}` before starting fresh. A zombie recording silently blocks the new one. On a target
   with no such probe, stop any running recording before starting one.
2. Start the recorder writing to the absolute path of `{dest}{stem}_{target}.mp4`, with a duration limit above
   the replay's expected length. A recording that hits its limit is truncated. Android's `screenrecord`
   caps at **180s** by default — past that, drive `adb shell screenrecord --time-limit 0` and pull the file.
   Any other per-target recorder cap belongs in that platform's pack § Stack quirks.
3. Replay the group's steps, noting the elapsed second each checkpoint lands on — those seconds go in the
   caller's result note.
4. Stop the recorder, and read back the path, size and duration it reports.

One recording per device at a time. A second start on a recording device is refused, not queued.

- Start the recorder at the decisive step, not at flow start. A long file with the failure in its last seconds
  reads as tester error.
- One filename per attempt. Restarting at the same path overwrites the previous take.

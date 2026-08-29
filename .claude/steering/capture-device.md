# Capture — Device Targets

Targets: `ios`, `android`. Driver: mobile MCP, per `.claude/steering/mobile-mcp-rule.md`.
Naming, labels, timing and verification: `.claude/steering/capture-mechanics.md`. This file is the
mobile mechanics for those rules, and nothing else.

**Read the `mobile_*` schemas with `ToolSearch` before the first call** — take every signature, argument name
and required flag from there, not from this file.

`mobile_save_screenshot` writes evidence. `mobile_take_screenshot` is perception only: never attach its frame
to a bug, a report, or a Jira comment.

## Screenshot

1. Bring the asserted element into the listing — swipe the container where it is off-screen.
2. Confirm it is in `mobile_list_elements_on_screen`.
3. `mobile_save_screenshot` with `output: "tasks/{KEY}/exec/evidence/{name}.png"`.

A native frame carries no injected label, so its file name is what attributes it — derive the name exactly and
never rename it afterwards. Write no `.md` beside it.

## Video — one replay pass per group per target

The recording is a replay, not the test. Test the group first, then replay every step inside one recording at
a steady pace. Restore the starting precondition first only where the test changed state.

1. **Check for a zombie recording first.** Run `adb shell pgrep screenrecord` — if a PID is returned, a prior
   recording is still active (e.g. left running after a crash). Kill it with `adb shell kill {PID}` before
   starting fresh. A zombie recording silently blocks the new one.
2. `mobile_start_screen_recording` with `output: "tasks/{KEY}/exec/evidence/{stem}_{target}.mp4"` and a `timeLimit`
   above the replay's expected length. A recording that hits its limit is truncated. `screenrecord` caps at
   **180s** by default — past that, drive `adb shell screenrecord --time-limit 0` and pull the file.
3. Replay the group's steps, noting the elapsed second each checkpoint lands on — those seconds go in the
   caller's result note, never in a file beside the recording.
4. `mobile_stop_screen_recording` — returns the path, size and duration.

One recording per device at a time. A second start on a recording device is refused, not queued.

- Start the recorder at the decisive step, not at flow start. A long file with the failure in its last seconds
  reads as tester error.
- One filename per attempt. Restarting at the same path overwrites the previous take.

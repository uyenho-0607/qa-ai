# Capture — Device Targets

Targets: `ios`, `android`. Driver: mobile MCP, per `.claude/steering/mobile-mcp-rule.md`.
Naming, labels, sidecars, timing and verification: `.claude/steering/capture-mechanics.md`. This file is the
mobile mechanics for those rules, and nothing else.

**Read the `mobile_*` schemas with `ToolSearch` before the first call** — take every signature, argument name
and required flag from there, not from this file.

`mobile_save_screenshot` writes evidence. `mobile_take_screenshot` is perception only: never attach its frame
to a bug, a report, or a Jira comment.

## Screenshot

1. Bring the asserted element into the listing — swipe the container where it is off-screen.
2. Confirm it is in `mobile_list_elements_on_screen`.
3. `mobile_save_screenshot` with `output: "evidence/{KEY}/{name}.png"`.
4. Write the sidecar. A native frame carries no label, so the sidecar is what attributes it.

## Video — one replay pass per group per target

The recording is a replay, not the test. Test the group first, then replay every step inside one recording at
a steady pace. Restore the starting precondition first only where the test changed state.

1. `mobile_start_screen_recording` with `output: "evidence/{KEY}/{stem}_{target}.mp4"` and a `timeLimit`
   above the replay's expected length. A recording that hits its limit is truncated.
2. Replay the group's steps, noting the elapsed second each checkpoint lands on — those seconds are the
   sidecar's ranges.
3. `mobile_stop_screen_recording` — returns the path, size and duration.

One recording per device at a time. A second start on a recording device is refused, not queued.

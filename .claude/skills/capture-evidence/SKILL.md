---
name: capture-evidence
description: Capture screenshot or video evidence for bug reports and verifications, on any target — Back Office web, the member mobile app, or its web build. Receives structured input, returns file paths. Use when capturing evidence for bugs, verifications, or any time screenshots/video are needed for Jira.
---

# Capture Evidence

Execution skill. Receives structured input, outputs file paths. Decides nothing about the finding — the caller
already knows what it wants shown.

## Pre-Flight

⛔ **FORCE READ:** `.claude/steering/capture-mechanics.md` — it owns the path, the file-name shape, the
label, the sidecar and the verification — then its row for the requested target, and no other row.

The caller names the target; this skill never guesses it. Only Android is verified today — no iOS build
exists yet (`.claude/steering/mobile-mcp-rule.md` § Platform reality). An `ios` request with no device
present returns the unavailability, never a substituted capture.

## Interface

**Input:**
```
type:       screenshot | video
ticket_key: "AO-925"
purpose:    bug | verify
targets:    [bo] | [ios, android] | …        one file per entry

For screenshot:
  element:     "{id= | desc= | text= of the asserted element}"
  label:       "{what is being verified}"
  annotations: [{ element, color: "red"|"green" }]     web targets only
  api_overlay: { url, status, body }                   BE bugs, web targets only

For video:
  steps:          [{ action, element, value?, url? }]
  moment_at_step: N
  label:          "{what is being verified}"

For a backend finding:
  backend: { method, path, status, compared_values }
```

**Output:**
```
file_paths:    ["evidence/AO-925/AO-925_bug_1_android.png"]
sidecar_paths: ["evidence/AO-925/AO-925_bug_1_android.md"]
```

## Stem

```
{ticket_key}_{purpose}_{N}[_v{M}]
```

- `{purpose}` — `bug` or `verify`.
- `{N}` — the caller's index within this ticket, from 1.
- `_v{M}` — re-capture of the same finding, `_v2` onward.

`capture-mechanics.md` § File name adds `_{target}` and the extension, and fixes the path.

An exec run names its files from its plan's stem — `TC_{ids}_{slug}` — and never uses this grammar.

## Flow

Per requested target, in order:

1. **Resolve the target.** Device → `mobile_list_available_devices`, reporting the unavailability rather than
   substituting another. Web → confirm the URL is reachable.
2. **Reach the asserted state.** Navigate or launch, then bring the element into view.
3. **Confirm the element is there** — a fresh DOM query, or `mobile_list_elements_on_screen`. An element that
   resolves at no tier is reported back to the caller unaddressable, together with a capture of the screen it
   sits on.
4. **Capture**, per this target's mechanics file and the `type`.
5. **Write the sidecar and verify the capture**, per `capture-mechanics.md`.
6. **Report the paths.**

## Hard Rules

- Resolve every element from a current query. Never act on a coordinate no listing returned.
- Never re-explore to find an element the caller already named — use what was passed.
- Capture every requested target into its own file. A target that could not run is reported, not skipped
  silently.
- Never auto-delete a file. Wait for confirmation.

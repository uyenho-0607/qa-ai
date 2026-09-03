# Maestro MCP Rules

Governs every Maestro MCP interaction during mobile test execution.

---

## Driver

Mobile execution runs through Maestro: **a flow of inline YAML**, plus a live screen inspection and a
screenshot outside a flow. Take the tools from your own tool list — including its syntax reference, the cheapest fix
when YAML fails to parse. This file names none, so it stays correct when the driver changes. Everything below is the YAML you write and the behaviour it must respect.

**`takeScreenshot` inside YAML requires a full absolute path.** A relative filename fails with a
read-only filesystem error.

```yaml
- takeScreenshot: /absolute/path/to/evidence/tc-01.png
```

---

## One Flow, Many Steps

**The flow is the unit of work, not the step.** Every step whose targets you already hold goes into one
flow — one call runs the lot. Driving mobile one tap per call is the largest avoidable cost on this platform:
each round trip pays full latency to deliver a single `tapOn`.

- **Inspect once per state change, not once per step.** One inspection resolves every target on that screen;
  act on all of them from it.
- An inspection goes stale the moment the screen moves — a scroll, a keyboard, a navigation, an animation.
  Re-inspect **then**, and only then.
- **Split a flow only where you must observe between steps**: an assertion, a state you cannot predict, or a
  checkpoint the plan names. Everything else is one flow.
- Never take a screenshot to find your way around — inspect instead. A screenshot is for evidence and for the
  visual read-back an assertion needs, and it costs far more to read.
- On failure, re-run **only the failing step forward**, never the flow from the top. See § Failure Recovery.

## Before Every Interaction — Inspect First

**Inspect the screen** before writing any `tapOn` or `assertVisible` that targets an element
you have not seen in the current screen state. Read `rid` (resource-id / testID) and `txt` (visible text)
from the output. Never guess selectors from a screenshot alone — screenshots lie about text values.

---

## Selector Priority

Use the first tier that resolves. Stop there.

1. `id:` — React Native `testID` / `resource-id`. Platform-neutral. Preferred always.
2. `text:` — visible on-screen text, **and** accessibility text: `content-desc` /
   `accessibilityLabel` are matched by `text:`, never by a key of their own.
3. `index:` — 0-based. Picks one of several elements a `text:` or `id:` matches.
4. Point coordinate — last resort. Never write one into a reusable flow.

`text:` and `id:` are **full-string regex, IGNORE_CASE**. A partial string never matches:
`text: "Log in"` misses an element reading `"Log in to continue"`. Use the whole on-screen
string, or anchor it — `"Log in.*"`.

`label:` is **not** a selector. It sets a command's human-readable name and matches nothing.

---

## Non-Clickable Label Rule

A `text:`/`id:` match can be a non-clickable node — Maestro taps it anyway and reports `success`, silently. Check `clickable: true` on the matched node before trusting it. If not clickable, target the clickable sibling/ancestor instead (by its own id, or by point).

---

## Duplicate Text Rule

When an inspection shows the same `txt` on more than one element, `text:` alone will
hit an unpredictable target. Switch to `id:` first. Where no `id:` exists, disambiguate with
`index:`, then with a positional qualifier anchored to a unique nearby element.

```yaml
# Preferred — use id
- tapOn:
    id: "unique-element-id"

# Fallback — pick by position in the match set (0-based)
- tapOn:
    text: "Duplicate text"
    index: 1

# Last resort — positional qualifier
- tapOn:
    text: "Duplicate text"
    below:
      text: "Unique nearby heading"
```

Inspect the hierarchy to confirm the anchor is unique before using it.
`above`/`below` shift when the keyboard is visible — only use them after `hideKeyboard`.
A dropdown's closed field and its bottom-sheet option share the same text — anchor `below:` the sheet heading,
which the closed field does not contain.

---

## Text Input Rule

**`inputText` appends — it does not replace existing content.** Typing into a non-empty field adds to
whatever is already there.

Always erase before typing:

```yaml
- tapOn:
    id: "some-input"
- eraseText: 50      # use a count larger than the field can hold
- inputText: "value"
- hideKeyboard
```

`clearText` is not a valid Maestro command — do not use it.
`longPressOn` does not reliably select-all on Android — do not use it for clearing.

---

## Keyboard Rule

**`hideKeyboard` is mandatory immediately after every `inputText`, before any other action.**

The keyboard stays visible after input. Any action fired while the keyboard is up hits the keyboard
overlay instead of the intended target. The flow reports `success` and no error is raised — the failure
is silent.

```yaml
- inputText: "value"
- hideKeyboard          # always immediately after inputText
- waitForAnimationToEnd
- tapOn:                # safe to tap now
    id: "next-element"
```

---

## Animation Rule

Call `waitForAnimationToEnd` after:
- Every `tapOn` that triggers navigation or opens/closes a sheet or modal
- Every `hideKeyboard`
- Every `launchApp` or `stopApp`

Never substitute `waitForAnimationToEnd` with a timed delay.

---

## App State Rule

Navigate to a known screen by relaunching or tapping a stable nav element — never by pressing Back
through history. Back-stack state is unpredictable across test cases.

Form fields do **not** reset when navigating away and back. If a clean form is required, relaunch:

```yaml
- stopApp
- launchApp
- waitForAnimationToEnd
```

---

## Failure Recovery

When a step fails or produces unexpected state:

1. Inspect the screen — read the live hierarchy.
2. Identify the cause: wrong element targeted, keyboard still up, animation mid-flight, wrong screen.
3. Fix the YAML inline and re-run only the failing step forward.
   - A file's `env:` block only applies when that file runs as the top-level target. A comment claiming a default is not one — pass every `${VAR}` yourself when running a subflow standalone.
4. Do **not** update the flow file on disk unless the user asks.
5. Do **not** rerun the whole flow from the top unless state is unrecoverable.
6. If the element is absent at all resolution tiers, mark the TC `🚫 BLOCKED` — never guess coordinates.

---

## Screenshot Rule

An inspection is for targeting only. It is never used to confirm pass/fail.

Use `takeScreenshot` (absolute path — § Driver) inside the flow to save evidence at the assertion moment,
then read the image back before recording PASSED/FAILED.

A flow reporting `success` only means no command threw an error — it does not mean the assertion passed.

---

## Invalid Commands

| Do not use | Use instead |
|---|---|
| `scrollDown` | `scroll` or `swipe: direction: UP` |
| `longPressOn` (for clearing) | `eraseText: <n>` |

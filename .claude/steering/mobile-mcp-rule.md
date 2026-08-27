# Mobile MCP Rules

Audience: mobile exec plan authors and plan runners. Governs every `mobile` MCP call.

App under test: `APP_PACKAGE` in `.claude/steering/project-config.md` § Environment. Read it from there;
never hardcode an identifier into a plan, a rule, or a command.

**Read the schemas, not a paraphrase.** The `mobile_*` tools are deferred: load their schemas with
`ToolSearch` before the first call, and take every signature, argument name, and required flag from there.
This file carries policy only. Where it disagrees with a schema, the schema wins.

**Platform reality.** Only Android is verified — see `.claude/locator-cache.json` §
`bfg-otc-app._verifiedOn`. No iOS build exists yet. The iOS rules below hold for when one does; until then an
`ios` target is `BLOCKED` per § Decision Rules and the present platform still runs.

## Element Resolution Rules

Resolution order: `id` → `desc` → `text` → coordinate. Take the first tier that resolves.

- `id` is the React Native `testID`. It surfaces as `resource-id` on Android (no package prefix),
  `accessibilityIdentifier` on iOS, and `data-testid` on web — the same string on all three. A plan
  written against an `id` is platform-neutral.
- `desc` is `accessibilityLabel`: `content-desc` on Android, `accessibilityLabel` on iOS, `aria-label`
  on web.
- `text` is visible on-screen text. It is locale-dependent, and a text input's `text` is its
  PLACEHOLDER while empty and the typed value once filled — match a placeholder only to find an empty
  field.
- A coordinate is Android-only, a last resort, and valid ONLY at the resolution it was measured at. It
  belongs to the run; never write one into a plan.

Read `.claude/locator-cache.json` § `bfg-otc-app` before recon and before a run — `screens` for
identifiers, `android` for commands and measured taps. One key at a time:
`jq '.["bfg-otc-app"].screens.{screen}' .claude/locator-cache.json`.

- **Never tap a coordinate no current listing returned**, unless it is a cached tap whose stamped
  resolution matches the live device. A guessed tap in a mutating flow is a false result, not a test.
- A target resolving at no tier — no `id`, no `desc`, no `text` — blocks its TC. Name the element, its
  screen, and the `testID` the app team must add. A node carrying a `testID` and no visible text is
  addressable, not blocked.
- Launch the app with an explicit locale wherever a TC asserts on `text`, so every platform returns the
  labels the plan was written against.

## Caching Rules

- An identifier is cacheable. A `testID` or an `accessibilityLabel` belongs to the build, not to the run.
- A coordinate is cacheable only alongside the resolution it was measured at, and only for Android.
  Re-measure on any other resolution; never scale.
- A `mobile_list_elements_on_screen` result is never cacheable. Resolve it immediately before the
  interaction it feeds, and discard it after.
- `.claude/locator-cache.json` is the only store.

## App State Rules

- Reach a known screen by terminating and relaunching the app, never by tapping back through the stack.
- Launch with the command in the cache's `android.launch`, and confirm the launch landed before the first
  interaction.
- Clear persisted Android state: `adb shell pm clear {APP_PACKAGE}`.
- Clear persisted iOS state: `xcrun simctl uninstall booted {APP_PACKAGE}`, then reinstall.
- **A clear costs the one-time setup steps.** After it the app demands the SIT env gate
  (`APP_ENV_GATE_EMAIL`, per install), then the passcode (`APP_PASSCODE`, per device), before any TC
  screen is reachable. Neither is product behaviour: keep both out of TC steps and out of results.
  Walkthrough: `.claude/domain/login-flow.md`.

## Diagnostic Rules

- After every failed assertion, list crashes and fetch any crash ID new to this run.
- Capture Android logs with `adb logcat -d -t 200` immediately after the failure.
- Capture iOS logs with `xcrun simctl spawn booted log show --last 2m`.
- Record the log lines naming `{APP_PACKAGE}`, and those lines only.

## Backend Verification Rules

- The `mobile` server observes no network traffic. An assertion that the app sent, or did not send, a
  request is unobservable — rewrite it as the state the screen and the backend must both show.
- This repo ships no API client. Verify backend state through the endpoints in
  `.claude/locator-cache.json` § `api`, authenticated with the bearer token that section names.
- Record the observed status and the compared field values, or `not checked` where no endpoint in that
  section covers the assertion.
- Label every backend result as corroboration of the screen, never as observation of the app's request.

Interception was evaluated and rejected: on Android, OkHttp on 7+ ignores user-installed CAs, so mitmproxy
needs a `network_security_config.xml` `<debug-overrides>` change in the app source plus a separate debug
variant — and certificate pinning defeats it either way. Revisit iOS-only mitmproxy if wrong-request bugs
start appearing. Maestro MCP was rejected in favour of `mobile-mcp` because its flow-YAML verb model fits
discrete plan steps worse.

## Decision Rules

- Plan beats device on every input value conflict.
- Live listing beats plan on every target and coordinate conflict.
- Absent device beats plan: mark that platform `BLOCKED` and execute the platform that is present.

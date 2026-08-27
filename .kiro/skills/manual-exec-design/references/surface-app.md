# Surface Pack — Member App

Targets: `ios`, `android` (mobile MCP, per `.kiro/steering/mobile-mcp-rule.md`), `app-web` (Playwright, the
Expo web build, per `.kiro/steering/playwright-rule.md`). Domain: `.kiro/domain/otc-mobile.md`; login
runbook `.kiro/domain/login-flow.md`. Cached locators: `.kiro/locator-cache.json` § `bfg-otc-app`.

App under test: `APP_PACKAGE` in `.kiro/steering/project-config.md` § Environment.

**No iOS build exists yet** — `mobile-mcp-rule.md` § Platform reality. Phase 1 may still select `ios`; every
TC on it blocks at Preflight and the other targets still run. Say so at the gate rather than letting the run
discover it.

## One codebase, three targets

Screens are platform-neutral — `.kiro/locator-cache.json` § `bfg-otc-app._note`. Only query syntax, launch
and reset differ, so **the same target string holds on all three**:

| Prefix | iOS | Android | `app-web` |
|---|---|---|---|
| `id=` | `accessibilityIdentifier` | `resource-id` | `data-testid` |
| `desc=` | `accessibilityLabel` | `content-desc` | `aria-label` |
| `text=` | visible text | visible text | visible text |

Resolution order and the coordinate rule: `mobile-mcp-rule.md` § Element Resolution Rules. No coordinate is
ever written into a plan.

`_testIdCoverage` reads **sparse**: only `password-toggle`, `otp-cell-0..5`, `home-header-notification-btn`
and `home-header-unread-dot` carry an `id=`. Everything else resolves by `desc=` or `text=`, so a bare `text=`
matching several list rows is the normal case here, not an edge case.

## Observables

An assertion may be tied to any of these, and nothing else:

- element text or accessibility label returned by the listing
- element present in, or absent from, that listing **after scrolling the container to its end** —
  `mobile_list_elements_on_screen` returns the visible viewport only; off-screen is not absent
- screen orientation from `mobile_get_orientation`
- app still running, or crashed, from `mobile_list_crashes`
- backend state through the endpoints in `.kiro/locator-cache.json` § `api`, per
  `mobile-mcp-rule.md` § Backend Verification Rules
- on `app-web` only: DOM attributes and `browser_network_requests`

On `ios` and `android` the mobile server observes no network traffic. A Level 3 network assertion becomes
backend corroboration there — labelled as corroboration of what the screen shows, never as observation of the
app's request. An assertion that the app fired no request is unobservable: rewrite it as the state the screen
and the backend must both still show, or drop the TC to the target that can see it.

## Unaddressable elements

Common in this app. Fix: ask the app team for a React Native `testID` — one `testID` fixes all three targets
at once, so it is never a per-platform ask.

## Label overlay

- `ios`, `android` — **unavailable.** A native screen takes no injected overlay, so every capture there
  carries a sidecar, and the sidecar is what attributes it.
- `app-web` — **available.** It is a DOM.

## State reset

The lightest reset that reaches a wave's first precondition, in ascending cost:

| Reset the plan states | What it restores |
|---|---|
| `relaunch app` | a known screen, session kept |
| `logged-out start` | relaunch, then sign out |
| `clear app state` | wipes persisted state — and re-costs the one-time setup steps, per `mobile-mcp-rule.md` § App State Rules. State that cost in the wave's Note. |
| `fresh context` | `app-web` only |

Launch with an explicit `locale`, so every target returns the labels the plan was written against.

## Preflight

Per device target: the identifier from `mobile_list_available_devices`, its OS version, the build, and where
the `.apk` or `.app` comes from. `app-web`: its URL and build — **the URL is not in `project-config.md`, so
ask the user for it.**

Plus: the app installed at that build on every device target · locale and timezone matched across targets.

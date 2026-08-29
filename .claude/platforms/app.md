# Platform Pack — Member App

Shape: `.claude/platforms/TEMPLATE.md`. Loaded only when a member-app platform is enabled in
`.claude/steering/project-config.md` § Platforms.

Domain: `.claude/domain/otc-mobile.md`; login runbook `.claude/domain/login-flow.md`.
Shared across platforms — password policy, OTP, statuses, decimal precision: `.claude/domain/otc-shared.md`.
Cached locators: `.claude/locator-cache.json` § `bfg-otc-app`.
App under test: `APP_PACKAGE` in `project-config.md` § Environment.

## Targets

| Platform id | Label | Viewport | Driver rule |
|---|---|---|---|
| `ios` | Member app (iOS) | — device | `.claude/steering/maestro-rule.md` |
| `android` | Member app | — device | `.claude/steering/maestro-rule.md` |
| `app-web` | Member app (web) | `<FILL_IN>` | `.claude/steering/playwright-rule.md` |

One React Native + Expo codebase serves all three. A platform disabled in the registry is never planned
against — the registry's Enabled column carries the reason.

## Target grammar

Screens are platform-neutral — `.claude/locator-cache.json` § `bfg-otc-app._note`. Only query syntax, launch
and reset differ, so **the same target string holds on all three**:

| Prefix | iOS | Android | `app-web` |
|---|---|---|---|
| `id=` | `accessibilityIdentifier` | `resource-id` | `data-testid` |
| `desc=` | `accessibilityLabel` | `content-desc` | `aria-label` |
| `text=` | visible text | visible text | visible text |

Resolution order and the coordinate rule: `maestro-rule.md` § Selector Priority.
**No coordinate is ever written into a plan.**

`_testIdCoverage` reads **sparse** — only `password-toggle`, `otp-cell-0..5`, `home-header-notification-btn`
and `home-header-unread-dot` carry an `id=`. Everything else resolves by `desc=` or `text=`, so a bare `text=`
matching several list rows is the normal case here, not an edge case.

## Observables

An assertion may be tied to any of these, and nothing else:

- element text or accessibility label returned by a screen inspection
- element present in, or absent from, that inspection **after scrolling the container to its end** — an
  inspection returns the visible viewport only; off-screen is not absent
- screen orientation
- app still running, or crashed, from the crash log
- backend state through the endpoints in `.claude/locator-cache.json` § `memberApi`, authenticated per that
  section's `_authHeaders` — `api` is the Back Office section and does not serve this platform
- on `app-web` only: DOM attributes and `browser_network_requests`

On a device target the driver observes no network traffic. A ripple-level network assertion becomes
**backend corroboration** there — labelled as corroboration of what the screen shows, never as observation of
the app's request. An assertion that the app fired *no* request is unobservable: rewrite it as the state the
screen and the backend must both still show, or drop the TC to the platform that can see it.

## Unaddressable elements

Common here. Fix: ask the app team for a React Native `testID` — one `testID` fixes all three platforms at
once, so it is never a per-platform ask.

## Label overlay

- `ios`, `android` — **unavailable.** A native screen takes no injected overlay, so a capture is attributed by
  its file name and by the result note the caller writes for it.
- `app-web` — **available.** It is a DOM.

## State reset

| Reset the wave states | What it restores |
|---|---|
| `relaunch app` | a known screen, session kept |
| `logged-out start` | relaunch, then sign out |
| `clear app state` | wipes persisted state — and re-costs the one-time setup steps, per `maestro-rule.md` § App State Rule. State that cost in the wave's Note. |
| `fresh context` | `app-web` only |

Launch with an explicit `locale`, so every platform returns the labels the plan was written against.

## Preflight

- Device platforms: the connected device's identifier, OS version, build, and where the `.apk` or `.app`
  comes from
- `app-web`: its URL and build — **the URL is not in `project-config.md`; ask the user for it**
- The app installed at the build under test on every device platform
- Locale and timezone matched across platforms

**Session lifetime is a preflight fact here.** Where the environment expires a member session faster than a
flow takes to execute, record the measured window at the gate — it blocks TCs, and it may itself be a defect.

## Stack quirks

Values the driver rules name as placeholders and never hardcode:

| Placeholder | Value here |
|---|---|
| stack | React Native + Expo — one `testID` serves all three targets, per § Target grammar |
| recorder duration cap | Android `screenrecord`, 180s — the `capture-device.md` default, nothing extra |
| `{scroll container selector}` (`app-web`) | `<FILL_IN>` — `app-web` is disabled; fill when its URL is configured |
| `API_PATHS` (`app-web`) | `<FILL_IN>` — same |

`ios` and `android` take no injected overlay, so no web placeholder applies to them.

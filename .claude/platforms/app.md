# Platform Pack — Member App

Shape: `.claude/platforms/TEMPLATE.md`. Loaded only when a member-app platform is enabled in
`.claude/steering/project-config.md` § Platforms.

Domain: `.claude/domain/wt-member-site.md` (screens, feature × platform) and `.claude/domain/wt-trading.md`;
login runbook `.claude/domain/login-flow.md` § Native app. Shared across platforms — matrix, clients,
password policy, OTP: `.claude/domain/wt-shared.md`.
Cached locators: `.claude/locator-cache.json` § `wt-app`.
App under test: `APP_PACKAGE` in `project-config.md` § Environment — **one build per env × client**; the
client's row in § Clients names it.

## Targets

| Platform id | Label | Viewport | Driver rule |
|---|---|---|---|
| `ios` | Member app (iOS) | — device | `.claude/steering/maestro-rule.md` |
| `android` | Member app (Android) | — device | `.claude/steering/maestro-rule.md` |

One React Native codebase serves both. The mobile-web layout (`web-app`) is **not** this app — it is the member
site at a phone viewport, served by `member-web.md`. A platform disabled in the registry is never planned
against — the registry's Enabled column carries the reason.

## Target grammar

Screens are platform-neutral — and shared with the member site: the same `testID` string is `data-testid` on
web, `resource-id` on Android, `accessibilityIdentifier` on iOS (`login-submit`, `trade-button-order-{buy|sell}`,
`price-alert-management-current-symbol-tab`…). Only query syntax, launch and reset differ:

| Prefix | iOS | Android |
|---|---|---|
| `id=` | `accessibilityIdentifier` | `resource-id` — **unqualified** (`login-submit`, never `com.aquariux…:id/login-submit`) |
| `desc=` | `accessibilityLabel` | `content-desc` |
| `text=` | visible text | visible text |

Resolution order and the coordinate rule: `maestro-rule.md` § Selector Priority.
**No coordinate is ever written into a plan.**

`id=` coverage is **broad** on this app — the reference automation targets almost every control by testid.
Try the web `data-testid` string as `id=` before falling back to `text=`. iOS reports many controls twice
(accessibility wrapper + control at the same frame); `login-account-type` sits on both a container and the
text field — qualify by element type when a bare `id=` matches two.

## Observables

An assertion may be tied to any of these, and nothing else:

- element text or accessibility label returned by a screen inspection
- element present in, or absent from, that inspection **after scrolling the container to its end** — an
  inspection returns the visible viewport only; off-screen is not absent
- screen orientation
- app still running, or crashed, from the crash log
- backend state through the endpoints in `.claude/locator-cache.json` § `api`, authenticated per that
  section's notes — this repo ships no API client

On a device target the driver observes no network traffic. A ripple-level network assertion becomes
**backend corroboration** there — labelled as corroboration of what the screen shows, never as observation of
the app's request. An assertion that the app fired *no* request is unobservable: rewrite it as the state the
screen and the backend must both still show, or drop the TC to the platform that can see it.

## Unaddressable elements

Common here. Fix: ask the app team for a React Native `testID` — one `testID` fixes all three platforms at
once, so it is never a per-platform ask.

## Label overlay

**Unavailable.** A native screen takes no injected overlay, so a capture is attributed by its file name and by
the result note the caller writes for it.

## State reset

| Reset the wave states | What it restores |
|---|---|
| `relaunch app` | a known screen, session kept |
| `logged-out start` | relaunch, then sign out |
| `clear app state` | wipes persisted state — session and onboarding survive a plain relaunch (`skip ads`, `Got it`, Remember me), per `maestro-rule.md` § App State Rule. State that cost in the wave's Note. |

Launch with an explicit `locale`, so every platform returns the labels the plan was written against.

## Preflight

- The connected device's identifier, OS version, build, and where the `.apk` or `.app` comes from
- **Build = env × client.** `adb shell pm list packages | grep aquariux` / `xcrun simctl listapps <udid> | grep -i aquariux`
  must show `APP_PACKAGE` for the client under test — `…sit.lirunex` and `…sit.transactcloudmt5` are different
  apps. A missing feature is a build mismatch until this check says otherwise
- Locale and timezone matched across platforms; record device model + OS in the plan
- Market open for the symbol under test — trading TCs are blocked, not failed, on a closed market

**Session lifetime is a preflight fact here.** Where the environment expires a member session faster than a
flow takes to execute, record the measured window at the gate — it blocks TCs, and it may itself be a defect.

## Stack quirks

Values the driver rules name as placeholders and never hardcode:

| Placeholder | Value here |
|---|---|
| stack | React Native — one `testID` serves web, Android and iOS, per § Target grammar |
| recorder duration cap | Android `screenrecord`, 180s — the `capture-device.md` default, nothing extra |
| pre-login gates | `ads-skip-button` (up to 3 taps), `Got it`, Remember me — `login-flow.md` § Native app |
| in-app browser | Manage Funds, Sign up, Pelican copy-trade open a webview/browser — close it before the next step |

Native screens take no injected overlay, so no web placeholder applies.

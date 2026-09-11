# Platform Pack — Member Site (web)

Shape: `.claude/platforms/TEMPLATE.md`. Loaded only when `web` or `web-app` is enabled in
`.claude/steering/project-config.md` § Platforms.

Domain: `.claude/domain/wt-member-site.md` (screens, feature × platform) and `.claude/domain/wt-trading.md`;
login runbook `.claude/domain/login-flow.md` § Member site. Shared across platforms — matrix, clients,
password policy, OTP: `.claude/domain/wt-shared.md`.
Cached locators: `.claude/locator-cache.json` § `wt-member-web`.
URL: the client's Member URL from `project-config.md` § Clients (`MEMBER_URL` is the default client).

## Targets

| Platform id | Label | Viewport | URL path | Driver rule |
|---|---|---|---|---|
| `web` | Member site (desktop) | desktop, 1920×1080 or wider | `/web` | `.claude/steering/playwright-rule.md` |
| `web-app` | Member site (mobile web) | `WEB_APP_VIEWPORT` 430×932 | `/mobile` | `.claude/steering/playwright-rule.md` |

Same URL, different UI. `web` has a sidebar IA (Trade, Quoteboard, Markets, Assets, Signal…); `web-app` has the
app's bottom-nav IA (Home, Markets, Trade, Assets, Menu). A TC is planned against the row whose IA owns the
feature — `wt-member-site.md` § Feature × platform. Set the viewport as the **first statement of every
driver call**; the MCP can reset it between calls.

## Target grammar

| Prefix | Resolves to | Playwright |
|---|---|---|
| `id=` | `data-testid` | `[data-testid="…"]` |
| `desc=` | `aria-label` | `[aria-label="…"]` |
| `text=` | visible text | text selector |

Resolution order `id= > desc= > role+name > text=`, per `playwright-rule.md` § DOM-First Rule.
**A coordinate never enters a plan.**

`id=` coverage is **broad** — the reference automation targets nearly every control by `data-testid`
(`tab-login-account-type-{live|demo|crm}`, `login-submit`, `trade-button-order-{buy|sell}`,
`tab-asset-order-type-{…}`, `side-bar-option-{…}`). The same string is the app's `testID`, so a locator verified
here seeds `wt-app` too. **Username-field divergence:** `web` (desktop) uses `login-user-id`; `web-app`,
`ios`, and `android` all use `login-account-type` for the same field — despite the name, confirmed in source.
Account-type tabs on `web-app` are text-only (`Live` / `Demo`) — the one known gap.

## Observables

An assertion may be tied to any of these, and nothing else:

- element present in, or absent from, the DOM
- attribute value — `disabled`, `readonly`, `aria-checked`, `class`, computed colour
- text content of a resolved element
- network response status and body from `browser_network_requests`
- console errors from `browser_console_messages`
- backend state through the endpoints in `.claude/locator-cache.json` § `api`, authenticated with the bearer
  token that section names — this repo ships no API client

Ripple-level network assertions are directly observable here, **including "no request fired"**.

Live values — current price, P/L, margin, equity — **move**. An assertion on one records the observed value and
time and compares with a tolerance, never exact-matches (`wt-trading.md` § Calculations).

## Unaddressable elements

Rare. Fix: ask the FE team for a `data-testid` — one `testID` fixes web, Android and iOS at once.

## Label overlay

**Available** — the DOM takes an injected overlay, so one frame may carry several labelled checkpoints.

## State reset

| Reset the wave states | What it restores |
|---|---|
| `navigate` | a known page, session kept |
| `fresh context` | a clean, logged-out browser session |

A wave depending on a logged-out start states `fresh context`; the runner never assumes one. Show/hide
balance (eye icon), theme, OCT and language **persist across refresh and re-login** — a wave that needs the
default states it and resets it.

## Preflight

- URL: the client's Member URL + `/web` or `/mobile` — confirm it responds, and that the footer / theme colour
  matches the client (`wt-shared.md` § Theme colours)
- Account: id + account type per `project-config.md` § Clients; CRM accounts need an inbox for the OTP
- Market open for the symbol under test — trading TCs are blocked, not failed, on a closed market
- Viewport per § Targets, set on every call
- Build: `unknown` is acceptable — the page exposes none in source

## Stack quirks

Values `playwright-rule.md` and `capture-web.md` name as placeholders and never hardcode:

| Placeholder | Value here |
|---|---|
| component library | `<FILL_IN>` — discover on first recon |
| hidden-state overlay class | `<FILL_IN>` |
| `{scroll container selector}` | `<FILL_IN>` — assets tables on `web` scroll inside their own container |
| `API_PATHS` | `['/api/']` — member calls are `/api/trade/`, `/api/order/`, `/api/market/`, `/api/user/`, `/api/config/`, `/api/notification/` |

After `networkidle`, wait a further 500 ms before reading the DOM — the SPA renders after the last response.
A locator timing out at 3 s means the locator is wrong; fix the selector, do not raise the timeout.

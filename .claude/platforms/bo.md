# Platform Pack — Back Office (web)

Shape: `.claude/platforms/TEMPLATE.md`. Loaded only when a `bo*` platform is enabled in
`.claude/steering/project-config.md` § Platforms.

Domain: `.claude/domain/wt-admin.md` § Back Office — one BO **per client**; the URL is the client's row in
`project-config.md` § Clients. Shared across platforms — matrix, clients, password policy, OTP:
`.claude/domain/wt-shared.md`. Login (captcha, user pool): `.claude/domain/login-flow.md` § Back Office.
Cached locators: `.claude/locator-cache.json` § `wt-bo`.

## Targets

| Platform id | Label | Viewport | Driver rule |
|---|---|---|---|
| `bo` | Back Office | desktop | `.claude/steering/playwright-rule.md` |

## Target grammar

| Prefix | Resolves to | Playwright |
|---|---|---|
| `id=` | `data-testid` | `[data-testid="…"]` |
| `desc=` | `aria-label` | `[aria-label="…"]` |
| `text=` | visible text | text selector |

Resolution order `id= > desc= > role+name > text=`, per `playwright-rule.md` § DOM-First Rule.
**A coordinate never enters a plan.**

Coverage is **unknown** — the reference automation drives this surface by API only and holds no BO locators.
Run `document.querySelectorAll('[data-testid]').length` at the gate; where it returns 0, every target string
falls through to role+name, CSS or attribute — record that, it is worth an ask.

## Observables

An assertion may be tied to any of these, and nothing else:

- element present in, or absent from, the DOM
- attribute value — `disabled`, `readonly`, `aria-checked`, `class`
- text content of a resolved element
- network response status and body from `browser_network_requests`
- console errors from `browser_console_messages`
- backend state through the endpoints in `.claude/locator-cache.json` § `api`, authenticated with the bearer
  token that section names — this repo ships no API client

Ripple-level network assertions are directly observable here, **including "no request fired"**.

## Unaddressable elements

Rare. Fix: ask the FE team for a `data-testid`.

## Label overlay

**Available** — the DOM takes an injected overlay, so one frame may carry several labelled checkpoints.

## State reset

| Reset the wave states | What it restores |
|---|---|
| `navigate` | a known page, session kept |
| `fresh context` | a clean, logged-out browser session |

A wave depending on a logged-out start states `fresh context`; the runner never assumes one.

## Preflight

- URL: the client's BO URL from `project-config.md` § Clients (`BO_URL` is the default client) — confirm it responds
- Login: `BO_USER` + `BO_PASSWORD` + captcha `CAPTCHA_SIT` — `login-flow.md` § Back Office
- Client and env of this BO stated in the plan — a BO change reaches every tester on that client
- Browser: chromium, desktop viewport
- Build: the page footer, or `unknown`
- **Never on prod** — BO is blocked there

## Stack quirks

Values `playwright-rule.md` and `capture-web.md` name as placeholders and never hardcode:

| Placeholder | Value here |
|---|---|
| component library | `<FILL_IN>` — discover on first recon |
| hidden-state overlay class | `<FILL_IN>` |
| `{scroll container selector}` | `<FILL_IN>` |
| `API_PATHS` | `['/api/admin/', '/backoffice/', '/configuration/']` |

Symbol config, pretrade, OCT, price-alert and copy-trade settings each post to `/api/admin/backoffice/config/v1/…`
or `/api/admin/configuration/v2/symbols` — the endpoints to watch when confirming a BO save landed.

# Platform Pack — Root Admin (web)

Shape: `.claude/platforms/TEMPLATE.md`. Loaded only when `root-admin` is enabled in
`.claude/steering/project-config.md` § Platforms.

Domain: `.claude/domain/wt-admin.md` § Root Admin — **one global portal** for every client; a client is a
*company* (tenant) inside it. Shared across platforms: `.claude/domain/wt-shared.md`.
Login (captcha, user pool): `.claude/domain/login-flow.md` § Root Admin.
Cached locators: `.claude/locator-cache.json` § `wt-root-admin`.
URL: `ROOT_ADMIN_URL` in `project-config.md` § Environment.

## Targets

| Platform id | Label | Viewport | Driver rule |
|---|---|---|---|
| `root-admin` | Root Admin | desktop | `.claude/steering/playwright-rule.md` |

Root Admin is mostly a **setup surface**: a TC changes a company setting here, then asserts on the member
site. Enable this row only when a TC asserts on Root Admin itself; otherwise the setup step lives in the
member-site wave's precondition and cites `wt-admin.md` § Cross-surface recipes.

## Target grammar

| Prefix | Resolves to | Playwright |
|---|---|---|
| `id=` | `data-testid` | `[data-testid="…"]` |
| `desc=` | `aria-label` | `[aria-label="…"]` |
| `text=` | visible text | text selector |

Resolution order `id= > desc= > role+name > text=`, per `playwright-rule.md` § DOM-First Rule.
**A coordinate never enters a plan.**

**No testids in source** — the reference automation reaches this portal with structural XPath only
(`//input[./following-sibling::div/img]` for the captcha field). Expect `id=` to resolve nothing; plan targets
as `desc=`, role+name or `text=`, and record the coverage count at the gate.

## Observables

An assertion may be tied to any of these, and nothing else:

- element present in, or absent from, the DOM
- attribute value — `disabled`, `checked`, `class`
- text content of a resolved element
- network response status and body from `browser_network_requests` — a saved company is one
  `PUT /api/root/company/v2` carrying the **whole** company object
- console errors from `browser_console_messages`
- the effect on the member site — observed on the `web` / `web-app` / `android` row, never assumed here

## Unaddressable elements

Common. Fix: ask the Root Admin FE team for a `data-testid`.

## Label overlay

**Available** — the DOM takes an injected overlay.

## State reset

| Reset the wave states | What it restores |
|---|---|
| `navigate` | a known page, session kept |
| `fresh context` | a clean, logged-out browser session |
| `restore company setting` | the value **read at setup** — never a default. Every wave that writes states this reset and the value it restores |

A company update is destructive for lists: saving features or languages **disables anything not included**.
A wave that edits one item states the full list it will save.

## Preflight

- URL: `ROOT_ADMIN_URL` (`…/root` on SIT — confirmed in `config/sit.yaml`, not yet round-tripped live) — confirm it responds
- Login: `ROOT_ADMIN_USER` + `ROOT_ADMIN_PASSWORD` from § Environment + captcha `CAPTCHA_SIT`
- Tenant: the company under test = the client in the plan; state it — a change reaches every tester on that client
- **Never on prod** — Root Admin is blocked there
- Build: `unknown` is acceptable

## Stack quirks

| Placeholder | Value here |
|---|---|
| component library | Mantine — generated element `id`s are unstable per render, never target them |
| hidden-state overlay class | `<FILL_IN>` |
| `{scroll container selector}` | `<FILL_IN>` |
| `API_PATHS` | `['/api/root/']` |

Captcha is an image with a single-use `cryptograph`; on SIT the code `123` is accepted. A wrong code refreshes
the image — re-read it before retrying.

# Platform Pack — Back Office (web)

Shape: `.kiro/platforms/TEMPLATE.md`. Loaded only when a `bo*` platform is enabled in
`.kiro/steering/project-config.md` § Platforms.

Domain: `.kiro/domain/otc-bo.md`, roles under § Roles & Permissions.
Cached locators: `.kiro/locator-cache.json` § `otc-bo`.

## Targets

| Platform id | Label | Viewport | Driver rule |
|---|---|---|---|
| `bo` | Back Office | desktop | `.kiro/steering/playwright-rule.md` |
| `bo-mv` | Back Office (mobile view) | 390×844 | `.kiro/steering/playwright-rule.md` |

## Target grammar

| Prefix | Resolves to | Playwright |
|---|---|---|
| `id=` | `data-testid` | `[data-testid="…"]` |
| `desc=` | `aria-label` | `[aria-label="…"]` |
| `text=` | visible text | text selector |

Resolution order `id= > desc= > role+name > text=`, per `playwright-rule.md` § DOM-First Rule.
**A coordinate never enters a plan.**

Coverage varies by deployment. Where `document.querySelectorAll('[data-testid]').length` returns 0, every
target string falls through to role+name, CSS or attribute — record that at the gate, it is worth an ask.

## Observables

An assertion may be tied to any of these, and nothing else:

- element present in, or absent from, the DOM
- attribute value — `disabled`, `readonly`, `aria-checked`, `class`
- text content of a resolved element
- network response status and body from `browser_network_requests`
- console errors from `browser_console_messages`
- backend state through the endpoints in `.kiro/locator-cache.json` § `api`, authenticated with the bearer
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

- URL: `BO_URL` from `project-config.md` § Environment — confirm it responds
- Browser: chromium. `bo` at desktop size, `bo-mv` at 390×844
- Build: the page footer, or `unknown`

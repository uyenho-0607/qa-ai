# Surface Pack — Back Office (web)

Targets: `bo` (desktop), `bo-mv` (390×844). Driver: Playwright MCP, per
`.kiro/steering/playwright-rule.md`. Domain: `.kiro/domain/otc-bo.md`, roles under § Roles & Permissions.
Cached locators: `.kiro/locator-cache.json` § `otc-bo`.

## Target grammar

| Prefix | Resolves to | Playwright |
|---|---|---|
| `id=` | `data-testid` | `[data-testid="…"]` |
| `desc=` | `aria-label` | `[aria-label="…"]` |
| `text=` | visible text | text selector |

Resolution order `id= > desc= > role+name > text=`, per `playwright-rule.md` § DOM-First Rule. A coordinate
never enters the plan.

BO coverage is dense — an `id=` exists for nearly every control. A target that falls through to `text=` is
worth a note at the gate.

## Observables

An assertion may be tied to any of these, and nothing else:

- element present in, or absent from, the DOM
- attribute value — `disabled`, `readonly`, `aria-checked`, `class`
- text content of a resolved element
- network response status and body from `browser_network_requests`
- console errors from `browser_console_messages`
- backend state through the endpoints in `.kiro/locator-cache.json` § `api`, authenticated with the bearer
  token that section names — this repo ships no API client

Level 3 network assertions are directly observable here, including "no request fired".

## Unaddressable elements

Rare in BO. Fix: ask the FE team for a `data-testid`.

## Label overlay

**Available** — the DOM takes an injected overlay, so a `normal`-mode SCREENSHOT group may carry several TCs
in one frame, each labelled.

## State reset

The lightest reset that reaches a wave's first precondition, in ascending cost:

| Reset the plan states | What it restores |
|---|---|
| `navigate` | a known page, session kept |
| `fresh context` | a clean, logged-out browser session |

A wave that depends on a logged-out start states `fresh context`; the runner never assumes one.

## Preflight

Both targets: URL `BO_URL`, browser chromium, build from the page footer or `unknown`; `bo` at desktop size,
`bo-mv` at 390×844.

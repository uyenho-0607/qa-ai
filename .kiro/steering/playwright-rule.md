---
inclusion: manual
---

# Playwright MCP Rules

Governs every browser interaction. **Names no platform id and no app-specific selector** — URLs and
credentials come from `.kiro/steering/project-config.md` § Environment, and every stack-specific value
(`{section}`, `{scroll container selector}`, `API_PATHS`, hidden-state classes) from the target's platform pack
in `.kiro/platforms/`.

## Tool Rule
Use `browser_run_code_unsafe` for ALL interactions. Never use `browser_snapshot`, `browser_click`,
`browser_type` — unreliable on SPAs.

Exception: `browser_navigate` as call 1 to handle dead sessions. Then `page.goto()` inside `run_code_unsafe`.

**Pattern:** call 1 = `browser_navigate` → call 2+ = `run_code_unsafe` (interact + read + screenshot)

## Timeouts
- `click()`, `fill()`, `check()`, `waitForSelector()`: `{ timeout: 3000 }`
- `page.goto()`: default
- After `waitForLoadState('networkidle')`: add `waitForTimeout(500)`

Timeout at 3s = wrong locator. Fix the selector, don't raise the timeout.

## DOM-First Rule
Before any click/fill: check `locator-cache.json` — **one screen at a time, never the whole file, never a
whole platform section**. `{section}` is the key the target's platform pack names under § Cached locators:
`jq '.["{section}"].screens | keys' .kiro/locator-cache.json` to list the screens, then
`jq '.["{section}"].screens.{screen}' .kiro/locator-cache.json` for the one in hand.

Missing? scan: `page.evaluate(() => [...document.querySelectorAll('[data-testid]')].map(e => e.dataset.testid))`

Priority: `data-testid` → `aria-label`/`desc=` → `role+name` → CSS → text

## Stateful Form Pattern
`navigate → capture state → input → waitForResponse|waitForTimeout(500) → evaluate DOM → next input`

Never batch multiple inputs without intermediate state verification.

## Locator Recovery
0. **A stale overlay is not a missing element.** Component libraries commonly leave closed dropdowns, modals
   and drawers mounted in the DOM. A locator that "resolves but is not visible" is matching a stale one —
   scope to the live node rather than raising the timeout. Library-agnostic: filter `[role=dialog]` by
   `getBoundingClientRect().width > 0`. For the library's own hidden-state class, read the target's platform
   pack § Stack quirks. Note that a fixed-position drawer has `offsetParent === null`, so that is not a
   visibility test.
1. Walk the § DOM-First Rule priority list, tier by tier.
2. Re-scan DOM via `page.evaluate()`
3. Screenshot + report found vs expected

## Session Reset
- Reach a known page by navigating to its URL, never by clicking back through history.
- A fresh session is a fresh context: `browser.newContext()`. Nothing else clears storage reliably.
- Viewport setting (probed or fixed) — see `capture-web.md` § Viewport.
- **Two concurrent independent sessions** — use two contexts from the same browser. Each context has isolated storage (localStorage, cookies, sessionStorage), so two accounts can be logged in simultaneously:
  ```js
  const browser = page.context().browser();
  const ctx2 = await browser.newContext();
  try {
    const page2 = await ctx2.newPage();
    // page = session A (already logged in), page2 = session B (log in separately)
    // ... drive both concurrently ...
  } finally {
    await ctx2.close();
  }
  ```
  This makes concurrency TCs (two admins acting simultaneously) agent-executable, not human-executable.
  `browser` is accessible via `page.context().browser()` — confirmed live.

## Network Inspection
Set listeners **before** navigation:
```js
const API_PATHS = ['{path prefix}'];   // from the target's platform pack § Stack quirks
const responses = [];
page.on('response', async resp => {
  if (API_PATHS.some(p => resp.url().includes(p))) {
    try { responses.push({ url: resp.url(), status: resp.status(), body: JSON.stringify(await resp.json()).slice(0,500) }); } catch {}
  }
});
await page.goto(TARGET_URL);
```

## Other
- Target 2 `run_code_unsafe` calls for simple tasks; more is fine for multi-page exploration

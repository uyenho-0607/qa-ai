# Playwright MCP Rules

Governs every browser interaction. URLs and credentials: `.claude/steering/project-config.md` § Environment.

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
Before any click/fill: check `locator-cache.json` — one page key at a time, never the whole file:
`jq 'keys' .claude/locator-cache.json` to find the key, then `jq '.{page_key}' .claude/locator-cache.json`.

Missing? scan: `page.evaluate(() => [...document.querySelectorAll('[data-testid]')].map(e => e.dataset.testid))`

Priority: `data-testid` → `role+name` → CSS → text

## Stateful Form Pattern
`navigate → capture state → input → waitForResponse|waitForTimeout(500) → evaluate DOM → next input`

Never batch multiple inputs without intermediate state verification.

## Locator Recovery
0. **A stale overlay is not a missing element.** Ant Design leaves closed dropdowns, modals and drawers in
   the DOM. A locator that "resolves but is not visible" is matching a stale one — scope to the live node
   (`.ant-dropdown:not(.ant-dropdown-hidden) …`, or filter `[role=dialog]` by `getBoundingClientRect().width > 0`)
   rather than raising the timeout. Note that a fixed-position drawer has `offsetParent === null`, so that is
   not a visibility test.
1. Try `data-testid` from cache
2. Try `role` + accessible name
3. Try CSS
4. Re-scan DOM via `page.evaluate()`
5. Screenshot + report found vs expected

## Session Reset
- Reach a known page by navigating to its URL, never by clicking back through history.
- A fresh session is a fresh context: `browser.newContext()`. Nothing else clears storage reliably.
- `bo-mv` calls `browser_resize` to 390×844 before its first navigation.

## Network Inspection
Set listeners **before** navigation:
```js
const responses = [];
page.on('response', async resp => {
  if (resp.url().includes('/api/') || resp.url().includes('/backoffice/')) {
    try { responses.push({ url: resp.url(), status: resp.status(), body: JSON.stringify(await resp.json()).slice(0,500) }); } catch {}
  }
});
await page.goto(TARGET_URL);
```

## Other
- Target 2 `run_code_unsafe` calls for simple tasks; more is fine for multi-page exploration
- Wrap `newContext` in `try/finally`. One video context at a time.

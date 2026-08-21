---
inclusion: manual
---

# Playwright MCP — Interaction Rules

Project URL and credentials (`BO_URL`, `BO_MAKER`, `BO_CHECKER`, `BO_ADMIN`, `SHARED_PASSWORD`) are in `project-config.md`. `BO_URL` requires VPN.

---

## Tool Rule

**Use `browser_run_code_unsafe` for all browser interactions.** Never use `browser_snapshot`, `browser_click`, `browser_type`, or other individual MCP tools — they are unreliable on SPAs.

**One exception:** use `browser_navigate` as the first call of every browser task to handle dead sessions (auto-creates a new page if the previous one closed). Within the same session, skip it and use `page.goto()` inside `run_code_unsafe`.

Never close the browser between tasks in the same session.

---

## Timeouts

- All `click()`, `fill()`, `check()`: `{ timeout: 3000 }`
- All `waitForSelector()`: `{ timeout: 3000 }`
- `page.goto()`: default timeout is acceptable
- After `waitForLoadState('networkidle')`: add `waitForTimeout(500)` for SPA render

**A locator timing out at 3s means the locator is wrong — fix the selector, do not increase the timeout.**

---

## DOM-First Rule

**Always read the DOM before interacting.** Never guess locators.

Before any click or fill:
1. If `.kiro/locator-cache.json` exists, check it for cached selectors — use them directly
2. If not cached: `page.evaluate(() => [...document.querySelectorAll('[data-testid]')].map(e => e.dataset.testid))` to scan
3. Use the discovered selector with `{ timeout: 3000 }`

Locator priority: `data-testid` → `role + name` → CSS → text (last resort)

---

## Stateful Form Pattern

For forms where UI state changes after each input (validation messages, field toggles, dynamic values):

```
navigate → capture state → input → waitForResponse OR waitForTimeout(500) → evaluate DOM → next input
```

**Never batch multiple inputs into one script block without intermediate state verification.**

Capture after every action that may trigger: validation messages, field enable/disable, value recalculation, new elements appearing.

---

## Locator Recovery Protocol

When a locator fails, run this sequence before reporting failure:

1. Try `data-testid` from cache
2. Try `role` + accessible name
3. Try CSS (unique class or attribute)
4. Re-scan DOM via `page.evaluate()` — page may have re-rendered
5. Take screenshot + report what was found vs what was expected

**Never guess or skip.** A locator failure means the page structure changed or was never mapped — it is not permission to proceed without the element.

---

## Network Inspection

Set up response listeners **before** navigation when API inspection is needed:

```js
const responses = [];
page.on('response', async resp => {
  const url = resp.url();
  if (url.includes('/api/') || url.includes('/backoffice/')) {
    try { responses.push({ url, status: resp.status(), body: JSON.stringify(await resp.json()).slice(0, 500) }); } catch {}
  }
});
await page.goto(TARGET_URL);
```

---

## Batching Rule

**Target: 2 `run_code_unsafe` calls per task** for simple interactions.

For exploration tasks (building checkpoint maps, multi-page discovery): use as many calls as needed — one call per page or state transition is acceptable. Never batch across state transitions.

---

## Context Cleanup

Wrap `newContext` in `try/finally`. Never leave orphaned contexts. One video context at a time.

# Capture — Web Targets

Targets: `bo`, `bo-mv`, `app-web`. Driver: Playwright, per `.claude/steering/playwright-rule.md`.
Naming, labels, timing and verification: `.claude/steering/capture-mechanics.md`. This file is the
Playwright mechanics for those rules, and nothing else.

**Every path is repo-relative.** `page.screenshot({ path })` and `recordVideo.dir` resolve against the
Playwright MCP server's working directory, so a bare `'shot.png'` lands at the repo root. Always write
`tasks/{KEY}/exec/evidence/…`, or `tasks/{KEY}/exec/recon/…` for recon. (AO-925, 2026-08-26)

## Viewport — first, always

```js
const { width, height } = await page.evaluate(() => ({ width: window.screen.width, height: window.screen.height }));
const vw = width  >= 1280 ? width  : 2560;
const vh = height >= 720  ? height : 1440;
await page.setViewportSize({ width: vw, height: vh });
```

`bo-mv` uses 390×844 instead, both for the viewport and for a recording's size.

## Bring the element into view

```js
// vertical
await page.locator('{selector}').scrollIntoViewIfNeeded({ timeout: 5000 });
await page.waitForTimeout(300);
// horizontal, for a wide table
await page.evaluate(() => {
  const c = document.querySelector('[data-testid*="table-scroll-container"]');
  if (c) c.scrollLeft = c.scrollWidth;
});
await page.waitForTimeout(500);
```

Scroll before labelling. Never label an element sitting behind an overlay.

## Checkpoint label — one per `**Exp:**` checkpoint

```js
await page.evaluate(({ label, replace }) => {
  if (replace) document.querySelectorAll('[data-exec-label]').forEach(n => n.remove());
  const d = document.createElement('div');
  d.setAttribute('data-exec-label', '1');
  d.textContent = label;
  d.style.cssText = 'position:fixed;left:12px;z-index:99999;background:#0a7;color:#fff;'
    + 'padding:6px 12px;border-radius:4px;font:bold 14px sans-serif;white-space:nowrap;'
    + `top:${12 + document.querySelectorAll('[data-exec-label]').length * 34}px;`;
  document.body.appendChild(d);
}, { label: '{TC-ID} | c{N} | {what is verified}', replace: true });
```

- **Video** — `replace: true`. Each label clears the last; the recording separates the checkpoints.
- **Screenshot** — `replace: false` after the first, so every checkpoint the frame proves appears in it.

## Element annotation — a bug or a fix, pointed at

```js
await page.evaluate(({ selector, label, color }) => {
  const el = document.querySelector(selector);
  if (!el) return;
  el.style.border = `3px solid ${color}`;
  el.style.backgroundColor = color === 'red' ? 'rgba(255,0,0,0.12)' : 'rgba(0,180,0,0.12)';
  const d = document.createElement('div');
  d.textContent = label;
  d.style.cssText = 'position:absolute;z-index:99999;padding:4px 8px;border-radius:4px;'
    + `background:${color};color:#fff;font:bold 13px sans-serif;white-space:nowrap;pointer-events:none;`;
  const r = el.getBoundingClientRect();
  d.style.top  = `${window.scrollY + r.top - 28}px`;
  d.style.left = `${window.scrollX + r.left}px`;
  document.body.appendChild(d);
}, { selector: '{selector}', label: '❌ {what is wrong}', color: 'red' });
```

❌ prefixes a bug, ✅ a fix.

## API response overlay — BE findings

```js
await page.evaluate(({ api }) => {
  const o = document.createElement('div');
  o.style.cssText = 'position:fixed;bottom:20px;right:20px;z-index:99999;background:#1e1e1e;color:#d4d4d4;'
    + 'padding:16px;border-radius:8px;font-family:monospace;font-size:12px;max-width:500px;'
    + 'max-height:300px;overflow:auto;border:2px solid red;';
  o.innerHTML = `<div style="color:red;font-weight:bold;margin-bottom:8px;">❌ API Response (${api.status})</div>`
    + `<div style="color:#9cdcfe;margin-bottom:8px;word-break:break-all;">${api.url}</div>`
    + `<pre style="margin:0;white-space:pre-wrap;color:#ce9178;">${api.body}</pre>`;
  document.body.appendChild(o);
}, { api: { url: '{path}', status: 200, body: JSON.stringify(captured, null, 2) } });
```

Register the network listener before navigating, per `.claude/steering/playwright-rule.md` § Network
Inspection. Overlay the one relevant response, truncated to the fields that matter.

## Screenshot

Viewport → scroll into view → label or annotate → capture:

```js
await page.screenshot({ path: 'tasks/{KEY}/exec/evidence/{name}.png', type: 'png', scale: 'device' });
```

Where one assertion needs two states — a table and its detail panel, a closed and an open dropdown, two
pages — change the state between frames and label only what is visible in each.

## Video — one replay pass per group

The recording is a replay, not the test. Test the group first, then replay every step inside one recording
context at a steady pace. Restore the starting precondition first only where the test changed state; a
read-only flow replays as-is.

```js
const state = await page.context().storageState();
const ctx = await page.context().browser().newContext({
  storageState: state,
  recordVideo: { dir: 'tasks/{KEY}/exec/evidence/', size: { width: vw, height: vh } },
  viewport: { width: vw, height: vh },
  screen:   { width: vw, height: vh }
});
const rec = await ctx.newPage();
try {
  // replay the group's steps, injecting each checkpoint's label at its assertion moment
  return await rec.video().path();
} finally {
  await ctx.close();   // the file is only finalized on close
}
```

Where the app keeps auth in `sessionStorage`, copy it into the recording context and reload before the first
step — `storageState()` does not carry it.

Convert and name it, then verify per `capture-mechanics.md` § Verify:

```bash
ffmpeg -y -i "<webm>" -c:v libx264 -preset fast -crf 23 "tasks/{KEY}/exec/evidence/{stem}_{target}.mp4"
```

Keep the `.webm` until the user confirms the `.mp4`. One video context at a time.

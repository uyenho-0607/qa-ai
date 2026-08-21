# Screenshot Guide — Code Templates

## Viewport Setup (always first)

```js
const { width, height } = await page.evaluate(() => ({
  width: window.screen.width, height: window.screen.height
}));
const vw = width >= 1280 ? width : 2560;
const vh = height >= 720 ? height : 1440;
await page.setViewportSize({ width: vw, height: vh });
```

---

## Scrolling

### Horizontal (table columns):
```js
await page.evaluate(() => {
  const container = document.querySelector('[data-testid*="table-scroll-container"]');
  if (container) container.scrollLeft = container.scrollWidth;
});
await page.waitForTimeout(500);
```

### Vertical (long tables):
```js
await page.locator('[data-testid="target-cell"]').scrollIntoViewIfNeeded({ timeout: 5000 });
await page.waitForTimeout(500);
```

### Combined:
```js
await page.locator('[data-testid="target-row"]').scrollIntoViewIfNeeded({ timeout: 5000 });
await page.waitForTimeout(300);
await page.evaluate(() => {
  const container = document.querySelector('[data-testid*="table-scroll-container"]');
  if (container) container.scrollLeft = container.scrollWidth;
});
await page.waitForTimeout(500);
```

---

## Annotation Label Overlay

```js
await page.evaluate(({ selector, label, color }) => {
  const el = document.querySelector(selector);
  if (!el) return;
  el.style.border = `3px solid ${color}`;
  el.style.backgroundColor = color === 'red' ? 'rgba(255,0,0,0.12)' : 'rgba(0,180,0,0.12)';
  const labelDiv = document.createElement('div');
  labelDiv.textContent = label;
  labelDiv.style.cssText = `
    position: absolute; z-index: 99999;
    background: ${color}; color: white;
    padding: 4px 8px; border-radius: 4px;
    font-size: 13px; font-weight: bold;
    white-space: nowrap; pointer-events: none;
  `;
  const rect = el.getBoundingClientRect();
  labelDiv.style.top = `${window.scrollY + rect.top - 28}px`;
  labelDiv.style.left = `${window.scrollX + rect.left}px`;
  document.body.appendChild(labelDiv);
}, { selector: '[data-testid="buggy-cell"]', label: '❌ Shows LIMIT instead of STOP LIMIT', color: 'red' });
```

- ❌ prefix for bugs, ✅ prefix for fixes

---

## BE Bug: API Response Overlay

```js
await page.evaluate(({ apiData }) => {
  const overlay = document.createElement('div');
  overlay.style.cssText = `
    position: fixed; bottom: 20px; right: 20px; z-index: 99999;
    background: #1e1e1e; color: #d4d4d4; padding: 16px;
    border-radius: 8px; font-family: monospace; font-size: 12px;
    max-width: 500px; max-height: 300px; overflow: auto;
    border: 2px solid red; box-shadow: 0 4px 12px rgba(0,0,0,0.5);
  `;
  overlay.innerHTML = `
    <div style="color:red;font-weight:bold;margin-bottom:8px;">❌ API Response (${apiData.status})</div>
    <div style="color:#9cdcfe;margin-bottom:8px;word-break:break-all;">${apiData.url}</div>
    <pre style="margin:0;white-space:pre-wrap;color:#ce9178;">${apiData.body}</pre>`;
  document.body.appendChild(overlay);
}, { apiData: { url: '/api/endpoint', status: 200, body: JSON.stringify(capturedResponse, null, 2) } });
```

Rules:
- Network listener BEFORE navigation
- Only overlay the RELEVANT response
- Truncate to relevant fields
- Position: fixed bottom-right
- Combine with element annotation

---

## Full Screenshot Template

```js
async (page) => {
  // 1. Viewport  — see §Viewport Setup
  // 2. Scroll    — see §Scrolling
  // 3. Annotate  — see §Annotation Label Overlay
  // 4. Screenshot
  await page.screenshot({ path: './OMS-950_bug_1.png', type: 'png', scale: 'device' });
}
```

---

## Multi-shot Rules

| Scenario | Shot 1 | Shot 2 |
|----------|--------|--------|
| Table + detail panel | Close panel → annotate table | Open panel → annotate field |
| Table + filter dropdown | Close dropdown → annotate table | Open dropdown → annotate option |
| Two tabs/pages | Navigate to A → annotate | Navigate to B → annotate |

- Change state BETWEEN shots
- Each shot annotates ONLY what's visible
- NEVER annotate behind an overlay


---

## Trimming Allure Video

When using allure video as evidence:

1. Read allure log → find "Start recording screen" timestamp (= video 0:00)
2. Identify the LAST relevant step/verify for this bug (not the full test)
3. Calculate: trim_seconds = (last_step_time - recording_start) + 3s buffer
4. `ffmpeg -y -i <source> -t <trim_seconds> -c copy <output>`
5. Verify with `ffprobe`: confirm output duration ≈ trim_seconds
6. NEVER guess timestamps — always derive from the log

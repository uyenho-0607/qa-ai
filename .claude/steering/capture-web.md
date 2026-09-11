# Capture — Web Targets

Playwright mechanics for `capture-mechanics.md`. Driver: `.claude/steering/playwright-rule.md`.

Destination and file name rules: `capture-mechanics.md` § File name.

## Viewport — first

Pack § Targets `Viewport` = `desktop` → run the probe below. A fixed size → set `vw`/`vh` from that row and
call `page.setViewportSize({ width: vw, height: vh })` inside `run_code_unsafe` — skip the probe.

```js
const { width, height } = await page.evaluate(() => ({ width: window.screen.width, height: window.screen.height }));
const vw = width  >= 1280 ? width  : 2560;
const vh = height >= 720  ? height : 1440;
await page.setViewportSize({ width: vw, height: vh });
```

The resulting `vw`/`vh` feeds `recordVideo.size` below.

## Bring the element into view

```js
// vertical
await page.locator('{selector}').scrollIntoViewIfNeeded({ timeout: 5000 });
await page.waitForTimeout(300);
// horizontal, for a wide table — selector from the platform pack § Stack quirks
await page.evaluate((sel) => {
  const c = document.querySelector(sel);
  if (c) c.scrollLeft = c.scrollWidth;
}, '{scroll container selector}');
await page.waitForTimeout(500);
```

Scroll before labelling. Never label an element sitting behind an overlay.

## Checkpoint label — one per `**Exp:**` checkpoint

Label availability is the platform pack's § Label overlay answer, per `capture-mechanics.md` § Label; this
section is only the injection mechanics.

The label must be readable on its own, without the tracker file open next to it: a viewer watching just the
recording should be able to tell what was checked, whether it held, and — on a failure — what actually
happened. Color carries the verdict at a glance; text carries the detail.

- **`status`** drives the background color. `'pass'` → `#0a7` (green). `'fail'` → `#c0392b` (red).
  `'blocked'` → `#c77c00` (amber). Never leave a failing checkpoint on the green default.
- **`label`** text: `` `{✅|❌|🚫} {TC-ID} · c{N} · {what was checked}` `` on a pass, plus
  `` ` — expected {X}, got {Y}` `` appended on a fail or block — the actual-vs-expected clause is what makes a
  failure legible without narration. Keep the whole line short enough to fit one row at 14px; trim the
  checked-item description before trimming the expected/got clause.

```js
await page.evaluate(({ label, replace, status }) => {
  if (replace) document.querySelectorAll('[data-exec-label]').forEach(n => n.remove());
  const color = { pass: '#0a7', fail: '#c0392b', blocked: '#c77c00' }[status] || '#0a7';
  const d = document.createElement('div');
  d.setAttribute('data-exec-label', '1');
  d.textContent = label;
  d.style.cssText = `position:fixed;left:12px;z-index:99999;background:${color};color:#fff;`
    + 'padding:6px 12px;border-radius:4px;font:bold 14px sans-serif;white-space:nowrap;'
    + `top:${12 + document.querySelectorAll('[data-exec-label]').length * 34}px;`;
  document.body.appendChild(d);
}, {
  label: '✅ {TC-ID} · c{N} · {what was checked}',                                    // pass
  // label: '❌ {TC-ID} · c{N} · {what was checked} — expected {X}, got {Y}',         // fail
  // label: '🚫 {TC-ID} · c{N} · {what was checked} — blocked: {reason}',             // blocked
  replace: true,
  status: 'pass',   // 'pass' | 'fail' | 'blocked' — set from the checkpoint's actual verdict, never hardcoded
});
```

- **Video** — `replace: true`. Each label clears the last; the recording separates the checkpoints.
- **Screenshot** — `replace: false` after the first, so every checkpoint the frame proves appears in it.

## Element annotation — a bug or a fix, pointed at

`{selector}` is CSS — translate the caller's `id=`/`desc=`/`text=` per the pack § Target grammar first.

**Always clear the previous annotation before applying the next one** — the border/background is written
directly onto the target element's inline style and the label is a floating `<div>`, neither of which the
browser removes on its own. Without the clear step, annotations from earlier TCs in the same session persist
and stack into later frames. The clear pass runs unconditionally, even before the first annotation of a run
(a no-op then).

```js
await page.evaluate(({ selector, label, color }) => {
  // Clear step — always first, regardless of whether anything was previously annotated.
  document.querySelectorAll('[data-exec-annotation]').forEach(n => {
    n.style.border = '';
    n.style.backgroundColor = '';
    n.removeAttribute('data-exec-annotation');
  });
  document.querySelectorAll('[data-exec-annotation-label]').forEach(n => n.remove());

  const el = document.querySelector(selector);
  if (!el) throw new Error('annotation selector unresolved: ' + selector);
  el.setAttribute('data-exec-annotation', '1');
  el.style.border = `3px solid ${color}`;
  el.style.backgroundColor = color === 'red' ? 'rgba(255,0,0,0.12)' : 'rgba(0,180,0,0.12)';
  const d = document.createElement('div');
  d.setAttribute('data-exec-annotation-label', '1');
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
await page.screenshot({ path: '{dest}{stem}_{target}.png', type: 'png', scale: 'device' });
```

Where one assertion needs two states — a table and its detail panel, a closed and an open dropdown, two
pages — change the state between frames and label only what is visible in each.

## Pointer overlay — recordings only

Playwright's video does not draw the mouse, so the pointer is drawn in the page. Run this on the **recording
context**, before its first page — never on `page`, which is what screenshots come from.

```js
const POINTER = { size: 28, glide: 110 };
await ctx.addInitScript(({ size, glide }) => {
  const mount = () => {
    if (document.querySelector('[data-exec-pointer]')) return;
    const st = document.createElement('style');
    st.textContent = '@keyframes exec-pop{60%{opacity:.7}'
      + 'to{transform:translate(-50%,-50%) scale(1.9);opacity:0}}';
    document.head.appendChild(st);

    const p = document.createElement('div');
    p.setAttribute('data-exec-pointer', '1');
    p.innerHTML = `<svg width="${size}" height="${size}" viewBox="0 0 40 40">
      <g fill="#f4849e" stroke="#fff" stroke-width="1.8">
        <ellipse cx="12.2" cy="14.4" rx="4.1" ry="5.1" transform="rotate(-16 12.2 14.4)"/>
        <ellipse cx="20" cy="11.4" rx="4.2" ry="5.3"/>
        <ellipse cx="27.8" cy="14.4" rx="4.1" ry="5.1" transform="rotate(16 27.8 14.4)"/>
        <ellipse cx="32.6" cy="22.4" rx="3.6" ry="4.3" transform="rotate(28 32.6 22.4)"/>
        <path d="M20 33.6c-5.6 0-9.8-3-9.8-7.1 0-3.7 4-6.6 9.8-6.6s9.8 2.9 9.8 6.6c0 4.1-4.2 7.1-9.8 7.1z"/>
      </g></svg>`;
    p.style.cssText = 'position:fixed;left:0;top:0;z-index:2147483647;pointer-events:none;opacity:0;'
      + `margin:${-size * 0.55}px 0 0 ${-size * 0.5}px;`
      + `transition:transform ${glide}ms cubic-bezier(.33,.66,.35,1);`;
    document.body.appendChild(p);

    // Carry the last position across a navigation — otherwise the pointer re-mounts hidden and
    // every post-navigation frame loses it until the next mouse action.
    const at = (x, y, animate) => {
      p.style.transition = animate ? `transform ${glide}ms cubic-bezier(.33,.66,.35,1)` : 'none';
      p.style.opacity = '1';
      p.style.transform = `translate(${x}px, ${y}px)`;
    };
    try {
      const seen = (sessionStorage.getItem('exec-pointer-at') || '').split(',');
      if (seen.length === 2) {
        at(+seen[0], +seen[1], false);
        requestAnimationFrame(() => { p.style.transition = `transform ${glide}ms cubic-bezier(.33,.66,.35,1)`; });
      }
    } catch (e) {}

    addEventListener('mousemove', e => {
      at(e.clientX, e.clientY, true);
      try { sessionStorage.setItem('exec-pointer-at', `${e.clientX},${e.clientY}`); } catch (err) {}
    }, true);

    const ripple = (x, y, delay) => {
      setTimeout(() => {            // fire when the pointer arrives, not before it
        const d = size * 1.9;
        const r = document.createElement('span');
        r.style.cssText = 'position:fixed;z-index:2147483646;pointer-events:none;border-radius:50%;'
          + `left:${x}px;top:${y}px;width:${d}px;height:${d}px;border:2.5px solid #f0879f;`
          + 'transform:translate(-50%,-50%) scale(.25);'
          + 'animation:exec-pop .5s cubic-bezier(.2,.7,.3,1) forwards;';
        document.body.appendChild(r);
        setTimeout(() => r.remove(), 520);
      }, delay);
    };

    addEventListener('mousedown', e => ripple(e.clientX, e.clientY, glide), true);

    // A raw in-page `element.click()` — the fallback whenever a locator won't resolve and the driver
    // calls `.click()` on the DOM node directly — never fires mousemove/mousedown, so the pointer above
    // would otherwise sit at opacity:0 for the whole capture. `isTrusted` is false only on a script-fired
    // event (real input, whether a person's or Playwright's own CDP-simulated click, is always trusted),
    // so this path fires exactly when the mousedown listener above did not.
    addEventListener('click', e => {
      if (e.isTrusted) return;
      const r = e.target.getBoundingClientRect();
      const x = r.left + r.width / 2, y = r.top + r.height / 2;
      at(x, y, false);
      ripple(x, y, 0);
    }, true);
  };
  if (document.readyState === 'loading') addEventListener('DOMContentLoaded', mount);
  else mount();
}, POINTER);
```

- **Hover before you type.** `fill()`, `press()` and `selectOption()` reach the element through focus, not
  the mouse — the pointer would sit still while a field fills itself. Precede each with
  `await rec.locator('{selector}').hover()` so it walks over first. `click()` already moves the mouse.
- `addInitScript` re-runs on every document, so the pointer survives navigation and reload inside the replay.
  Its position rides along in `sessionStorage`, same-origin only — a cross-origin hop drops it, and it
  reappears at the next mouse action.
- `data-exec-pointer` is its own attribute — the § Checkpoint label and § Element annotation clear passes
  never touch it, and must not be widened to.
- The glyph is inline SVG, not an emoji: a headless Chromium is not guaranteed an emoji font, and a missing
  one records as an empty box.

## Video — one replay pass per group

Replay-pass rule: `capture-mechanics.md` § When to capture. Playwright mechanics for it:

```js
const state = await page.context().storageState();
const ctx = await page.context().browser().newContext({
  storageState: state,
  recordVideo: { dir: '{dest}', size: { width: vw, height: vh } },
  viewport: { width: vw, height: vh },
  screen:   { width: vw, height: vh }
});
// § Pointer overlay — always, and only here
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
ffmpeg -y -i "<webm>" -c:v libx264 -preset fast -crf 23 "{dest}{stem}_{target}.mp4"
```

Keep the `.webm` until the user confirms the `.mp4`. One video context at a time — see `playwright-rule.md` §
Session Reset for the two-independent-sessions exception (concurrency TCs, not two recordings).

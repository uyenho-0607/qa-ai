# Capture Mechanics

**Follow `.claude/steering/playwright-rule.md`: `browser_navigate` once per session, `browser_run_code_unsafe` for everything else. Substitute `{KEY}`, `{ids}` and `{slug}` with real values before running any snippet below — they are placeholders, not code.**

---

## Label overlay

- **Video** — pass `replace: true`. Each label clears the last; the recording separates the checkpoints.
- **Screenshot** — pass `replace: false` for every checkpoint after the first, so all of them appear in the one frame.

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
}, { label: '{TC-ID} | {what is verified}', replace: true });
```

## Screenshot

1. Scroll the asserted element into view.
2. Inject the label overlay.
3. `await page.screenshot({ path: '<group path>', type: 'png', scale: 'device' })`

`<group path>` is `evidence/{KEY}/` plus the Evidence Groups table's File column — `TC_{ids}_{slug}.png`.
Never invent a name and never rename after the fact; the name lists the group's TC-IDs.

## Video — one replay pass per group

The recording is a replay, not the test. Test the group first, then replay every step inside one recording context at a steady pace. Restore the starting precondition first only where the test changed state — a read-only flow replays as-is.

Enter the context knowing every step and every locator. Resolving anything inside it puts the agent's own latency into the video.

```js
const { width, height } = await page.evaluate(() => ({ width: window.screen.width, height: window.screen.height }));
const vw = width  >= 1280 ? width  : 2560;
const vh = height >= 720  ? height : 1440;
const state = await page.context().storageState();

const ctx = await page.context().browser().newContext({
  storageState: state,
  recordVideo: { dir: 'evidence/{KEY}/', size: { width: vw, height: vh } },
  viewport: { width: vw, height: vh },
  screen:   { width: vw, height: vh }
});
const rec = await ctx.newPage();
try {
  // Replay the group's steps, injecting each TC's label at its assertion moment
  const webm = await rec.video().path();
  return webm;
} finally {
  await ctx.close();   // video file is only finalized on close
}
```

Convert and name it:

```bash
ffmpeg -y -i "<webm>" -c:v libx264 -preset fast -crf 23 "evidence/{KEY}/TC_{ids}_{slug}.mp4"
```

- Take `TC_{ids}_{slug}` verbatim from the Evidence Groups table's File column — see
  `.claude/skills/manual-exec-design/references/evidence-rules.md` § Naming.
- Keep the `.webm` until the user confirms the `.mp4`.
- For EMS Trader, transfer `sessionStorage` into the recording context and reload — see `.claude/skills/capture-evidence/video-guide.md`.

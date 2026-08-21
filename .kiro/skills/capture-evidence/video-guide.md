# Video Guide — Two-Browser Recording

## Why two browsers?

First browser = already open from exploration. Second browser = clean recording context. Everything was already confirmed, so the recording is smooth.

---

## EMS Trader Auth Transfer

```js
// From first browser — get ALL auth state
const state = await page.context().storageState();
const sessionData = await page.evaluate(() => {
  const ss = {};
  for (let i = 0; i < sessionStorage.length; i++) {
    ss[sessionStorage.key(i)] = sessionStorage.getItem(sessionStorage.key(i));
  }
  return ss;
});
```

Restore in new context:
```js
if (Object.keys(sessionData).length > 0) {
  await newPage.evaluate((d) => {
    for (const [k, v] of Object.entries(d)) sessionStorage.setItem(k, v);
  }, sessionData);
  await newPage.reload();
  await newPage.waitForLoadState('networkidle');
}
```

---

## Full Recording Template

```js
async (page) => {
  const { width, height } = await page.evaluate(() => ({
    width: window.screen.width, height: window.screen.height
  }));
  const vw = width >= 1280 ? width : 2560;
  const vh = height >= 720 ? height : 1440;
  const state = await page.context().storageState();
  const sessionData = await page.evaluate(() => {
    const ss = {};
    for (let i = 0; i < sessionStorage.length; i++) {
      ss[sessionStorage.key(i)] = sessionStorage.getItem(sessionStorage.key(i));
    }
    return ss;
  });

  const browser = page.context().browser();
  const newContext = await browser.newContext({
    storageState: state,
    recordVideo: { dir: '/tmp/', size: { width: vw, height: vh } },
    viewport: { width: vw, height: vh },
    screen: { width: vw, height: vh }
  });
  const newPage = await newContext.newPage();

  try {
    await newPage.goto(TARGET_URL);
    await newPage.waitForLoadState('networkidle');
    if (Object.keys(sessionData).length > 0) {
      await newPage.evaluate((d) => {
        for (const [k, v] of Object.entries(d)) sessionStorage.setItem(k, v);
      }, sessionData);
    }
    await newPage.waitForTimeout(1000);

    // === EXECUTE PRE-PLANNED STEPS ===

    // At annotation moment:
    await newPage.evaluate(({ selector, label, color }) => {
      const el = document.querySelector(selector);
      if (!el) return;
      el.style.border = `3px solid ${color}`;
      el.style.backgroundColor = color === 'red' ? 'rgba(255,0,0,0.12)' : 'rgba(0,180,0,0.12)';
      const labelDiv = document.createElement('div');
      labelDiv.textContent = label;
      labelDiv.style.cssText = `position:absolute;z-index:99999;background:${color};color:white;padding:4px 8px;border-radius:4px;font-size:13px;font-weight:bold;white-space:nowrap;`;
      const rect = el.getBoundingClientRect();
      labelDiv.style.top = `${window.scrollY + rect.top - 28}px`;
      labelDiv.style.left = `${window.scrollX + rect.left}px`;
      document.body.appendChild(labelDiv);
    }, { selector: '[data-testid="target"]', label: '❌ Bug visible here', color: 'red' });
    await newPage.waitForTimeout(2000);

    const videoPath = await newPage.video().path();
    return videoPath;
  } finally {
    await newContext.close();
  }
}
```

---

## Convert + Confirm

```bash
ffmpeg -y -i "recorded.webm" -c:v libx264 -preset fast -crf 23 "./OMS-950_bug_1.mp4"
```

1. Convert `.webm` → `.mp4`
2. Report file path + filename to calling skill
3. Wait for user confirmation before deleting `.webm`
4. First browser stays alive

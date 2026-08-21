---
name: capture-evidence
description: Capture screenshot or video evidence for bug reports and verifications via Playwright MCP. Forces reading playwright-rule.md before any browser interaction. Use when capturing evidence for bugs, verifications, or any time screenshots/video are needed for Jira.
---

# Capture Evidence

Execution skill. Receives structured input, outputs file paths.

## Pre-Flight
⛔ **FORCE READ:** `.claude/steering/playwright-rule.md`

## Interface

**Input:**
```
type: screenshot | video
ticket_key: "OMS-950"

For screenshot:
  screenshots: [{ annotations: [selector...], color: "red"|"green", label: "text" }]
  api_overlay (BE bugs): { url, status, body }

For video:
  steps: [{ action, selector, value?, url? }]
  annotate_at_step: N
  annotate_element: selector
  color / label
```

**Output:**
```
file_paths: ["./OMS-950_bug_1.png"]
filenames: ["OMS-950_bug_1.png"]
```

## File Naming
`{ticket_key}_{purpose}_{N}.{ext}`
- Purpose: `bug` or `verify`
- Re-captures: `_v2`, `_v3`

## Screenshot Flow
⛔ Read `screenshot-guide.md` first.

1. Set dynamic viewport (fallback 2560x1440)
2. Scroll to target if off-screen
3. Inject annotation label overlay
4. For BE bugs: inject API overlay
5. `page.screenshot({ path, type: 'png', scale: 'device' })`

## Video Flow
⛔ Read `video-guide.md` first.

1. Get auth state + screen size
2. Create context with `recordVideo`
3. Navigate + restore session
4. Execute steps
5. At bug moment: inject annotation
6. Close context → convert webm → mp4
7. Report paths

## Hard Rules
- ONLY use `browser_navigate` + `browser_run_code_unsafe`
- Never use individual MCP tools (browser_click, etc.)
- Never annotate behind overlay
- Never re-explore DOM — use passed selectors
- Never auto-delete — wait for confirmation
- Always `scale: 'device'` on screenshots
- Always scroll BEFORE annotate
- Always close recording context in `finally`
- For EMS: transfer storageState AND sessionStorage

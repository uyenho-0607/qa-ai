---
name: exec-workflow
description: End-to-end manual SIT execution workflow — fetch Jira, collect TCs, design exec plan, run tests, paste evidence into a doc, and report. Use when user says "run full workflow", "exec workflow", /exec-workflow.
---

# Exec Workflow

Orchestrates the full manual SIT cycle for a Jira ticket in one invocation. Each phase delegates to an
existing skill; this file owns only the sequencing, the setup questions, and the handoffs between them.

## Contract

- **Args:** `{KEY}` — e.g. `AO-925`
- **Reads:** nothing beyond what each delegated skill reads
- **Writes:** whatever each delegated skill writes, plus the evidence doc
- **Gate mode:** set once at Phase 0; applies to every phase-level gate in the workflow

## Phase 0 — Setup

Ask the user these questions in **one message**, in this order. Wait for all answers before continuing.

```
1. Gates on or off?
   Gates pause at each design phase for your confirmation before continuing.
   Default: off (auto-continue through every gate).

2. Evidence destination — pick one:
   a. Create a new Google Doc (default — I create it and set the permission)
   b. Paste into your Google Doc — give me the link
   c. Upload to a Google Drive folder — give me the link

3. Annotations on screenshots?
   Default: yes — each capture is labelled with its TC id and checkpoint.
```

Record:
- `gates` — `on` | `off` (default `off`)
- `evidence_dest` — `new-doc` | `user-doc:{url}` | `drive:{url}` (default `new-doc`)
- `annotations` — `yes` | `no` (default `yes`)

Done when: all three are recorded.

## Phase 1 — Evidence destination setup

Act on `evidence_dest`:

### `new-doc`
Create a Google Doc titled `[{KEY}] SIT Evidence` with `mcp__google-docs__createDocument`.
Set permission to anyone-with-link reader with `mcp__google-docs__setFilePermission`.
Record the doc ID and URL. Proceed to Phase 2.

### `user-doc:{url}`
Extract the doc ID from the URL.
Test write access: attempt `mcp__google-docs__appendText` with a single space, then delete it with
`mcp__google-docs__deleteRange`. If that succeeds → use the doc directly; record its ID. If it fails with a
permission error → create an internal working doc titled `[{KEY}] SIT Evidence (working copy)`, record both
IDs as `working_doc` and `target_doc`. At Phase 6 the working copy will be merged into the target doc.

### `drive:{url}`
Extract the folder ID from the URL.
Test write access by uploading a 1-byte probe file with `mcp__google-docs__uploadFile`, then delete it.
If that succeeds → record the folder ID. If it fails → inform the user and ask for a folder with write access
or fall back to `new-doc`.

Done when: the evidence destination is confirmed reachable and its ID is recorded.

## Phase 2 — Fetch Jira and collect test cases

Check whether `tasks/{KEY}/base/jira.md` exists. Missing → invoke `jira-retriever` with `{KEY} save`.
Check whether `tasks/{KEY}/base/tc.md` exists. Missing → invoke `collect-testmo-cases` with `{KEY} save no-gate`.

Both files already exist → skip fetching and proceed.

Done when: both `tasks/{KEY}/base/jira.md` and `tasks/{KEY}/base/tc.md` exist.

## Phase 3 — Design the exec plan

Invoke `manual-exec-design-v2` with `{KEY}`.

The design skill runs its own phases and gates internally. When it reaches its Phase 9 GATE it will present
blockers, Tier-1 results, added coverage, discrepancies and open questions and stop for user approval.

If `gates = off`: after `manual-exec-design-v2` presents its Phase 9 gate summary, auto-approve and continue
unless there are **Blockers** — blockers always stop regardless of gate mode, because they block specific TCs
and the user must decide whether to proceed without them.

Done when: `tasks/{KEY}/exec/exec-v2.md` exists and the design gate is resolved.

## Phase 4 — Run the tests

Invoke `manual-exec-run-v2` with `{KEY}`.

If `annotations = yes`: pass this context to the run so every capture is labelled with its TC id and
checkpoint id. The run skill uses this flag when calling `capture-evidence`.

If `gates = off`: the run skill's own wave-start confirmations are skipped; it executes wave by wave without
stopping. Failures still pause — a failed TC always requires a human decision before the next TC in the same
wave.

Done when: `tasks/{KEY}/exec/exec-v2.md` carries a result on every result line (no `⏳ PENDING` remaining), and
`tasks/{KEY}/exec/report-v2.md` exists.

## Phase 5 — Paste evidence into the doc

### `new-doc` or `working-doc`

Read `tasks/{KEY}/exec/report-v2.md` to get the full TC list and their case names.
Scaffold the doc with one heading per case name using `mcp__google-docs__appendMarkdown` — one `## {name}`
heading followed by a blank paragraph for each TC, in the order the report lists them.

Then for each TC that has captured evidence under `tasks/{KEY}/exec/evidence/`:

1. Find the heading in the doc with `mcp__google-docs__findElement`.
2. Insert each image or video link immediately after the heading.
   - Images (`.png`): `mcp__google-docs__insertImage` at the heading's `endIndex + 1`, width 450pt,
     height proportional. For device screenshots (portrait) use width 220pt.
   - Videos (`.mp4`): insert as a Drive link using `mcp__google-docs__insertRichLink` — videos cannot be
     embedded inline in Docs.
3. If `annotations = yes`, the file names already carry the TC id and checkpoint id — no further labelling
   needed in the doc.

TCs with no evidence (skipped, human-executable, blocked) get the heading only — leave the blank paragraph.

### `drive:{folder_id}`

For each file under `tasks/{KEY}/exec/evidence/`, upload it to the Drive folder using
`mcp__google-docs__uploadFile` with the folder as parent. Preserve the file names exactly — they encode the
TC id and checkpoint id.

No doc scaffolding needed for a Drive destination.

### Merge working copy → target doc

Only when `user-doc` was provided and a `working_doc` was created:

For each inserted image in the working doc, read its `contentUri` from `inlineObjects` via
`mcp__google-docs__readDocument format=json`, then `mcp__google-docs__insertImage` that URI as `imageUrl`
into the target doc at the matching index. Delete the working doc when all images are transferred.

Done when: every executed TC's evidence appears in the destination, and any working copy is deleted.

## Phase 6 — Report

Present a concise summary to the user:

```
## {KEY} — SIT Run Complete

**Pass rate:** {passed}/{total} ({pct}%)
**Evidence:** {doc url | drive folder url}

**Bugs found:** {n} — {list of bug descriptions, one per line, or "none"}

**Needs manual execution ({n} TCs):**
These were skipped by the agent and require a human tester to execute:
- {TC id} · {title} — {one-line reason}

**Blocked / skipped by environment ({n} TCs):**
These could not run due to data or environment constraints — no human action needed:
- {TC id} · {title} — {one-line reason}

**Open items:** {anything still needing a human decision}
```

If any TC still has `⏳ PENDING` at this point, list them explicitly as "not executed — reason unknown" and
ask the user whether to retry or close.

Done when: the summary is presented and the user has no outstanding questions.

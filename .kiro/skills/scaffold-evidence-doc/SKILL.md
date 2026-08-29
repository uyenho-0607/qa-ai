---
name: scaffold-evidence-doc
description: Scaffold a Google Doc of Testmo case names — one heading per case, blank space beneath for pasting screenshots. Use when asked for a test evidence doc for a ticket, /evidence-doc.
---

# Scaffold Evidence Doc

Build the empty container a tester fills by hand. This makes the document; `capture-evidence` makes the images; `docs-media` puts them in.

**Done when:** a Google Doc exists holding one block per linked Testmo case, and its link is delivered.

## Contract

| | |
|---|---|
| **Args** | `{KEY}` [, platform] [, Drive folder URL] |
| **Reads** | `.kiro/steering/testmo.md` — Testmo project ids and Configuration names |
| **Testmo** | `testmo_find_cases_by_issue` — names only, no per-case fetch |
| **Docs** | `mcp__google-docs__createDocument` |
| **Writes** | one Google Doc; no repo file |

Case names come from the repository, not from a run: `testmo_list_run_results` returns only tests that already carry a submitted result, which is empty at the moment an evidence doc is needed.

---

## 1. Collect case names

`tasks/{KEY}/base/tc.md` exists → read the names from its `## ` headings and skip the Testmo call. Those headings read `{KEY}_TC-NN — {name}`; keep only the part after the em dash.

Otherwise resolve `{KEY}`'s project id from `.kiro/steering/testmo.md` and call `testmo_find_cases_by_issue(projectId, issueKey: "{KEY}")`. Parse every `"<caseId> <caseName>"` entry, keeping its folder grouping and the response's order.

No cases returned → report that and stop. Offer `collect-testmo-cases` or a folder name to search instead, and invent nothing.

**Done when:** every case name is recorded with its folder, the total is stated, and no name still carries a TC-id prefix.

## 2. Confirm scope

Platform tags come from the TC set, not from a guess: read the `Configuration` values in `tasks/{KEY}/gen/manual-tcs.md` when it exists, and propose every distinct value. A set spanning platforms keeps all of them — `Android app; iOS app` is one valid tag, not a choice between two. Every name must match `.kiro/steering/testmo.md`.

Present the folder groups and the total, then ask in one message:

```
{KEY} — [n] cases across [n] folders
Platform tag for the title: [proposed]
Scaffold the doc? (yes / adjust)
```

**GATE — wait for confirmation before creating the doc.**

## 3. Create the doc

Title: `[{KEY}] {Jira summary} ({Platform tag})`
Example: `[AO-306] [OTC][MobileApp] Personal Onboarding (Android app; iOS app)`

Take the summary from the `## Title` line of `tasks/{KEY}/base/jira.md` when it exists; otherwise invoke `jira-retriever` with `{KEY}`.

One `createDocument` call carries the whole scaffold:

- `contentFormat: "raw"` — **required.** Markdown collapses consecutive newlines into a single paragraph break, which erases the space the tester pastes into.
- `initialContent` — one block per case in Step 1 order: the name, then two blank lines. Every block carries them, the last one included.
- `parentFolderId` — the folder id parsed from the Drive URL, when one was given.

The case name stands alone: no numbering, no `Status:` line, no `Evidence:` label.

**Done when:** block count equals the Step 1 total.

## 4. Deliver

Report the doc link, the case count, and the platform tag.

A Drive folder URL arrives only after the doc exists → `mcp__google-docs__moveFile` with that folder id, then say where it landed.

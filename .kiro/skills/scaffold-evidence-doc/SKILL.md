---
name: scaffold-evidence-doc
description: Scaffold a Google Doc of Testmo case names — one plain-paragraph section per case, blank space beneath for pasting screenshots. Use when asked for a test evidence doc for a ticket, /evidence-doc.
---

# Scaffold Evidence Doc

Build the empty container a tester fills by hand. This makes the document; `capture-evidence` makes the images; `docs-media` puts them in.

**Done when:** a Google Doc exists holding one block per linked Testmo case, and its link is delivered.

## Contract

| | |
|---|---|
| **Args** | `{KEY}` [, platform] [, Drive folder URL] |
| **Reads** | `awk '/^## /{p = /Configurations by Project/} p' .kiro/steering/testmo.md` — valid platform tag names; `tasks/{KEY}/base/tc.md`, `tasks/{KEY}/gen/manual-tcs.md`, `tasks/{KEY}/base/jira.md` |
| **Docs** | `mcp__google-docs__createDocument`, `mcp__google-docs__moveFile` |
| **Producers** | `tasks/{KEY}/base/tc.md` missing → `/collect-testmo-cases {KEY} save`; `tasks/{KEY}/base/jira.md` missing → `/jira-retriever {KEY} save` (see project-config.md § Producers) |
| **Writes** | one Google Doc; no repo file |

Case names come from the Testmo case repository, not from a run.

---

## 1. Collect case names

`tasks/{KEY}/base/tc.md` exists → read the names from it:

```
grep -n '^#### \|^### ' tasks/{KEY}/base/tc.md
```

Each `#### TC-{testmoId} · {name}` line names one case — split on the middle dot `·` and keep the part after it. Each case's folder is the nearest preceding `### {folder} ({n} cases)` line.

Missing → stop and name `/collect-testmo-cases {KEY} save`.

**Done when:** every case name is recorded with its folder, the total is stated, and no name still carries a TC-id prefix.

## 2. Confirm scope

Platform tags come from the TC set, not from a guess: read the single `Configuration` header field in `tasks/{KEY}/gen/manual-tcs.md` when it exists:

```
grep -m1 '\*\*Configuration:\*\*' tasks/{KEY}/gen/manual-tcs.md
```

Propose that value verbatim — a set spanning platforms already reads as one `;`-joined list, e.g. `Android app; iOS app`, not a choice between two. Every name must match `.kiro/steering/testmo.md` § Configurations by Project.

Present the folder groups and the total, then ask in one message:

```
{KEY} — [n] cases across [n] folders
Platform tag for the title: [proposed]
Scaffold the doc? (yes / adjust)
```

**GATE — wait for confirmation before creating the doc.**

## 3. Create the doc

Title: `[{KEY}] {Jira summary} ({Platform tag})`
Example: `[{KEY}] [Module][Surface] Personal Onboarding (Admin BO; Android app)`

Take the summary from `tasks/{KEY}/base/jira.md`:

```
grep -A1 '^## Title' tasks/{KEY}/base/jira.md
```

Missing → stop and name `/jira-retriever {KEY} save`.

One `createDocument` call carries the whole scaffold:

- `contentFormat: "raw"` — **required.** Markdown collapses consecutive newlines into a single paragraph break, which erases the space the tester pastes into.
- `initialContent` — one block per case in Step 1 order: the name, then two blank lines. Every block carries them, the last one included.
- `parentFolderId` — the folder id parsed from the Drive URL, when one was given.

The case name stands alone: no numbering, no `Status:` line, no `Evidence:` label.

`scripts/evidence_upload.py` § `_is_section_boundary` ends a section at the next paragraph carrying text. A stray line steals the anchor.

Reserved, written by `manual-exec-run` only — never scaffold them:

- `FAILED` `PASSED` `BLOCKED` `PENDING` `SKIPPED` — whole line
- lines starting `Actual:` `Expected:` `Note:` `Bug:` `Evidence:`

**Done when:** block count equals the Step 1 total.

## 4. Deliver

Report the doc link, the case count, and the platform tag.

A Drive folder URL arrives only after the doc exists → `mcp__google-docs__moveFile` with that folder id, then say where it landed.

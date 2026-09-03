---
name: jira-retriever
description: Retrieve structured content from a Jira ticket for downstream test design — description, ACs, sub-tasks, comments, linked issues, images, and Figma links. Use when another skill needs full Jira ticket context, or when user says "fetch ticket", "get ticket content", "retrieve Jira", /jira-retriever.
---

# Jira Retriever

Fetch everything a Jira ticket contains. Done when all content is captured and every image is readable.

## Contract

- **Arg:** `{KEY}` [, `save`] [, `skip-figma`]
- **Writes:** `tasks/{KEY}/base/jira.md` — **only when `save` is given**
- **Default:** return the Output block below in chat; write no file
- **Attachments:** `tasks/{KEY}/base/attachments/`, regardless of `save`, when the ticket or a sub-task carries a matching attachment
- **Delegates:** `figma-retriever` — Step 4, unless `skip-figma`

## Steps

### 1. Fetch ticket

`grep -m1 cloudId .kiro/steering/jira.md` to get `cloudId`.

Use the Atlassian MCP tool to fetch the issue. Pass `fields`:

```
fields: ["summary", "description", "status", "assignee", "reporter", "issuetype",
         "created", "updated", "subtasks", "issuelinks", "attachment", "comment", "customfield_10327"]
```

Never fall back to `*all`.

### 2. Fetch ALL sub-tasks details

> Fetch details with:

```
fields: ["summary", "status", "issuetype", "description", "comment", "attachment", "customfield_10327"]
```

Extract: title, type, status, ACs (if present), description, comments, and `customfield_10327` value (used only in Step 4 to scan for Figma links — no Output section carries it).

If a call fails: note `⚠️ [KEY]: Could not retrieve — [reason]` and continue.

Done when: **ALL sub-task** details fetched.

### 3. Download images

Check attachments on **both the parent ticket and every sub-task**. For any attachment with `mimeType: image/*` or `video/*`, run once for the parent:

```bash
bash .kiro/skills/jira-retriever/download-jira-attachments.sh {KEY}
```

then once per sub-task carrying a matching attachment, passing `{KEY}` as the destination:

```bash
bash .kiro/skills/jira-retriever/download-jira-attachments.sh <SUB-KEY> {KEY}
```

Both save into `tasks/{KEY}/base/attachments/`. After each run, read `tasks/{KEY}/base/attachments/comment-images.txt` to map each image to its comment context.

If the script fails: note which files could not be downloaded and continue with text-only context.

### 4. Fetch Figma

Skip this step when `skip-figma` was passed, or when `tasks/{KEY}/base/figma/figma-snapshot.md` exists and `tasks/{KEY}/base/figma/figma-screenshots/` has ≥1 PNG.

Otherwise, find `figma.com` URL by scanning:
- Parent ticket: description and all comments
- Every sub-task fetched in Step 2: description, all comments, and `customfield_10327` value

Per link extract: full URL, file key, node-id query param (or `none`), and source (`description` / `comment` / `sub-task [KEY]`). Deduplicate — if the same URL appears in multiple places, list it once and note all sources. Write all links to the `## Figma Links` section. No links found anywhere: write `None`.

- Links found → invoke `figma-retriever` with `{KEY}` and the Figma URL(s).
- Links not found → ask "No Figma links found. Give the links?" → link given → invoke `figma-retriever`. Non-interactive caller → record "no Figma links" and continue.

Done when: `skip-figma` passed, or no links exist and that is recorded, or `figma-snapshot.md` exists with `figma-screenshots/` holding ≥1 PNG. Any failure noted as a blocker.

### 5. Read images

Call `Read` on each downloaded file:
- Jira attachments: `tasks/{KEY}/base/attachments/`
- Extracted video frames: `tasks/{KEY}/base/attachments/*-frames/`
- Figma screenshots: `tasks/{KEY}/base/figma/figma-screenshots/`

Describe what each shows — UI states, error states, or before/after behaviour relevant to the ACs. Note any discrepancies between Figma designs and the requirements (ACs, BRs, error messages).

## Output

Both paths use the structure below. `save` → write it to `tasks/{KEY}/base/jira.md`, then say "Written to `tasks/{KEY}/base/jira.md`" No `save` → return it in chat.

```markdown
# Jira: [KEY]

## Title
[summary]

## Status
[status] | Assignee: [name] | Reporter: [name]

## Description
[description]

## Business Requirements
- BR-n: [requirement]

## Acceptance Criteria
- AC-n: [criterion]   *(mark `derived` when taken from the description)*

## Error Messages
- ERR-n: "[exact string]"  (source: [description | comment by [author], [date]])

## Out of Scope
- [item as the ticket states it]

## Linked Issues
- [KEY]: [summary] ([link type])

## Sub-tasks
### [SUB-KEY]: [title]
- Type: [type] | Status: [status]
- ACs: [if present, list them; otherwise omit]

## Figma Links
- [full URL] — file key: [key] | node-id: [id | none] (source: [description | comment | sub-task KEY])

## Visual Context
- [filename]: [what it shows]

## Figma Discrepancies
- [Figma element / screen]: [what Figma shows] vs [what AC/BR/ERR states] (source: [AC-n | BR-n | ERR-n])

## Open Items from Comments
- [unresolved question or pending decision] (by [author], [date])

```

Every heading above is written verbatim, including when the ticket words it differently — downstream skills match on the exact text. Attribute a source on the item, never by extending the heading. A section the ticket has nothing for gets the heading and `None`.

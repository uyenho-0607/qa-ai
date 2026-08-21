---
name: jira-retriever
description: Retrieve structured content from a Jira ticket for downstream test design — description, ACs, sub-tasks, comments, linked issues, images, and Figma links. Use when another skill needs full Jira ticket context, or when user says "fetch ticket", "get ticket content", "retrieve Jira", /fetch-jira.
---

# Jira Retriever

Fetch everything a Jira ticket contains. Done when all content is captured and every image is readable.

## Contract

- **Arg:** `{KEY}` [, `save`]
- **Writes:** `tasks/{KEY}/jira.md` — **only when `save` is given**
- **Default:** return the Output block below in chat; write no file
- **Attachments:** always `tasks/{KEY}/attachments/`, regardless of `save`

## Steps

### 1. Fetch ticket

Use the Atlassian MCP tool to fetch the issue. Pass `fields` explicitly:

```
fields: ["summary", "description", "status", "assignee", "reporter", "issuetype",
         "created", "updated", "subtasks", "issuelinks", "attachment", "comment"]
```

If the description does not contain acceptance criteria and the project is known to store ACs in a custom field, add that field explicitly rather than falling back to `*all`.

### 2. Fetch sub-tasks

For each sub-task key, use the Atlassian MCP tool to fetch its details. Extract title, status, ACs.

If a call fails: note `⚠️ [KEY]: Could not retrieve — [reason]` and continue.

### 3. Download images

If any attachment has `mimeType: image/*`, run:

```bash
bash .kiro/skills/jira-retriever/download-jira-attachments.sh <ISSUE-KEY>
```

Saves to `tasks/<ISSUE-KEY>/attachments/`. The script also generates `comment-images.txt` in the same directory — a cross-reference of each image to the comment it was posted in (or `ticket-description` if uploaded directly). Read this file after download to know which image belongs to which context.

If the script fails: note which files could not be downloaded and continue with text-only context.

### 4. Read images

Call `Read` on each downloaded image. Describe what it shows — UI states, error states, or before/after behaviour relevant to the ACs.

### 5. Extract Figma links

Run in both modes. Scan description and comments for `figma.com` URLs. Per link extract: full URL, file key, node-id query param, source (`description` / `comment`). Write them to the `## Figma Links` section. No links found: write `None` under that heading.

Extraction only — never fetch design content here. `figma-retriever` owns that.

**Without `save`** only: after extracting, ask "Figma links found — would you like me to fetch the design content too?" Under `save` the caller owns that decision — extract, write, and continue without stopping.

## Output

Both paths use the structure below. `save` → write it to `tasks/{KEY}/jira.md` without showing the content in chat, then say "Written to `tasks/{KEY}/jira.md` — check it and flag anything to update." No `save` → return it in chat.

```markdown
# Jira: [KEY]

## Title
## Status
[status] | Assignee: [name] | Reporter: [name]

## Description
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

## Visual Context
- [filename]: [what it shows]

## Figma Links
- [URL] (source: [description | comment]) — File Key: [key], Node ID: [node-id or none]

## Open Items from Comments
- [unresolved question or pending decision] (by [author], [date])
```

Every heading above is written verbatim, including when the ticket words it differently — downstream skills match on the exact text. Attribute a source on the item, never by extending the heading. A section the ticket has nothing for gets the heading and `None`.

Business Requirements and Error Messages carry the values `generate-tcs` asserts verbatim — capture every BR-table row and every error string, even when the ticket states them outside the AC section.

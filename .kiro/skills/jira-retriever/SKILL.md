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

Saves to `tasks/<ISSUE-KEY>/attachments/`.

If the script fails: note which files could not be downloaded and continue with text-only context.

### 4. Read images

Call `read_file` on each downloaded image. Describe what it shows — UI states, error states, or before/after behaviour relevant to the ACs.

### 5. Extract Figma links *(optional)*

Ask the user: "Figma links found — would you like me to fetch the design content too?"

If yes: scan description and comments for `figma.com` URLs. Per link extract:
- full URL, file key (segment after `design/` or `file/`), node-id query param, source (`description` / `comment`)

If no links found: report "No Figma links discovered" and skip.

## Output

```markdown
## Jira: [KEY]

### Title
### Status
[status] | Assignee: [name] | Reporter: [name]

### Description
### Acceptance Criteria
### Linked Issues
- [KEY]: [summary] ([link type])

### Sub-task Criteria
#### [SUB-KEY]: [title]

### Visual Context
- [filename]: [what it shows]

### Figma Links
- [URL] (source: [description | comment]) — File Key: [key], Node ID: [node-id or none]
```

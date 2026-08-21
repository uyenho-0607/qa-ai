---
name: docs-media
description: Insert local images/screenshots into Google Docs via MCP pipeline (stage → upload → insert → cleanup). Use when user asks to add images to a Google Doc, attach evidence to a doc, or says /docs-media, /docs-upload, /upload-docs.
---

# Docs Media — Insert Images into Google Docs

## Purpose

Insert local image files as inline images into a Google Document using MCP tools.

---

## MCP Tools Used

| Tool | Server | Purpose |
|------|--------|---------|
| `manage_drive` (upload, share) | google-workspace | Stage images to Drive |
| `readdocument` (format=json) | google-docs | Read doc structure for indices |
| `replacedocumentwithmarkdown` | google-docs | Format doc BEFORE inserting images |
| `insertimage` | google-docs | Insert image at index |
| `deletefile` | google-docs | Remove temp Drive files after |

---

## Workflow

### Phase 1 — Read Doc & Match Images

1. Get the Google Doc URL from user (extract document ID — string between `/d/` and `/edit`)
2. **Read the doc** with `readdocument` format=json → understand the structure (numbered points, headings, labels)
3. Get the local image paths from user
4. **Match images to insertion points** — by name, number, or user instruction. Each image maps to a specific point in the doc.
5. If the mapping is ambiguous, ask user to clarify before proceeding.

### Phase 2 — Format Doc Structure (if needed)

Only if the doc needs new headings/structure added before images.

Use `replacedocumentwithmarkdown` to set up headings/labels FIRST.

⛔ Do this BEFORE inserting images — markdown replace wipes inline objects.

### Phase 3 — Stage & Upload

For each image:

1. **Copy** to staging dir: `~/.local/share/google-workspace-mcp/workspace/<filename>`
2. **Upload** to Drive: `manage_drive { operation: "upload", email: "ngocuyen.ho@aquariux.com", filePath: "<filename>", name: "<filename>" }` → save File ID
3. **Share** publicly: `manage_drive { operation: "share", fileId: "<id>", role: "reader", type: "anyone" }`

### Phase 4 — Insert Images

1. If Phase 2 was performed, re-read doc with `readdocument` format=json (indices shifted)
2. **Map each image to its target index** — find the paragraph matching the label/number from Phase 1, use its `endIndex` as insertion point
3. **Insert in REVERSE order** (last image first) to avoid index shifting
4. Use `insertimage`:
   ```
   documentId: "<doc_id>"
   imageUrl: "https://drive.google.com/uc?id=<file_id>"
   index: <target_paragraph_endIndex>
   width: <see table below>
   ```

#### Width

Default: **450pt** (fits A4 with margins). Override if user specifies otherwise.

### Phase 5 — Cleanup

1. **Delete Drive files** — `deletefile { fileId: "<id>", permanent: true }` (safe — images are internalized by Google Docs to its own CDN)
2. **Delete local staging copies** — `rm ~/.local/share/google-workspace-mcp/workspace/<filename>`

### Phase 6 — Verify

Read doc with `readdocument` format=json. Confirm `inlineObjects` section has entries with `contentUri` on `lh7-rt.googleusercontent.com`.

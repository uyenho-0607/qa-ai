---
name: docs-media
description: Insert local images/screenshots into Google Docs as inline images. Use when user asks to add images to a Google Doc, attach evidence to a doc, or says /docs-media, /docs-upload, /upload-docs.
---

# Docs Media — Insert Images into Google Docs

## Tools

| Tool | Server |
|------|--------|
| `findElement` | google-docs |
| `readDocument` (format=json) | google-docs |
| `insertImage` | google-docs |
| `deleteRange` | google-docs |
| `replaceDocumentWithMarkdown` | google-docs |
| `searchDriveFiles`, `createFolder`, `copyFile` | google-docs |
| `listDriveFiles`, `deleteFile` | google-docs |

`readDocument` format=json returns 50–100KB+ raw JSON, truncated by the harness. Use only for `inlineObjects` (step 4 working copy, step 5). Parse the saved output file, not the raw text.

## Workflow

### 1. Read the doc & map images to sections

1. Get the doc ID from the URL (the string between `/d/` and `/edit`).
2. `findElement` with `elementType: "paragraph"` → lists paragraphs with index ranges and text previews. Use for target section titles, not `readDocument`.
3. Get local image paths from the user. Match each to its section by name, number, or instruction. Ambiguous mapping → ask before proceeding.
4. Insertion index: `endIndex` of the paragraph immediately after the section title (usually a blank line). `findElement` with `textQuery` also returns this directly for a known title.
5. Local image path must resolve inside the MCP server's working directory (the project root) — paths under `~`, `/tmp`, or elsewhere are rejected. `evidence/` files satisfy this.

### 2. (Optional) Add headings first

If new headings/structure are needed, add them with `replaceDocumentWithMarkdown` before inserting any images.

### 3. Size every image — always pass both width and height

`insertImage` only sizes the image when both `width` and `height` are given. `width` alone is ignored — the image inserts at full native pixel size.

```
height = width * (native_height / native_width)
```

Sizing convention:
- Portrait mobile screenshots (phone UI, tall aspect ratio): width **220pt**
- Everything else (desktop screenshots, diagrams, landscape images): width **450pt**

Applies to every `insertImage` call in step 4.

### 4. Insert — try the original doc first, fall back to a working copy if blocked

Call `insertImage` for the first mapped image, directly into the original doc (`localImagePath`, index/size from steps 1 and 3).

- **Succeeds** → insert every remaining image the same way, in reverse order (last section first). Skip to step 5.
- **Fails** with "Bad Request" / "problem retrieving the image" → switch to the working copy below for all remaining images. Do not retry the direct path.

#### Working copy (only on the "Fails" branch above)

1. `searchDriveFiles { query: "docs-media-workspace", mimeType: "folder" }` — reuse if found. Otherwise `createFolder { name: "docs-media-workspace" }` in My Drive.
2. `copyFile` the original doc into that folder → the working doc.
3. Insert every remaining image into the working doc — same index/size/reverse-order rules as above.
4. Some mapped sections still lack an image? Stop: report progress (n of m), share the working doc link. Don't merge back yet.
5. Once every mapped section has its image: for each, `readDocument` the working doc, read `contentUri` from its `inlineObjects` entry, then `insertImage` that `contentUri` as `imageUrl` (not `localImagePath`) into the original doc at the same index.
6. Delete the working doc (`deleteFile`).

Wrong index or size, in either doc? `deleteRange` the image (1 character — via `findElement` or the `inlineObjects` entry), then re-run `insertImage` with correct values.

### 5. Verify

`readDocument` format=json on the original doc → `inlineObjects` should have one entry per inserted image, each with a `contentUri` on `lh7-rt.googleusercontent.com` and a `size` matching the passed values.

### Optional cleanup

`insertImage` with `localImagePath` leaves an uploaded copy in Drive — safe to delete. The tool's response doesn't return its file ID. Find it with `listDriveFiles` (`orderBy: createdTime`, `sortDirection: desc`, filtered by filename), then `deleteFile { fileId, permanent: true }`.

# ADF Templates — Bug Descriptions & Comments

## Bug Description Structure

```json
{
  "version": 1,
  "type": "doc",
  "content": [
    // "Steps to Reproduce:" (bold paragraph)
    // orderedList with steps (URLs = link marks, API paths = code marks)
    // "Actual Result:" (bold paragraph)
    // bulletList with findings
    // mediaSingle node(s) — RIGHT AFTER Actual Result
    {
      "type": "mediaSingle",
      "attrs": {"layout": "center", "width": 500, "widthType": "pixel"},
      "content": [{
        "type": "media",
        "attrs": {
          "type": "file",
          "id": "{MEDIA_1}",
          "alt": "filename.png",
          "collection": "",
          "width": "{WIDTH_1}",
          "height": "{HEIGHT_1}"
        }
      }]
    },
    // "Expected Result:" (bold paragraph)
    // bulletList with expected behavior
    // "Root Cause:" paragraph (FE/BE + explanation)
    // "Environment:" paragraph with link
  ]
}
```

---

## ADF Rules

- ALWAYS `"type": "file"` (NOT `"type": "external"`) — enables inline playback
- `"collection": ""` — always empty string
- `"id"` = media UUID (NOT the attachment numeric ID)
- **Image size:** two nodes, two jobs. `media.width`/`media.height` = the file's **real** pixel size (aspect ratio only — never guess it). `mediaSingle.width` + `"widthType": "pixel"` = the **rendered** width. Height is not settable; the renderer derives it as `mediaSingle.width × (media.height / media.width)`.
- **mediaSingle layout:** `"layout": "center"` with a pixel width — 500px is the default. `"full-width"` only when the real dimensions are unknown; a fake intrinsic on a portrait screenshot is what made images render as thumbnails.
- Place mediaSingle AFTER "Actual Result", BEFORE "Expected Result"
- Multiple evidence = multiple mediaSingle nodes in sequence
- URLs in STR: `"marks": [{"type": "link", "attrs": {"href": "..."}}]`
- Code/API paths: `"marks": [{"type": "code"}]`
- Use `{MEDIA_1}`, `{MEDIA_2}` placeholders — `jira_desc_update.py` replaces them, and `"{WIDTH_1}"`/`"{HEIGHT_1}"` (quoted) with the file's real dimensions

---

## Ordered List Node (STR steps)

```json
{
  "type": "orderedList",
  "content": [
    {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Navigate to "}, {"type": "text", "text": "https://...", "marks": [{"type": "link", "attrs": {"href": "https://..."}}]}]}]},
    {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Click ..."}]}]}
  ]
}
```

## Root Cause + Environment

```json
{"type": "paragraph", "content": [{"type": "text", "text": "Root Cause:", "marks": [{"type": "strong"}]}, {"type": "text", "text": " BE — API returns wrong data"}]},
{"type": "paragraph", "content": [{"type": "text", "text": "Environment:", "marks": [{"type": "strong"}]}, {"type": "text", "text": " SIT ("}, {"type": "text", "text": "https://admin.aqxoms-sit...", "marks": [{"type": "link", "attrs": {"href": "https://admin.aqxoms-sit..."}}]}, {"type": "text", "text": ")"}]}
```

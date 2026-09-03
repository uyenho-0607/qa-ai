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
      "attrs": {"layout": "full-width"},
      "content": [{
        "type": "media",
        "attrs": {
          "type": "file",
          "id": "{MEDIA_1}",
          "alt": "filename.png",
          "collection": "",
          "width": 2560,
          "height": 1440
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
- **mediaSingle layout:** Always use `"layout": "full-width"`. Never use `"center"` — it shrinks portrait/vertical images to unreadable thumbnails.
- Place mediaSingle AFTER "Actual Result", BEFORE "Expected Result"
- Multiple evidence = multiple mediaSingle nodes in sequence
- URLs in STR: `"marks": [{"type": "link", "attrs": {"href": "..."}}]`
- Code/API paths: `"marks": [{"type": "code"}]`
- Use `{MEDIA_1}`, `{MEDIA_2}` placeholders — `jira_desc_update.py` replaces them

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

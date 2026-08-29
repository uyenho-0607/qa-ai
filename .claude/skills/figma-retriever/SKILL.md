---
name: figma-retriever
description: Snapshot Figma design content into a structured markdown file + PNG screenshots. Use when generating test cases from a Figma URL, capturing a UI design baseline, or when another skill needs figma-snapshot.md. Provide the Figma URL and Jira ticket ID.
---

# Figma Retriever

UI/UX design analyst for QA. Extract Figma structure, write a frozen design snapshot, and download PNG screenshots. Downstream skill: `generate-tcs` references `figma-snapshot.md` via `tasks/{KEY}/base/attachments/`.

## Input

Figma URL and Jira ticket ID.

## Output

```
tasks/<TICKET_ID>/attachments/
  figma-snapshot.md
  figma-screenshots/<frame-name>.png …
```

---

## What to Extract (UI/UX only)

- Page layout — nav, breadcrumbs, content areas
- Interactive components — buttons, inputs, dropdowns, toggles, radios, checkboxes, date pickers
- Component states — Default, Hover, Focused, Active, Disabled, Selected, Error
- Tables — headers, sort indicators, row actions
- Modals / sheets / drawers — title, body, footer buttons
- Forms — field names, types, required markers, placeholders, order
- Empty states — illustration, message, CTA
- Pagination — record count format, navigation style
- Toasts — position, message, dismiss
- Action menus — items, destructive actions
- Tabs — labels, active/inactive
- Search & filter — placeholder, filter options
- Confirmation dialogs — title, body, button labels

## What to Ignore

Never extract:
- Designer annotation boxes (blue/colored notes with specifications or validation rules)
- Frames named "Notes", "Annotations", or similar
- Step headers / flow labels added for internal designer reference
- Figma comments

---

## Workflow

### Step 1: Parse the Figma URL

Extract `fileKey` and `nodeId`:

- **fileKey**: alphanumeric segment after `figma.com/file/` or `figma.com/design/`  
  `https://www.figma.com/design/abc123XYZ/…` → `abc123XYZ`
- **nodeId**: `node-id` query param, converting hyphens to colons  
  `?node-id=920-154018` → `920:154018`  
  If absent, omit nodeId.

Reference URL format: `https://www.figma.com/design/<fileKey>/<name>?node-id=<nodeId>&m=dev`

---

### Step 2: Fetch Figma Data

```
mcp__figma__get_figma_data(fileKey: "<fileKey>", nodeId: "<nodeId>")
```

Process the node tree in-context — no scripts. If the response is too large, drill down by calling again with a child `nodeId` until manageable.

---

### Step 3: Extract Design Content

Walk every distinct UI screen/state in the node tree and extract:

**Component hierarchy** — nesting, parent-child relationships.

**Interactive elements** — identify by name patterns:
- Buttons: names containing `button`, `btn`, `cta`
- Inputs: `input`, `field`, `text field`, `search`, `textarea`
- Dropdowns: `dropdown`, `select`, `picker`, `combobox`
- Modals: `modal`, `dialog`, `popup`, `overlay`
- Links: `link`, `anchor`, or hyperlink-styled text
- Checkboxes: `checkbox`, `check`
- Toggles: `toggle`, `switch`
- Tabs: `tab`
- Radios: `radio`

Label each by its visible text; fall back to component name. Record the parent component.

**Text content** — every text node value with its parent context. Copy labels, placeholders, and messages verbatim.

**State deduplication** — group artboards that show different states of the same screen (empty/filled/error/hover/toast) under one base name. Document variants as states, not separate screens.

---

### Step 4: Generate Snapshot

Save to `tasks/<TICKET_ID>/attachments/figma-snapshot.md`:

```markdown
# Figma Design Snapshot: <TICKET_ID>

## Metadata
- **Figma File**: <file name>
- **Figma URL**: <original URL>
- **File Key**: <fileKey>
- **Node ID**: <nodeId>
- **Extraction Date**: <current date/time>
- **Jira Ticket**: <TICKET_ID>

## Page Structure

### Navigation
- **Side Navigation**: <active item, sub-items>
- **Top Navigation**: <user info, dropdowns>
- **Breadcrumbs**: <if present>

### Main Page: <page name>

#### Header
- **Title**: …
- **Subtitle**: …
- **Primary Action Button**: …

#### Search & Filter
- **Search Field**: Placeholder: "…"
- **Filter Dropdown**: Options: […]

#### Table
| Column | Sortable | Data Type | Sample Data |
|--------|----------|-----------|-------------|

#### Pagination
- **Format**: "…"
- **Style**: …

#### Action Menu (per row)
- <action> (destructive: yes/no)

### Modal/Sheet: <name>

#### Header
- **Title**: …  **Subtitle**: …

#### Form Fields
| Field | Type | Required | Placeholder | Notes |
|-------|------|----------|-------------|-------|

#### Footer
- **Primary**: … | **Secondary**: … | **Destructive**: …

### State: <name>
- **Visual**: …  **Title**: …  **Message**: …  **CTA**: …

## Component States Summary
| Component | States |
|-----------|--------|

## UI Flow Summary
1. …
```

---

### Step 5: Download Screenshots

Export top-level frame nodes as PNGs:

```
mcp__figma__download_figma_images(
  fileKey: "<fileKey>",
  nodes: [{ nodeId: "<id>", fileName: "<descriptive-name>.png" }],
  localPath: "tasks/<TICKET_ID>/attachments/figma-screenshots",
  pngScale: 2
)
```

Descriptive filenames: `listing-page-with-data.png`, `create-sheet-default.png`, `delete-confirmation-modal.png`, `empty-state.png`.

If download fails, note in the snapshot:
```
⚠️ Screenshots unavailable. Extraction based on node tree only.
```

---

### Step 6: Read and Analyse Screenshots

After all PNGs are saved, `Read` each one:

```
Read tasks/<TICKET_ID>/attachments/figma-screenshots/<frame-name>.png
```

For each image, visually observe and note:
- Overall layout structure — where nav, header, content, footer sit
- Visual hierarchy — what draws the eye first, section groupings
- Component arrangement — how forms, tables, modals are laid out
- Rendered states — what active/selected/disabled elements actually look like
- Anything the node tree missed — overlapping elements, visual-only separators, icon usage

Incorporate these observations into the snapshot. If the visual reading contradicts or enriches what the node tree said, the visual reading wins.

Update `tasks/<TICKET_ID>/attachments/figma-snapshot.md`: append or revise the relevant section with visual observations. Edit the section directly — do not append a separate block at the end.

---

## Error Handling

On `mcp__figma__get_figma_data` failure, return to the orchestrator:

```
❌ Figma retrieval failed
   Reason: <error>
   File key: <fileKey>
   Node ID: <nodeId or "none">
```

Common causes: malformed URL, file not shared, node-id not found, MCP not configured.

---

## Constraints

- UI/UX only — no validation logic, business rules, or designer notes
- No source code (.ts, .tsx, .js, .jsx, .css)
- Process metadata in-context — no Python scripts
- One snapshot per ticket — overwrite on re-run

---
name: figma-retriever
description: Snapshot Figma design content into a structured markdown file + PNG screenshots. Use when generating test cases from a Figma URL, or when another skill needs figma-snapshot.md.
---

# Figma Retriever

UI/UX design analyst for QA. Extract Figma structure, write a frozen design snapshot, and download PNG screenshots.

## Contract

- **Args:** one Figma URL, `<TICKET_ID>`; several URLs → run Steps 1-4 per URL, one merged snapshot
- **Writes:** `tasks/<TICKET_ID>/base/figma/figma-snapshot.md`, `tasks/<TICKET_ID>/base/figma/figma-screenshots/<frame-name>.png`, `.tmp/census-<TICKET_ID>.tsv`
- **Scope:** rendered UI only

---

## Workflow

### Step 1: Parse the Figma URL

Extract `fileKey` and `nodeId`:

- **fileKey**: alphanumeric segment after `figma.com/file/` or `figma.com/design/`  
  `https://www.figma.com/design/abc123XYZ/…` → `abc123XYZ`
- **nodeId**: `node-id` query param, converting hyphens to colons  
  `?node-id=920-154018` → `920:154018`  
  No node-id in the URL → ask the caller for a frame link. figma.py requires one.

---

### Step 2: Map the board

```bash
python3 .kiro/skills/figma-retriever/figma.py census <fileKey> <nodeId> --depth 3 > .tmp/census-<TICKET_ID>.tsv
grep '^TITLE'  .tmp/census-<TICKET_ID>.tsv           # screen inventory — what each screen IS
grep 'State='  .tmp/census-<TICKET_ID>.tsv           # component-set variants — node id in column 2
grep '<title text>' .tmp/census-<TICKET_ID>.tsv      # that screen's TITLE row plus every frame under it
```

Columns are `type · node id · name · owning title`. Grepping a title string returns the frames that belong to it.

Row, TITLE, and variant counts print to stderr. `Notes` and `Annotations` are already pruned.

**Work from the TITLE rows.** Frames are named for what they are built from (`Modal-basic`), not what they show; the `📁 Step header` beside each screen is the only thing that names it. A TITLE naming a screen you have not fetched is a target you have missed — including the far side of an action, where `Disable/Enable …` titles cover both directions.

Write a target list before fetching anything else:

- Every top-level screen frame → a screenshot in Step 6.
- **Every `State=` variant → a documented state in Step 5**, with or without an exportable frame. No frame → record it and note the missing screenshot; do not drop it.
- Designer annotation boxes and Figma comments → excluded.

---

### Step 3: Fetch each target

The census carries no copy. Batch every target node id into one call, comma-separated:

```bash
python3 .kiro/skills/figma-retriever/figma.py text <fileKey> <id>,<id>,<id>
```

Output is grouped `## <nodeId> <name>`, then that node's text in document order. Read it directly — it is already filtered to copy.

Every `State=` node id from the census goes in the batch. No exportable frame is not a reason to skip one — that fetch is the only place its copy exists. "No frame" is never reported as "no content". Every batched id returns a `## <id>` block. A `NOT FOUND` on stderr is recorded as unread, never as "no content".

⚠️ A component **instance** can return the base component's defaults instead of the instance overrides — placeholder strings like `Header` or `No results found`. Instance disagrees with the component-set variant → the variant wins. Record the discrepancy, not the placeholder.

---

### Step 4: Extract Design Content

Walk every distinct UI screen/state in the census and text extraction and extract:

**Interactive elements** — label each by its visible text; fall back to component name. Record the parent component.

**Text content** — every text node value with its parent context. Copy labels, placeholders, and messages verbatim.

**State deduplication** — group artboards showing different states of the same screen under one base name. Document variants as states, not separate screens.

**Verbatim, once per variant.** Record each variant's string in full, on its own line. Never collapse two variants into a template (`This [bank account / crypto address] cannot be…`); never hedge (`"Saved successfully." (or similar)`). A string you could not read is recorded as unread, not approximated.

---

### Step 5: Generate Snapshot

Save to `tasks/<TICKET_ID>/base/figma/figma-snapshot.md`.

Required sections and fields:

- **Metadata**: Figma File, Figma URL, File Key, Node ID, Extraction Date, Jira Ticket
- **Page Structure** — record the platform the design shows; omit the other platform's block
  - *Web (BO)*: Navigation (side nav active item + sub-items, top nav, breadcrumbs), Header (title, subtitle, primary action), Search & Filter (placeholder, options), Table (columns, sortable, sample data), Pagination (format, style), Action Menu (items, destructive flag)
  - *Mobile (member app)*: Tab bar (items, active), Header bar (title, back, right action), Section headers, List/Card rows (fields shown, tap target), Scroll or pull-to-refresh, Floating action
  - *Either*: Modal/Sheet (per modal) — Header (title, subtitle), Form Fields (name, type, required, placeholder), Footer (primary, secondary, destructive CTAs)
  - *Either*: State (per empty/error/loading state) — Visual, Title, Message, CTA
- **Component States Summary**: table of component → states (Default, Hover, Focused, Active, Disabled, Selected, Error — those observed)
- **UI Flow Summary**: numbered steps

---

### Step 6: Download Screenshots

One batched call for every target — `nodeId=filename`, comma-separated, relative `--out` path:

```bash
python3 .kiro/skills/figma-retriever/figma.py images <fileKey> \
  "<id>=<descriptive-name>,<id>=<descriptive-name>" \
  --out tasks/<TICKET_ID>/base/figma/figma-screenshots
```

Descriptive filenames: `listing-page-with-data`, `create-sheet-default`, `delete-confirmation-modal`, `empty-state`. The `.png` extension is added for you.

A `State=` variant with no top-level frame still exports — pass its node id like any other. "No exportable frame" is not a reason to skip a screenshot.

One line per node: `OK` with the path and byte size, or `FAIL` with the reason. Every `FAIL` is recorded in the snapshot's Component States Summary as a missing screenshot.

---

### Step 7: Read and Analyse Screenshots

After all PNGs are saved, read each PNG in `tasks/<TICKET_ID>/base/figma/figma-screenshots/`.

For each image, note the rendered states (what active/selected/disabled elements actually look like) and anything the census and text extraction missed — overlapping elements, visual-only separators, icon usage. If the visual reading contradicts or enriches the census and text extraction, the visual reading wins.

**A render never deletes extracted copy.** "Visual wins" settles what a state *looks like*, not whether a string exists. A frame that renders blank, generic, or with placeholder text (`Header`, `Item`, `No results found`, an empty component) is an unbuilt instance — keep the Step 3 string, record the render as a discrepancy. Never report a string as absent from the file when Step 3 returned it: absence is a claim about the file, and the extraction is the evidence.

Update `tasks/<TICKET_ID>/base/figma/figma-snapshot.md` in place — edit sections directly, do not append a separate block.

---

## Error Handling

On `figma.py` failure, return to the orchestrator:

```
❌ Figma retrieval failed
   Reason: <error>
   File key: <fileKey>
   Node ID: <nodeId or "none">
```

---

## Constraints

- One snapshot per ticket. Re-run overwrites; a second URL appends sections, never overwrites.

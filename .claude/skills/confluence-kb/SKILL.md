---
name: confluence-kb
description: Document a ticket's feature as a Confluence KB page and in .claude/domain/ — standard, sources, observe live, draft, gate, write. Use when asked to document a ticket on Confluence, to update or add a KB/wiki page for a ticket, or /confluence-kb.
---

# Confluence KB

The ticket supplies the scope; the screen supplies the words.

**Done when:** a draft link is returned, and every domain candidate is written or accounted for.

## Contract

- **Args:** `{KEY}`, `{root page}` [, `{standard page}`] — page as URL or id
- **Writes:** one Confluence page, `status: draft` — updated in place, or created under `{root page}`
- **Publishes:** nothing. The Confluence page stays a draft.

Missing `{root page}` → ask.

## Phase 1 — Standard

The standard is the page whose shape this one copies.

`{standard page}` given → read it. Otherwise list the children of `{root page}`
(`getConfluencePageDescendants`), read the ticket's platform off its summary tag
(`[MobileApp]` → member app, else Back Office), and read the children documenting that same platform. Two or three is enough.

Done when you can name, from the standard: its section order, its heading pattern, every table's columns, where screenshots sit, and its footer row.

## Phase 2 — Sources

- `jira-retriever {KEY}` — scope, ACs, linked issues, sub-tasks.
- `domain-expert` — what `.claude/domain/` already holds on this feature, and its `GAPS:`.
- Captures a run already made: `ls evidence/{KEY}/ tasks/{KEY}/exec/evidence/ 2>/dev/null`
- Closed SIT bugs on the ticket. A bug closed **Won't Do** is accepted behaviour: the page states it positively and cites the key.

## Phase 3 — Observed

Drive the live app or BO and read every string off the screen. Platforms and credentials:

```bash
awk '/^## /{p = /^## (Environment|Platforms)/} p' .claude/steering/project-config.md
```

Cold-start runbook for the member app: `.claude/domain/login-flow.md`.

Every claim on the page is one of two kinds:

- **observed** — you saw it this run, or a capture in `evidence/` shows it.
- **spec** — it comes from the ticket, an AC, or Figma, and is written on the page as `Not yet verified — <what it claims>`.

Where ticket and screen differ, the screen wins. Check by hand: success and error strings, field labels and placeholders, button enable rules, and what the screen does *after* a successful submit.

Capture what the page still lacks. A capture with a debug overlay, a stale banner, or a cropped control gets retaken.

Done when every string destined for the page is marked observed or spec, and the post-success screen has been reached at least once.

## Phase 4 — Draft

Search `{root page}`'s children for a page already covering this feature.

- **Found** → that page is the target; keep its id and every media id already on it.
- **None** → the target is a new child of `{root page}`, titled the way its siblings are titled. Phase 6 creates it.

Call `getContentFormatGuide` for the body HTML before writing it.

Build the body in the standard's shape from Phase 1. Write in the present tense of what the
screen does. Screenshots carry a caption.

Three things the format guide will not tell you:

- **No attachment upload exists.** Reuse the media ids already on the target page — they survive a body replacement. A capture not yet attached gets a note panel naming its repo path.
- **`title` is plain text.** Writing `&amp;` there saves the five characters literally.
- **Pass `status: "draft"`** on create and on update. The default is `current`, which publishes.

## Phase 5 — Gate

Show, before writing anything:

- update or create, and the target page
- section-by-section what changes, and what is being removed with the reason
- every claim still marked spec
- every capture a human must attach

Wait for approval (`CLAUDE.md` § Approval before writes).

## Phase 6 — Write and report

1. Create or update the page, `status: draft`.
2. Read the page back. Confirm the body rendered and every image survived.
3. Hand Phase 3's claims to `learn-domain` — observed and spec both, each carrying `{KEY}`and the run date for its `src:` line. Flag any that contradict a line already in `.claude/domain/`.

Then report briefly: the draft URL and whether it was updated or created, each correction the screen forced, anything still spec or awaiting a human attach, and what `learn-domain`
wrote.

Lead the report with the corrections. A run that corrected nothing says so in one line.

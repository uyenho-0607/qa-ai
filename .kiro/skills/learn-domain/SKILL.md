---
name: learn-domain
description: Append newly learned domain knowledge to .kiro/domain/ — classify, place, propose, write, sync. Use on a `GAPS:` list from domain-expert, an "undocumented" note in a run report, a ui-discovery output, or /learn-domain.
---

# Learn Domain

`.kiro/domain/` is the only durable record of what this product is *supposed* to do. This skill is its sole write path. `domain-expert` reads; this skill appends.

**Done when:** every candidate is either written, routed to another store, or rejected with a reason — none left unaccounted.

## Inputs

One or more of:
- A `GAPS:` block returned by `domain-expert`.
- A run report (`tasks/{KEY}/report.md`) — grep for `undocumented`, `not mentioned`, `not in`.
- A `ui-discovery` Phase 4 output.
- A `confluence-kb` Phase 3 claim list — observed and spec, each with its key and date.
- A fact the user states directly.

Missing the ticket key or the observation date? Ask. Never invent provenance.

## Phase 0 — Route

Read `.kiro/domain/INDEX.md`. It names the file and section each candidate belongs to.

## Phase 1 — Classify every candidate

| Verdict | Candidate is | Goes to |
|---|---|---|
| **tier 1** | A spec fact — one rule, error string, field, screen, permission | One tagged line in the KB section |
| **tier 2** | A whole feature mapped live | New `.kiro/domain/flows/{feature}.md` + one `#flow` pointer line in the KB |
| **naming** | A Module / Sub-module / Feature name | `tc-naming-ref.md` — but that file mirrors an external sheet. **Ask before editing it** |
| **lesson** | A tool or driver gotcha (Maestro, Playwright, adb, upload worker) | `.kiro/docs/lessons.md`. Not domain knowledge |
| **locator** | A selector, testid, or tap coordinate | `.kiro/locator-cache.json` (coordinate: never without its resolution) |
| **flow script** | A reusable Maestro flow | `flows/flows-index.json` |
| **reject** | A defect, or data belonging to one run (member id, test email, balance) | Jira, or `tasks/{KEY}/`. Say so and move on |

**A bug is never a rule.** The KB records intended behaviour. Observed-but-wrong behaviour goes to Jira; it enters the KB only once the intent is confirmed.

## Phase 2 — Write the line

Tier-1 format — append under the matching `## Section`, aligned with the lines already there:

```
#screen  Verify Identity | post Log in, pre Passcode | 6-digit email OTP | src: AO-970 (2026-09-11, observed)
```

`src:` is mandatory on every line this skill writes:

- `src: AO-970 (2026-09-11, observed)` — seen live. Carries the date because it can go stale.
- `src: AO-970 (spec)` — from a ticket, AC, or Figma. Not yet seen live.

Tier-2: write the flow file per the `ui-discovery` Phase 4 template, then add the KB pointer line and a row to `INDEX.md` § Flow files.

## Phase 3 — Contradictions

A candidate that disagrees with an existing line is an **amend**, never an append, and never a silent overwrite:

```
#rule    Action Required access | Admin: full | was: "Maker + Admin: no access" until AO-925 (2026-08-26, observed)
```

Live observation beats a `(spec)` line. Two live observations disagreeing is a real question — surface it, don't pick.

Resolve the contradiction in **every** file that holds it. A note left in one file pointing at stale text in another is not resolved.

## Phase 4 — Propose → GATE

Show, per candidate: verdict · target `file:line` · the exact line to be written. Wait for approval (`CLAUDE.md` § Approval before writes).

## Phase 5 — Write, sync, report

1. Apply the approved edits.
2. Update `INDEX.md` if a section, flow file, or tag is new.
3. `python3 sync-kiro.py`
4. Report one line per candidate: `<fact> -> <file:line>` or `<fact> -> routed to <store>` or `<fact> -> rejected (<reason>)`.

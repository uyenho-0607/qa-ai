---
name: audit-skills
description: Audit a skill or steering file and the docs it loads — token cost, cross-file duplication, contract bugs. Use when asked to optimize, prune, or trim agent docs for token waste, or /audit-skills.
---

# Audit Skills

**Done when:** every file in scope is measured, every finding is reported with its token cost and multiplier, and Phase 4 returns clean.

## Contract

- **Args:** the skill or steering file to audit [, `report-only`]
- **Scope:** the named target plus the files it loads or executes. Stay inside it — a widening audit is this skill's own failure mode.
- **Writes:** the audited files (Phase 3 only)
- **Delegates:** form of a convention file → disclose_context("writing-conventions"), Audit branch. Pointer strength, no-ops, information hierarchy → disclose_context("writing-for-agents").
- **report-only:** stop at the Phase 2 gate, apply nothing

---

## Phase 1 — Measure

```bash
# always-loaded — the only tokens paid on every turn of every session
wc -c CLAUDE.md; grep -n 'STEERING_ALWAYS' sync-kiro.py

# per-file cost across the scope
python3 -c "
import sys; from pathlib import Path
for f in sys.argv[1:]:
    t = Path(f).read_text()
    print(f'{round(len(t)/3.7):6} tok {len(t.splitlines()):4} L  {f}')
" <files in scope>

# verbatim duplication across the scope
python3 .kiro/skills/audit-skills/find-dupes.py <files in scope>
```

`find-dupes.py` reports 8-word repeats across two or more files. It catches verbatim duplication only — one file restating another's rules in its own words surfaces by reading both. A repeat that is deliberate (the same instruction at several load sites) is not a finding.

---

## Phase 2 — Rank, find, report → GATE

**2.1 Rank by multiplier, not by size.**

| Tier | Multiplier | Look for |
|---|---|---|
| Always-loaded | every turn × every session | `CLAUDE.md` restating the harness skill listing, `.gitignore`, or anything one `ls` away |
| Read path | per run × times read | a step reading a whole artifact to extract two fields — replace with `grep` |
| File content | per invocation | duplication, sprawl, form |

A 500-token file read once loses to a 20-token line loaded every turn. Work down the tiers in order.

**2.2 Check contracts.** Cross-skill bugs hide where one skill's declaration meets another's behaviour:

| Check | Failure it catches |
|---|---|
| `Writes:` lists every file the skill produces | an artifact nobody owns, lost on session restart |
| Declared artifact structure matches the file produced | template declares 8 sections, runs produce 10 |
| Every artifact a phase reads exists by that phase | a step patching a sheet a later phase creates |
| No gate asks what an earlier gate settled | export target confirmed after its tab name |
| Numeric cross-refs resolve after a table edit | `#17` pointing at a merged row |
| Pointer strength matches need | a mandatory file named in prose with no read step |
| No line is explanation disguised as instruction | a line containing `— run this every time`, `so that`, `, so ` (comma-so trailing clause), `because`, `in order to`, `this ensures`, or `the caller` with no imperative verb — flag for removal or rewrite |
| Partial file needed — use section extract | a `cat` or `Read` of a multi-section file where the skill only uses one or two named sections — replace with `awk '/^## /{p = /Section/} p'` |

**2.3 Report.** One row per finding, ordered by tokens saved:

```
Audit — {target}    [n] findings · [n] tok/turn · [n] tok/run
| Finding | Tier | Saves | Fix |
```

Name what a fix costs elsewhere — a parser change, a broken task file, a less readable review surface. A cut that moves cost rather than removing it is reported, never applied silently.

**GATE — stop until findings are approved.** *(skip with `report-only`: report and end)*

---

## Phase 3 — Apply

Apply approved findings only. Preserve every meaning: a rule that moves keeps one home and gains a pointer from its old one.

---

## Phase 4 — Verify

```bash
python3 sync-kiro.py            # regenerate the .kiro/ mirror from the Phase 3 edits
python3 sync-kiro.py --check    # mirror in step

# every file path named in the audited docs still resolves
python3 .kiro/skills/audit-skills/check-refs.py <files in scope>
```

`check-refs.py` resolves a ref against the repo root and against the naming file's own directory. What it lists are candidates: a doc may name `AGENTS.md` or `CLAUDE.md` as a kind of document rather than a path.

Format consumed by a parser → run the parser on a real artifact before and after, and diff the output. Identical output is the only proof a format change was safe.

---
name: writing-conventions
description: Write or audit a convention file for this project. Use when asked to write a new convention or update an existing one.
---

# Writing Conventions

Convention file = single source of truth for one concern.

**A convention is applied, not studied. Write constraints and decision rules the agent follows — never material that teaches it the subject.**

## Contract

- **Args:** convention name or file [, `audit` [, `report-only`]]
- **Writes:** `.kiro/steering/<name>.md`; the load step of each skill that needs it; `.kiro/` via `sync-kiro.py`
- **Gate:** propose the file and the skill edits, wait for approval, then write.

## Branch: Write

### 1. Understand the concern
- What single concern does this govern?
- Who is audience — test author, POM author, both?

### 2. Check overlap
```bash
ls .kiro/steering/
```
Read every file whose concern touches the new one. Note existing rules; exclude them from the new file.

### 3. Draft using TEMPLATE.md
```bash
cat .kiro/skills/writing-conventions/TEMPLATE.md
```
Rules:
- Open every rule with a verb — imperative, not descriptive
- One rule per bullet, one obligation, ≤20 words
- State the constraint; never why it exists — no rationale, aphorisms, or consequence sentences
- Name each heading for the action it governs, not the topic
- Include an example only to disambiguate a judgment call the rule cannot express
- Positive framing (state what to do)
- Write every obligation as "must"
- Strip no-op rules (agent already does by default)

### 4. Validate against steering
Compare the draft to the rules noted in step 2. Zero contradictions — the existing file wins.

### 5. Save and wire up
Save to `.kiro/steering/<kebab-case-name>.md`. Write no frontmatter — `sync-kiro.py` injects Kiro's `inclusion:` on the way out.

Steering files load only when a skill reads them. Name the new file in the load step of every skill that needs it, or it never loads and nothing errors. Then:
```bash
python3 sync-kiro.py
```

## Branch: Audit

1. Read every rule in *Draft* above; note each one the file fails. New files only: also flag missing or wrong-order sections against TEMPLATE.md.
2. Report each failure as `{file}:{line} — rule violated → fix`.
3. Apply the fixes only when the caller did not pass `report-only`.

## Hard Rules
- `## Purpose` ≤ 2 sentences
- No `## Validation` section
- New files only: section headers match TEMPLATE.md

`TEMPLATE.md` governs new files.

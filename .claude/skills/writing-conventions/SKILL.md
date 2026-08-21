---
name: writing-conventions
description: Write or audit a convention file for this project. Use when asked to write a new convention, update an existing one, or convert a raw document into convention format.
---

# Writing Conventions

Convention file = single source of truth for one concern. Prescriptive, minimal, maintainable.

**A convention is applied, not studied. Write constraints and decision rules the agent follows — never material that teaches it the subject.**

## Branch: Write

### 1. Understand the concern
- What single concern does this govern?
- Who is audience — test author, POM author, both?
- Which steering file overlaps? Read it.

### 2. Check overlap
Search `.claude/steering/`. Note existing rules, exclude from new file.

### 3. Draft using TEMPLATE.md
Rules:
- Open every rule with a verb — imperative, not descriptive
- Every rule is single, actionable sentence
- State the constraint; never state why it exists
- No explanations/rationale inline — rules only
- Cut aphorisms and consequence sentences — they are rationale in disguise
- Name each heading for the action it governs, not the topic
- Include an example only to disambiguate a judgment call the rule cannot express
- Positive framing (state what to do)
- No weasel words: "must", not "should"
- One rule per bullet, ≤20 words
- Strip no-op rules (agent already does by default)

### 4. Validate against steering
```bash
ls .claude/steering/
```
Read every file whose concern touches the new one. Zero contradictions — the existing file wins.

### 5. Save and wire up
Save to `.claude/steering/<kebab-case-name>.md`. Write no frontmatter — `sync-kiro.py` injects Kiro's `inclusion:` on the way out.

Steering files load only when a skill reads them. Name the new file in the load step of every skill that needs it, or it never loads and nothing errors. Then:
```bash
python3 sync-kiro.py
```

## Branch: Audit

### 1. Note deviations
- Missing/wrong-order section
- Rule is explanation, not prescription
- Descriptive bullet that reads as a statement, not a command
- Aphorism or consequence sentence carrying rationale
- Example that demonstrates the subject instead of disambiguating a rule
- Heading naming a topic instead of an action
- Weasel words, no-ops, duplicates
- Two obligations per bullet
- Negative framing that can be positive

### 2. Fix in-place
Same rules as Write. Don't change meaning — only form.

## Hard Rules
- Never include teaching material — no tutorials, walkthroughs, or worked examples
- `## Purpose` ≤ 2 sentences
- No `## Validation` section — rules are the only enforcement.
- Never add `## Background` or `## Why`
- File name = kebab-case matching title
- Section headers match TEMPLATE.md exactly

`TEMPLATE.md` governs new files. The existing `.claude/steering/` files predate it and use their own shapes — audit one for rule form, never to reshape it into the template.

# CLAUDE.md

Skills-based manual QA framework. No app build or test suite — only Python helper scripts invoked by skills.
Skills and steering docs live under `.claude/`.

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # fill in JIRA_EMAIL, JIRA_API, GOOGLE_* tokens
```

Fill in `<FILL_IN>` placeholders in `.claude/steering/project-config.md` before running any workflow.

## Architecture

Skills live at `.claude/skills/<name>/SKILL.md`. They never call each other — communication is via shared artifact files under `tasks/{KEY}/`: `jira.md`, `tc.md`, `tc-plan.md`, `manual-tcs.md`/`.csv`, `tc-review.md`, `attachments/`.

**Resumption:** check what exists in `tasks/{KEY}/`, start at the first step whose output is missing.

### Workflows

- **TC generation/review** — `generate-tcs` → `grill-tcs` → `review-tcs`: scope ACs/BRs, plan coverage, write TCs, export.
- **Bug verification** — `verify-bug`: reproduce STR, capture evidence, comment, transition.
- **Git** — `git-workflow`: create branch, push files, create GitLab MR.

### Steering docs (`.claude/steering/`)

| File | Purpose |
|---|---|
| `project-config.md` | Loaded every session (`inclusion: always`). Env vars, project ids. |
| `tc-conventions.md` | TC fields, naming, phrasing, export column order. |
| `tc-priority-guide.md`, `tc-scenario-guide.md` | Priority and scenario-type rules. |
| `manual-qa-anti-patterns.md` | Smell → fix-owner index for TC/run reviews. |
| `bug-conventions.md`, `jira.md`, `testmo.md` | Jira/Testmo reference data. |
| `playwright-rule.md` | Read before any Playwright MCP interaction. |
| `reasoning-standards.md` | Label claims as fact / assumption / recommendation / unknown. |

### Behavior-modifying skills

Active for the whole session once triggered:

- `confirm-force` — require explicit approval before any file write/edit/delete.
- `skill-follow` — follow activated skill steps exactly, no skipping.
- `caveman` — terse, low-token mode.

Both `confirm-force` and `skill-follow` are mandatory at session start (set in `project-config.md`).

### Writing or editing a skill

Read `.claude/skills/writing-for-agents/SKILL.md` first for house style and frontmatter conventions.

## Python helper scripts

Invoked by their owning skill, not run standalone:

- `.claude/skills/jira-handler/` — `jira_common.py`, `jira_comment.py`, `jira_desc_update.py`, `jira_attach.py`
- `.claude/skills/collect-gsheet-cases/fetch_gsheet_tcs.py` — fetches TCs from Google Sheets
- `.claude/skills/jira-retriever/download-jira-attachments.sh` — downloads Jira attachments to `tasks/{KEY}/attachments/`

## `.kiro/` mirror

`.kiro/` is a generated mirror of `.claude/` for Kiro IDE. **Never hand-edit `.kiro/`** — edit `.claude/`, then regenerate:

```bash
python3 sync-kiro.py            # regenerate .kiro/ from .claude/
python3 sync-kiro.py --check    # list stale files, exit 1 if any (used by pre-commit hook)
```

The trees differ by exactly two mechanical transforms: `Read .claude/skills/<name>/SKILL.md` → `disclose_context("<name>")`, and `.claude/...` → `.kiro/...` paths.

If you edited `.kiro/` by mistake: `python3 sync-kiro.py --promote .kiro/path/to/file.md` inverse-transforms that one file back into `.claude/`. It overwrites the whole `.claude` file — review the diff before regenerating.

## State / gitignore

`.gitignore` covers: `.env`, `.venv/`, `.playwright-mcp`, Python cache. `tasks/`, `evidence/`, `reports/` are **not** gitignored — avoid broad `git add`.

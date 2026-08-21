---
name: git-workflow
description: Git helper for QA manual tasks — create feature branch, stage and push files, create GitLab MR. Use when user says "start branch", "push files", "create MR", /git, /branch, /push, /mr.
argument-hint: "Ticket key or action: branch | push | mr"
---

# Git Workflow

Three actions: **branch → push → mr**.
GitLab project id: `project-config.md` → Tools section.

---

## Action: branch

1. `git branch --show-current` — if not on `main`/`master`/`develop`, warn and confirm before continuing.
2. If `{KEY}` not already known, ask: **"Ticket key?"**
3. Branch name: `qa/{KEY}` — use as-is unless user specifies a custom name.
4. `git checkout -b qa/{KEY}`
5. Confirm: "Branch `qa/{KEY}` created."

---

## Action: push

1. `git status --short` — show the output.
2. If user already named files in their message, use those. Otherwise ask: **"Which files? (list them or say 'all')"**
3. Stage: `git add <files>` or `git add -A` for all.
4. If user provided a commit message, use it. Otherwise ask: **"Commit message?"** — suggest `"[{KEY}] <short description>"`.
5. Check if remote branch exists: `git ls-remote --heads origin {branch}`
   - Exists → `git push`
   - New → `git push -u origin {branch}`
6. Show push output.

---

## Action: mr

1. `git branch --show-current` — get current branch.
2. Extract `{KEY}` from branch name if possible (e.g. `qa/OMS-123` → `OMS-123`).
3. Propose title: `[{KEY}] <short description>` — ask user to confirm or change.
4. Propose description from template below — user can edit or say "use default".
5. Target branch: `main` — ask only if user says otherwise.
6. Create MR:
   ```
   glab mr create --source-branch {branch} --target-branch main --title "{title}" --description "{description}"
   ```
   If `glab` is unavailable, print the URL:
   `https://gitlab.com/{project-path}/-/merge_requests/new?merge_request[source_branch]={branch}`
7. Return the MR URL.

### MR description template

```
## Summary


## Ticket
{KEY}

## Files changed


## Notes

```

---

## Guardrails

- Never `git add -A` without showing `git status` first.
- Never branch off or push directly to `main`/`master`/`develop`.
- If `git push` is rejected, show the error and ask before doing anything else.
- "start task {KEY}" / "begin {KEY}" → run **branch** automatically.
- "done" / "ready to review" → prompt **push** then **mr** in sequence.

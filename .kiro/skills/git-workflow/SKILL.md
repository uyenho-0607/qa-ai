---
name: git-workflow
description: Git helper for QA manual tasks — create feature branch, stage and push files, rebase, open a GitHub PR. Use when user says "start branch", "push files", "rebase", "create PR", "create MR", /git, /branch, /push, /rebase, /pr, /mr.
argument-hint: "Ticket key or action: branch | push | rebase | pr"
---

# Git Workflow

Four actions: **branch → push → rebase → pr**.
Remote is GitHub; `gh` reads owner/repo from `git remote`, so nothing to configure.
`/mr` is accepted as an alias for `pr`.

---

## Action: branch

1. `git branch --show-current` — record it as `{base}`. Branching off a protected branch is expected here; this action is how you leave one.
2. If `{KEY}` not already known, ask: **"Ticket key?"**
3. Branch name: `qa/{KEY}` — use as-is unless user specifies a custom name.
4. `git fetch origin` — then bring `{base}` up to date so the branch does not start stale:
   - `git status --porcelain` empty **and** `{base}` behind `origin/{base}` → `git merge --ff-only origin/{base}`.
   - Dirty tree, or the fast-forward is refused → skip it and say the branch starts from the current local commit. Never force it.
5. `git checkout -b qa/{KEY}`
   - Fails with `already exists` → the branch is left over from earlier work. `git switch qa/{KEY}` instead, and say that is what happened.
6. Confirm: "Branch `qa/{KEY}` created." If files were already edited, add: "Your uncommitted changes came with you — nothing was lost."

---

## Action: push

1. `git branch --show-current` — on `main`/`master`/`develop`, **stop immediately**: "⛔ You are on a protected branch. Run the `branch` action first. Your uncommitted changes will move to the new branch with you — nothing is lost." Do not continue.
2. `git status --short` — show the output.
3. If user already named files in their message, use those. Otherwise ask: **"Which files? (list them or say 'all')"**
4. Stage: `git add <files>` or `git add -A` for all.
5. If user provided a commit message, use it. Otherwise ask: **"Commit message?"** — suggest `"[{KEY}] <short description>"`.
6. Commit: `git commit -m "{message}"`
7. Check if remote branch exists: `git ls-remote --heads origin {branch}`
   - Exists → `git push`
   - New → `git push -u origin {branch}`
   - Rejected as non-fast-forward right after a rebase → that is expected; see the `rebase` action's last step.
8. Show push output.

---

## Action: rebase

1. `git branch --show-current` — confirm not on `main`/`master`/`develop` (hard block same as branch action).
2. `git status --porcelain` — not empty → **stop**: "⛔ Rebase needs a clean tree. Commit the changes first (run the `push` action), or stash them: `git stash push -u`." Rebasing over unstaged changes aborts, so do not attempt it. If the user chooses to stash, run it and `git stash pop` after step 7.
3. Ask: **"Rebase onto which branch? (default: main)"**
4. `git fetch origin`
5. `git rebase origin/{target}`
6. If conflicts: show conflicting files, stop, and instruct: "Resolve the conflicts, then run `git rebase --continue`. Run `git rebase --abort` to cancel."
7. If clean: confirm "Rebase onto `{target}` complete."
8. The rebase rewrote history, so the branch has diverged from its remote and a plain `git push` will be rejected. If the branch was already pushed, push with `git push --force-with-lease`. Never plain `--force` — `--force-with-lease` refuses if someone else pushed meanwhile.

---

## Action: pr

1. `git branch --show-current` — get current branch.
2. Extract `{KEY}` from branch name if possible (e.g. `qa/AO-306` → `AO-306`).
3. Propose title: `[{KEY}] <short description>` — ask user to confirm or change.
4. Propose a body from the template below — user can edit or say "use default".
5. Base branch: `main` — ask only if user says otherwise.
6. Write the body to a temp file, then:
   ```
   gh pr create --base main --head {branch} --title "{title}" --body-file {body_path}
   ```
   `--body-file` avoids quoting problems with a multi-line body.
   If `gh` is missing or unauthenticated, invoke `git-setup`. If the user declines, print the URL:
   `https://github.com/{owner}/{repo}/compare/{branch}?expand=1`
7. Return the PR URL.

### PR body template

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
- Never commit, push, or rebase while on `main`/`master`/`develop` — hard block, no confirmation prompt. The `branch` action is the exception: it runs from a protected branch by design.
- If `git push` is rejected, show the error and ask before doing anything else. The one expected rejection is non-fast-forward straight after a rebase — answer that with `git push --force-with-lease`, never `--force`.
- Edits made while on a protected branch are not lost: `git checkout -b` carries uncommitted changes onto the new branch. Say so instead of suggesting a stash.
- A commit that already landed on a protected branch locally: `git branch qa/{KEY}` to keep it, then `git reset --hard origin/{base}` to clear the protected branch. Show both commands and get confirmation before running the reset — it discards anything uncommitted.
- "start task {KEY}" / "begin {KEY}" → run **branch** automatically.
- "done" / "ready to review" → prompt **push** then **pr** in sequence.

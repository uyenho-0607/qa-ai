---
name: git-setup
description: Set up gh (GitHub CLI) for this repo. Use when user says "setup gh", /git-setup, or when a git or gh command fails because gh is missing or unauthenticated.
---

# Git Setup

One-time setup. Run before first use of `git-workflow`.

1. Check `gh` is installed: `gh --version`
   - Not found → `brew install gh` (macOS). Wait for it to finish.
2. Check auth: `gh auth status`
   - Reports a valid login → "Already set up. You're good to go." Stop here.
   - Reports `token in keyring is invalid` → the stored token expired. Continue; the steps below replace it.
3. Ask: **"Do you have a GitHub Personal Access Token?"**
   - No → instruct:
     1. https://github.com/settings/tokens → **Generate new token (classic)**
     2. Scopes: `repo`, `read:org`. Copy it — shown only once.
4. Ask the user to run this in their own terminal (keeps the token out of the transcript), then report back:
   ```
   gh auth login --hostname github.com --git-protocol https --with-token
   ```
   Paste the token at the prompt. Do not run this from the agent — the Bash tool has no interactive stdin, so it hangs until the timeout.
5. Wire the token into `git push`: `gh auth setup-git`
   Without this, `gh pr create` works but `git push` still prompts for a password.
6. Confirm: `gh auth status` — show output.
7. "Setup complete. You can now use branch, push, rebase, and pr."

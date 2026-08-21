---
name: git-setup
description: Install gh (GitHub CLI), authenticate it with a personal access token, and wire it into git push. Use when user says "setup gh", /git-setup, or when a git or gh command fails because gh is missing or unauthenticated.
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
     1. GitHub → avatar (top-right) → **Settings** → **Developer settings**
     2. **Personal access tokens** → **Tokens (classic)** → **Generate new token**
     3. Scopes: `repo` and `read:org`. For a public-only repo, `public_repo` is enough.
     4. **Generate token** — copy it. It is shown only once.
4. Authenticate with the token:
   ```
   gh auth login --hostname github.com --git-protocol https --with-token
   ```
   Paste the token on stdin. Never echo the token into the transcript or a file.
5. Wire the token into `git push`: `gh auth setup-git`
   Without this, `gh pr create` works but `git push` still prompts for a password.
6. Confirm: `gh auth status` — show output.
7. "Setup complete. You can now use branch, push, rebase, and pr."

## Notes

- The remote is a **public GitHub repo**. Cloning needs no auth; pushing and opening PRs do.
- `gh` reads the owner/repo from `git remote`, so there is no project id to configure.

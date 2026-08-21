---
name: git-setup
description: One-time setup for glab (GitLab CLI) — install and authenticate. Use when user says "setup git", "install glab", /setup, or when glab is not found.
---

# Git Setup

One-time setup. Run before first use of `git-workflow`.

1. Check if `glab` is installed: `glab --version`
   - Not found → `brew install glab` (macOS). Wait for it to finish.
2. Check auth: `glab auth status`
   - Already authenticated → "Already set up. You're good to go." Stop here.
3. Ask: **"Do you have a GitLab Personal Access Token?"**
   - No → instruct:
     1. GitLab → avatar (top-right) → **Edit profile** → **Access Tokens**
     2. **Add new token** — any name, set expiry, scopes: `api`, `read_user`, `write_repository`
     3. **Create** — copy the token (shown only once)
4. Run `glab auth login` — when prompted:
   - Hostname: GitLab host (e.g. `gitlab.com` or company host)
   - Token: paste the PAT
5. Confirm: `glab auth status` — show output.
6. "Setup complete. You can now use branch, push, and mr."

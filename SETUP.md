# Setup

## Who runs what

**A person at a terminal → run the wizard.**

```bash
./onboarding.sh
```

It covers everything below. For each credential it asks whether you already have one — say yes and it skips straight to pasting, no walkthrough. Anything already configured (a saved `.env` value, a connected MCP server) is detected and left alone, so it is safe to stop with Ctrl-C and re-run later.

**An agent → do not run the wizard.** It prompts for pasted secrets and waits on keystrokes. Run from a tool call, every prompt reads empty and blank values overwrite a good `.env`. The script refuses to start without a terminal for exactly that reason.

An agent has two options: tell the user to run `./onboarding.sh` themselves, or work through the manual steps below, asking the user for each `<ASK>` value in conversation. Either way the secrets come from the user.

`./onboarding.sh --test` is safe for anyone to run — it writes nothing and opens no browser tabs.
`./onboarding.sh --fresh` also writes nothing, but pretends nothing is configured, so you can rehearse
the whole flow on a machine that is already set up.

## Prompting from Kiro IDE

Kiro is a VS Code fork, so Claude Code runs inside it as an extension. Do this before the
numbered steps — they assume a Claude session to type into.

1. Open Kiro, then the Extensions view (`⇧⌘X` on Mac, `Ctrl+Shift+X` elsewhere).
2. Search **Claude Code**, publisher Anthropic, and Install. If Kiro's marketplace does not
   list it, install from Open VSX: https://open-vsx.org/extension/Anthropic/claude-code
3. Reload Kiro, then open this project folder.
4. Open the Claude panel and sign in through the browser when it asks. Needs a paid Claude
   plan (Pro, Max, Team, Enterprise) or a Console account — the free plan has no access.

Run the numbered steps below from Kiro's integrated terminal (`` ⌘` ``).

Two things trip people up:

- **The extension reads `.claude/`, not `.kiro/`.** Skills and steering load from `.claude/`
  whenever you prompt through the Claude panel. `.kiro/` feeds Kiro's own agent only, so
  `python3 sync-kiro.py` matters to you only if you use that agent too.
- **MCP servers come from step 3's `claude mcp add`, not `~/.kiro/settings/mcp.json`.** That
  Kiro file does nothing for the Claude panel. Check what is connected with `/mcp` in the panel.

## The manual steps

The wizard automates exactly these. Values marked `<ASK>` are secrets — ask the user for each one. Never guess or invent a value.

## 1. Python dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`.venv/` is gitignored, so a fresh clone has none. Skip the venv and `pip install` fails on Homebrew Python with `externally-managed-environment` (PEP 668).

Skills call `.venv/bin/python3` directly, so nothing needs activating to use them. Activate only when running a helper script by hand.

## 2. Secrets file

```bash
cp .env.example .env
```

Fill `JIRA_EMAIL`, `JIRA_API`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN`.
These feed the Python helpers. The MCP servers in step 3 authenticate separately.

### Google refresh token

`GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` belong to the team's shared Google Cloud project — ask the team lead. The refresh token is per user:

```bash
.venv/bin/python scripts/google_auth.py
```

Opens a browser, you sign in, and it writes both `GOOGLE_REFRESH_TOKEN` and `GOOGLE_SHEETS_REFRESH_TOKEN` to `.env`. Nothing to copy.

This needs that OAuth client to be a **Desktop app** type, or a Web client with `http://localhost` among its authorised redirect URIs. If it is neither, use the [OAuth Playground](https://developers.google.com/oauthplayground) instead:

1. Gear icon — rightmost of the three buttons, top right → tick **Use your own OAuth credentials** → paste the Client ID and Client Secret.
2. Same panel: **Access type** must be **Offline**. Online returns an access token and no refresh token, which is the value you need.
3. Close the panel. Ignore the long API list; in **Input your own scopes** at the bottom of the left column, paste one line:

   ```
   https://www.googleapis.com/auth/spreadsheets https://www.googleapis.com/auth/documents https://www.googleapis.com/auth/drive
   ```

4. **Authorize APIs** → sign in. A `redirect_uri_mismatch` error means the client is missing `https://developers.google.com/oauthplayground` as an authorised redirect URI — the project owner has to add it.
5. Under **Step 2**, click **Exchange authorization code for tokens**, then copy **Refresh token**.
6. Put that value in `.env` as *both* `GOOGLE_REFRESH_TOKEN` and `GOOGLE_SHEETS_REFRESH_TOKEN`.

Only the `spreadsheets` scope is actually read from `.env` — both helpers hit the Sheets API only. Docs and Drive are requested so one consent covers them if that changes.

## 3. MCP servers

List what is already connected, then add only what is missing:

```bash
claude mcp list
```

```bash
claude mcp add -s user playwright -- npx -y @playwright/mcp@latest --browser chrome

claude mcp add -s user testmo \
  -e TESTMO_URL=<ASK> -e TESTMO_API_KEY=<ASK> -e TESTMO_EMAIL=<ASK> -e TESTMO_PASSWORD=<ASK> \
  -- npx -y @aqx-qa/testmo-mcp

claude mcp add -s user figma -e FIGMA_API_KEY=<ASK> -- npx -y figma-developer-mcp --stdio

claude mcp add -s user google-docs \
  -e GOOGLE_CLIENT_ID=<ASK> -e GOOGLE_CLIENT_SECRET=<ASK> \
  -- npx -y @a-bonus/google-docs-mcp
```

`GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` are the same values as in `.env` — one Google OAuth app serves both.

Atlassian Rovo serves Jira and is a claude.ai connector, not a CLI install. The user authorizes it at claude.ai → Settings → Connectors.

## 4. GitHub CLI

Invoke the `git-setup` skill. It installs `gh`, authenticates it with a personal access token, and runs `gh auth setup-git` so `git push` works too.

The repo is public, so cloning needs no auth — pushing and opening PRs do. `gh` reads owner/repo from `git remote`; there is no project id to fill in.

## 5. Project config

Fill every `<FILL_IN>` in `.claude/steering/project-config.md`, then run `python3 sync-kiro.py`.

## 6. Verify

```bash
python3 -c "import jira, googleapiclient, dotenv"   # silent = venv active, deps installed
claude mcp list              # playwright, testmo, figma, google-docs, Atlassian Rovo → Connected
python3 sync-kiro.py --check # 0 stale
```

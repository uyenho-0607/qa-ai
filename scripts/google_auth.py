#!/usr/bin/env python3
"""
Mint a Google refresh token and save it to .env.

Replaces the OAuth Playground walkthrough: opens your browser once, you sign
in with your own account, and the token lands in .env under both names the
helpers read.

    .venv/bin/python scripts/google_auth.py

Needs GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET already in .env — those come
from the team's shared Google Cloud project, not from your account.

The local-server flow needs that OAuth client to be a Desktop app type, or a
Web client with http://localhost among its authorised redirect URIs. If it is
neither, this fails and SETUP.md section 2 has the manual route.
"""

import sys
from pathlib import Path

# Reuse the .env reader/writer rather than reimplementing them.
sys.path.insert(0, str(Path(__file__).parent))
from format_tc_sheet import load_env, save_env_key  # noqa: E402

# Only `spreadsheets` is read from .env today (fetch_gsheet_tcs.py and
# format_tc_sheet.py both hit the Sheets API only). Docs and Drive are here so
# one consent covers the helpers if they ever stop going through the MCP.
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive",
]

# fetch_gsheet_tcs.py prefers GOOGLE_SHEETS_REFRESH_TOKEN; other callers and
# SETUP.md use GOOGLE_REFRESH_TOKEN. Write both so neither goes looking.
TOKEN_KEYS = ("GOOGLE_REFRESH_TOKEN", "GOOGLE_SHEETS_REFRESH_TOKEN")


def main():
    env_file = Path(__file__).parent.parent / ".env"
    env = load_env(env_file)

    client_id = env.get("GOOGLE_CLIENT_ID", "").strip()
    client_secret = env.get("GOOGLE_CLIENT_SECRET", "").strip()
    if not client_id or not client_secret:
        sys.exit("ERROR: set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in .env first")

    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        sys.exit("ERROR: pip install -r requirements.txt")

    flow = InstalledAppFlow.from_client_config(
        {
            "installed": {
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uris": ["http://localhost"],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        SCOPES,
    )

    print("\n  Opening your browser — sign in with your Aquariux account.\n")
    creds = flow.run_local_server(port=0, open_browser=True)

    # Google withholds the refresh token when this app already has consent.
    # Revoking forces a fresh one on the next run.
    if not creds.refresh_token:
        sys.exit(
            "ERROR: no refresh token returned. Remove this app under\n"
            "       https://myaccount.google.com/permissions, then run again."
        )

    for key in TOKEN_KEYS:
        save_env_key(env_file, key, creds.refresh_token)
        print(f"  ✓ saved {key} → .env")


if __name__ == "__main__":
    main()

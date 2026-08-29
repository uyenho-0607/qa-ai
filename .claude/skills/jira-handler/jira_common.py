"""Shared Jira utilities — auth, media UUID resolution, ADF parsing."""

import base64
import os
import re
import ssl
import urllib.request
from pathlib import Path

from dotenv import load_dotenv
from jira import JIRA

load_dotenv(Path(__file__).resolve().parents[3] / ".env")

# Site is project config, not code: set JIRA_SERVER in .env.
# The value for this project is in .claude/steering/jira.md § Rovo MCP.
def server() -> str:
    value = os.environ.get("JIRA_SERVER", "").strip()
    if not value:
        raise SystemExit(
            "JIRA_SERVER is not set. Add it to .env — the value for this project is in "
            ".claude/steering/jira.md § Rovo MCP."
        )
    return value if value.startswith("http") else f"https://{value}"


def get_jira_client() -> JIRA:
    return JIRA(
        server=server(),
        basic_auth=(
            os.environ.get(
                "JIRA_EMAIL", Path("~/.jira_email").expanduser().read_text().strip()
            ),
            Path("~/.jira_token").expanduser().read_text().strip(),
        ),
    )


def get_auth_header() -> str:
    email = Path("~/.jira_email").expanduser().read_text().strip()
    token = Path("~/.jira_token").expanduser().read_text().strip()
    return "Basic " + base64.b64encode(f"{email}:{token}".encode()).decode()


def get_ssl_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def get_media_uuid(attachment_id: str) -> str:
    """Resolve Jira attachment numeric ID → Media Services UUID via redirect.

    The UUID enables "type": "file" in ADF media nodes for inline video playback.
    """
    url = f"{server()}/rest/api/3/attachment/content/{attachment_id}"
    req = urllib.request.Request(
        url,
        method="HEAD",
        headers={
            "Authorization": get_auth_header(),
        },
    )

    class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    opener = urllib.request.build_opener(
        NoRedirectHandler, urllib.request.HTTPSHandler(context=get_ssl_context())
    )
    try:
        opener.open(req)
    except urllib.error.HTTPError as e:
        if e.code in (301, 302, 303, 307, 308):
            location = e.headers.get("Location", "")
            match = re.search(r"/file/([a-f0-9-]+)/binary", location)
            if match:
                return match.group(1)
            raise ValueError(f"UUID not found in Location: {location[:200]}")
        raise
    raise ValueError(f"Expected redirect for attachment {attachment_id}")


def parse_inline_marks(text: str) -> list:
    """Parse **bold** and `code` marks from text into ADF inline nodes."""
    nodes = []
    pattern = r"(\*\*(.+?)\*\*|`(.+?)`)"
    last_end = 0

    for match in re.finditer(pattern, text):
        # Add plain text before this match
        if match.start() > last_end:
            plain = text[last_end : match.start()]
            if plain:
                nodes.append({"type": "text", "text": plain})

        if match.group(2):  # bold
            nodes.append(
                {"type": "text", "text": match.group(2), "marks": [{"type": "strong"}]}
            )
        elif match.group(3):  # code
            nodes.append(
                {"type": "text", "text": match.group(3), "marks": [{"type": "code"}]}
            )
        last_end = match.end()

    # Remaining text
    if last_end < len(text):
        remaining = text[last_end:]
        if remaining:
            nodes.append({"type": "text", "text": remaining})

    if not nodes:
        nodes.append({"type": "text", "text": text})

    return nodes


def markdown_to_adf_content(comment_text: str) -> list:
    """Convert simple markdown comment to ADF content nodes.

    Supported:
    - **bold** → strong mark
    - `code` → code mark
    - Lines starting with "- " → bulletList
    - Blank lines → paragraph breaks
    - Everything else → paragraph
    """
    blocks = []
    lines = comment_text.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i]

        if not line.strip():
            i += 1
            continue

        # Bullet list
        if line.strip().startswith("- "):
            list_items = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                item_text = lines[i].strip()[2:]
                item_nodes = parse_inline_marks(item_text)
                list_items.append(
                    {
                        "type": "listItem",
                        "content": [{"type": "paragraph", "content": item_nodes}],
                    }
                )
                i += 1
            blocks.append({"type": "bulletList", "content": list_items})
            continue

        # Regular paragraph
        para_content = parse_inline_marks(line)
        if para_content:
            blocks.append({"type": "paragraph", "content": para_content})
        i += 1

    return blocks

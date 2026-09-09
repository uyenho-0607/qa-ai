"""Shared Jira utilities — auth, media UUID resolution, ADF parsing."""

import base64
import os
import re
import shutil
import ssl
import subprocess
import urllib.request
from pathlib import Path

from dotenv import load_dotenv
from jira import JIRA

load_dotenv(Path(__file__).resolve().parents[3] / ".env")

# Site is project config, not code: set JIRA_SERVER in .env.
# The value for this project is in .kiro/steering/jira.md § Rovo MCP.
def server() -> str:
    value = os.environ.get("JIRA_SERVER", "").strip()
    if not value:
        raise SystemExit(
            "JIRA_SERVER is not set. Add it to .env — the value for this project is in "
            ".kiro/steering/jira.md § Rovo MCP."
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


# Verdict words carry Jira's bold palette colour on top of **bold**, so a comment's
# result line reads Passed/Failed at a glance. Keys are matched exactly, case-sensitive.
VERDICT_COLORS = {"Passed": "#00875a", "Failed": "#de350b"}


def parse_inline_marks(text: str) -> list:
    """Parse **bold** and `code` marks from text into ADF inline nodes.

    A bold span whose text is a VERDICT_COLORS key also gets a textColor mark.
    """
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
            marks = [{"type": "strong"}]
            color = VERDICT_COLORS.get(match.group(2))
            if color:
                marks.append({"type": "textColor", "attrs": {"color": color}})
            nodes.append({"type": "text", "text": match.group(2), "marks": marks})
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


def media_size(path: str):
    """Read a file's real pixel dimensions -> (width, height), or None.

    ADF media nodes carry intrinsic size only to pin the aspect ratio; the
    rendered size lives on the mediaSingle parent. A wrong intrinsic makes the
    renderer reserve the wrong box, so read the true numbers per file.

    PNG and JPEG are parsed from the header (no dependency); video falls back
    to ffprobe when installed. Anything unreadable returns None.
    """
    p = Path(path)
    try:
        head = p.open("rb").read(2)
    except OSError:
        return None

    if head == b"\x89P":
        return _png_size(p)
    if head == b"\xff\xd8":
        return _jpeg_size(p)
    return _ffprobe_size(p)


def _png_size(p: Path):
    """IHDR is always the first chunk: width/height as big-endian uint32."""
    with p.open("rb") as f:
        data = f.read(24)
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return (
        int.from_bytes(data[16:20], "big"),
        int.from_bytes(data[20:24], "big"),
    )


def _jpeg_size(p: Path):
    """Walk the segment chain to the SOF marker that holds the dimensions."""
    sof = set(range(0xC0, 0xC4)) | set(range(0xC5, 0xC8)) | set(range(0xC9, 0xCC))
    sof |= set(range(0xCD, 0xD0))
    with p.open("rb") as f:
        if f.read(2) != b"\xff\xd8":
            return None
        while True:
            byte = f.read(1)
            if not byte:
                return None
            if byte != b"\xff":
                continue
            marker = f.read(1)
            while marker == b"\xff":  # fill bytes
                marker = f.read(1)
            if not marker:
                return None
            code = marker[0]
            if code in (0xD8, 0xD9) or 0xD0 <= code <= 0xD7:
                continue
            length = f.read(2)
            if len(length) < 2:
                return None
            seg = int.from_bytes(length, "big") - 2
            if code in sof:
                body = f.read(5)
                if len(body) < 5:
                    return None
                height = int.from_bytes(body[1:3], "big")
                width = int.from_bytes(body[3:5], "big")
                return (width, height)
            f.seek(seg, 1)


def _ffprobe_size(p: Path):
    """Video dimensions via ffprobe. None when ffprobe is absent or fails."""
    if not shutil.which("ffprobe"):
        return None
    try:
        out = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-select_streams",
                "v:0",
                "-show_entries",
                "stream=width,height",
                "-of",
                "csv=p=0:s=x",
                str(p),
            ],
            capture_output=True,
            text=True,
            timeout=20,
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None
    parts = out.split("x")[:2]
    if len(parts) != 2 or not all(x.isdigit() for x in parts):
        return None
    return (int(parts[0]), int(parts[1]))

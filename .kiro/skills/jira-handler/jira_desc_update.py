"""Update Jira issue DESCRIPTION with ADF format + inline media.

Atomic: uploads file(s) + resolves UUID(s) + builds ADF + updates description — all in one call.
NOT for comments. For comments use jira_comment.py.

Usage:
    # Atomic: upload evidence + update description with inline media
    .venv/bin/python ~/.kiro/skills/jira-handler/jira_desc_update.py --issue OMS-807 \
        --file ./screenshot.png --filename name.png \
        --adf-file /tmp/desc.json

    # Same but with multiple files
    .venv/bin/python ~/.kiro/skills/jira-handler/jira_desc_update.py --issue OMS-807 \
        --file ./screenshot.png --filename screenshot.png \
        --file ./video.mp4 --filename video.mp4 \
        --adf-file /tmp/desc.json

    # Update description from pre-built ADF file (no upload, UUIDs already in the file)
    .venv/bin/python ~/.kiro/skills/jira-handler/jira_desc_update.py --issue OMS-807 \
        --adf-file /tmp/desc.json

    # Get media UUID for an existing attachment (helper)
    .venv/bin/python ~/.kiro/skills/jira-handler/jira_desc_update.py --get-media-uuid 110043

    # Get multiple media UUIDs at once (comma-separated)
    .venv/bin/python ~/.kiro/skills/jira-handler/jira_desc_update.py --get-media-uuid 111913,111914
"""

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from jira_common import (
    get_auth_header,
    get_jira_client,
    get_media_uuid,
    get_ssl_context,
    SERVER,
)


def update_description(issue_key: str, adf_body: dict):
    """Replace the issue description with ADF content."""
    url = f"{SERVER}/rest/api/3/issue/{issue_key}"
    payload = json.dumps({"fields": {"description": adf_body}}).encode()
    req = urllib.request.Request(
        url,
        data=payload,
        method="PUT",
        headers={
            "Authorization": get_auth_header(),
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    resp = urllib.request.urlopen(req, context=get_ssl_context())
    print(f"✅ Updated {issue_key} description (HTTP {resp.status})")


def main():
    parser = argparse.ArgumentParser(
        description="Update Jira issue DESCRIPTION with ADF (not comments)"
    )
    parser.add_argument("--issue", help="Issue key to update")
    parser.add_argument(
        "--file",
        action="append",
        help="File to upload + inline in description (repeatable)",
    )
    parser.add_argument(
        "--filename", action="append", help="Filename in Jira (repeatable)"
    )
    parser.add_argument(
        "--adf-file",
        help="Path to ADF JSON file. Use {MEDIA_1}, {MEDIA_2}... as placeholders for uploaded file UUIDs.",
    )
    parser.add_argument(
        "--get-media-uuid",
        dest="attachment_ids",
        help="Print media UUID(s) for attachment ID(s). Comma-separated for multiple (e.g. 111913,111914)",
    )
    args = parser.parse_args()

    # Helper mode: just print UUID(s)
    if args.attachment_ids:
        ids = [x.strip() for x in args.attachment_ids.split(",")]
        for att_id in ids:
            uuid = get_media_uuid(att_id)
            print(uuid)
        return

    if not args.issue or not args.adf_file:
        parser.print_help()
        return

    jira = get_jira_client()

    # Upload files if provided and collect UUIDs
    media_uuids = []
    if args.file:
        filenames = args.filename or []
        for i, filepath in enumerate(args.file):
            fname = filenames[i] if i < len(filenames) else Path(filepath).name
            att = jira.add_attachment(
                issue=args.issue, attachment=filepath, filename=fname
            )
            att_id = att.id if hasattr(att, "id") else None
            print(f"Attached {fname} to {args.issue} (id={att_id})")
            uuid = get_media_uuid(str(att_id))
            media_uuids.append(uuid)

    # Read ADF file
    with open(args.adf_file) as f:
        adf_text = f.read()

    # Replace placeholders {MEDIA_1}, {MEDIA_2}, etc. with actual UUIDs
    for i, uuid in enumerate(media_uuids, start=1):
        adf_text = adf_text.replace(f"{{MEDIA_{i}}}", uuid)

    adf_body = json.loads(adf_text)

    # Update description
    update_description(args.issue, adf_body)


if __name__ == "__main__":
    main()

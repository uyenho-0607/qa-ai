"""Post ADF comments to Jira issues with inline media support.

Atomic: uploads file(s) + resolves UUID(s) + posts ONE ADF comment — all in one call.

Usage:
    # Single file + comment
    .venv/bin/python3 .claude/skills/jira-handler/jira_comment.py --issue OMS-807 \
        --file ./video.mp4 --filename name.mp4 \
        --comment $'✅ Verified FIXED — SIT\n\n**Result:**\n- bullet 1'

    # Multiple files + comment (ONE comment, all media inline)
    .venv/bin/python3 .claude/skills/jira-handler/jira_comment.py --issue OMS-807 \
        --file ./screenshot.png --filename neg.png \
        --file ./video.mp4 --filename pos.mp4 \
        --comment $'✅ Verified FIXED — SIT\n\n**Result:**\n- negative case OK\n- positive case OK'

    # Override the inline width (default 500px, height follows aspect ratio)
    .venv/bin/python3 .claude/skills/jira-handler/jira_comment.py --issue OMS-807 \
        --file ./screenshot.png --filename evidence.png --width 700 \
        --comment $'✅ Verified FIXED — SIT'

    # Comment only (no attachment)
    .venv/bin/python3 .claude/skills/jira-handler/jira_comment.py --issue OMS-807 \
        --comment $'✅ Verified FIXED — SIT\n\n**Result:**\n- details'

    # Delete a comment
    .venv/bin/python3 .claude/skills/jira-handler/jira_comment.py --issue OMS-807 --delete 240061
"""

import argparse
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from jira_common import (
    get_auth_header,
    get_jira_client,
    get_media_uuid,
    get_ssl_context,
    markdown_to_adf_content,
    media_size,
    server,
)

DEFAULT_DISPLAY_WIDTH = 500


def build_media_node(media_uuid: str, filename: str, size, display_width: int):
    """One mediaSingle node sized to display_width px.

    Height is not settable in ADF -- the renderer derives it as
    mediaSingle.width x (media.height / media.width). So the media child must
    carry the file's real dimensions and the display width goes on the
    mediaSingle parent with widthType "pixel".

    size None (dimensions unreadable) falls back to the full-width layout.
    """
    media_attrs = {
        "type": "file",
        "id": media_uuid,
        "alt": filename,
        "collection": "",
    }
    if size and display_width:
        media_attrs["width"], media_attrs["height"] = size
        single_attrs = {
            "layout": "center",
            "width": display_width,
            "widthType": "pixel",
        }
    else:
        media_attrs["width"], media_attrs["height"] = size or (2560, 1440)
        single_attrs = {"layout": "full-width"}

    return {
        "type": "mediaSingle",
        "attrs": single_attrs,
        "content": [{"type": "media", "attrs": media_attrs}],
    }


def post_adf_comment(
    issue_key: str,
    comment_text: str,
    media_items: list = None,
    display_width: int = DEFAULT_DISPLAY_WIDTH,
):
    """Post ONE ADF comment with optional inline media.

    Args:
        issue_key: e.g. "OMS-1008"
        comment_text: Markdown-ish text (supports **bold**, `code`, - bullets)
        media_items: List of (media_uuid, filename, size) tuples, size being
            (width, height) or None. None = text only.
        display_width: Rendered width in px; height follows the aspect ratio.
            0 = full-width layout instead.
    """
    content_nodes = markdown_to_adf_content(comment_text)

    if media_items:
        for media_uuid, filename, size in media_items:
            content_nodes.append(
                build_media_node(media_uuid, filename, size, display_width)
            )

    adf_body = {"version": 1, "type": "doc", "content": content_nodes}
    url = f"{server()}/rest/api/3/issue/{issue_key}/comment"
    payload = json.dumps({"body": adf_body}).encode()
    req = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={
            "Authorization": get_auth_header(),
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    resp = urllib.request.urlopen(req, context=get_ssl_context())
    if media_items:
        names = ", ".join(f for _, f, _s in media_items)
        print(
            f"ADF comment posted on {issue_key} (HTTP {resp.status}) with inline: {names}"
        )
    else:
        print(f"ADF comment posted on {issue_key} (HTTP {resp.status})")


def main():
    parser = argparse.ArgumentParser(
        description="Post ADF comment to Jira (with inline media)"
    )
    parser.add_argument("--issue", required=True, help="Jira issue key")
    parser.add_argument(
        "--file", action="append", help="File to upload + inline (repeatable)"
    )
    parser.add_argument(
        "--filename", action="append", help="Filename in Jira (repeatable)"
    )
    parser.add_argument("--comment", help="Comment text (use $'...' for newlines)")
    parser.add_argument(
        "--width",
        type=int,
        default=DEFAULT_DISPLAY_WIDTH,
        help=f"inline media display width in px (default {DEFAULT_DISPLAY_WIDTH}); "
        "height follows the file's aspect ratio. 0 = full-width layout",
    )
    parser.add_argument(
        "--delete", help="Comment ID to delete (before posting new one)"
    )
    args = parser.parse_args()

    jira = get_jira_client()

    # Delete old comment first if requested
    if args.delete:
        comment = jira.comment(args.issue, args.delete)
        comment.delete()
        print(f"Deleted comment {args.delete} from {args.issue}")

    if not args.comment:
        return

    # Upload files and resolve media UUIDs
    media_items = []
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
            size = media_size(filepath)
            if size is None:
                print(f"  ! dimensions unreadable for {fname} — using full-width")
            media_items.append((uuid, fname, size))

    # Post ONE comment with all media inline
    post_adf_comment(args.issue, args.comment, media_items or None, args.width)


if __name__ == "__main__":
    main()

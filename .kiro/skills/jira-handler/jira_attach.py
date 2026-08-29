"""Upload attachments to a Jira issue. Nothing else.

Usage:
    .venv/bin/python3 .kiro/skills/jira-handler/jira_attach.py --issue OMS-807 --file ./video.mp4 --filename name.mp4
    .venv/bin/python3 .kiro/skills/jira-handler/jira_attach.py --issue OMS-807 --file ./a.png --filename a.png --file ./b.mp4 --filename b.mp4
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from jira_common import get_jira_client


def main():
    parser = argparse.ArgumentParser(description="Upload attachments to Jira")
    parser.add_argument("--issue", required=True, help="Jira issue key")
    parser.add_argument(
        "--file", action="append", help="File path (repeatable)"
    )
    parser.add_argument(
        "--filename",
        action="append",
        help="Filename in Jira (repeatable, defaults to local name)",
    )
    parser.add_argument(
        "--delete",
        action="append",
        type=int,
        help="Attachment ID to delete before uploading (repeatable)",
    )
    args = parser.parse_args()

    jira = get_jira_client()

    # Delete old attachments first if requested
    if args.delete:
        for att_id in args.delete:
            jira.delete_attachment(att_id)
            print(f"Deleted attachment {att_id}")

    # Upload
    if args.file:
        filenames = args.filename or []
        for i, filepath in enumerate(args.file):
            fname = filenames[i] if i < len(filenames) else Path(filepath).name
            att = jira.add_attachment(issue=args.issue, attachment=filepath, filename=fname)
            att_id = att.id if hasattr(att, "id") else None
            print(f"Attached {fname} to {args.issue} (id={att_id})")


if __name__ == "__main__":
    main()

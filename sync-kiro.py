#!/usr/bin/env python3
"""Regenerate .kiro/ from .claude/.

.claude/ is the source of truth. .kiro/ is generated output — do not hand-edit it.
The two trees differ by exactly two mechanical transforms:

  1. skill invocation:  Read .claude/skills/<name>/SKILL.md  ->  disclose_context("<name>")
  2. paths:             .claude/...                           ->  .kiro/...

Usage:
    python3 sync-kiro.py                 regenerate .kiro/ from .claude/
    python3 sync-kiro.py --check         report what is stale, change nothing (exit 1 if stale)
    python3 sync-kiro.py --promote PATH  inverse-transform one hand-edited .kiro file back
                                         into .claude (use when you edited the mirror by mistake)

Sync is one-way on purpose: without a stored baseline of the last-synced state, a
two-way sync cannot tell "the source changed" from "the mirror changed", and would
silently discard one side. --promote is the deliberate, per-file exception.
"""
import re
import shutil
import sys
from pathlib import Path

SRC, DST = Path(".claude"), Path(".kiro")
TEXT_SUFFIXES = {".md", ".py", ".sh", ".yaml", ".yml", ".json", ".txt"}

SKILL_READ = re.compile(r"Read\s+\.claude/skills/([A-Za-z0-9_-]+)/SKILL\.md")
DISCLOSE = re.compile(r'disclose_context\("([A-Za-z0-9_-]+)"\)')


def to_kiro(s):
    return SKILL_READ.sub(r'disclose_context("\1")', s).replace(".claude", ".kiro")


def to_claude(s):
    s = s.replace(".kiro", ".claude")
    return DISCLOSE.sub(r"Read .claude/skills/\1/SKILL.md", s)


def sync(check):
    stale, orphans = [], []
    for src in sorted(p for p in SRC.rglob("*") if p.is_file()):
        dst = DST / src.relative_to(SRC)
        if src.suffix in TEXT_SUFFIXES:
            want = to_kiro(src.read_text())
            have = dst.read_text() if dst.exists() else None
            differs = want != have
        else:
            want = None
            differs = not dst.exists() or src.read_bytes() != dst.read_bytes()
        if not differs:
            continue
        stale.append(dst)
        if not check:
            dst.parent.mkdir(parents=True, exist_ok=True)
            if want is None:
                shutil.copy2(src, dst)
            else:
                dst.write_text(want)

    for d in sorted(p for p in DST.rglob("*") if p.is_file()):
        if not (SRC / d.relative_to(DST)).exists():
            orphans.append(d)

    verb = "stale" if check else "synced"
    for p in stale:
        print(f"  {verb}: {p}")
    for p in orphans:
        print(f"  orphan (exists only in .kiro, left alone): {p}")
    print(f"{len(stale)} file(s) {verb}, {len(orphans)} orphan(s)")
    return 1 if (check and stale) else 0


def promote(arg):
    src = Path(arg)
    if not src.is_file():
        sys.exit(f"not a file: {src}")
    try:
        rel = src.relative_to(DST)
    except ValueError:
        sys.exit(f"--promote expects a path inside {DST}/, got: {src}")
    if src.suffix not in TEXT_SUFFIXES:
        sys.exit(f"--promote handles text files only, got: {src.suffix}")
    dst = SRC / rel
    want = to_claude(src.read_text())
    if dst.exists() and dst.read_text() == want:
        print(f"no change: {dst} already matches")
        return 0
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(want)
    print(f"promoted {src} -> {dst}")
    print("Review the diff, then run sync-kiro.py to regenerate the mirror.")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--promote":
        if len(args) != 2:
            sys.exit("usage: sync-kiro.py --promote .kiro/path/to/file.md")
        sys.exit(promote(args[1]))
    if args and args[0] not in ("--check",):
        sys.exit(f"unknown argument: {args[0]}\n{__doc__}")
    sys.exit(sync(check=bool(args)))

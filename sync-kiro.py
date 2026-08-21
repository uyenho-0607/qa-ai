#!/usr/bin/env python3
"""Regenerate .kiro/ from .claude/.

.claude/ is the source of truth. .kiro/ is generated output — do not hand-edit it.
The two trees differ by exactly three mechanical transforms:

  1. skill invocation:  invoke .claude/skills/<name>/SKILL.md  ->  disclose_context("<name>")
                        Read .claude/skills/<name>/SKILL.md   ->  disclose_context("<name>")
                        Invoke the `<name>` skill             ->  disclose_context("<name>")
  2. paths:             .claude/...                           ->  .kiro/...
  3. steering frontmatter: absent in .claude  ->  "inclusion: <value>" in .kiro

`inclusion:` is Kiro-only frontmatter. Claude Code does not parse it in a plain .md, so
it is stripped from .claude/steering/ and injected on the way out. STEERING_ALWAYS lists
the files Kiro should always load; every other .claude/steering/*.md gets "manual".

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

SKILL_READ = re.compile(
    r"(?:[Ii]nvoke\s+the\s+`([A-Za-z0-9_-]+)`\s+skill"
    r"|`?[Rr]ead\s+\.claude/skills/([A-Za-z0-9_-]+)/SKILL\.md`?)"
)
DISCLOSE = re.compile(r'disclose_context\("([A-Za-z0-9_-]+)"\)')

# Kiro steering docs it should load every session. Everything else in steering/ is "manual".
STEERING_ALWAYS = {"project-config.md"}
INCLUSION_FM = re.compile(r"\A---\ninclusion:[^\n]*\n---\n\n?")


def inclusion_for(rel):
    """Kiro `inclusion:` value for this file, or None if it takes no frontmatter."""
    if rel.parent.name != "steering" or rel.suffix != ".md":
        return None
    return "always" if rel.name in STEERING_ALWAYS else "manual"


def _skill_sub(m):
    name = m.group(1) or m.group(2)
    return f'disclose_context("{name}")'


def to_kiro(s, rel):
    s = SKILL_READ.sub(_skill_sub, s).replace(".claude", ".kiro")
    value = inclusion_for(rel)
    if value:
        # strip first so a stray frontmatter in .claude cannot be doubled
        s = f"---\ninclusion: {value}\n---\n\n{INCLUSION_FM.sub('', s)}"
    return s


def to_claude(s, rel):
    s = s.replace(".kiro", ".claude")
    s = DISCLOSE.sub(r"invoke .claude/skills/\1/SKILL.md", s)
    if inclusion_for(rel):
        s = INCLUSION_FM.sub("", s)
    return s


def sync(check):
    stale, orphans = [], []
    for src in sorted(p for p in SRC.rglob("*") if p.is_file()):
        dst = DST / src.relative_to(SRC)
        if src.suffix in TEXT_SUFFIXES:
            want = to_kiro(src.read_text(), src.relative_to(SRC))
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
    want = to_claude(src.read_text(), rel)
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

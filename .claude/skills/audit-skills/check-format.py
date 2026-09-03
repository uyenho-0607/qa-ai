#!/usr/bin/env python3
"""Markdown structure lint: split code spans, unclosed fences, cramped headings."""
import sys
from pathlib import Path

bad = 0
for f in sys.argv[1:]:
    lines = Path(f).read_text().split("\n")
    fence = False
    prev = ""
    for n, l in enumerate(lines, 1):
        if l.strip().startswith("```"):
            fence = not fence
            prev = l
            continue
        if not fence:
            if l.count("`") % 2:
                print(f"{f}:{n}: code span split across lines -> {l.strip()[-60:]!r}")
                bad += 1
            if l.startswith("#") and prev.strip():
                print(f"{f}:{n}: heading with no blank line above -> {l[:50]!r}")
                bad += 1
        prev = l
    if fence:
        print(f"{f}: unclosed ``` fence")
        bad += 1
print(f"{bad} format issue(s)")
sys.exit(1 if bad else 0)

"""Report backticked file references in the given docs that resolve nowhere.

A ref resolves if it exists relative to the repo root, relative to the directory
of the file naming it, or as a basename anywhere in the tree. Templated segments
({KEY}, <name>) are treated as wildcards. What is left is a candidate, not an
error: a doc may name `AGENTS.md` as a kind of document rather than a path.
"""
import re, sys
from collections import defaultdict
from pathlib import Path

REF = re.compile(r"`([^`\s]+\.(?:md|py|sh|json|yaml|yml))`")
SKIP = {".git", ".venv", "node_modules", "__pycache__"}

index = set()
for p in Path(".").rglob("*"):
    if p.is_file() and not any(s in p.parts for s in SKIP):
        index.add(p.name)

unresolved = defaultdict(set)
for f in sys.argv[1:]:
    src = Path(f)
    for ref in set(REF.findall(src.read_text())):
        name = Path(ref).name
        if name in index or Path(ref).exists() or (src.parent / ref).exists():
            continue
        unresolved[ref].add(f)

for ref in sorted(unresolved):
    print(f"  {ref}")
    for f in sorted(unresolved[ref]):
        print(f"      named in {f}")
if not unresolved:
    print("  every ref resolves")

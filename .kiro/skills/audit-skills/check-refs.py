"""Report backticked file references in the given docs that resolve nowhere.

A ref resolves if it exists relative to the repo root, relative to the directory
of the file naming it, or as a basename anywhere in the tree — but the basename
fallback only counts when that basename is unique across the repo; otherwise the
reference must resolve as an actual path. Templated segments ({KEY}, <name>) are
treated as wildcards: matched via glob after substituting them with `*`. What is
left is a candidate, not an error: a doc may name `AGENTS.md` as a kind of
document rather than a path.
"""
import glob
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

REF = re.compile(r"`([^`\s]+\.(?:md|py|sh|json|yaml|yml))`")
SKIP = {".git", ".venv", "node_modules", "__pycache__"}
TEMPLATE = re.compile(r"\{[^}]+\}|<[^>]+>")

index = Counter()
for p in Path(".").rglob("*"):
    if p.is_file() and not any(s in p.parts for s in SKIP):
        index[p.name] += 1


def resolves(ref, src):
    if TEMPLATE.search(ref):
        pattern = TEMPLATE.sub("*", ref)
        return bool(glob.glob(pattern) or glob.glob(str(src.parent / pattern)))
    if Path(ref).exists() or (src.parent / ref).exists():
        return True
    return index[Path(ref).name] == 1


unresolved = defaultdict(set)
for f in sys.argv[1:]:
    src = Path(f)
    for ref in set(REF.findall(src.read_text())):
        if resolves(ref, src):
            continue
        unresolved[ref].add(f)

for ref in sorted(unresolved):
    print(f"  {ref}")
    for f in sorted(unresolved[ref]):
        print(f"      named in {f}")
if not unresolved:
    print("  every ref resolves")

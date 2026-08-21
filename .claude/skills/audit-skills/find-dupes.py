import re, sys
from collections import defaultdict
from pathlib import Path
N = 8
seen = defaultdict(set)
for f in sys.argv[1:]:
    for line in Path(f).read_text().splitlines():
        w = re.findall(r"[a-z]{3,}", line.lower())
        for i in range(len(w) - N + 1):
            seen[" ".join(w[i:i+N])].add(f)
hits = {k: v for k, v in seen.items() if len(v) > 1}
merged, used = [], set()
for k in sorted(hits, key=len, reverse=True):
    if any(k in m for m in used): continue
    used.add(k); merged.append((k, hits[k]))
LIMIT = 12
for k, v in merged[:LIMIT]:
    print(f"  [{len(v)}] {k[:88]}")
    for f in sorted(v): print(f"        {f}")
if not merged:
    print("  no repeats across files")
elif len(merged) > LIMIT:
    print(f"  ... {len(merged) - LIMIT} more repeat(s) suppressed")

#!/usr/bin/env python3
"""Figma reader that filters server-side so only useful bytes reach context.

  figma.py census <fileKey> <nodeId> [--depth N]   screens, variants and their titles, TSV
  figma.py text   <fileKey> <nodeId>[,<nodeId>...] verbatim TEXT copy, document order
  figma.py images <fileKey> <nodeId>[=<name>],...  export PNGs, batched, to --out

Raw payloads run to megabytes; all three subcommands emit well under 1% of that.
Token: FIGMA_API_KEY, from .env at the repo root or the environment.
"""
import argparse, json, os, pathlib, sys, urllib.parse, urllib.request

API = "https://api.figma.com/v1"
PRUNE = ("Notes", "Annotations")   # designer commentary — dropped with its subtree
TITLE = "Step header"              # names the screen it sits beside — kept as a TITLE row
# INSTANCE carries real screens too (a Snackbar on the board is an instance, not a frame)
KEEP_TYPES = ("FRAME", "COMPONENT", "COMPONENT_SET", "INSTANCE", "GROUP")


def token():
    t = os.environ.get("FIGMA_API_KEY")
    if t:
        return t
    for parent in [pathlib.Path.cwd(), *pathlib.Path.cwd().parents]:
        env = parent / ".env"
        if env.exists():
            for line in env.read_text().splitlines():
                if line.startswith("FIGMA_API_KEY="):
                    return line.split("=", 1)[1].strip()
    sys.exit("FIGMA_API_KEY not found in environment or .env")


def fetch(file_key, node_ids, depth=None):
    q = {"ids": node_ids}
    if depth:
        q["depth"] = depth
    url = f"{API}/files/{file_key}/nodes?{urllib.parse.urlencode(q)}"
    req = urllib.request.Request(url, headers={"X-Figma-Token": token()})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"Figma API {e.code}: {e.read().decode()[:200]}")


def walk(node, depth=0, prune=False):
    yield node, depth
    for c in node.get("children", []) or []:
        if prune and c.get("name", "") in PRUNE:
            continue
        yield from walk(c, depth + 1, prune)


def node_text(n):
    out = []
    if n.get("type") == "TEXT":
        s = (n.get("characters") or "").strip()
        if s:
            out.append(s)
    for c in n.get("children", []) or []:
        out += node_text(c)
    return out


def bbox(n):
    b = n.get("absoluteBoundingBox") or {}
    return b.get("x"), b.get("y"), b.get("width"), b.get("height")


def bind_titles(headers, frames):
    """A step header labels the frames sitting below it in its x-band.

    Header and screen are siblings, not parent and child, so the link is spatial:
    each frame belongs to the nearest header above it whose x-band covers the
    frame's centre. One header may own several frames (a Disable *and* an Enable
    modal share one title)."""
    owner = {}
    for f in frames:
        fx, fy, fw, _ = bbox(f)
        if None in (fx, fy, fw):
            continue
        cx = fx + fw / 2
        best = None
        for h in headers:
            hx, hy, hw, _ = bbox(h)
            if None in (hx, hy, hw):
                continue
            if hx <= cx <= hx + hw and hy < fy and (best is None or hy > bbox(best)[1]):
                best = h
        if best is not None:
            owner[f["id"]] = best
    return owner


def cmd_census(a):
    data = fetch(a.file_key, a.node_id, a.depth)
    rows, seen, titles = [], set(), {}
    for doc in (v.get("document") for v in data.get("nodes", {}).values() if v):
        kids = doc.get("children", []) or []
        headers = [k for k in kids if TITLE in k.get("name", "")]
        frames = [k for k in kids if TITLE not in k.get("name", "") and k.get("name", "") not in PRUNE]
        owner = bind_titles(headers, frames)
        for h in headers:
            titles[h["id"]] = " / ".join(node_text(h)) or "(untitled)"
        # id -> owning title, propagated to every descendant of an owned frame
        label = {}
        for f in frames:
            h = owner.get(f["id"])
            if h is None:
                continue
            for n, _ in walk(f, prune=True):
                label[n["id"]] = titles[h["id"]]
        for h in headers:
            rows.append(f"TITLE\t{h['id']}\t{titles[h['id']]}\t")
        for n, _ in walk(doc, prune=True):
            name = n.get("name", "")
            if name in PRUNE or TITLE in name:
                continue
            if n.get("type") not in KEEP_TYPES:
                continue
            key = (n["type"], n["id"], name)
            if key in seen:
                continue
            seen.add(key)
            rows.append(f"{n['type']}\t{n['id']}\t{name}\t{label.get(n['id'], '')}")
    print("\n".join(rows))
    bound = sum(1 for r in rows if r.endswith("\t") is False and r.split("\t")[0] != "TITLE")
    variants = [r for r in rows if "State=" in r]
    print(f"\n# {len(rows)} rows | {len(titles)} TITLE | {bound} title-bound | {len(variants)} State= variants",
          file=sys.stderr)


def cmd_text(a):
    data = fetch(a.file_key, a.node_id)
    for nid, v in (data.get("nodes") or {}).items():
        if not v:
            print(f"## {nid}: NOT FOUND", file=sys.stderr)
            continue
        doc = v["document"]
        print(f"## {nid}  {doc.get('name','')}")
        last, out = None, []
        for n, _ in walk(doc):
            if n.get("type") == "TEXT":
                s = (n.get("characters") or "").strip()
                if s and s != last:
                    out.append(s)
                    last = s
        print("\n".join(out) if out else "(no text nodes)")
        print()


def cmd_images(a):
    items = [s for s in a.node_id.split(",") if s.strip()]
    want = {}
    for it in items:
        nid, _, fname = it.partition("=")
        want[nid.strip()] = fname.strip() or nid.strip().replace(":", "-")
    q = {"ids": ",".join(want), "format": a.format, "scale": a.scale}
    url = f"{API}/images/{a.file_key}?{urllib.parse.urlencode(q)}"
    req = urllib.request.Request(url, headers={"X-Figma-Token": token()})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            payload = json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"Figma API {e.code}: {e.read().decode()[:200]}")
    if payload.get("err"):
        sys.exit(f"Figma images error: {payload['err']}")
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    ok = 0
    for nid, link in (payload.get("images") or {}).items():
        name = want.get(nid, nid.replace(":", "-"))
        if not name.endswith(f".{a.format}"):
            name += f".{a.format}"
        dest = out / name
        if not link:
            print(f"FAIL\t{nid}\t{name}\tno render URL (node not exportable)")
            continue
        try:
            with urllib.request.urlopen(link, timeout=180) as r:
                dest.write_bytes(r.read())
            print(f"OK\t{nid}\t{dest}\t{dest.stat().st_size}")
            ok += 1
        except Exception as e:
            print(f"FAIL\t{nid}\t{name}\t{e}")
    print(f"\n# {ok}/{len(want)} exported to {out}", file=sys.stderr)


p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
sub = p.add_subparsers(dest="cmd", required=True)
c = sub.add_parser("census", help="frames + component-set variants as TSV")
c.add_argument("file_key"); c.add_argument("node_id"); c.add_argument("--depth", type=int)
c.set_defaults(func=cmd_census)
t = sub.add_parser("text", help="verbatim TEXT copy for one or more nodes")
t.add_argument("file_key"); t.add_argument("node_id", help="comma-separated for a batch")
t.set_defaults(func=cmd_text)
i = sub.add_parser("images", help="export PNGs for one or more nodes")
i.add_argument("file_key"); i.add_argument("node_id", help="comma-separated; nodeId=filename to name it")
i.add_argument("--out", required=True); i.add_argument("--scale", type=float, default=2)
i.add_argument("--format", default="png", choices=["png", "svg", "jpg", "pdf"])
i.set_defaults(func=cmd_images)
a = p.parse_args()
a.func(a)

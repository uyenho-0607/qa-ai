#!/usr/bin/env python3
"""
Evidence upload CLI — queue a capture, let a background worker ship it.

The exec run must never block on network I/O. `add` writes one job file and
returns immediately; `serve` runs as a detached worker that drains the queue
while the run carries on testing.

    # once per run, backgrounded by the caller
    python scripts/evidence_upload.py serve  --key AO-925

    # after each capture — returns in milliseconds
    python scripts/evidence_upload.py add    --key AO-925 \\
        --file tasks/AO-925/exec/evidence/TC_161968_c1_login.png \\
        --dest 'doc:1AbC...#TC-161968 · Login with valid passcode'

    # after a wave — block until what you queued has shipped
    python scripts/evidence_upload.py wait   --key AO-925 --timeout 240

    # at report time
    python scripts/evidence_upload.py status --key AO-925 --json
    python scripts/evidence_upload.py retry  --key AO-925
    python scripts/evidence_upload.py stop   --key AO-925

Destinations are chosen by the caller, one `--dest` per target, repeatable:

    drive:{folderId}            file it into that Drive folder, stays private
    doc:{docId}#{heading}       insert it under that heading in a Google Doc

This CLI never edits exec.md. The exec run records its own results; a second
writer racing the run's line index is how a result lands on the wrong TC.

State lives under tasks/{KEY}/exec/.upload/ — queue/, done/, failed/.
"""

import argparse
import hashlib
import json
import os
import signal
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent))
from format_tc_sheet import load_env  # noqa: E402

# ── Config ──────────────────────────────────────────────────────────────────

REPO_ROOT    = Path(__file__).parent.parent
TOKEN_URL    = "https://oauth2.googleapis.com/token"
DRIVE_UPLOAD = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&supportsAllDrives=true"
DRIVE_FILE   = "https://www.googleapis.com/drive/v3/files/{id}?supportsAllDrives=true"
DRIVE_PERM   = "https://www.googleapis.com/drive/v3/files/{id}/permissions?supportsAllDrives=true"
DRIVE_PERM_D = "https://www.googleapis.com/drive/v3/files/{id}/permissions/{pid}?supportsAllDrives=true"
DOCS_GET     = "https://docs.googleapis.com/v1/documents/{id}"
DOCS_BATCH   = "https://docs.googleapis.com/v1/documents/{id}:batchUpdate"

TOKEN_TTL    = 2700          # refresh the access token every 45 min
MIME         = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                ".gif": "image/gif", ".mp4": "video/mp4", ".webm": "video/webm",
                ".mov": "video/quicktime"}
DOC_INSERTABLE = {".png", ".jpg", ".jpeg", ".gif"}


def state_dir(key: str) -> Path:
    return REPO_ROOT / "tasks" / key / "exec" / ".upload"


def dirs(key: str):
    root = state_dir(key)
    return root / "queue", root / "done", root / "failed"


def ensure_dirs(key: str):
    for d in dirs(key):
        d.mkdir(parents=True, exist_ok=True)
    return dirs(key)


def log(msg: str):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


# ── Auth ────────────────────────────────────────────────────────────────────

def get_access_token() -> str:
    env = load_env(REPO_ROOT / ".env")
    for k, v in env.items():
        os.environ.setdefault(k, v)
    missing = [k for k in ("GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "GOOGLE_REFRESH_TOKEN")
               if not os.environ.get(k)]
    if missing:
        raise RuntimeError(f"missing in .env: {', '.join(missing)} — run scripts/google_auth.py")
    resp = requests.post(TOKEN_URL, data={
        "client_id":     os.environ["GOOGLE_CLIENT_ID"],
        "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
        "refresh_token": os.environ["GOOGLE_REFRESH_TOKEN"],
        "grant_type":    "refresh_token",
    }, timeout=20)
    resp.raise_for_status()
    return resp.json()["access_token"]


# ── Drive ───────────────────────────────────────────────────────────────────

def drive_upload(path: Path, token: str, folder_id: str | None) -> str:
    """Upload one file, return its Drive file id. Private unless shared later."""
    mime = MIME.get(path.suffix.lower(), "application/octet-stream")
    meta = {"name": path.name, "mimeType": mime}
    if folder_id:
        meta["parents"] = [folder_id]
    resp = requests.post(
        DRIVE_UPLOAD,
        headers={"Authorization": f"Bearer {token}"},
        files={
            "metadata": (None, json.dumps(meta), "application/json; charset=UTF-8"),
            "file":     (path.name, path.read_bytes(), mime),
        },
        timeout=180,
    )
    resp.raise_for_status()
    return resp.json()["id"]


def drive_share_public(file_id: str, token: str) -> str:
    resp = requests.post(DRIVE_PERM.format(id=file_id),
                         headers={"Authorization": f"Bearer {token}"},
                         json={"role": "reader", "type": "anyone"}, timeout=20)
    resp.raise_for_status()
    return resp.json()["id"]


def drive_unshare(file_id: str, perm_id: str, token: str):
    requests.delete(DRIVE_PERM_D.format(id=file_id, pid=perm_id),
                    headers={"Authorization": f"Bearer {token}"}, timeout=20)


def drive_delete(file_id: str, token: str):
    requests.delete(DRIVE_FILE.format(id=file_id),
                    headers={"Authorization": f"Bearer {token}"}, timeout=20)


# ── Docs ────────────────────────────────────────────────────────────────────

def _para_text(elem) -> str:
    para = elem.get("paragraph")
    if not para:
        return ""
    return "".join(r.get("textRun", {}).get("content", "")
                   for r in para.get("elements", [])).strip()


# What a run writes INTO a section, rather than to start the next one. Both
# carry text, so without these a note would read as the next section's name and
# the following capture would be filed above it.
_STATUS_MARKERS = {"FAILED", "PASSED", "BLOCKED", "PENDING", "SKIPPED"}
_NOTE_PREFIXES = ("ACTUAL:", "EXPECTED:", "NOTE:", "BUG:", "EVIDENCE:")


def _is_section_boundary(elem) -> bool:
    """
    True when `elem` begins the NEXT section.

    A scaffolded evidence doc names each case in a **plain paragraph** — the
    scaffold writes it with `contentFormat: "raw"` so the blank lines a tester
    pastes into survive, and raw text carries no heading style. Paragraph style
    therefore cannot be what separates one section from the next; carrying text
    is. A styled heading still carries text, so a doc that does use heading
    styles keeps working unchanged.

    Three things carry text without starting a section, and each is excluded: an
    image paragraph (no text at all), a verdict marker, and an annotation line.
    Anything else with text is the next case name.
    """
    text = _para_text(elem)
    if not text:
        return False
    upper = text.upper()
    if upper in _STATUS_MARKERS:
        return False
    return not upper.startswith(_NOTE_PREFIXES)


def doc_section_end(doc_id: str, heading: str, token: str) -> int:
    """
    Index to insert at so the image lands at the END of `heading`'s section.

    Inserting at the name's own endIndex puts every new image directly under the
    name, so a TC's frames stack up in reverse. Anchoring to the next section
    keeps them in capture order.
    """
    resp = requests.get(DOCS_GET.format(id=doc_id),
                        headers={"Authorization": f"Bearer {token}"}, timeout=30)
    resp.raise_for_status()
    content = resp.json().get("body", {}).get("content", [])

    start = None
    for i, elem in enumerate(content):
        if _para_text(elem) == heading:
            start = i
            break
    if start is None:
        raise RuntimeError(f"section not found in doc: {heading!r}")

    for elem in content[start + 1:]:
        if _is_section_boundary(elem):
            return elem["startIndex"] - 1
    return content[-1]["endIndex"] - 1


def _image_size(path: Path):
    """Native (width, height) of a PNG/GIF/JPEG, from the header bytes. None if unreadable."""
    try:
        with open(path, "rb") as f:
            head = f.read(26)
            if head.startswith(b"\x89PNG\r\n\x1a\n"):
                return (int.from_bytes(head[16:20], "big"),
                        int.from_bytes(head[20:24], "big"))
            if head[:6] in (b"GIF87a", b"GIF89a"):
                return (int.from_bytes(head[6:8], "little"),
                        int.from_bytes(head[8:10], "little"))
            if head[:2] == b"\xff\xd8":  # JPEG: walk markers to the first SOFn
                f.seek(2)
                while True:
                    marker = f.read(2)
                    if len(marker) < 2 or marker[0] != 0xFF:
                        return None
                    if 0xC0 <= marker[1] <= 0xCF and marker[1] not in (0xC4, 0xC8, 0xCC):
                        f.read(3)
                        h = int.from_bytes(f.read(2), "big")
                        w = int.from_bytes(f.read(2), "big")
                        return (w, h)
                    seg = int.from_bytes(f.read(2), "big")
                    f.seek(seg - 2, 1)
    except OSError:
        pass
    return None


def doc_image_size_pt(path: Path):
    """Insert size in points: width 220 for portrait (docs-media convention),
    450 otherwise; height keeps the native aspect ratio."""
    dims = _image_size(path)
    if dims and dims[0] and dims[1]:
        width = 220.0 if dims[1] > dims[0] else 450.0
        return width, round(width * dims[1] / dims[0], 1)
    return 450.0, 315.0


def doc_insert_image(doc_id: str, at: int, img_url: str, token: str,
                     size_pt=(450.0, 315.0)):
    """
    Open a fresh paragraph at `at`, place the image in it, force it to body text.

    In an empty section `at` lands inside the heading's own paragraph, so the
    break inherits HEADING_n. Left alone, the image paragraph then reads as a
    heading — it shows up in the outline, and the next insert into that section
    anchors to it instead of to the real next heading.
    """
    width, height = size_pt
    payload = {"requests": [
        {"insertText": {"location": {"index": at}, "text": "\n"}},
        {"insertInlineImage": {
            "location": {"index": at + 1},
            "uri": img_url,
            "objectSize": {"height": {"magnitude": height, "unit": "PT"},
                           "width":  {"magnitude": width, "unit": "PT"}},
        }},
        {"updateParagraphStyle": {
            "range": {"startIndex": at + 1, "endIndex": at + 2},
            "paragraphStyle": {"namedStyleType": "NORMAL_TEXT"},
            "fields": "namedStyleType",
        }},
    ]}
    resp = requests.post(DOCS_BATCH.format(id=doc_id),
                         headers={"Authorization": f"Bearer {token}",
                                  "Content-Type": "application/json"},
                         json=payload, timeout=60)
    resp.raise_for_status()


# ── Job execution ───────────────────────────────────────────────────────────

def run_job(job: dict, token: str) -> dict:
    path = Path(job["file"])
    if not path.exists():
        raise RuntimeError(f"file is gone: {path}")

    kind, _, rest = job["dest"].partition(":")

    if kind == "drive":
        file_id = drive_upload(path, token, rest or None)
        return {"drive_file_id": file_id,
                "url": f"https://drive.google.com/file/d/{file_id}/view"}

    if kind == "doc":
        doc_id, _, heading = rest.partition("#")
        if not heading:
            raise RuntimeError("doc dest needs '#<heading>'")
        if path.suffix.lower() not in DOC_INSERTABLE:
            raise RuntimeError(f"{path.suffix} cannot be inlined in a Doc — use a drive: dest")

        # Docs fetches the bytes server-side, so the file must be reachable for
        # the length of one insert. Stage it, insert, then take the sharing back
        # off and drop the staged copy — the Doc keeps its own copy of the image.
        file_id = drive_upload(path, token, job.get("stage_folder"))
        perm_id = None
        try:
            perm_id = drive_share_public(file_id, token)
            at = doc_section_end(doc_id, heading, token)
            doc_insert_image(doc_id, at, f"https://drive.google.com/uc?export=view&id={file_id}", token,
                             size_pt=doc_image_size_pt(path))
        finally:
            if perm_id:
                try:
                    drive_unshare(file_id, perm_id, token)
                except Exception as e:      # noqa: BLE001 — never mask the real error
                    log(f"  WARN could not revoke public link on {file_id}: {e}")
            if not job.get("keep_staged"):
                try:
                    drive_delete(file_id, token)
                except Exception as e:      # noqa: BLE001
                    log(f"  WARN could not delete staged file {file_id}: {e}")
        return {"doc_id": doc_id, "heading": heading}

    raise RuntimeError(f"unknown dest kind {kind!r} — use drive: or doc:")


def _doc_section_ends(content, headings):
    """Anchor index for each heading, from one already-fetched document body."""
    out = {}
    for heading in set(headings):
        start = next((i for i, e in enumerate(content) if _para_text(e) == heading), None)
        if start is None:
            out[heading] = None
            continue
        nxt = next((e["startIndex"] - 1 for e in content[start + 1:] if _is_section_boundary(e)), None)
        out[heading] = content[-1]["endIndex"] - 1 if nxt is None else nxt
    return out


def run_doc_batch(jobs: list, doc_id: str, token: str) -> dict:
    """
    Ship every job targeting one Doc in a single pass, and return {job id: result}.

    Per job the serial path costs six round-trips, one of them a full
    `documents.get` to find the anchor. Here the document is read once, the files
    are staged in parallel, and every insert goes in one `batchUpdate`.

    Requests run in the order given, so an insert shifts every index after it.
    Emitting them by descending anchor keeps the earlier ones valid; ties break by
    descending arrival so two captures in one section stay in capture order.
    """
    resp = requests.get(DOCS_GET.format(id=doc_id),
                        headers={"Authorization": f"Bearer {token}"}, timeout=30)
    resp.raise_for_status()
    content = resp.json().get("body", {}).get("content", [])

    plan, results = [], {}
    anchors = _doc_section_ends(content, [j["dest"].partition("#")[2] for j in jobs])
    for order, job in enumerate(jobs):
        heading = job["dest"].partition("#")[2]
        path = Path(job["file"])
        if not path.exists():
            results[job["id"]] = RuntimeError(f"file is gone: {path}")
        elif path.suffix.lower() not in DOC_INSERTABLE:
            results[job["id"]] = RuntimeError(f"{path.suffix} cannot be inlined in a Doc — use a drive: dest")
        elif anchors.get(heading) is None:
            results[job["id"]] = RuntimeError(f"section not found in doc: {heading!r}")
        else:
            plan.append({"job": job, "path": path, "heading": heading,
                         "at": anchors[heading], "order": order})
    if not plan:
        return results

    def stage(item):
        try:
            item["file_id"] = drive_upload(item["path"], token, item["job"].get("stage_folder"))
            item["perm_id"] = drive_share_public(item["file_id"], token)
        except Exception as e:      # noqa: BLE001
            item["error"] = e
        return item

    with ThreadPoolExecutor(max_workers=min(8, len(plan))) as pool:
        plan = list(pool.map(stage, plan))
    staged = [i for i in plan if not i.get("error")]
    for item in plan:
        if item.get("error"):
            results[item["job"]["id"]] = item["error"]

    if staged:
        staged.sort(key=lambda i: (-i["at"], -i["order"]))
        requests_ = []
        for item in staged:
            at = item["at"]
            width, height = doc_image_size_pt(item["path"])
            requests_ += [
                {"insertText": {"location": {"index": at}, "text": "\n"}},
                {"insertInlineImage": {
                    "location": {"index": at + 1},
                    "uri": f"https://drive.google.com/uc?export=view&id={item['file_id']}",
                    "objectSize": {"height": {"magnitude": height, "unit": "PT"},
                                   "width":  {"magnitude": width, "unit": "PT"}}}},
                {"updateParagraphStyle": {
                    "range": {"startIndex": at + 1, "endIndex": at + 2},
                    "paragraphStyle": {"namedStyleType": "NORMAL_TEXT"},
                    "fields": "namedStyleType"}},
            ]
        try:
            r = requests.post(DOCS_BATCH.format(id=doc_id),
                              headers={"Authorization": f"Bearer {token}",
                                       "Content-Type": "application/json"},
                              json={"requests": requests_}, timeout=120)
            r.raise_for_status()
            for item in staged:
                results[item["job"]["id"]] = {"doc_id": doc_id, "heading": item["heading"]}
        except Exception as e:      # noqa: BLE001
            # One batch is all-or-nothing, so every job in it failed together.
            for item in staged:
                results[item["job"]["id"]] = e

    def cleanup(item):
        if item.get("perm_id"):
            try:
                drive_unshare(item["file_id"], item["perm_id"], token)
            except Exception as e:      # noqa: BLE001
                log(f"  WARN could not revoke public link on {item['file_id']}: {e}")
        if item.get("file_id") and not item["job"].get("keep_staged"):
            try:
                drive_delete(item["file_id"], token)
            except Exception as e:      # noqa: BLE001
                log(f"  WARN could not delete staged file {item['file_id']}: {e}")

    with ThreadPoolExecutor(max_workers=min(8, len(staged) or 1)) as pool:
        list(pool.map(cleanup, staged))
    return results


# ── Subcommands ─────────────────────────────────────────────────────────────

def cmd_add(args) -> int:
    queue, done, failed = ensure_dirs(args.key)
    path = Path(args.file)
    if not path.is_absolute():
        path = REPO_ROOT / path
    if not path.exists():
        print(f"ERROR: no such file: {path}", file=sys.stderr)
        return 1
    if path.stat().st_size == 0:
        print(f"ERROR: file is empty: {path}", file=sys.stderr)
        return 1

    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    queued = 0
    for dest in args.dest:
        # Same bytes to the same place is the same job. This is what stops a
        # re-captured TC, a resumed wave or a retry from double-posting.
        job_id = f"{digest[:16]}_{hashlib.sha1(dest.encode()).hexdigest()[:8]}"
        if not args.force and any(d.joinpath(f"{job_id}.json").exists() for d in (queue, done)):
            print(f"skip (already sent): {path.name} → {dest}")
            continue
        job = {
            "id": job_id,
            "key": args.key,
            "file": str(path),
            "dest": dest,
            "sha256": digest,
            "label": args.label,
            "stage_folder": args.stage_folder,
            "keep_staged": args.keep_staged,
            "queued_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
        # Written whole to a temp name, then moved into place: the worker only
        # ever globs complete files, so it can never read a half-written job.
        tmp = queue / f".{job_id}.part"
        tmp.write_text(json.dumps(job, indent=2))
        tmp.rename(queue / f"{job_id}.json")
        print(f"queued: {path.name} → {dest}")
        queued += 1
    return 0


def cmd_serve(args) -> int:
    queue, done, failed = ensure_dirs(args.key)
    pid_file = state_dir(args.key) / "worker.pid"
    pid_file.write_text(str(os.getpid()))

    stopping = {"now": False}

    def _stop(signum, frame):      # noqa: ARG001
        stopping["now"] = True
        log("stop requested, finishing current job")

    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)

    log(f"worker up — watching {queue}")
    token, minted = None, 0.0
    try:
        while not stopping["now"]:
            pending = sorted(queue.glob("*.json"), key=lambda p: p.stat().st_mtime)
            if not pending:
                if args.once:
                    log("queue drained")
                    break
                time.sleep(args.poll)
                continue

            if token is None or time.time() - minted > TOKEN_TTL:
                token, minted = get_access_token(), time.time()

            loaded = []
            for job_file in pending:
                try:
                    loaded.append((job_file, json.loads(job_file.read_text())))
                except Exception as e:      # noqa: BLE001
                    log(f"unreadable job {job_file.name}: {e}")
                    job_file.rename(failed / job_file.name)

            def settle(job_file, job, outcome):
                if isinstance(outcome, Exception):
                    job["error"] = f"{type(outcome).__name__}: {outcome}"
                    job["failed_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
                    (failed / job_file.name).write_text(json.dumps(job, indent=2))
                    log(f"  FAIL {Path(job['file']).name}: {job['error']}")
                else:
                    job["result"] = outcome
                    job["finished_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
                    (done / job_file.name).write_text(json.dumps(job, indent=2))
                    log(f"  ok  {Path(job['file']).name}")
                job_file.unlink(missing_ok=True)

            # Doc jobs sharing a document ship together — one read, one batchUpdate.
            groups: dict = {}
            singles = []
            for job_file, job in loaded:
                kind, _, rest = job["dest"].partition(":")
                doc_id, sep, heading = rest.partition("#")
                if kind == "doc" and sep and heading:
                    groups.setdefault(doc_id, []).append((job_file, job))
                else:
                    singles.append((job_file, job))

            for doc_id, members in groups.items():
                if len(members) == 1:
                    singles.append(members[0])
                    continue
                log(f"batch → {doc_id} ({len(members)} captures)")
                try:
                    outcomes = run_doc_batch([j for _, j in members], doc_id, token)
                except Exception as e:      # noqa: BLE001
                    outcomes = {j["id"]: e for _, j in members}
                for job_file, job in members:
                    settle(job_file, job, outcomes.get(job["id"], RuntimeError("no result returned")))

            for job_file, job in singles:
                log(f"{job['id']} → {job['dest']}")
                try:
                    settle(job_file, job, run_job(job, token))
                except Exception as e:      # noqa: BLE001
                    settle(job_file, job, e)
    finally:
        pid_file.unlink(missing_ok=True)
        log("worker down")
    return 0


def cmd_status(args) -> int:
    queue, done, failed = ensure_dirs(args.key)
    pid_file = state_dir(args.key) / "worker.pid"
    worker = None
    if pid_file.exists():
        try:
            pid = int(pid_file.read_text().strip())
            os.kill(pid, 0)
            worker = pid
        except (ValueError, ProcessLookupError, PermissionError):
            worker = None

    fails = [json.loads(f.read_text()) for f in sorted(failed.glob("*.json"))]
    report = {
        "key": args.key,
        "worker_pid": worker,
        "queued": len(list(queue.glob("*.json"))),
        "done": len(list(done.glob("*.json"))),
        "failed": len(fails),
        "failures": [{"file": Path(j["file"]).name, "dest": j["dest"],
                      "error": j.get("error", "")} for j in fails],
    }
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        state = f"running (pid {worker})" if worker else "not running"
        print(f"{args.key}: worker {state} · queued {report['queued']} · "
              f"done {report['done']} · failed {report['failed']}")
        for f in report["failures"]:
            print(f"  FAILED  {f['file']} → {f['dest']}\n          {f['error']}")
    # 2 = there is something outstanding, so a caller can branch on it
    return 2 if (report["queued"] or report["failed"]) else 0


def cmd_retry(args) -> int:
    queue, done, failed = ensure_dirs(args.key)
    moved = 0
    for f in sorted(failed.glob("*.json")):
        job = json.loads(f.read_text())
        job.pop("error", None)
        job.pop("failed_at", None)
        (queue / f.name).write_text(json.dumps(job, indent=2))
        f.unlink()
        moved += 1
    print(f"requeued {moved} failed job(s)")
    return 0


def _worker_alive(key: str) -> bool:
    pid_file = state_dir(key) / "worker.pid"
    if not pid_file.exists():
        return False
    try:
        os.kill(int(pid_file.read_text().strip()), 0)
        return True
    except (ValueError, ProcessLookupError, PermissionError):
        return False


def cmd_wait(args) -> int:
    """Block until the queue drains — the one safe way for a caller to wait.

    A caller that wants to know its uploads landed must never start a second
    `serve` to find out: two workers glob the same queue, pick the same job,
    and the loser records a spurious failure over an upload that already went.
    So this polls and never uploads.

    With --drained, an empty queue is not enough: every job must have finished,
    which means nothing queued and nothing failed.
    """
    queue, done, failed = ensure_dirs(args.key)
    deadline = time.time() + args.timeout
    while True:
        queued = len(list(queue.glob("*.json")))
        fails = len(list(failed.glob("*.json")))
        if queued == 0 and (fails == 0 or not args.drained):
            return 0
        if queued and not _worker_alive(args.key):
            # Nobody is going to drain this. Say so rather than spinning to the
            # deadline — the caller decides whether to serve --once itself.
            print(f"ERROR: {queued} job(s) queued and no worker is running",
                  file=sys.stderr)
            return 3
        if time.time() > deadline:
            print(f"ERROR: timed out after {args.timeout}s — "
                  f"{queued} queued, {fails} failed", file=sys.stderr)
            return 2
        time.sleep(args.poll)


def cmd_stop(args) -> int:
    pid_file = state_dir(args.key) / "worker.pid"
    if not pid_file.exists():
        print("no worker running")
        return 0
    try:
        pid = int(pid_file.read_text().strip())
        os.kill(pid, signal.SIGTERM)
        print(f"stopped worker {pid}")
    except (ValueError, ProcessLookupError):
        pid_file.unlink(missing_ok=True)
        print("worker already gone")
    return 0


# ── Entry ───────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(prog="evidence_upload.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def with_key(p):
        p.add_argument("--key", required=True, help="Jira key, e.g. AO-925")
        return p

    a = with_key(sub.add_parser("add", help="queue one file for one or more destinations"))
    a.add_argument("--file", required=True)
    a.add_argument("--dest", required=True, action="append",
                   help="drive:{folderId} | doc:{docId}#{heading} — repeatable")
    a.add_argument("--label", default=None, help="free-text note carried on the job")
    a.add_argument("--stage-folder", default=None,
                   help="Drive folder to stage doc: uploads in (default: My Drive root)")
    a.add_argument("--keep-staged", action="store_true",
                   help="keep the staged Drive copy after inserting into the Doc")
    a.add_argument("--force", action="store_true", help="queue even if already sent")
    a.set_defaults(fn=cmd_add)

    s = with_key(sub.add_parser("serve", help="drain the queue until stopped"))
    s.add_argument("--poll", type=float, default=2.0)
    s.add_argument("--once", action="store_true", help="exit as soon as the queue is empty")
    s.set_defaults(fn=cmd_serve)

    t = with_key(sub.add_parser("status", help="queued / done / failed counts"))
    t.add_argument("--json", action="store_true")
    t.set_defaults(fn=cmd_status)

    w = with_key(sub.add_parser("wait", help="block until the queue drains"))
    w.add_argument("--timeout", type=float, default=240.0)
    w.add_argument("--poll", type=float, default=3.0)
    w.add_argument("--drained", action="store_true",
                   help="also require zero failed jobs, not just an empty queue")
    w.set_defaults(fn=cmd_wait)

    with_key(sub.add_parser("retry", help="move failed jobs back to the queue")).set_defaults(fn=cmd_retry)
    with_key(sub.add_parser("stop", help="signal the worker to finish and exit")).set_defaults(fn=cmd_stop)

    args = ap.parse_args()
    try:
        return args.fn(args)
    except KeyboardInterrupt:
        return 130
    except Exception as e:      # noqa: BLE001
        print(f"ERROR: {type(e).__name__}: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

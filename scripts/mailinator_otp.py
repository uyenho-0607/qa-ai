#!/usr/bin/env python3
"""
mailinator_otp.py
-----------------
Read a Mailinator *public* inbox and pull the OTP out of it.

No signup, no API key, no inbox to create — a public inbox exists the moment
mail arrives at it. Pick any name and hand `<name>@mailinator.com` to the app
under test.

Usage (shell):
    # trigger the OTP in the app first, then
    .venv/bin/python scripts/mailinator_otp.py otp mth2608@mailinator.com
    .venv/bin/python scripts/mailinator_otp.py otp mth2608 --max-age 120

    # only accept mail that lands from here on — use this when re-running a
    # login on an inbox that already holds an older code
    .venv/bin/python scripts/mailinator_otp.py otp mth2608 --after now --timeout 90

    # narrow it when the inbox gets more than one kind of mail
    .venv/bin/python scripts/mailinator_otp.py otp mth2608 \
        --sender aqxotc-sit@s20ip12.com --subject "Verification Code"

    # inspect
    .venv/bin/python scripts/mailinator_otp.py list mth2608
    .venv/bin/python scripts/mailinator_otp.py read mth2608-1787736994-012141308531012

Usage (from another script):
    import sys; sys.path.insert(0, "scripts")
    from mailinator_otp import PublicInbox

    box = PublicInbox("mth2608")          # or the full @mailinator.com address
    cutoff = box.now_ms()                 # stamp BEFORE triggering the mail
    ...trigger the OTP in the app...
    code = box.wait_for_otp(timeout=90, after=cutoff)

Limits worth knowing:
    - Public inboxes are PUBLIC. Anyone who guesses the name reads the mail.
      Fine for SIT throwaways, never for anything real.
    - Mailinator reaps public mail after a few hours, and the listing endpoint
      returns an empty `msgs` array intermittently under rate limiting — this
      polls every 3s and retries past those blips rather than trusting one
      empty read.
    - Only *public* inboxes work without a key. A private/company domain needs
      an API token on /api/v2/domains/private/..., which this does not do.
    - Some apps blocklist disposable-mail domains. If signup rejects the
      address, that is a blocklist, not a bug here.
    - yopmail is blocked on the office network; mailinator is reachable. That
      is the reason this script exists alongside [[mailtm_otp]].

Requirements: requests (already in requirements.txt).
"""

import argparse
import re
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mailtm_otp import extract_otp, strip_html  # noqa: E402  same-dir sibling

API = "https://www.mailinator.com"
POLL_SECONDS = 3
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)


class MailinatorError(RuntimeError):
    """Any non-recoverable failure talking to Mailinator."""


def _request(path, params=None, attempts=5):
    """One Mailinator call, retrying past rate limits and 5xx blips."""
    delay = 1.0
    last = None
    for _ in range(attempts):
        try:
            resp = requests.get(
                f"{API}{path}",
                params=params,
                headers={"Accept": "application/json", "User-Agent": UA},
                timeout=20,
            )
        except requests.RequestException as exc:
            last = str(exc)
        else:
            if resp.status_code in (429, 500, 502, 503, 504):
                last = f"HTTP {resp.status_code}"
            elif resp.status_code == 401:
                raise MailinatorError(
                    f"{path} needs an API token — this script only reads public inboxes"
                )
            elif not resp.ok:
                raise MailinatorError(f"HTTP {resp.status_code} from {path}: {resp.text[:200]}")
            else:
                try:
                    return resp.json()
                except ValueError:
                    last = f"non-JSON body from {path}: {resp.text[:200]}"
        time.sleep(delay)
        delay = min(delay * 2, 8)
    raise MailinatorError(f"{path} failed after {attempts} tries: {last}")


def inbox_name(value):
    """`mth2608@mailinator.com` or `mth2608` -> `mth2608`."""
    name = str(value).strip().split("@", 1)[0]
    if not re.fullmatch(r"[A-Za-z0-9._+-]+", name or ""):
        raise MailinatorError(f"not a usable inbox name: {value!r}")
    return name


class PublicInbox:
    """A Mailinator public inbox. Nothing to create — naming it is enough."""

    def __init__(self, name):
        self.name = inbox_name(name)

    @property
    def address(self):
        return f"{self.name}@mailinator.com"

    @staticmethod
    def now_ms():
        """Epoch-ms stamp to pass as `after`. Take it BEFORE triggering mail."""
        return int(time.time() * 1000)

    # -- messages -----------------------------------------------------------

    def messages(self):
        """Message headers, newest first."""
        data = _request(f"/api/v2/domains/public/inboxes/{self.name}")
        msgs = data.get("msgs") or []
        return sorted(msgs, key=lambda m: m.get("time") or 0, reverse=True)

    def message(self, message_id):
        """Full message. `fetch_public` is the public-inbox body endpoint."""
        data = _request("/fetch_public", params={"msgid": message_id})
        if isinstance(data, dict) and data.get("error"):
            raise MailinatorError(f"{message_id}: {data['error']}")
        return data.get("data") or data

    def body(self, message_id):
        """Subject plus every part, de-tagged, ready to search."""
        full = self.message(message_id)
        parts = [full.get("subject", "")]
        for part in full.get("parts") or []:
            raw = part.get("body") or ""
            ctype = (part.get("headers") or {}).get("content-type", "")
            parts.append(strip_html(raw) if "html" in ctype.lower() else raw)
        return "\n".join(p for p in parts if p)

    # -- waiting ------------------------------------------------------------

    def _matches(self, msg, after, max_age, sender, subject):
        if after is not None and (msg.get("time") or 0) <= int(after):
            return False
        if max_age is not None and (msg.get("seconds_ago") or 0) > int(max_age):
            return False
        if sender:
            known = f"{msg.get('fromfull','')} {msg.get('origfrom','')} {msg.get('from','')}"
            if sender.lower() not in known.lower():
                return False
        if subject and subject.lower() not in (msg.get("subject") or "").lower():
            return False
        return True

    def wait_for_message(self, timeout=90, after=None, max_age=None, sender=None, subject=None):
        """Block until a matching message lands. Returns the header dict.

        A rate-limited listing is a blip, not an answer: keep polling until the
        deadline rather than mistaking a 429 for an empty inbox.
        """
        deadline = time.monotonic() + timeout
        stalled = None
        while True:
            try:
                for msg in reversed(self.messages()):  # oldest first
                    if self._matches(msg, after, max_age, sender, subject):
                        return msg
            except MailinatorError as exc:
                stalled = exc
            if time.monotonic() >= deadline:
                if stalled:
                    raise MailinatorError(
                        f"could not read {self.address} within {timeout}s: {stalled}"
                    )
                raise TimeoutError(f"no matching mail for {self.address} after {timeout}s")
            time.sleep(POLL_SECONDS)

    def wait_for_otp(
        self, timeout=90, digits=6, after=None, max_age=None, sender=None, subject=None
    ):
        """Block until a matching message carries an N-digit code. Returns it."""
        deadline = time.monotonic() + timeout
        while True:
            remaining = max(1, int(deadline - time.monotonic()))
            msg = self.wait_for_message(
                timeout=remaining, after=after, max_age=max_age, sender=sender, subject=subject
            )
            code = extract_otp(self.body(msg["id"]), digits=digits)
            if code:
                return code
            # Right sender, no code in it — step past this one and keep waiting.
            after = msg.get("time") or after
            if time.monotonic() >= deadline:
                raise TimeoutError(
                    f"mail arrived for {self.address} but held no {digits}-digit code"
                )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _resolve_after(value):
    """`now` -> current epoch ms. Anything else is passed through as ms."""
    if value is None:
        return None
    if str(value).lower() == "now":
        return PublicInbox.now_ms()
    try:
        return int(value)
    except ValueError:
        raise MailinatorError(f"--after wants 'now' or an epoch-ms integer, got {value!r}")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Read a Mailinator public inbox and pull out the OTP.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_otp = sub.add_parser("otp", help="wait for an OTP and print it")
    p_otp.add_argument("inbox", help="mth2608 or mth2608@mailinator.com")
    p_otp.add_argument("--timeout", type=int, default=90)
    p_otp.add_argument("--digits", type=int, default=6)
    p_otp.add_argument(
        "--after",
        help="'now', or an epoch-ms stamp taken before triggering the mail",
    )
    p_otp.add_argument(
        "--max-age",
        type=int,
        help="ignore mail older than N seconds — guards against a stale code",
    )
    p_otp.add_argument("--sender", help="substring match on the From address")
    p_otp.add_argument("--subject", help="substring match on the subject")

    p_list = sub.add_parser("list", help="list messages in the inbox")
    p_list.add_argument("inbox")

    p_read = sub.add_parser("read", help="print one message body")
    p_read.add_argument("message_id", help="id from `list` (it carries the inbox name)")

    args = parser.parse_args(argv)

    try:
        if args.command == "read":
            if not args.message_id.strip():
                raise MailinatorError("read wants a message id — get one from `list`")
            # A message id starts with its inbox name: mth2608-1787...-0121...
            box = PublicInbox(args.message_id.split("-", 1)[0])
            print(box.body(args.message_id))
            return 0

        box = PublicInbox(args.inbox)

        if args.command == "otp":
            print(
                box.wait_for_otp(
                    timeout=args.timeout,
                    digits=args.digits,
                    after=_resolve_after(args.after),
                    max_age=args.max_age,
                    sender=args.sender,
                    subject=args.subject,
                )
            )

        elif args.command == "list":
            msgs = box.messages()
            if not msgs:
                print(f"{box.address}: empty", file=sys.stderr)
            for m in msgs:
                print(
                    f"{m['id']}\t{m.get('seconds_ago','?')}s ago\t"
                    f"{m.get('fromfull','?')}\t{m.get('subject','')}"
                )

        return 0

    except (MailinatorError, TimeoutError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

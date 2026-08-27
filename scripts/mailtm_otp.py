#!/usr/bin/env python3
"""
mailtm_otp.py
-------------
Create a throwaway inbox on mail.tm and pull the OTP out of it.

Free, no signup, no API key. Use it wherever a test needs a real address
that can actually receive mail.

Usage (shell):
    # 1. make an inbox — prints the address, remembers the credentials
    .venv/bin/python scripts/mailtm_otp.py new
    .venv/bin/python scripts/mailtm_otp.py new --slot user-b --prefix signup

    # 2. trigger the OTP in the app under test, then
    .venv/bin/python scripts/mailtm_otp.py otp --timeout 90

    # inspect / clean up
    .venv/bin/python scripts/mailtm_otp.py address
    .venv/bin/python scripts/mailtm_otp.py list
    .venv/bin/python scripts/mailtm_otp.py read <message-id>
    .venv/bin/python scripts/mailtm_otp.py purge

Usage (from another script):
    import sys; sys.path.insert(0, "scripts")
    from mailtm_otp import Inbox

    box = Inbox.create()          # or Inbox.load("user-b")
    print(box.address)            # sign up with this
    code = box.wait_for_otp(timeout=90)

Credentials live in .tmp/mailtm/{slot}.json, which is gitignored. --slot keeps
separate inboxes side by side so parallel tests never share one mailbox.
MAILTM_ADDRESS / MAILTM_PASSWORD override the stored slot if set.

Requirements: requests (already in requirements.txt).

Limits worth knowing:
    - mail.tm rate-limits around 8 requests/sec; this polls every 3s.
    - Inboxes are throwaway. mail.tm reaps idle accounts, so make a new one
      per run rather than pinning an address into a test fixture.
    - Some apps block disposable-mail domains. If signup rejects the address
      as invalid, that is a blocklist, not a bug here — fall back to a real
      Gmail account with +tag addressing.
"""

import argparse
import json
import os
import re
import secrets
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from html import unescape
from pathlib import Path

import requests

API = "https://api.mail.tm"
POLL_SECONDS = 3
STATE_DIR = Path(__file__).resolve().parent.parent / ".tmp" / "mailtm"


class MailTmError(RuntimeError):
    """Any non-recoverable failure talking to mail.tm."""


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------

def _request(method, path, token=None, body=None, attempts=5):
    """One mail.tm call, retrying past rate limits and 5xx blips."""
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    delay = 1.0
    response = None
    for _ in range(attempts):
        try:
            response = requests.request(
                method, API + path, headers=headers, json=body, timeout=20
            )
        except requests.RequestException as exc:
            response = None
            time.sleep(delay)
            delay *= 2
            last_exc = exc
            continue
        if response.status_code == 429 or response.status_code >= 500:
            time.sleep(delay)
            delay *= 2
            continue
        break

    if response is None:
        raise MailTmError(f"mail.tm unreachable: {last_exc}")
    if response.status_code >= 400:
        raise MailTmError(
            f"mail.tm {method} {path} -> {response.status_code}: {response.text[:300]}"
        )
    if not response.content:
        return {}
    try:
        return response.json()
    except ValueError:
        return {}


def _members(payload):
    """mail.tm answers either a bare list or a hydra collection."""
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        return payload.get("hydra:member") or payload.get("member") or []
    return []


def pick_domain():
    domains = [
        d["domain"]
        for d in _members(_request("GET", "/domains"))
        if d.get("isActive", True) and not d.get("isPrivate")
    ]
    if not domains:
        raise MailTmError("mail.tm returned no usable domains")
    return domains[0]


# ---------------------------------------------------------------------------
# Text handling
# ---------------------------------------------------------------------------

def strip_html(html):
    if not html:
        return ""
    html = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", html)
    text = re.sub(r"(?s)<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", unescape(text)).strip()


def extract_otp(text, digits=6):
    """Pull an N-digit code out of a mail body.

    Labelled matches win over a bare digit run, so an order number or a year
    sitting elsewhere in the mail does not get mistaken for the code.
    """
    if not text:
        return None

    labelled = re.compile(
        rf"(?:otp|code|pin|passcode|password|verification|verify|token)"
        rf"\W{{0,40}}?(\d{{{digits}}})(?!\d)",
        re.I | re.S,
    )
    match = labelled.search(text)
    if match:
        return match.group(1)

    trailing = re.compile(
        rf"(?<!\d)(\d{{{digits}}})\W{{0,40}}?(?:is your|is the|is you)",
        re.I | re.S,
    )
    match = trailing.search(text)
    if match:
        return match.group(1)

    match = re.search(rf"(?<!\d)(\d{{{digits}}})(?!\d)", text)
    return match.group(1) if match else None


def _parse_ts(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# Inbox
# ---------------------------------------------------------------------------

@dataclass
class Inbox:
    address: str
    password: str
    token: str = ""
    account_id: str = ""
    slot: str = "default"
    created_at: str = field(default="")

    # -- lifecycle ----------------------------------------------------------

    @classmethod
    def create(cls, prefix="qa", slot="default", save=True):
        """Register a fresh mailbox and log into it."""
        address = f"{prefix}-{secrets.token_hex(5)}@{pick_domain()}"
        password = secrets.token_urlsafe(12)
        created = _request(
            "POST", "/accounts", body={"address": address, "password": password}
        )
        box = cls(
            address=address,
            password=password,
            account_id=created.get("id", ""),
            slot=slot,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        box.login()
        if save:
            box.save()
        return box

    @classmethod
    def load(cls, slot="default"):
        """Reopen a saved inbox, or the one named by MAILTM_ADDRESS."""
        env_address = os.environ.get("MAILTM_ADDRESS")
        env_password = os.environ.get("MAILTM_PASSWORD")
        if env_address and env_password:
            box = cls(address=env_address, password=env_password, slot=slot)
            box.login()
            return box

        path = cls.state_path(slot)
        if not path.exists():
            raise MailTmError(
                f"no saved inbox for slot '{slot}'. Run: "
                f"python3 scripts/mailtm_otp.py new --slot {slot}"
            )
        data = json.loads(path.read_text())
        box = cls(
            address=data["address"],
            password=data["password"],
            account_id=data.get("account_id", ""),
            slot=slot,
            created_at=data.get("created_at", ""),
        )
        box.login()
        return box

    @staticmethod
    def state_path(slot):
        return STATE_DIR / f"{slot}.json"

    def save(self):
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        path = self.state_path(self.slot)
        path.write_text(
            json.dumps(
                {
                    "address": self.address,
                    "password": self.password,
                    "account_id": self.account_id,
                    "created_at": self.created_at,
                },
                indent=2,
            )
        )
        path.chmod(0o600)
        return path

    def login(self):
        data = _request(
            "POST", "/token", body={"address": self.address, "password": self.password}
        )
        self.token = data.get("token", "")
        if not self.token:
            raise MailTmError(f"mail.tm refused login for {self.address}")
        self.account_id = self.account_id or data.get("id", "")
        return self.token

    # -- messages -----------------------------------------------------------

    def messages(self):
        """Message headers, newest first."""
        items = _members(_request("GET", "/messages", token=self.token))
        return sorted(items, key=lambda m: m.get("createdAt", ""), reverse=True)

    def message(self, message_id):
        return _request("GET", f"/messages/{message_id}", token=self.token)

    def body(self, message_id):
        """Subject plus text plus de-tagged HTML, ready to search."""
        full = self.message(message_id)
        html = full.get("html") or []
        if isinstance(html, list):
            html = " ".join(html)
        parts = [full.get("subject", ""), full.get("text", ""), strip_html(html)]
        return "\n".join(p for p in parts if p)

    def delete(self, message_id):
        _request("DELETE", f"/messages/{message_id}", token=self.token)

    def purge(self):
        """Empty the inbox. Do this before re-triggering on a reused mailbox."""
        count = 0
        for msg in self.messages():
            self.delete(msg["id"])
            count += 1
        return count

    # -- waiting ------------------------------------------------------------

    def wait_for_message(self, timeout=90, after=None, sender=None, subject=None):
        """Block until a matching message lands. Returns the header dict."""
        cutoff = _parse_ts(after) if after else None
        deadline = time.monotonic() + timeout
        while True:
            for msg in reversed(self.messages()):  # oldest first
                if cutoff:
                    stamp = _parse_ts(msg.get("createdAt"))
                    if stamp and stamp <= cutoff:
                        continue
                if sender:
                    from_addr = (msg.get("from") or {}).get("address", "")
                    if sender.lower() not in from_addr.lower():
                        continue
                if subject and subject.lower() not in msg.get("subject", "").lower():
                    continue
                return msg
            if time.monotonic() >= deadline:
                raise TimeoutError(
                    f"no matching mail for {self.address} after {timeout}s"
                )
            time.sleep(POLL_SECONDS)

    def wait_for_otp(self, timeout=90, digits=6, after=None, sender=None, subject=None):
        """Block until a matching message carries an N-digit code. Returns it."""
        deadline = time.monotonic() + timeout
        while True:
            remaining = max(1, int(deadline - time.monotonic()))
            msg = self.wait_for_message(
                timeout=remaining, after=after, sender=sender, subject=subject
            )
            code = extract_otp(self.body(msg["id"]), digits=digits)
            if code:
                return code
            # Right sender, no code in it — skip past this one and keep waiting.
            after = msg.get("createdAt") or after
            if time.monotonic() >= deadline:
                raise TimeoutError(
                    f"mail arrived for {self.address} but held no {digits}-digit code"
                )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _resolve_after(value):
    if value is None:
        return None
    if value.lower() == "now":
        return datetime.now(timezone.utc).isoformat()
    return value


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Throwaway mail.tm inbox + OTP fetcher.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--slot", default="default", help="named inbox, for parallel tests"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_new = sub.add_parser("new", help="create an inbox and print the address")
    p_new.add_argument("--prefix", default="qa", help="local-part prefix")

    p_otp = sub.add_parser("otp", help="wait for an OTP and print it")
    p_otp.add_argument("--timeout", type=int, default=90, help="seconds (default 90)")
    p_otp.add_argument("--digits", type=int, default=6, help="code length (default 6)")
    p_otp.add_argument("--after", help="ISO timestamp, or 'now' to ignore old mail")
    p_otp.add_argument("--sender", help="only mail whose From contains this")
    p_otp.add_argument("--subject", help="only mail whose Subject contains this")

    sub.add_parser("address", help="print the saved address")
    sub.add_parser("list", help="list messages in the inbox")
    sub.add_parser("purge", help="delete every message in the inbox")

    p_read = sub.add_parser("read", help="print one message body")
    p_read.add_argument("message_id")

    args = parser.parse_args(argv)

    try:
        if args.command == "new":
            box = Inbox.create(prefix=args.prefix, slot=args.slot)
            print(f"saved to {box.state_path(box.slot)}", file=sys.stderr)
            print(box.address)
            return 0

        box = Inbox.load(slot=args.slot)

        if args.command == "address":
            print(box.address)

        elif args.command == "otp":
            code = box.wait_for_otp(
                timeout=args.timeout,
                digits=args.digits,
                after=_resolve_after(args.after),
                sender=args.sender,
                subject=args.subject,
            )
            print(code)

        elif args.command == "list":
            msgs = box.messages()
            if not msgs:
                print(f"{box.address}: empty", file=sys.stderr)
            for m in msgs:
                sender = (m.get("from") or {}).get("address", "?")
                print(f"{m['id']}\t{m.get('createdAt','')}\t{sender}\t{m.get('subject','')}")

        elif args.command == "read":
            print(box.body(args.message_id))

        elif args.command == "purge":
            print(f"deleted {box.purge()} message(s) from {box.address}", file=sys.stderr)

        return 0

    except (MailTmError, TimeoutError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

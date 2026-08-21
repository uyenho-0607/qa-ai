"""Fetch test cases from a Google Sheet and save as a structured markdown file.

Reads a sheet tab named {issue-key} (or TC-{issue-key} as fallback) from the
given spreadsheet, merges continuation rows (one row per step), and writes
`tasks/{issue-key}/tc.md`.

Auth: uses GOOGLE_SHEETS_REFRESH_TOKEN from .env (falls back to GOOGLE_REFRESH_TOKEN).
Run `scripts/format_tc_sheet.py` first to generate/update the target sheet.

Usage:
    python3 .claude/skills/collect-gsheet-cases/fetch_gsheet_tcs.py \
        --issue AO-306 \
        --sheet-id 1WqA2mpZpcg2e3IRetZOjD0L8Si_6Z8Q2xkbKwiAIYOc

Output: tasks/{issue-key}/tc.md
"""

import argparse
import os
import re
from pathlib import Path

import requests
from dotenv import load_dotenv

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
SHEETS_API_URL = "https://sheets.googleapis.com/v4/spreadsheets"

# Logical field -> accepted header spellings (normalised: lowercase, alphanumeric only).
FIELD_HEADERS = {
    "id": ["testid"],
    "module": ["module"],
    "name": ["name"],
    "scenario": ["testscenario", "scenario"],
    "type": ["testcasetype", "tescasetype", "type"],
    "prerequisites": ["prerequisites", "prerequisite"],
    "steps": ["steps", "step"],
    "test_data": ["testdata"],
    "expected": ["expectedresult", "expectedresults"],
    "priority": ["priority"],
    "requirement_ref": ["requirementreference", "requirementref"],
    "automation": ["automation"],
}


def repo_root() -> Path:
    """Return the repository root, found by walking up from this file."""
    for parent in Path(__file__).resolve().parents:
        if (parent / ".git").exists():
            return parent
    raise SystemExit("Repository root not found — no .git directory above this script.")


def get_access_token() -> str:
    """Exchange refresh token for a short-lived access token."""
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    # Prefer the dedicated Sheets token; fall back to the generic refresh token
    refresh_token = os.getenv("GOOGLE_SHEETS_REFRESH_TOKEN") or os.getenv("GOOGLE_REFRESH_TOKEN")

    missing = [k for k, v in [
        ("GOOGLE_CLIENT_ID", client_id),
        ("GOOGLE_CLIENT_SECRET", client_secret),
        ("GOOGLE_SHEETS_REFRESH_TOKEN / GOOGLE_REFRESH_TOKEN", refresh_token),
    ] if not v]
    if missing:
        raise SystemExit(f"Missing env vars: {', '.join(missing)}. Check your .env file.")

    resp = requests.post(GOOGLE_TOKEN_URL, data={
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
    }, timeout=10)
    resp.raise_for_status()
    return resp.json()["access_token"]


def find_sheet_tab(spreadsheet_id: str, issue_key: str, token: str) -> str:
    """Return the sheet tab name matching {issue-key} or TC-{issue-key}."""
    resp = requests.get(
        f"{SHEETS_API_URL}/{spreadsheet_id}",
        headers={"Authorization": f"Bearer {token}"},
        params={"fields": "sheets.properties.title"},
        timeout=10,
    )
    resp.raise_for_status()
    sheets = [s["properties"]["title"] for s in resp.json().get("sheets", [])]
    # Try exact match first, then TC-{key} prefix convention
    for candidate in [issue_key, f"TC-{issue_key}"]:
        if candidate in sheets:
            return candidate
    raise SystemExit(f"Tab '{issue_key}' or 'TC-{issue_key}' not found. Available tabs: {', '.join(sheets)}")


def fetch_rows(spreadsheet_id: str, tab: str, token: str) -> list[list[str]]:
    """Fetch all rows from the sheet tab."""
    resp = requests.get(
        f"{SHEETS_API_URL}/{spreadsheet_id}/values/{tab}!A1:Z1000",
        headers={"Authorization": f"Bearer {token}"},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json().get("values", [])


def map_columns(header_row: list[str]) -> dict[str, int]:
    """Map each logical field to its column index, based on the sheet's own header row."""
    normalised = {re.sub(r"[^a-z0-9]", "", h.lower()): i for i, h in enumerate(header_row)}
    cols = {}
    for field, spellings in FIELD_HEADERS.items():
        for spelling in spellings:
            if spelling in normalised:
                cols[field] = normalised[spelling]
                break
    if "id" not in cols:
        raise SystemExit(f"No 'Test ID' column in header row: {header_row}")
    return cols


def _prefix_er(er_cell: str, step_num: int) -> str:
    """Prefix each bullet in an ER cell with [step_num] if not already prefixed.

    The sheet stores ER bullets as "1. text\\n2. text" local numbering within the cell.
    We strip that local numbering and replace with [step_num] so tc.md carries the
    correct step association for downstream review tooling.
    """
    lines = [ln.strip() for ln in er_cell.splitlines() if ln.strip()]
    result = []
    for ln in lines:
        # Strip leading "1. " / "2. " local bullet numbering from the sheet cell
        ln = re.sub(r"^\d+\.\s+", "", ln)
        if not re.match(r"^\[\d+\]", ln):
            ln = f"[{step_num}] {ln}"
        result.append(ln)
    return "\n".join(result)


def parse_tcs(rows: list[list[str]], cols: dict[str, int]) -> list[dict]:
    """Parse raw rows into TC dicts, merging continuation rows into parent TC."""
    width = max(cols.values()) + 1

    def cell(row: list[str], field: str) -> str:
        return row[cols[field]].strip() if field in cols else ""

    tcs = []
    current = None

    for row in rows[1:]:  # skip header row
        row = row + [""] * (width - len(row))  # pad short rows to full column width

        if cell(row, "id"):
            if current:
                tcs.append(current)
            current = {
                "id": cell(row, "id"),
                "module": cell(row, "module"),
                "name": cell(row, "name"),
                "scenario": cell(row, "scenario"),
                "type": cell(row, "type"),
                "prerequisites": cell(row, "prerequisites"),
                "steps": [cell(row, "steps")] if cell(row, "steps") else [],
                "test_data": cell(row, "test_data"),
                "expected": [_prefix_er(cell(row, "expected"), 1)] if cell(row, "expected") else [],
                "priority": cell(row, "priority"),
                "requirement_ref": cell(row, "requirement_ref"),
                "automation": cell(row, "automation"),
            }
        elif current:
            # continuation row — merge steps, expected result and test data
            if cell(row, "steps"):
                current["steps"].append(cell(row, "steps"))
            if cell(row, "expected"):
                step_num = len(current["steps"])  # step was appended above
                current["expected"].append(_prefix_er(cell(row, "expected"), step_num))
            if cell(row, "test_data"):
                current["test_data"] = f"{current['test_data']}\n{cell(row, 'test_data')}".strip()

    if current:
        tcs.append(current)

    return tcs


def render_markdown(issue_key: str, tcs: list[dict]) -> str:
    """Render TC list as markdown for consumption by the analysis skill."""
    lines = [f"# Test Cases — {issue_key}\n", f"**Total:** {len(tcs)}\n"]

    for tc in tcs:
        lines.append("---\n")
        lines.append(f"## {tc['id']} — {tc['name']}\n")
        if tc["module"]:
            lines.append(f"- **Module:** {tc['module']}")
        lines.append(f"- **Scenario:** {tc['scenario']}")
        if tc["type"]:
            lines.append(f"- **Type:** {tc['type']}")
        lines.append(f"- **Priority:** {tc['priority'] or 'Not set'}")
        lines.append(f"- **Automation:** {tc['automation'] or 'Not set'}")
        if tc["prerequisites"]:
            lines.append(f"- **Pre-requisites:** {tc['prerequisites']}")
        if tc["test_data"]:
            lines.append(f"- **Test Data:** {tc['test_data']}")
        if tc["requirement_ref"]:
            lines.append(f"- **Requirement Ref:** {tc['requirement_ref']}")
        if tc["steps"]:
            lines.append("\n**Steps:**")
            for step in tc["steps"]:
                lines.append(f"{step}")
        if tc["expected"]:
            lines.append("\n**Expected Result:**")
            for exp in tc["expected"]:
                for bullet in exp.splitlines():
                    if bullet.strip():
                        lines.append(f"- {bullet.strip()}")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--issue", required=True, help="Jira issue key, e.g. OMS-165")
    parser.add_argument("--sheet-id", required=True, help="Google Sheets spreadsheet ID")
    args = parser.parse_args()

    root = repo_root()
    load_dotenv(root / ".env")

    issue_key = args.issue.upper()

    print(f"Fetching TCs for {issue_key}...")
    token = get_access_token()
    tab = find_sheet_tab(args.sheet_id, issue_key, token)
    print(f"Found tab: {tab}")

    rows = fetch_rows(args.sheet_id, tab, token)
    if not rows:
        raise SystemExit(f"Tab '{tab}' is empty.")
    tcs = parse_tcs(rows, map_columns(rows[0]))
    if not tcs:
        raise SystemExit(f"No test cases parsed from tab '{tab}'.")
    print(f"Parsed {len(tcs)} test cases")

    output_dir = root / "tasks" / issue_key
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "tc.md"
    output_path.write_text(render_markdown(issue_key, tcs))
    print(f"Saved to {output_path}")


main()

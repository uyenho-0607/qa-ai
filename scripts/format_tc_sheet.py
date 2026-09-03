#!/usr/bin/env python3
"""
format_tc_sheet.py
------------------
Reads a manual-tcs.md file, explodes TCs into one row per step,
writes to a Google Sheet, then applies formatting.

Usage:
    python3 scripts/format_tc_sheet.py \
        --md tasks/{KEY}/manual-tcs.md \
        --sheet 1WqA2mpZpcg2e3IRetZOjD0L8Si_6Z8Q2xkbKwiAIYOc \
        --tab "{KEY}"

Requirements:
    pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
    GOOGLE_APPLICATION_CREDENTIALS or OAuth token in ~/.config/gcloud/
    (or use the same credentials already set up for the MCP Google Workspace integration)

Layout rules (per team convention):
    - Each step = its own sheet row
    - TC metadata (ID, Module, Name, Scenario, Type, Pre-reqs, Test Data,
      Priority, Req Ref, Login Method, Configuration, Story, Automation)
      → written ONLY on the first step row of each TC
    - Expected Result → written ONLY on the LAST step row of each TC
    - Continuation rows: all metadata columns blank, only Steps filled
      (except Expected Result on the last row)

Column order (tc-conventions.md):
    Test ID | Module | Name | Test Scenario | Test Case Type | Pre-requisites |
    Steps | Test Data | Expected Result | Priority | Requirement Reference |
    Login Method | Configuration | Story | Automation
"""

import argparse
import math
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

COLUMNS = [
    "Test ID", "Module", "Name", "Test Scenario", "Test Case Type",
    "Pre-requisites", "Steps", "Test Data", "Expected Result",
    "Priority", "Requirement Reference", "Login Method",
    "Configuration", "Story", "Automation",
]

COL_IDX = {name: i for i, name in enumerate(COLUMNS)}

# TC ID = "{JIRA-KEY}_TC-{nn}", e.g. AO-306_TC-07. The key comes from the .md the agent
# passes in — never hardcoded here, so any project key works. "_TC-INSERT" is the sentinel
# an --insert-md file may use for a TC whose number is assigned by the renumber pass.
TC_ID_RE = re.compile(
    r"^##\s+([A-Za-z][A-Za-z0-9]*-\d+_TC-(?:\d+|INSERT))", re.MULTILINE
)


def parse_tcs(md_path: Path) -> list[dict]:
    """Parse manual-tcs.md into a list of TC dicts."""
    text = md_path.read_text(encoding="utf-8")

    # Extract header-level Story and Configuration
    story = ""
    configuration = ""
    story_m = re.search(r"\*\*Story:\*\*\s*(\S+)", text)
    config_m = re.search(r"\*\*Configuration:\*\*\s*(.+)", text)
    if story_m:
        story = story_m.group(1).strip()
    if config_m:
        configuration = config_m.group(1).strip()

    # Split into TC blocks
    blocks = re.split(r"\n---\n", text)
    tcs = []

    for block in blocks:
        tc_id_m = TC_ID_RE.search(block)
        if not tc_id_m:
            continue

        def field(label: str) -> str:
            # Match only the inline (same-line) value after the label.
            # Stopping at end-of-line prevents empty fields like
            # "**Test Data:**\n" from bleeding into the next field's content.
            pattern = rf"\*\*{re.escape(label)}:\*\*[ \t]*(.+)"
            m = re.search(pattern, block)
            return m.group(1).strip() if m else ""

        def list_field(label: str) -> str:
            """Extract a numbered/bullet list that follows a label, stopping at the next ** field."""
            pattern = rf"\*\*{re.escape(label)}:\*\*\n((?:(?!\*\*).+\n?)+)"
            m = re.search(pattern, block)
            return m.group(1).strip() if m else ""

        # Steps: numbered list
        steps_block = list_field("Steps")
        if not steps_block:
            # fallback: inline
            steps_block = field("Steps")
        steps = re.findall(r"\d+\.\s+(.+)", steps_block)
        steps = [s.replace("`", "") for s in steps]
        if not steps:
            steps = [steps_block] if steps_block else [""]

        # Expected Result: bullet lines
        er_block = list_field("Expected Result")
        if not er_block:
            er_block = field("Expected Result")
        # Normalise to bullet lines
        er_lines = [
            line.lstrip("-• ").strip()
            for line in er_block.splitlines()
            if line.strip().lstrip("-• ").strip()
        ]

        # Split ER bullets: [N] prefix → per-step dict; no prefix → fallback (last row)
        step_prefix_re = re.compile(r"^\[(\d+)\]\s*(.*)")
        er_by_step = {}   # {step_num: [bullet_text, ...]}
        er_fallback = []  # bullets with no [N] prefix — placed on last step row
        for line in er_lines:
            m = step_prefix_re.match(line)
            if m:
                snum = int(m.group(1))
                text = m.group(2).strip()
                er_by_step.setdefault(snum, []).append(f"- {text}")
            else:
                # No [N] prefix — convention requires [N] on every bullet;
                # fall back to last step row to avoid data loss
                er_fallback.append(f"- {line}")

        # Test Data: may have inline backticks or plain text
        test_data_raw = field("Test Data")
        test_data = test_data_raw.replace("`", "").replace("*(recalculate to today", "(recalculate to today")
        # "(empty)" is a human placeholder meaning no test data — treat as blank
        if test_data.strip().lower() == "(empty)":
            test_data = ""

        name_value = field("Name")
        # Module = the first "[Module] – [Sub-module] – ..." segment of the Name field
        # (tc-conventions.md § Name Test Cases). Split on the en/em dash separator —
        # never hardcode a single module for every TC in the file.
        module = re.split(r"[–—]", name_value)[0].strip() if name_value else ""

        # Login Method has its own optional block field (TEMPLATE.md: written inline
        # only when the TC spans multiple platforms). Track whether it was present at
        # all, not just whether it's non-empty, so patch mode (below) can tell an
        # explicit override apart from "this TC doesn't state one".
        login_method_m = re.search(r"\*\*Login Method:\*\*[ \t]*(.+)", block)
        login_method = login_method_m.group(1).strip() if login_method_m else ""

        # Configuration: a per-TC override in the block (TEMPLATE.md note) wins over
        # the file header's default — falls back to the header when the block has none.
        tc_configuration = field("Configuration") or configuration

        tcs.append({
            "id": tc_id_m.group(1),
            "module": module,
            "name": name_value,
            "scenario": field("Test Scenario"),
            "type": field("Test Case Type"),
            "prereqs": field("Pre-requisites"),
            "steps": steps,
            "test_data": test_data,
            "er_by_step": er_by_step,
            "er_fallback": er_fallback,
            "priority": field("Priority"),
            "req_ref": field("Requirement Reference"),
            "login_method": login_method,
            "login_method_explicit": login_method_m is not None,
            "configuration": tc_configuration,
            "story": story,
            "automation": "",
        })

    if not tcs:
        print(f"WARNING: no TC blocks matched in {md_path}. Every block heading must read "
              f"'## {{KEY}}_TC-nn' (e.g. '## AO-306_TC-01').", file=sys.stderr)
    elif story:
        stray = sorted({t["id"] for t in tcs if not t["id"].startswith(f"{story}_TC-")})
        if stray:
            print(f"WARNING: {len(stray)} TC ID(s) do not match the file's "
                  f"**Story:** key '{story}': {', '.join(stray)}", file=sys.stderr)

    return tcs


def explode_to_rows(tcs: list[dict]) -> tuple[list[list[str]], list[tuple[int, int, str]]]:
    """
    Convert TC list to sheet rows.
    - Each step = one row
    - Metadata only on first step row
    - Expected Result only on last step row

    Returns:
        rows: list of row arrays (first entry is the header)
        tc_row_ranges: list of (start, end) 0-based row indices per TC (end exclusive)
    """
    rows = [COLUMNS]  # header
    tc_row_ranges = []

    for tc in tcs:
        steps = tc["steps"]
        n = len(steps)
        tc_start = len(rows)  # 0-based index of this TC's first row

        for i, step in enumerate(steps):
            is_first = i == 0
            is_last  = i == n - 1
            step_num = i + 1  # 1-based

            row = [""] * len(COLUMNS)
            row[COL_IDX["Steps"]] = f"{step_num}. {step}"

            if is_first:
                row[COL_IDX["Test ID"]]              = tc["id"]
                row[COL_IDX["Module"]]               = tc["module"]
                row[COL_IDX["Name"]]                 = tc["name"]
                row[COL_IDX["Test Scenario"]]        = tc["scenario"]
                row[COL_IDX["Test Case Type"]]       = tc["type"]
                prereqs_parts = [p.strip() for p in tc["prereqs"].split(";") if p.strip()]
                prereqs_parts = [p[0].upper() + p[1:] if p else p for p in prereqs_parts]
                row[COL_IDX["Pre-requisites"]]       = "\n".join(f"- {p}" for p in prereqs_parts)
                row[COL_IDX["Test Data"]]            = tc["test_data"]
                row[COL_IDX["Priority"]]             = tc["priority"]
                row[COL_IDX["Requirement Reference"]]= tc["req_ref"]
                row[COL_IDX["Login Method"]]         = tc["login_method"]
                row[COL_IDX["Configuration"]]        = tc["configuration"]
                row[COL_IDX["Story"]]                = tc["story"]
                row[COL_IDX["Automation"]]           = tc["automation"]

            # Distribute Expected Result bullets to their target step rows.
            # Bullets prefixed [N] go on step row N; others go on the last row.
            step_er = tc["er_by_step"].get(step_num, [])
            fallback_er = tc["er_fallback"] if is_last else []
            all_er = step_er + fallback_er
            if all_er:
                numbered_er = [f"{i+1}. {line.lstrip('-• ').strip()}" for i, line in enumerate(all_er)]
                row[COL_IDX["Expected Result"]] = "\n".join(numbered_er)

            rows.append(row)

        tc_row_ranges.append((tc_start, len(rows), tc["priority"]))  # end is exclusive

    return rows, tc_row_ranges


# ---------------------------------------------------------------------------
# Google Sheets API helpers
# ---------------------------------------------------------------------------

def load_env(env_file: Path) -> dict:
    """Parse a .env file into a dict, ignoring comments and blank lines."""
    result = {}
    if not env_file.exists():
        return result
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        result[key.strip()] = val.strip().strip('"').strip("'")
    return result


def save_env_key(env_file: Path, key: str, value: str):
    """Update or append a single key in the .env file."""
    lines = env_file.read_text(encoding="utf-8").splitlines() if env_file.exists() else []
    updated = False
    new_lines = []
    for line in lines:
        if line.strip().startswith(f"{key}="):
            new_lines.append(f'{key}="{value}"')
            updated = True
        else:
            new_lines.append(line)
    if not updated:
        new_lines.append(f'{key}="{value}"')
    env_file.write_text("\n".join(new_lines) + "\n", encoding="utf-8")


def get_sheets_service():
    """
    Build a Sheets API service using Google OAuth (installed-app / Desktop flow).

    Auth strategy:
    1. Load GOOGLE_CLIENT_ID + GOOGLE_CLIENT_SECRET from .env  (required)
    2. If GOOGLE_SHEETS_REFRESH_TOKEN exists in .env → use it silently
    3. Otherwise → open browser for one-time OAuth consent, save the new
       refresh token to .env as GOOGLE_SHEETS_REFRESH_TOKEN for future runs

    Note: uses GOOGLE_SHEETS_REFRESH_TOKEN (not GOOGLE_REFRESH_TOKEN) to
    avoid colliding with the MCP integration token.
    """
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request

    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    TOKEN_KEY = "GOOGLE_SHEETS_REFRESH_TOKEN"

    env_file = Path(__file__).parent.parent / ".env"
    env = load_env(env_file)

    client_id     = env.get("GOOGLE_CLIENT_ID", "").strip()
    client_secret = env.get("GOOGLE_CLIENT_SECRET", "").strip()

    if not client_id or not client_secret:
        print("ERROR: GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET must be set in .env", file=sys.stderr)
        sys.exit(1)

    refresh_token = env.get(TOKEN_KEY, "").strip()

    creds = None

    # --- Try cached refresh token ---
    if refresh_token:
        creds = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret,
            scopes=SCOPES,
        )
        try:
            creds.refresh(Request())
            print("  Auth: cached refresh token (.env → GOOGLE_SHEETS_REFRESH_TOKEN)")
        except Exception as e:
            print(f"  Cached token invalid ({e}), re-authorising ...", file=sys.stderr)
            creds = None

    # --- Browser OAuth flow (first run or token expired) ---
    if not creds or not creds.valid:
        try:
            from google_auth_oauthlib.flow import InstalledAppFlow
        except ImportError:
            print("ERROR: pip install google-auth-oauthlib", file=sys.stderr)
            sys.exit(1)

        client_config = {
            "installed": {
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uris": ["http://localhost", "urn:ietf:wg:oauth:2.0:oob"],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        }

        print("\n  Opening browser for Google OAuth consent ...")
        print("  Sign in with the account that owns the target spreadsheet.\n")
        flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
        creds = flow.run_local_server(port=0, open_browser=True)

        # Persist for next run
        save_env_key(env_file, TOKEN_KEY, creds.refresh_token)
        print(f"  Refresh token saved to .env ({TOKEN_KEY})")

    return build("sheets", "v4", credentials=creds)


def col_letter(n: int) -> str:
    """Convert 0-based column index to letter (A, B, ..., Z, AA, ...)."""
    result = ""
    n += 1
    while n:
        n, r = divmod(n - 1, 26)
        result = chr(65 + r) + result
    return result


def hex_to_rgb(hex_color: str) -> dict:
    """Convert #RRGGBB to Sheets API RGB dict (0.0–1.0)."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return {"red": r / 255, "green": g / 255, "blue": b / 255}


# ---------------------------------------------------------------------------
# Style — single source of truth for every write path
# ---------------------------------------------------------------------------

HEADER_BG         = "#1F3864"   # dark navy
HEADER_FG         = "#FFFFFF"   # white
ROW_ODD_BG        = "#FFFFFF"   # white
ROW_EVEN_BG       = "#F5F5F5"   # warm grey
BORDER_COLOR      = "#AAAAAA"   # mid-grey — inner grid
BORDER_COLOR_HARD = "#555555"   # outer edge + header separator
FONT_FAMILY       = "Arial"
HEADER_FONT_SIZE  = 10
DATA_FONT_SIZE    = 9
ROW_HEIGHT_HEADER = 36          # px — header row, always fixed
FREEZE_ROWS       = 1
FREEZE_COLS       = 1

# Row-height estimation. Sheets' autoResizeDimensions ignores WRAP, so the
# wrapped line count is estimated from char length / chars-per-line.
LINE_H        = 16    # px per wrapped line (Arial 9pt)
CELL_PAD      = 10    # top+bottom cell padding
CHAR_PX       = 6.0   # avg px per char (Arial 9pt)
ROW_MIN_FIRST = 60    # first row of each TC carries most metadata
ROW_MIN_CONT  = 25    # continuation step rows can be compact

PRIORITY_COLORS = {
    "High":   {"bg": "#F4CCCC", "fg": "#990000"},  # red tones
    "Medium": {"bg": "#FCE5CD", "fg": "#7F4F00"},  # orange tones
    "Low":    {"bg": "#D9EAD3", "fg": "#274E13"},  # green tones
}

COL_WIDTHS = {
    COL_IDX["Test ID"]:               120,
    COL_IDX["Module"]:                80,
    COL_IDX["Name"]:                  220,
    COL_IDX["Test Scenario"]:         220,
    COL_IDX["Test Case Type"]:        110,
    COL_IDX["Pre-requisites"]:        200,
    COL_IDX["Steps"]:                 240,
    COL_IDX["Test Data"]:             160,
    COL_IDX["Expected Result"]:       260,
    COL_IDX["Priority"]:              90,
    COL_IDX["Requirement Reference"]: 140,
    COL_IDX["Login Method"]:          80,
    COL_IDX["Configuration"]:         120,
    COL_IDX["Story"]:                 80,
    COL_IDX["Automation"]:            80,
}

# Only Steps and Expected Result drive row height. Metadata columns appear on
# the first step row only and are short; including them oversizes the row.
HEIGHT_DRIVER_COLS = {COL_IDX["Steps"], COL_IDX["Expected Result"]}

BORDER_SOLID  = {"style": "SOLID",        "color": hex_to_rgb(BORDER_COLOR)}
BORDER_MEDIUM = {"style": "SOLID_MEDIUM", "color": hex_to_rgb(BORDER_COLOR_HARD)}


def grid_range(sheet_id: int, start_row: int, end_row: int,
               start_col: int = 0, end_col: int | None = None) -> dict:
    """GridRange spanning the full column set by default."""
    return {
        "sheetId": sheet_id,
        "startRowIndex": start_row,
        "endRowIndex": end_row,
        "startColumnIndex": start_col,
        "endColumnIndex": len(COLUMNS) if end_col is None else end_col,
    }


def row_height(row_data: list[str], is_first: bool) -> int:
    """Estimated px height for one sheet row, floored by its position in the TC."""
    max_lines = 1
    for ci, cell in enumerate(row_data):
        if not cell or ci not in HEIGHT_DRIVER_COLS:
            continue
        chars_per_line = max(1, int(COL_WIDTHS.get(ci, 100) / CHAR_PX))
        lines = sum(
            math.ceil(len(seg) / chars_per_line) if seg else 1
            for seg in cell.split("\n")
        )
        max_lines = max(max_lines, lines)
    return max(max_lines * LINE_H + CELL_PAD,
               ROW_MIN_FIRST if is_first else ROW_MIN_CONT)


def base_font_request(sheet_id: int, start_row: int, end_row: int) -> dict:
    """Data-row baseline: font, top-align, wrap."""
    return {
        "repeatCell": {
            "range": grid_range(sheet_id, start_row, end_row),
            "cell": {
                "userEnteredFormat": {
                    "textFormat": {"fontSize": DATA_FONT_SIZE, "fontFamily": FONT_FAMILY},
                    "verticalAlignment": "TOP",
                    "wrapStrategy": "WRAP",
                }
            },
            "fields": "userEnteredFormat(textFormat,verticalAlignment,wrapStrategy)",
        }
    }


def tc_block_requests(sheet_id: int, sheet_start: int, rows_slice: list[list[str]],
                      priority: str, tc_idx: int) -> list[dict]:
    """Zebra background, Priority-cell colouring, and row heights for one TC block."""
    bg = ROW_ODD_BG if (tc_idx % 2 == 0) else ROW_EVEN_BG
    p_colors = PRIORITY_COLORS.get(priority, {"bg": bg, "fg": "#000000"})
    priority_col = COL_IDX["Priority"]
    sheet_end = sheet_start + len(rows_slice)

    requests = [
        {"repeatCell": {
            "range": grid_range(sheet_id, sheet_start, sheet_end),
            "cell": {"userEnteredFormat": {"backgroundColor": hex_to_rgb(bg)}},
            "fields": "userEnteredFormat.backgroundColor",
        }},
        {"repeatCell": {
            "range": grid_range(sheet_id, sheet_start, sheet_end,
                                priority_col, priority_col + 1),
            "cell": {"userEnteredFormat": {
                "backgroundColor": hex_to_rgb(p_colors["bg"]),
                "textFormat": {
                    "bold": True,
                    "foregroundColor": hex_to_rgb(p_colors["fg"]),
                    "fontSize": DATA_FONT_SIZE,
                    "fontFamily": FONT_FAMILY,
                },
                "horizontalAlignment": "CENTER",
                "verticalAlignment": "MIDDLE",
            }},
            "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment)",
        }},
    ]

    for local_i, row_data in enumerate(rows_slice):
        idx = sheet_start + local_i
        requests.append({
            "updateDimensionProperties": {
                "range": {"sheetId": sheet_id, "dimension": "ROWS",
                          "startIndex": idx, "endIndex": idx + 1},
                "properties": {"pixelSize": row_height(row_data, local_i == 0)},
                "fields": "pixelSize",
            }
        })
    return requests


def block_border_request(sheet_id: int, start_row: int, end_row: int) -> dict:
    """Edge + inner grid borders for a freshly written block."""
    return {
        "updateBorders": {
            "range": grid_range(sheet_id, start_row, end_row),
            "bottom": BORDER_MEDIUM,
            "left":   BORDER_MEDIUM,
            "right":  BORDER_MEDIUM,
            "innerHorizontal": BORDER_SOLID,
            "innerVertical":   BORDER_SOLID,
        }
    }


def write_values(service, spreadsheet_id: str, tab: str,
                 start_row_0based: int, values: list[list[str]]):
    """Write values into columns A-O starting at a 0-based sheet row index."""
    last_col = col_letter(len(COLUMNS) - 1)
    first = start_row_0based + 1
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"{tab}!A{first}:{last_col}{first + len(values) - 1}",
        valueInputOption="RAW",
        body={"values": values},
    ).execute()


def flush(service, spreadsheet_id: str, requests: list[dict]):
    """Fire collected formatting requests as one batchUpdate."""
    if not requests:
        return
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id, body={"requests": requests},
    ).execute()
    print(f"   Formatting applied ({len(requests)} requests)")


def renumber_tc_ids(service, spreadsheet_id: str, tab: str,
                    id_pattern: str = r"^(.+)_TC-(\d+)$") -> int:
    """Renumber every TC ID in the sheet sequentially. Returns the count changed."""
    sheet_rows = read_sheet_rows(service, spreadsheet_id, tab)
    tc_id_re = re.compile(id_pattern)
    tid_col = COL_IDX["Test ID"]
    key_prefix = ""
    ordered_ids: list[tuple[int, str]] = []
    for i, row in enumerate(sheet_rows):
        if i == 0:
            continue
        cell = row[tid_col].strip() if len(row) > tid_col else ""
        m = tc_id_re.match(cell) if cell else None
        if m:
            key_prefix = key_prefix or m.group(1)
            ordered_ids.append((i, cell))

    if not key_prefix:
        print("   ⚠️  No TC IDs found — skipping renumber")
        return 0

    updates = []
    for seq, (row_idx, old_id) in enumerate(ordered_ids, start=1):
        new_id = f"{key_prefix}_TC-{seq:02d}"
        if old_id != new_id:
            updates.append({"range": f"{tab}!{col_letter(tid_col)}{row_idx + 1}",
                            "values": [[new_id]]})
            print(f"   {old_id} → {new_id}")

    if updates:
        service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={"valueInputOption": "RAW", "data": updates},
        ).execute()
    return len(updates)


def write_data(service, spreadsheet_id: str, tab: str, rows: list[list[str]]):
    """Clear TC data columns (A–O) and write all rows. Col P onwards (notes) are preserved."""
    sheets = service.spreadsheets()
    last_col = col_letter(len(COLUMNS) - 1)  # = O

    # Clear only the TC data columns — preserves col P+ (reviewer notes, etc.)
    sheets.values().clear(
        spreadsheetId=spreadsheet_id,
        range=f"{tab}!A:{last_col}",
    ).execute()
    print(f"  Cleared columns A–{last_col} in tab '{tab}' (col P+ preserved)")

    # Write
    last_col = col_letter(len(COLUMNS) - 1)
    range_notation = f"{tab}!A1:{last_col}{len(rows)}"
    sheets.values().update(
        spreadsheetId=spreadsheet_id,
        range=range_notation,
        valueInputOption="RAW",
        body={"values": rows},
    ).execute()
    print(f"  Wrote {len(rows)} rows ({len(rows) - 1} data rows + header)")


def get_sheet_id(service, spreadsheet_id: str, tab: str) -> int:
    """Resolve tab name to numeric sheetId."""
    meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    for sheet in meta["sheets"]:
        if sheet["properties"]["title"] == tab:
            return sheet["properties"]["sheetId"]
    raise ValueError(f"Tab '{tab}' not found in spreadsheet.")


def apply_formatting(
    service,
    spreadsheet_id: str,
    tab: str,
    sheet_id: int,
    num_data_rows: int,
    num_cols: int,
    tc_row_ranges: list,
    rows: list,
):
    """Apply all formatting in a single batchUpdate call."""
    total_rows = num_data_rows + 1  # +1 for header
    requests = []

    # ------------------------------------------------------------------
    # 1. Freeze rows and columns
    # ------------------------------------------------------------------
    requests.append({
        "updateSheetProperties": {
            "properties": {
                "sheetId": sheet_id,
                "gridProperties": {
                    "frozenRowCount": FREEZE_ROWS,
                    "frozenColumnCount": FREEZE_COLS,
                },
            },
            "fields": "gridProperties.frozenRowCount,gridProperties.frozenColumnCount",
        }
    })

    # ------------------------------------------------------------------
    # 2. Header row formatting
    # ------------------------------------------------------------------
    requests.append({
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": 0,
                "endRowIndex": 1,
                "startColumnIndex": 0,
                "endColumnIndex": num_cols,
            },
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": hex_to_rgb(HEADER_BG),
                    "textFormat": {
                        "foregroundColor": hex_to_rgb(HEADER_FG),
                        "bold": True,
                        "fontSize": HEADER_FONT_SIZE,
                        "fontFamily": FONT_FAMILY,
                    },
                    "verticalAlignment": "MIDDLE",
                    "horizontalAlignment": "CENTER",
                    "wrapStrategy": "WRAP",
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat,verticalAlignment,horizontalAlignment,wrapStrategy)",
        }
    })

    # ------------------------------------------------------------------
    # 3. Data rows — base font + wrap + vertical align TOP
    # ------------------------------------------------------------------
    requests.append(base_font_request(sheet_id, 1, total_rows))

    # ------------------------------------------------------------------
    # 4. Per-TC block — zebra background, Priority colour, row heights
    #    tc_row_ranges: list of (start, end, priority) per TC, 0-based
    # ------------------------------------------------------------------
    for tc_idx, (start, end, priority) in enumerate(tc_row_ranges):
        requests.extend(
            tc_block_requests(sheet_id, start, rows[start:end], priority, tc_idx)
        )

    # ------------------------------------------------------------------
    # 5. Borders — outer edge on the whole table + inner grid
    # ------------------------------------------------------------------
    # Outer border (medium)
    requests.append({
        "updateBorders": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": 0,
                "endRowIndex": total_rows,
                "startColumnIndex": 0,
                "endColumnIndex": num_cols,
            },
            "top":    BORDER_MEDIUM,
            "bottom": BORDER_MEDIUM,
            "left":   BORDER_MEDIUM,
            "right":  BORDER_MEDIUM,
        }
    })

    # Inner horizontal lines (thin)
    requests.append({
        "updateBorders": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": 0,
                "endRowIndex": total_rows,
                "startColumnIndex": 0,
                "endColumnIndex": num_cols,
            },
            "innerHorizontal": BORDER_SOLID,
            "innerVertical":   BORDER_SOLID,
        }
    })

    # Header bottom — slightly thicker to separate from data
    requests.append({
        "updateBorders": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": 0,
                "endRowIndex": 1,
                "startColumnIndex": 0,
                "endColumnIndex": num_cols,
            },
            "bottom": BORDER_MEDIUM,
        }
    })

    # ------------------------------------------------------------------
    # 6. Column widths — fixed
    # ------------------------------------------------------------------
    for col_idx, width_px in COL_WIDTHS.items():
        requests.append({
            "updateDimensionProperties": {
                "range": {
                    "sheetId": sheet_id,
                    "dimension": "COLUMNS",
                    "startIndex": col_idx,
                    "endIndex": col_idx + 1,
                },
                "properties": {"pixelSize": width_px},
                "fields": "pixelSize",
            }
        })

    # ------------------------------------------------------------------
    # 7. Header row height — fixed (data-row heights emitted in step 4)
    # ------------------------------------------------------------------
    requests.append({
        "updateDimensionProperties": {
            "range": {"sheetId": sheet_id, "dimension": "ROWS",
                      "startIndex": 0, "endIndex": 1},
            "properties": {"pixelSize": ROW_HEIGHT_HEADER},
            "fields": "pixelSize",
        }
    })

    flush(service, spreadsheet_id, requests)


# ---------------------------------------------------------------------------
# Patch mode — overwrite only specific TC rows in the existing sheet
# ---------------------------------------------------------------------------

def read_sheet_rows(service, spreadsheet_id: str, tab: str) -> list[list[str]]:
    """Read all current rows from the sheet tab. Returns list of row arrays."""
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=tab,
        valueRenderOption="FORMATTED_VALUE",
    ).execute()
    return result.get("values", [])


def find_tc_row_ranges_in_sheet(sheet_rows: list[list[str]]) -> dict[str, tuple[int, int]]:
    """
    Scan existing sheet rows and return a map of tc_id → (start_row, end_row),
    where start_row and end_row are 0-based sheet row indices (end exclusive).
    Row 0 is assumed to be the header.
    """
    tc_ranges: dict[str, tuple[int, int]] = {}
    current_id: str | None = None
    current_start: int = 0
    tid_col = COL_IDX["Test ID"]

    for i, row in enumerate(sheet_rows):
        if i == 0:
            continue  # skip header
        cell_id = row[tid_col].strip() if len(row) > tid_col else ""
        if cell_id and cell_id != current_id:
            # Close previous TC
            if current_id:
                tc_ranges[current_id] = (current_start, i)
            current_id = cell_id
            current_start = i
    # Close last TC
    if current_id:
        tc_ranges[current_id] = (current_start, len(sheet_rows))

    return tc_ranges


def patch_rows_in_place(
    service,
    spreadsheet_id: str,
    tab: str,
    sheet_id: int,
    tcs: list[dict],              # parsed TC dicts — needed to know what was explicit
    new_rows: list[list[str]],   # full set from parse (includes header at [0])
    new_tc_row_ranges: list,     # (start, end, priority) 0-based in new_rows
    patch_id_set: set[str],
):
    """
    Patch only the rows belonging to the TC IDs in patch_id_set.

    Strategy per TC:
    1. Find the TC's current row range in the live sheet (by scanning Test ID column).
    2. Find the TC's new rows in new_rows.
    3. If new step-count == old step-count: update values in-place (no row insert/delete).
       If counts differ: delete old rows, insert the correct number of blank rows, then write.
    4. Re-apply formatting to the affected rows only.

    Module and Automation have no dedicated block field in manual-tcs.md — "module" is
    always *derived* from the Name field, never an explicit per-TC value, and Automation
    is never parsed at all. A patch therefore never has real data for those two columns,
    so it must never overwrite them: doing so would blank/misclassify a value a reviewer
    set directly in the live sheet. Login Method does have an explicit block field, so a
    patch may overwrite it only when that field was actually present in the source block.
    Live values for all three are restored onto the patched row below.
    """
    tcs_by_id = {t["id"]: t for t in tcs}

    # Read current sheet state
    print("   Reading current sheet state ...")
    sheet_rows = read_sheet_rows(service, spreadsheet_id, tab)
    existing_ranges = find_tc_row_ranges_in_sheet(sheet_rows)

    # Build lookup: tc_id → new rows for that TC
    new_tc_lookup: dict[str, list[list[str]]] = {}
    new_priority_lookup: dict[str, str] = {}
    for start, end, priority in new_tc_row_ranges:
        tc_rows_slice = new_rows[start:end]
        if tc_rows_slice:
            tc_id = tc_rows_slice[0][COL_IDX["Test ID"]]
            new_tc_lookup[tc_id] = tc_rows_slice
            new_priority_lookup[tc_id] = priority

    requests = []  # batchUpdate formatting requests collected here
    sheets_api = service.spreadsheets()

    for tc_id in sorted(patch_id_set):
        if tc_id not in new_tc_lookup:
            print(f"   ⚠️  {tc_id} not found in {Path(new_rows[0][0] if new_rows else '').name} — skipping")
            continue

        new_tc_rows = new_tc_lookup[tc_id]
        new_step_count = len(new_tc_rows)

        if tc_id not in existing_ranges:
            print(f"   ⚠️  {tc_id} not found in sheet — skipping (use full write to add new TCs)")
            continue

        old_start, old_end = existing_ranges[tc_id]
        old_step_count = old_end - old_start

        # Snapshot the live values for the columns a patch must not clobber, before
        # any structural change below can shift or blank the row.
        live_first_row = sheet_rows[old_start] if old_start < len(sheet_rows) else []
        def live_val(col_name: str) -> str:
            idx = COL_IDX[col_name]
            return live_first_row[idx] if idx < len(live_first_row) else ""
        live_module = live_val("Module")
        live_login_method = live_val("Login Method")
        live_automation = live_val("Automation")

        print(f"   Patching {tc_id}: sheet rows {old_start+1}–{old_end} "
              f"({old_step_count} step rows) → {new_step_count} step rows")

        # --- Step count changed: delete old rows then insert blanks ---
        if new_step_count != old_step_count:
            diff = new_step_count - old_step_count
            if diff > 0:
                # Insert rows after old_start so we have enough space
                sheets_api.batchUpdate(
                    spreadsheetId=spreadsheet_id,
                    body={"requests": [{
                        "insertDimension": {
                            "range": {
                                "sheetId": sheet_id,
                                "dimension": "ROWS",
                                "startIndex": old_end,
                                "endIndex": old_end + diff,
                            },
                            "inheritFromBefore": True,
                        }
                    }]},
                ).execute()
            else:
                # Delete excess rows from the bottom of the old range
                sheets_api.batchUpdate(
                    spreadsheetId=spreadsheet_id,
                    body={"requests": [{
                        "deleteDimension": {
                            "range": {
                                "sheetId": sheet_id,
                                "dimension": "ROWS",
                                "startIndex": old_end + diff,  # diff is negative
                                "endIndex": old_end,
                            }
                        }
                    }]},
                ).execute()
            # Refresh sheet state after structural change
            sheet_rows = read_sheet_rows(service, spreadsheet_id, tab)
            existing_ranges = find_tc_row_ranges_in_sheet(sheet_rows)
            old_start, old_end = existing_ranges.get(tc_id, (old_start, old_start + new_step_count))

        # --- Restore Module/Login Method/Automation onto the first row unless the
        #     patch source explicitly specifies them (see docstring above) ---
        tc_obj = tcs_by_id.get(tc_id, {})
        if new_tc_rows:
            first_row = list(new_tc_rows[0])
            first_row[COL_IDX["Module"]] = live_module
            if not tc_obj.get("login_method_explicit"):
                first_row[COL_IDX["Login Method"]] = live_login_method
            first_row[COL_IDX["Automation"]] = live_automation
            new_tc_rows = [first_row] + [list(r) for r in new_tc_rows[1:]]

        # --- Write new values into the (now-correct-size) row range ---
        write_values(service, spreadsheet_id, tab, old_start, new_tc_rows)

        # --- Collect formatting requests for this TC block ---
        priority = new_priority_lookup.get(tc_id, "Medium")
        tc_idx = sorted(patch_id_set).index(tc_id)  # zebra parity within the patch set
        requests.append(base_font_request(sheet_id, old_start, old_start + new_step_count))
        requests.extend(tc_block_requests(sheet_id, old_start, new_tc_rows, priority, tc_idx))

    flush(service, spreadsheet_id, requests)
    print(f"   ✅ Patched {len(patch_id_set)} TC(s) — all other rows untouched")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def append_rows_to_sheet(
    service,
    spreadsheet_id: str,
    tab: str,
    sheet_id: int,
    new_rows: list[list[str]],       # rows to append (NO header row)
    new_tc_row_ranges: list,          # (start, end, priority) 0-based within new_rows
    first_new_sheet_row: int,         # 0-based sheet row index where appended data starts
):
    """
    Append new_rows below existing sheet data, then format only those rows.
    Existing rows are never read, modified, or re-formatted.
    """
    if not new_rows:
        print("   Nothing to append.")
        return

    write_values(service, spreadsheet_id, tab, first_new_sheet_row, new_rows)
    print(f"   Wrote {len(new_rows)} rows starting at sheet row {first_new_sheet_row + 1}")

    requests = [base_font_request(sheet_id, first_new_sheet_row,
                                  first_new_sheet_row + len(new_rows))]
    for tc_idx, (local_start, local_end, priority) in enumerate(new_tc_row_ranges):
        requests.extend(tc_block_requests(
            sheet_id, first_new_sheet_row + local_start,
            new_rows[local_start:local_end], priority, tc_idx,
        ))
    requests.append(block_border_request(
        sheet_id, first_new_sheet_row, first_new_sheet_row + len(new_rows)))

    flush(service, spreadsheet_id, requests)
    print(f"   ✅ Appended {len(new_rows)} rows — all existing rows untouched")


def insert_before_tc(
    service,
    spreadsheet_id: str,
    tab: str,
    sheet_id: int,
    before_tc_id: str,
    new_rows: list[list[str]],        # rows to insert (NO header)
    new_tc_row_ranges: list,           # (start, end, priority) 0-based within new_rows
):
    """
    Insert new_rows immediately before the first row of before_tc_id, write and
    format them, then renumber every TC ID sequentially. Col P+ (notes) untouched.
    """
    print("   Reading current sheet ...")
    sheet_rows = read_sheet_rows(service, spreadsheet_id, tab)
    existing_ranges = find_tc_row_ranges_in_sheet(sheet_rows)

    if before_tc_id not in existing_ranges:
        print(f"   ERROR: {before_tc_id} not found in sheet.", file=sys.stderr)
        sys.exit(1)

    insert_at_row, _ = existing_ranges[before_tc_id]  # 0-based sheet row index
    n_new = len(new_rows)
    print(f"   Inserting {n_new} row(s) before sheet row {insert_at_row + 1} ({before_tc_id})")

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={"requests": [{
            "insertDimension": {
                "range": {
                    "sheetId": sheet_id,
                    "dimension": "ROWS",
                    "startIndex": insert_at_row,
                    "endIndex": insert_at_row + n_new,
                },
                "inheritFromBefore": True,
            }
        }]},
    ).execute()

    write_values(service, spreadsheet_id, tab, insert_at_row, new_rows)
    print(f"   Wrote {n_new} row(s) at sheet rows "
          f"{insert_at_row + 1}–{insert_at_row + n_new}")

    requests = [base_font_request(sheet_id, insert_at_row, insert_at_row + n_new)]
    for tc_idx, (local_start, local_end, priority) in enumerate(new_tc_row_ranges):
        requests.extend(tc_block_requests(
            sheet_id, insert_at_row + local_start,
            new_rows[local_start:local_end], priority, tc_idx,
        ))
    requests.append(block_border_request(sheet_id, insert_at_row, insert_at_row + n_new))
    flush(service, spreadsheet_id, requests)

    print("   Renumbering all TC IDs ...")
    changed = renumber_tc_ids(service, spreadsheet_id, tab,
                              id_pattern=r"^(.+)_TC-(\d+|INSERT)$")
    print(f"   ✅ Inserted {n_new} row(s), renumbered {changed} TC ID(s)")


def remove_and_renumber(
    service,
    spreadsheet_id: str,
    tab: str,
    sheet_id: int,
    remove_id_set: set[str],
):
    """
    Delete every row belonging to the TCs in remove_id_set (bottom-up, so row
    indices stay valid), then renumber the survivors sequentially.
    """
    print("   Reading current sheet ...")
    sheet_rows = read_sheet_rows(service, spreadsheet_id, tab)  # [0] = header

    # --- Build map: tc_id → [row_indices] (0-based within sheet_rows) ---
    tc_ranges: dict[str, list[int]] = {}
    current_id: str | None = None
    tid_col = COL_IDX["Test ID"]

    for i, row in enumerate(sheet_rows):
        if i == 0:
            continue
        cell = row[tid_col].strip() if len(row) > tid_col else ""
        if cell:
            current_id = cell
            tc_ranges[current_id] = [i]
        elif current_id:
            tc_ranges[current_id].append(i)

    rows_to_delete: list[int] = []
    for tc_id in remove_id_set:
        if tc_id not in tc_ranges:
            print(f"   ⚠️  {tc_id} not found in sheet — skipping")
            continue
        rows_to_delete.extend(tc_ranges[tc_id])
        print(f"   Removing {tc_id} ({len(tc_ranges[tc_id])} row(s))")

    if not rows_to_delete:
        print("   Nothing to delete.")
        return

    # Delete from the bottom up so earlier indices stay valid
    rows_to_delete.sort(reverse=True)

    def merge_ranges(indices: list[int]) -> list[tuple[int, int]]:
        """Collapse a descending index list into (startIndex, endIndex) spans."""
        ranges = []
        start = end = indices[0]
        for idx in indices[1:]:
            if idx == end - 1:
                end = idx
            else:
                ranges.append((end, start + 1))
                start = end = idx
        ranges.append((end, start + 1))
        return ranges

    delete_ranges = merge_ranges(rows_to_delete)
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={"requests": [
            {"deleteDimension": {
                "range": {"sheetId": sheet_id, "dimension": "ROWS",
                          "startIndex": s, "endIndex": e}
            }}
            for s, e in delete_ranges
        ]},
    ).execute()
    print(f"   Deleted {len(rows_to_delete)} row(s) in {len(delete_ranges)} range(s)")

    changed = renumber_tc_ids(service, spreadsheet_id, tab)
    print(f"   ✅ Removed {len(remove_id_set)} TC(s), renumbered {changed} ID(s)")


def main():
    parser = argparse.ArgumentParser(description="Write and format TC sheet from manual-tcs.md")
    parser.add_argument("--md",         required=True, help="Path to manual-tcs.md")
    parser.add_argument("--sheet",      required=True, help="Google Spreadsheet ID")
    parser.add_argument("--tab",        required=True, help="Sheet tab name")
    parser.add_argument("--dry-run",    action="store_true", help="Parse and print rows only; no API calls")
    parser.add_argument("--patch-ids",  default="",
                        help="Comma-separated TC IDs to patch in-place (e.g. AO-306_TC-02,AO-306_TC-14 — any project key). "
                             "Only those rows are overwritten; all other sheet rows are untouched.")
    parser.add_argument("--insert-before", default="",
                        help="Insert TCs from --insert-md immediately before this TC ID in the sheet, "
                             "then renumber all TCs sequentially. Example: AO-306_TC-18")
    parser.add_argument("--insert-md", default="",
                        help="Path to a manual-tcs.md file whose TCs are inserted at the position "
                             "specified by --insert-before.")
    parser.add_argument("--remove-ids",  default="",
                        help="Comma-separated TC IDs to remove from the sheet, then renumber all remaining "
                             "TCs sequentially. Example: AO-306_TC-06,AO-306_TC-07")
    parser.add_argument("--append-md",  default="",
                        help="Path to a second manual-tcs.md whose TCs are appended after the last "
                             "existing data row. Existing rows are never modified.")
    args = parser.parse_args()

    md_path = Path(args.md)
    if not md_path.exists():
        print(f"ERROR: {md_path} not found", file=sys.stderr)
        sys.exit(1)

    print(f"\n📄 Parsing {md_path} ...")
    tcs = parse_tcs(md_path)
    print(f"   Found {len(tcs)} TCs")

    rows, tc_row_ranges = explode_to_rows(tcs)
    num_data_rows = len(rows) - 1
    print(f"   Exploded to {num_data_rows} sheet rows (one per step)")

    if args.dry_run:
        # Default to the first two parsed TCs; --patch-ids narrows to specific ones.
        check_ids = (
            {i.strip() for i in args.patch_ids.split(",") if i.strip()}
            or {t["id"] for t in tcs[:2]}
        )
        print(f"\n--- DRY RUN: showing all rows for {', '.join(sorted(check_ids))} ---")
        in_tc = None
        for r in rows[1:]:
            tid = r[COL_IDX["Test ID"]]
            if tid in check_ids:
                in_tc = tid
            if in_tc:
                er_snippet = r[COL_IDX["Expected Result"]][:45] if r[COL_IDX["Expected Result"]] else ""
                print(f"  ID={r[COL_IDX['Test ID']]!r:22}  step={r[COL_IDX['Steps']][:55]!r:58}  ER={er_snippet!r}")
                if r[COL_IDX["Expected Result"]]:
                    in_tc = None
        print(f"\n   Total: {len(tcs)} TCs → {num_data_rows} rows, {len(tc_row_ranges)} TC blocks")
        print("\n✅ Dry run complete — no changes made.")
        return

    print("\n🔌 Connecting to Google Sheets ...")
    service = get_sheets_service()
    sheet_id = get_sheet_id(service, args.sheet, args.tab)
    print(f"   Tab '{args.tab}' → sheetId {sheet_id}")

    # ------------------------------------------------------------------
    # Append mode — add TCs from a second .md below existing data
    # ------------------------------------------------------------------
    if args.append_md:
        append_path = Path(args.append_md)
        if not append_path.exists():
            print(f"ERROR: --append-md path {append_path} not found", file=sys.stderr)
            sys.exit(1)

        print(f"\n📄 Parsing append source {append_path} ...")
        append_tcs = parse_tcs(append_path)
        print(f"   Found {len(append_tcs)} TCs to append")

        append_rows_data, append_tc_ranges = explode_to_rows(append_tcs)
        # explode_to_rows returns [header, ...data]; strip the header for append
        append_data_rows = append_rows_data[1:]
        # Shift tc_row_ranges: explode_to_rows uses 0-based indices starting at row 1
        # (because row 0 is the header). Strip the +1 offset so they're 0-based within append_data_rows.
        shifted_ranges = [(s - 1, e - 1, p) for s, e, p in append_tc_ranges]

        print(f"   Exploded to {len(append_data_rows)} sheet rows")

        if args.dry_run:
            for r in append_data_rows[:5]:
                print(f"  {r[COL_IDX['Test ID']]!r:25} {r[COL_IDX['Steps']][:60]!r}")
            print("\n✅ Dry run complete — no changes made.")
            return

        print("\n🔌 Connecting to Google Sheets ...")
        service = get_sheets_service()
        sheet_id = get_sheet_id(service, args.sheet, args.tab)

        # Find last occupied row — read only column A to avoid timeout on large sheets
        result = service.spreadsheets().values().get(
            spreadsheetId=args.sheet,
            range=f"{args.tab}!A:A",
            valueRenderOption="FORMATTED_VALUE",
        ).execute()
        col_a = result.get("values", [])
        # Find last non-empty cell in column A (TC IDs + continuation rows start here)
        # Then read full last few rows to find true last data row
        first_new_sheet_row = len(col_a)
        # Trim trailing empties
        while first_new_sheet_row > 0 and (not col_a[first_new_sheet_row - 1] or not col_a[first_new_sheet_row - 1][0]):
            first_new_sheet_row -= 1
        print(f"   Appending at sheet row {first_new_sheet_row + 1} (1-based)")

        append_rows_to_sheet(
            service, args.sheet, args.tab, sheet_id,
            append_data_rows, shifted_ranges, first_new_sheet_row,
        )
        print(f"\n✅ Append done → https://docs.google.com/spreadsheets/d/{args.sheet}")
        return

    # ------------------------------------------------------------------
    # Insert-before mode — insert TCs at a specific position then renumber
    # ------------------------------------------------------------------
    if args.insert_before:
        if not args.insert_md:
            print("ERROR: --insert-before requires --insert-md", file=sys.stderr)
            sys.exit(1)
        insert_path = Path(args.insert_md)
        if not insert_path.exists():
            print(f"ERROR: --insert-md path {insert_path} not found", file=sys.stderr)
            sys.exit(1)

        print(f"\n📄 Parsing insert source {insert_path} ...")
        insert_tcs = parse_tcs(insert_path)
        print(f"   Found {len(insert_tcs)} TC(s) to insert")

        insert_rows_all, insert_tc_ranges = explode_to_rows(insert_tcs)
        insert_data_rows = insert_rows_all[1:]  # strip header
        shifted_ranges = [(s - 1, e - 1, p) for s, e, p in insert_tc_ranges]

        if args.dry_run:
            for r in insert_data_rows:
                print(f"  {r[COL_IDX['Test ID']]!r:25} {r[COL_IDX['Steps']][:60]!r}")
            print("\n✅ Dry run complete — no changes made.")
            return

        print("\n🔌 Connecting to Google Sheets ...")
        service = get_sheets_service()
        sheet_id = get_sheet_id(service, args.sheet, args.tab)

        insert_before_tc(
            service, args.sheet, args.tab, sheet_id,
            args.insert_before,
            insert_data_rows, shifted_ranges,
        )
        print(f"\n✅ Insert done → https://docs.google.com/spreadsheets/d/{args.sheet}")
        return

    # ------------------------------------------------------------------
    # Remove + renumber mode
    # ------------------------------------------------------------------
    if args.remove_ids:
        remove_id_set = {rid.strip() for rid in args.remove_ids.split(",") if rid.strip()}
        print(f"\n🗑️  Remove mode — deleting {len(remove_id_set)} TC(s): {', '.join(sorted(remove_id_set))}")
        print("\n🔌 Connecting to Google Sheets ...")
        service = get_sheets_service()
        sheet_id = get_sheet_id(service, args.sheet, args.tab)
        remove_and_renumber(service, args.sheet, args.tab, sheet_id, remove_id_set)
        print(f"\n✅ Remove + renumber done → https://docs.google.com/spreadsheets/d/{args.sheet}")
        return

    # ------------------------------------------------------------------
    # Patch mode — overwrite only the rows for the listed TC IDs
    # ------------------------------------------------------------------
    if args.patch_ids:
        patch_id_set = {pid.strip() for pid in args.patch_ids.split(",") if pid.strip()}
        print(f"\n🩹 Patch mode — targeting {len(patch_id_set)} TC(s): {', '.join(sorted(patch_id_set))}")
        patch_rows_in_place(service, args.sheet, args.tab, sheet_id, tcs, rows, tc_row_ranges, patch_id_set)
        print(f"\n✅ Patch done → https://docs.google.com/spreadsheets/d/{args.sheet}")
        return

    # ------------------------------------------------------------------
    # Full write mode (default)
    # ------------------------------------------------------------------
    print("\n✏️  Writing data ...")
    write_data(service, args.sheet, args.tab, rows)

    print("\n🎨 Applying formatting ...")
    apply_formatting(
        service, args.sheet, args.tab, sheet_id,
        num_data_rows=num_data_rows,
        num_cols=len(COLUMNS),
        tc_row_ranges=tc_row_ranges,
        rows=rows,
    )

    print(f"\n✅ Done → https://docs.google.com/spreadsheets/d/{args.sheet}")


if __name__ == "__main__":
    main()

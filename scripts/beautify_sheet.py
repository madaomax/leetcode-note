"""Apply visual formatting to the 刷题日程 tab (driven by cell content)."""
import google.auth.transport.requests
from google.oauth2 import service_account
import requests

KEY_PATH = "sheets-sa.json"
SPREADSHEET_ID = "1nOuzdTY-t5M-iyS2VuLvV5BxeA_YDAXq2sCJlfTcpJY"
TAB = "刷题日程"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
BASE = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}"

creds = service_account.Credentials.from_service_account_file(KEY_PATH, scopes=SCOPES)
creds.refresh(google.auth.transport.requests.Request())
H = {"Authorization": f"Bearer {creds.token}"}


def rgb(hexstr):
    h = hexstr.lstrip("#")
    return {"red": int(h[0:2], 16) / 255, "green": int(h[2:4], 16) / 255, "blue": int(h[4:6], 16) / 255}


WHITE = rgb("#FFFFFF")
NCOLS = 11  # A..K

# palette
TITLE_BG = rgb("#1A237E")
HEAD_BG = rgb("#303F9F")
SECTION_BG = rgb("#546E7A")
BORDER = rgb("#CFD8DC")

DIFF = {  # (bg, text) — muted pastels
    "E": (rgb("#E8F5E9"), rgb("#2E7D32")),
    "M": (rgb("#FFF3E0"), rgb("#EF6C00")),
    "H": (rgb("#FFEBEE"), rgb("#C62828")),
}
TIER = [  # (substr, bg) — muted pastels
    ("Core", rgb("#E3F2FD")),
    ("Stretch", rgb("#F5F5F5")),
    ("Mock", rgb("#EDE7F6")),
    ("复习", rgb("#E0F7FA")),
    ("Review", rgb("#E0F7FA")),
    ("行为", rgb("#FCE4EC")),
    ("Behav", rgb("#FCE4EC")),
    ("面试", rgb("#FFF8E1")),
    ("Interview", rgb("#FFF8E1")),
]

# --- read current values + sheet meta ---
meta = requests.get(BASE, headers=H, params={"fields": "sheets.properties"}).json()
sid = next(s["properties"]["sheetId"] for s in meta["sheets"] if s["properties"]["title"] == TAB)
vals = requests.get(f"{BASE}/values/{TAB}", headers=H).json().get("values", [])
nrows = len(vals)


def gr(r0, r1, c0=0, c1=NCOLS):
    return {"sheetId": sid, "startRowIndex": r0, "endRowIndex": r1,
            "startColumnIndex": c0, "endColumnIndex": c1}


def repeat(r0, r1, fmt, fields, c0=0, c1=NCOLS):
    return {"repeatCell": {"range": gr(r0, r1, c0, c1),
                           "cell": {"userEnteredFormat": fmt}, "fields": fields}}


reqs = []

# freeze title + header rows, set tab color
reqs.append({"updateSheetProperties": {
    "properties": {"sheetId": sid, "gridProperties": {"frozenRowCount": 2},
                   "tabColor": HEAD_BG},
    "fields": "gridProperties.frozenRowCount,tabColor"}})

# base body format: middle-align, wrap, font 10
reqs.append(repeat(2, nrows, {
    "verticalAlignment": "MIDDLE", "wrapStrategy": "WRAP",
    "textFormat": {"fontSize": 10}},
    "userEnteredFormat(verticalAlignment,wrapStrategy,textFormat.fontSize)"))

# per-column horizontal alignment (centered cols: date,星期,难度,来源,Tier,完成,用时)
for col in (0, 1, 4, 5, 6, 7, 8):
    reqs.append(repeat(2, nrows, {"horizontalAlignment": "CENTER"},
                       "userEnteredFormat.horizontalAlignment", col, col + 1))
for col in (2, 3, 9, 10):
    reqs.append(repeat(2, nrows, {"horizontalAlignment": "LEFT"},
                       "userEnteredFormat.horizontalAlignment", col, col + 1))

# title row (0): merge + style
reqs.append({"mergeCells": {"range": gr(0, 1), "mergeType": "MERGE_ALL"}})
reqs.append(repeat(0, 1, {
    "backgroundColor": TITLE_BG, "horizontalAlignment": "LEFT", "verticalAlignment": "MIDDLE",
    "wrapStrategy": "WRAP",
    "textFormat": {"foregroundColor": WHITE, "bold": True, "fontSize": 13}},
    "userEnteredFormat(backgroundColor,horizontalAlignment,verticalAlignment,wrapStrategy,textFormat)"))

# header row (1): column titles
reqs.append(repeat(1, 2, {
    "backgroundColor": HEAD_BG, "horizontalAlignment": "CENTER", "verticalAlignment": "MIDDLE",
    "wrapStrategy": "WRAP",
    "textFormat": {"foregroundColor": WHITE, "bold": True, "fontSize": 10}},
    "userEnteredFormat(backgroundColor,horizontalAlignment,verticalAlignment,wrapStrategy,textFormat)"))

# per-row content-driven styling
for i in range(2, nrows):
    row = vals[i]
    if not row or all(c.strip() == "" for c in row):
        continue
    is_section = row[0].strip() != "" and all(c.strip() == "" for c in row[1:])
    if is_section:
        reqs.append({"mergeCells": {"range": gr(i, i + 1), "mergeType": "MERGE_ALL"}})
        reqs.append(repeat(i, i + 1, {
            "backgroundColor": SECTION_BG, "horizontalAlignment": "LEFT", "verticalAlignment": "MIDDLE",
            "wrapStrategy": "WRAP",
            "textFormat": {"foregroundColor": WHITE, "bold": True, "fontSize": 10}},
            "userEnteredFormat(backgroundColor,horizontalAlignment,verticalAlignment,wrapStrategy,textFormat)"))
        continue
    # difficulty (col E = idx 4)
    if len(row) > 4:
        d = row[4].strip()[:1].upper()
        if d in DIFF:
            bg, tx = DIFF[d]
            reqs.append(repeat(i, i + 1, {
                "backgroundColor": bg, "textFormat": {"foregroundColor": tx, "bold": True}},
                "userEnteredFormat(backgroundColor,textFormat.foregroundColor,textFormat.bold)", 4, 5))
    # tier (col G = idx 6)
    if len(row) > 6:
        t = row[6]
        for sub, bg in TIER:
            if sub in t:
                reqs.append(repeat(i, i + 1, {
                    "backgroundColor": bg, "textFormat": {"bold": False}},
                    "userEnteredFormat(backgroundColor,textFormat.bold)", 6, 7))
                break
    # done check (col H = idx 7): bold green if marked
    if len(row) > 7 and row[7].strip() not in ("", "—"):
        reqs.append(repeat(i, i + 1, {
            "textFormat": {"foregroundColor": rgb("#2E7D32"), "bold": True}},
            "userEnteredFormat.textFormat", 7, 8))

# borders over whole table
reqs.append({"updateBorders": {"range": gr(0, nrows),
    "innerHorizontal": {"style": "SOLID", "color": BORDER},
    "innerVertical": {"style": "SOLID", "color": BORDER},
    "top": {"style": "SOLID", "color": BORDER}, "bottom": {"style": "SOLID", "color": BORDER},
    "left": {"style": "SOLID", "color": BORDER}, "right": {"style": "SOLID", "color": BORDER}}})

# column widths
widths = {0: 50, 1: 48, 2: 165, 3: 300, 4: 52, 5: 72, 6: 92, 7: 60, 8: 78, 9: 210, 10: 220}
for col, w in widths.items():
    reqs.append({"updateDimensionProperties": {
        "range": {"sheetId": sid, "dimension": "COLUMNS", "startIndex": col, "endIndex": col + 1},
        "properties": {"pixelSize": w}, "fields": "pixelSize"}})

r = requests.post(f"{BASE}:batchUpdate", headers=H, json={"requests": reqs})
if not r.ok:
    print("ERROR", r.status_code, r.text[:1000])
    r.raise_for_status()
print(f"applied {len(reqs)} formatting requests over {nrows} rows")

"""Alternating background tint per date group on the 刷题日程 tab.
Applies to all columns except 难度(4) and Tier(6) so the chips keep their color.
Skips section-divider rows and empty rows. Safe to re-run."""
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


SHADES = [rgb("#FFFFFF"), rgb("#E9EFF5")]  # alternating per date group
COL_RUNS = [(0, 4), (5, 6), (7, 11)]  # skip col 4 (难度) and 6 (Tier)

meta = requests.get(BASE, headers=H, params={"fields": "sheets.properties"}).json()
sid = next(s["properties"]["sheetId"] for s in meta["sheets"] if s["properties"]["title"] == TAB)
vals = requests.get(f"{BASE}/values/{TAB}", headers=H).json().get("values", [])
nrows = len(vals)

# assign a shade to each eligible data row (toggle when the date in col A changes)
shade_of = {}
prev_date, idx = None, 0
for i in range(2, nrows):
    row = vals[i]
    if not row or all(c.strip() == "" for c in row):
        continue
    is_section = row[0].strip() != "" and all(c.strip() == "" for c in row[1:])
    if is_section:
        continue
    date = row[0].strip()
    if date and date != prev_date:
        idx ^= 1
        prev_date = date
    shade_of[i] = idx

# group consecutive eligible rows with the same shade into ranges
reqs = []
runs = []
start = None
for i in range(2, nrows):
    cur = shade_of.get(i)
    if cur is None:
        if start is not None:
            runs.append((start, i, shade_of[start]))
            start = None
        continue
    if start is None:
        start = i
    elif shade_of[i] != shade_of[start]:
        runs.append((start, i, shade_of[start]))
        start = i
if start is not None:
    runs.append((start, nrows, shade_of[start]))

for r0, r1, sh in runs:
    for c0, c1 in COL_RUNS:
        reqs.append({"repeatCell": {
            "range": {"sheetId": sid, "startRowIndex": r0, "endRowIndex": r1,
                      "startColumnIndex": c0, "endColumnIndex": c1},
            "cell": {"userEnteredFormat": {"backgroundColor": SHADES[sh]}},
            "fields": "userEnteredFormat.backgroundColor"}})

resp = requests.post(f"{BASE}:batchUpdate", headers=H, json={"requests": reqs})
if not resp.ok:
    print("ERROR", resp.status_code, resp.text[:1000])
    resp.raise_for_status()
print(f"banded {len(runs)} date groups with {len(reqs)} requests")

"""Recolor only the 难度(4) and Tier(6) columns with muted pastels.
Mirrors the palette in beautify_sheet.py. Leaves banding/borders/headers intact."""
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


DIFF = {
    "E": (rgb("#E8F5E9"), rgb("#2E7D32")),
    "M": (rgb("#FFF3E0"), rgb("#EF6C00")),
    "H": (rgb("#FFEBEE"), rgb("#C62828")),
}
TIER = [
    ("Core", rgb("#E3F2FD")), ("Stretch", rgb("#F5F5F5")), ("Mock", rgb("#EDE7F6")),
    ("复习", rgb("#E0F7FA")), ("Review", rgb("#E0F7FA")), ("行为", rgb("#FCE4EC")),
    ("Behav", rgb("#FCE4EC")), ("面试", rgb("#FFF8E1")), ("Interview", rgb("#FFF8E1")),
]

meta = requests.get(BASE, headers=H, params={"fields": "sheets.properties"}).json()
sid = next(s["properties"]["sheetId"] for s in meta["sheets"] if s["properties"]["title"] == TAB)
vals = requests.get(f"{BASE}/values/{TAB}", headers=H).json().get("values", [])

reqs = []
for i in range(2, len(vals)):
    row = vals[i]
    if not row or all(c.strip() == "" for c in row):
        continue
    if row[0].strip() != "" and all(c.strip() == "" for c in row[1:]):
        continue  # section divider
    if len(row) > 4:
        d = row[4].strip()[:1].upper()
        if d in DIFF:
            bg, tx = DIFF[d]
            reqs.append({"repeatCell": {
                "range": {"sheetId": sid, "startRowIndex": i, "endRowIndex": i + 1,
                          "startColumnIndex": 4, "endColumnIndex": 5},
                "cell": {"userEnteredFormat": {"backgroundColor": bg,
                         "textFormat": {"foregroundColor": tx, "bold": True}}},
                "fields": "userEnteredFormat(backgroundColor,textFormat.foregroundColor,textFormat.bold)"}})
    if len(row) > 6:
        for sub, bg in TIER:
            if sub in row[6]:
                reqs.append({"repeatCell": {
                    "range": {"sheetId": sid, "startRowIndex": i, "endRowIndex": i + 1,
                              "startColumnIndex": 6, "endColumnIndex": 7},
                    "cell": {"userEnteredFormat": {"backgroundColor": bg, "textFormat": {"bold": False}}},
                    "fields": "userEnteredFormat(backgroundColor,textFormat.bold)"}})
                break

resp = requests.post(f"{BASE}:batchUpdate", headers=H, json={"requests": reqs})
if not resp.ok:
    print("ERROR", resp.status_code, resp.text[:1000])
    resp.raise_for_status()
print(f"recolored chips with {len(reqs)} requests")

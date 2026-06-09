"""Make the README Dashboard live: formulas counting Core/done from 刷题日程."""
import google.auth.transport.requests
from google.oauth2 import service_account
import requests

KEY_PATH = "sheets-sa.json"
SPREADSHEET_ID = "1nOuzdTY-t5M-iyS2VuLvV5BxeA_YDAXq2sCJlfTcpJY"
README = "说明 README"
README_SID = 144527833
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
BASE = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}"

creds = service_account.Credentials.from_service_account_file(KEY_PATH, scopes=SCOPES)
creds.refresh(google.auth.transport.requests.Request())
H = {"Authorization": f"Bearer {creds.token}"}

S = "'刷题日程'"  # data: row 3+, Tier=G, 完成✓=H
data = [
    {"range": f"{README}!B4", "values": [[f'=COUNTIF({S}!G3:G1000,"*Core*")']]},
    {"range": f"{README}!B5", "values": [[f'=COUNTIFS({S}!G3:G1000,"*Core*",{S}!H3:H1000,"<>")']]},
    {"range": f"{README}!B6", "values": [["=IFERROR(B5/B4,0)"]]},
    {"range": f"{README}!B7", "values": [[f'=COUNTA({S}!H3:H1000)']]},
]
r = requests.post(f"{BASE}/values:batchUpdate", headers=H,
                  json={"valueInputOption": "USER_ENTERED", "data": data})
r.raise_for_status()
print("formulas written:", r.json().get("totalUpdatedCells"))

# B6 as percent
fmt = {"repeatCell": {
    "range": {"sheetId": README_SID, "startRowIndex": 5, "endRowIndex": 6,
              "startColumnIndex": 1, "endColumnIndex": 2},
    "cell": {"userEnteredFormat": {"numberFormat": {"type": "PERCENT", "pattern": "0%"}}},
    "fields": "userEnteredFormat.numberFormat"}}
requests.post(f"{BASE}:batchUpdate", headers=H, json={"requests": [fmt]}).raise_for_status()

# read back computed values
got = requests.get(f"{BASE}/values/{README}!A4:B7", headers=H,
                   params={"valueRenderOption": "FORMATTED_VALUE"}).json().get("values", [])
for row in got:
    print(" | ".join(row))

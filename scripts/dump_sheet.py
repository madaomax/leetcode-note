"""Dump all tabs + values from a Google Sheet via service account."""
import sys, json
import google.auth.transport.requests
from google.oauth2 import service_account
import requests

KEY_PATH = "sheets-sa.json"
SPREADSHEET_ID = sys.argv[1] if len(sys.argv) > 1 else "1nOuzdTY-t5M-iyS2VuLvV5BxeA_YDAXq2sCJlfTcpJY"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
BASE = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}"

creds = service_account.Credentials.from_service_account_file(KEY_PATH, scopes=SCOPES)
creds.refresh(google.auth.transport.requests.Request())
tok = creds.token
H = {"Authorization": f"Bearer {tok}"}

out = open("scripts/sheet_dump.txt", "w", encoding="utf-8")
meta = requests.get(BASE, headers=H, params={"fields": "sheets.properties"}).json()
for s in meta.get("sheets", []):
    p = s["properties"]
    title = p["title"]
    out.write(f"\n===== TAB: {title} (gid={p['sheetId']}) =====\n")
    r = requests.get(f"{BASE}/values/{title}", headers=H).json()
    for row in r.get("values", []):
        out.write(" | ".join(row) + "\n")
out.close()
print("done")

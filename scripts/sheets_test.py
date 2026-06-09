"""Test write access to a Google Sheet via the REST API using a service account.

Usage:
    python scripts/sheets_test.py            # uses defaults below
    python scripts/sheets_test.py <key.json> <spreadsheetId> <testCell>

Does a non-destructive round-trip:
    1. mint an access token from the service account JSON
    2. read the test cell's current value (saved)
    3. write a timestamp marker
    4. read it back and confirm
    5. restore the original value (clears if it was empty)
"""
import sys
import datetime
import google.auth.transport.requests
from google.oauth2 import service_account
import requests

KEY_PATH = sys.argv[1] if len(sys.argv) > 1 else "sheets-sa.json"
SPREADSHEET_ID = sys.argv[2] if len(sys.argv) > 2 else "1ju185_P23yDjHaxKsrNwyEepOPtErpg4FNnmBSBej1g"
TEST_CELL = sys.argv[3] if len(sys.argv) > 3 else "Z999"  # far from your data

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
BASE = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}"


def token():
    creds = service_account.Credentials.from_service_account_file(KEY_PATH, scopes=SCOPES)
    creds.refresh(google.auth.transport.requests.Request())
    print(f"  service account: {creds.service_account_email}")
    return creds.token


def get_cell(tok, cell):
    r = requests.get(f"{BASE}/values/{cell}", headers={"Authorization": f"Bearer {tok}"})
    r.raise_for_status()
    vals = r.json().get("values", [[""]])
    return vals[0][0] if vals and vals[0] else ""


def put_cell(tok, cell, value):
    r = requests.put(
        f"{BASE}/values/{cell}",
        headers={"Authorization": f"Bearer {tok}"},
        params={"valueInputOption": "RAW"},
        json={"values": [[value]]},
    )
    r.raise_for_status()
    return r.json()


def main():
    print("1. minting token...")
    tok = token()

    print(f"2. reading current value of {TEST_CELL}...")
    original = get_cell(tok, TEST_CELL)
    print(f"   original = {original!r}")

    marker = f"claude-test {datetime.datetime.now().isoformat(timespec='seconds')}"
    print(f"3. writing marker {marker!r}...")
    put_cell(tok, TEST_CELL, marker)

    print("4. reading back...")
    readback = get_cell(tok, TEST_CELL)
    assert readback == marker, f"mismatch: {readback!r} != {marker!r}"
    print(f"   confirmed: {readback!r}")

    print(f"5. restoring original ({original!r})...")
    put_cell(tok, TEST_CELL, original)

    print("\nSUCCESS - write access works end-to-end.")


if __name__ == "__main__":
    main()

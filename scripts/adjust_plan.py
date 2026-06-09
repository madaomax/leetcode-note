"""Re-tier the 6/5-6/6 rows to '4 core + 1 爆种 stretch' per day, update notes/header."""
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

vals = requests.get(f"{BASE}/values/{TAB}", headers=H).json().get("values", [])


def find(date, problem_sub):
    for idx, row in enumerate(vals):
        if len(row) > 3 and row[0].strip() == date and problem_sub in row[3]:
            return idx + 1  # 1-based A1 row
    raise SystemExit(f"row not found: {date} / {problem_sub}")


def find_contains(text_sub):
    for idx, row in enumerate(vals):
        if row and text_sub in row[0]:
            return idx + 1
    raise SystemExit(f"row not found: {text_sub}")


data = []

# section header -> spell out the 4题/爆种 rule
hdr = find_contains("延期补充")
data.append({"range": f"{TAB}!A{hdr}",
             "values": [["延期补充 6/5–6/7（面试改 6/8 周一）· 每天 best case 4 道新题，爆种 5 道 · 真题仅 3 道确认，其余＝补全未触及套路"]]})

# 6/5 Non-overlapping Intervals -> 爆种 stretch
r = find("6/5", "Non-overlapping Intervals")
data.append({"range": f"{TAB}!G{r}", "values": [["加练 Stretch"]]})
data.append({"range": f"{TAB}!J{r}", "values": [["贪心，按结束排序 · 爆种第5题"]]})

# 6/6 Letter Combinations -> 爆种 stretch
r = find("6/6", "Letter Combinations")
data.append({"range": f"{TAB}!G{r}", "values": [["加练 Stretch"]]})
data.append({"range": f"{TAB}!J{r}", "values": [["回溯，未触及套路 · 爆种第5题"]]})

# 6/6 Mock #1 -> note that its 2 problems count toward today's 4
r = find("6/6", "模拟面试")
data.append({"range": f"{TAB}!J{r}", "values": [["像真面试一样讲 · 这2道新题算进今天的4道"]]})

resp = requests.post(f"{BASE}/values:batchUpdate", headers=H,
                     json={"valueInputOption": "RAW", "data": data})
if not resp.ok:
    print("ERROR", resp.status_code, resp.text[:1000])
    resp.raise_for_status()
print("updated cells:", resp.json().get("totalUpdatedCells"))

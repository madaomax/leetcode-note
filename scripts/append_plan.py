"""Append the 6/5-6/7 final-stretch rows to the 刷题日程 tab."""
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

# cols: 日期 | 星期 | 主题 Pattern | 题目 | 难度 | 来源 | Tier | 完成✓ | 用时 | 备注 | more notes
rows = [
    ["", "", "", "", "", "", "", "", "", "", ""],
    ["延期补充 6/5–6/7 · 面试改到 6/8 周一 · 只有真题3道是确认的，其余按「补全未触及套路」排", "", "", "", "", "", "", "", "", "", ""],
    ["6/5", "周五", "Design", "Encode and Decode Strings", "M", "Premium", "必做 Core", "", "", "长度前缀编码，design 高频", "未触及套路"],
    ["6/5", "周五", "Intervals", "Meeting Rooms II", "M", "Premium", "必做 Core", "", "", "扫描线 / 最小堆，超高频", ""],
    ["6/5", "周五", "Intervals", "Non-overlapping Intervals", "M", "LC75", "必做 Core", "", "", "贪心，按结束排序", ""],
    ["6/5", "周五", "Topological Sort", "Course Schedule", "M", "LC75", "必做 Core", "", "", "拓扑排序入门", "拓扑你还没做过"],
    ["6/5", "周五", "Design", "LRU Cache", "M", "LC75", "必做 Core", "", "", "单轮设计经典", ""],
    ["6/6", "周六", "Topological Sort", "Alien Dictionary", "H", "Premium", "必做 Core", "", "", "拓扑，接 Course Schedule", ""],
    ["6/6", "周六", "Union Find", "Number of Islands II", "H", "Premium", "必做 Core", "", "", "动态并查集，未触及套路", "太重就换 LC323"],
    ["6/6", "周六", "Backtracking", "Letter Combinations of a Phone Number", "M", "LC75", "必做 Core", "", "", "回溯，未触及套路", ""],
    ["6/6", "周六", "Timed Mock #1", "模拟面试：2道全新 medium，各限时 35min，出声讲（1 graph + 1 array/string）", "—", "—", "Mock", "", "", "像真面试一样讲", ""],
    ["6/7", "周日", "Taper · 真题默写", "冷写3道确认真题（计时）：Spiral Matrix / Island Perimeter / strstr", "—", "—", "复习 Review", "", "", "你的底线，必须自动化", ""],
    ["6/7", "周日", "Monotonic Stack", "模板复习 + LC84 Largest Rectangle 或 LC42 Trapping Rain Water（任一）", "M/H", "LC75", "加练 Stretch", "", "", "唯一还虚的套路，累就跳过", ""],
    ["6/7", "周日", "Timed Mock #2", "模拟面试：1道全新 medium，出声讲", "—", "—", "Mock", "", "", "", ""],
    ["6/7", "周日", "行为面 Behavioral", "出声练：自我介绍 / infra项目（分布式缓存·图数据库）/ why DepthFirst（AI security × infra）", "—", "—", "行为 Behav", "", "", "边写边讲复杂度 + edge case", ""],
    ["6/7", "周日", "收尾 Wind-down", "过一遍 pattern 模板，调试设备，早睡", "—", "—", "复习 Review", "", "", "保持状态", ""],
    ["6/8", "周一", "面试日 Interview Day", "早上1道 easy 热身（Reverse Linked List / Move Zeroes），过模板，不碰新难题", "E", "—", "面试 Interview", "", "", "保持状态，提前调好设备", ""],
]

r = requests.post(
    f"{BASE}/values/{TAB}:append",
    headers=H,
    params={"valueInputOption": "RAW", "insertDataOption": "INSERT_ROWS"},
    json={"values": rows},
)
r.raise_for_status()
res = r.json()
print("appended range:", res.get("updates", {}).get("updatedRange"))
print("rows added:", res.get("updates", {}).get("updatedRows"))

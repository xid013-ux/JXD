from datetime import date, timedelta
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

cases = [
    ("300715.SZ", "凯伦股份", "2025-01-07"), ("605289.SH", "罗曼股份", "2025-08-05"),
    ("300960.SZ", "通业科技", "2025-08-18"), ("300948.SZ", "冠中生态", "2025-09-28"),
    ("603758.SH", "秦安股份", "2025-11-12"), ("603353.SH", "和顺石油", "2025-11-17"),
    ("003018.SZ", "金富科技", "2026-02-05"), ("002980.SZ", "华盛昌", "2026-02-27"),
    ("603221.SH", "爱丽家居", "2026-07-21"), ("001696.SZ", "宗申动力", "2023-05-25"),
    ("300420.SZ", "五洋自控", "2026-06-04"), ("688228.SH", "开普云", "2025-08-25"),
]
wb = Workbook()
ws = wb.active; ws.title = "说明"
ws.append(["证券代码", "公司", "首次公告日（初步）", "取数起始日", "取数结束日", "工作表"])
for c, n, d in cases:
    t = date.fromisoformat(d)
    ws.append([c, n, d, (t - timedelta(days=30)).isoformat(), (t + timedelta(days=45)).isoformat(), n])
ws.append([])
ws.append(["用法：用装了Wind Excel插件的电脑打开本文件，点插件的“刷新”（或Ctrl+Alt+F9），每个工作表A1的WSD公式会拉出前复权日收盘价；确认有数后保存发回即可，涨跌幅由我计算。"])
ws.append(["如某只股票在区间内停牌，停牌日不会出现在序列里，不影响计算。"])
for col, w in zip("ABCDEF", [12, 10, 16, 12, 12, 10]):
    ws.column_dimensions[col].width = w
for c, n, d in cases:
    t = date.fromisoformat(d)
    s = wb.create_sheet(n)
    s["A1"] = f'=WSD("{c}","close,pct_chg,trade_status","{(t - timedelta(days=30)).isoformat()}","{(t + timedelta(days=45)).isoformat()}","PriceAdj=F")'
    s["F1"] = f"{n} {c} 首次公告日 {d}"
    s["F1"].font = Font(bold=True)
wb.save("Wind取数模板.xlsx")

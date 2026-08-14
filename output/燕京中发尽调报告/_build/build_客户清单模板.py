# -*- coding: utf-8 -*-
"""2-4-2 / 1-8-5 客户清单填报模板"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

F   = 'Arial'
TIT = Font(name=F, size=14, bold=True)
H1  = Font(name=F, size=10, bold=True, color='FFFFFF')
BOLD= Font(name=F, size=10, bold=True)
N   = Font(name=F, size=10)
NOTE= Font(name=F, size=9, italic=True, color='7F7F7F')
EX  = Font(name=F, size=10, italic=True, color='808080')
BLUE= Font(name=F, size=10, color='0000FF')

FILL_H  = PatternFill('solid', fgColor='1F4E79')
FILL_IN = PatternFill('solid', fgColor='FFFF00')   # 需公司填写
FILL_CAL= PatternFill('solid', fgColor='F2F2F2')   # 公式，勿改
FILL_SEC= PatternFill('solid', fgColor='DDEBF7')

thin = Side(style='thin', color='BFBFBF')
BOX  = Border(left=thin, right=thin, top=thin, bottom=thin)
WRAP = Alignment(horizontal='left', vertical='center', wrap_text=True)
CTR  = Alignment(horizontal='center', vertical='center', wrap_text=True)

# 期间与对应营业收入（元），来源见说明页
PERIODS = ['2024年度', '2025年度', '2026年1-6月']
REV_ZF  = {'2024年度': 212656418.65, '2025年度': 434358616.85, '2026年1-6月': 208146233.34}
REV_XT  = {'2024年度': 5163572.58,   '2025年度': 100430167.78, '2026年1-6月': 29375817.27}

COLS = [
    ('期间', 12, 'text'), ('序号', 6, 'text'), ('客户名称（全称）', 34, 'text'),
    ('统一社会信用代码', 22, 'text'), ('客户类型', 13, 'list_type'), ('销售模式', 14, 'list_mode'),
    ('经销区域', 14, 'text'), ('主要销售产品', 20, 'text'), ('合作起始时间', 13, 'date'),
    ('本期销售金额\n（不含税，元）', 17, 'money'), ('占当期营业收入\n比例（%）', 14, 'calc_pct'),
    ('本期回款金额\n（含税，元）', 17, 'money'), ('期末应收账款\n余额（元）', 16, 'money'),
    ('期末合同负债\n（预收）余额（元）', 18, 'money'),
    ('是否存在\n第三方回款', 12, 'list_yn'), ('第三方回款方名称及金额', 26, 'text'),
    ('是否关联方或存在\n关联关系', 14, 'list_yn'),
    ('关联关系说明\n（是否为股东、董监高、员工及其近亲属持股或任职）', 34, 'text'),
    ('备注', 18, 'text'),
]
ROWS_PER_PERIOD = 20

def band(ws, r0, ncol, fill):
    for c in range(1, ncol+1):
        ws.cell(r0, c).fill = fill

def sheet_list(wb, title, entity, revmap, example):
    ws = wb.create_sheet(title)
    ws['A1'] = f'{entity} 主要客户清单'
    ws['A1'].font = TIT
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(COLS))
    ws.row_dimensions[1].height = 24
    ws['A2'] = ('填报要求：各期至少填列前20名客户，且前列客户销售金额合计占当期营业收入比例不低于50%；'
                '如前20名合计未达50%，请继续向下补充至达标。黄色底纹单元格由公司填写，灰色底纹为公式，请勿修改。')
    ws['A2'].font = NOTE
    ws['A2'].alignment = WRAP
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=len(COLS))
    ws.row_dimensions[2].height = 30

    # 营业收入假设区（唯一数据源，供占比公式引用）
    ws['A3'] = '当期营业收入（元）'
    ws['A3'].font = BOLD; ws['A3'].fill = FILL_SEC; ws['A3'].border = BOX; ws['A3'].alignment = CTR
    REVCELL = {}
    col = 2
    for p_ in PERIODS:
        lc = ws.cell(3, col, p_); lc.font = BOLD; lc.alignment = CTR; lc.border = BOX; lc.fill = FILL_SEC
        vc = ws.cell(3, col+1, revmap[p_]); vc.font = BLUE; vc.number_format = '#,##0.00'
        vc.border = BOX; vc.alignment = CTR; vc.fill = FILL_IN
        REVCELL[p_] = f'${get_column_letter(col+1)}$3'
        col += 2
    ws.cell(3, col, '← 蓝色数字取自财务报表，如与账面不符请直接修改，占比公式将自动更新').font = NOTE
    ws.row_dimensions[3].height = 18

    hr = 5
    for i, (name, w, _) in enumerate(COLS, start=1):
        c = ws.cell(hr, i, name)
        c.font, c.fill, c.alignment, c.border = H1, FILL_H, CTR, BOX
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[hr].height = 42
    ws.freeze_panes = ws.cell(hr+1, 3)

    # 示例行
    er = hr + 1
    for i, v in enumerate(example, start=1):
        c = ws.cell(er, i, v)
        c.font, c.border, c.alignment = EX, BOX, (CTR if i in (1,2,5,6,9,11,15,17) else WRAP)
    ws.cell(er, 10).number_format = '#,##0.00'
    ws.cell(er, 12).number_format = '#,##0.00'
    ws.cell(er, 13).number_format = '#,##0.00'
    ws.cell(er, 14).number_format = '#,##0.00'
    ws.cell(er, 11).number_format = '0.00'
    band(ws, er, len(COLS), PatternFill('solid', fgColor='FFF2CC'))
    ws.cell(er, 19).value = '↑ 示例行，填报时请删除'

    r = er + 1
    blocks = []
    for p in PERIODS:
        # 期间分隔条
        ws.cell(r, 1, p).font = BOLD
        ws.cell(r, 1).alignment = CTR
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=len(COLS))
        band(ws, r, len(COLS), FILL_SEC)
        for c in range(1, len(COLS)+1): ws.cell(r, c).border = BOX
        r += 1
        first = r
        for k in range(1, ROWS_PER_PERIOD+1):
            ws.cell(r, 1, p).font = N; ws.cell(r, 1).alignment = CTR; ws.cell(r,1).border = BOX
            ws.cell(r, 2, k).font = N;  ws.cell(r, 2).alignment = CTR; ws.cell(r,2).border = BOX
            for c in range(3, len(COLS)+1):
                cell = ws.cell(r, c)
                cell.border, cell.font = BOX, N
                cell.alignment = CTR if c in (5,6,9,15,17) else WRAP
                if c == 11:
                    cell.value = f'=IF(J{r}="","",J{r}/{REVCELL[p]})'
                    cell.number_format = '0.00%'
                    cell.fill = FILL_CAL
                else:
                    cell.fill = FILL_IN
                    if c in (10,12,13,14): cell.number_format = '#,##0.00'
            r += 1
        last = r - 1
        # 小计
        ws.cell(r, 3, '前20名合计').font = BOLD
        ws.cell(r, 3).alignment = CTR
        ws.cell(r, 1, p).font = BOLD; ws.cell(r,1).alignment = CTR
        for c in (10, 12, 13, 14):
            L = get_column_letter(c)
            cc = ws.cell(r, c, f'=SUM({L}{first}:{L}{last})')
            cc.number_format = '#,##0.00'; cc.font = BOLD; cc.fill = FILL_CAL
        cc = ws.cell(r, 11, f'=IF(J{r}="","",J{r}/{REVCELL[p]})')
        cc.number_format = '0.00%'; cc.font = BOLD; cc.fill = FILL_CAL
        ws.cell(r, 15, '是否达到50%').font = BOLD
        cc = ws.cell(r, 16, f'=IF(J{r}=0,"未填",IF(K{r}>=0.5,"达标","未达标，请补充客户"))')
        cc.font = BOLD; cc.fill = FILL_CAL
        for c in range(1, len(COLS)+1):
            ws.cell(r, c).border = BOX
            if not ws.cell(r, c).fill.fgColor.rgb == '00F2F2F2':
                ws.cell(r, c).fill = PatternFill('solid', fgColor='E2EFDA')
        for c in (10,11,12,13,14,16): ws.cell(r, c).fill = FILL_CAL
        blocks.append((p, first, last, r))
        r += 2

    # 勾稽核对
    ws.cell(r, 1, '勾稽核对').font = BOLD
    band(ws, r, 6, FILL_SEC); r += 1
    hdr = ['期间', '当期营业收入（元）', '前20名合计（元）', '合计占比', '差额（元）', '说明']
    for i, h in enumerate(hdr, start=1):
        c = ws.cell(r, i, h); c.font, c.fill, c.alignment, c.border = H1, FILL_H, CTR, BOX
    r += 1
    for p, first, last, sub in blocks:
        ws.cell(r, 1, p).font = N; ws.cell(r,1).alignment = CTR
        c = ws.cell(r, 2, f'={REVCELL[p]}'); c.number_format = '#,##0.00'; c.font = Font(name=F, size=10, color='008000')
        c = ws.cell(r, 3, f'=J{sub}'); c.number_format = '#,##0.00'; c.font = N
        c = ws.cell(r, 4, f'=IF(C{r}=0,"",C{r}/B{r})'); c.number_format = '0.00%'; c.font = N
        c = ws.cell(r, 5, f'=IF(C{r}=0,"",B{r}-C{r})'); c.number_format = '#,##0.00'; c.font = N
        ws.cell(r, 6, '前20名以外客户的合计销售金额').font = NOTE
        for i in range(1, 7):
            ws.cell(r, i).border = BOX
            ws.cell(r, i).alignment = CTR if i in (1, 4) else WRAP
        r += 1
    ws.cell(r, 1, '注：B列营业收入引用第3行的假设单元格，如需修改请改第3行；绿色字体表示引用本表其他单元格。').font = NOTE
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)

    # 下拉
    n_end = er + 1 + (ROWS_PER_PERIOD + 2) * 3
    dv_t = DataValidation(type='list', formula1='"经销商,直销客户,电商平台,商超,其他"', allow_blank=True)
    dv_m = DataValidation(type='list', formula1='"买断经销,委托代销,直销,平台入仓,平台代销,其他"', allow_blank=True)
    dv_y = DataValidation(type='list', formula1='"是,否"', allow_blank=True)
    for dv in (dv_t, dv_m, dv_y): ws.add_data_validation(dv)
    dv_t.add(f'E{er+1}:E{n_end}'); dv_m.add(f'F{er+1}:F{n_end}')
    dv_y.add(f'O{er+1}:O{n_end}'); dv_y.add(f'Q{er+1}:Q{n_end}')
    return ws

wb = openpyxl.Workbook()

# ---------------- 说明页 ----------------
ws = wb.active; ws.title = '填报说明'
ws.column_dimensions['A'].width = 14
ws.column_dimensions['B'].width = 108
ws['A1'] = '燕京中发IPO项目  客户清单填报说明'
ws['A1'].font = Font(name=F, size=15, bold=True)
ws.merge_cells('A1:B1'); ws.row_dimensions[1].height = 28

rows = [
 ('对应清单编号', '2-4-2（北京燕京中发生物技术有限公司）、1-8-5（燕京中发生物技术（邢台）有限公司）'),
 ('清单原文要求', '2-4-2：2024年、2025年、2026年1-6月各期至少前20名且占销售金额比例至少50%以上客户清单、金额、占比及回款情况的列表。\n'
                  '1-8-5：燕京中发生物技术（邢台）有限公司2024年、2025年、2026年1-6月各期前20大客户清单、前10大供应商清单。'),
 ('填报范围', '两家主体分别填报，分别对应“客户清单-燕京中发”“客户清单-中发邢台”两个工作表；每家各填报三个期间。'),
 ('填报口径', '1、销售金额为不含税口径，与当期利润表营业收入可勾稽；\n'
             '2、客户名称须填写工商登记全称，与销售合同、发票开具名称一致，同一客户在各期须使用同一名称；\n'
             '3、同一集团下的不同法人主体请分别列示，并在备注栏注明所属集团；\n'
             '4、回款金额为含税口径，指本期实际收到的款项；\n'
             '5、各期按销售金额由大到小排列。'),
 ('必须达到的比例', '各期前列客户销售金额合计占当期营业收入的比例不得低于50%。若前20名合计未达50%，请在该期间区块下方继续插入行补充客户，直至“是否达到50%”显示“达标”。'),
 ('单元格颜色', '黄色底纹：需公司填写；\n灰色底纹：公式自动计算，请勿修改；\n蓝色字体：已由项目组预填的既有数据（营业收入），请公司复核。'),
 ('重点提示一', '第三方回款：如存在合同签订方、发票开具方与实际汇款方不一致的情形（例如由经销商的经营者、股东个人账户付款），务必在“是否存在第三方回款”栏选“是”，并填列付款方名称及金额。该事项为IPO审核重点核查事项。'),
 ('重点提示二', '关联关系：请核查客户及其股东、实际控制人、主要经办人员，与发行人的股东、董事、监事、高级管理人员、员工及其近亲属之间是否存在持股、任职、亲属或其他关联关系，并在“关联关系说明”栏如实填列。公司拟实施经销商入股，该栏信息将直接影响相关论证。'),
 ('重点提示三', '客户重合度：两家主体的客户清单填报完成后，项目组将据以分析客户重合情况，用于同业竞争事项的论证，因此两表的客户名称口径必须统一。'),
 ('营业收入来源', '燕京中发：2024年212,656,418.65元、2025年434,358,616.85元、2026年1-6月208,146,233.34元，取自公司2024年度审计报告、2025年度财务报表及2026年6月30日利润表。\n'
                 '中发邢台：2024年5,163,572.58元、2025年100,430,167.78元、2026年1-6月29,375,817.27元，取自其2024及2025年度审计报告、2026年6月30日利润表。'),
 ('反馈方式', '填报完成后请连同“2-4-3 上述客户的销售合同”一并反馈项目组。如某栏确无法提供，请填“无”或“不适用”并说明原因，不要留空。'),
]
r = 3
for k, v in rows:
    a = ws.cell(r, 1, k); a.font = BOLD; a.fill = FILL_SEC; a.alignment = Alignment(vertical='top', wrap_text=True); a.border = BOX
    b = ws.cell(r, 2, v); b.font = N; b.alignment = WRAP; b.border = BOX
    ws.row_dimensions[r].height = max(30, 15 * (v.count('\n') + 1) + 12)
    r += 1

EX_ZF = ['2025年度', 1, '示例：××省××商贸有限公司', '91XXXXXXXXXXXXXXXX', '经销商', '买断经销', '华北区',
         '肠溶型纳豆胶囊、燕京纳福多肽', '2021-03', 12345678.90, None, 13950000.00, 0.00, 1200000.00,
         '是', '××（自然人，系该经销商股东）付款 300,000.00 元', '否', '无', '']
EX_XT = ['2025年度', 1, '示例：××省××生物科技有限公司', '91XXXXXXXXXXXXXXXX', '经销商', '买断经销', '华东区',
         '纳福多肽、有机全脂羊乳粉', '2024-08', 8765432.10, None, 9905000.00, 0.00, 500000.00,
         '否', '无', '否', '无', '']

sheet_list(wb, '客户清单-燕京中发', '北京燕京中发生物技术有限公司', REV_ZF, EX_ZF)
sheet_list(wb, '客户清单-中发邢台', '燕京中发生物技术（邢台）有限公司', REV_XT, EX_XT)

# ---------------- 客户重合度分析 ----------------
ws = wb.create_sheet('客户重合度分析')
ws['A1'] = '发行人与中发邢台客户重合情况分析'
ws['A1'].font = TIT; ws.merge_cells('A1:J1'); ws.row_dimensions[1].height = 24
ws['A2'] = '本表由项目组根据前两表填报结果编制，用于同业竞争事项论证。公司无需填写。'
ws['A2'].font = NOTE; ws.merge_cells('A2:J2')
h = ['序号', '客户名称（全称）', '统一社会信用代码',
     '燕京中发\n2024年度', '燕京中发\n2025年度', '燕京中发\n2026年1-6月',
     '中发邢台\n2024年度', '中发邢台\n2025年度', '中发邢台\n2026年1-6月', '说明']
w = [6, 34, 22, 16, 16, 16, 16, 16, 16, 30]
for i, (x, ww) in enumerate(zip(h, w), start=1):
    c = ws.cell(4, i, x); c.font, c.fill, c.alignment, c.border = H1, FILL_H, CTR, BOX
    ws.column_dimensions[get_column_letter(i)].width = ww
ws.row_dimensions[4].height = 36
for r in range(5, 35):
    for i in range(1, 11):
        c = ws.cell(r, i); c.border = BOX; c.font = N
        c.alignment = CTR if i == 1 else WRAP
        if 4 <= i <= 9: c.number_format = '#,##0.00'
ws.freeze_panes = 'C5'
ws.cell(36, 2, '重合客户合计').font = BOLD
for i in range(4, 10):
    c = ws.cell(36, i, f'=SUM({get_column_letter(i)}5:{get_column_letter(i)}34)')
    c.number_format = '#,##0.00'; c.font = BOLD; c.fill = FILL_CAL; c.border = BOX
ws.cell(36, 2).border = BOX

wb.save('/home/user/JXD/work/xls/2-4-2 客户清单填报模板.xlsx')
print('已生成')

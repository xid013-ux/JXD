# -*- coding: utf-8 -*-
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import TYJZ, TDSG, SRQR, FANLI

DOC = '/home/user/JXD/work/unpacked/word/document.xml'
RF  = '<w:rFonts w:hint="eastAsia" w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
RFP = '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
PPR = ('<w:spacing w:before="163" w:beforeLines="50" w:after="163" w:afterLines="50"'
       ' w:line="360" w:lineRule="auto"/><w:ind w:firstLine="480" w:firstLineChars="200"/>'
       '<w:jc w:val="both"/>')

def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def para(text, bold=False):
    """正文段落；bold=True 时整段加粗（用于（1）小标题及"建议："段）"""
    b = '<w:b/><w:bCs/>' if bold else ''
    return ('<w:p><w:pPr>' + PPR + '<w:rPr>' + RFP + b + '</w:rPr></w:pPr>'
            '<w:r><w:rPr>' + RF + b + '</w:rPr><w:t>' + esc(text) + '</w:t></w:r></w:p>')

def unit_para(text):
    """表格上方右对齐的"单位：万元"小字"""
    rpr = '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="21"/><w:szCs w:val="20"/>'
    return ('<w:p><w:pPr><w:pStyle w:val="432"/><w:spacing w:before="0" w:beforeLines="0" w:after="0"'
            ' w:afterLines="0" w:line="240" w:lineRule="auto"/><w:ind w:firstLine="0" w:firstLineChars="0"/>'
            '<w:jc w:val="right"/><w:rPr>' + rpr + '</w:rPr></w:pPr>'
            '<w:r><w:rPr>' + rpr + '</w:rPr><w:t>' + esc(text) + '</w:t></w:r></w:p>')

def cell(text, width, align, bold):
    b = '<w:b/>' if bold else ''
    jc = {'center': 'center', 'right': 'right', 'left': 'both'}[align]
    rpr = RF + b + '<w:kern w:val="2"/><w:sz w:val="21"/><w:szCs w:val="21"/>'
    run = ('<w:r><w:rPr>' + rpr + '</w:rPr><w:t>' + esc(text) + '</w:t></w:r>') if text else ''
    return ('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/><w:vAlign w:val="center"/></w:tcPr>'
            '<w:p><w:pPr><w:widowControl w:val="0"/><w:jc w:val="%s"/><w:rPr>%s</w:rPr></w:pPr>%s</w:p></w:tc>'
            % (width, jc, rpr, run))

def table(spec):
    widths, aligns, rows = spec['widths'], spec['aligns'], spec['rows']
    total = sum(widths)
    xml = ('<w:tbl><w:tblPr><w:tblStyle w:val="64"/><w:tblW w:w="%d" w:type="dxa"/><w:jc w:val="center"/>'
           '<w:tblBorders><w:top w:val="single" w:color="auto" w:sz="12" w:space="0"/>'
           '<w:left w:val="single" w:color="auto" w:sz="12" w:space="0"/>'
           '<w:bottom w:val="single" w:color="auto" w:sz="12" w:space="0"/>'
           '<w:right w:val="single" w:color="auto" w:sz="12" w:space="0"/>'
           '<w:insideH w:val="single" w:color="auto" w:sz="6" w:space="0"/>'
           '<w:insideV w:val="single" w:color="auto" w:sz="6" w:space="0"/></w:tblBorders>'
           '<w:tblLayout w:type="fixed"/><w:tblCellMar><w:top w:w="0" w:type="dxa"/>'
           '<w:left w:w="108" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/>'
           '<w:right w:w="108" w:type="dxa"/></w:tblCellMar></w:tblPr><w:tblGrid>' % total)
    xml += ''.join('<w:gridCol w:w="%d"/>' % w for w in widths) + '</w:tblGrid>'
    for ri, row in enumerate(rows):
        head = (ri == 0)
        xml += '<w:tr><w:trPr><w:trHeight w:val="397" w:hRule="atLeast"/><w:jc w:val="center"/></w:trPr>'
        for ci, txt in enumerate(row):
            al = 'center' if head else aligns[ci]
            xml += cell(txt, widths[ci], al, head)
        xml += '</w:tr>'
    return xml + '</w:tbl>'

def render(blocks):
    out = []
    for kind, val in blocks:
        if kind == 'h':      out.append(para(val, bold=True))    # 法律事项（1）（2）（3）标题：加粗
        elif kind == 's':    out.append(para(val, bold=False))   # 财务事项（1）小标题：不加粗
        elif kind == 'b':    out.append(para(val, bold=True))    # "建议：..."整段加粗
        elif kind == 'p':    out.append(para(val, bold=False))
        elif kind == 'unit': out.append(unit_para(val))
        elif kind == 'table':out.append(table(val))
        else: raise ValueError(kind)
    return ''.join(out)

# ---------- 定位并替换 ----------
x = open(DOC, encoding='utf8').read()
orig_len = len(x)

def pblock(xml, text, frm=0):
    """返回包含 text 的 <w:p> 段落块的 (start, end)"""
    i = xml.find('>' + text + '<', frm)
    if i < 0:
        i = xml.find(text, frm)
    if i < 0:
        raise SystemExit('NOT FOUND: ' + text)
    s = max(xml.rfind('<w:p ', 0, i), xml.rfind('<w:p>', 0, i))
    e = xml.find('</w:p>', i) + 6
    return s, e

# 四个待填充区域：(区域起点=标题段之后, 区域终点=下一标题段之前)
anchors = [
    ('同业竞争',                 '土地收购',                     TYJZ),
    ('土地收购',                 '独立性',                       TDSG),
    ('收入确认',                 '经销商返利政策的会计处理',      SRQR),
    ('经销商返利政策的会计处理', '（三）业务事项',                FANLI),
]

regions = []
for head, nxt, blocks in anchors:
    hs, he = pblock(x, head)
    ns, ne = pblock(x, nxt, he)
    regions.append((he, ns, blocks, head))

# 校验区域互不重叠、顺序递增
for a, b in zip(regions, regions[1:]):
    assert a[1] <= b[0], (a[3], b[3])

EMPTY_P = re.compile(r'<w:p\b[^>]*>(?:(?!<w:t[ >]).)*?</w:p>\s*$', re.S)

for start, end, blocks, head in reversed(regions):
    tail = ''
    seg = x[start:end]
    # 保留区域末尾原有的空段落（章节之间的间距）
    while True:
        m = EMPTY_P.search(seg)
        if not m or m.start() == 0:
            break
        tail = m.group(0) + tail
        seg = seg[:m.start()]
    x = x[:start] + render(blocks) + tail + x[end:]
    print('filled: %s  (%d -> %d chars)' % (head, end - start, len(render(blocks)) + len(tail)))

open(DOC, 'w', encoding='utf8').write(x)
print('document.xml: %d -> %d' % (orig_len, len(x)))

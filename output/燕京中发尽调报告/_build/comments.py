# -*- coding: utf-8 -*-
"""重新挂载 Word 批注（build.py 重写正文区域后批注标记会被清除，故每次 build 后需运行本脚本）"""
import re, os

W = '/home/user/JXD/work/unpacked/word'

# (锚定段落的起始文字, paraId, durableId, 批注正文)
COMMENTS = [
    ("两个方案在税务成本与资金占用上以方案一为优", "50A38C79", "5B79A389",
     "本节按框架性列示股权支付与现金支付两个方案，未作具体作价、股权比例及税费测算，待资产评估完成后补充。"
     "需公司确认或落实的事项："
     "一、方案选择取决于燕京集团（17.50%）及食品发酵研究院（2.50%）是否同意放弃优先认缴出资权并接受稀释，建议先行沟通并取得书面意见；"
     "二、企业所得税按25%法定税率，系因燕京啤酒为法人股东；20%系自然人股东转让股权的个人所得税税率，本次不适用；"
     "三、比例测算以重组前一个会计年度即2025年度数据为准，若重组推迟至2027年实施须以2026年度数据重新测算。"
     "中发邢台2026年6月末其他应收款16,640.95万元已使其资产总额占比升至54.85%，建议在重组实施前先行清理，避免比例被动跨档；"
     "四、对燕京啤酒审议层级的判断依据其2025年11月版《公司章程》第4.11条、第4.12条、第6.3条及第6.14条，"
     "建议由发行人律师与燕京啤酒董事会办公室及其常年法律顾问复核确认。"),

    ("解决路径有两条", "50A38C7A", "5B79A38A",
     "本节按框架性列示两个方案，未作具体作价及税费测算。"
     "最重要的待核事项是标的公司的经营现状：据其2025年度审计报告，2025年度啤酒收入23,294.41万元、占营业收入的77.61%，"
     "2024年度21,993.96万元，啤酒生产经营持续进行，与此前了解到的厂区已整体转为纳豆生产、不再从事啤酒生产的情况不一致。"
     "该事实直接决定方案选择——采用方案一的，发行人将一并取得该啤酒业务，与控股股东构成新的同业竞争，"
     "且两笔重组合并测算的营业收入占比达92.22%、已接近100%的临界值。请优先核实厂区的实际使用状况及两类生产活动的划分方式。"
     "其余待核事项："
     "一、该审计报告附注列示至“六、关联方”标题后即无内容，关联方及关联交易披露缺失，请会计师补充提供；"
     "二、该公司2025年度处置土地使用权账面原值475.66万元、账面价值332.96万元，需核实处置的是哪一宗宗地、受让方及定价，"
     "以确认拟收购范围内的土地是否完整；"
     "三、2025年度新增租赁收入366.97万元，需核实承租方是否为中发邢台；若是，则与中发邢台使用权资产为零的记账口径不符，需一并核对；"
     "四、其他应收款7,987.48万元，其中集团往来款账面余额7,949.25万元、几乎构成全部，且当年经营活动现金流量净额为负，需核查资金占用及回收安排；"
     "五、未分配利润-5,652.01万元、当年所得税费用为零，需取得税务口径的可弥补亏损余额及结转年限，用于测算方案二的所得税成本；"
     "六、宗地二的出让合同，其证载终止日期倒推的起始日期晚于发证日，两者不衔接；"
     "七、宗地四的实际使用状况及建设、环保手续；"
     "八、标的公司员工的劳动关系归属；"
     "九、标的公司的营业执照及公司章程。"),
]

AUTHOR, INITIALS, DATE = "燕京中发IPO项目组", "YJ", "2026-08-25T09:00:00Z"


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def root_open(s):
    m = re.match(r'^<\?xml[^>]*\?>\s*<[^>]+>', s, re.S)
    assert m, 'root tag not found'
    return m.group(0)


# ---------- 1. 重写四个批注文件 ----------
def rewrite(fname, body):
    p = os.path.join(W, fname)
    s = open(p, encoding='utf8').read()
    open(p, 'w', encoding='utf8').write(root_open(s) + body + s[s.rindex('</'):])


rpr = ('<w:rFonts w:hint="eastAsia" w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="宋体"/>'
       '<w:color w:val="000000"/><w:sz w:val="20"/><w:szCs w:val="20"/>')

rewrite('comments.xml', ''.join(
    '<w:comment w:id="%d" w:author="%s" w:date="%s" w:initials="%s">'
    '<w:p w14:paraId="%s" w14:textId="77777777"><w:pPr><w:pStyle w:val="CommentText"/></w:pPr>'
    '<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:annotationRef/></w:r>'
    '<w:r><w:rPr>%s</w:rPr><w:t xml:space="preserve">%s</w:t></w:r></w:p></w:comment>'
    % (i, AUTHOR, DATE, INITIALS, pid, rpr, esc(txt))
    for i, (_, pid, _d, txt) in enumerate(COMMENTS)))

rewrite('commentsExtended.xml', ''.join(
    '<w15:commentEx w15:paraId="%s" w15:done="0"/>' % pid for _, pid, _d, _t in COMMENTS))

rewrite('commentsIds.xml', ''.join(
    '<w16cid:commentId w16cid:paraId="%s" w16cid:durableId="%s"/>' % (pid, did)
    for _, pid, did, _t in COMMENTS))

rewrite('commentsExtensible.xml', ''.join(
    '<w16cex:commentExtensible w16cex:durableId="%s" w16cex:dateUtc="%s"/>' % (did, DATE)
    for _, _p, did, _t in COMMENTS))

# ---------- 2. 在正文中挂载标记 ----------
dp = os.path.join(W, 'document.xml')
x = open(dp, encoding='utf8').read()
assert 'commentRangeStart' not in x, '正文中已存在批注标记，请先运行 build.py 重建'

PARA = re.compile(r'<w:p\b[^>]*>.*?</w:p>', re.S)

for cid, (anchor, _p, _d, _t) in enumerate(COMMENTS):
    hit = None
    for m in PARA.finditer(x):
        seg = m.group(0)
        if anchor in re.sub(r'<[^>]+>', '', seg):
            hit = m
            break
    assert hit, '未找到锚定段落：' + anchor

    seg = hit.group(0)
    # commentRangeStart 必须是 w:p 的直接子元素，且位于 w:pPr 之后
    mp = re.search(r'</w:pPr>', seg)
    ins = mp.end() if mp else seg.index('>') + 1
    new = (seg[:ins]
           + '<w:commentRangeStart w:id="%d"/>' % cid
           + seg[ins:-len('</w:p>')]
           + '<w:commentRangeEnd w:id="%d"/>' % cid
           + '<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr>'
             '<w:commentReference w:id="%d"/></w:r></w:p>' % cid)
    x = x[:hit.start()] + new + x[hit.end():]
    print('批注 %d 已挂载：%s…' % (cid, anchor[:20]))

open(dp, 'w', encoding='utf8').write(x)
print('document.xml 更新完成，共 %d 条批注' % len(COMMENTS))

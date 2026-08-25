# -*- coding: utf-8 -*-
"""重新挂载 Word 批注（build.py 重写正文区域后批注标记会被清除，故每次 build 后需运行本脚本）"""
import re, os

W = '/home/user/JXD/work/unpacked/word'

# (锚定段落的起始文字, paraId, durableId, 批注正文)
COMMENTS = [
    ("综合考虑，本报告倾向于建议采用方案一", "50A38C79", "5B79A389",
     "本节按要求列示股权支付与现金支付两个方案，比例测算与交易对价统一采用2025年度经审计数据。"
     "需公司确认或落实的事项："
     "一、方案选择取决于燕京集团（17.50%）及食品发酵研究院（2.50%）是否同意放弃优先认缴出资权并接受稀释，"
     "建议先行沟通并取得书面意见，再最终定案；"
     "二、企业所得税按25%法定税率测算。燕京啤酒为法人股东，适用企业所得税法定税率；"
     "20%系自然人股东转让股权的个人所得税税率，本次不适用。若需同时列示20%口径的测算结果，请告知；"
     "三、交易对价以账面净资产模拟测算，实际须以经国资备案的评估结果为准。"
     "若采用收益法评估并产生增值，现金支付方案的所得税税负与股权支付方案的稀释幅度均将同步上升，届时需重新比选；"
     "四、《证券期货法律适用意见第3号》的比例测算以重组前一个会计年度即2025年度数据为准；"
     "若重组推迟至2027年实施，须以2026年度数据重新测算。中发邢台2026年6月末其他应收款达16,640.95万元，"
     "导致其资产总额占比升至54.85%，建议在重组实施前先行清理内部资金往来，避免比例被动跨档；"
     "五、对燕京啤酒审议层级的判断依据其2025年11月版《公司章程》第4.12条、第6.3条及第6.14条，"
     "结论为未达股东会及董事会的量化审议标准，但因章程规定出售资产事项不得授权经营管理层，仍建议提请董事会审议。"
     "该判断建议由发行人律师与燕京啤酒董事会办公室及其常年法律顾问复核确认。"),

    ("解决路径有两条", "50A38C7A", "5B79A38A",
     "按要求，本节只写方案、暂不填具体数据，交易对价及税费待取得燕京啤酒（邢台）有限公司财务数据后补充测算。"
     "最紧急待补材料：燕京啤酒（邢台）有限公司最近两年及一期财务报表（审计版最佳，未审亦可）。"
     "该数据不仅决定本节的对价与税费，更直接决定申报时点——"
     "其资产总额低于6,506.83万元的，两笔重组合并测算后仍处20%至50%档，申报节奏不受影响；"
     "介于6,506.83万元至26,499.94万元的，落入50%至100%档，申报文件范围与核查工作量显著增加；"
     "达到或超过26,499.94万元的，须在重组完成后运行一个完整会计年度方可申报，原定申报节点将丢失。"
     "鉴于该公司持有全部四宗宗地合计272.85亩及地上厂房、工商登记显示其7,300.00万元注册资本已全额实缴，"
     "落入第二档存在较大可能，请优先落实。需说明此为方向性判断：工商公示的实缴出资额未经登记机关核验，"
     "宗地取得于2009年至2015年、土地厂房已计提多年摊销折旧，账面资产总额与实际价值可能差异较大，"
     "均不能替代实际测算。另注意燕京啤酒母公司报表中对该公司的长期股权投资17,172.00万元系其收购股权的支付成本，"
     "该公司系非同一控制下企业合并取得、对价支付给原股东，不构成该公司自身资产，不能据以推算其资产总额。"
     "其余待核事项："
     "一、标的公司的或有负债、对外担保、未决诉讼、行政处罚、税务合规及环保遗留情况，若有重大问题宜转向方案二；"
     "二、宗地二的出让合同。该证载终止日期为2066年10月15日，按工业用地五十年最高年限倒推的起始日期晚于其2015年12月18日的发证日，两者不衔接，需核对；"
     "三、宗地四的实际使用状况及建设、环保手续。该宗地证载用途为工业用地，与公司说明的污水处理用途不一致；"
     "四、中发邢台与燕京啤酒（邢台）有限公司之间土地及厂房使用的书面协议及租金支付凭证。"
     "中发邢台账面使用权资产为零，通常意味着双方未签署书面租赁协议或未实际支付租金，涉及关联方利益输送嫌疑，需核实并规范；"
     "五、啤酒生产线停产及改建为纳豆生产线的书面依据。燕京啤酒2025年年度报告显示，"
     "其因收购该公司形成的商誉1,278.72万元已全额计提减值准备，可作为原啤酒业务已不具备持续盈利能力的佐证，"
     "但仍需取得停产决议、技改立项文件、设备处置记录等直接证据；"
     "六、113名员工的实际工作内容及劳动关系归属；"
     "七、标的公司的营业执照及公司章程。"),
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

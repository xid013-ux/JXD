#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GTHT 内部研究报告 —— 定稿自检

用法：
    python3 check_report.py 报告.docx            # 全量，定稿前跑一次
    python3 check_report.py 报告.docx --brief     # 只报错误，提醒折叠成计数

检查项对应 references/写作规范.md 的定稿检查清单中可自动化的部分。
人工仍需过一遍内容类检查（是否有小结段、是否有内部语的漏网之鱼等）。
"""
import re
import sys
from collections import Counter

try:
    from docx import Document
    from docx.oxml.ns import qn
except ImportError:
    sys.exit('需要 python-docx：pip install python-docx')


# ---------- 规则表 ----------

# 全篇禁用：不确定标注、免责声明、第一人称判断
BANNED = [
    (r'待核实|待确认|存疑|未经核实|尚需核实', '不确定标注（应核实后确定，或整条删除）'),
    (r'建议以.{0,12}复核|有待进一步确认|建议进一步核实', '复核建议（不应出现在正文）'),
    (r'本报告仅供内部参考|免责声明', '免责声明（正文不写）'),
    (r'我们认为|笔者认为|笔者以为', '第一人称判断'),
    (r'据不完全统计', '模糊统计口径'),
]

# 观点性表述：多列事实、少列观点（微信明确要求）
OPINION = [
    (r'业内(普遍)?认为|市场(普遍)?认为|一般认为|普遍认为|有观点认为|'
     r'业内人士(表示|指出|认为)|分析师认为|市场预期', '无主体的观点引用，应换成有主体、有时间、有口径的事实'),
    (r'有望|或将|料将|前景广阔|大有可为|值得期待', '推测性表述，应换成已发生的事实或注明预测主体与时间'),
    (r'某(券商|机构|研报)认为|研报(认为|指出)', '第三方观点直接引用，应改为陈述其发布了什么数据'),
]

# 仅在"拜访/关注要点"专章之外禁用的内部语
# 领导保留了整章拜访内容，反对的是把它撒进行业和公司章节
BANNED_OUTSIDE_VISIT = [
    (r'本次拜访|此次拜访|本次调研|本次走访', '内部语（应集中到拜访专章）'),
    (r'对我司|对我们的意义|对本项目的意义', '内部语（应集中到拜访专章）'),
    (r'可对接的客户资源|潜在合作机会', '内部语（应集中到拜访专章）'),
]
# 拜访专章的一级标题特征，命中后其后所有内容豁免上述内部语检查
VISIT_CHAPTER = re.compile(r'拜访|关注要点|尽调')

# 小节标题里的小结类词。注意：领导删掉了"6.7 资本化特征小结"（纯归纳段落），
# 但保留了"7.5 关联全景与小结"（以事实汇总表为主）。所以只提醒、不判错。
BANNED_HEADING = [
    (r'小结|总结|启示|归纳|几点判断|特征总结', '小结类章节：确认本节以事实汇总为主，'
                                    '若只是推论性归纳则应删除（领导删过 6.7 资本化特征小结）'),
]
# 例外：拜访专章的"初步判断"是题目要求的部分
HEADING_EXEMPT = re.compile(r'初步判断')

# 固定用词（仅检查来源注，正文叙述中的表述不强制）
WORDING_IN_SOURCE = [
    # 领导的写法是"Wind整理成果"或"Wind金融数据库整理成果"，关键在"整理成果"，
    # 不要改写成"Wind数据库"（他 9 处全部改了回去）
    # 只在"Wind"直接作为出处出现时检查；"Wind指标ID""Wind收录"等描述性用法不触发
    (r'Wind\s*(?!(金融数据库)?整理成果|指标|收录|终端|资讯|代码)',
     'Wind 取数在来源注中应写"Wind整理成果"或"Wind金融数据库整理成果"，不要写"Wind数据库"'),
]

# 署名：领导定稿版一律用「本报告整理」，从不用"国泰海通投资银行部整理"
BAD_SIGNOFF = re.compile(r'国泰海通投资银行部整理|国泰海通证券整理|本部门整理')

# 表图标题：编号与题名之间用空格，不用冒号
CAPTION = re.compile(r'^\s*([表图])\s*(\d+)\s*([：:])')

SOURCE_PREFIX = re.compile(r'^\s*(数据来源|资料来源)[:：]')


def para_style(p):
    return p.style.name if p.style is not None else 'Normal'


def around(text, m, span=26):
    """截取命中位置上下文，便于定位。"""
    t = text.strip()
    a = max(0, m.start() - span)
    b = min(len(t), m.end() + span)
    return ('…' if a else '') + t[a:b] + ('…' if b < len(t) else '')


def iter_body_text(doc):
    """按文档顺序产出 (kind, index, style, text)。"""
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    pi = 0
    for ch in doc.element.body.iterchildren():
        if ch.tag == qn('w:p'):
            p = Paragraph(ch, doc)
            pi += 1
            yield 'p', pi, para_style(p), p.text
        elif ch.tag == qn('w:tbl'):
            t = Table(ch, doc)
            for r, row in enumerate(t.rows):
                for c in row.cells:
                    yield 'tc', pi, 'TableCell', c.text


def main(path, brief=False):
    doc = Document(path)
    problems = []   # (级别, 位置, 说明, 摘录)

    paras = list(doc.paragraphs)
    all_text = '\n'.join(p.text for p in paras)

    # 1) 禁用表述
    in_visit_chapter = False
    for kind, idx, style, text in iter_body_text(doc):
        if style == 'Heading 2':
            in_visit_chapter = bool(VISIT_CHAPTER.search(text))
        if not text.strip():
            continue
        for pat, why in BANNED:
            m = re.search(pat, text)
            if m:
                problems.append(('错误', f'第{idx}段附近', why, around(text, m)))
        if not in_visit_chapter:
            for pat, why in BANNED_OUTSIDE_VISIT:
                m = re.search(pat, text)
                if m:
                    problems.append(('错误', f'第{idx}段附近', why, around(text, m)))
        for pat, why in OPINION:
            m = re.search(pat, text)
            if m:
                problems.append(('提醒', f'第{idx}段附近',
                                 f'「{m.group(0)}」{why}', around(text, m)))
        m = CAPTION.match(text)
        if m:
            problems.append(('错误', f'第{idx}段',
                             f'表图标题的编号与题名之间应用空格，不用「{m.group(3)}」'
                             f'（领导定稿版 25 个标题全部用空格）',
                             text.strip()[:40]))
        if SOURCE_PREFIX.match(text):
            m = BAD_SIGNOFF.search(text)
            if m:
                problems.append(('错误', f'第{idx}段',
                                 f'来源注署名应为「本报告整理」，不写「{m.group(0)}」',
                                 around(text, m)))
            for pat, why in WORDING_IN_SOURCE:
                if re.search(pat, text):
                    problems.append(('提醒', f'第{idx}段附近', why, text.strip()[:60]))
            # 双出处：原始出处 + 转述出处
            body_txt = SOURCE_PREFIX.sub('', text).split('。')[0]
            seps = sum(body_txt.count(c) for c in '，,；;、')
            if seps < 1:
                problems.append(('提醒', f'第{idx}段附近',
                                 '来源注疑似只有单一出处，应保留"原始出处 + 转述出处"两个维度',
                                 text.strip()[:60]))

    # 2) 小结类标题
    for i, p in enumerate(paras, 1):
        st = para_style(p)
        if st.startswith('Heading'):
            t = p.text.strip()
            for pat, why in BANNED_HEADING:
                if re.search(pat, t) and not HEADING_EXEMPT.search(t):
                    problems.append(('提醒', f'第{i}段', why, t))

    # 3) ASCII 直引号
    n_quote = all_text.count('"')
    if n_quote:
        problems.append(('错误', '全文', f'存在 {n_quote} 处 ASCII 直引号，应改为全角“”', ''))
    n_apos = len(re.findall(r"(?<![A-Za-z])'|'(?![A-Za-z])", all_text))
    if n_apos:
        problems.append(('提醒', '全文', f'存在 {n_apos} 处可疑 ASCII 单引号', ''))

    # 4) 表/图编号连续性
    def check_seq(kind, pat):
        nums = [int(m) for m in re.findall(pat, all_text)]
        seen = []
        for n in nums:
            if n not in seen:
                seen.append(n)
        if not seen:
            return
        expect = list(range(1, max(seen) + 1))
        missing = [n for n in expect if n not in seen]
        if missing:
            problems.append(('错误', '全文',
                             f'{kind}编号不连续，缺 {kind}' + '、'.join(map(str, missing)), ''))
        dup = [n for n, c in Counter(
            [int(m) for m in re.findall(pat + r'[：:]', all_text)]).items() if c > 1]
        if dup:
            problems.append(('提醒', '全文',
                             f'{kind}编号重复：' + '、'.join(map(str, dup)), ''))

    check_seq('表', r'表\s*(\d+)')
    check_seq('图', r'图\s*(\d+)')

    # 5) 来源注：字号与居中
    n_src, bad_sz, bad_jc = 0, 0, 0
    for p in paras:
        if not SOURCE_PREFIX.match(p.text):
            continue
        n_src += 1
        szs = [int(sz.get(qn('w:val')))
               for sz in p._p.findall('.//' + qn('w:sz'))]
        if not szs or any(s != 11 for s in szs):
            bad_sz += 1
        jc = p._p.find(qn('w:pPr') + '/' + qn('w:jc'))
        if jc is None or jc.get(qn('w:val')) != 'center':
            bad_jc += 1
    if bad_sz:
        problems.append(('错误', '全文', f'{bad_sz}/{n_src} 条来源注不是七号字（w:sz=11）', ''))
    if bad_jc:
        problems.append(('错误', '全文', f'{bad_jc}/{n_src} 条来源注未居中', ''))

    # 6) 每张表/图后是否有来源注
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    kids = list(doc.element.body.iterchildren())
    n_tbl = sum(1 for ch in kids if ch.tag == qn('w:tbl'))
    n_pic = len(doc.element.body.findall('.//' + qn('w:drawing')))
    if n_src < n_tbl + n_pic:
        problems.append(('提醒', '全文',
                         f'来源注 {n_src} 条，少于 表{n_tbl} + 图{n_pic} = {n_tbl + n_pic}，'
                         f'可能有表或图缺来源注', ''))

    lv = Counter(para_style(p) for p in paras)

    # 7) 目录（仅完整正文报告需要）
    # 提纲 memo：无表无图且篇幅短
    # 单章节选：一级标题不足 2 个，说明不是完整报告
    chars_total = sum(len(p.text) for p in paras)
    is_memo = n_tbl == 0 and n_pic == 0 and chars_total < 4000
    is_excerpt = lv.get('Heading 2', 0) < 2
    if not (is_memo or is_excerpt):
        has_toc = 'TOC \\o' in doc.element.body.xml
        if not has_toc:
            problems.append(('错误', '全文', '未检出 TOC 域，目录可能是手打的', ''))
        uf = doc.settings.element.find(qn('w:updateFields'))
        if uf is None or uf.get(qn('w:val')) not in ('true', '1', 'on'):
            problems.append(('提醒', '全文',
                             'settings.xml 未设 updateFields=true，打开时不会刷新页码', ''))
    elif is_memo:
        # 提纲 memo 的专属约束：纯文字、不超过两页
        if chars_total > 2600:
            problems.append(('提醒', '全文',
                             f'提纲约 {chars_total} 字，可能超过两页，需精简', ''))

    # 8b) 表图编号连续性与交叉引用
    caps = {}
    for kind, idx, style, text in iter_body_text(doc):
        if kind != 'p':
            continue
        m = re.match(r'^(表|图)\s*(\d+)\s', text.strip())
        if m:
            caps.setdefault(m.group(1), []).append(int(m.group(2)))
    for kw, nums in caps.items():
        want = list(range(1, len(nums) + 1))
        if nums != want:
            problems.append(('错误', '全文',
                             f'{kw}编号不连续或有重复：{nums}', ''))
    # 正文里的"见表X/图X"是否越界
    for kw, nums in caps.items():
        top = max(nums) if nums else 0
        for m in re.finditer(rf'{kw}\s*(\d+)', all_text):
            n = int(m.group(1))
            if n > top:
                problems.append(('错误', '全文',
                                 f'引用了不存在的{kw}{n}（全文最大为{kw}{top}）',
                                 around(all_text, m)))
                break

    # 8c) 长难句与全文重复长句
    body_paras = [p.text for p in paras
                  if para_style(p) not in ('Heading 2', 'Heading 3')
                  and not re.match(r'^(表|图)\s*\d+\s', p.text.strip())
                  and not p.text.strip().startswith(('资料来源', '数据来源'))]
    seen = {}
    for txt in body_paras:
        for sent in re.split(r'(?<=。)', txt):
            sent = sent.strip()
            if len(sent) < 22:
                continue
            # 分号并列、顿号清单都属可读结构，不算长难句；
            # 真正要拎出来的是靠嵌套定语堆长的句子
            listy = ('；' in sent) or (sent.count('、') >= 3)
            if len(sent) >= 70 and not listy:
                problems.append(('提醒', '正文',
                                 f'长难句 {len(sent)} 字，考虑拆分', sent[:60] + '…'))
            seen[sent] = seen.get(sent, 0) + 1
    for sent, n in seen.items():
        if n > 1:
            problems.append(('错误', '正文',
                             f'该句全文出现 {n} 次，上文说过下文不必再说',
                             sent[:60] + '…'))

    # 8d) 表格几何回归校验
    sect = doc.element.body.find(qn('w:sectPr'))
    if sect is not None:
        pg = sect.find(qn('w:pgSz')); mar = sect.find(qn('w:pgMar'))
        if pg is not None and mar is not None:
            content_tw = (int(pg.get(qn('w:w')))
                          - int(mar.get(qn('w:left'))) - int(mar.get(qn('w:right'))))
            for ti, tbl in enumerate(doc.element.body.iter(qn('w:tbl')), 1):
                pr = tbl.find(qn('w:tblPr'))
                if pr is None:
                    continue
                tw = pr.find(qn('w:tblW'))
                lay = pr.find(qn('w:tblLayout'))
                grid = tbl.find(qn('w:tblGrid'))
                if tw is None or tw.get(qn('w:type')) != 'dxa':
                    problems.append(('错误', f'表{ti}',
                                     '表宽不是 dxa 绝对值；pct + 自适应会让列宽被 Word 重排', ''))
                elif int(tw.get(qn('w:w'))) != content_tw:
                    problems.append(('错误', f'表{ti}',
                                     f'表宽 {tw.get(qn("w:w"))} ≠ 版心 {content_tw}', ''))
                if lay is None or lay.get(qn('w:type')) != 'fixed':
                    problems.append(('错误', f'表{ti}', '未设 tblLayout=fixed，列宽保不住', ''))
                if grid is not None:
                    gs = sum(int(c.get(qn('w:w'))) for c in grid.findall(qn('w:gridCol')))
                    if gs != content_tw:
                        problems.append(('错误', f'表{ti}',
                                         f'tblGrid 合计 {gs} ≠ 版心 {content_tw}', ''))

    # 8) 标题层级
    if lv.get('Heading 1', 0):
        problems.append(('提醒', '全文', f'出现 {lv["Heading 1"]} 个 Heading 1，本体例只用 Heading 2/3', ''))
    if lv.get('Heading 4', 0):
        problems.append(('提醒', '全文', f'出现 {lv["Heading 4"]} 个 Heading 4，本体例只用两级标题', ''))

    # ---------- 输出 ----------
    chars = sum(len(p.text) for p in paras)
    errs = [p for p in problems if p[0] == '错误']
    warns = [p for p in problems if p[0] == '提醒']

    # --brief：只报错误，提醒折叠成计数。改稿轮反复跑用这个，省上下文。
    if brief:
        print(f'{path} ｜ 段{len(paras)} 表{n_tbl} 图{n_pic} 源{n_src} 约{chars}字 '
              f'｜ 错误{len(errs)} 提醒{len(warns)}')
        for _, where, why, _s in errs:
            print(f'  ✗ {where}：{why}')
        if not errs:
            print('  ✓ 无错误项' + (f'（{len(warns)} 项提醒已折叠，去掉 --brief 查看）'
                                  if warns else ''))
        return 1 if errs else 0

    print(f'文件：{path}')
    print(f'段落 {len(paras)} ｜ 表 {n_tbl} ｜ 图 {n_pic} ｜ 来源注 {n_src} ｜ 正文约 {chars} 字')
    print(f'标题：一级 {lv.get("Heading 2", 0)} 个，二级 {lv.get("Heading 3", 0)} 个')
    print('-' * 72)

    if not problems:
        print('✅ 自动检查项全部通过。仍需人工过一遍内容类检查清单。')
        return 0

    for level, group in (('错误', errs), ('提醒', warns)):
        if not group:
            continue
        print(f'\n【{level}】{len(group)} 项')
        for _, where, why, snippet in group:
            print(f'  · {where}：{why}')
            if snippet:
                print(f'      「{snippet}」')
    print('\n' + '-' * 72)
    print('人工仍需检查：归纳性段落、内部语漏网、口径一致性（统计对象/地域/品类/时间）、'
          '是否跨口径做过乘除、股东与保荐关系是否混淆、上市地是否查全、'
          '主营业务描述是否属实、竞争格局是否只列了公司名单、'
          '是否使用了客户非公开信息。')
    return 1 if errs else 0


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--brief']
    if len(args) != 1:
        sys.exit(__doc__)
    sys.exit(main(args[0], brief='--brief' in sys.argv[1:]))

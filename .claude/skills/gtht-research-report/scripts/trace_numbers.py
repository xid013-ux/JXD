# -*- coding: utf-8 -*-
"""数字溯源：把报告正文里的数字回原始资料逐个比对。

定稿前跑一次全量。check_report.py 是无依赖的快检，这个脚本需要原始语料，
所以单独放。

用法：
    python3 trace_numbers.py <报告.docx> <原始资料目录> [更多目录...]

原始资料目录里放招股说明书、问询回复、年报等的**纯文本**（.txt）。
PDF 先转文本：pdftotext -layout xxx.pdf xxx.txt

输出：报告里出现、但在原始资料中找不到的数字，逐个列出上下文。
本报告自行加总、来自 Wind 或网络检索的数字会被标出来，需人工确认，
不是错误。
"""
import sys, os, re, glob, zipfile
from lxml import etree

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


def doc_text(path):
    x = etree.fromstring(zipfile.ZipFile(path).read('word/document.xml'))
    for sdt in list(x.iter(W + 'sdt')):        # 去掉目录域
        sdt.getparent().remove(sdt)
    return ''.join(t.text or '' for t in x.iter(W + 't'))


def load_corpus(dirs):
    txt = []
    for d in dirs:
        for f in glob.glob(os.path.join(d, '**', '*.txt'), recursive=True):
            with open(f, encoding='utf-8', errors='ignore') as fh:
                txt.append(fh.read())
    return '\n'.join(txt)


def main(report, dirs):
    body = doc_text(report)
    corpus = load_corpus(dirs)
    if not corpus:
        print('原始资料目录里没有 .txt，先把 PDF 转成文本：')
        print('  pdftotext -layout xxx.pdf xxx.txt')
        return 1
    flat = re.sub(r'[\s,，]', '', corpus)

    # 带小数的数字最容易抄错，优先全查；纯整数误报多，只查四位以上
    # 后面跟字母的是代码类（统一社会信用代码、证券代码等），不是数据
    pats = [r'(?<![\d.])\d{1,3}(?:,\d{3})*\.\d{1,2}(?![\d])',
            r'(?<![\d.,])\d{4,}(?![\d.A-Za-z])']
    hits = []
    for pat in pats:
        for m in re.finditer(pat, body):
            hits.append((m.group(), m.start()))

    seen, miss = set(), []
    for num, pos in hits:
        if num in seen:
            continue
        seen.add(num)
        if num.replace(',', '') in flat or num in corpus:
            continue
        miss.append((num, body[max(0, pos - 45):pos + len(num) + 15]))

    print(f'报告：{report}')
    print(f'原始资料：{len(corpus):,} 字符')
    print(f'待查数字 {len(seen)} 个，其中 {len(miss)} 个未在原始资料中找到')
    print('-' * 72)
    if not miss:
        print('全部可溯源。')
        return 0
    for num, ctx in miss:
        print(f'  ★ {num}')
        print(f'      …{ctx.strip()}…')
    print('-' * 72)
    print('以上需逐个确认：本报告加总的、来自 Wind 或网络检索的属正常，')
    print('但必须能说出出处；说不出出处的整条删掉，不要留在纸面上。')
    return 0


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    sys.exit(main(sys.argv[1], sys.argv[2:]))

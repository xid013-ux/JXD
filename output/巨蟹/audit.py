# -*- coding: utf-8 -*-
"""抽出正文里所有含数字或公司主语的句子，供逐条核源。"""
import re
from docx import Document

d = Document('巨蟹智能尽调报告第六章_公司所处行业分析.docx')
paras = [p.text.strip() for p in d.paragraphs if p.text.strip()]

NUM = re.compile(r'\d')
COMPANY = re.compile(r'公司|巨蟹')
seen = set()
n = 0
for p in paras:
    if p.startswith('资料来源') or p.startswith('图'):
        continue
    for s in re.split(r'(?<=[。；])', p):
        s = s.strip()
        if len(s) < 6 or s in seen:
            continue
        if NUM.search(s) or COMPANY.search(s):
            seen.add(s)
            n += 1
            print(f'{n:02d}. {s}')
print(f'\n共 {n} 条')

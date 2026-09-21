# -*- coding: utf-8 -*-
"""合并生成《第五章 业务与技术分析》《第六章 公司所处行业分析》单一交付稿。

两章各自的 ch5.py / ch6.py 仍可独立运行出单章文件；本脚本复用其正文内容，
共用一个 Builder 写入同一文档，并将第六章的图表编号顺延，保证全篇连续：
    表1—表9（第五章）、表10—表13（第六章）
    图1—图3（第五章）、图4—图8（第六章）
"""
import os
import re
from fmt import Builder

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '巨蟹智能尽调报告第五章第六章.docx')

TBL_OFFSET = 9   # 第五章共 9 张表
FIG_OFFSET = 3   # 第五章共 3 张图


def run(fname, builder, tbl_off=0, fig_off=0):
    path = os.path.join(HERE, fname)
    ns = {'SHARED_BUILDER': builder, '__file__': path, '__name__': 'merged'}
    if tbl_off or fig_off:
        origin = builder.figcap

        def shifted(text):
            m = re.match(r'^(表|图)(\d+)(\s.*)$', text)
            if m:
                off = tbl_off if m.group(1) == '表' else fig_off
                text = '%s%d%s' % (m.group(1), int(m.group(2)) + off, m.group(3))
            return origin(text)

        builder.figcap = shifted
        try:
            exec(compile(open(path, encoding='utf-8').read(), fname, 'exec'), ns)
        finally:
            builder.figcap = origin
    else:
        exec(compile(open(path, encoding='utf-8').read(), fname, 'exec'), ns)


b = Builder()
run('ch5.py', b)
run('ch6.py', b, TBL_OFFSET, FIG_OFFSET)
b.save(OUT)
print('已生成', os.path.basename(OUT))

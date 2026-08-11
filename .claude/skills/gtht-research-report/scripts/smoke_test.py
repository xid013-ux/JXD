#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""构建工具链冒烟测试

验证 assets/ 里的模板与构建代码在当前环境可用，并演示标准调用方式。

    python3 smoke_test.py [输出目录]

跑通后会在输出目录生成 smoke.docx，可用 check_report.py 与
/mnt/skills/public/docx/scripts/office/validate.py 复验。
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), 'assets')

OUTDIR = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
CHARTS = os.path.join(OUTDIR, 'charts')
os.makedirs(CHARTS, exist_ok=True)

# --- 造一张符合配色规范的图 ---
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei']
matplotlib.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt

PALETTE = ['#123F63', '#2E6C97', '#5B93B8', '#8FB6CE', '#C3D6E3', '#E3EBF1']
fig, ax = plt.subplots(figsize=(8, 3.4))
ax.bar(['2023年', '2024年', '2025年'], [3, 8, 20], color=PALETTE[:3])
for s in ('top', 'right'):
    ax.spines[s].set_visible(False)
ax.grid(axis='y', linestyle='--', color='#DDDDDD')
ax.set_axisbelow(True)
ax.set_ylabel('出货量（千台）')
for i, v in enumerate([3, 8, 20]):
    ax.text(i, v + 0.4, str(v), ha='center', fontsize=9)
fig.tight_layout()
fig.savefig(os.path.join(CHARTS, 'fig1.png'), dpi=200)
plt.close(fig)

# --- 构建 docx ---
sys.path.insert(0, ASSETS)
os.environ['DOCX_OUT'] = os.path.join(OUTDIR, 'smoke.docx')
os.environ['DOCX_CHARTS'] = CHARTS
from _helpers import *          # noqa: E402,F403

title('中国XX产业链研究')

h2('产业概述')
h3('1.1 行业简介')
para('这是一段正文，用于验证样式、首行缩进与"引号"自动转全角是否正常。')

h3('1.2 代表企业')
table(
    ['公司', '所属环节', '主营业务情况'],
    [['甲公司', '谐波减速器', '精密谐波减速器的研发、生产与销售'],
     ['乙公司', '一体化关节模组', '关节模组及伺服驱动系统']],
    [18, 20, 62],
    caption='表1：代表企业一览',
    source='数据来源：Wind整理成果，国泰海通投资银行部整理',
    aligns=['center', 'center', 'left'],
)

h2('市场规模')
h3('2.1 出货量')
figure('fig1.png', '图1：出货量趋势',
       '数据来源：行业协会统计，国泰海通投资银行部整理')

make_toc(doc)                   # noqa: F405 —— 必须在所有标题之后
import _fixup                   # noqa: E402,F401 —— 必须是最后一步，保存在这里发生

print('冒烟测试通过。接着跑：')
print(f'  python3 /mnt/skills/public/docx/scripts/office/validate.py {os.environ["DOCX_OUT"]}')
print(f'  python3 {os.path.join(HERE, "check_report.py")} {os.environ["DOCX_OUT"]}')

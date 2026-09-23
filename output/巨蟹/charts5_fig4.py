# -*- coding: utf-8 -*-
"""第五章 图4 公司营业收入情况。

数据来源
    2024年度、2025年度  企业《盈利预测》表列 2024A、2025A 实际数
    2026年1-7月         随尽调资料提供的客户级销售明细按期加总
    上述两条来源在 2025 年度相互勾稽，差额为零；口径均为不含税、未经审计。

2026年为 1-7 月数，与前两期全年数不可直接比较，故另列月均数并加注说明。
"""
import os, matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei']
matplotlib.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

W_IN = 5.75
PT_U = 72 * W_IN / 100
P = ['#1F4E79', '#2E75B6', '#9DC3E6', '#BDD7EE', '#DEEBF7']
TXT = '#404A56'

DATA = [('2024年度', 3168.54, 12), ('2025年度', 5278.54, 12),
        ('2026年1-7月', 11467.06, 7)]


def fig_rev(out=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'fig', 'c5_fig4.png')):
    FS_V, FS_X, FS_S = 9.5, 9.0, 8.0
    YH = 43.0
    fig, ax = plt.subplots(figsize=(W_IN, W_IN * YH / 100))
    ax.set_xlim(0, 100); ax.set_ylim(0, YH); ax.axis('off')

    base, top = 12.0, 34.0                       # 基线与柱顶上限
    vmax = max(d[1] for d in DATA)
    BW = 14.5
    xs = [22.0, 50.0, 78.0]

    # 淡色参考线
    for f in (0.25, 0.50, 0.75, 1.0):
        y = base + (top - base) * f
        ax.plot([10, 92], [y, y], color='#EDF1F5', lw=0.8, zorder=0)
    ax.plot([10, 92], [base, base], color='#B7C4D2', lw=1.0, zorder=2)

    for (name, v, months), x in zip(DATA, xs):
        h = (top - base) * v / vmax
        c = P[0] if months == 7 else P[1]
        ax.add_patch(Rectangle((x - BW / 2, base), BW, h, facecolor=c,
                               edgecolor='none', zorder=3))
        ax.text(x, base + h + 1.5, '%s' % format(v, ',.2f'), ha='center',
                va='bottom', fontsize=FS_V, color=P[0], fontweight='bold')
        ax.text(x, base - 2.6, name, ha='center', va='center',
                fontsize=FS_X, color=TXT)
        ax.text(x, base - 5.8, '月均 %s' % format(v / months, ',.2f'),
                ha='center', va='center', fontsize=FS_S, color='#7A8794')

    ax.text(10, top + 5.2, '单位：万元', ha='left', va='center',
            fontsize=FS_S, color=TXT)
    ax.text(10, 3.0, '注：2026年为1-7月数，与前两期全年数不可直接比较',
            ha='left', va='center', fontsize=FS_S, color='#7A8794')
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    fig.savefig(out, dpi=300, facecolor='white')
    plt.close(fig)
    return out


if __name__ == '__main__':
    print('已生成', fig_rev())

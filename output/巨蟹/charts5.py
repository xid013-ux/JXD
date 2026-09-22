# -*- coding: utf-8 -*-
"""第五章 业务与技术分析 插图"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, FancyArrowPatch

plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei']
plt.rcParams['axes.unicode_minus'] = False

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, 'fig')
os.makedirs(FIG, exist_ok=True)

DARK = '#1F4E79'
MID = '#2E75B6'
LIGHT = '#DEEBF7'
EDGE = '#1F4E79'


def box(ax, x, y, w, h, text, fill=LIGHT, fs=8.5, bold=False):
    p = FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                       boxstyle='round,pad=0.012,rounding_size=0.02',
                       linewidth=1.0, edgecolor=EDGE, facecolor=fill, zorder=3)
    ax.add_patch(p)
    ax.text(x, y, text, ha='center', va='center', fontsize=fs, zorder=4,
            color='white' if fill == DARK else '#1a1a1a',
            fontweight='bold' if bold else 'normal', linespacing=1.4)


def diamond(ax, x, y, w, h, text, fs=8.5):
    pts = [(x, y + h / 2), (x + w / 2, y), (x, y - h / 2), (x - w / 2, y)]
    ax.add_patch(Polygon(pts, closed=True, linewidth=1.0,
                         edgecolor=EDGE, facecolor='#FFFFFF', zorder=3))
    ax.text(x, y, text, ha='center', va='center', fontsize=fs, zorder=4)


def arrow(ax, p0, p1, rad=0.0):
    ax.add_patch(FancyArrowPatch(
        p0, p1, arrowstyle='-|>', mutation_scale=9, linewidth=0.9,
        color=MID, zorder=2,
        connectionstyle=f'arc3,rad={rad}' if rad else 'arc3'))


# ==================== 图1 研发流程 ====================
def fig_rd():
    fig, ax = plt.subplots(figsize=(6.6, 7.4))
    ax.set_xlim(0, 10); ax.set_ylim(0, 11.6); ax.axis('off')

    lanes = ['相关部门', '产品研发部门', '研发经理', '总经理']
    lx = [1.55, 4.0, 6.45, 8.65]
    for i, (nm, x) in enumerate(zip(lanes, lx)):
        ax.text(x, 11.15, nm, ha='center', va='center', fontsize=9,
                fontweight='bold', color=DARK)
    ax.plot([0.35, 9.75], [10.85, 10.85], color=DARK, lw=1.2)
    for xb in [2.8, 5.25, 7.6]:
        ax.plot([xb, xb], [0.3, 10.85], color='#C9D6E4', lw=0.7, zorder=1)

    W, H = 2.0, 0.62
    y = [10.15, 9.25, 8.15, 7.05, 6.15, 5.35, 4.35, 3.25, 2.35, 1.45]

    box(ax, lx[0], y[0], W, H, '研发需求')
    box(ax, lx[1], y[1], W, H, '立项')
    box(ax, lx[2], y[1], W, H, '组织评审')
    diamond(ax, lx[3], y[1], 1.7, 0.9, '审批')
    box(ax, lx[1], y[2], W, H, '制定研发计划')
    diamond(ax, lx[2], y[2], 1.7, 0.9, '评审')
    box(ax, lx[1], y[3], W, H, '技术及\n工作图设计')
    diamond(ax, lx[2], y[3], 1.7, 0.9, '评审')
    box(ax, lx[0], y[4], W, H, '试制')
    box(ax, lx[0], y[5], W, H, '测试验证')
    box(ax, lx[1], y[5], W, H, '改进修正')
    diamond(ax, lx[1], y[6], 1.7, 0.9, '确认')
    box(ax, lx[2], y[6], W, H, '组织评审')
    diamond(ax, lx[3], y[6], 1.7, 0.9, '审批')
    box(ax, lx[0], y[7], W, H, '产品认证\n申请专利')
    box(ax, lx[0], y[8], W, H, '批量生产')
    box(ax, lx[1], y[9], W, H, '资料存档')

    arrow(ax, (lx[0] + W / 2, y[0]), (lx[1] - W / 2, y[1] + H / 2 + 0.06))
    arrow(ax, (lx[1] + W / 2, y[1]), (lx[2] - W / 2, y[1]))
    arrow(ax, (lx[2] + W / 2, y[1]), (lx[3] - 0.85, y[1]))
    arrow(ax, (lx[3], y[1] - 0.45), (lx[1] + 0.35, y[2] + H / 2))
    arrow(ax, (lx[1] + W / 2, y[2]), (lx[2] - 0.85, y[2]))
    arrow(ax, (lx[2], y[2] - 0.45), (lx[1] + 0.35, y[3] + H / 2))
    arrow(ax, (lx[1] + W / 2, y[3]), (lx[2] - 0.85, y[3]))
    arrow(ax, (lx[2], y[3] - 0.45), (lx[0] + 0.35, y[4] + H / 2))
    arrow(ax, (lx[0], y[4] - H / 2), (lx[0], y[5] + H / 2))
    arrow(ax, (lx[0] + W / 2, y[5]), (lx[1] - W / 2, y[5]))
    arrow(ax, (lx[1], y[5] - H / 2), (lx[1], y[6] + 0.45))
    arrow(ax, (lx[1] + 0.85, y[6]), (lx[2] - W / 2, y[6]))
    arrow(ax, (lx[2] + W / 2, y[6]), (lx[3] - 0.85, y[6]))
    arrow(ax, (lx[3], y[6] - 0.45), (lx[0] + 0.35, y[7] + H / 2))
    arrow(ax, (lx[0], y[7] - H / 2), (lx[0], y[8] + H / 2))
    arrow(ax, (lx[0], y[8] - H / 2), (lx[1] - 0.35, y[9]))

    fig.tight_layout(pad=0.15)
    fig.savefig(os.path.join(FIG, 'c5_fig1.png'), dpi=210,
                bbox_inches='tight', facecolor='white')
    plt.close(fig)


# ==================== 图2 采购流程 ====================
def fig_buy():
    nodes = [
        ('采购单', '需求部门、采购经理', False),
        ('批准', '采购经理', True),
        ('比价议价', '采购经理', False),
        ('批准（定价）', '总经理', True),
        ('制定采购订单', '采购', False),
        ('发出采购订单', '采购', False),
        ('交期跟进', '采购', False),
        ('物料接收', '仓库', False),
        ('对账', '采购', False),
        ('付款', '采购', False),
    ]
    fig, ax = plt.subplots(figsize=(6.0, 7.2))
    ax.set_xlim(0, 10); ax.set_ylim(0, len(nodes) * 1.16 + 0.5); ax.axis('off')
    ax.text(3.9, len(nodes) * 1.16 + 0.15, '流程', ha='center', fontsize=9,
            fontweight='bold', color=DARK)
    ax.text(7.9, len(nodes) * 1.16 + 0.15, '过程所有者', ha='center', fontsize=9,
            fontweight='bold', color=DARK)
    for i, (t, owner, isd) in enumerate(nodes):
        y = (len(nodes) - i) * 1.16 - 0.55
        if isd:
            diamond(ax, 3.9, y, 2.9, 0.86, t, fs=8.8)
        else:
            box(ax, 3.9, y, 3.1, 0.68, t, fill=DARK if i == 0 else LIGHT,
                fs=9, bold=(i == 0))
        ax.text(7.9, y, owner, ha='center', va='center', fontsize=8.4,
                color='#333333')
        if i < len(nodes) - 1:
            top = 0.43 if isd else 0.34
            nxt = (len(nodes) - i - 1) * 1.16 - 0.55
            nt = 0.43 if nodes[i + 1][2] else 0.34
            arrow(ax, (3.9, y - top), (3.9, nxt + nt))
    y1 = (len(nodes) - 1) * 1.16 - 0.55
    y0 = len(nodes) * 1.16 - 0.55
    ax.plot([2.45, 1.6, 1.6, 2.35], [y1, y1, y0, y0], color=MID, lw=0.9, zorder=2)
    ax.add_patch(FancyArrowPatch((1.7, y0), (2.35, y0), arrowstyle='-|>',
                                 mutation_scale=9, linewidth=0.9, color=MID))
    ax.text(1.32, (y0 + y1) / 2, '否', ha='center', va='center', fontsize=8.2,
            color='#555555')
    fig.tight_layout(pad=0.15)
    fig.savefig(os.path.join(FIG, 'c5_fig2buy.png'), dpi=210,
                bbox_inches='tight', facecolor='white')
    plt.close(fig)


if __name__ == '__main__':
    fig_rd()
    fig_buy()
    print('图已生成')

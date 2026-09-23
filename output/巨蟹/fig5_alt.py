# -*- coding: utf-8 -*-
"""第六章 关节模组需求结构图的三个备选画法。数据与原图一致：

    总量 72.0 万个
    按关节类型  旋转关节 68.0  直线关节 4.0
    按整机归属  国产整机 50.2  境外整机 21.8
"""
import os
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei']
matplotlib.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Wedge

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, 'fig')
os.makedirs(FIG, exist_ok=True)

W_IN = 5.75                       # 版心宽度，作图即插入尺寸
DPI = 300
DARK, MID, SOFT, PALE = '#1F4E79', '#2E75B6', '#9DC3E6', '#DEEBF7'
TXT = '#404A56'
PT_U = 72 * W_IN / 100            # 1 个横向单位折合磅值

TOTAL = 72.0
ROWS = [('按关节类型', [('旋转关节', 68.0, DARK, 'white'),
                        ('直线关节', 4.0, SOFT, TXT)]),
        ('按整机归属', [('国产整机需求', 50.2, MID, 'white'),
                        ('境外整机需求', 21.8, PALE, TXT)])]


def twidth(s, fs):
    return sum(0.55 if ord(c) < 0x2000 else 1.0 for c in s) * fs / PT_U


def _fig(height_u):
    h_in = W_IN * height_u / 100
    fig, ax = plt.subplots(figsize=(W_IN, h_in))
    ax.set_xlim(0, 100); ax.set_ylim(0, height_u)
    ax.axis('off')
    return fig, ax


def _save(fig, name):
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    fig.savefig(os.path.join(FIG, name), dpi=DPI, facecolor='white')
    plt.close(fig)


# ═══════ 方案一：等长百分比堆积条，两种划分上下对照 ═══════
def plan_a(name='fig3_a.png'):
    FS_T, FS_L = 9.5, 8.2
    x0, x1 = 3.0, 97.0
    span = x1 - x0
    BAR, PAD = 6.4, 3.2
    H_T = FS_T * 1.5 / PT_U           # 小标题行高
    H_L = FS_L * 1.5 / PT_U           # 标签行高
    row_h = H_T + 1.4 + BAR + 1.8 + H_L
    YH = PAD + row_h * 2 + 4.6 + 3.4 + H_L + PAD

    fig, ax = _fig(YH)
    y = YH - PAD
    for title, segs in ROWS:
        ax.text(x0, y - H_T / 2, title, ha='left', va='center',
                fontsize=FS_T, color=DARK, fontweight='bold')
        ybar = y - H_T - 1.4 - BAR / 2
        cur = x0
        for nm, v, fc, tc in segs:
            w = span * v / TOTAL
            ax.add_patch(Rectangle((cur, ybar - BAR / 2), w, BAR,
                                   facecolor=fc, edgecolor='white',
                                   linewidth=1.1, zorder=3))
            lab = '%s  %.1f万个  %.0f%%' % (nm, v, v / TOTAL * 100)
            if twidth(lab, FS_L) + 2.4 < w:            # 段宽足够则标于条内
                ax.text(cur + w / 2, ybar, lab, ha='center', va='center',
                        fontsize=FS_L, color=tc, fontweight='bold', zorder=4)
            else:                                       # 否则标于条下右端
                ax.text(x1, ybar - BAR / 2 - 1.8 - H_L / 2, lab,
                        ha='right', va='center', fontsize=FS_L, color=TXT,
                        zorder=4)
            cur += w
        y -= row_h + 4.6

    y += 4.6 - 3.4
    ax.plot([x0, x1], [y, y], color='#D8DFE7', lw=0.8)
    ax.text(x0, y - 1.8 - H_L / 2, '两种划分口径下的需求合计均为 72.0 万个',
            ha='left', va='center', fontsize=FS_L, color=TXT)
    _save(fig, name)


# ═══════ 方案二：等大圆环并列，中心标总量 ═══════
def plan_b(name='fig3_b.png', donut=True):
    FS_T, FS_L = 9.5, 8.2
    R, RIN = 13.2, 7.9
    H_T = FS_T * 1.5 / PT_U
    H_L = FS_L * 1.5 / PT_U
    PAD = 3.0
    YH = PAD + H_T + 2.2 + 2 * R + 3.4 + 2 * H_L + 1.2 + PAD

    fig, ax = _fig(YH)
    ax.set_aspect('equal')
    cy = YH - PAD - H_T - 2.2 - R
    cxs = [26.0, 74.0]

    for cx, (title, segs) in zip(cxs, ROWS):
        ax.text(cx, YH - PAD - H_T / 2, title, ha='center', va='center',
                fontsize=FS_T, color=DARK, fontweight='bold')
        a0 = 90.0
        for nm, v, fc, tc in segs:
            ang = v / TOTAL * 360
            ax.add_patch(Wedge((cx, cy), R, a0 - ang, a0,
                               width=(R - RIN) if donut else None,
                               facecolor=fc, edgecolor='white',
                               linewidth=1.2, zorder=3))
            a0 -= ang
        if donut:
            ax.text(cx, cy + 1.5, '72.0', ha='center', va='center',
                    fontsize=12, color=DARK, fontweight='bold')
            ax.text(cx, cy - 3.4, '万个', ha='center', va='center',
                    fontsize=FS_L, color=TXT)
        for k, (nm, v, fc, tc) in enumerate(segs):
            yy = cy - R - 3.4 - H_L / 2 - k * (H_L + 1.2)
            ax.add_patch(Rectangle((cx - 21.0, yy - 1.3), 2.6, 2.6,
                                   facecolor=fc, edgecolor='#C9D6E4',
                                   linewidth=0.5, zorder=3))
            ax.text(cx - 17.2, yy, nm, ha='left', va='center',
                    fontsize=FS_L, color=TXT)
            ax.text(cx + 21.0, yy, '%.1f万个  %.0f%%' % (v, v / TOTAL * 100),
                    ha='right', va='center', fontsize=FS_L, color=DARK,
                    fontweight='bold')
    _save(fig, name)


# ═══════ 方案三：保留双饼，只规范版式 ═══════
def plan_c(name='fig3_c.png'):
    plan_b(name=name, donut=False)


# ═══════ 方案三（优化）═══════
import math

ROWS_C = [('按关节类型', [('旋转关节', 68.0, DARK, 'white'),
                          ('直线关节', 4.0, SOFT, TXT)]),
          ('按整机归属', [('国产整机需求', 50.2, MID, 'white'),
                          ('境外整机需求', 21.8, '#BDD7EE', TXT)])]


def plan_c2(name='fig3_c2.png'):
    FS_T, FS_L, FS_P = 9.5, 8.2, 9.0
    R = 11.5
    H_T = FS_T * 1.5 / PT_U
    H_L = FS_L * 1.5 / PT_U
    PAD, GAP_L = 3.0, 0.8

    # 图例各列按最长一项定宽，数值与占比分列右对齐
    w_nm = max(twidth(nm, FS_L) for _, sg in ROWS_C for nm, *_ in sg)
    w_vl = max(twidth('%.1f万个' % v, FS_L) for _, sg in ROWS_C for _, v, *_ in sg)
    w_pc = max(twidth('%.0f%%' % (v / TOTAL * 100), FS_L)
               for _, sg in ROWS_C for _, v, *_ in sg)
    SQ, g1, g2, g3 = 2.6, 1.6, 2.6, 2.2
    w_leg = SQ + g1 + w_nm + g2 + w_vl + g3 + w_pc

    YH = PAD + H_T + 2.0 + 2 * R + 3.6 + 2 * H_L + GAP_L + PAD
    fig, ax = _fig(YH)
    ax.set_aspect('equal')
    cy = YH - PAD - H_T - 2.0 - R
    cxs = [26.5, 73.5]

    # 两个口径之间的分隔
    ax.plot([50, 50], [cy - R - 3.0, cy + R + 3.0], color='#E2E8EF',
            lw=0.8, zorder=0)

    for cx, (title, segs) in zip(cxs, ROWS_C):
        ax.text(cx, YH - PAD - H_T / 2, title, ha='center', va='center',
                fontsize=FS_T, color=DARK, fontweight='bold')
        a0 = 90.0
        for nm, v, fc, tc in segs:
            ang = v / TOTAL * 360
            ax.add_patch(Wedge((cx, cy), R, a0 - ang, a0, facecolor=fc,
                               edgecolor='white', linewidth=1.4, zorder=3))
            if ang >= 45:                     # 扇形够大才在图上标占比
                mid = math.radians(a0 - ang / 2)
                ax.text(cx + 0.62 * R * math.cos(mid),
                        cy + 0.62 * R * math.sin(mid),
                        '%.0f%%' % (v / TOTAL * 100), ha='center',
                        va='center', fontsize=FS_P, color=tc,
                        fontweight='bold', zorder=4)
            a0 -= ang
        # 浅色扇形补一圈浅灰描边，避免与白底相融
        ax.add_patch(Wedge((cx, cy), R, 0, 360, facecolor='none',
                           edgecolor='#C9D6E4', linewidth=0.7, zorder=4))

        x_leg = cx - w_leg / 2
        for k, (nm, v, fc, tc) in enumerate(segs):
            yy = cy - R - 3.6 - H_L / 2 - k * (H_L + GAP_L)
            ax.add_patch(Rectangle((x_leg, yy - SQ / 2), SQ, SQ, facecolor=fc,
                                   edgecolor='#C9D6E4', linewidth=0.5, zorder=3))
            ax.text(x_leg + SQ + g1, yy, nm, ha='left', va='center',
                    fontsize=FS_L, color=TXT)
            ax.text(x_leg + SQ + g1 + w_nm + g2 + w_vl, yy, '%.1f万个' % v,
                    ha='right', va='center', fontsize=FS_L, color=DARK,
                    fontweight='bold')
            ax.text(x_leg + w_leg, yy, '%.0f%%' % (v / TOTAL * 100),
                    ha='right', va='center', fontsize=FS_L, color=DARK,
                    fontweight='bold')
    _save(fig, name)


if __name__ == '__main__':
    plan_a(); plan_b(); plan_c()
    print('三方案已生成')


# ═══════ 方案三（再优化）：标签直接上图，去掉图例 ═══════
# 绘制次序使两饼的小扇形分处左上与右上，标注得以各自向外展开
ROWS_D = [('按关节类型', [('旋转关节', 68.0, DARK, 'white'),
                          ('直线关节', 4.0, SOFT, TXT)]),
          ('按整机归属', [('境外整机需求', 21.8, SOFT, TXT),
                          ('国产整机需求', 50.2, DARK, 'white')])]


def plan_d(name='fig3_d.png'):
    FS_T, FS_N, FS_P = 9.5, 8.2, 13.0
    R = 13.5
    H_T = FS_T * 1.5 / PT_U
    PAD = 3.0
    UP = 6.8                                   # 外挂标签高出饼顶的部分
    YH = PAD + H_T + 2.2 + H_T + 1.6 + UP + 2 * R + PAD
    fig, ax = _fig(YH)
    ax.set_aspect('equal')
    cy = PAD + R
    cxs = [26.0, 70.0]

    y_title = cy + R + UP + 1.6 + H_T / 2
    ax.text(50, y_title + H_T / 2 + 2.2 + H_T / 2,
            '2025年关节模组需求合计 72.0 万个', ha='center', va='center',
            fontsize=FS_T, color=DARK, fontweight='bold')

    def stack(x, y, nm, v, tc, ha='center'):
        """名称、占比、数量三行，占比居中放大。"""
        ax.text(x, y + 3.5, nm, ha=ha, va='center', fontsize=FS_N,
                color=tc, zorder=5)
        ax.text(x, y - 0.2, '%.0f%%' % (v / TOTAL * 100), ha=ha, va='center',
                fontsize=FS_P, color=tc, fontweight='bold', zorder=5)
        ax.text(x, y - 3.9, '%.1f万个' % v, ha=ha, va='center', fontsize=FS_N,
                color=tc, zorder=5)

    for cx, (title, segs) in zip(cxs, ROWS_D):
        ax.text(cx, y_title, title, ha='center', va='center', fontsize=FS_T,
                color=DARK, fontweight='bold')
        a0 = 90.0
        for nm, v, fc, tc in segs:
            ang = v / TOTAL * 360
            ax.add_patch(Wedge((cx, cy), R, a0 - ang, a0, facecolor=fc,
                               edgecolor='white', linewidth=1.4, zorder=3))
            mid = math.radians(a0 - ang / 2)
            if ang >= 180:                     # 过半圆，标注置于扇形内
                k = 0.42 if ang >= 300 else 0.50
                stack(cx + k * R * math.cos(mid),
                      cy + k * R * math.sin(mid), nm, v, tc)
            else:                              # 其余引线挑出至饼外
                out = -1 if cx < 50 else 1     # 各自朝版面外侧展开
                x1, y1 = cx + R * math.cos(mid), cy + R * math.sin(mid)
                x2, y2 = cx + 1.16 * R * math.cos(mid), cy + 1.16 * R * math.sin(mid)
                x3 = cx + out * (R + 2.2)
                ax.plot([x1, x2, x3 - out * 0.6], [y1, y2, y2],
                        color='#9AA7B4', lw=0.8, zorder=2)
                stack(x3, y2, nm, v, TXT,
                      ha='right' if out < 0 else 'left')
            a0 -= ang
        ax.add_patch(Wedge((cx, cy), R, 0, 360, facecolor='none',
                           edgecolor='#C9D6E4', linewidth=0.7, zorder=4))
    _save(fig, name)

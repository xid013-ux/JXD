# -*- coding: utf-8 -*-
"""图3（生产工艺流程）三种版式方案，供比选。"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei']
plt.rcParams['axes.unicode_minus'] = False

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, 'fig')
os.makedirs(FIG, exist_ok=True)

DARK, MID = '#1F4E79', '#2E75B6'

# (标题, 宽行说明, 窄行说明)
STEPS = [
    ('原材料准备\n与预处理',
     '特种钢材、合金材料入库检验\n锻件粗加工与退火预处理',
     '特种钢材、合金\n材料入库检验\n锻件粗加工\n与退火预处理'),
    ('核心齿形\n精密车削',
     '柔轮、刚轮外圆与内孔加工\n柔轮齿形精密加工',
     '柔轮、刚轮外圆\n与内孔加工\n柔轮齿形\n精密加工'),
    ('热处理与\n表面处理',
     '真空热处理、渗碳淬火\n防锈防腐涂层处理',
     '真空热处理\n渗碳淬火\n防锈防腐\n涂层处理'),
    ('精密检测',
     '三坐标、齿轮测量中心\n关键尺寸与齿形误差全数检测',
     '三坐标、齿轮\n测量中心\n关键尺寸与齿形\n误差全数检测'),
    ('总成装配与\n传感器集成',
     '无尘车间高精度装配\n驱动器、编码器一体化封装',
     '无尘车间\n高精度装配\n驱动器、编码器\n一体化封装'),
    ('性能测试与\n老化验证',
     '空载与负载跑合、综合性能测试\n高低温及特殊环境适应性测试',
     '空载与负载跑合\n综合性能测试\n高低温及特殊\n环境适应性测试'),
    ('包装入库与\n数字化追溯',
     '成品清洁、防锈包装\n数字化追溯',
     '成品清洁\n防锈包装\n数字化追溯'),
]


def rbox(ax, x, y, w, h, t, fill, fs, tc='#FFFFFF', bold=True):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle='round,pad=0.008,rounding_size=0.018',
                                linewidth=1.0, edgecolor=fill,
                                facecolor=fill, zorder=3))
    ax.text(x, y, t, ha='center', va='center', fontsize=fs, color=tc,
            fontweight='bold' if bold else 'normal', linespacing=1.42, zorder=4)


def varrow(ax, x, y0, y1, lw=1.05):
    ax.add_patch(FancyArrowPatch((x, y0), (x, y1), arrowstyle='-|>',
                                 mutation_scale=9, linewidth=lw,
                                 color=MID, zorder=2))


def harrow(ax, x0, x1, y, lw=1.0):
    ax.add_patch(FancyArrowPatch((x0, y), (x1, y), arrowstyle='-|>',
                                 mutation_scale=9, linewidth=lw,
                                 color=MID, zorder=2))


# ═════════ 方案一：两列纵向，右列拉开使两列等高 ═════════
def plan1():
    fig, ax = plt.subplots(figsize=(6.9, 3.4))
    ax.set_xlim(0, 14); ax.set_ylim(0.1, 8.5); ax.axis('off')
    BW, BH = 2.45, 1.30
    cx = [1.50, 8.35]
    top, bot = 7.10, 1.35
    y1 = [top - i * (top - bot) / 3 for i in range(4)]
    y2 = [top - i * (top - bot) / 2 for i in range(3)]
    for i in range(4):
        t, d, _ = STEPS[i]
        rbox(ax, cx[0], y1[i], BW, BH, f'{i+1}　{t}', DARK, 8.5)
        ax.text(cx[0] + BW / 2 + 0.26, y1[i], d, ha='left', va='center',
                fontsize=7.6, color='#333333', linespacing=1.62)
        if i < 3:
            varrow(ax, cx[0], y1[i] - BH / 2, y1[i + 1] + BH / 2)
    for i in range(3):
        t, d, _ = STEPS[i + 4]
        rbox(ax, cx[1], y2[i], BW, BH, f'{i+5}　{t}', DARK, 8.5)
        ax.text(cx[1] + BW / 2 + 0.26, y2[i], d, ha='left', va='center',
                fontsize=7.6, color='#333333', linespacing=1.62)
        if i < 2:
            varrow(ax, cx[1], y2[i] - BH / 2, y2[i + 1] + BH / 2)
    yb = bot - BH / 2 - 0.52
    ax.plot([cx[0], cx[0], cx[1], cx[1]],
            [bot - BH / 2, yb, yb, top + BH / 2 + 0.46],
            color=MID, lw=1.05, zorder=2, solid_capstyle='round')
    varrow(ax, cx[1], top + BH / 2 + 0.50, top + BH / 2)
    fig.tight_layout(pad=0.1)
    fig.savefig(os.path.join(FIG, 'c5_fig3_p1.png'), dpi=220,
                bbox_inches='tight', facecolor='white')
    plt.close(fig)


# ═════════ 方案二：横向七段，说明置于色块内 ═════════
def plan2():
    fig, ax = plt.subplots(figsize=(6.9, 2.75))
    ax.set_xlim(0, 14); ax.set_ylim(1.86, 5.45); ax.axis('off')
    n, gap, m = 7, 0.26, 0.14
    W = (14 - 2 * m - gap * (n - 1)) / n
    yh, HH = 4.62, 0.98          # 标题条
    yd, HD = 2.98, 1.74          # 说明区
    for i, (t, d_wide, d_narrow) in enumerate(STEPS):
        x = m + W / 2 + i * (W + gap)
        ax.add_patch(FancyBboxPatch((x - W / 2, yd - HD / 2), W, HD,
                                    boxstyle='round,pad=0.006,rounding_size=0.014',
                                    linewidth=0.9, edgecolor='#C9D6E4',
                                    facecolor='#F5F9FD', zorder=1))
        rbox(ax, x, yh, W, HH, t, DARK, 7.8)
        ax.add_patch(Circle((x - W / 2 + 0.18, yh + HH / 2 - 0.02), 0.20,
                            facecolor='#FFFFFF', edgecolor=MID,
                            linewidth=0.9, zorder=5))
        ax.text(x - W / 2 + 0.18, yh + HH / 2 - 0.02, str(i + 1),
                ha='center', va='center', fontsize=6.6, color=DARK,
                fontweight='bold', zorder=6)
        ax.text(x, yd, d_narrow, ha='center', va='center', fontsize=6.5,
                color='#3a3a3a', linespacing=1.72, zorder=3)
        if i < n - 1:
            harrow(ax, x + W / 2 + 0.02, x + W / 2 + gap - 0.02, yh, lw=0.95)
    fig.tight_layout(pad=0.1)
    fig.savefig(os.path.join(FIG, 'c5_fig3_p2.png'), dpi=220,
                bbox_inches='tight', facecolor='white')
    plt.close(fig)


# ═════════ 方案三：蛇形两行，第二行三格均分整行 ═════════
def plan3():
    fig, ax = plt.subplots(figsize=(6.9, 3.2))
    ax.set_xlim(0, 14); ax.set_ylim(0.85, 6.75); ax.axis('off')
    m, gap, HB = 0.30, 0.34, 1.12
    RESV = 0.92                      # 右侧为折回线预留
    W1 = (14 - m - RESV - 3 * gap) / 4
    W2 = (14 - 2 * m - 2 * gap) / 3
    r1 = [m + W1 / 2 + i * (W1 + gap) for i in range(4)]
    r2 = [m + W2 / 2 + i * (W2 + gap) for i in range(3)]
    Y1, Y2 = 5.95, 2.32
    for i in range(4):
        t, d, _ = STEPS[i]
        rbox(ax, r1[i], Y1, W1, HB, f'{i+1}　{t}', DARK, 8.2)
        ax.text(r1[i], Y1 - HB / 2 - 0.26, d, ha='center', va='top',
                fontsize=6.9, color='#3a3a3a', linespacing=1.62)
        if i < 3:
            harrow(ax, r1[i] + W1 / 2 + 0.03, r1[i + 1] - W1 / 2 - 0.03, Y1)
    for i in range(3):
        t, d, _ = STEPS[i + 4]
        rbox(ax, r2[i], Y2, W2, HB, f'{i+5}　{t}', DARK, 8.2)
        ax.text(r2[i], Y2 - HB / 2 - 0.26, d, ha='center', va='top',
                fontsize=6.9, color='#3a3a3a', linespacing=1.62)
        if i < 2:
            harrow(ax, r2[i] + W2 / 2 + 0.03, r2[i + 1] - W2 / 2 - 0.03, Y2)
    xe = r1[3] + W1 / 2
    xr = 14 - RESV / 2
    ymid = 4.02
    ax.plot([xe + 0.14, xr, xr, r2[0], r2[0]],
            [Y1, Y1, ymid, ymid, Y2 + HB / 2 + 0.34],
            color=MID, lw=1.0, zorder=2, solid_capstyle='round')
    varrow(ax, r2[0], Y2 + HB / 2 + 0.38, Y2 + HB / 2)
    fig.tight_layout(pad=0.1)
    fig.savefig(os.path.join(FIG, 'c5_fig3_p3.png'), dpi=220,
                bbox_inches='tight', facecolor='white')
    plt.close(fig)


if __name__ == '__main__':
    plan1(); plan2(); plan3()
    print('三方案已生成')

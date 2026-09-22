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


# 方案四用：(工序, 主要投入, 主要作业内容)
LANE = [
    ('原材料准备与预处理', '特种钢材\n合金材料',
     '入库检验\n锻件粗加工与退火预处理'),
    ('核心齿形精密车削', '柔轮、刚轮胚料',
     '外圆与内孔加工\n柔轮齿形精密加工'),
    ('热处理与表面处理', '',
     '真空热处理、渗碳淬火\n防锈防腐涂层处理'),
    ('精密检测', '',
     '三坐标、齿轮测量中心\n关键尺寸与齿形误差全数检测'),
    ('总成装配与传感器集成', '无框电机、轴承\n驱动器、编码器等',
     '无尘车间高精度装配\n驱动器、编码器一体化封装'),
    ('性能测试与老化验证', '',
     '空载与负载跑合、综合性能测试\n高低温及特殊环境适应性测试'),
    ('包装入库与数字化追溯', '',
     '成品清洁、防锈包装\n数字化追溯'),
]


# ═════════ 方案四：三栏泳道，中置工序主线，左投入右作业 ═════════
def plan4():
    fig, ax = plt.subplots(figsize=(6.9, 3.5))
    ax.set_xlim(0, 14); ax.set_ylim(0.88, 9.52); ax.axis('off')
    cx, BW, BH = 6.49, 4.40, 0.80
    top, step = 8.30, 1.12
    ys = [top - i * step for i in range(7)]
    xl, xr = cx - BW / 2 - 0.30, cx + BW / 2 + 0.30

    # 栏目标题
    yhead = 9.02
    for x, t, ha in ((xl, '主要投入', 'right'), (cx, '生产工序', 'center'),
                     (xr, '主要作业内容', 'left')):
        ax.text(x, yhead, t, ha=ha, va='center', fontsize=8.2,
                color=DARK, fontweight='bold')
    ax.plot([0.25, 13.75], [yhead - 0.36, yhead - 0.36],
            color='#B7C7D8', lw=0.9, zorder=1)
    # 栏间竖向分隔
    for x in (cx - BW / 2 - 0.15, cx + BW / 2 + 0.15):
        ax.plot([x, x], [yhead - 0.36, ys[-1] - BH / 2 - 0.30],
                color='#DCE5EE', lw=0.8, zorder=1)

    for i, (t, sup, act) in enumerate(LANE):
        y = ys[i]
        rbox(ax, cx, y, BW, BH, '%d　%s' % (i + 1, t), DARK, 8.8)
        if sup:
            ax.text(xl - 0.30, y, sup, ha='right', va='center', fontsize=7.8,
                    color='#333333', linespacing=1.55)
            harrow(ax, xl - 0.18, cx - BW / 2 - 0.02, y, lw=0.95)
        ax.text(xr, y, act, ha='left', va='center', fontsize=7.8,
                color='#333333', linespacing=1.55)
        if i < 6:
            varrow(ax, cx, y - BH / 2, ys[i + 1] + BH / 2)
    fig.tight_layout(pad=0.1)
    fig.savefig(os.path.join(FIG, 'c5_fig3_p4.png'), dpi=220,
                bbox_inches='tight', facecolor='white')
    plt.close(fig)


# ═════════ 方案五：按工艺段分组，两段底色区 ═════════
def plan5():
    fig, ax = plt.subplots(figsize=(6.9, 3.45))
    ax.set_xlim(0, 14); ax.set_ylim(0.28, 7.32); ax.axis('off')
    m, gap, HB = 0.34, 0.32, 1.02
    RESV = 0.88
    XR = 14 - RESV                       # 工序框区右界，右侧留作折回通道
    W1 = (XR - m - 3 * gap) / 4
    W2 = (XR - m - 2 * gap) / 3
    r1 = [m + W1 / 2 + i * (W1 + gap) for i in range(4)]
    r2 = [m + W2 / 2 + i * (W2 + gap) for i in range(3)]
    Y1, Y2 = 5.72, 2.06

    def band(yc, label):
        ax.add_patch(FancyBboxPatch((m - 0.16, yc - 1.62), XR + 0.32 - m, 3.06,
                                    boxstyle='round,pad=0.01,rounding_size=0.03',
                                    linewidth=0.9, edgecolor='#C9D6E4',
                                    facecolor='#F5F9FD', zorder=0))
        ax.text(m, yc + 1.12, label, ha='left', va='center',
                fontsize=8.2, color=DARK, fontweight='bold', zorder=1)

    band(Y1, '一、核心零部件加工')
    band(Y2, '二、模组总成与出库')

    for i in range(4):
        t, d, _ = STEPS[i]
        rbox(ax, r1[i], Y1, W1, HB, '%d　%s' % (i + 1, t.replace('\n', '')),
             DARK, 7.6)
        ax.text(r1[i], Y1 - HB / 2 - 0.24, d, ha='center', va='top',
                fontsize=6.9, color='#3a3a3a', linespacing=1.60)
        if i < 3:
            harrow(ax, r1[i] + W1 / 2 + 0.03, r1[i + 1] - W1 / 2 - 0.03, Y1)
    for i in range(3):
        t, d, _ = STEPS[i + 4]
        rbox(ax, r2[i], Y2, W2, HB, '%d　%s' % (i + 5, t.replace('\n', '')),
             DARK, 7.6)
        ax.text(r2[i], Y2 - HB / 2 - 0.24, d, ha='center', va='top',
                fontsize=6.9, color='#3a3a3a', linespacing=1.60)
        if i < 2:
            harrow(ax, r2[i] + W2 / 2 + 0.03, r2[i + 1] - W2 / 2 - 0.03, Y2)

    xe, xj = r1[3] + W1 / 2, XR + 0.16 + (14 - XR - 0.16) / 2
    ymid = 3.80
    ax.plot([xe + 0.12, xj, xj, r2[0], r2[0]],
            [Y1, Y1, ymid, ymid, Y2 + HB / 2 + 0.32],
            color=MID, lw=1.0, zorder=2, solid_capstyle='round')
    varrow(ax, r2[0], Y2 + HB / 2 + 0.36, Y2 + HB / 2)
    fig.tight_layout(pad=0.1)
    fig.savefig(os.path.join(FIG, 'c5_fig3_p5.png'), dpi=220,
                bbox_inches='tight', facecolor='white')
    plt.close(fig)


# ═════════ 方案六：自制线与外购件双线汇合于总成 ═════════
def plan6():
    fig, ax = plt.subplots(figsize=(6.9, 3.15))
    ax.set_xlim(0, 14); ax.set_ylim(0.55, 7.25); ax.axis('off')
    m, gap, HB = 0.32, 0.32, 1.02
    RESV = 0.86
    W1 = (14 - m - RESV - 3 * gap) / 4
    W2 = (14 - 2 * m - 2 * gap) / 3
    r1 = [m + W1 / 2 + i * (W1 + gap) for i in range(4)]
    r2 = [m + W2 / 2 + i * (W2 + gap) for i in range(3)]
    Y1, Y2 = 6.28, 1.92

    for i in range(4):
        t, d, _ = STEPS[i]
        rbox(ax, r1[i], Y1, W1, HB, '%d　%s' % (i + 1, t.replace('\n', '')),
             DARK, 7.6)
        ax.text(r1[i], Y1 - HB / 2 - 0.24, d, ha='center', va='top',
                fontsize=6.9, color='#3a3a3a', linespacing=1.60)
        if i < 3:
            harrow(ax, r1[i] + W1 / 2 + 0.03, r1[i + 1] - W1 / 2 - 0.03, Y1)
    ax.text(m - 0.06, Y1 + HB / 2 + 0.34, '自制：柔轮、刚轮等谐波减速机核心件',
            ha='left', va='center', fontsize=7.4, color=DARK,
            fontweight='bold')

    for i in range(3):
        t, d, _ = STEPS[i + 4]
        rbox(ax, r2[i], Y2, W2, HB, '%d　%s' % (i + 5, t.replace('\n', '')),
             DARK, 7.6)
        ax.text(r2[i], Y2 - HB / 2 - 0.24, d, ha='center', va='top',
                fontsize=6.9, color='#3a3a3a', linespacing=1.60)
        if i < 2:
            harrow(ax, r2[i] + W2 / 2 + 0.03, r2[i + 1] - W2 / 2 - 0.03, Y2)

    # 外购与委外件支线
    bw, bh, bx, by = 3.05, 1.12, 1.60, 4.08
    ax.add_patch(FancyBboxPatch((bx - bw / 2, by - bh / 2), bw, bh,
                                boxstyle='round,pad=0.008,rounding_size=0.02',
                                linewidth=1.0, edgecolor=MID,
                                facecolor='#EAF2FA', zorder=3))
    ax.text(bx, by, '外购与委外件\n无框电机、轴承\n驱动器、编码器等',
            ha='center', va='center', fontsize=6.9, color='#23425F',
            linespacing=1.58, zorder=4)
    varrow(ax, bx, by - bh / 2, Y2 + HB / 2)

    xe, xj = r1[3] + W1 / 2, 14 - RESV / 2
    ymid = 4.08
    xin = 3.55
    ax.plot([xe + 0.12, xj, xj, xin, xin],
            [Y1, Y1, ymid, ymid, Y2 + HB / 2 + 0.32],
            color=MID, lw=1.0, zorder=2, solid_capstyle='round')
    varrow(ax, xin, Y2 + HB / 2 + 0.36, Y2 + HB / 2)
    fig.tight_layout(pad=0.1)
    fig.savefig(os.path.join(FIG, 'c5_fig3_p6.png'), dpi=220,
                bbox_inches='tight', facecolor='white')
    plt.close(fig)


if __name__ == '__main__':
    plan1(); plan2(); plan3()
    plan4(); plan5(); plan6()
    print('六方案已生成')

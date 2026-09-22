# -*- coding: utf-8 -*-
"""第五、六章插图（统一样式版）。内容与原图一致，只改版式与美工。"""
import os
from style import (canvas, save, twidth, wmax, theight, block, pill, numdot,
                   hline, vline, link_v, link_h, tri_d, tri_r,
                   U, PT_U, DARK, MID, LIGHT, PALE, BAND, TXT, RULE, WHITE,
                   FS_H1, FS_BODY, FS_DESC, FS_TICK, LW_RULE, LW_LINK, LW_EDGE)

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, 'fig')
os.makedirs(FIG, exist_ok=True)


# ══════════════ 图3  公司主要产品生产工艺流程 ══════════════
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


def fig3_process(out='c5_fig3.png'):
    names = [t for t, _, _ in LANE]
    sups = [l for _, s, _ in LANE for l in s.split('\n') if l]
    acts = [l for _, _, a in LANE for l in a.split('\n')]

    RDOT = 0.26                                   # 序号圆半径
    HB = 0.88                                     # 色块高，亦为说明底块高
    GAP = 0.22                                    # 行间距
    step = HB + GAP
    PADP = 0.26                                   # 说明底块内左右留白

    # 三栏宽度按各栏最长一行反推
    WL = wmax(sups, FS_DESC)
    WB = 2 * RDOT + 0.30 + wmax(names, FS_BODY) + 0.46
    WR = wmax(acts, FS_DESC) + PADP * 2
    mrg = 0.52
    rest = U - 2 * mrg - (WL + WB + WR)
    assert rest > 1.0, '版心放不下三栏'
    g1, g2 = rest * 0.62, rest * 0.38             # 投入→工序、工序→作业内容

    xl = mrg + WL                                 # 左栏文字右端
    xb0 = xl + g1                                 # 色块左边
    cx = xb0 + WB / 2
    xr0 = xb0 + WB + g2                           # 说明底块左边
    xr1 = U - mrg                                 # 说明底块右边
    v1 = xl + g1 * 0.50                           # 左侧栏分隔线
    v2 = xb0 + WB + g2 * 0.46                     # 右侧栏分隔线

    hh = theight(1, FS_H1, 1.5)
    pad, hgap = 0.22, 0.30
    H = pad + hh + 0.10 + hgap + HB + 6 * step + hgap + pad
    fig, ax = canvas(H)

    # 栏目标题与三段式分隔线：各栏一段，互不相连
    yhead = H - pad - hh / 2
    yrule = yhead - hh / 2 - 0.10
    ybot = yrule - hgap - HB / 2 - 6 * step - HB / 2 - hgap
    for x, t, ha in ((xl, '主要投入', 'right'), (cx, '生产工序', 'center'),
                     (xr0 + PADP, '主要作业内容', 'left')):
        ax.text(x, yhead, t, ha=ha, va='center', fontsize=FS_H1,
                color=DARK, fontweight='bold')
    for x0, x1 in ((mrg, v1 - 0.18), (xb0, xb0 + WB), (xr0, xr1)):
        hline(ax, x0, x1, yrule, color=MID, lw=LW_EDGE, z=2)
        hline(ax, x0, x1, ybot, color=MID, lw=LW_EDGE, z=2)
    ys = [yrule - hgap - HB / 2 - i * step for i in range(7)]

    # 栏间竖线止于上下收口线之间；左侧一条在投入箭头穿过处断开
    vline(ax, v2, ybot, yrule)
    brk = sorted(ys[i] for i in range(7) if LANE[i][1])
    y0 = ybot
    for b in brk:
        vline(ax, v1, y0, b - 0.24)
        y0 = b + 0.24
    vline(ax, v1, y0, yrule)
    for i, (name, sup, act) in enumerate(LANE):
        y = ys[i]
        block(ax, cx, y, WB, HB, '')
        numdot(ax, xb0 + 0.30 + RDOT, y, i + 1, r=RDOT)
        ax.text(xb0 + 0.30 + 2 * RDOT + 0.30, y, name, ha='left', va='center',
                fontsize=FS_BODY, color=WHITE, fontweight='bold', zorder=4)
        pill(ax, xr0, xr1, y, HB, act, pad=PADP)
        if sup:
            ax.text(xl, y, sup, ha='right', va='center', fontsize=FS_DESC,
                    color=TXT, linespacing=1.42)
            link_h(ax, xl + 0.22, xb0 - 0.04, y)
        if i < 6:
            tri_d(ax, cx, y - HB / 2 - (GAP - 0.155) / 2, s=0.10)

    save(fig, os.path.join(FIG, out))
    return out


# ══════════════ 图1  公司研发流程图 ══════════════
def fig1_rd(out='c5_fig1_v2.png'):
    """四泳道结构，节点与连线走向与原图一致，只改样式。"""
    from matplotlib.patches import Polygon, FancyArrowPatch, FancyBboxPatch
    from style import ROUND

    UX = 10.0                                 # 本图横向沿用 0-10 坐标
    lanes = ['相关部门', '产品研发部门', '研发经理', '总经理']
    lx = [1.55, 4.00, 6.45, 8.65]
    vx = [2.80, 5.25, 7.60]
    xa, xz = 0.40, 9.62
    W, HBX = 2.00, 0.78                       # 作业框，单双行等高
    WD, HD = 1.44, 0.80                       # 判断框
    y = [10.15 - i * 0.95 for i in range(10)]

    ytitle, yrule = 11.02, 10.68
    ybot = y[9] - HBX / 2 - 0.34
    H_u = ytitle + 0.44 - (ybot - 0.26)
    fig, ax = canvas(H_u * U / UX)            # 等比：1 横向单位 = 1 纵向单位
    ax.set_xlim(0, UX)
    ax.set_ylim(ybot - 0.26, ytitle + 0.44)

    def nbox(x, yy, text, w=W, h=HBX):
        ax.add_patch(FancyBboxPatch(
            (x - w / 2, yy - h / 2), w, h,
            boxstyle='round,pad=0,rounding_size=%.3f' % (ROUND * UX / U),
            linewidth=0, facecolor=DARK, zorder=3))
        ax.text(x, yy, text, ha='center', va='center', fontsize=FS_BODY,
                color=WHITE, fontweight='bold', linespacing=1.30, zorder=4)

    def dia(x, yy, text):
        ax.add_patch(Polygon(
            [(x, yy + HD / 2), (x + WD / 2, yy), (x, yy - HD / 2),
             (x - WD / 2, yy)], closed=True, linewidth=1.0,
            edgecolor=MID, facecolor=PALE, zorder=3))
        ax.text(x, yy, text, ha='center', va='center', fontsize=FS_BODY,
                color=DARK, fontweight='bold', zorder=4)

    def arw(p0, p1):
        ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle='-|>',
                                     mutation_scale=8, linewidth=LW_LINK,
                                     color=MID, zorder=2, shrinkA=0, shrinkB=0))

    # 泳道标题与分段收口线
    for nm, x in zip(lanes, lx):
        ax.text(x, ytitle, nm, ha='center', va='center', fontsize=FS_H1,
                color=DARK, fontweight='bold')
    edges = [xa] + vx + [xz]
    for a, z in zip(edges[:-1], edges[1:]):
        ax.plot([a + 0.10, z - 0.10], [yrule, yrule], color=MID,
                lw=LW_EDGE, zorder=2, solid_capstyle='butt')
        ax.plot([a + 0.10, z - 0.10], [ybot, ybot], color=MID,
                lw=LW_EDGE, zorder=2, solid_capstyle='butt')
    for x in vx:
        ax.plot([x, x], [ybot, yrule], color='#C9D6E4', lw=LW_RULE, zorder=1,
                solid_capstyle='butt')

    nbox(lx[0], y[0], '研发需求')
    nbox(lx[1], y[1], '立项')
    nbox(lx[2], y[1], '组织评审')
    dia(lx[3], y[1], '审批')
    nbox(lx[1], y[2], '制定研发计划')
    dia(lx[2], y[2], '评审')
    nbox(lx[1], y[3], '技术及\n工作图设计')
    dia(lx[2], y[3], '评审')
    nbox(lx[0], y[4], '试制')
    nbox(lx[0], y[5], '测试验证')
    nbox(lx[1], y[5], '改进修正')
    dia(lx[1], y[6], '确认')
    nbox(lx[2], y[6], '组织评审')
    dia(lx[3], y[6], '审批')
    nbox(lx[0], y[7], '产品认证\n申请专利')
    nbox(lx[0], y[8], '批量生产')
    nbox(lx[1], y[9], '资料存档')

    hb, hd = HBX / 2, HD / 2
    arw((lx[0] + W / 2, y[0]), (lx[1] - W / 2, y[1] + hb + 0.06))
    arw((lx[1] + W / 2, y[1]), (lx[2] - W / 2, y[1]))
    arw((lx[2] + W / 2, y[1]), (lx[3] - WD / 2, y[1]))
    arw((lx[3], y[1] - hd), (lx[1] + 0.35, y[2] + hb))
    arw((lx[1] + W / 2, y[2]), (lx[2] - WD / 2, y[2]))
    arw((lx[2], y[2] - hd), (lx[1] + 0.35, y[3] + hb))
    arw((lx[1] + W / 2, y[3]), (lx[2] - WD / 2, y[3]))
    arw((lx[2], y[3] - hd), (lx[0] + 0.35, y[4] + hb))
    arw((lx[0], y[4] - hb), (lx[0], y[5] + hb))
    arw((lx[0] + W / 2, y[5]), (lx[1] - W / 2, y[5]))
    arw((lx[1], y[5] - hb), (lx[1], y[6] + hd))
    arw((lx[1] + WD / 2, y[6]), (lx[2] - W / 2, y[6]))
    arw((lx[2] + W / 2, y[6]), (lx[3] - WD / 2, y[6]))
    arw((lx[3], y[6] - hd), (lx[0] + 0.35, y[7] + hb))
    arw((lx[0], y[7] - hb), (lx[0], y[8] + hb))
    arw((lx[0], y[8] - hb), (lx[1] - 0.35, y[9] + hb))

    save(fig, os.path.join(FIG, out))
    return out


if __name__ == '__main__':
    print('已生成', fig3_process(), fig1_rd())

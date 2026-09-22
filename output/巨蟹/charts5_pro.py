# -*- coding: utf-8 -*-
"""图3（生产工艺流程）版式重做。

工序名称与说明文字与原图完全一致，只改版式与美工。
画布宽度直接取版心 5.75 英寸，图内字号即为文档中的实际字号；
所有色条、栏宽均按文字实际渲染宽度反推，不靠目测。
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon

plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei']
plt.rcParams['axes.unicode_minus'] = False

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, 'fig')
os.makedirs(FIG, exist_ok=True)

W_IN = 5.75                      # 版心宽度
U = 14.0                         # 横向坐标单位数
PT_U = 72 * W_IN / U             # 每单位折合磅值
DARK = '#1F4E79'
MID = '#2E75B6'
TXT = '#55606D'
RULE = '#DFE6EE'
BAND = '#F6F9FC'

NAMES = ['原材料准备与预处理', '核心齿形精密车削', '热处理与表面处理',
         '精密检测', '总成装配与传感器集成', '性能测试与老化验证',
         '包装入库与数字化追溯']

# 原图说明合并为单行（方案七用）
DESC_LINE = [
    '特种钢材、合金材料入库检验；锻件粗加工与退火预处理',
    '柔轮、刚轮外圆与内孔加工；柔轮齿形精密加工',
    '真空热处理、渗碳淬火；防锈防腐涂层处理',
    '三坐标、齿轮测量中心；关键尺寸与齿形误差全数检测',
    '无尘车间高精度装配；驱动器、编码器一体化封装',
    '空载与负载跑合、综合性能测试；高低温及特殊环境适应性测试',
    '成品清洁、防锈包装；数字化追溯',
]

# 原图说明按窄列断行（方案八用，每行不超过 12 字）
DESC_N = [
    '特种钢材、合金材料\n入库检验\n锻件粗加工与退火预处理',
    '柔轮、刚轮外圆与内孔加工\n柔轮齿形精密加工',
    '真空热处理、渗碳淬火\n防锈防腐涂层处理',
    '三坐标、齿轮测量中心\n关键尺寸与齿形\n误差全数检测',
    '无尘车间高精度装配\n驱动器、编码器一体化封装',
    '空载与负载跑合、\n综合性能测试\n高低温及特殊环境\n适应性测试',
    '成品清洁、防锈包装\n数字化追溯',
]

# 原图说明保持两行（方案九用）
DESC_2L = [
    '特种钢材、合金材料入库检验\n锻件粗加工与退火预处理',
    '柔轮、刚轮外圆与内孔加工\n柔轮齿形精密加工',
    '真空热处理、渗碳淬火\n防锈防腐涂层处理',
    '三坐标、齿轮测量中心\n关键尺寸与齿形误差全数检测',
    '无尘车间高精度装配\n驱动器、编码器一体化封装',
    '空载与负载跑合、综合性能测试\n高低温及特殊环境适应性测试',
    '成品清洁、防锈包装\n数字化追溯',
]


def twidth(s, fs):
    """估算一行文字的渲染宽度（单位 u）：中文全角计 1 字宽，半角计 0.55。"""
    n = sum(0.55 if ord(c) < 0x2000 else 1.0 for c in s)
    return n * fs / PT_U


def wmax(lines, fs):
    return max(twidth(x, fs) for x in lines)


def canvas(height_u):
    fig, ax = plt.subplots(figsize=(W_IN, W_IN * height_u / U))
    ax.set_xlim(0, U)
    ax.set_ylim(0, height_u)
    ax.axis('off')
    return fig, ax


def bar(ax, x, y, w, h, text, fs):
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h,
                           facecolor=DARK, edgecolor='none', zorder=3))
    ax.text(x, y, text, ha='center', va='center', fontsize=fs,
            color='#FFFFFF', fontweight='bold', linespacing=1.34, zorder=4)


def tri_r(ax, x, y, s=0.15):
    ax.add_patch(Polygon([[x, y + s], [x + s * 1.6, y], [x, y - s]],
                         closed=True, facecolor=MID, edgecolor='none',
                         zorder=4))


def tri_d(ax, x, y, s=0.15):
    ax.add_patch(Polygon([[x - s, y], [x + s, y], [x, y - s * 1.6]],
                         closed=True, facecolor=MID, edgecolor='none',
                         zorder=4))


# ═════════ 方案七：清单式，序号—工序—说明三列对齐 ═════════
def plan7():
    FS_NAME, FS_DESC = 9.5, 8.0
    n, rh, pad = 7, 0.84, 0.24
    x0, x1 = 0.18, 13.82
    wnum = 0.80
    xname = x0 + wnum + 0.26
    xdesc = xname + wmax(NAMES, FS_NAME) + 0.62
    assert xdesc + wmax(DESC_LINE, FS_DESC) < x1 - 0.1, '说明栏溢出'

    H = n * rh + pad * 2
    fig, ax = canvas(H)
    top = H - pad
    for i in range(n):
        yc = top - (i + 0.5) * rh
        if i % 2 == 0:
            ax.add_patch(Rectangle((x0, yc - rh / 2), x1 - x0, rh,
                                   facecolor=BAND, edgecolor='none', zorder=0))
        if i < n - 1:
            ax.plot([x0 + wnum / 2, x0 + wnum / 2],
                    [yc - 0.25, yc - rh + 0.25], color='#B9CADB',
                    lw=0.8, zorder=1)
        ax.add_patch(Rectangle((x0, yc - 0.25), wnum, 0.50,
                               facecolor=DARK, edgecolor='none', zorder=3))
        ax.text(x0 + wnum / 2, yc, str(i + 1), ha='center', va='center',
                fontsize=9.0, color='#FFFFFF', fontweight='bold', zorder=4)
        ax.text(xname, yc, NAMES[i], ha='left', va='center',
                fontsize=FS_NAME, color=DARK, fontweight='bold')
        ax.text(xdesc, yc, DESC_LINE[i], ha='left', va='center',
                fontsize=FS_DESC, color=TXT)

    ax.plot([xdesc - 0.31, xdesc - 0.31],
            [top - n * rh + 0.12, top - 0.12], color=RULE, lw=0.8, zorder=1)
    for y in (top, top - n * rh):
        ax.plot([x0, x1], [y, y], color=DARK, lw=1.1, zorder=2)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    fig.savefig(os.path.join(FIG, 'c5_fig3_p7.png'), dpi=300,
                facecolor='white')
    plt.close(fig)


# ═════════ 方案八：四三分行，色条等宽，次行居中 ═════════
def plan8():
    FS_NAME, FS_DESC = 7.8, 7.6
    labels = list(NAMES)                    # 顺序由箭头表达，色条内不再放序号
    HB, pad, mid = 0.70, 0.22, 0.86
    BW = wmax(labels, FS_NAME) + 0.30
    # 首行四列、次行三列分别按整幅等分定位，说明文字可用整格宽度
    c1 = [U * (2 * i + 1) / 8 for i in range(4)]
    c2 = [U * (2 * i + 1) / 6 for i in range(3)]
    # 首行窄、次行宽，各按本行格宽断行
    d1, d2 = DESC_N[:4], DESC_2L[4:]
    assert BW < U / 4 - 0.30, '色条宽超出首行格宽'
    assert wmax([l for d in d1 for l in d.split('\n')],
                FS_DESC) < U / 4 - 0.40, '说明宽超出首行格宽'
    assert wmax([l for d in d2 for l in d.split('\n')],
                FS_DESC) < U / 3 - 0.40, '说明宽超出次行格宽'

    n1 = max(d.count('\n') for d in d1) + 1
    n2 = max(d.count('\n') for d in d2) + 1
    dh1, dh2 = n1 * FS_DESC * 1.52 / PT_U, n2 * FS_DESC * 1.52 / PT_U
    H = pad * 2 + (HB + 0.18 + dh1) + mid + (HB + 0.18 + dh2)
    fig, ax = canvas(H)
    Y1 = H - pad - HB / 2
    Y2 = pad + dh2 + 0.18 + HB / 2

    for i in range(4):
        bar(ax, c1[i], Y1, BW, HB, labels[i], FS_NAME)
        ax.text(c1[i], Y1 - HB / 2 - 0.18, d1[i], ha='center', va='top',
                fontsize=FS_DESC, color=TXT, linespacing=1.52)
        if i < 3:
            tri_r(ax, c1[i] + BW / 2 + 0.06, Y1)
    for i in range(3):
        bar(ax, c2[i], Y2, BW, HB, labels[i + 4], FS_NAME)
        ax.text(c2[i], Y2 - HB / 2 - 0.18, d2[i], ha='center',
                va='top', fontsize=FS_DESC, color=TXT, linespacing=1.52)
        if i < 2:
            tri_r(ax, c2[i] + BW / 2 + 0.06, Y2)

    # 折回线自工序四正下方引出，不占用版心右侧
    ytop = Y1 - HB / 2 - 0.18 - dh1 - 0.18
    ymid = (ytop + Y2 + HB / 2 + 0.30) / 2
    ax.plot([c1[3], c1[3], c2[0], c2[0]],
            [ytop, ymid, ymid, Y2 + HB / 2 + 0.30],
            color=MID, lw=0.9, zorder=2, solid_capstyle='butt')
    tri_d(ax, c2[0], Y2 + HB / 2 + 0.30)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    fig.savefig(os.path.join(FIG, 'c5_fig3_p8.png'), dpi=300,
                facecolor='white')
    plt.close(fig)


# ═════════ 方案九：双栏条目式，序号在前说明在下 ═════════
def plan9():
    FS_NAME, FS_DESC = 9.0, 8.4
    mrg, mid = 0.22, 0.62
    CW = (U - mrg * 2 - mid) / 2
    colx = [mrg, mrg + CW + mid]
    wnum = 0.62
    assert wnum + 0.24 + wmax(NAMES, FS_NAME) < CW, '工序名溢出栏宽'
    assert wmax([l for d in DESC_2L for l in d.split('\n')],
                FS_DESC) < CW - wnum - 0.24, '说明溢出栏宽'

    dh = 2 * FS_DESC * 1.44 / PT_U
    blk = 0.46 + 0.16 + dh                  # 标题行 + 间隔 + 两行说明
    step = blk + 0.34
    pad = 0.24
    H = pad * 2 + 4 * step - 0.34
    fig, ax = canvas(H)
    top = H - pad

    ax.plot([mrg + CW + mid / 2, mrg + CW + mid / 2],
            [pad + 0.05, top - 0.05], color=RULE, lw=0.8, zorder=0)

    for c in (0, 1):
        idx = list(range(4)) if c == 0 else list(range(4, 7))
        for k, i in enumerate(idx):
            yt = top - k * step
            xb = colx[c]
            ax.add_patch(Rectangle((xb, yt - 0.46), wnum, 0.46,
                                   facecolor=DARK, edgecolor='none', zorder=3))
            ax.text(xb + wnum / 2, yt - 0.23, str(i + 1), ha='center',
                    va='center', fontsize=8.6, color='#FFFFFF',
                    fontweight='bold', zorder=4)
            ax.text(xb + wnum + 0.24, yt - 0.23, NAMES[i], ha='left',
                    va='center', fontsize=FS_NAME, color=DARK,
                    fontweight='bold')
            ax.text(xb + wnum + 0.24, yt - 0.46 - 0.16, DESC_2L[i],
                    ha='left', va='top', fontsize=FS_DESC, color=TXT,
                    linespacing=1.44)
            ax.plot([xb, xb + CW], [yt - blk - 0.14, yt - blk - 0.14],
                    color=RULE, lw=0.7, zorder=1)
            if k < len(idx) - 1:
                ax.plot([xb + wnum / 2, xb + wnum / 2],
                        [yt - blk - 0.14, yt - step],
                        color='#B9CADB', lw=0.8, zorder=1)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    fig.savefig(os.path.join(FIG, 'c5_fig3_p9.png'), dpi=300,
                facecolor='white')
    plt.close(fig)


# (工序, 主要投入, 主要作业内容)
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


# ═════════ 方案四（优化）：三栏泳道，中置工序主线 ═════════
def plan10():
    FS_HEAD, FS_NAME, FS_DESC = 9.0, 9.5, 8.2
    HB, LS = 0.72, 1.45
    labels = ['%d　%s' % (i + 1, t) for i, (t, _, _) in enumerate(LANE)]
    sup = [l for _, s, _ in LANE for l in s.split('\n') if l]
    act = [l for _, _, a in LANE for l in a.split('\n')]

    # 三栏宽度按各自最长一行反推，余量均分给栏间距与左右边距
    WL = wmax(sup, FS_DESC)
    WB = wmax(labels, FS_NAME) + 0.60
    WR = wmax(act, FS_DESC)
    mrg = 0.86                                # 左右边距固定，余量按比例分给两处栏间距
    rest = U - 2 * mrg - (WL + WB + WR)
    assert rest > 1.2, '版心放不下三栏'
    g1, g2 = rest * 1.30 / 2.20, rest * 0.90 / 2.20

    xl = mrg + WL                             # 左栏文字右端
    xb0 = xl + g1                             # 工序框左边
    cx = xb0 + WB / 2
    xr = xb0 + WB + g2                        # 右栏文字左端

    step = 2 * FS_DESC * LS / PT_U + 0.22
    pad, hgap = 0.24, 0.26
    H = pad + FS_HEAD * 1.5 / PT_U + 0.06 + hgap + HB + 6 * step + hgap + pad
    fig, ax = canvas(H)

    yhead = H - pad - FS_HEAD * 1.5 / PT_U / 2
    yline = yhead - FS_HEAD * 1.5 / PT_U / 2 - 0.06
    ax.text(xl, yhead, '主要投入', ha='right', va='center',
            fontsize=FS_HEAD, color=DARK, fontweight='bold')
    ax.text(cx, yhead, '生产工序', ha='center', va='center',
            fontsize=FS_HEAD, color=DARK, fontweight='bold')
    ax.text(xr, yhead, '主要作业内容', ha='left', va='center',
            fontsize=FS_HEAD, color=DARK, fontweight='bold')

    ys = [yline - hgap - HB / 2 - i * step for i in range(7)]
    for i, (t, s, a) in enumerate(LANE):
        y = ys[i]
        bar(ax, cx, y, WB, HB, labels[i], FS_NAME)
        if s:
            ax.text(xl, y, s, ha='right', va='center', fontsize=FS_DESC,
                    color=TXT, linespacing=LS)
            ax.plot([xl + 0.20, xb0 - 0.19], [y, y], color=MID, lw=0.9,
                    zorder=2)
            tri_r(ax, xb0 - 0.19, y, 0.11)
        ax.text(xr, y, a, ha='left', va='center', fontsize=FS_DESC,
                color=TXT, linespacing=LS)
        if i < 6:
            tri_d(ax, cx, y - HB / 2 - (step - HB) / 2 + 0.09, 0.11)

    for y in (yline, ys[-1] - HB / 2 - hgap):
        ax.plot([mrg, U - mrg], [y, y], color=DARK, lw=1.0, zorder=2)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    fig.savefig(os.path.join(FIG, 'c5_fig3_p10.png'), dpi=300,
                facecolor='white')
    plt.close(fig)


if __name__ == '__main__':
    plan7(); plan8(); plan9(); plan10()
    print('已生成')

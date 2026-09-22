# -*- coding: utf-8 -*-
"""第五章 图3 公司主要产品生产工艺流程。

画布宽度取版心 5.75 英寸，插入文档时亦按 5.75 英寸满宽，
图内标注的字号即为印在纸上的字号。
三栏宽度按各栏文字的实际渲染宽度反推，不靠目测。
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


# ═════════ 三栏泳道：中置工序主线，左投入右作业 ═════════
def fig_process():
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
    fig.savefig(os.path.join(FIG, 'c5_fig3.png'), dpi=300,
                facecolor='white')
    plt.close(fig)

if __name__ == '__main__':
    fig_process()
    print('已生成 c5_fig3.png')

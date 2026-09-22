# -*- coding: utf-8 -*-
"""第五、六章插图统一样式。

统一基准
    画布宽度一律等于版心 5.75 英寸，插入文档时亦按 5.75 英寸满宽，
    缩放系数恒为 1，图内标注的字号即为印在纸上的字号。
    横向坐标一律 0-14 个单位，1 个单位 = 29.571 磅。

字号阶梯
    受 Word 图题（宋体加粗 10.5pt）约束，图内任何文字不得触及该字号。
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon

# ---------- 基准 ----------
W_IN = 5.75                      # 版心宽度（英寸）
U = 14.0                         # 横向单位数
PT_U = 72 * W_IN / U             # 每单位折合磅值 = 29.571
DPI = 300

# ---------- 字体 ----------
FONT = 'Noto Sans CJK SC'


def setup():
    """注册字体。思源黑体含常规与加粗两个字重，加粗方能生效。"""
    if not any(f.name == FONT for f in fm.fontManager.ttflist):
        fm._load_fontmanager(try_read_cache=False)
    plt.rcParams['font.sans-serif'] = [FONT, 'WenQuanYi Zen Hei']
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['axes.unicode_minus'] = False


# ---------- 字号 ----------
FS_H1 = 10.0                     # 栏目标题、坐标轴标题
FS_BODY = 9.5                    # 色块内主体文字
FS_DESC = 8.2                    # 说明文字、数值标签
FS_TICK = 7.5                    # 刻度、脚注、单位

# ---------- 配色 ----------
DARK = '#1F4E79'                 # 主色：色块底、标题字
MID = '#2E75B6'                  # 辅色：连接线、箭头、序号圆
LIGHT = '#8FB4D9'                # 浅辅色：次级数据系列
PALE = '#EAF2FA'                 # 说明底块
BAND = '#F6F9FC'                 # 隔行底纹
TXT = '#55606D'                  # 说明文字
RULE = '#DFE6EE'                 # 分隔线
WHITE = '#FFFFFF'

# ---------- 线宽 ----------
LW_RULE = 0.8                    # 分栏线、网格线
LW_LINK = 0.9                    # 流程连接线
LW_EDGE = 1.0                    # 收口线、轴线

# ---------- 圆角 ----------
ROUND = 0.055                    # 约 1.6 磅


def canvas(height_u):
    """按统一基准开画布。height_u 为纵向单位数。"""
    setup()
    fig, ax = plt.subplots(figsize=(W_IN, W_IN * height_u / U))
    ax.set_xlim(0, U)
    ax.set_ylim(0, height_u)
    ax.axis('off')
    return fig, ax


def save(fig, path):
    """输出精确等于版心宽度，不作裁剪，以免各图缩放系数不一。"""
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    fig.savefig(path, dpi=DPI, facecolor='white')
    plt.close(fig)


def twidth(s, fs):
    """估算一行文字的渲染宽度（单位 u）：全角计 1 字宽，半角计 0.55。"""
    return sum(0.55 if ord(c) < 0x2000 else 1.0 for c in s) * fs / PT_U


def wmax(lines, fs):
    return max(twidth(x, fs) for x in lines)


def theight(nline, fs, ls=1.42):
    """估算多行文字的高度（单位 u）。"""
    return nline * fs * ls / PT_U


# ---------- 图元 ----------
def block(ax, x, y, w, h, text, fs=FS_BODY, fill=DARK, tc=WHITE,
          bold=True, ls=1.34, align='center', z=3):
    """圆角实心色块。align 为 center 时文字居中，left 时左对齐留出序号位。"""
    ax.add_patch(FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle='round,pad=0,rounding_size=%.3f' % ROUND,
        linewidth=0, edgecolor='none', facecolor=fill, zorder=z))
    if text:
        ax.text(x, y, text, ha='center', va='center', fontsize=fs, color=tc,
                fontweight='bold' if bold else 'normal', linespacing=ls,
                zorder=z + 1)


def pill(ax, x0, x1, y, h, text, fs=FS_DESC, fill=PALE, tc=TXT,
         pad=0.24, ls=1.42, z=1):
    """浅色圆角底块 + 左对齐说明文字。与主色块等高、中心对齐。"""
    ax.add_patch(FancyBboxPatch(
        (x0, y - h / 2), x1 - x0, h,
        boxstyle='round,pad=0,rounding_size=%.3f' % ROUND,
        linewidth=0, edgecolor='none', facecolor=fill, zorder=z))
    ax.text(x0 + pad, y, text, ha='left', va='center', fontsize=fs,
            color=tc, linespacing=ls, zorder=z + 1)


def numdot(ax, x, y, n, r=0.26, fill=MID, tc=WHITE, fs=8.5, z=5):
    """序号圆点。置于色块内左侧。"""
    ax.add_patch(Circle((x, y), r, facecolor=fill, edgecolor='none', zorder=z))
    ax.text(x, y, str(n), ha='center', va='center', fontsize=fs, color=tc,
            fontweight='bold', zorder=z + 1)


def tri_d(ax, x, y, s=0.12, color=MID, z=4):
    """朝下的小三角，y 为顶边所在高度。"""
    ax.add_patch(Polygon([[x - s, y], [x + s, y], [x, y - s * 1.55]],
                         closed=True, facecolor=color, edgecolor='none',
                         zorder=z))


def tri_r(ax, x, y, s=0.12, color=MID, z=4):
    """朝右的小三角，x 为左边所在位置。"""
    ax.add_patch(Polygon([[x, y + s], [x, y - s], [x + s * 1.55, y]],
                         closed=True, facecolor=color, edgecolor='none',
                         zorder=z))


def hline(ax, x0, x1, y, color=RULE, lw=LW_RULE, z=1):
    ax.plot([x0, x1], [y, y], color=color, lw=lw, zorder=z,
            solid_capstyle='butt')


def vline(ax, x, y0, y1, color=RULE, lw=LW_RULE, z=1):
    ax.plot([x, x], [y0, y1], color=color, lw=lw, zorder=z,
            solid_capstyle='butt')


def link_v(ax, x, y0, y1, lw=LW_LINK, color=MID, z=2):
    """自上而下的连接线，末端带三角。"""
    ax.plot([x, x], [y0, y1 + 0.02], color=color, lw=lw, zorder=z,
            solid_capstyle='butt')
    tri_d(ax, x, y1 + 0.02, color=color, z=z + 1)


def link_h(ax, x0, x1, y, lw=LW_LINK, color=MID, z=2):
    """自左而右的连接线，末端带三角。"""
    ax.plot([x0, x1 - 0.02], [y, y], color=color, lw=lw, zorder=z,
            solid_capstyle='butt')
    tri_r(ax, x1 - 0.02, y, color=color, z=z + 1)

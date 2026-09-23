# -*- coding: utf-8 -*-
"""第六章配图五张。配色取模板正文的深蓝系，图内文字用黑体类字体。

图一 机器人产业链结构与公司所处环节
图二 人形机器人硬件成本结构
图三 2025年全球人形机器人关节模组需求结构
图四 全球谐波减速机产能
图五 人形机器人单机成本与人工成本
"""
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei']
matplotlib.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Wedge
import math
import os

P = ['#1F4E79', '#2E75B6', '#9DC3E6', '#BDD7EE', '#DEEBF7']
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fig')
os.makedirs(D, exist_ok=True)


def _clean(ax):
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.grid(axis='y', linestyle='--', color='#DDDDDD', linewidth=.7)
    ax.set_axisbelow(True)


def _box(ax, x, y, w, h, text, fc, ec, fs=10.5, tc='#000000', bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle='round,pad=0.008,rounding_size=0.012',
                                facecolor=fc, edgecolor=ec, linewidth=.9))
    ax.text(x + w / 2, y + h / 2, text, ha='center', va='center',
            fontsize=fs, color=tc, linespacing=1.5,
            fontweight='bold' if bold else 'normal')


# ---------- 图一 产业链结构 ----------
fig, ax = plt.subplots(figsize=(7.8, 3.5))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')

# 三层标题带
for x, lab in ((0.02, '上游'), (0.29, '本环节（公司产品）'), (0.79, '下游')):
    ax.text(x + 0.085, 0.95, lab, ha='center', va='center',
            fontsize=11.5, color=P[0], fontweight='bold')

# 上游
_box(ax, 0.02, 0.62, 0.17, 0.22, '金属材料及\n工程材料', P[4], P[2])
_box(ax, 0.02, 0.37, 0.17, 0.22, '轴承', P[4], P[2])
_box(ax, 0.02, 0.12, 0.17, 0.22, '电子元器件', P[4], P[2])

# 本环节
_box(ax, 0.275, 0.62, 0.18, 0.22, '谐波减速机', P[2], P[1])
_box(ax, 0.275, 0.37, 0.18, 0.22, '驱动器\n编码器', P[2], P[1])
_box(ax, 0.275, 0.12, 0.18, 0.22, '力传感器组件', P[2], P[1])
_box(ax, 0.515, 0.32, 0.155, 0.42, '一体化\n关节模组', P[0], P[0], fs=11,
     tc='#FFFFFF', bold=True)

# 下游
_box(ax, 0.755, 0.66, 0.225, 0.18, '人形机器人', P[3], P[1])
_box(ax, 0.755, 0.44, 0.225, 0.18, '协作机器人及\n工业机器人', P[3], P[1])
_box(ax, 0.755, 0.22, 0.225, 0.18, '医疗康复、低空经济\n精密制造等', P[3], P[1], fs=9.5)

# 箭头
for y in (0.73, 0.48, 0.23):
    ax.add_patch(FancyArrowPatch((0.195, y), (0.27, y),
                                 arrowstyle='-|>', mutation_scale=11,
                                 color='#9DC3E6', linewidth=1.1))
for y in (0.73, 0.48, 0.23):
    ax.add_patch(FancyArrowPatch((0.46, y), (0.512, 0.53),
                                 arrowstyle='-|>', mutation_scale=11,
                                 color='#2E75B6', linewidth=1.1,
                                 connectionstyle='arc3,rad=0.08'))
for y in (0.75, 0.53, 0.31):
    ax.add_patch(FancyArrowPatch((0.673, 0.53), (0.75, y),
                                 arrowstyle='-|>', mutation_scale=11,
                                 color='#2E75B6', linewidth=1.1,
                                 connectionstyle='arc3,rad=-0.08'))
fig.tight_layout()
fig.savefig(D + '/fig1.png', dpi=220, bbox_inches='tight')
plt.close(fig)

# ---------- 图二 人形机器人硬件成本结构 ----------
fig, ax = plt.subplots(figsize=(7.2, 2.9))
items = [('执行器', 40, 60), ('感知系统', 10, 20), ('计算与控制平台', 10, 15),
         ('结构件', 5, 10), ('电池模组', 5, 10)]
ypos = range(len(items))[::-1]
for i, (name, lo, hi) in zip(ypos, items):
    ax.barh(i, hi - lo, left=lo, height=0.5,
            color=P[0] if name == '执行器' else P[2],
            edgecolor='#FFFFFF', linewidth=.6)
    ax.text(hi + 1.2, i, f'{lo}%–{hi}%', va='center', fontsize=9.5,
            color=P[0] if name == '执行器' else '#333333')
ax.set_yticks(list(ypos))
ax.set_yticklabels([n for n, _, _ in items], fontsize=10)
ax.set_xlabel('占整机物料成本的比重（%）', fontsize=9.5)
ax.set_xlim(0, 72)
for s in ('top', 'right', 'left'):
    ax.spines[s].set_visible(False)
ax.grid(axis='x', linestyle='--', color='#DDDDDD', linewidth=.7)
ax.set_axisbelow(True)
ax.tick_params(axis='y', length=0)
fig.tight_layout()
fig.savefig(D + '/fig2.png', dpi=220, bbox_inches='tight')
plt.close(fig)

# ---------- 图三 关节模组需求结构 ----------
# 画布宽度即插入宽度（5.70 英寸），横向坐标 0-100，故图内字号即纸上字号，
# 与本章其余各图缩放后的实际字号取齐：小标题 7.5pt、正文 7.3pt。
_W_IN, _PT_U = 5.70, 72 * 5.70 / 100
_FS_T, _FS_N, _FS_P = 7.5, 7.3, 10.0
_TOTAL, _R, _PAD, _UP = 72.0, 15.0, 3.0, 6.8
_TXT = '#404A56'
# 绘制次序使两饼的小扇形分处左上与右上，标注得以各自向外展开
_GRP = [('按关节类型', [('旋转关节', 68.0, P[0], 'white'),
                        ('直线关节', 4.0, P[2], _TXT)]),
        ('按整机归属', [('境外整机需求', 21.8, P[2], _TXT),
                        ('国产整机需求', 50.2, P[0], 'white')])]


def _tw(t, fs):
    """估算一行文字的渲染宽度（坐标单位）：全角计 1 字宽，半角计 0.55。"""
    return sum(0.55 if ord(c) < 0x2000 else 1.0 for c in t) * fs / _PT_U


_H_T = _FS_T * 1.5 / _PT_U
_YH = _PAD + _H_T + 2.2 + _H_T + 1.6 + _UP + 2 * _R + _PAD
fig, ax = plt.subplots(figsize=(_W_IN, _W_IN * _YH / 100))
ax.set_xlim(0, 100); ax.set_ylim(0, _YH); ax.axis('off'); ax.set_aspect('equal')
_cy, _cxs = _PAD + _R, [29.0, 71.0]
_yt = _cy + _R + _UP + 1.6 + _H_T / 2
ax.text(50, _yt + _H_T + 2.2, '2025年关节模组需求合计 72.0 万个',
        ha='center', va='center', fontsize=_FS_T, color=P[0], fontweight='bold')


def _stack(x, y, nm, v, tc, ha='center'):
    """名称、占比、数量三行就近标注，占比居中放大。"""
    ax.text(x, y + 3.2, nm, ha=ha, va='center', fontsize=_FS_N, color=tc, zorder=5)
    ax.text(x, y - 0.1, '%.0f%%' % (v / _TOTAL * 100), ha=ha, va='center',
            fontsize=_FS_P, color=tc, fontweight='bold', zorder=5)
    ax.text(x, y - 3.4, '%.1f万个' % v, ha=ha, va='center', fontsize=_FS_N,
            color=tc, zorder=5)


for _cx, (_title, _segs) in zip(_cxs, _GRP):
    ax.text(_cx, _yt, _title, ha='center', va='center', fontsize=_FS_T,
            color=P[0], fontweight='bold')
    _a0 = 90.0
    for _nm, _v, _fc, _tc in _segs:
        _ang = _v / _TOTAL * 360
        ax.add_patch(Wedge((_cx, _cy), _R, _a0 - _ang, _a0, facecolor=_fc,
                           edgecolor='white', linewidth=1.4, zorder=3))
        _mid = math.radians(_a0 - _ang / 2)
        if _ang >= 180:
            # 外移系数使名称行整体落在圆心之下，字顶不致越过扇形分界
            _k = 0.42 if _ang >= 300 else 0.53
            _stack(_cx + _k * _R * math.cos(_mid),
                   _cy + _k * _R * math.sin(_mid), _nm, _v, _tc)
        else:
            _o = -1 if _cx < 50 else 1          # 各自朝版面外侧展开
            _x1, _y1 = _cx + _R * math.cos(_mid), _cy + _R * math.sin(_mid)
            _x2, _y2 = _cx + 1.16 * _R * math.cos(_mid), _cy + 1.16 * _R * math.sin(_mid)
            _x3 = _cx + _o * (_R + 2.2)
            ax.plot([_x1, _x2, _x3 - _o * 0.6], [_y1, _y2, _y2],
                    color='#9AA7B4', lw=0.8, zorder=2)
            _stack(_x3, _y2, _nm, _v, _TXT, ha='right' if _o < 0 else 'left')
        _a0 -= _ang
    ax.add_patch(Wedge((_cx, _cy), _R, 0, 360, facecolor='none',
                       edgecolor='#C9D6E4', linewidth=0.7, zorder=4))
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
fig.savefig(D + '/fig3.png', dpi=300, facecolor='white')
plt.close(fig)

# ---------- 图四 全球谐波减速机产能 ----------
fig, ax = plt.subplots(figsize=(7.2, 3.2))
yr = ['2024年', '2025年（预计）', '2030年（预计）']
cap = [489.7, 600.0, 1000.0]
ax.bar(range(3), cap, 0.44, color=[P[0], P[1], P[2]],
       edgecolor='#FFFFFF', linewidth=.6)
for i, v in enumerate(cap):
    ax.text(i, v + 22, f'{v:,.1f}', ha='center', fontsize=9.5, color=P[0])
ax.set_xticks(range(3)); ax.set_xticklabels(yr, fontsize=10)
ax.set_ylabel('全球产能（万台）', fontsize=10)
ax.set_ylim(0, 1150)
_clean(ax)
fig.tight_layout()
fig.savefig(D + '/fig4.png', dpi=220, bbox_inches='tight')
plt.close(fig)

# ---------- 图五 人形机器人单机成本与人工成本 ----------
fig, ax = plt.subplots(figsize=(6.2, 3.2))
yrs = ['2023年', '2026年']
robot = [7.0, 2.0]
wage = [5.37, 6.16]
x = range(2)
w = 0.26
ax.bar([i - w / 2 for i in x], robot, w, color=P[0], label='人形机器人单机成本',
       edgecolor='#FFFFFF', linewidth=.6)
ax.bar([i + w / 2 for i in x], wage, w, color='#C00000', label='美国制造业工人年薪',
       edgecolor='#FFFFFF', linewidth=.6)
for i, v in zip(x, robot):
    ax.text(i - w / 2, v + 0.15, f'{v:.0f}', ha='center', fontsize=9.5, color=P[0])
for i, v in zip(x, wage):
    ax.text(i + w / 2, v + 0.15, f'{v:.2f}', ha='center', fontsize=9.5, color='#C00000')
ax.annotate('', xy=(1 - w / 2, 2.35), xytext=(0 - w / 2, 6.8),
            arrowprops=dict(arrowstyle='-|>', color=P[1], linewidth=1.3,
                            connectionstyle='arc3,rad=0.18'))
ax.text(0.30, 4.55, '降幅超过 70%', fontsize=10, color=P[1], ha='center')
ax.text(1 + w / 2, 6.72, '+15%', fontsize=10, color='#C00000', ha='center')
ax.set_xticks(list(x)); ax.set_xticklabels(yrs, fontsize=10)
ax.set_ylabel('万美元', fontsize=10)
ax.set_ylim(0, 8.4); ax.set_xlim(-0.48, 1.48)
ax.legend(fontsize=9, frameon=False, loc='upper center', ncol=2,
          bbox_to_anchor=(0.5, -0.13))
_clean(ax)
fig.tight_layout()
fig.savefig(D + '/fig5.png', dpi=220, bbox_inches='tight')
plt.close(fig)

print('五张图已生成：', sorted(os.listdir(D)))

# ---------- 图一 机器人产业链结构与公司所处环节 ----------
fig, ax = plt.subplots(figsize=(7.9, 2.75))
ax.set_xlim(0, 1); ax.set_ylim(0.225, 0.99); ax.axis('off')

def box(x, y, w, h, t, fc, ec, fs=10, tc='#000000', bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle='round,pad=0.006,rounding_size=0.012',
                 facecolor=fc, edgecolor=ec, linewidth=.9))
    ax.text(x+w/2, y+h/2, t, ha='center', va='center', fontsize=fs,
            color=tc, linespacing=1.55, fontweight='bold' if bold else 'normal')

W, G = 0.288, 0.056
xs = [0.014 + i*(W+G) for i in range(3)]

# 表头带
for x, t, fc in zip(xs, ['上游：基础材料与通用零部件',
                         '中游：核心零部件与一体化关节模组',
                         '下游：机器人整机及终端应用'],
                    [P[1], P[0], P[1]]):
    box(x, 0.855, W, 0.095, t, fc, fc, fs=10, tc='#FFFFFF', bold=True)

# 上游
for i, t in enumerate(['金属材料及工程材料', '轴承', '电子元器件']):
    box(xs[0], 0.645-i*0.175, W, 0.13, t, P[4], P[2], fs=9.5)

# 中游
box(xs[1], 0.585, W, 0.215, '电机 · 谐波减速机 · 驱动器\n编码器 · 力传感器', P[3], P[1], fs=9)
ax.add_patch(FancyArrowPatch((xs[1]+W/2, 0.585), (xs[1]+W/2, 0.515),
             arrowstyle='-|>', mutation_scale=11, color=P[1], linewidth=1.2))
box(xs[1], 0.345, W, 0.16, '一体化关节模组', P[0], P[0], fs=11.5, tc='#FFFFFF', bold=True)
ax.text(xs[1]+W/2, 0.275, '公司所处环节', ha='center', fontsize=10, color=P[0],
        fontweight='bold')

# 下游
box(xs[2], 0.625, W, 0.175, '人形机器人 · 协作机器人\n工业机器人', P[3], P[1], fs=9.5)
ax.add_patch(FancyArrowPatch((xs[2]+W/2, 0.615), (xs[2]+W/2, 0.545),
             arrowstyle='-|>', mutation_scale=11, color=P[1], linewidth=1.2))
box(xs[2], 0.345, W, 0.19, '工业制造 · 商业服务\n医疗康复 · 科研教育', P[4], P[2], fs=9.5)

for i in range(2):
    ax.add_patch(FancyArrowPatch((xs[i]+W+0.008, 0.52), (xs[i+1]-0.008, 0.52),
                 arrowstyle='-|>', mutation_scale=15, color=P[1], linewidth=1.7))
fig.tight_layout()
fig.savefig(D + '/fig0.png', dpi=220, bbox_inches='tight')


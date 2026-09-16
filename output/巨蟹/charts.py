# -*- coding: utf-8 -*-
"""第六章配图五张。配色取模板正文的深蓝系，图内文字用黑体类字体。

图一 机器人产业链结构与公司所处环节
图二 人形机器人硬件成本结构
图三 2025年全球人形机器人关节模组需求结构
图四 全球谐波减速机产能
图五 全球通用具身智能机器人出货量
"""
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei']
matplotlib.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
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
fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.1))
axes[0].pie([68.0, 4.0], labels=['旋转关节\n68.0万个', '直线关节\n4.0万个'],
            autopct='%1.0f%%', startangle=90, colors=[P[0], P[2]],
            textprops={'fontsize': 9}, wedgeprops={'linewidth': .8, 'edgecolor': 'white'})
axes[0].set_title('按关节类型', fontsize=10, pad=8)
axes[1].pie([50.2, 21.8], labels=['国产整机需求\n50.2万个', '境外整机需求\n21.8万个'],
            autopct='%1.0f%%', startangle=90, colors=[P[1], P[3]],
            textprops={'fontsize': 9}, wedgeprops={'linewidth': .8, 'edgecolor': 'white'})
axes[1].set_title('按整机归属', fontsize=10, pad=8)
fig.tight_layout()
fig.savefig(D + '/fig3.png', dpi=220, bbox_inches='tight')
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

# ---------- 图五 全球通用具身智能机器人出货量 ----------
fig, ax = plt.subplots(figsize=(5.4, 3.1))
ax.bar(range(2), [0.23, 1.30], 0.42, color=[P[2], P[0]],
       edgecolor='#FFFFFF', linewidth=.6)
for i, v in enumerate([0.23, 1.30]):
    ax.text(i, v + 0.05, f'{v:.2f} 万台', ha='center', fontsize=10, color=P[0])
ax.add_patch(FancyArrowPatch((0.18, 0.28), (0.92, 1.30),
                             arrowstyle='-|>', mutation_scale=11,
                             color='#2E75B6', linewidth=1.2,
                             connectionstyle='arc3,rad=-0.22'))
ax.text(0.5, 1.30, '增长近 5 倍', ha='center', fontsize=10, color='#2E75B6')
ax.set_xticks(range(2)); ax.set_xticklabels(['2024年', '2025年'], fontsize=10)
ax.set_ylabel('出货量（万台）', fontsize=10)
ax.set_ylim(0, 1.6); ax.set_xlim(-0.55, 1.55)
_clean(ax)
fig.tight_layout()
fig.savefig(D + '/fig5.png', dpi=220, bbox_inches='tight')
plt.close(fig)

print('五张图已生成：', sorted(os.listdir(D)))

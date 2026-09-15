# -*- coding: utf-8 -*-
"""第六章配图。配色取模板正文的深蓝系，图内文字用黑体类字体。"""
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei']
matplotlib.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt
import numpy as np
import os

P = ['#1F4E79', '#2E75B6', '#9DC3E6', '#BDD7EE', '#DEEBF7']
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fig')
os.makedirs(D, exist_ok=True)


def _clean(ax):
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.grid(axis='y', linestyle='--', color='#DDDDDD', linewidth=.7)
    ax.set_axisbelow(True)


# 图一 2025年全球人形机器人关节模组需求结构
fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.2))
a = axes[0]
a.pie([68.0, 4.0], labels=['旋转关节\n68.0万个', '直线关节\n4.0万个'],
      autopct='%1.0f%%', startangle=90, colors=[P[0], P[2]],
      textprops={'fontsize': 9}, wedgeprops={'linewidth': .8, 'edgecolor': 'white'})
a.set_title('按关节类型', fontsize=10, pad=8)
b = axes[1]
b.pie([50.2, 21.8], labels=['国产整机需求\n50.2万个', '境外整机需求\n21.8万个'],
      autopct='%1.0f%%', startangle=90, colors=[P[1], P[3]],
      textprops={'fontsize': 9}, wedgeprops={'linewidth': .8, 'edgecolor': 'white'})
b.set_title('按整机归属', fontsize=10, pad=8)
fig.tight_layout()
fig.savefig(D + '/fig1.png', dpi=220, bbox_inches='tight')
plt.close(fig)

# 图二 全球谐波减速机产能与国产厂商份额
fig, ax = plt.subplots(figsize=(7.6, 3.4))
yr = ['2024年', '2025年（预计）', '2030年（预计）']
cap = [489.7, 600.0, 1000.0]
bars = ax.bar(range(3), cap, 0.46, color=[P[0], P[1], P[2]],
              edgecolor='#FFFFFF', linewidth=.6)
for i, v in enumerate(cap):
    ax.text(i, v + 22, f'{v:,.1f}', ha='center', fontsize=9.5, color='#1F4E79')
ax.set_xticks(range(3))
ax.set_xticklabels(yr, fontsize=10)
ax.set_ylabel('全球产能（万台）', fontsize=10)
ax.set_ylim(0, 1150)
_clean(ax)
fig.tight_layout()
fig.savefig(D + '/fig2.png', dpi=220, bbox_inches='tight')
plt.close(fig)

# 图三 全球通用具身智能机器人出货量
fig, ax = plt.subplots(figsize=(5.4, 3.2))
lab = ['2024年', '2025年']
val = [0.23, 1.30]
ax.bar(range(2), val, 0.42, color=[P[2], P[0]],
       edgecolor='#FFFFFF', linewidth=.6)
for i, v in enumerate(val):
    ax.text(i, v + 0.05, f'{v:.2f} 万台', ha='center', fontsize=10, color='#1F4E79')
ax.annotate('', xy=(0.92, 1.30), xytext=(0.18, 0.28),
            arrowprops=dict(arrowstyle='->', color='#2E75B6', lw=1.2,
                            connectionstyle='arc3,rad=-0.22'))
ax.text(0.5, 1.30, '增长近 5 倍', ha='center', fontsize=10, color='#2E75B6')
ax.set_xlim(-0.55, 1.55)
ax.set_xticks(range(2))
ax.set_xticklabels(lab, fontsize=10)
ax.set_ylabel('出货量（万台）', fontsize=10)
ax.set_ylim(0, 1.6)
_clean(ax)
fig.tight_layout()
fig.savefig(D + '/fig3.png', dpi=220, bbox_inches='tight')
plt.close(fig)

print('三张图已生成：', os.listdir(D))

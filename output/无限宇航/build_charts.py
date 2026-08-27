# -*- coding: utf-8 -*-
"""图表生成。配色取部门规定蓝灰系；去上右边框、浅灰虚线网格、无3D无阴影无渐变。"""
import matplotlib
matplotlib.use('Agg')
from matplotlib import font_manager as fm
fm.fontManager.addfont('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc')
matplotlib.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei']
matplotlib.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt
import numpy as np

DARK, MID, LIGHT = '#123F63', '#5B93B8', '#C3D6E3'
GRID = '#D9D9D9'
INK  = '#333333'

def _frame(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    for s in ('left', 'bottom'):
        ax.spines[s].set_color(GRID); ax.spines[s].set_linewidth(0.8)
    ax.yaxis.grid(True, linestyle='--', linewidth=0.6, color=GRID)
    ax.set_axisbelow(True)
    ax.tick_params(colors=INK, labelsize=9, length=0)

# ---------- 图1 国内OTV市场规模预测 ----------
yr  = ['2026','2027','2028','2029','2030','2031','2032','2033','2034','2035']
bw  = [0.70, 4.99, 35.60, 80.44, 111.95, 139.76, 157.09, 162.32, 206.08, 249.00]
zw  = [5.23, 18.27, 30.11, 45.60, 55.35, 65.10, 62.38, 84.00, 119.62, 55.00]
xw  = [5.62, 11.35, 44.00, 55.50, 62.36, 56.93, 45.93, 54.13, 64.60, 31.05]

fig, ax = plt.subplots(figsize=(9.2, 4.4), dpi=200)
x = np.arange(len(yr))
b1 = ax.bar(x, bw, 0.62, label='OTV补网市场', color=DARK,  edgecolor='white', linewidth=0.9)
b2 = ax.bar(x, zw, 0.62, bottom=bw, label='OTV组网市场', color=MID,
            edgecolor='white', linewidth=0.9)
b3 = ax.bar(x, xw, 0.62, bottom=np.array(bw)+np.array(zw), label='OTV小卫星市场',
            color=LIGHT, edgecolor='#8FA9BA', linewidth=0.7)
tot = np.array(bw)+np.array(zw)+np.array(xw)
for xi, t in zip(x, tot):
    ax.text(xi, t + 9, f'{t:.0f}', ha='center', va='bottom',
            fontsize=8.5, color=INK)
_frame(ax)
ax.set_xticks(x); ax.set_xticklabels(yr)
ax.set_ylabel('亿元', fontsize=9, color=INK)
ax.set_ylim(0, 440)
ax.legend(frameon=False, fontsize=9, loc='upper left', labelcolor=INK, ncol=3)
fig.tight_layout()
fig.savefig('charts/fig1.png', bbox_inches='tight', facecolor='white')
plt.close(fig)

# ---------- 图2 三大星座发射与补网卫星数量 ----------
new = [545, 870, 1195, 1520, 1845, 2170, 2495, 4200, 5981, 2750]
rep = [29, 79, 165, 335, 622, 932, 1257, 1623, 2061, 2490]

fig, ax = plt.subplots(figsize=(9.2, 4.0), dpi=200)
w = 0.38
ax.bar(x - w/2, new, w, label='新发射卫星数量', color=DARK, edgecolor='white', linewidth=0.8)
ax.bar(x + w/2, rep, w, label='补网卫星数量', color='#8FB6CE', edgecolor='#8FA9BA', linewidth=0.7)
for xi, v in zip(x, new):
    ax.text(xi - w/2, v + 90, f'{v}', ha='center', va='bottom', fontsize=7.5, color=INK)
for xi, v in zip(x, rep):
    ax.text(xi + w/2, v + 90, f'{v}', ha='center', va='bottom', fontsize=7.5, color=INK)
_frame(ax)
ax.set_xticks(x); ax.set_xticklabels(yr)
ax.set_ylabel('颗', fontsize=9, color=INK)
ax.set_ylim(0, 6800)
ax.legend(frameon=False, fontsize=9, loc='upper left', labelcolor=INK)
fig.tight_layout()
fig.savefig('charts/fig2.png', bbox_inches='tight', facecolor='white')
plt.close(fig)
print('charts done')

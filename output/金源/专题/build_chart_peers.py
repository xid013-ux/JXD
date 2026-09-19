# 可比公司半导体零部件业务收入与毛利率（2026 年 1—6 月）
# 数据源：各公司 2026 年半年度报告
# 毛利率：披露值优先；未披露的由营业收入与营业成本测算（已与披露值交叉验证一致）
import os
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei']
matplotlib.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt

PALETTE = ['#123F63', '#2E6C97', '#5B93B8', '#8FB6CE', '#C3D6E3', '#E3EBF1']

# (公司, 披露口径, 收入亿元, 毛利率%, 材料路线)
DATA = [
    ('江丰电子', '精密零部件',          6.4504, 23.97, '金属'),
    ('托伦斯',   '半导体工艺零部件',    2.3903, 26.65, '金属'),
    ('先锋精科', '工艺部件',            4.7245, 28.10, '金属'),
    ('珂玛科技', '先进陶瓷材料零部件',  5.4343, 48.51, '非金属'),
    ('臻宝科技', '泛半导体零部件',      4.0173, 50.65, '非金属'),
]
DATA.sort(key=lambda r: r[3])

OUT = os.environ.get('DD_CHARTS', 'output/金源/专题/charts')
os.makedirs(OUT, exist_ok=True)

names = [f'{d[0]}\n{d[1]}' for d in DATA]
rev = [d[2] for d in DATA]
gm = [d[3] for d in DATA]
colors = [PALETTE[3] if d[4] == '金属' else PALETTE[1] for d in DATA]

fig, ax = plt.subplots(figsize=(9.2, 4.6), dpi=200)
x = range(len(DATA))
ax.bar(x, rev, width=0.56, color=colors)
for i, v in enumerate(rev):
    ax.text(i, v + 0.12, f'{v:.2f}', ha='center', va='bottom',
            fontsize=8.5, color='#333333')

ax2 = ax.twinx()
ax2.plot(x, gm, color=PALETTE[0], linewidth=0, marker='D', markersize=6.5)
for i, g in enumerate(gm):
    ax2.text(i, g + 1.6, f'{g:.2f}%', ha='center', va='bottom',
             fontsize=8.5, color=PALETTE[0], fontweight='bold')

ax.set_ylabel('零部件业务收入（亿元）', fontsize=9)
ax2.set_ylabel('该业务毛利率', fontsize=9)
ax.set_xticks(list(x))
ax.set_xticklabels(names, fontsize=8.5)
ax.set_ylim(0, 9.5)
ax2.set_ylim(10, 60)
ax2.set_yticks([20, 30, 40, 50])
ax2.set_yticklabels(['20%', '30%', '40%', '50%'], fontsize=8.5)
ax.tick_params(axis='y', labelsize=8.5)

# 两档之间的差距不加辅助线：任何横线都会穿过柱子，被读成收入阈值。
# 分档由柱色与菱形高度体现，具体差距写在正文。

ax.yaxis.grid(True, linestyle='--', linewidth=0.6, color='#D8D8D8')
ax.set_axisbelow(True)
for s in ('top', 'right'):
    ax.spines[s].set_visible(False)
    ax2.spines[s].set_visible(False)
ax.spines['left'].set_color('#999999')
ax.spines['bottom'].set_color('#999999')
ax2.spines['left'].set_visible(False)
ax2.spines['bottom'].set_visible(False)

import matplotlib.patches as mp
handles = [mp.Patch(color=PALETTE[3], label='金属路线（柱：收入）'),
           mp.Patch(color=PALETTE[1], label='非金属路线（柱：收入）'),
           plt.Line2D([], [], color=PALETTE[0], marker='D', linestyle='',
                      markersize=6, label='该业务毛利率（右轴）')]
ax.legend(handles=handles, loc='upper left', frameon=False,
          fontsize=8.5, ncol=3, bbox_to_anchor=(0.0, 1.11))

fig.tight_layout()
path = os.path.join(OUT, 'fig_peers.png')
fig.savefig(path, bbox_inches='tight', facecolor='white')
print('saved', path)
for n, c, r, g, m in DATA:
    print(f'  {n:6s} {c:18s} {r:6.2f}亿  {g:6.2f}%  {m}')

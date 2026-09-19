# 可比公司半导体零部件业务收入与毛利率（2026 年 1—6 月）
# 数据源：各公司 2026 年半年度报告
# 图中只画收入。毛利率留在 DATA 里供数据来源清单引用，不进交付物正文：
# 金源主力产品线走金属路线，分档对比会主动展开对其不利的一面。
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
DATA.sort(key=lambda r: -r[2])

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

ax.set_ylabel('零部件业务收入（亿元）', fontsize=9)
ax.set_xticks(list(x))
ax.set_xticklabels(names, fontsize=8.5)
ax.set_ylim(0, 7.6)
ax.tick_params(axis='y', labelsize=8.5)

ax.yaxis.grid(True, linestyle='--', linewidth=0.6, color='#D8D8D8')
ax.set_axisbelow(True)
for s in ('top', 'right'):
    ax.spines[s].set_visible(False)
ax.spines['left'].set_color('#999999')
ax.spines['bottom'].set_color('#999999')

import matplotlib.patches as mp
handles = [mp.Patch(color=PALETTE[3], label='金属路线'),
           mp.Patch(color=PALETTE[1], label='非金属路线')]
ax.legend(handles=handles, loc='upper right', frameon=False,
          fontsize=8.5, ncol=2)

fig.tight_layout()
path = os.path.join(OUT, 'fig_peers.png')
fig.savefig(path, bbox_inches='tight', facecolor='white')
print('saved', path)
for n, c, r, g, m in DATA:
    print(f'  {n:6s} {c:18s} {r:6.2f}亿  {g:6.2f}%  {m}')

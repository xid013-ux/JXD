# 图1 中国晶圆厂零部件采购额及直接采购占比（2020—2029E）
# 数据源：弗若斯特沙利文，经重庆臻宝科技股份有限公司招股说明书（注册稿）披露
import os
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei']
matplotlib.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt

PALETTE = ['#123F63', '#2E6C97', '#5B93B8', '#8FB6CE', '#C3D6E3', '#E3EBF1']

YEARS = ['2020', '2021', '2022', '2023', '2024',
         '2025E', '2026E', '2027E', '2028E', '2029E']
DIRECT = [49.6, 71.8, 80.3, 96.8, 126.6, 162.3, 189.2, 219.6, 253.6, 291.8]
VIA_OEM = [24.9, 34.7, 37.2, 42.6, 50.7, 59.0, 62.5, 65.8, 68.7, 71.6]
TOTAL = [74.5, 106.5, 117.6, 139.4, 177.2, 221.3, 251.7, 285.3, 322.3, 363.4]
RATIO = [d / t * 100 for d, t in zip(DIRECT, TOTAL)]

OUT = os.environ.get('DOCX_CHARTS', 'output/金源/专题/charts')
os.makedirs(OUT, exist_ok=True)

fig, ax = plt.subplots(figsize=(9.2, 4.6), dpi=200)
x = range(len(YEARS))

ax.bar(x, DIRECT, width=0.62, color=PALETTE[1], label='向零部件厂商直接采购')
ax.bar(x, VIA_OEM, width=0.62, bottom=DIRECT, color=PALETTE[3], label='向设备厂采购')

for i, t in enumerate(TOTAL):
    ax.text(i, t + 6, f'{t:,.1f}', ha='center', va='bottom',
            fontsize=7.5, color='#333333')

ax2 = ax.twinx()
ax2.plot(x, RATIO, color=PALETTE[0], linewidth=1.6,
         marker='o', markersize=3.6, label='直接采购占比（右轴）')
for i, r in enumerate(RATIO):
    if i in (0, 4, 9):
        ax2.text(i, r + 2.0, f'{r:.1f}%', ha='center', va='bottom',
                 fontsize=7.5, color=PALETTE[0])

ax.set_ylabel('采购额（亿元）', fontsize=9)
ax2.set_ylabel('直接采购占比', fontsize=9)
ax.set_xticks(list(x))
ax.set_xticklabels(YEARS, fontsize=8.5)
ax.set_ylim(0, 520)
ax2.set_ylim(62, 84)
ax2.set_yticks([65, 70, 75, 80])
ax2.set_yticklabels(['65%', '70%', '75%', '80%'], fontsize=8.5)
ax.tick_params(axis='y', labelsize=8.5)

ax.yaxis.grid(True, linestyle='--', linewidth=0.6, color='#D8D8D8')
ax.set_axisbelow(True)
for s in ('top', 'right'):
    ax.spines[s].set_visible(False)
    ax2.spines[s].set_visible(False)
ax.spines['left'].set_color('#999999')
ax.spines['bottom'].set_color('#999999')
ax2.spines['left'].set_visible(False)
ax2.spines['bottom'].set_visible(False)

h1, l1 = ax.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, loc='upper left', frameon=False,
          fontsize=8.5, ncol=3, bbox_to_anchor=(0.0, 1.10))

fig.tight_layout()
path = os.path.join(OUT, 'fig1.png')
fig.savefig(path, bbox_inches='tight', facecolor='white')
print('saved', path)
print('占比序列:', [round(r, 1) for r in RATIO])

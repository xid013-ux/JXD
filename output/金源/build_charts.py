# -*- coding: utf-8 -*-
import matplotlib; matplotlib.use('Agg')
matplotlib.rcParams['font.sans-serif']=['WenQuanYi Zen Hei']
matplotlib.rcParams['axes.unicode_minus']=False
import matplotlib.pyplot as plt
import numpy as np
P=['#123F63','#2E6C97','#5B93B8','#8FB6CE','#C3D6E3','#E3EBF1']
D='/home/user/JXD/output/金源/charts/'
def base(ax):
    for s in ('top','right'): ax.spines[s].set_visible(False)
    ax.grid(axis='y',linestyle='--',color='#DDDDDD'); ax.set_axisbelow(True)

# 图1 晶圆厂零部件采购额
cats=['零部件整体','其中：非金属','硅','石英','陶瓷']
y24=[177.2,113.5,43.8,34.8,29.4]; d24=[126.6,80.4,35.7,22.7,19.3]
fig,ax=plt.subplots(figsize=(8.4,3.9)); x=np.arange(len(cats)); w=0.36
ax.bar(x-w/2,y24,w,label='晶圆厂采购额合计',color=P[3])
ax.bar(x+w/2,d24,w,label='其中向零部件厂商直接采购',color=P[0])
for i,(a,b) in enumerate(zip(y24,d24)):
    ax.text(x[i]-w/2,a+3,f'{a:.1f}',ha='center',fontsize=9)
    ax.text(x[i]+w/2,b+3,f'{b:.1f}',ha='center',fontsize=9,color=P[0])
ax.set_xticks(x); ax.set_xticklabels(cats); ax.set_ylabel('采购额（亿元）'); ax.set_ylim(0,205)
base(ax); ax.legend(frameon=False,fontsize=9)
fig.tight_layout(); fig.savefig(D+'fig1_caigou.png',dpi=200); plt.close(fig)

# 图2 可比公司毛利率（按材料路线）
co=['珂玛科技','臻宝科技','先锋精科','托伦斯','富创精密']
g=[53.94,49.85,29.02,27.14,24.94]
grp=['非金属','非金属','金属','金属','金属含模组']
cmap={'非金属':P[0],'金属':P[3],'金属含模组':P[4]}
fig,ax=plt.subplots(figsize=(8.0,3.7))
ax.bar(range(len(co)),g,0.52,color=[cmap[x] for x in grp],edgecolor='#BBBBBB',linewidth=.5)
for i,v in enumerate(g): ax.text(i,v+1.2,f'{v:.2f}',ha='center',fontsize=9.5)
ax.set_xticks(range(len(co))); ax.set_xticklabels(co,fontsize=10)
ax.set_ylabel('2025年主营业务毛利率（%）'); ax.set_ylim(0,62)
base(ax)
import matplotlib.patches as mp
ax.legend(handles=[mp.Patch(color=c,label=k) for k,c in cmap.items()],
          frameon=False,fontsize=9,ncol=3,loc='upper center',bbox_to_anchor=(0.5,1.13))
fig.tight_layout(); fig.savefig(D+'fig2_maolilv.png',dpi=200); plt.close(fig)

# 图3 与金源对应品类的分产品毛利率：两家厂商对比
lbl=['匀气盘\n先锋精科','匀气盘\n托伦斯','气体分布盘\n托伦斯',
     '加热器\n先锋精科','加热器\n托伦斯']
y22=[43.31,26.72,40.93,49.85,-18.68]
y23=[39.76,27.44,20.05,39.85,14.39]
y24=[40.73,31.86,25.88,43.66,52.79]
fig,ax=plt.subplots(figsize=(8.6,3.9)); x=np.arange(len(lbl)); w=0.26
ax.bar(x-w,y22,w,label='2022年',color=P[4])
ax.bar(x,  y23,w,label='2023年',color=P[3])
ax.bar(x+w,y24,w,label='2024年',color=P[0])
for i in range(len(lbl)):
    for dx,v,c in ((-w,y22[i],'#333333'),(0,y23[i],'#333333'),(w,y24[i],P[0])):
        ax.text(x[i]+dx,v+(1.2 if v>=0 else -3.6),f'{v:.2f}',
                ha='center',fontsize=8,color=c)
ax.axhline(0,color='#999999',lw=.9)
ax.set_xticks(x); ax.set_xticklabels(lbl,fontsize=9)
ax.set_ylabel('毛利率（%）'); ax.set_ylim(-26,62)
base(ax); ax.legend(frameon=False,fontsize=9,ncol=3,loc='upper left')
fig.tight_layout(); fig.savefig(D+'fig3_danpin.png',dpi=200); plt.close(fig)

# 图4 问询收敛
comp=['神工股份','珂玛科技','先锋精科','托伦斯','臻宝科技']
rounds=['首轮','第二轮','第三轮','第四轮','落实函']
data={'神工股份':[49,20,8,8,2],'珂玛科技':[19,5,None,None,3],
      '先锋精科':[18,7,None,None,None],
      '托伦斯':[15,3,None,None,1],'臻宝科技':[13,5,None,None,None]}
fig,ax=plt.subplots(figsize=(8.6,3.8))
x=np.arange(len(comp)); w=0.16
for r in range(5):
    vals=[data[c][r] for c in comp]
    pos=[x[i]+(r-2)*w for i in range(len(comp))]
    pv=[(p,v) for p,v in zip(pos,vals) if v is not None]
    ax.bar([p for p,_ in pv],[v for _,v in pv],w,label=rounds[r],color=P[r])
    for p,v in pv:
        ax.text(p,v+1.0,str(v),ha='center',fontsize=8,
                color='#333333' if r>1 else P[0])
ax.set_xticks(x); ax.set_xticklabels(comp,fontsize=10)
ax.set_ylabel('该轮问题数量（个）'); ax.set_ylim(0,58)
base(ax); ax.legend(frameon=False,fontsize=9,ncol=5,loc='upper center',
                    bbox_to_anchor=(0.5,1.13))
fig.tight_layout(); fig.savefig(D+'fig4_shoulian.png',dpi=200); plt.close(fig)
print('四张图已生成')

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

# 图3 与金源对应产品的分品类毛利率变动
prod=['加热器\n（对应加热盘）','匀气盘\n（对应气体喷头）','气体分布盘\n（对应气体喷头）']
y23=[14.39,27.44,20.05]; y24=[52.79,31.86,25.88]
fig,ax=plt.subplots(figsize=(7.6,3.7)); x=np.arange(len(prod)); w=0.34
ax.bar(x-w/2,y23,w,label='2023年',color=P[3])
ax.bar(x+w/2,y24,w,label='2024年',color=P[0])
for i in range(len(prod)):
    ax.text(x[i]-w/2,y23[i]+1.0,f'{y23[i]:.2f}',ha='center',fontsize=9)
    ax.text(x[i]+w/2,y24[i]+1.0,f'{y24[i]:.2f}',ha='center',fontsize=9,color=P[0])
ax.set_xticks(x); ax.set_xticklabels(prod,fontsize=9.5)
ax.set_ylabel('毛利率（%）'); ax.set_ylim(0,62)
base(ax); ax.legend(frameon=False,fontsize=9.5)
fig.tight_layout(); fig.savefig(D+'fig3_danpin.png',dpi=200); plt.close(fig)

# 图4 问询收敛
fig,ax=plt.subplots(figsize=(7.8,3.5))
rounds=['首轮','第二轮','第三轮','第四轮','落实函']
data={'神工股份':[49,20,8,8,2],'珂玛科技':[19,5,None,None,3],
      '托伦斯':[15,3,None,None,1],'臻宝科技':[13,5,None,None,None]}
off={'神工股份':(0,9),'珂玛科技':(0,9),'托伦斯':(0,-15),'臻宝科技':(13,-4)}
cols=[P[0],P[1],P[2],P[3]]
for i,(k,v) in enumerate(data.items()):
    xs=[j for j,y in enumerate(v) if y is not None]; ys=[y for y in v if y is not None]
    for a,b in zip(range(len(xs)-1),range(1,len(xs))):
        st='-' if xs[b]-xs[a]==1 else ':'
        ax.plot([xs[a],xs[b]],[ys[a],ys[b]],st,lw=1.8,color=cols[i])
    ax.plot(xs,ys,'o',ms=6,label=k,color=cols[i])
    for j,y in zip(xs,ys):
        ax.annotate(str(y),(j,y),textcoords='offset points',
                    xytext=off[k],ha='center',fontsize=9,color=cols[i])
ax.set_xticks(range(5)); ax.set_xticklabels(rounds)
ax.set_ylabel('该轮问题数量（个）'); ax.set_ylim(-4,56)
base(ax); ax.legend(frameon=False,fontsize=9.5)
ax.text(0.99,0.72,'虚线表示该企业无第三、四轮问询',transform=ax.transAxes,
        ha='right',fontsize=8,color='#555555')
fig.tight_layout(); fig.savefig(D+'fig4_shoulian.png',dpi=200); plt.close(fig)
print('四张图已生成')

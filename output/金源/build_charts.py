# -*- coding: utf-8 -*-
import matplotlib; matplotlib.use('Agg')
matplotlib.rcParams['font.sans-serif']=['WenQuanYi Zen Hei']
matplotlib.rcParams['axes.unicode_minus']=False
import matplotlib.pyplot as plt
import numpy as np
P=['#123F63','#2E6C97','#5B93B8','#8FB6CE','#C3D6E3','#E3EBF1']
D='/home/user/JXD/output/金源/charts/'

# 图1 中国晶圆厂零部件采购额（弗若斯特沙利文）
cats=['零部件整体','其中：非金属','硅','石英','陶瓷']
y24=[177.2,113.5,43.8,34.8,29.4]
d24=[126.6,80.4,35.7,22.7,19.3]
fig,ax=plt.subplots(figsize=(9,4.3))
x=np.arange(len(cats)); w=0.36
b1=ax.bar(x-w/2,y24,w,label='晶圆厂采购额合计',color=P[3])
b2=ax.bar(x+w/2,d24,w,label='其中向零部件厂商直接采购',color=P[0])
for i,(a,b) in enumerate(zip(y24,d24)):
    ax.text(x[i]-w/2,a+2.5,f'{a:.1f}',ha='center',fontsize=8.5)
    ax.text(x[i]+w/2,b+2.5,f'{b:.1f}',ha='center',fontsize=8.5,color=P[0])
    ax.text(x[i]+w/2,b/2,f'{b/a*100:.1f}%',ha='center',va='center',fontsize=8,color='white')
ax.set_xticks(x); ax.set_xticklabels(cats); ax.set_ylabel('采购额（亿元）')
ax.set_ylim(0,205)
for s in ('top','right'): ax.spines[s].set_visible(False)
ax.grid(axis='y',linestyle='--',color='#DDDDDD'); ax.set_axisbelow(True)
ax.legend(frameon=False,fontsize=9,loc='upper right')
fig.tight_layout(); fig.savefig(D+'fig1_caigou.png',dpi=200); plt.close(fig)

# 图2 可比公司毛利率
co=['珂玛科技','臻宝科技','Ferrotec','先锋精科','托伦斯','京鼎精密','富创精密','超科林']
g25=[53.94,49.85,29.95,29.02,27.14,25.14,24.94,15.72]
g24=[58.49,48.05,26.74,33.83,29.89,26.06,25.80,16.99]
g23=[39.78,42.56,31.41,29.93,23.26,26.16,25.20,15.99]
fig,ax=plt.subplots(figsize=(9.6,4.4))
x=np.arange(len(co)); w=0.26
ax.bar(x-w,g23,w,label='2023年',color=P[4])
ax.bar(x  ,g24,w,label='2024年',color=P[2])
ax.bar(x+w,g25,w,label='2025年',color=P[0])
for i,v in enumerate(g25): ax.text(x[i]+w,v+1.1,f'{v:.1f}',ha='center',fontsize=7.8,color=P[0])
ax.axhline(32.65,color='#B5533C',ls='--',lw=1.1)
ax.text(len(co)-0.4,34.2,'七家可比公司2025年平均 32.65%（不含托伦斯）',
        fontsize=8,color='#B5533C',ha='right')
ax.set_xticks(x); ax.set_xticklabels(co,fontsize=9); ax.set_ylabel('主营业务毛利率（%）')
ax.set_ylim(0,66)
for s in ('top','right'): ax.spines[s].set_visible(False)
ax.grid(axis='y',linestyle='--',color='#DDDDDD'); ax.set_axisbelow(True)
ax.legend(frameon=False,fontsize=9,ncol=3,loc='upper right')
fig.tight_layout(); fig.savefig(D+'fig2_maoli.png',dpi=200); plt.close(fig)

# 图3 2025年营收与净利率
co3=['超科林','京鼎精密','富创精密','先锋精科','珂玛科技','臻宝科技','托伦斯']
rev=[144.37,45.18,35.51,12.38,10.70,8.68,7.20]
npm=[-8.82,11.60,-0.26,15.37,29.06,26.04,13.64]
fig,ax=plt.subplots(figsize=(9.4,4.3))
x=np.arange(len(co3))
cols=[P[0] if c in ('珂玛科技','臻宝科技') else P[3] for c in co3]
ax.bar(x,rev,0.5,color=cols)
for i,v in enumerate(rev): ax.text(x[i],v+2.5,f'{v:.2f}',ha='center',fontsize=8.5)
ax.set_xticks(x); ax.set_xticklabels(co3,fontsize=9)
ax.set_ylabel('2025年营业收入（亿元）'); ax.set_ylim(0,168)
for s in ('top','right'): ax.spines[s].set_visible(False)
ax.grid(axis='y',linestyle='--',color='#DDDDDD'); ax.set_axisbelow(True)
ax2=ax.twinx()
ax2.plot(x,npm,color='#B5533C',marker='D',ms=5,lw=0)
for i,v in enumerate(npm):
    ax2.annotate(f'{v:.2f}%',(x[i],v),textcoords='offset points',xytext=(0,-15),
                 ha='center',fontsize=8,color='#B5533C')
ax2.axhline(0,color='#CCCCCC',lw=.8); ax2.set_ylabel('销售净利率（%）'); ax2.set_ylim(-22,42)
for s in ('top',): ax2.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig(D+'fig3_shouru.png',dpi=200); plt.close(fig)

# 图4 问询收敛
fig,ax=plt.subplots(figsize=(8.6,4.0))
rounds=['首轮','第二轮','第三轮','第四轮','落实函']
data={'中微公司':[52,10,3,2,3],'托伦斯':[15,3,None,None,1],
      '臻宝科技':[13,5,None,None,None],'珂玛科技':[13,5,None,None,3]}
for i,(k,v) in enumerate(data.items()):
    xs=[j for j,y in enumerate(v) if y is not None]
    ys=[y for y in v if y is not None]
    ax.plot(xs,ys,marker='o',ms=6,lw=1.8,label=k,color=P[i])
    for a,b in zip(xs,ys): ax.annotate(str(b),(a,b),textcoords='offset points',
                                       xytext=(0,7),ha='center',fontsize=8,color=P[i])
ax.set_xticks(range(5)); ax.set_xticklabels(rounds)
ax.set_ylabel('该轮问题数量（个）'); ax.set_ylim(0,58)
for s in ('top','right'): ax.spines[s].set_visible(False)
ax.grid(axis='y',linestyle='--',color='#DDDDDD'); ax.set_axisbelow(True)
ax.legend(frameon=False,fontsize=9)
fig.tight_layout(); fig.savefig(D+'fig4_shoulian.png',dpi=200); plt.close(fig)
print('四张图已生成')

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
fig,ax=plt.subplots(figsize=(8.6,4.0)); x=np.arange(len(cats)); w=0.36
ax.bar(x-w/2,y24,w,label='晶圆厂采购额合计',color=P[3])
ax.bar(x+w/2,d24,w,label='其中向零部件厂商直接采购',color=P[0])
for i,(a,b) in enumerate(zip(y24,d24)):
    ax.text(x[i]-w/2,a+3,f'{a:.1f}',ha='center',fontsize=9)
    ax.text(x[i]+w/2,b+3,f'{b:.1f}',ha='center',fontsize=9,color=P[0])
ax.set_xticks(x); ax.set_xticklabels(cats); ax.set_ylabel('采购额（亿元）'); ax.set_ylim(0,205)
base(ax); ax.legend(frameon=False,fontsize=9)
fig.tight_layout(); fig.savefig(D+'fig1_caigou.png',dpi=200); plt.close(fig)

# 图2 金源对应细分市场规模
seg=['刻蚀设备用\n气体分配盘','半导体\n陶瓷加热器','静电卡盘']
a=[9.44,14.28,17.9]; b=[15.44,21.56,24.1]; yr=['2030年','2030年','2028年']
fig,ax=plt.subplots(figsize=(8.0,4.0)); x=np.arange(len(seg)); w=0.34
ax.bar(x-w/2,a,w,label='基期',color=P[3])
ax.bar(x+w/2,b,w,label='预测期',color=P[0])
for i in range(len(seg)):
    ax.text(x[i]-w/2,a[i]+0.5,f'{a[i]}',ha='center',fontsize=9)
    ax.text(x[i]+w/2,b[i]+0.5,f'{b[i]}',ha='center',fontsize=9,color=P[0])
    ax.text(x[i]+w/2,b[i]+2.0,yr[i],ha='center',fontsize=8,color='#666666')
ax.set_xticks(x); ax.set_xticklabels(seg,fontsize=9)
ax.set_ylabel('市场规模（亿美元）'); ax.set_ylim(0,29)
base(ax); ax.legend(frameon=False,fontsize=9,loc='upper left')
fig.tight_layout(); fig.savefig(D+'fig2_xifen.png',dpi=200); plt.close(fig)

# 图3 可比公司营业收入（单一维度）
co=['超科林','京鼎精密','富创精密','先锋精科','珂玛科技','臻宝科技','托伦斯']
rev=[144.37,45.18,35.51,12.38,10.70,8.68,7.20]
fig,ax=plt.subplots(figsize=(8.6,3.8))
ax.barh(range(len(co))[::-1],rev,0.55,color=P[0])
for i,v in enumerate(rev):
    ax.text(v+2.5,len(co)-1-i,f'{v:.2f}',va='center',fontsize=9)
ax.set_yticks(range(len(co))[::-1]); ax.set_yticklabels(co,fontsize=9.5)
ax.set_xlabel('2025年营业收入（亿元）'); ax.set_xlim(0,168)
for s in ('top','right'): ax.spines[s].set_visible(False)
ax.grid(axis='x',linestyle='--',color='#DDDDDD'); ax.set_axisbelow(True)
fig.tight_layout(); fig.savefig(D+'fig3_shouru.png',dpi=200); plt.close(fig)

# 图4 可比公司销售净利率（单一维度）
co4=['珂玛科技','臻宝科技','先锋精科','托伦斯','京鼎精密','富创精密','超科林']
npm=[29.06,26.04,15.37,13.64,11.60,-0.26,-8.82]
fig,ax=plt.subplots(figsize=(8.6,3.8))
cols=[P[0] if v>=0 else '#B5533C' for v in npm]
ax.barh(range(len(co4))[::-1],npm,0.55,color=cols)
for i,v in enumerate(npm):
    ax.text(v+(0.7 if v>=0 else -0.7),len(co4)-1-i,f'{v:.2f}%',
            va='center',ha='left' if v>=0 else 'right',fontsize=9)
ax.axvline(0,color='#999999',lw=.9)
ax.set_yticks(range(len(co4))[::-1]); ax.set_yticklabels(co4,fontsize=9.5)
ax.set_xlabel('2025年销售净利率（%）'); ax.set_xlim(-14,36)
for s in ('top','right'): ax.spines[s].set_visible(False)
ax.grid(axis='x',linestyle='--',color='#DDDDDD'); ax.set_axisbelow(True)
fig.tight_layout(); fig.savefig(D+'fig4_jinglilv.png',dpi=200); plt.close(fig)

# 图5 毛利率按材料路线
co5=['珂玛科技','臻宝科技','Ferrotec','先锋精科','托伦斯','京鼎精密','富创精密','超科林']
g25=[53.94,49.85,29.95,29.02,27.14,25.14,24.94,15.72]
grp=['非金属','非金属','非金属为主','金属','金属','金属含模组','金属含模组','含子系统与模组']
cmap={'非金属':P[0],'非金属为主':P[2],'金属':P[3],'金属含模组':P[4],'含子系统与模组':P[5]}
fig,ax=plt.subplots(figsize=(9.0,3.9))
ax.bar(range(len(co5)),g25,0.55,color=[cmap[g] for g in grp],edgecolor='#BBBBBB',linewidth=.5)
for i,v in enumerate(g25): ax.text(i,v+1.2,f'{v:.2f}',ha='center',fontsize=9)
ax.set_xticks(range(len(co5))); ax.set_xticklabels(co5,fontsize=9)
ax.set_ylabel('2025年主营业务毛利率（%）'); ax.set_ylim(0,62)
base(ax)
import matplotlib.patches as mp
ax.legend(handles=[mp.Patch(color=c,label=k) for k,c in cmap.items()],
          frameon=False,fontsize=8.5,ncol=5,loc='upper center',bbox_to_anchor=(0.5,1.14))
fig.tight_layout(); fig.savefig(D+'fig5_maolilv.png',dpi=200); plt.close(fig)

def shoulian(fname,rounds,data,offs,ymax,colors):
    fig,ax=plt.subplots(figsize=(7.6,3.4))
    for i,(k,v) in enumerate(data.items()):
        xs=[j for j,y in enumerate(v) if y is not None]; ys=[y for y in v if y is not None]
        ax.plot(xs,ys,marker='o',ms=6,lw=1.8,label=k,color=colors[i])
        for j,y in zip(xs,ys):
            ax.annotate(str(y),(j,y),textcoords='offset points',
                        xytext=offs[k][j],ha='center',fontsize=9,color=colors[i])
    ax.set_xticks(range(len(rounds))); ax.set_xticklabels(rounds)
    ax.set_ylabel('该轮问题数量（个）'); ax.set_ylim(-ymax*0.09,ymax)
    base(ax); ax.legend(frameon=False,fontsize=9.5)
    fig.tight_layout(); fig.savefig(D+fname,dpi=200); plt.close(fig)

# 图6 四轮问询样本的收敛
shoulian('fig6_shoulian4.png',['首轮','第二轮','第三轮','第四轮','落实函'],
         {'中微公司':[52,10,3,2,3],'神工股份':[49,20,8,8,2]},
         {'中微公司':[(0,9),(0,-16),(-13,-4),(-13,-4),(0,9)],
          '神工股份':[(0,-16),(0,9),(0,9),(0,9),(0,-16)]},60,[P[0],P[2]])

# 图7 两轮问询样本的收敛
shoulian('fig7_shoulian2.png',['首轮','第二轮','落实函'],
         {'珂玛科技':[19,5,3],'托伦斯':[15,3,1],'臻宝科技':[13,5,None]},
         {'珂玛科技':[(0,9),(0,9),(0,9)],
          '托伦斯':[(14,-4),(0,-16),(0,-16)],
          '臻宝科技':[(0,-16),(15,-4),None]},22,[P[1],P[2],P[3]])

print('七张图已生成（每张单一维度）')

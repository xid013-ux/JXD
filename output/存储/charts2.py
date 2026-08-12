# -*- coding: utf-8 -*-
import matplotlib; matplotlib.use('Agg')
matplotlib.rcParams['font.sans-serif']=['WenQuanYi Zen Hei']
matplotlib.rcParams['axes.unicode_minus']=False
import matplotlib.pyplot as plt
import numpy as np
P=['#123F63','#2E6C97','#5B93B8','#8FB6CE','#C3D6E3','#E3EBF1']
D='/home/user/JXD/output/存储/charts/'

# 图：深科技分产品收入结构
yrs=['2021年','2022年','2023年','2024年','2025年']
stor=[28.85,26.47,25.59,35.22,40.91]
mfg =[121.44,115.94,91.22,82.92,85.35]
met =[13.32,17.94,25.45,29.35,30.21]
oth =[1.27,0.82,0.39,0.78,1.01]
pct =[17.50,16.42,17.94,23.75,25.98]
fig,ax=plt.subplots(figsize=(9,4.4))
x=np.arange(len(yrs)); w=0.58
b=np.zeros(len(yrs))
for vals,lab,c in ((mfg,'高端制造',P[3]),(stor,'存储半导体业务',P[0]),
                   (met,'计量智能终端',P[2]),(oth,'其他业务',P[4])):
    ax.bar(x,vals,w,bottom=b,label=lab,color=c); b=b+np.array(vals)
for i,v in enumerate(stor):
    ax.text(x[i], mfg[i]+v/2, f'{v:.1f}', ha='center', va='center',
            fontsize=8.5, color='white')
ax.set_xticks(x); ax.set_xticklabels(yrs); ax.set_ylabel('营业收入（亿元）')
for s in ('top','right'): ax.spines[s].set_visible(False)
ax.grid(axis='y',linestyle='--',color='#DDDDDD'); ax.set_axisbelow(True)
ax2=ax.twinx()
ax2.plot(x,pct,color='#B5533C',marker='o',ms=4,lw=1.6,label='存储半导体业务占比（右轴）')
for i,v in enumerate(pct):
    ax2.annotate(f'{v:.2f}%',(x[i],v),textcoords='offset points',
                 xytext=(0,8),ha='center',fontsize=8,color='#B5533C')
ax2.set_ylabel('占营业收入比重（%）'); ax2.set_ylim(0,40)
for s in ('top',): ax2.spines[s].set_visible(False)
h1,l1=ax.get_legend_handles_labels(); h2,l2=ax2.get_legend_handles_labels()
ax.legend(h1+h2,l1+l2,loc='upper center',bbox_to_anchor=(0.5,-0.09),
          ncol=5,frameon=False,fontsize=8.5)
fig.tight_layout(); fig.savefig(D+'fig_struct.png',dpi=200,bbox_inches='tight'); plt.close(fig)

# 图：主要子公司营收与净利率
names=['深科技东莞','深科技香港','深圳沛顿','深科技马来西亚','深科技苏州',
       '深科技成都\n（开发科技）','深科技精密']
rev=[83.74,73.93,46.35,34.21,30.70,30.22,9.47]
mgn=[1.91,-3.29,3.78,3.58,2.24,23.40,22.75]
fig,ax=plt.subplots(figsize=(9,4.2))
x=np.arange(len(names))
cols=[P[0] if n=='深圳沛顿' else P[3] for n in names]
ax.bar(x,rev,0.55,color=cols)
for i,v in enumerate(rev):
    ax.text(x[i],v+1.5,f'{v:.2f}',ha='center',fontsize=8.5)
ax.set_xticks(x); ax.set_xticklabels(names,fontsize=8.5)
ax.set_ylabel('营业收入（亿元）'); ax.set_ylim(0,100)
for s in ('top','right'): ax.spines[s].set_visible(False)
ax.grid(axis='y',linestyle='--',color='#DDDDDD'); ax.set_axisbelow(True)
ax2=ax.twinx()
ax2.plot(x,mgn,color='#B5533C',marker='D',ms=5,lw=0,label='净利率（右轴）')
for i,v in enumerate(mgn):
    ax2.annotate(f'{v:.2f}%',(x[i],v),textcoords='offset points',
                 xytext=(0,-14),ha='center',fontsize=8,color='#B5533C')
ax2.axhline(0,color='#CCCCCC',lw=.8)
ax2.set_ylabel('净利率（%）'); ax2.set_ylim(-8,30)
for s in ('top',): ax2.spines[s].set_visible(False)
ax2.legend(loc='upper right',frameon=False,fontsize=8.5)
fig.tight_layout(); fig.savefig(D+'fig_subs.png',dpi=200,bbox_inches='tight'); plt.close(fig)
print('两张图已生成')

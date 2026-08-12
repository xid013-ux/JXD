# -*- coding: utf-8 -*-
import matplotlib; matplotlib.use('Agg')
matplotlib.rcParams['font.sans-serif']=['WenQuanYi Zen Hei']
matplotlib.rcParams['axes.unicode_minus']=False
import matplotlib.pyplot as plt
import numpy as np
P=['#123F63','#2E6C97','#5B93B8','#8FB6CE','#C3D6E3','#E3EBF1']
D='/home/user/JXD/output/存储/charts/'

# 图：2025Q4 DRAM 与 NAND 厂商份额
fig,axes=plt.subplots(1,2,figsize=(9.6,4.0))
for ax,(title,labs,vals) in zip(axes,[
    ('DRAM', ['三星电子\n37.1%','SK海力士\n33.1%','美光科技\n20.8%','其他\n9.0%'],
     [37.1,33.1,20.8,9.0]),
    ('NAND Flash', ['三星电子\n27.0%','SK海力士\n22.1%','其他\n50.9%'],
     [27.0,22.1,50.9])]):
    ax.pie(vals,labels=labs,colors=P[:len(vals)],startangle=90,
           counterclock=False,textprops={'fontsize':9},
           wedgeprops={'edgecolor':'white','linewidth':1.2})
    ax.set_title(title,fontsize=11,color='#123F63')
fig.tight_layout(); fig.savefig(D+'fig_share.png',dpi=200,bbox_inches='tight'); plt.close(fig)

# 图：全球市场规模
fig,ax=plt.subplots(figsize=(8.4,4.0))
lab=['2024年\nDRAM','2024年\nNAND','2025年第四季度\nDRAM','2025年第四季度\nNAND']
val=[974,696,519.65,235.45]
bars=ax.bar(range(4),val,0.5,color=[P[0],P[2],P[0],P[2]])
for i,v in enumerate(val):
    ax.text(i,v+18,f'{v:,.0f}' if v>=600 else f'{v:,.2f}',ha='center',fontsize=9)
ax.set_xticks(range(4)); ax.set_xticklabels(lab,fontsize=9)
ax.set_ylabel('市场规模（亿美元）'); ax.set_ylim(0,1150)
for s in ('top','right'): ax.spines[s].set_visible(False)
ax.grid(axis='y',linestyle='--',color='#DDDDDD'); ax.set_axisbelow(True)
ax.axvline(1.5,color='#CCCCCC',ls='--',lw=.9)
ax.text(0.5,1080,'年度口径',ha='center',fontsize=9,color='#666666')
ax.text(2.5,1080,'季度口径',ha='center',fontsize=9,color='#666666')
fig.tight_layout(); fig.savefig(D+'fig_size.png',dpi=200,bbox_inches='tight'); plt.close(fig)
print('两张图已生成')

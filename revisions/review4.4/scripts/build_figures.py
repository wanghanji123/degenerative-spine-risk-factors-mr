"""Publication figures from traceable tabular outputs; no generated data art."""
from pathlib import Path
import json,re
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,FancyArrowPatch
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'figures';OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'axes.titlesize':13,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'svg.fonttype':'none','savefig.facecolor':'white'})
COL={'BMI':'#237A82','Smoking initiation':'#AC4C60','IVDD':'#237A82','Spinal stenosis':'#B56330'}
def save(fig,n):
    for ext in ['png','pdf','svg']:fig.savefig(OUT/f'Figure{n}.{ext}',dpi=300,bbox_inches='tight')
    plt.close(fig)
def clean(ax):
    ax.axvline(1,color='#808080',lw=.9,ls='--',zorder=0)
    ax.set_xscale('log');ax.grid(axis='x',color='#E6E6E6',lw=.6);ax.set_axisbelow(True)
    ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())

fig,ax=plt.subplots(figsize=(10,6.4));ax.set_xlim(0,10);ax.set_ylim(0,6.4);ax.axis('off')
def box(x,y,w,h,title,body,color):
    ax.add_patch(Rectangle((x,y),w,h,facecolor='white',edgecolor=color,lw=1.4))
    ax.text(x+.15,y+h-.24,title,weight='bold',va='top',fontsize=11,color=color)
    ax.text(x+.15,y+h-.66,body,va='top',fontsize=10,linespacing=1.45)
def arrow(x,y,x2,y2):ax.add_patch(FancyArrowPatch((x,y),(x2,y2),arrowstyle='-|>',mutation_scale=13,lw=1.1,color='#666666'))
box(.15,4.7,4.6,1.5,'Exposure instruments','BMI: 501 SNPs\nSmoking initiation: 93 SNPs',COL['BMI'])
box(5.25,4.7,4.6,1.5,'Primary registry outcomes','FinnGen R5 IVDD: 20,001 cases\nSpinal stenosis: 9,169 cases\n164,682 controls for each endpoint',COL['Smoking initiation'])
box(.15,2.45,4.6,1.65,'Primary univariable analyses','480 BMI / 85 smoking SNPs per outcome\nIVW; four tests, alpha = 0.0125\nWeighted median; MR-Egger; diagnostics','#444444')
box(5.25,2.45,4.6,1.65,'Exploratory multivariable analyses','594 union SNPs; 1 coordinate exclusion\n501 joint-LD-selected candidates\n429 exact, nonpalindromic SNPs per outcome','#444444')
ax.plot([2.45,2.45,7.55,7.55],[4.7,4.4,4.4,4.7],color='#666666',lw=1.1)
arrow(2.45,4.4,2.45,4.12);arrow(7.55,4.4,7.55,4.12)
box(.15,.2,9.7,1.55,'Interpretation boundaries','Secondary: symptom endpoints, alternative adiposity, reverse MR, CAD comparison\nNo independent outcome replication; no measured zero-overlap claim\nMRlap corrections and unverified UKB pain ORs excluded from current inference','#444444')
arrow(2.45,2.45,2.45,1.77);arrow(7.55,2.45,7.55,1.77)
save(fig,1)

d=pd.read_csv(next((ROOT/'supplementary').glob('Supplementary_Table_S3_*.csv')))
oids=['finn-b-M13_INTERVERTEB','finn-b-M13_SPINSTENOSIS'];methods=['Inverse variance weighted','Weighted median','MR Egger']
fig,axes=plt.subplots(1,2,figsize=(10,4.6),sharey=True)
for ax,exp in zip(axes,['BMI','Smoking initiation']):
    labels=[]
    for k,oid in enumerate(oids):
        for j,m in enumerate(methods):
            r=d[(d.exposure_run==exp)&(d['id.outcome']==oid)&(d.method==m)].iloc[0];y=6-k*3.5-j
            ax.errorbar(r['or'],y,xerr=[[r['or']-r.ci95_lower],[r.ci95_upper-r['or']]],fmt=['s','o','^'][j],color=COL[exp],capsize=3,ms=6,lw=1.1)
            labels.append(('IVDD' if k==0 else 'Stenosis')+' | '+['IVW','Weighted median','MR-Egger'][j])
    ax.set_yticks([6,5,4,2.5,1.5,.5],labels);ax.tick_params(axis='y',length=0)
    ax.set_title(exp,weight='bold');clean(ax);ax.set_xlim(.45,5);ax.set_xticks([.5,1,2,4],[.5,1,2,4]);ax.set_xlabel('Odds ratio (95% CI)')
axes[0].set_xlabel('Per approximately 1-SD higher BMI');axes[1].set_xlabel('Per source-GWAS smoking-liability unit')
fig.tight_layout(w_pad=2);save(fig,2)

a=pd.read_csv(next((ROOT/'supplementary').glob('Supplementary_Table_S10_*.csv')))
ids=[x for x in a.exposure_id.drop_duplicates() if x!='ieu-a-999']
names=[a[a.exposure_id==x].exposure.iloc[0]+(' (UKB)' if x.startswith('ukb-') else ' (non-UKB)') for x in ids]
fig,ax=plt.subplots(figsize=(10,6.4))
for i,eid in enumerate(ids):
    for j,oid in enumerate(oids):
        r=a[(a.exposure_id==eid)&(a.outcome_id==oid)].iloc[0];v=[r.ivw_OR_verified,r.ivw_CI_lower_verified,r.ivw_CI_upper_verified];y=len(names)-i+(.12 if j==0 else -.12)
        ax.errorbar(v[0],y,xerr=[[v[0]-v[1]],[v[2]-v[0]]],fmt='o' if j==0 else 's',color=list(COL.values())[0] if j==0 else '#B56330',capsize=3,ms=5,label=['IVDD','Spinal stenosis'][j] if i==0 else None)
ax.set_yticks(range(1,len(names)+1),list(reversed(names)));ax.tick_params(axis='y',length=0);clean(ax);ax.set_xlim(.45,3.5);ax.set_xticks([.5,1,1.5,2,3],[.5,1,1.5,2,3]);ax.set_xlabel('IVW odds ratio (95% CI), per source-exposure unit');ax.legend(frameon=False,loc='lower center',bbox_to_anchor=(.5,1.02),ncol=2);fig.tight_layout();save(fig,3)

m=pd.read_csv(ROOT/'analysis/MVMR_repaired_results.csv');g=pd.read_csv(ROOT/'analysis/MVMR_repaired_covariance_grid.csv')
fig,(ax,bx)=plt.subplots(1,2,figsize=(10,4.8),gridspec_kw={'width_ratios':[1.05,1]})
labels=[]
for i,r in enumerate(m.to_dict('records')):
    y=4-i;ax.errorbar(r['OR'],y,xerr=[[r['OR']-r['CI_lower']],[r['CI_upper']-r['OR']]],fmt='o',color=COL[r['exposure']],capsize=3)
    labels.append(('BMI' if r['exposure']=='BMI' else 'Smoking')+' | '+('IVDD' if 'INTERVERTEB' in r['outcome_id'] else 'Stenosis'))
ax.set_yticks([4,3,2,1],labels);clean(ax);ax.set_xlim(.75,2);ax.set_xticks([.8,1,1.25,1.5,2],[.8,1,1.25,1.5,2]);ax.set_ylim(.3,4.7);ax.set_title('A  Exploratory direct estimates',loc='left',weight='bold');ax.set_xlabel('Odds ratio (95% CI); 429 SNPs')
for exp in ['BMI','Smoking initiation']:
    q=g[(g.exposure==exp)&(g.outcome_id==oids[0])];bx.plot(q.rho,q.conditional_F,label=exp,c=COL[exp],marker='o',ms=3)
bx.axhline(10,c='#555555',ls='--',lw=1);bx.set_yscale('log');bx.set_yticks([3,5,10,20,50,100],[3,5,10,20,50,100]);bx.set_xlabel('Assumed exposure-error\ncorrelation');bx.set_ylabel('Conditional F statistic');bx.set_title('B  Covariance sensitivity',loc='left',weight='bold');bx.legend(frameon=True,facecolor='white',edgecolor='white',framealpha=1,fontsize=10);bx.grid(axis='y',color='#E6E6E6');fig.tight_layout(w_pad=2);save(fig,4)
(OUT/'figure_source_manifest.json').write_text(json.dumps({'Figure1':'Design and verified sample/SNP counts','Figure2':'S3; primary weighted median fixed-seed 5000 bootstrap; Egger t-CI','Figure3':'S10 full-precision independently recalculated IVW confidence intervals; units differ by exposure','Figure4':'S19 and S27; exploratory, not independent effects established','formats':['PNG 300 dpi','vector PDF','editable SVG'],'image_generation_used':False},indent=2),encoding='utf-8')
print('Four figures generated from audited tables')

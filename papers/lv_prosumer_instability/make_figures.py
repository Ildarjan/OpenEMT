from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'figures'; OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.grid':True,'grid.alpha':.22,'svg.fonttype':'none','pdf.fonttype':42})
names=['unstable_100us','unstable_50us','unstable_25us','retuned_50us','stiff_50us','nine_only_50us']
D={n:np.genfromtxt(ROOT/'data'/f'{n}.csv',delimiter=',',names=True) for n in names}
def save(fig,name):
 fig.tight_layout()
 for ext in ['png','pdf','svg']: fig.savefig(OUT/f'{name}.{ext}',dpi=300,bbox_inches='tight')
 plt.close(fig)
def event(ax):
 ax.axvline(3,color='.35',ls=':',lw=1)
 ax.axvspan(3,3.15,color='grey',alpha=.1)
 ax.set_xlim(.5,5)
d=D['unstable_50us']; t=d['time_s']
fig,axs=plt.subplots(2,1,figsize=(7.2,5.2),sharex=True)
for ph,col in zip('abc',['#c33c36','#2478b4','#28834b']): axs[0].plot(t,d[f'V{ph}_rms_V'],label=f'Phase {ph.upper()}',color=col,lw=1.2)
axs[0].set_ylabel('Terminal voltage (V rms)');axs[0].legend(ncol=3,loc='upper left');axs[0].set_title('Remote inverter connection at 3.0 s')
axs[1].plot(t,d['P719_W']/1000,label='Active power',color='#2478b4')
axs[1].plot(t,d['Q719_var']/1000,label='Reactive power',color='#b87816')
axs[1].set_ylabel('P (kW), Q (kvar)');axs[1].set_xlabel('Time (s)');axs[1].legend()
for a in axs:event(a)
save(fig,'fig01_connection_response')
fig,axs=plt.subplots(2,1,figsize=(7.2,5.2),sharex=True)
for name,label,col in [('unstable_50us','Aggressive controller, weak feeder','#c33c36'),('retuned_50us','Reduced integral gains','#2478b4'),('stiff_50us','Feeder impedance divided by three','#28834b'),('nine_only_50us','Nine inverters, no connection','#777777')]:
 z=D[name];axs[0].plot(z['time_s'],z['Va_rms_V'],label=label,color=col,lw=1)
 axs[1].plot(z['time_s'],z['I719_rms_A'],label=label,color=col,lw=1)
axs[0].set_ylabel('Phase A voltage (V rms)');axs[0].legend(fontsize=8,loc='upper left')
axs[1].set_ylabel('Inverter current (A rms)');axs[1].set_xlabel('Time (s)')
for a in axs:event(a)
save(fig,'fig02_control_comparisons')
fig,ax=plt.subplots(figsize=(7.2,3.3))
for n,label in [('unstable_100us','100 microseconds'),('unstable_50us','50 microseconds'),('unstable_25us','25 microseconds')]:
 z=D[n];ax.plot(z['time_s'],z['Va_rms_V'],label=label,lw=1)
ax.set_xlim(3.2,5);ax.set_xlabel('Time (s)');ax.set_ylabel('Phase A voltage (V rms)');ax.legend();save(fig,'fig03_time_step_refinement')
metrics={}
for name,z in D.items():
 metrics[name]={}
 for window,lo,hi in [('pre',2.4,2.9),('early',3.4,4),('late',4.4,4.99)]:
  v=z['Va_rms_V'][(z['time_s']>=lo)&(z['time_s']<=hi)]
  metrics[name][window]={'min_V':float(v.min()),'max_V':float(v.max()),'span_V':float(np.ptp(v))}
(ROOT/'data'/'metrics.json').write_text(json.dumps(metrics,indent=2))
print(json.dumps(metrics,indent=2))

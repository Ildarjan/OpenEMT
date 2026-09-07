const fs = require('fs');
const path = require('path');
const {OpenEMT} = require('../../api/core');
const base = JSON.parse(fs.readFileSync(path.join(__dirname, '../../examples/lv_04kv_rooftop_pv.json')));
fs.mkdirSync(path.join(__dirname, 'data'), {recursive:true});
const cases = [['unstable_100us',100,'base'],['unstable_50us',50,'base'],['unstable_25us',25,'base'],['retuned_50us',50,'retuned'],['stiff_50us',50,'stiff'],['nine_only_50us',50,'nine']];
for(const [name,dt,mode] of cases){
 const c=JSON.parse(JSON.stringify(base));
 c.sim.dtUs=dt; c.sim.plotUs=250;
 const inv=c.blocks.find(b=>b.id===719);
 if(mode==='retuned') Object.assign(inv.params,{kiP:.2,kiQ:2});
 if(mode==='nine') inv.params.tConn=6000;
 if(mode==='stiff') c.blocks.filter(b=>b.type==='line'&&b.id>=200&&b.id<=204).forEach(b=>{b.params.R/=3;b.params.L/=3;});
 const em=new OpenEMT();em.loadCircuit(c);const run=em.runSimulation();
 if(run.err)throw new Error(name+': '+run.err);
 const get=(id,s)=>em.query(id,s,{runId:run.runId}).series;
 const v=get(105,'Vrms'),p=get(719,'P')[0],q=get(719,'Q')[0],i=get(719,'Irms')[0];
 const rows=['time_s,Va_rms_V,Vb_rms_V,Vc_rms_V,P719_W,Q719_var,I719_rms_A'];
 run.result.t.forEach((t,k)=>rows.push([t/1000,v[0][k],v[1][k],v[2][k],p[k],q[k],i[k]].join(',')));
 fs.writeFileSync(path.join(__dirname,'data',name+'.csv'),rows.join('\n')+'\n');
 fs.writeFileSync(path.join(__dirname,'data',name+'_circuit.json'),JSON.stringify(c,null,2));
 const span=(lo,hi)=>{const a=v[0].filter((_,k)=>run.result.t[k]>=lo&&run.result.t[k]<=hi);return Math.max(...a)-Math.min(...a);};
 console.log(JSON.stringify({name,pre:span(2400,2900),early:span(3400,4000),late:span(4400,4990)}));
}

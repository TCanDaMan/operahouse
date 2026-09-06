const assert=require('node:assert/strict');
const fs=require('node:fs');
const dsp=require('../web/room-audio.js');
const data=JSON.parse(fs.readFileSync('data/seats.json'));
const seats=data.seats;
for(const s of seats){
  assert.equal(s.aur.version,2);
  for(const key of ['singer','pit']){
    const a=s.aur[key];
    assert(a.bands.every(v=>Number.isFinite(v)&&v>=0));
    assert(a.tail_energy.every(v=>Number.isFinite(v)&&v>0));
    assert(a.r.every(t=>t[0]>=-0.1&&t[7].length===4&&t[7].every(v=>Number.isFinite(v)&&v>=0)));
    assert(a.tail_start_ms>=0);
  }
}
function energy(a){let v=0;for(const x of a){assert(Number.isFinite(x));v+=x*x;}return v;}
const fixture={id:'fixture',aur:{version:2,rt:[1.9,1.55,1.4,1.15]}};
fixture.aur.singer=fixture.aur.pit={t0:50,d:[.02,.02,0,0],bands:[.02,.02,.02,.02],r:[],tail_energy:[.002,.002,.002,.002],tail_start_ms:40,tail_rise_s:.025};
const center=dsp.build(fixture,'singer',48000,{directOnly:true});
assert.deepEqual(center.left,center.right,'center must be centered');
const pair=energy(center.left)+energy(center.right);
assert(Math.abs(pair-(.02*22)**2)<1e-6,'complementary bands must sum to unity');
const first=dsp.build(fixture,'singer',48000),repeat=dsp.build(fixture,'singer',48000);
assert.deepEqual(first.left,repeat.left,'repeated seat auditions must be identical');
for(const x of first.tailAudit)assert(Math.abs(x.rendered/x.target-1)<1e-12);
const old=fixture.aur.singer;
fixture.aur.singer={...old,d:[.02,.02,60,0]};
const right=dsp.build(fixture,'singer',48000,{directOnly:true});
fixture.aur.singer={...old,d:[.02,.02,-60,0]};
const left=dsp.build(fixture,'singer',48000,{directOnly:true});
assert.deepEqual(right.right,left.left);assert.deepEqual(right.left,left.right);
assert(energy(right.right)>energy(right.left),'right source must favor right ear');
assert(dsp.ears(90,0,3).itd>0.0006&&dsp.ears(90,0,3).itd<0.0007);
// Tail for the pit must not depend on the singer's direct pressure.
const pit1=dsp.build(fixture,'pit',44100);
fixture.aur.singer={...old,bands:[1,1,1,1],d:[1,1,0,0]};
assert.deepEqual(pit1.left,dsp.build(fixture,'pit',44100).left);
const selected=[];
for(const level of new Set(seats.map(s=>s.level))){const group=seats.filter(s=>s.level===level);selected.push(group[0],group.at(-1));}
for(const s of selected)for(const key of ['singer','pit']){
  const ir=dsp.build(s,key,44100);assert(energy(ir.left)+energy(ir.right)>0);
  assert(ir.tailAudit.every(a=>Math.abs(a.target-a.rendered)<1e-9));
}
assert.notDeepEqual(dsp.build(selected[0],'singer',44100).left,dsp.build(selected.at(-1),'singer',44100).left);
console.log(`PASS: ${seats.length} seat records; ${selected.length*2} rendered source/seat responses; determinism, stereo direction, energy, sample rates and source independence.`);
// Estimate RT from the actual synthesized waveform's backward energy integral.
const decaySeat=JSON.parse(JSON.stringify(fixture));
for(const k of ['singer','pit'])decaySeat.aur[k]={...old,bands:[0,0,0,0],d:[0,0,0,0],tail_energy:[0,.002,0,0]};
decaySeat.aur.rt=[1.4,1.4,1.4,1.4];
const decay=dsp.build(decaySeat,'singer',48000);
const sch=new Float64Array(decay.left.length);let sum=0;
for(let i=sch.length-1;i>=0;i--){sum+=decay.left[i]**2+decay.right[i]**2;sch[i]=sum;}
const crossing=db=>sch.findIndex(v=>v<=sum*Math.pow(10,db/10))/48000;
const measuredRT=(crossing(-25)-crossing(-5))*3;
assert(Math.abs(measuredRT-1.4)<.12,`decay RT ${measuredRT} should follow 1.4 s input`);
assert(Math.abs(sum-.002*22*22*.36)<1e-6,'actual summed stereo samples conserve tail energy');
console.log(`PASS: rendered T20 extrapolation ${measuredRT.toFixed(3)} s for 1.4 s input, with measured stereo tail energy.`);

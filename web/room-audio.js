/* Seat-specific impulse response synthesis. No browser dependencies: tested in Node.
 * Four broad frequency bands, approximate spherical-head ITD/ILD (not measured HRTFs).
 * All gains share one reference across seats; summed L/R late energy is conserved.
 */
(function(root){
  'use strict';
  const AMP = 22, TAPS = 129;
  function random(seed){
    let s = seed >>> 0;
    return () => { s ^= s << 13; s ^= s >>> 17; s ^= s << 5; return (s >>> 0)/4294967296*2-1; };
  }
  function lowpass(sr, hz){
    const h = new Float64Array(TAPS), m = (TAPS-1)/2, f = hz/sr;
    let total=0;
    for(let i=0;i<TAPS;i++){
      const x=i-m;
      h[i]=(x===0 ? 2*f : Math.sin(2*Math.PI*f*x)/(Math.PI*x)) * (0.42-0.5*Math.cos(2*Math.PI*i/(TAPS-1))+0.08*Math.cos(4*Math.PI*i/(TAPS-1)));
      total+=h[i];
    }
    return h.map(v=>v/total);
  }
  const filterCache = new Map();
  function filters(sr){
    if(filterCache.has(sr)) return filterCache.get(sr);
    const lo=[250,1000,3200].map(f=>lowpass(sr,Math.min(f,sr*.45)));
    const bands=Array.from({length:4},()=>new Float64Array(TAPS));
    for(let i=0;i<TAPS;i++){
      bands[0][i]=lo[0][i]; bands[1][i]=lo[1][i]-lo[0][i];
      bands[2][i]=lo[2][i]-lo[1][i]; bands[3][i]=(i===(TAPS-1)/2?1:0)-lo[2][i];
    }
    filterCache.set(sr,bands); return bands;
  }
  function ears(az, el, band){
    const lateral=Math.sin(az*Math.PI/180)*Math.cos(el*Math.PI/180);
    const theta=Math.asin(Math.min(1,Math.abs(lateral)));
    const itd=0.0875/343*(theta+Math.sin(theta))*Math.sign(lateral);
    // Head shadow increases with frequency. Near ear is never arbitrarily muted.
    const shadow=Math.pow(10,-[0.5,2,6,10][band]*Math.abs(lateral)/20);
    let l=lateral>0?shadow:1, r=lateral<0?shadow:1;
    const scale=1/Math.hypot(l,r); l*=scale; r*=scale;
    return {l,r,itd};
  }
  function addKernel(out,h,sample,gain){
    const n=Math.floor(sample), f=sample-n;
    for(let i=0;i<h.length;i++){
      if(n+i>=0 && n+i<out.length) out[n+i]+=gain*h[i]*(1-f);
      if(n+i+1>=0 && n+i+1<out.length) out[n+i+1]+=gain*h[i]*f;
    }
  }
  // Fast RBJ band noise, energy normalized AFTER filtering and decay shaping.
  function bandNoise(n,sr,b,seed){
    const rnd=random(seed), f=[180,600,2000,4500][b], w=2*Math.PI*Math.min(f,sr*.45)/sr;
    const c=Math.cos(w), alpha=Math.sin(w)/(2*.707), a0=1+alpha;
    let b0,b1,b2;
    if(b===0){ b0=(1-c)/2; b1=1-c; b2=b0; }
    else if(b===3){ b0=(1+c)/2; b1=-(1+c); b2=b0; }
    else { b0=alpha; b1=0; b2=-alpha; }
    const a1=-2*c/a0,a2=(1-alpha)/a0; b0/=a0;b1/=a0;b2/=a0;
    const out=new Float32Array(n);let x1=0,x2=0,y1=0,y2=0;
    for(let i=0;i<n;i++){const x=rnd(),y=b0*x+b1*x1+b2*x2-a1*y1-a2*y2;out[i]=y;x2=x1;x1=x;y2=y1;y1=y;}
    return out;
  }
  function build(seat,key,sr,options={}){
    const a=seat.aur,src=a[key];
    if(a.version!==2) throw new Error('Rebuild seat data for audio engine v2.');
    const rt=a.rt, base=8+src.t0-Math.min(a.singer.t0,a.pit.t0);
    const latest=Math.max(src.tail_start_ms,...src.r.map(t=>t[0]));
    const len=Math.ceil(sr*((base+latest)/1000+Math.max(...rt)*1.25))+TAPS;
    const L=new Float32Array(len), R=new Float32Array(len), hs=filters(sr);
    const taps=[{t:0,bands:src.bands,az:src.d[2],el:src.d[3]}];
    if(!options.directOnly) for(const t of src.r) taps.push({t:t[0],bands:t[7],az:t[3],el:t[4]});
    for(const t of taps) for(let b=0;b<4;b++){
      const e=ears(t.az,t.el,b),n=(base+t.t)/1000*sr,g=t.bands[b]*AMP;
      addKernel(L,hs[b],n+Math.max(0,e.itd)*sr,g*e.l);
      addKernel(R,hs[b],n+Math.max(0,-e.itd)*sr,g*e.r);
    }
    const audit=[];
    if(!options.directOnly){
      const start=Math.round((base+src.tail_start_ms)/1000*sr)+(TAPS-1)/2;
      // Broad-band audition weights; these do not redefine octave-band metrics.
      const weights=[.16,.36,.33,.15];
      for(let b=0;b<4;b++){
        const channels=[]; let total=0;
        for(let ch=0;ch<2;ch++){
          // Same diffuse field for every seat: geometry/gain changes, not random timbre.
          const noise=bandNoise(len-start,sr,b,0x51f15e+7919*b+104729*ch+(key==='pit'?65537:0));
          for(let i=0;i<noise.length;i++){
            const t=i/sr; noise[i]*=Math.exp(-3*Math.log(10)*t/rt[b])*(1-Math.exp(-t/src.tail_rise_s));
            total+=noise[i]*noise[i];
          }
          channels.push(noise);
        }
        const target=src.tail_energy[b]*AMP*AMP*weights[b];
        const gain=Math.sqrt(target/Math.max(total,1e-30));
        channels.forEach((noise,ch)=>{const out=ch?R:L;for(let i=0;i<noise.length;i++)out[start+i]+=noise[i]*gain;});
        audit.push({band:b,target,rendered:total*gain*gain});
      }
    }
    return {left:L,right:R,sampleRate:sr,tailAudit:audit};
  }
  const api={build,ears,filters};
  if(typeof module!=='undefined') module.exports=api;
  else root.RoomAudio=api;
})(globalThis);

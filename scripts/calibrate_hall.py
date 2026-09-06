"""Reproducible audit of legacy angular observations; no production geometry writes."""
import contextlib,io,json,runpy,sys
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares
ROOT=Path(__file__).resolve().parents[1]
sys.argv=[str(ROOT/'scripts/solve_pano_poses.py')]
with contextlib.redirect_stdout(io.StringIO()):
 legacy=runpy.run_path(sys.argv[0])
obs=legacy['OBS']; names=legacy['PANOS']; project=legacy['project']; unpack=legacy['unpack']; initial=legacy['p0']
def solve(pitch_sigma=1,lip_z=-4.33,omit=None):
 def residual(p):
  cams,apex,left,right,chan=unpack(p); r=[]
  features={'val':[0,35,0],'apex':[0,apex,0],'lip':[0,3.5,lip_z],'scrL':left,'scrR':right,'chan':chan}
  for n,f,az,el in obs:
   if f==omit:continue
   cam=cams[n]; X=[-26 if f=='pilL' else 26,cam[1],0] if f in ('pilL','pilR') else features[f]
   a,e=project(cam,np.array(X));r.append(((a-az+180)%360-180)/legacy['SIG'][n])
   if el is not None:r.append((e-el)/legacy['SIG'][n])
  return np.r_[r,[cams[n][4]/pitch_sigma for n in names]]
 fit=least_squares(residual,initial,loss='soft_l1',max_nfev=3000)
 cams,apex,left,right,chan=unpack(fit.x); records=[]
 for n,f,az,el in obs:
  cam=cams[n];features={'val':[0,35,0],'apex':[0,apex,0],'lip':[0,3.5,lip_z],'scrL':left,'scrR':right,'chan':chan}
  X=[-26 if f=='pilL' else 26,cam[1],0] if f in ('pilL','pilR') else features[f]
  a,e=project(cam,np.array(X));records.append(dict(camera=n,feature=f,observed=[az,el],predicted=[a,e if el is not None else None],error_deg=[(a-az+180)%360-180,e-el if el is not None else None],held_out=f==omit))
 errors=[v for r in records if not r['held_out'] for v in r['error_deg'] if v is not None]
 return dict(success=bool(fit.success),rms_deg=float(np.sqrt(np.mean(np.square(errors)))),cameras={n:list(map(float,cams[n])) for n in names},observations=records,apex_y=float(apex))
base=solve();variants={str(s):solve(s) for s in [.5,2,5]};sign=solve(lip_z=4.33);holdout=solve(omit='lip')
out={'units':'feet; x across, y up, z toward rear; camera arrays x,y,z,heading_deg,pitch_deg','status':'Diagnostic fit of legacy hand-read angles. Panorama pixel origin and feature identity not independently verified. Not a calibrated hall shell.','baseline':base,'pitch_sensitivity':variants,'positive_lip_z_test':sign,'held_out_lip':holdout}
(ROOT/'data/calibration_audit.json').write_text(json.dumps(out,indent=2)+'\n')
print('Baseline RMS degrees',base['rms_deg'],'positive lip test',sign['rms_deg'])
for n in names:
 depths=[base['cameras'][n][2]]+[v['cameras'][n][2] for v in variants.values()]
 print(n,'depth',round(depths[0],1),'pitch-prior range',round(min(depths),1),round(max(depths),1))

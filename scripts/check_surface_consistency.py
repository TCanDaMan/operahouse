"""Regression checks for upper-tier footprint/render agreement."""
import contextlib,io,runpy
from pathlib import Path
root=Path(__file__).resolve().parents[1]
with contextlib.redirect_stdout(io.StringIO()): m=runpy.run_path(str(root/'scripts/build_seats.py'))
t=m['shell']['tiers'][1]; contains=m['_upper_contains'];soffit=m['_upper_soffit']
for i,(x,front) in enumerate(t['rail']['arc']):
 rear=t['rows'][-1]['arc'][i][1]+4
 assert not contains(x,front-.1),(x,'front')
 assert contains(x,front+.1),(x,'inside')
 assert not contains(x,rear+.1),(x,'rear')
 for r in t['rows']:
  z=r['arc'][i][1]
  expected=t['soffit_lip_y']+t['slope']*(r['z']-t['rail']['z'])
  assert abs(soffit(x,z)-expected)<.02,(x,z)
assert not contains(50,40),'Removed gallery must not occlude front orchestra'
assert not contains(m['HALF_BREADTH']+1,130),'Outside auditorium'
assert len(m['seats'])==3006
assert not m['shell']['balcony_sweep']['enabled']
print('PASS: 81 upper-deck sections match footprint and soffit; phantom gallery excluded; 3,006 seats.')

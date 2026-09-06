"""Digitized section audit. Coordinates refer to the unresized 1990×1312 source."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
# Manual picks from the source drawing, not from a browser-scaled screenshot.
# Retain pixel uncertainty and datum ambiguity rather than fitting model to itself.
r={'source':'sources/research/beranek1996/p159_section_zoom.png','image_size':[1990,1312],
 'method':'manual visual digitization; schematic section, not survey drawing',
 'scale_anchors':[{'feet':0,'pixel_x':868},{'feet':90,'pixel_x':1592}],
 'stage_floor_pixel_y':754,'stage_height_ft':3.5,
 'curtain_candidate_pixel_x':1500,'proscenium_candidate_pixel_x':1450,
 'pixel_pick_uncertainty':8,'datum_status':'Two visible verticals; curtain identity requires independent plan confirmation.',
 'features':{
 'box_front_floor':[888,636], 'grand_tier_front_floor':[897,548],
 'grand_tier_rear_floor':[448,420], 'balcony_front_floor':[869,369],
 'balcony_rear_floor':[290,151], 'dome_apex':[1210,168],
 'rear_ceiling':[300,65]},
 'profiles':{'boxes':[[735,636],[888,636]],'lower_tier':[[448,420],[897,548]],'upper_tier':[[290,151],[869,369]],'ceiling':[[230,65],[350,65],[510,92],[650,144],[795,208],[905,178],[1210,168],[1430,211]]}}
scale=(1592-868)/90;r['pixels_per_foot']=scale;r['floor_origin_pixel_y']=754+3.5*scale
for name,p in list(r['features'].items()):
 r['features'][name]={'pixel':p,'depth_ft':(1500-p[0])/scale,'height_ft':(r['floor_origin_pixel_y']-p[1])/scale,'depth_with_alternate_datum_ft':(1450-p[0])/scale}
s=json.loads((ROOT/'data/seats.json').read_text());t=s['shell']['tiers'];b=s['shell']['boxes'];center=min(b['rail'],key=lambda p:abs(p[0]))
compare={'box_front_floor':(center[1],b['floor_y']),'grand_tier_front_floor':(t[0]['rail']['z'],t[0]['rail']['y']),'balcony_front_floor':(t[1]['rail']['z'],t[1]['rail']['y'])}
r['comparison']={k:{'model_depth_ft':v[0],'model_height_ft':v[1],'depth_difference_ft':v[0]-r['features'][k]['depth_ft'],'height_difference_ft':v[1]-r['features'][k]['height_ft']} for k,v in compare.items()}
(ROOT/'data/section_registration.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r['comparison'],indent=2))

#!/usr/bin/env python3
"""Import the SF Opera / Adage SmartSeat seat map into a flat CSV.

Fetches (or reads from sources/smartseat/) the four venue levels of the
War Memorial Opera House seat map: every seat's section, row, seat number,
price zone, live price, plan glyph position in the map's SVG frame, and
the id of the seat-view photo the map shows for that seat.

Usage:
  scripts/import_smartseat.py                # read sources/smartseat/level*.json
  scripts/import_smartseat.py --fetch 7995   # fetch fresh for itemNumber 7995
                                             # (the itemNumber in a sfopera.com
                                             # /smartseat/?itemNumber=... link)

Output: data/seats_smartseat.csv

Notes on the plan coordinates: each level is drawn in its own 1900x1200
frame and the drawings are schematic (row spacing is not to scale between
levels), so x/y are useful for row shape, aisle positions and seat order,
not for metric row pitch.
"""
import csv, json, re, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'sources' / 'smartseat'
OUT = ROOT / 'data' / 'seats_smartseat.csv'
API = 'https://www.sfopera.com/api/seating/GetSeatmap'
VIEW_URL = 'https://www.sfopera.com/api/seating/GetSeatViewImageFile?seatViewImageId='
LEVELS = {0: 'orchestra', 1: 'boxes', 2: 'lower_tier', 3: 'upper_tier'}
SECTION_KEY = {'Orchestra': 'orchestra', 'Box': 'boxes', 'Grand Tier': 'grand_tier',
               'Dress Circle': 'dress_circle', 'Balcony Circle': 'balcony_circle',
               'Balcony': 'balcony'}

def fetch_level(item, level):
    body = {"itemType": 0, "itemId": int(item), "minPrice": 0, "maxPrice": 9999,
            "allowSeparatedSeats": False,
            "priceTypeQuantities": [{"priceTypeId": 1, "quantity": 1}],
            "venueLevels": [level], "selectedAllLevels": False,
            "allowAisleAccessSelected": False, "additionalSeatingOptions": [],
            "language": "en-US", "seatsToIgnore": [], "isSyosOnly": False}
    req = urllib.request.Request(API, data=json.dumps(body).encode(),
                                 headers={'Accept': 'application/json',
                                          'Content-Type': 'application/json',
                                          'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

_tok = re.compile(r'[MmLlHhVvCcSsQqTtAaZz]|-?\d*\.?\d+(?:e-?\d+)?')
def path_bbox_centre(d):
    toks = _tok.findall(d); i = 0; cmd = None; x = y = 0; pts = []
    need = {'M': 2, 'L': 2, 'H': 1, 'V': 1, 'C': 6, 'S': 4, 'Q': 4, 'T': 2, 'A': 7}
    while i < len(toks):
        if toks[i].isalpha():
            cmd = toks[i]; i += 1
            if cmd in 'Zz':
                continue
        n = need[cmd.upper()]; args = [float(v) for v in toks[i:i + n]]; i += n
        rel = cmd.islower(); c = cmd.upper()
        if c == 'H': x = (x if rel else 0) + args[0]
        elif c == 'V': y = (y if rel else 0) + args[0]
        elif c == 'A': x = (x if rel else 0) + args[5]; y = (y if rel else 0) + args[6]
        else: x = (x if rel else 0) + args[-2]; y = (y if rel else 0) + args[-1]
        pts.append((x, y))
        if c == 'M': cmd = 'l' if rel else 'L'
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2

def main():
    fetch = '--fetch' in sys.argv
    item = sys.argv[sys.argv.index('--fetch') + 1] if fetch else None
    rows = []
    for lv, lvname in LEVELS.items():
        if fetch:
            j = fetch_level(item, lv)
            SRC.mkdir(parents=True, exist_ok=True)
            (SRC / f'level{lv}.json').write_text(json.dumps(j))
        else:
            j = json.load(open(SRC / f'level{lv}.json'))
        pricing = {p['zoneId']: p for p in j.get('allSeatPricing', [])}
        for s in j['levelSeats']:
            t = s['tessituraSeat']
            pr = pricing.get(t['zoneId'], {}).get('prices') or []
            price = next((p['price'] for p in pr if p.get('priceTypeId') == 1), pr[0]['price'] if pr else None)
            cx, cy = path_bbox_centre(s['svgPath'])
            sec = t['sectionDescription']
            rows.append(dict(
                level=lvname, section=SECTION_KEY.get(sec, sec.lower()),
                row=t['rowText'].replace('Row ', '').strip(),
                seat=t['numberText'].replace('Seat ', '').strip(),
                zone=s['zoneDescription'], zone_id=t['zoneId'], price=price,
                map_x=round(cx, 2), map_y=round(cy, 2),
                seat_type=t['seatType'], aisle=t['aisle'],
                view_image_id=s.get('seatViewImageId') or '',
                tessitura_seat=t['seatNumber'], seat_id=s['seatId']))
    OUT.parent.mkdir(exist_ok=True)
    with open(OUT, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    views = {r['view_image_id'] for r in rows if r['view_image_id']}
    print(f'{len(rows)} seats -> {OUT.relative_to(ROOT)}; {len(views)} seat-view images '
          f'(fetch with {VIEW_URL}<id>)')

if __name__ == '__main__':
    main()

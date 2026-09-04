# War Memorial Opera House seat model

A seat-by-seat 3D model of the War Memorial Opera House (San Francisco) built
to answer one question: which seat is the best value for a given performance,
once you account for what is above you, how far off-axis you sit, whether the
tier in front clips the top of the stage picture, and whether you can see
into the pit. The reference staging is Wagner's *Die Walküre* (SF Opera,
fall 2027; full Ring cycles June 2028).

Open `web/index.html` in a browser. It is self-contained.

## How the house is stacked

Three tiers sit above the rear of the orchestra:

| Level | Rows | What is above it |
|---|---|---|
| Orchestra | A–ZZ | box ring over about the last ten rows (S–ZZ at centre, R–ZZ at the sides) and the standing room |
| Boxes | ring A–Z | the Grand Tier slab, set just behind the rear boxes |
| Grand Tier | AA–EE | nothing: open to the ceiling |
| Dress Circle | A–L | Balcony, whose lip lands over row A |
| Balcony Circle + Balcony | AA–EE, A–L | nothing but the dome |

Grand Tier and Dress Circle are one continuous slab: five rows along the
front rail, the cross-aisle at the 2nd-floor doors, then eleven rows rising
to the 3rd-floor doors, with the Balcony overhang beginning right at the
first Dress Circle row. Balcony Circle and Balcony are the same arrangement
one level up, with no overhang at all. Evidence for all of this is in
`sources/CALIBRATION.md`.

## What the model says about Grand Tier vs Dress Circle

The overhang line and the price line coincide here, which is unusual: every
Grand Tier row is open to the ceiling, and the Balcony lip starts at Dress
Circle A. So "one row back" from Grand Tier EE into Dress Circle A is the one
step that actually changes what is above you. Within the Dress Circle the
premium/standard boundary at rows B/C changes nothing.

Model output for the centre seats:

| Seat | Above you | Opening angle | Depth ÷ opening | Score |
|---|---|---|---|---|
| Grand Tier AA | open | open | – | 73 |
| Grand Tier EE | open | open | – | 67 |
| Dress Circle A | Balcony, lip 4 ft in front | 81° | 0.3 | 63 |
| Dress Circle C | Balcony | 56° | 0.6 | 60 |
| Dress Circle E | Balcony | 37° | 0.9 | 52 |
| Dress Circle G | Balcony | 25° | 1.3 | 49 |
| Dress Circle J | Balcony | 18° | 1.6 | 39 |
| Dress Circle L | Balcony | 13° | 1.9 | 31 |

Beranek's rule of thumb for opera houses is depth ÷ opening below about 2
and an opening angle that keeps the ceiling in play. Under this model the
Balcony soffit is high (about 14 ft over the eyes), so the front half of the
Dress Circle keeps a wide opening; the loss is gradual and becomes real
around row G, where the opening drops below 25° and the ceiling reflection
is gone. No Dress Circle row loses the top of the proscenium.

Conclusion for "one row back, half the price":

- Grand Tier EE versus Dress Circle A or B at a much lower price: the
  Dress Circle seat is 7 ft further back and gains a lip 4 ft in front of
  it, but the lip is high and the opening is still 80°. For most operas that
  is a good trade. For Walküre, where the top of the picture matters, both
  keep the full proscenium.
- Dress Circle B (premium) versus C (standard): take C. Same conditions.
- Dress Circle D versus E, and anything from G back: the discount is paying
  for a real loss.
- The rear orchestra under the box ring (about W–ZZ) is the most compromised
  seating in the house for its price: 4 ft of soffit over the eyes, an
  opening under 20°, and from row Y back the model predicts the top of the
  proscenium is hidden. That last prediction is unverified.
- If sound is the priority, the Balcony Circle front rows are open to the
  dome, 110 ft from the singer, with the pit fully visible, at a third of
  the Grand Tier price.

The far side blocks are a separate story: Grand Tier 29–40 and Dress Circle
seats past about 20 lose part of the stage width behind the proscenium
edge, reported as "stage width visible".

## What is published and what is fitted

Published (War Memorial technical specifications, `sources/`): auditorium
113 ft wide, 74 ft high, 116 ft deep at orchestra level and 161 ft at balcony
level; proscenium 52 ft wide, valence 31 ft 6 in; stage 3 ft 6 in above the
house floor; curtain line to pit apron 4 ft 4 in; pit 19 ft 10 in front to
back with the floor 6 ft 8 in to 8 ft 2 in below the stage; pit capacity 90;
**Grand Tier lighting rail 80 ft from the footlights**.

Transcribed (seat charts): every row and seat number on every level,
including wheelchair platforms, companion and transfer seats, the sound
position in Dress Circle row K and the followspot gap in Balcony rows A–B.
Total 3,006 seats. The published orchestra count (1,174) is larger than the
current chart (1,078); the chart is what SF Opera sells today.

Fitted to photographs (`sources/CALIBRATION.md`): which rows each tier
covers and the tier heights, chosen so that the seven SF Opera seat photos
and the tour frames come out right (Dress Circle J keeps the full
proscenium arch; standing room fits under the box ring; the Balcony lip
lands over Dress Circle A). Row pitch, the plan offset between the two slab
rails, and the box ring's position at centre remain estimates, each marked
in `data/house_geometry.json`.

Price zones follow SF Opera's zone map. Zone prices in
`data/seating_spec.py` are placeholders inside the ranges SF Opera showed
for the Nov 27 2026 *Figaro*; replace them with the performance you are
pricing and rebuild.

## Metrics per seat

Computed by `scripts/build_seats.py` into `data/seats.json` and
`data/seats.csv`:

- distance to a downstage singer and to the pit; off-axis angle; elevation
- the lowest overhang above the seat, its lip distance, headroom over the
  eyes, opening height at the lip, depth ÷ opening, and the opening angle
  between the singer and the lip
- whether the lip clips the top of the proscenium and how much remains
- stage width visible through the proscenium at 25 ft upstage
- fraction of the pit floor visible over the pit rail
- whether the first-order ceiling reflection from the singer and from the
  pit reaches the seat (image-source check against the overhang)
- direct-sound level relative to orchestra row A (inverse square)
- a 0–100 view score combining the above, and score per dollar

The score weights are opinions, written in `view_score()`.

## Layout of the repository

- `sources/` the spec sheet, the two seat-chart PDFs, and `calibration/`
  with the tour and seat-view photographs the geometry was fitted to
- `data/house_geometry.json` every dimension with its source and confidence
- `data/seating_spec.py` the seat inventory and price zones
- `scripts/build_seats.py` placement, metrics, and viewer build
- `web/template.html` the viewer; `web/index.html` is generated with the data inlined

Deep links: `web/index.html?seat=dress_circle:L:105&view=sit` opens sitting
in that seat looking at the stage. Views: `overview`, `top`, `section`,
`stagefront`, `sit`.

## Not modelled

Wave acoustics. The geometric checks above (direct level, overhang, ceiling
reflection) are the part of acoustics that seat choice actually changes; the
hall's reverberation is the same for everyone. Heads in the row in front are
not modelled because the row-to-row rise is not published. The ceiling is a
flat plane at the dome height; the lower cove over the rear Balcony rows is
not drawn.

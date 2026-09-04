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
| Grand Tier | AA–EE | open to the ceiling except row EE, where the Balcony lip lands |
| Dress Circle | A–L | Balcony |
| Balcony Circle + Balcony | AA–EE, A–L | nothing but the dome |

Grand Tier and Dress Circle are one continuous slab: five rows along the
front rail, the cross-aisle at the 2nd-floor doors, then eleven rows rising
to the 3rd-floor doors, with the Balcony overhang beginning about 8 ft behind
the Grand Tier rail (Beranek's 1931 section), i.e. over row EE. Balcony Circle and Balcony are the same arrangement
one level up, with no overhang at all. Evidence for all of this is in
`sources/CALIBRATION.md`.

## What the model says about Grand Tier vs Dress Circle

The overhang line and the price line nearly coincide: Grand Tier AA–DD are open
to the ceiling, the Balcony lip lands over Grand Tier EE, and from Dress Circle
A back the opening closes quickly. So the last Grand Tier row is already under
the lip, and "one row back" into Dress Circle A roughly halves the opening angle
again. Within the Dress Circle the premium/standard boundary at rows B/C changes
little.

Model output for the centre seats:

| Seat | Above you | Opening angle | Depth ÷ opening | Score |
|---|---|---|---|---|
| Grand Tier AA | open | open | – | 74 |
| Grand Tier EE | Balcony, lip 5.7 ft in front | 79° | 0.3 | 67 |
| Dress Circle A | Balcony, lip 12.6 ft in front | 54° | 0.7 | 58 |
| Dress Circle C | Balcony | 38° | 1.0 | 55 |
| Dress Circle E | Balcony | 28° | 1.3 | 52 |
| Dress Circle G | Balcony | 21° | 1.7 | 44 |
| Dress Circle J | Balcony | 16° | 2.0 | 37 |
| Dress Circle L | Balcony | 13° | 2.3 | 37 |

Beranek's rule of thumb for opera houses is depth ÷ opening below about 2
and an opening angle that keeps the ceiling in play. With the section-derived heights the
Balcony soffit is about 9 ft over the eyes at Dress Circle A and the lip is 8 ft
behind the Grand Tier rail, so the opening closes faster than the earlier
photo-fitted model said: 54° at row A, 38° at C, under 25° from row G, and
depth ÷ opening passes 2 at row J. No Dress Circle row loses the top of the
proscenium, which matches the row J seat photo.

Conclusion for "one row back, half the price":

- Grand Tier EE versus Dress Circle A or B at a much lower price: EE is
  already under the lip with a 79° opening; Dress Circle A is 7 ft further
  back with a 54° opening. Still a fair trade for most operas, but it is no
  longer a free one. For Walküre, where the top of the picture matters, both
  keep the full proscenium.
- Dress Circle B (premium) versus C (standard): take C. Nearly the same conditions.
- Dress Circle D versus E, and anything from G back: the discount is paying
  for a real loss.
- The rear orchestra under the box ring (about W–ZZ) is still compromised
  for its price, but less than the earlier model said: the box soffit is
  about 16 ft up (1931 section), giving a 33° opening at W and 17° at ZZ.
  At centre the top of the proscenium stays visible, which the SF Opera
  seat photo for the centre rear block confirms; the side rear blocks'
  photos show the soffit clipping the arch, which the model does not yet
  capture (the ring is lower toward the sides).
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

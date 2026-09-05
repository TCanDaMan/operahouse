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
| Orchestra | A–ZZ | box ring over the outer seats of rows S–ZZ and the standing room; the Grand Tier slab over the last rows at centre |
| Boxes | ring A–Z | the Grand Tier slab over the rear boxes; the side slips over the side boxes |
| Grand Tier | AA–EE | nothing: open to the ceiling |
| Dress Circle | A–L | Balcony, whose lip lands over rows B–C (25 ft behind the Grand Tier rail at centre, 20 ft at the sides) |
| Balcony Circle + Balcony | AA–EE, A–L | nothing but the dome |

Grand Tier and Dress Circle are one continuous slab: five rows along the
front rail, the cross-aisle at the 2nd-floor doors, then eleven rows rising
to the 3rd-floor doors, with the Balcony overhang beginning 25 ft behind the
Grand Tier rail at centre (1993 plans), i.e. over Dress Circle row B–C. Balcony Circle and Balcony are the same arrangement
one level up, with no overhang at all. Evidence for all of this is in
`sources/CALIBRATION.md`.

## What the model says about Grand Tier vs Dress Circle

The overhang line sits two rows behind the price line: every Grand Tier row
and Dress Circle A are open to the ceiling, and the Balcony lip lands over
Dress Circle B–C. So "one row back" from Grand Tier EE into Dress Circle A
changes nothing above you; the step that matters is B into C, where the
premium/standard boundary also falls.

Model output for the centre seats:

| Seat | Above you | Opening angle | Depth ÷ opening | Score |
|---|---|---|---|---|
| Grand Tier AA | open | open | – | 76 |
| Grand Tier EE | open | open | – | 70 |
| Dress Circle A | open | open | – | 67 |
| Dress Circle C | Balcony, lip 0.5 ft in front | 102° | 0.0 | 64 |
| Dress Circle E | Balcony | 59° | 0.5 | 61 |
| Dress Circle G | Balcony | 29° | 1.0 | 52 |
| Dress Circle J | Balcony | 18° | 1.4 | 42 |
| Dress Circle L | Balcony | 11° | 1.9 | 32 |

Beranek's rule of thumb for opera houses is depth ÷ opening below about 2
and an opening angle that keeps the ceiling in play. With the plan-traced Balcony front and the section-derived heights, the
soffit is about 8.4 ft over the eyes at Dress Circle C right under the lip; the
opening is still 102° there, 59° at E, 29° at G, 18° at J and 11° at L, and
depth ÷ opening passes 2 only at row L. No Dress Circle row loses the top of
the proscenium, which matches the row J seat photo.

Conclusion for "one row back, half the price":

- Grand Tier EE versus Dress Circle A at a much lower price: both are open
  to the ceiling; A is 7 ft further back. For most operas that is a good trade. For Walküre, where the top of the picture matters, both
  keep the full proscenium.
- Dress Circle B (premium) versus C (standard): C is the first row under the
  lip, but the lip is right overhead and the opening is still wide. Take C.
- Dress Circle D versus E, and anything from G back: the discount is paying
  for a real loss.
- The rear orchestra: at centre the last rows (S–ZZ) sit under the Grand
  Tier slab, whose soffit is about 25 ft up, with the box ring 97 ft back
  behind them; the view stays open and the proscenium top is never hidden,
  which the centre rear seat photo confirms. The outer seats of the same rows
  are under the ring's legs (soffit about 13 ft), and there the side seat
  photo shows the arch clipped; the model gives those seats a 20–25° opening.
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

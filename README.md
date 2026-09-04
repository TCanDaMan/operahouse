# War Memorial Opera House seat model

A seat-by-seat 3D model of the War Memorial Opera House (San Francisco) built
to answer one question: which seat is the best value for a given performance,
once you account for what is above you, how far off-axis you sit, whether the
tier in front clips the top of the stage picture, and whether you can see
into the pit. The reference staging is Wagner's *Die Walküre* (SF Opera,
fall 2027; full Ring cycles June 2028).

Open `web/index.html` in a browser. It is self-contained.

## How the house is stacked

Four tiers sit above the rear of the orchestra, each on its own slab:

| Level | Rows | What is above it |
|---|---|---|
| Orchestra | A–ZZ | box ring over roughly rows W–ZZ and the standing room |
| Boxes | ring A–Z | Grand Tier over the rear-centre boxes |
| Grand Tier | AA–EE | Dress Circle, a low flat soffit from row BB back |
| Dress Circle | A–L | Balcony from row B back |
| Balcony Circle + Balcony | AA–EE, A–L | nothing but the dome |

The Grand Tier and Dress Circle are separate floors about ten feet apart
(spec sheet: 2nd and 3rd floor; tour panorama from the Grand Tier shows five
rows rising to a rear wall under the Dress Circle's soffit). The Balcony
Circle and Balcony are one continuous open tier. Evidence for all of this is
in `sources/CALIBRATION.md`.

## What the model says about Grand Tier vs Dress Circle

The two are different animals, and the price map does not follow the
geometry:

- **Grand Tier AA** is the best seat on the level: open to the ceiling, 96 ft
  from a downstage singer, a partial view into the pit. It is priced the same
  as every other Grand Tier centre seat.
- **Grand Tier BB–EE** sit under the Dress Circle with 3.5–4 ft of soffit
  above eye level. By row EE the opening between the singer and the lip is
  down to 17° and the ceiling reflection is gone. Same price as AA.
- **Dress Circle A** is open to the ceiling, one floor up and 6 ft further
  back than Grand Tier EE. Its view score is higher than Grand Tier EE's, at
  a lower zone price.
- **Dress Circle B–D** are under the Balcony but close to its lip: the
  opening angle is still 50–100°, the top of the proscenium is intact.
- **Dress Circle E–G** lose most of the room above (opening 20–30°, no ceiling
  reflection). **J–L** are deep under the Balcony: opening 10–13°, depth to
  opening ratio over 2, and row L starts to lose the top of the proscenium.

Model output for the centre seats:

| Seat | Above you | Headroom over eyes | Opening angle | Depth ÷ opening | Score |
|---|---|---|---|---|---|
| Grand Tier AA | open | – | open | – | 73 |
| Grand Tier CC | Dress Circle | 3.5 ft | 42° | 0.5 | 58 |
| Grand Tier EE | Dress Circle | 4.1 ft | 17° | 1.3 | 46 |
| Dress Circle A | open | – | open | – | 72 |
| Dress Circle B | Balcony | 6.0 ft | 98° | 0.1 | 70 |
| Dress Circle C | Balcony | 6.3 ft | 68° | 0.4 | 68 |
| Dress Circle E | Balcony | 6.9 ft | 32° | 1.0 | 59 |
| Dress Circle G | Balcony | 7.5 ft | 19° | 1.5 | 49 |
| Dress Circle J | Balcony | 8.2 ft | 13° | 2.1 | 39 |
| Dress Circle L | Balcony | 8.7 ft | 10° | 2.7 | 25 |

Beranek's rule of thumb for opera houses is depth ÷ opening below about 2.

Conclusion for "one row back, half the price":

- Grand Tier EE at full price versus Dress Circle A or B at a lower zone
  price: take the Dress Circle. You gain the ceiling and lose nothing.
- Dress Circle B (Premium) versus C (standard): take C. Same conditions, one
  row further.
- Dress Circle D versus E, or anything from G back: the discount is paying
  for a real loss. Row G is where the room above disappears.
- If you want the sound the whole house is famous for, the Balcony Circle
  front rows are open to the dome, 117 ft from the singer, with the pit
  fully visible, at a third of the Grand Tier price.

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

Fitted to photographs (`sources/CALIBRATION.md`): the order and count of the
tiers, which rows each tier covers, and the tier heights, chosen so that the
seven SF Opera seat photos and the tour panoramas come out right (Dress
Circle J keeps the full proscenium arch; the rear boxes and the Grand Tier
rear rows keep about 8 ft floor-to-soffit; standing room fits under the box
ring). Row pitch and the plan offset between successive tier rails remain
estimates, each marked `confidence: low` in `data/house_geometry.json`.

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

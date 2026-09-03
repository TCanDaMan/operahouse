# War Memorial Opera House seat model

A seat-by-seat 3D model of the War Memorial Opera House (San Francisco) built
to answer one question: which seat is the best value for a given performance,
once you account for what is above you, how far off-axis you sit, whether the
tier in front clips the top of the stage picture, and whether you can see
into the pit. The reference staging is Wagner's *Die Walküre* (SF Opera,
fall 2027; full Ring cycles June 2028).

Open `web/index.html` in a browser. It is self-contained.

## What the model says about Grand Tier vs Dress Circle

The two are **one continuous balcony**, not two stacked levels. The Grand
Tier is rows AA–EE at the front, entered by walking down from the 2nd-floor
doors; the Dress Circle is rows A–L behind the cross-aisle, rising to the
3rd-floor doors at row L. SF Opera's own map labels them "2nd and 3rd Floor"
on one drawing, and its accessibility notes describe exactly that stair
pattern. The Balcony Circle (AA–EE) and Balcony (A–L) are the same
arrangement one level up.

So a price cliff at the Grand Tier / Dress Circle boundary, or at the Dress
Circle Premium / Dress Circle boundary a row or two later, is a demand
boundary on a continuous rake. The acoustic boundary is somewhere else: it is
the Balcony's front lip, which in this model sits above Grand Tier row CC.
Everything behind it is under the Balcony, and the question for each row is
how much open air is left between you and the stage.

Model output for the center of the lower tier (all geometry estimated, see
below):

| Seat | Opening angle to the lip | Depth ÷ opening | Proscenium visible |
|---|---|---|---|
| Grand Tier AA | open to ceiling | – | 31.5 ft |
| Grand Tier EE | 77° | 0.25 | 31.5 ft |
| Dress Circle A | 53° | 0.58 | 31.5 ft |
| Dress Circle C | 36° | 0.85 | 31.5 ft |
| Dress Circle G | 17° | 1.38 | 31.5 ft |
| Dress Circle L | 9° | 1.92 | 28.3 ft (top clipped) |

Beranek's rule of thumb for opera houses is depth ÷ opening below about 2
and a generous opening angle. Rows A–D of the Dress Circle are fine on both
counts; from about row G back the room above is gone and the ceiling
reflection is blocked; the last rows start to lose the top of the
proscenium. The top of the proscenium matters more for *Walküre* than for
most operas because of the Act III mountaintop and the projected fire.

Conclusion for "one row back, half the price": if the two rows are both in
the front half of the Dress Circle, take the cheaper one. If the cheaper row
is H or further back, you are paying less for a real loss.

The far side blocks are a separate story: Grand Tier 29–40 and Dress Circle
seats above about 20 lose part of the stage width behind the proscenium
edge, which the model reports as "stage width visible".

## What is published and what is guessed

Published (War Memorial technical specifications): auditorium 113 ft wide,
74 ft high, 116 ft deep at orchestra level and 161 ft deep at balcony level;
proscenium 52 ft wide, valence 31 ft 6 in; stage 3 ft 6 in above the house
floor; curtain line to pit apron 4 ft 4 in; pit 19 ft 10 in front to back at
the centerline with the floor 6 ft 8 in to 8 ft 2 in below the stage; pit
capacity 90.

Transcribed (seat charts): every row and seat number on every level,
including wheelchair platforms, companion and transfer seats, the sound
position in Dress Circle row K and the followspot gap in Balcony rows A–B.
Total 3,006 seats. The published orchestra count (1,174) is larger than the
current chart (1,078); the chart is what SF Opera sells today.

Estimated (marked `confidence: low` in `data/house_geometry.json`): row
pitch, floor rise on each level, the height of each tier, and where each
tier's front lip sits in plan. The overall stack is constrained by the
published height and depths and by the seat counts fitting the width, but
the lip positions could easily be off by a few rows. The War Memorial
virtual tour (blocked from the build environment) is the way to pin them
down: a photo from Dress Circle L toward the stage shows how much of the
proscenium the Balcony lip takes.

Price zones follow SF Opera's zone map. Zone prices in
`data/seating_spec.py` are placeholders inside the ranges SF Opera showed
for the Nov 27 2026 *Figaro*; replace them with the performance you are
pricing and rebuild.

## Metrics per seat

Computed by `scripts/build_seats.py` into `data/seats.json` and
`data/seats.csv`:

- distance to a downstage singer and to the pit; off-axis angle; elevation
- the lowest overhang above the seat, its lip distance, headroom, opening
  height at the lip, depth ÷ opening, and the opening angle between the
  singer and the lip
- whether the lip clips the top of the proscenium and how much remains
- stage width visible through the proscenium at 25 ft upstage
- fraction of the pit floor visible over the pit rail
- whether the first-order ceiling reflection from the singer and from the
  pit reaches the seat (image-source check against the overhang)
- direct-sound level relative to orchestra row A (inverse square)
- a 0–100 view score combining the above, and score per dollar

The score weights are opinions, written in `view_score()`.

## Layout of the repository

- `sources/` the two PDFs the model is built from
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
not modelled because the row-to-row rise is not published.

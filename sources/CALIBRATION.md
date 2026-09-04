# Calibration evidence

What the model's tier topology and heights rest on, beyond the seat charts.
Images in `calibration/` were captured by the owner on 2026-09-03/04 from the
War Memorial 360° virtual tour (sfwarmemorial.org/virtual-tour, one panorama
per level) and from SF Opera's "view from seat" photos for the Sep 19 2026
*Simon Boccanegra* listing.

## Published (wmoh-technical-specs.pdf, p.9)

- Proscenium 52 ft wide, valence 31 ft 6 in at centreline
- Stage 3 ft 6 in above house floor; curtain line to pit apron 4 ft 4 in
- Pit 19 ft 10 in front to back at centreline, playing floor 6 ft 8 in to
  8 ft 2 in below stage, capacity 90
- **Balcony rail to footlights: 80 ft.** The tour photos show the front-of-house
  lighting instruments on the Grand Tier rail (`06_house_from_orchestra_front`),
  so this is taken as the Grand Tier rail, 84.3 ft behind the curtain line.
- Auditorium 113 ft wide, 74 ft high, 116 ft deep at orchestra level and
  161 ft at balcony level (p.3 of the earlier brochure text)
- Capacity by level (p.5): Orchestra 1174 seated + 100 standing, Boxes 192,
  Grand Tier 274, Dress Circle 598, Balcony 610, Balcony Circle 278 + 100 standing

## Tier topology

`06_house_from_orchestra_front_all_tiers.jpg` and
`01_orchestra_front_looking_back_at_tiers.jpg` show four fronts stacked above
the rear orchestra: the paneled box ring with a lit soffit over the orchestra
standing room; the Grand Tier with the lighting rail; the Dress Circle; and
the Balcony Circle at the top with the dome beyond.

`02_grand_tier_looking_back_under_dress_circle.jpg`: from the front of the
Grand Tier looking back, about five rows rise to a rear wall with doors under
a low flat soffit with octagonal light panels. That soffit is the underside
of the Dress Circle. The Grand Tier is its own shallow slab, not the front of
the Dress Circle.

`03_grand_tier_front_to_stage.jpg`: from the Grand Tier rail, the orchestra
rows are visible directly beyond the rail with no box seats between, so the
rear-centre boxes sit under the Grand Tier front rather than in front of it.

`04_dress_circle_front_looking_up_to_stage.jpg`: from the Dress Circle
panorama, pitched up 12°, the full dome and chandelier are visible with no
soffit edge in frame. The Balcony lip is above or behind that position, so
the front row of the Dress Circle is open and the lip lands near row B.

`05_balcony_to_stage.jpg`: the Balcony panorama looks over the Balcony Circle
seats with only the dome above. Balcony Circle and Balcony are one open tier.

The War Memorial floor plans (spec p.5) draw the Grand Tier and Dress Circle
as crescents on separate floors (2nd and 3rd) and Balcony Circle + Balcony as
one crescent on the 4th, consistent with the above.

## Seat photos (`calibration/seat-views/`)

| Seat | What the photo shows | Model |
|---|---|---|
| Orchestra M-118 | Level view, stage lip at eye height, no pit visible | pit 0%, open |
| Orchestra Z-113 | Valence top at frame edge, dark soffit above | under box ring, proscenium not clipped |
| Grand Tier CC-106 | Full arch plus wall above it | under Dress Circle, lip 40° above the sightline |
| Dress Circle C-21 | Side view, stage partly behind the proscenium jamb | stage width 88% |
| Dress Circle J-116 | Full arch with margin above, steep view into the pit | Balcony lip 4° above the arch top, pit 42% |
| Balcony Circle CC-13 | Steep view, pit fully visible | open, pit 58% |
| Balcony F-113 | Steeper still, Balcony Circle rail in foreground | open, pit 58% |

The Balcony floor height was set so that Dress Circle J keeps the top of
the proscenium, as its photo shows. Row heights, row pitch and the plan
offset between tier rails are still estimates; each carries `confidence` in
`data/house_geometry.json`.

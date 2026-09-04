# Calibration evidence

What the model's tier topology and heights rest on, beyond the seat charts.
Images in `calibration/` were captured by the owner on 2026-09-03/04 from the
War Memorial 360° virtual tour (sfwarmemorial.org/virtual-tour) and from SF
Opera's "view from seat" photos for the Sep 19 2026 *Simon Boccanegra*
listing.

## Published (wmoh-technical-specs.pdf, p.9)

- Proscenium 52 ft wide, valence 31 ft 6 in at centreline
- Stage 3 ft 6 in above house floor; curtain line to pit apron 4 ft 4 in
- Pit 19 ft 10 in front to back at centreline, playing floor 6 ft 8 in to
  8 ft 2 in below stage, capacity 90
- **Balcony rail to footlights: 80 ft.** The tour frames show the front-of-house
  lighting instruments on the Grand Tier rail
  (`06_house_from_orchestra_front_all_tiers.jpg`), so this is the Grand Tier
  rail, 84.3 ft behind the curtain line.
- Auditorium 113 ft wide, 74 ft high, 116 ft deep at orchestra level and
  161 ft at balcony level
- Capacity by level (p.5): Orchestra 1174 seated + 100 standing, Boxes 192,
  Grand Tier 274, Dress Circle 598, Balcony 610, Balcony Circle 278 + 100 standing

## Tier topology

Three tiers stack above the rear orchestra: the box ring, one slab carrying
the Grand Tier and the Dress Circle, and one slab carrying the Balcony Circle
and the Balcony.

**Grand Tier and Dress Circle are one slab.** The decisive frame is a tour
capture from the Grand Tier cross-aisle looking along the rows toward the
stage (owner's capture, 2026-09-04, not in this folder): the Grand Tier
rows run along the front rail; the carpeted cross-aisle the camera stands
on; a skirted step up into the Dress Circle rows; and the Balcony's soffit
edge curving in above that first Dress Circle row. The SF Opera map draws
both on one page ("2nd and 3rd Floor") and its accessibility notes describe
walking down to the Grand Tier and up to Dress Circle L. The War Memorial
floor plans (spec p.5) show the Grand Tier crescent on the 2nd-floor plan
and the Dress Circle crescent, further back, on the 3rd-floor plan, which
is the same slab crossing two floor levels.

An earlier reading of `02_grand_tier_looking_back_under_dress_circle.jpg`
took its low soffit for a separate Dress Circle above the Grand Tier. That
camera stands on the cross-aisle, so the soffit it shows is the Balcony's
underside over the Dress Circle rows. The file keeps its old name.

**Balcony Circle and Balcony are one open tier.** `05_balcony_to_stage.jpg`
looks over the Balcony Circle seats with only the dome above.

**Box ring.** `03_grand_tier_front_to_stage.jpg` shows orchestra rows
directly beyond the Grand Tier rail with no box seats between, so the
rear-centre boxes sit under the Grand Tier front. The owner's recollection
is that the ring covers about the last ten orchestra rows; the SF Opera map's
side blocks narrow to two seats at rows R–T, where the ring's structure
lands, so the rear rail is placed between rows R and S.

## Seat photos (`calibration/seat-views/`)

| Seat | What the photo shows | Model |
|---|---|---|
| Orchestra M-118 | Level view, stage lip at eye height, no pit visible | open, pit 0% |
| Orchestra Z-113 | Valence bottom at the frame top, dark band above | under box ring; model predicts the arch top is hidden. Unverified: the photo may simply be framed tight |
| Grand Tier CC-106 | Full arch plus wall above it | open to the ceiling |
| Dress Circle C-21 | Side view, stage partly behind the proscenium jamb | stage width 88% |
| Dress Circle J-116 | Full arch with margin above, steep view into the pit | Balcony lip 4° above the arch top, pit 25% |
| Balcony Circle CC-13 | Steep view, pit fully visible | open, pit 58% |
| Balcony F-113 | Steeper still, Balcony Circle rail in foreground | open, pit 50% |

The Balcony floor height was set so that Dress Circle J keeps the top of
the proscenium, as its photo shows. Row pitch, the plan offset between the
two slab rails, and the box-ring position at centre are estimates; each
carries `confidence` in `data/house_geometry.json`.

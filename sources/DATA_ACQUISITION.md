# Data acquisition log, 2026-09-03

What was pulled, what it showed, and what it is worth for calibration.

## 1. SF Opera ticketing seat map (Adage SmartSeat) — `smartseat/`, `data/seats_smartseat.csv`
- `POST https://www.sfopera.com/api/seating/GetSeatmap` with `venueLevels:[n]` (0 orchestra,
  1 boxes, 2 grand tier + dress circle, 3 balcony circle + balcony) returns every seat with
  section, row, seat number, price zone, live price, SVG glyph path and a seat-view image id.
  No session needed. `scripts/import_smartseat.py` regenerates the CSV; `--fetch <itemNumber>`
  pulls fresh prices for another performance.
- 3,006 seats; row-by-row counts match `data/seats.csv` exactly (82 rows, zero differences).
- The plan drawing is schematic per level (row spacing not to scale between levels): use it for
  row shape, aisles and seat order, not metric pitch.
- 47 seat-view photos (`smartseat/seat-views/`, `smartseat/views.txt` maps each to its seat
  block). Rear-orchestra side blocks (V–ZZ) show the box-ring soffit clipping the top of the
  proscenium; the centre rear block (U–ZZ) keeps the valance. Partial answer to open question 1.

## 2. War Memorial virtual tour panoramas — `panoramas/`
- TourBuilder/Panoskin. Full equirectangulars on S3:
  `https://panoskin.s3.us-east-2.amazonaws.com/SVE/644ad1977efdb6532e6775d8/tours/644ad1bf7efdb6532e6775dc/<island>/<pano>/full.jpg`
  Scene index with ids, names and GPS poses: `panoramas/other/tourbuilder_scene_index.tsv`.
- Five 13,060 x 6,530 auditorium panoramas (2023 reshoot) + six 6,000 x 3,000 older ones.
  Tour menu labels are unreliable: "OH Balcony" is at the Grand Tier rail, "OH Dress Circle"
  is on the upper slab cross-aisle.
- `scripts/solve_pano_poses.py`: joint least-squares of camera position, height, heading and
  pitch from hand-picked feature angles (valance bottom = 35 ft above house floor at the
  proscenium, pilaster inner edges 52 ft apart, stage lip 3.5 ft, plus chandelier tip and
  supertitle screen as free 3D points). Fit residuals under 1 degree. With a 1-degree pitch prior:

  | Camera | height above orchestra-front floor | distance from curtain line | 1-sigma |
  |---|---|---|---|
  | orchestra row A (P1) | 7.5 ft | 30 ft | 0.5 |
  | box level (P2, Q4) | 23–24 ft | 76–81 ft | 1.5 |
  | grand tier, ~2 rows behind rail (P3, Q2) | 36–38 ft | 85 ft | 1.5 |
  | upper cross-aisle (P4, Q1) | 56–57 ft | 97–100 ft | 1.5 |
  | balcony row L (P5) | 86 ft | 149 ft | 3.3 |

  Derived: proscenium arch apex 53 ft above the house floor (49.5 ft above stage, matching the
  1932 "approximately fifty feet"); chandelier tip about 60 ft up, 39 ft from the curtain line.
  Subtract the tripod height (P1 says 6–7.5 ft above the row-A floor) for floor heights. This
  says the Grand Tier floor near the rail is about 30 ft, not the 22 ft in `house_geometry.json`,
  and the upper-slab cross-aisle about 50 ft. The balcony row L height (79 ft floor) exceeds the
  73 ft dome height and needs checking against the section (pitch or valance-datum error).
- Reads were taken from degree-gridded crops by eye (±0.3–0.5°). A proper pass should pick
  features at full resolution and add more shared points (box rails, tier rails, ceiling oval).

## 3. Archival drawings — `research/`
- `ae1932/AE_Nov1932_p16_LONGITUDINAL_SECTION_auditorium.png`: Brown/Lansburgh longitudinal
  section, The Architect and Engineer, Nov 1932, p. 16 (archive.org usmodernist-AECA-1932-10-1933-03).
  Halftone ~9 px/ft, dimension strings illegible; scale it from 52 ft proscenium / 74 ft dome /
  116 ft orchestra depth. Orchestra rake, box ring, both tier slabs, soffits and ceiling are all there.
- `ae1932/` also: foyer section (sheet 22 of the 1931 set), structural plan of boxes/balconies
  (sheet S-14 referenced), first-floor plan. Text: proscenium ~50 ft high x 52 ft; pit 15 ft below
  stage; fly galleries 39 ft, grid 116 ft.
- `hsr1993/`: Carey & Co. Historic Structure Report (1993) floor plans for every level at one
  scale — box ring plan position, tier rail setbacks, row counts. No section.
- Beranek 2004 (Hall 22, pp. 141–144): V 738,600 ft3; N 3,252; H 73 ft, W 104 ft, L 120 ft,
  D 122 ft; ITDG 51 ms; RT occupied (2001) 1.59/1.58/1.53/1.46/1.39/1.26 s at 125–4k Hz;
  stage 40 in above the floor at row A. Beranek 1962 p. 561: row-to-row 31 in main floor /
  36 in balcony, seat-to-seat 21 in (the 1965 city report says orchestra spacing was 36 in, so the
  columns may be transposed). Section drawing on p. 143 needs a borrowed copy (archive.org CDL).
- Originals: Bancroft Library, Arthur Brown Jr. papers BANC MSS 81/142 c, rolls 42/43 (sheets
  1–49, 1931) and 67 (structural S1–30). Request scans via bancref-library@berkeley.edu.
  A 1997 Sound and Vibration article reproduces a Bureau of Architecture longitudinal section.

## Next
1. Digitize the 1932 section: pick the orchestra floor, each slab's front rail, soffit and
   rear, and the ceiling; scale; write to `house_geometry.json` with source "AE 1932 section".
2. Reconcile with the panorama solve; resolve the balcony-row-L discrepancy.
3. Rebuild and re-run the Dress Circle vs Grand Tier comparison in the README.

## 4. Beranek 1996, Hall 19, p. 159 section — `research/beranek1996/`
Clean line-drawing section with a feet scale bar (screenshot at ~4.4 px/ft, so ±0.5 ft).
Datums: house floor at the front row, proscenium wall. First reading:

| feature | height ft | from proscenium ft |
|---|---|---|
| dome apex | 74.3 | 46 |
| box floor, front lip | 16.4 | 77.5 |
| Grand Tier rail floor | 26.6 | 74.5 |
| Grand Tier rear / cross-aisle landing | 32.3 | 95 |
| Dress Circle rear row | 45.0 | 131 |
| Balcony rail floor | 53.9 | 86 |
| Balcony Circle cross-aisle landing | 61.4 | 104 |
| Balcony rear row | 76.4 | 138 |
| rear wall at balcony level | 76.4 | 157 (published 161) |
| orchestra floor at the rear under the boxes | 1.6 | 77.5 |

Agreement with the panorama solve (tripod ~7 ft): box 16.4 vs 23.5-7; Grand Tier 27-28 vs 36-38-8;
rear balcony 76 vs 86-8. Outlier: the upper cross-aisle panoramas (P4, Q1) solve to a 49-50 ft
floor where the section shows 61 ft; unresolved.
Implied corrections to `house_geometry.json`: lower_tier.floor_y 22 -> 26.6; upper_tier.floor_y
46 -> 54; boxes.floor_y 13 -> 16.4; Balcony Circle rise ~1.3 ft/row confirmed; Dress Circle rise
~1.0-1.1 ft/row (was 1.3); Grand Tier ~0.85 ft/row.

### Second pass, zoomed screenshots (`p159_section_zoom.png` at 7.98 px/ft, `p159_plan_zoom.png`)
Datums: stage floor line (3.5 ft) and proscenium wall. Distances are from the proscenium wall
(add ~4 ft for the curtain-line frame used in `house_geometry.json`).

| feature | height ft | from proscenium ft | notes |
|---|---|---|---|
| orchestra floor, row A | 0 | 5 | |
| orchestra floor at 50 ft | ~2 | 50 | |
| orchestra floor under box soffit | 4.6 | 80 | rake ~4.6 ft total (model had 2.5) |
| rear orchestra promenade floor | 4.5 | 80–115 | flat under the boxes |
| box-ring soffit over rear orchestra | 16.3 | 80 back to the rear wall | last ~10 rows + standing room |
| box floor | 17–18.5 | 75 (front) | |
| Grand Tier rail floor | 27.6 | 70–75 | published rail-to-footlights 80 |
| Grand Tier / Dress Circle landing | 29–33 | 85–90 | ambiguous in the redrawn section |
| Dress Circle rear row | 46 | 124 | DC rise ≈1.1–1.5 ft/row |
| Balcony rail floor | 50 | 78 | 8 ft behind the GT rail in section (model had 16) |
| Balcony Circle / Balcony cross-aisle | 62 | 109 | |
| Balcony rear row (L) | 80 | 141 | balcony rise ≈1.5 ft/row |
| dome apex | 74–76 | 46 | published 74 |

Plan (scaled by the 52 ft proscenium, 8.65 px/ft): box-ring rail 66 ft from the proscenium at
14 ft off-centre, i.e. rear rail ~70 ft (model rear rail z=71 from the curtain line, consistent);
Grand Tier front rows ~71 ft; Balcony front ~83 ft.

Caveat: this is Beranek's redrawn schematic of the 1931 section; row counts and pitches are not
exact (Balcony draws ~12 steps, GT+DC draws ~16). Heights at rails and rear rows are the reliable
part (±1 ft). The upper cross-aisle panoramas (P4, Q1) still solve ~9 ft below the drawing's
Balcony Circle cross-aisle and ~8 ft above the Dress Circle one; unresolved.

## 5. Wikimedia Commons photo — `calibration/commons/`
"War Memorial Opera House Director's Circle & balcony levels", BrokenSphere, 2009-01-11,
CC BY-SA 4.0, 2448x3264. Shot from the side of the Grand Tier near the stage-left wall,
looking along the tier toward the grille arch. Shows, qualitatively:
- The tiers are horseshoes, not just rear arcs: the Grand Tier and the Balcony both run
  forward along the side walls and step down toward the proscenium; the Balcony's side arm
  ends at the wall just above the grille arch, well below its rear-rail height.
- So the Balcony soffit is lower over the side blocks of the Dress Circle and the Grand
  Tier than at centre, and the Grand Tier soffit is lower over the side boxes. This is the
  side-block counterpart of the box-ring clipping seen in the rear-orchestra side seat photos.
- The Dress Circle side blocks rise steeply behind the Grand Tier's side sweep.
No scale; use for topology, not dimensions. The model currently draws each tier as a single
arc about `curve_center_z`; a side-arm descent per tier is not modelled.

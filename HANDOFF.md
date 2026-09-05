# Checkpoint, 2026-09-04

Working name for the product: **Sound Purchase**. See the seat, hear the
seat, price the seat; one venue package per house.

## Where things stand

- Branch `claude/opera-house-seat-model-94ksm4`, all work pushed.
- `python3 scripts/build_seats.py` regenerates `data/seats.json`,
  `data/seats.csv` and `web/index.html` from the geometry and seat spec.
  No dependencies beyond the standard library.
- `web/index.html` is self-contained; open it in a browser. Deep link:
  `?seat=dress_circle:A:105&view=sit`.
- Published viewer: https://claude.ai/code/artifact/5c086e14-1b66-4836-8184-695d51e9c50e
- The 3D pane loads three.js r128 from cdnjs. It was never rendered in the
  build sandbox (host blocked), so the first thing to do on the Mac is open
  `web/index.html` and look at it. The seat panel, lookup, compare and value
  list are verified; the scene is not.

## House model as of this checkpoint

Three tiers above the rear orchestra: box ring; one slab carrying Grand Tier
AA–EE, a cross-aisle, and Dress Circle A–L; one open slab carrying Balcony
Circle AA–EE and Balcony A–L. Balcony lip over Dress Circle A. Box ring over
about the last ten orchestra rows. Grand Tier rail 80 ft from the footlights
(published). Full reasoning and the photo evidence: `sources/CALIBRATION.md`.
Every dimension with its source and confidence: `data/house_geometry.json`.

## Open questions on the geometry (updated 2026-09-03 late)

Answered: the box ring does not hide the proscenium top at centre (its rear
rail is at z≈97, behind the Grand Tier rail; only the outer seats of rows
S–ZZ are under it, and the side seat photo shows the clip). Box ring plan and
the Balcony rail (8 ft behind the Grand Tier rail) come from the 1993 plans
and the 1931 section. Orchestra pitch 2.55 ft from the plan and Beranek.

Tier fronts, the box ring and the Balcony side sweeps are now traced
polylines from the 1993 plans (`plan_curves` in `house_geometry.json`; see
`sources/DATA_ACQUISITION.md` §7 for the frame correction that made them right).

Still open:
1. Grand Tier far blocks (seats 29–40) sit on the side slips and curve forward
   along the walls; the model still puts them on the crescent.
2. Tier row pitch (2.85 ft) and the per-row rises on the upper tier are not
   measured; the Beranek section is a redrawn schematic.
3. Balcony sweep heights (33–57 ft) rest on one panorama's lighting-rail reads.
4. Orchestra pitch 3.0 ft is bracketed (31 in Beranek, 36 in 1965 report).

## Next build: Sound Purchase

1. **Venue package format.** One folder per house: `venue.json` (dimensions
   with provenance), `seats.csv` (id, level, row, seat, x, y, z, zone),
   `zones.json` (prices), `media/` (panoramas, seat photos, splat). The
   current `data/` is the first package in all but layout.
2. **Importer.** SF Opera's seat map is a vector drawing with one element per
   seat. A paste-the-page importer reads seat ids and plan positions, which
   replaces hand transcription for any Tessitura or AudienceView venue.
3. **See layer.** Level 1: project the tour's five 360° panoramas onto the
   geometry. Level 2: Gaussian splat of the auditorium rendered in three.js,
   with the seat overlay, the overhang lip drawn on the real ceiling, and the
   Walküre set as meshes placed on the real stage.
4. **Hear layer.** Per-seat impulse response from geometric acoustics on the
   same geometry (direct, early reflections, shared late tail), convolved
   with a dry excerpt in the browser with Web Audio.
5. **Value layer.** Live prices pasted from a listing, opera-specific weights,
   "best seat under $X".

## Getting the assets

**Tour panoramas.** Open sfwarmemorial.org/virtual-tour in Chrome, open
DevTools, Network tab, filter by image, and click into each auditorium
position (Orchestra, Grand Tier, Dress Circle, Balcony, side box). The tour
loads either one equirectangular JPEG per position or a set of cube-face
tiles; save whichever appears, one folder per position, into
`sources/panoramas/<position>/`. Note the position on the minimap for each.

**Capture recipe for a splat.** Next time in the house with the house lights
up, before the performance or at intermission:

- Phone in landscape, video at 4K if available, exposure locked, no HDR, no
  zoom. Walk slowly, half normal pace, and keep the phone moving in smooth
  arcs rather than pans from one spot; the training needs parallax.
- Cover each level as a loop: along the front rail, then along a cross-aisle
  or the rear, with the camera pointed across the house, then at the ceiling,
  then at the stage. Ten to fifteen minutes total is enough. Overlap matters
  more than resolution.
- Include the proscenium and pit from at least three levels, and the
  underside of each overhang from the rows beneath it.
- Feed the video to the Luma or Polycam app (both produce a splat file from
  video) or to nerfstudio on a machine with a GPU. Export as `.ply` or
  `.splat` and drop it into the venue package under `media/`.

**Seat photos.** SF Opera's seat map shows a view photo for sample seats on
each level. Save each with its seat id; they are the ground truth the tier
heights are fitted to. Seven are already in `sources/calibration/seat-views/`.

## Running on the Mac

```
git clone <repo> && cd operahouse
git checkout claude/opera-house-seat-model-94ksm4
python3 scripts/build_seats.py
open web/index.html
```

Prices: edit `ZONE_PRICES` in `data/seating_spec.py` to the listing you are
pricing, rebuild, and the value list updates.

## Update, 2026-09-03 late: calibration from the 1931 section and the tour panoramas

`sources/DATA_ACQUISITION.md` has the full log. Short version: the SmartSeat API gave all
3,006 seats with live prices and 47 seat-view photos; the virtual tour gave eleven full
equirectangular panoramas (five at 13k px); a research pass found the Brown/Lansburgh
longitudinal section (Architect and Engineer, Nov 1932) and Beranek's redrawn version with a
scale bar (1996, p. 159). Tier heights in `data/house_geometry.json` are now from that section
(box floor 17.5, Grand Tier rail 27.6, Balcony rail 50 at z=92, rear balcony ~80, orchestra rake
4.6) and agree with a pose solve of the panoramas (`scripts/solve_pano_poses.py`) to within a
tripod height. Rebuilt; README table and conclusions updated. Open items: the upper cross-aisle
panoramas solve ~9 ft below the drawing; the box ring is lower toward the sides than the model
draws (side rear-orchestra seat photos show the arch clipped); per-row rises on the upper tier
are averages, not measured.

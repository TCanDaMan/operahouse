# Sound Purchase — current handoff, 2026-09-05

## Start here

User wants a realistic, dimensionally credible War Memorial Opera House model
for choosing opera seats, and a repeatable reconstruction workflow for other
halls. Keep working autonomously; do not make the user repeatedly say continue.
Explain results in plain language. They supplied plans, sections, and tour views.

Repository: TCanDaMan/operahouse. Local checkout:
`/Users/tyler/Developer/personal/soundpurchase` (an older copy may exist under ~/Documents/ChatGPT).
Checkpoint branch: `codex/hall-calibration-checkpoint`.
Base before this work: `75e4048` on `claude/opera-house-seat-model-94ksm4`.
Do not mistake old README conclusions or historical calibration logs for verified
current facts. The prior handoff is archived in sources/history/.

## Run

```sh
python3 scripts/build_seats.py
python3 scripts/check_surface_consistency.py
python3 -m http.server 8765 --bind 127.0.0.1
```

Open `/web/index.html` for the model and `/web/calibration.html` for Geometry Lab.
The model builds with the Python standard library. Audit additionally needs NumPy
and SciPy: `python3 scripts/calibrate_hall.py`. Section digitization:
`python3 scripts/register_section.py`. These audit scripts do not update hall geometry.
Three.js r128 is bundled in web/vendor with its license. Keep that folder beside
index.html; the viewer is no longer a standalone single HTML file.

## Implemented and checked

- Instanced chair components, material/analysis modes, stepped upper decks,
  soffits, brass trim, box dividers and padded caps; illustrative detail.
- Full-width upper decks use the same clamped row curve as seat placement.
  Risers offset forward of chair centers. Structural clipping works.
- Stagefront camera fixed. Browser-checked multiple views and selected seats.
- Removed unsupported giant side-sweep solids AND their phantom occlusion.
  Upper-deck containment now has matching width, front, rear and soffit slope.
  462 overhang classifications changed in that correction, all seat IDs/positions
  preserved. Regression checks cover 81 upper-deck sections.
- Main-ceiling plane is below 224 rear-balcony listeners. Their headroom and
  ceiling-reflection results are now null / "Not modeled", not negative headroom
  or a spurious yes/no. Unknown reflection does not incur a blocked-reflection penalty.
- All 3,006 seats remain. Scores/prices are not validated purchase advice.

## Provisional changes — do not promote to measured facts

- Rear-center box rail was shifted 17 ft forward, tapered to zero at |x|=40.
  Old trace retained in house_geometry.json. This was a visual/section-based
  hypothesis, NOT a completed plan registration. Its placement changes metrics.
  Owner reviewed tour screenshots on 2026-09-05 and chose to KEEP the shift:
  the box parapet visibly sits close under the Grand Tier front. Do not revert
  without new plan evidence. Still needs plan registration for a measured depth.
- Box parapet 2.2 ft, dividers, molding and chairs are illustrative.
- Tier depths remain unresolved. Do NOT move Balcony forward 26 ft just because
  the lab reports that discrepancy. The picked schematic section feature and
  floor-plan void boundary have not been shown to be equivalent. Floor plans
  are horizontal cuts at different elevations, not necessarily front-rail plans.
- The flat ceiling, side-slip seating and box depth/floors still need reconstruction.
- Only upper-deck surface consistency is regression-checked. Do not claim all
  rendered architecture matches the ray model. Dividers are not ray obstacles.

## Calibration work

scripts/calibrate_hall.py wraps legacy hand-read angular observations, uses a
robust fit, varies pitch priors, tests both stage-lip z signs, and excludes lip
observations for a feature holdout. JSON: data/calibration_audit.json.
Baseline RMS .383 degrees, opposite sign .409; both fit well while some camera
depths differ 4–5 ft. Held-out lip RMS ~1.26 degrees. Not independent validation.
Old solver uses lip z=-4.33 whereas viewer apron is +4.33: feature/datum identity
must be checked, not "resolved" by choosing lower fit error.

Geometry Lab displays fits, adjustable section overlay and original panoramas.
Manual pixel recorder saves browser-local observations and exports JSON.
Two seed picks copied to data/panorama_landmarks.json; ~35 px estimated uncertainty,
not refined full-resolution points. Legacy P/Q camera IDs are not reliably mapped
back to file/pixel longitude origin; lab deliberately avoids false photo overlays.

Section source-pixel picks, scale anchors and alternate datum retained in
scripts/register_section.py and data/section_registration.json. Approximate
8.044 px/ft; picks +/-8 px, additional schematic/datum uncertainty. Profiles are
candidate interpretations. More detail: sources/CALIBRATION_NEXT.md.

## Next substantive work

1. Register source plans separately from shared stable architecture, preserving
   pixel anchors, scale and origin for each sheet. Identify actual tier fronts
   rather than arbitrary floor-cut boundaries.
2. Match exact panorama filenames to known camera positions; refine landmark
   picks at full resolution across multiple images, including architectural rails.
3. Fit cameras and surface geometry jointly; keep unfit observations for checks.
4. Replace provisional box shift only with evidence. Rebuild seats AND shell from
   common geometry. Add a rear ceiling/cove profile before restoring rear-ceiling
   acoustic claims. Validate with photo overlays from identified cameras.
5. Continue improving shape; do not stop at building another diagnostic tool.

## References

Twelve user tour screenshots saved as sources/calibration/user-tour-2026-09-05/
01–12.png, with an index README. Original panoramas, 1932 sections, 1993 plans,
Beranek section, and SmartSeat seat photos already live under sources/.
No external messages sent. No merge or deployment performed in this checkpoint.

## Follow-up: box-floor consistency

Box decks now have three horizontal elevations matching the existing chair
floor heights, replacing the former continuous ramp. No seat positions changed.
The source exports deck_rows so rendering consumes the same floor elevations.
14 box seat centers lie beyond the rectangular hall half-width of 56.5 ft;
data/geometry_conflicts.json records their IDs. Do not squeeze them inward:
register the actual wall outline and box layout first. The rectangular enclosure
is a visualization approximation, not a confirmed interior wall footprint.

Viewer copy no longer claims that ceiling reflections are "mostly gone" based
only on the opening angle. That was an unsupported acoustic conclusion from a
geometric measurement. It now describes the opening without claiming sound quality.

## Follow-up: section envelope

Replaced the constant-height rectangular wire enclosure with a switchable
section-derived wire envelope (Section envelope button). Its candidate outer
profile rises from ~71–76 ft over the main room to ~89 ft at the rear. Source
pixels and uncertainties are preserved in section_registration.json; copied
profile is in house_geometry.json > ceiling_profile. It is NOT an interior
ceiling, transverse dome, wall footprint or acoustic reflection surface.
The 224 unknown rear-ceiling results remain unknown. Browser checked overview;
upper-surface regressions passed. Controls wrap to avoid covering the cutaway.

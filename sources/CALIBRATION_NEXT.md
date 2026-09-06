# Geometry audit — 2026-09-05

Run `python3 scripts/calibrate_hall.py` with NumPy and SciPy installed.
Open `web/calibration.html` through the local HTTP server. This is a diagnostic
workbench, not a completed reconstruction. It does not modify production geometry.

## Findings

The legacy camera fit and viewer disagree on stage-lip z sign: -4.33 versus
+4.33 feet. A robust fit has 0.383 degree RMS using the old sign and 0.409 using
the opposite sign. Both fit well; the residual cannot determine the correct
physical convention. Grand Tier camera depths change by about 4–5 feet between
these alternatives. Small residuals must not be presented as accuracy proof.

Changing the pitch prior from 0.5 to 5 degrees yields approximately 29.8–30.7 ft
for P1, 85.3–85.4 for P3, and 148.8–149.0 for P5. These are sensitivity ranges
conditional on the original feature identifications and 52 ft stage-width
anchor, not confidence intervals. P5 camera height remains about 86 ft: the
ceiling over the rear balcony cannot be represented by the main dome's 74 ft
height as a flat room-wide plane.

The script also excludes all lip observations and reports their prediction
errors separately. This is a feature holdout, not validation on an independently
measured photograph. The pilaster observations supply azimuth only and assume
features in the stage plane; that approximation still needs verification.

## Evidence alignment still required

- Verify P/Q camera IDs against exact panorama filenames, not tour labels.
- Preserve original full-resolution pixel picks and longitude origin; the legacy
  hand-read angle list does not record enough information for a trustworthy
  photographic overlay.
- Register every plan independently using shared architectural landmarks. A
  copied pixel scale and origin across differently cropped sheets is unsafe.
- Align the section with its scale bar and explicitly distinguish the
  proscenium wall, curtain line, stage apron, and audience-side pit rail.
- Replace provisional box shift only after this registration. Current section
  controls provide visual alignment and export, not automatic calibration.

## Reusable interface

A venue needs source assets, landmark observations (source, feature ID, pixel,
uncertainty), per-image projection/registration, physical anchors, surface
parameters, and validation observations. The current audit JSON exports fitted
camera poses, individual residuals, sensitivity variants, and held-out errors.
The workbench shows these alongside an adjustable section overlay and raw
panoramas. Next implementation: persisted pixel landmark capture and a joint
surface/camera fit with both image and drawing residuals.

## Registered section candidate

`scripts/register_section.py` preserves manual source-pixel picks and writes
`data/section_registration.json`. Scale: 724 px across 90 ft = 8.044 px/ft.
The two candidate vertical datums are 50 px apart (6.22 ft); datum identity is
not yet independently verified. These are approximate visual picks, not exact
survey observations. Model-minus-section front depths are box +4.0 ft, Grand
Tier +4.2 ft, Balcony +26.0 ft. The unequal offsets cannot be fixed by translating
all three tiers together. The upper front could be a side profile in this
schematic section; validate its identity against a registered plan before moving it.
The lab now displays the actual picked features and profiles over the drawing.

Two source-linked panorama seed observations were recorded through the lab and
preserved in `data/panorama_landmarks.json`. They demonstrate the capture path;
they are not enough for a new camera fit. The curtain-bottom feature is named
literally rather than incorrectly equated with the stage apron. Full-resolution
refinement, cross-view correspondences and plan registration remain outstanding.


## Cross-check and production correction

The HSR second- and fourth-floor drawings are horizontal floor-level plans.
Their visible void boundaries have not been established as the same front-rail
landmarks picked from the schematic section. Consequently the 26 ft number is
a discrepancy between interpretations, not a verified error to apply to the
Balcony. No tier was translated on that basis.

A definite inconsistency was corrected: the unsupported side-gallery trace was
still active in upper-tier occlusion. Upper-tier containment now follows the
same clamped front, full deck width and finite rear boundary as the displayed
mesh. Its soffit uses the same slope. The trace remains archived in source data
but is disabled in the shell and in sightline calculations. This changes 462
seat overhang classifications while preserving all 3,006 seat IDs and positions.
Run scripts/check_surface_consistency.py to check 81 deck cross-sections and
regress the former phantom obstruction above front orchestra seats.

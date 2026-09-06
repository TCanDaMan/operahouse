# Seat audio checkpoint — 2026-09-06

This improves Fable's `cd83c9e` acoustic engine. It is a predictive reconstruction,
not a measured binaural reproduction of War Memorial Opera House.

## What changed

- All 3,006 seat records now export four-band direct and reflected pressure,
  all valid first/second-order paths (no 14/8 tap cap), and source-specific late
  energy/onset. Legacy fields remain for the path display. Schema version is 2.
- `web/room-audio.js` is a reusable, browser-independent DSP module. It uses
  complementary 129-tap FIR bands for early arrivals, approximate head-shadow
  and spherical-head ear delays, and fractional sample placement. Fixed seeds
  keep the diffuse noise field repeatable across auditions and neighboring seats.
- Corrected the reversed listener-right vector. Removed the old extreme
  equal-power panning that silenced the far ear at 90 degrees. These are generic
  ear cues, not individualized HRTFs; elevation mainly reduces lateral cues.
- Late energy is shared across the two ears, not independently duplicated in
  each. The pit tail no longer derives from the singer's direct amplitude.
  There is no per-seat loudness normalization. Model units use a common gain of 22.
- Tail onset and its 25 ms smooth rise are exported. C80 integrates that same
  envelope per band. Onset cannot precede the first computed non-floor return
  (minimum 20 ms; fallback 80 ms when there is none). This is still an assumed
  transition to the diffuse field, not a measurement of mixing time.
- Source directivity is frequency-dependent: provisional multipliers
  [0.15, 0.5, 1, 1.2] on the existing rear-attenuation pattern. Do not interpret
  this as a measured singer radiation pattern.
- The displayed main ceiling and the acoustic ceiling now share
  `interior_ceiling` parameters. The dome has 36 bounded acoustic facets for
  first-order returns only; the rear starts at the same main-ceiling junction.
  Both still use unverified interior dimensions. The old outer section trace
  remains labeled low confidence. Headroom outside overhangs uses the flat/rear
  profile conservatively and does not add the dome rise.
- Added “Without room echoes” using the same source and distance/head cues.
  Uploads are explicitly downmixed to one stage source; they now also work in
  voice-plus-orchestra mode. “Use test voice” resets the upload. Stop now stops
  the synth oscillators; finished playback disconnects its graph.

## Run / validation

```sh
python3 scripts/build_seats.py
python3 scripts/check_surface_consistency.py
python3 -m unittest discover -s tests -p 'test_*.py'
node tests/room-audio.test.cjs
python3 -m http.server 8877 --bind 127.0.0.1
```

Open `web/index.html`. Keep `web/room-audio.js` and `web/vendor/` beside it.
The generated HTML is not standalone.

Checked: every seat's metadata; 24 rendered singer/pit responses across all six
levels; two sample rates; repeatability; mirrored ear responses; an analytical
image-source reflection; summed stereo tail energy; rendered energy-decay RT
(1.392 s for a 1.4 s input); 81 structural sections. Seat IDs, coordinates, floors,
and prices are identical to Fable's checkpoint. Browser voice/both/direct/stop
controls were exercised. No subjective listening validation or uploaded-file
browser test was performed.

## What is still needed for convincing opera reproduction

1. **Dry source recordings.** The built-in sawtooth/formant voice and chord are
   test signals. A hall recording already contains its own reverberation and
   cannot serve as a clean source. Use licensed dry vocal and instrument stems.
2. **Measured calibration.** Acquire octave-band impulse-response data at several
   known seats with a known source position, or at least measured occupied RTs.
   Fit decay, early arrival timing, and direct/reverberant balance against held-out
   seats. The single published 51 ms reference does not validate the hall.
3. **Better boundary geometry.** Validate interior ceiling/soffits, box walls and
   curved side walls. Current slab occlusion samples a 2 ft grid; it can miss or
   overblock thin edges. Diffraction still uses fixed attenuation. Seat-dip is
   flagged but not synthesized; dome focusing and detailed scattering are absent.
4. **Distributed orchestra and real binaural filters.** The pit remains one
   source, with equal-power assumptions for the displayed voice/pit metric.
   A full orchestra needs separately positioned, independently recorded stems.
   Add licensed measured HRTFs/SOFA data and head orientation before claiming
   convincing front/back/elevation externalization.
5. **Diffuse-field calibration.** Room constant uses an assumed 8,000 m² surface
   area and RT, overhang coupling is heuristic, and the statistical field is added
   to explicit early paths. Its power allocation and transition need measured
   calibration; it is not a full wave solver. Broad audition bands and generic
   ear cues mean broadband rendered metrics need not exactly equal octave-band
   pressure metrics. Do not rank purchases based on unvalidated sound scores.

Reference methods: [Web Audio convolution and normalization](https://www.w3.org/TR/webaudio-1.0/)
(normalization stays disabled); [DAFx BinRIR](https://dafx.de/paper-archive/details/lUF_cLvEDGdaZjWoH1jBrQ)
illustrates adapting binaural late noise to a **measured** decay curve. This
implementation does not implement that paper's full method or have its measurement inputs.

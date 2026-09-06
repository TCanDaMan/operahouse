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

## Follow-up 2026-09-06 (Fable): tail onset ramp shortened to 5 ms

Merged this branch into `claude/opera-house-seat-model-94ksm4` (fast-forward) and
compared the regenerated metrics with checkpoint `cd83c9e`. House-median C80 had
fallen about 3 dB in every level (Grand Tier -1.9 to -5.9 dB) and sound scores
moved by up to 75 points. Decomposition over all 3,006 seats: the new mixing-time
rule and the explicit-path/tail double count each change C80 by under 0.3 dB;
the entire drop came from the 25 ms onset ramp with the tail energy renormalised
after ramping, which pushes fixed diffuse energy past 80 ms. Since the coarse
image-source set carries only 4-17% of the reflected energy, the tail has to stand
in for early reflected energy the model does not resolve, and a long ramp removes
exactly that. `TAIL_RISE_S` in scripts/acoustics.py is now 0.005 s, still shared
by the metric and the renderer through `tail_rise_s`. Result: house C80 median
-0.9 dB (range -7.9 to +1.8), within the -4 to +4 dB range reported for opera
houses; level medians are within 0.4 dB of the checkpoint except Grand Tier.

Still open from this comparison:

- Grand Tier C80 is 1 dB below the checkpoint because the dome hole removes the
  flat-ceiling reflection for 144 of 264 Grand Tier seats and the 36 facets return
  it to only some. Dome size/position are illustrative; a real concave dome of this
  curvature would focus and then spread the reflection, not drop it. Either
  refine the facet mesh or treat the dome as a diffusing flat patch until the
  ceiling is measured.
- boxes A:4/5 and Z:5/6 (among the 14 seats outside the rectangular half-width)
  get no significant early reflection and C80 -7.9 dB. That is the wall-footprint
  conflict in data/geometry_conflicts.json, not a listening result.

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

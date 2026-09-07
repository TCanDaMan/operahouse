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

## Follow-up 2026-09-06 (Fable, afternoon): deep research and recalibration

Five parallel research passes (sources/research/DEEP_RESEARCH_2026-09-06.md and the
per-angle reports beside it). Changes made on that evidence:

- RT is Beranek's measured 2001 occupied value (1.59/1.58/1.53/1.46/1.39/1.26 s),
  the only published measurement for the hall. No C80, G, EDT or IACC exists.
- The dome is acoustic plaster (Beranek 1996 p160; Swan 1932). The 36 facets are
  replaced by a flat acoustic-plaster patch in the ceiling plane; faceting a dome
  puts Rindel's diffraction cut-off near 500 Hz and makes coverage patchy.
- Tail law is Barron & Lee revised theory: (31200 T/V) exp(-0.04 r/T) relative to
  the direct sound at 10 m, per source and band, starting at the direct arrival,
  with the explicit image-source energy subtracted (floor 25%). tail_start_ms is
  now 0 and TAIL_RISE_S 2 ms. Validated for a fore-stage source; the pit source is
  outside that validation.
- Seat dip: elevation-scaled excess attenuation of the direct sound on the main
  floor (0.7 dB/m of audience at 400 Hz-3 kHz, 0.5 dB/m at 125 Hz, zero above 15
  degrees), applied to both sources. Exported as seat_dip_db. Low confidence:
  rests mainly on Kahle/Rummler 2025.
- sound_score recentred on occupied opera ranges: G penalty below 0 dB, C80 centred
  on +2.5 dB, seat-dip penalty proportional.

Calibration after the changes (level medians): C80 +1.3..+3.0 dB (target +2..+4
occupied stage source; Barron for this V,T +0.6..+2.2 in the stalls), G -2.4..+1.0
(target -1.5..+1.5), house C80 sd 1.3 (within-house sd 1-2.5 in measured houses),
main-floor centre ITDG 52-55 ms (measured 51). Dress Circle and Balcony G sit at
the low edge. Next geometry job: enrich the explicit reflector set (box fronts,
proscenium splays, side-wall segments) so it carries 35-50% of reflected energy.

## Follow-up 2026-09-06 (Fable, evening): horseshoe fronts and finite reflectors

- The three tier fronts are now the traced HSR 1993 horseshoe curves as vertical
  planar segments facing into the house (both sides), replacing three flat
  centre planes. Every bounded panel carries Rindel's finite-reflector cut-off
  (Plane.dims; 6 dB/octave below f_g = c a*/(2 S cos theta), S = smaller
  dimension squared), so a 3-4 ft fascia returns 2-4 kHz but little at 125 Hz.
- Effect: tier seats gain lateral energy (Grand Tier LF 0.17 to 0.26; the Grand
  Tier front is the first reflection for 186 seats). The main floor is
  unchanged: with a low source and a low listener the specular point on a
  vertical fascia lies below it, so parapets cannot serve the stalls. The
  Orchestra's 13% explicit share is a ceiling/side-wall question.
- sound_score: ITDG penalty now from 20 ms (Hidaka & Beranek recommend <= 20;
  measured houses 14-41), base 94 with a presence bonus for G up to +2 dB, so
  the top no longer saturates at 100 (404 seats had been pinned there).
- Level medians unchanged within 0.3 dB: C80 +1.3..+3.0, G -2.4..+1.0,
  main-floor centre ITDG 55 ms.

## Follow-up 2026-09-07 (Fable): ceiling oval and splayed upper side walls from the 1993 plans

The HSR 1993 attic plan (p139) shows the auditorium ceiling from above and the
upper balcony plan (p137) the walls at that level; Beranek's p159 section and tour
photos 01/05 corroborate. Traced with stage house 135 ft / breadth 113 ft as scale
anchors (sheets differ by up to 8%, so +/-4 ft):

- Recessed oval: about 73 ft across the house, 51-60 ft along it, centre about
  47 ft behind the proscenium, rise about 5 ft. interior_ceiling is now
  dome_radius 36.5, aspect 0.75, dome_z 47, rise 5 (was illustrative 26/0.85/46/7).
  Still an acoustic-plaster patch acoustically; the chandelier is 25-27 ft.
- Upper side walls fan out from the proscenium: half-width about 29 ft at the
  proscenium wall, 49 ft at 37 ft back, full 56.5 ft by about 75 ft. Above the
  box zone (y > 22 ft) the engine now has two splayed bays per side with a mixed
  plaster/curtain coefficient (arch_wall), because the three organ-loft arches on
  those bays are open grilles with heavy curtains behind. The viewer draws the
  same splay (shell.side_wall_plan) with the arches on the splayed bays.
- Effect: Grand Tier ITDG 39 -> 27 ms (splay is its first reflection for 102
  seats), Balcony Circle gains splay reflections; main-floor centre ITDG stays
  55 ms because the splays sit above a low listener's specular point, consistent
  with the measured 51 ms. Level C80/G medians unchanged.
- Conflict recorded (data/geometry_conflicts.json > box_ring_width_vs_plan): the
  mezzanine plan (p107) shows the box-front void only 37-40 ft from centre, not
  the traced 51-53 ft. Seat positions were NOT moved; the ring needs re-tracing
  with its own scale anchor. The 14 out-of-wall box seats are likely this.

## Follow-up 2026-09-07 (Fable, later): box ring registered

The mezzanine plan p107 was registered on its own scale (7.12 px/ft from the
rear stair-tower spacing; sheets differ ~4%) and the void boundary auto-traced:
box rail legs 38-40 ft from centre for z 10-52, rear centre 72-73 ft. SmartSeat's
own plan independently gives boxes/orchestra width 0.98 (old model 1.28, new
1.04). plan_curves.box_ring_rail replaced; old traces kept as previous_value.
Effects: 192 box seats move ~11 ft inward and the rear ring ~7 ft forward; no
box seat is outside the wall any more; 506 rear-Orchestra seats are now under
the box ring (was 274 boxes + 94 Grand Tier), matching listener reports of low
ceilings from about row T; boxes G -0.9 -> +1.1, ITDG 8.5 -> 24 ms. Level C80
medians unchanged (+1.7..+2.5); main-floor centre ITDG 55 ms.

## Note on the pit source and uncertainty (2026-09-07)

The pit source sits at z = +14 ft, inside the house volume in front of the
proscenium, so Barron & Lee's fore-stage condition holds for it at least as
well as for the singer (z = -8 ft, just upstage of the proscenium line). The
pit well's shielding is handled by pit_visible (-5 dB when the pit is hidden).
Pit figures still assume equal source power with the singer. Following the
methods review, the viewer now labels C80 and G with +/-1.5 dB: the best
analytic models reach 1.0-1.4 dB rms against measured halls, and C80's JND is
1 dB, so seat-to-seat differences under about 1.5 dB should not drive a choice.

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

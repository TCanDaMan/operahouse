# Deep Research: making the War Memorial Opera House acoustic model as accurate as the evidence allows

Date: 2026-09-06. Five parallel research passes (measured data, opera-house parameter
ranges, interior geometry and renovation history, hybrid-model methodology, listener and
critic ground truth). Full per-angle reports with every source are in
`deep-research-2026-09-06/`. This file is the synthesis and records what was changed in
the model as a result.

## Executive summary

Exactly one measured acoustic dataset exists for this hall: Beranek's own 2001 occupied
reverberation time, 1.59 / 1.58 / 1.53 / 1.46 / 1.39 / 1.26 s from 125 Hz to 4 kHz
(Beranek 2004, Appendix 3, p. 592), plus the 51 ms main-floor initial time delay gap and
the geometry box on p. 160 of the 1996 edition. No clarity, strength, EDT or IACC was
ever published for the house; it is not among Hidaka and Beranek's 23 measured opera
houses (JASA 107, 2000, p. 369 lists it as questionnaire-only). The only other
measurements, by Paoletti Associates for the 1990s renovation (JASA 103 Suppl. 2861,
1998), are unpublished. Every seat-level acoustic figure for this hall is therefore a
prediction, and the honest way to judge the model is against (a) the measured RT and
ITDG, and (b) the occupied ranges Hidaka and Beranek measured across comparable houses.

Against those ranges the engine as of this morning was wrong in a consistent direction:
level-median C80 of -0.5 to -3 dB where comparable occupied houses run +2 to +4 dB, and
strength G of +0.8 to +2.8 dB where a full 20,000 m³ opera house sits near 0 dB. The
methods research identified the cause as a position-independent Sabine tail (4/R) that
overstates late energy by 0.174 r/T dB (3.5 dB at 30 m), compounded by starting the tail
at a mixing time and ramping it. Replacing that with Barron and Lee's revised theory,
starting the tail at the direct arrival, subtracting the explicit image-source energy,
using the measured RT, treating the dome as the acoustic-plaster absorber Beranek
recorded, and adding an elevation-scaled seat-dip filter moved every level median into
the published ranges without any per-level tuning. Main-floor centre ITDG stays at
52 to 55 ms against the measured 51.

The resulting seat ranking now agrees with the hall's own guidance and with the
multiply-corroborated listener consensus: SF Opera's 2023 patron email recommends the
Grand Tier, Dress Circle and Balcony for sound and the Orchestra for views; forum and
critic reports put the best sound in the upper centre and the weakest in the last ten
Orchestra rows under the Grand Tier overhang, which begins around row T.

## Key findings

1. **Measured RT exists and was not being used.** Beranek 2004 p. 592, occupied, 2001:
   1.59/1.58/1.53/1.46/1.39/1.26 s; RT_mid 1.50 s, bass ratio 1.06. The engine had an
   "assumed" 1.9/1.55/1.4/1.15. Now fixed. Source:
   https://books.google.com/books?id=_jLTBwAAQBAJ (2004 edition), corroborated by
   `sources/research/beranek1996/p160.png` for the geometry box.
2. **The dome is acoustic plaster, not a reflector.** Beranek 1996 p. 160: ceiling
   "plaster except for center domed section which architect says is acoustic plaster."
   Swan's 1932 Architect and Engineer article says concave focusing surfaces were
   deliberately rejected in design. The Carey and Co. 1993 Historic Structure Report
   describes "a large recessed oval" with the 27 ft sunburst chandelier at its centre
   (25 ft per SFGATE/SFCV). No source dimensions the oval; ceiling height is only
   Beranek's H = 73 ft. Source: https://archive.org/details/historicstructur3199care
3. **Calibration ranges (Hidaka and Beranek 2000, Table I, recovered in full).**
   Occupied stage-source C80 +2 to +4 dB; pit-source C80 -2 to +1 dB; occupied G about
   0 dB (-1.5 to +1.5) for a 20,000 to 25,000 m³ house; BQI 0.45 to 0.65; ITDG 14 to
   41 ms across the sample, so SF's 51 ms is a genuine outlier and a hard geometric
   check. Within one house C80 varies seat to seat with sd 1 to 2.5 dB (Garai et al.,
   11 houses); boxes run about 2 dB quieter than stalls; under-balcony seats gain
   +2.6 dB C80 and lose 2.5 dB of late level (Barron 1995). Source:
   https://www.researchgate.net/publication/12672199
4. **Barron and Lee revised theory is the right tail law.** Reflected energy
   (31200 T/V) exp(-0.04 r/T) relative to the direct sound at 10 m; rms error 1.0 dB on G
   and 1.4 dB on C80 over 212 measurements in 19 halls. Barron's 170-measurement test
   shows integrating reflected energy from the direct arrival beats starting at the
   first reflection (early-level rms 1.30 vs 1.61 dB; C80 bias 0.1 vs 1.3 dB). Source:
   https://www.akutek.info/Papers/MB_ConcertHall_SoundLevels.pdf
5. **Do not facet a dome.** Rindel's finite-reflector cut-off puts 36 facets of ~7 m² at
   about 500 Hz and 144 facets at about 2 kHz: faceting creates a low-frequency hole and
   patchy coverage. A true spherical treatment would add a curvature gain of up to
   +10.7 dB in the convergence footprint. With the dome recorded as absorptive, the
   interim flat acoustic-plaster patch is the defensible choice. Source:
   https://strutt.arup.com/help/Auditorium_Acoustics/Rindel_Reflector_Theory.pdf
6. **Seat dip is broadband and elevation-dependent.** Scale-model and transfer-function
   data give about 0.7 dB per metre of audience traversed across 400 Hz to 3 kHz at 0°
   source elevation, falling to nothing above 15°, in addition to the classic 100 to
   160 Hz notch. Neglecting grazing attenuation was a named failure in Round Robin 1.
   Source: https://kahle.be/articles/2025-ForumAcusticumEuronoise2025-ForgetAboutTheSeatDipEffect.pdf
7. **The explicit image-source set is too sparse.** It carries 4 to 17% of reflected
   energy; a complete order-1-2 set should carry 36 to 51%. The subtractive tail keeps
   the totals right, but the missing box fronts, proscenium splays and side-wall
   segments are the next geometry job.
8. **Ground truth.** Beranek's conductor survey ranks the house 13th of 21 opera houses.
   There is no electronic enhancement in the Opera House (the Meyer Constellation is in
   the 299-seat Taube Atrium Theater). The pit takes 90 players, with lift positions
   6'8" / 7'11" / 8'2" below stage and a 4 ft "Torpedo Room" strip under the stage
   since 1938. Seats were replaced in 2013 (boxes), 2015 (Balcony) and 2021
   (Orchestra, Grand Tier, Dress Circle, with Threshold Acoustics briefed to preserve
   RT); the SmartSeat geometry the repo uses is post-2021.
9. **Newly archived primary documents.** The full text of the Carey and Co. 1993
   Historic Structure Report and the 1965 War Memorial rehabilitation report are now in
   `sources/research/hsr1993/` and `sources/research/report1965/`.

## What changed in the model today

| Change | Evidence | Effect |
|---|---|---|
| Tail ramp 25 ms to 2 ms; metric integrates the un-ramped envelope | Barron 2015 Table VII; decomposition over 3,006 seats | Removed a 3 dB house-wide C80 collapse |
| Measured occupied RT replaces assumed RT | Beranek 2004 p. 592 | Bass 0.3 s shorter, treble 0.1 s longer |
| Dome facets replaced by a flat acoustic-plaster patch | Beranek 1996 p. 160; Swan 1932; Rindel cut-off | No LF hole; weak, complete dome return |
| Sabine 4/R replaced by Barron and Lee with distance decay, tail from direct arrival, explicit paths subtracted | Barron 2015 | C80 +3 dB, G -2 to -3 dB, now in range |
| Elevation-scaled seat-dip filter on both sources, main floor | Kahle 2025; Round Robin 1 | Rear Orchestra direct sound -9 to -13 dB mid band |
| Sound score recentred on occupied opera ranges (G 0 dB, C80 +2.5 dB) | Hidaka and Beranek 2000 | Ranking matches SF Opera guidance |

Level medians before (checkpoint cd83c9e) and after:

| Level | C80 before | C80 after | G before | G after | ITDG after |
|---|---|---|---|---|---|
| Orchestra | -1.0 | +1.3 | +2.7 | +1.0 | 37 ms |
| Boxes | +0.6 | +3.0 | +0.9 | -0.9 | 9 ms |
| Grand Tier | -1.9 | +1.6 | +2.5 | +0.2 | 39 ms |
| Dress Circle | -0.7 | +2.4 | +0.8 | -2.4 | 22 ms |
| Balcony Circle | -0.5 | +2.6 | +2.4 | -1.0 | 15 ms |
| Balcony | -0.7 | +2.0 | +2.2 | -2.1 | 7 ms |

House C80 median +2.0 dB (sd 1.3), G median -0.7 dB (sd 2.2). Targets: C80 +2 to +4,
G -1.5 to +1.5, within-house C80 sd 1 to 2.5.

## Contrarian views and risks

- The seat-dip magnitude rests mainly on one 2025 conference paper; the classic
  literature gives a narrow low-frequency notch only. The filter is marked low
  confidence and is the first thing to revisit if rear-Orchestra scores look too harsh.
- Barron and Lee is validated for a fore-stage source. The pit source under the
  proscenium is outside that validation; pit-source figures deserve wider error bars.
- The published 51 ms ITDG exceeds every value in Hidaka and Beranek's sample. Either
  the hall is unusual or the measurement position differed; the model reproduces it,
  which is reassuring but not proof.
- Anstendig (1996, self-published) claims the side boxes have the worst sound and the
  rear under-balcony seats good sound, the opposite of the consensus. Critic Lisa
  Hirsch calls the back Balcony immediate but "harsh." Neither is modelled.
- Dress Circle and Balcony G medians (-2.4, -2.1) sit at or just past the lower edge of
  the target range. Distance and overhang coupling explain part of it; the missing
  explicit reflectors likely explain the rest.
- Model error floor: the best analytic model in the literature is 1.0 to 1.4 dB rms;
  C80's just-noticeable difference is 1 dB. Seat-to-seat differences under about 1.5 dB
  are noise and should not drive a purchase.

## Open questions

1. Oval/dome dimensions and true ceiling height: only the Bancroft Library Arthur Brown
   Jr. drawings (BANC MSS 81/142 c) will settle them.
2. Paoletti Associates' 1990s RT and noise measurements: unpublished; would validate the
   only measured RT and add an unoccupied figure.
3. Whether EDT runs well below RT here (opera houses often show cliff-type decays); if
   so Barron's exponent should use EDT.
4. Enriching the explicit reflector set (box fronts, proscenium splays, side-wall
   segments) to carry 35 to 50% of reflected energy.
5. Dome curvature gain in the convergence footprint, once the dome is dimensioned.

## Sources

Primary and peer-reviewed
- Beranek 2004, Concert Halls and Opera Houses, App. 3 p. 592 (WMOH occupied RT) and p. 141: https://books.google.com/books?id=_jLTBwAAQBAJ
- Beranek 1996, Concert and Opera Halls: How They Sound, pp. 157-160 (repo scan `sources/research/beranek1996/`)
- Hidaka and Beranek 2000, JASA 107(1) 368-383, full text: https://www.researchgate.net/publication/12672199
- Barron 2015, JASA 137(6), revised theory and tests: https://www.akutek.info/Papers/MB_ConcertHall_SoundLevels.pdf
- Barron 2013, Objective assessment of concert hall acoustics: https://www.akutek.info/Papers/MB_Objective_Assessment_2013.pdf
- Barron 2005, ISO 3382 occupancy corrections: https://www.jstage.jst.go.jp/article/ast/26/2/26_2_162/_pdf
- Lindau, Kosanke and Weinzierl 2012, mixing time: https://d-nb.info/1252736983/34
- Aspöck, RWTH thesis, round robins and BRAS: https://publications.rwth-aachen.de/record/808553/files/808553.pdf
- Kahle/Rummler 2025, seat dip: https://kahle.be/articles/2025-ForumAcusticumEuronoise2025-ForgetAboutTheSeatDipEffect.pdf
- Rindel reflector theory (Arup summary): https://strutt.arup.com/help/Auditorium_Acoustics/Rindel_Reflector_Theory.pdf
- Vercammen, concave spherical surfaces: https://dael.euracoustics.org/bin/EAA/aaua_dl?document_id=64913
- Paoletti, Graffy, Tedford, Wetherill 1998, JASA 103(5) Suppl. 2861, abstract only: doi 10.1121/1.421604
- Carey and Co. 1993 Historic Structure Report: https://archive.org/details/historicstructur3199care
- 1965 War Memorial rehabilitation report: https://archive.org/details/reportonrehabili1196publ
- Swan 1932, The Acoustics of the San Francisco Opera House, Architect and Engineer Nov 1932 (repo text `sources/research/ae1932/`)

Institutional and secondary
- SF War Memorial technical specifications: https://sfwarmemorial.org/wp-content/uploads/oh_final17.pdf
- SF Opera seat map: https://www.sfopera.com/contact/seatmap/
- SF Opera backstage blog on the chandelier: https://www.sfopera.com/blog/backstage-with-matthew/2017/backstage-with-matthew-all-change-above/
- Meyer Sound, Taube Atrium Theater Constellation: https://meyersound.com/news/san-francisco-opera/
- Marshall Long, Architectural Acoustics, Table 19.15 (Beranek conductor ranking): https://www.sciencedirect.com/topics/engineering/opera-houses
- Lisa Hirsch, Iron Tongue of Midnight, 2023: https://irontongue.blogspot.com/2023/09/san-francisco-opera-says-quiet-part-out.html
- Anstendig 1996 (contrarian, low credibility): http://www.anstendig.org/OperaHouseRenovation.html
- Listener threads (credibility C): r/opera 1qk32nu, 1d27sgs; r/sanfrancisco 1hn7f8i, 1qfu7ty; r/AskSF 1gp8evs; TripAdvisor k7793046, k7944305; Quora overhang thread

## Rerun inputs
workflow: firecrawl-deep-research
topic: WMOH measured acoustics, opera-house calibration ranges, interior geometry, hybrid image-source plus statistical tail methodology, listener ground truth
depth: exhaustive (five parallel Opus agents, ~120 searches, ~130 scraped sources)
output: markdown (this file) plus HTML artifact

# Calibration ranges for opera-house acoustic parameters

Target of the sanity check: San Francisco War Memorial Opera House — V = 20,900 m³
(Beranek 1996 p160, 738,600 ft³), N ≈ 3,146–3,252, horseshoe with boxes + four upper
tiers, plaster interior, t_I (ITDG, centre of main floor) = 51 ms.
V/N ≈ 6.4–6.6 m³/seat.

Research date 2026-09-06. All raw scrapes are under
`/Users/tyler/Developer/personal/soundpurchase/.firecrawl/p_*.md`.

---

## 0. The single most important source, and what it actually measured

**Hidaka & Beranek, JASA 107(1) 368–383 (2000), "Objective and subjective evaluations
of twenty-three opera houses in Europe, Japan and the Americas."** Full author-uploaded
text was recovered from the ResearchGate publication page (scrape: `p_rg_hb2000.md`):
https://www.researchgate.net/publication/12672199_Objective_and_subjective_evaluations_of_twenty-three_opera_houses_in_Europe_Japan_and_the_Americas
(abstract/metadata: https://pubs.aip.org/asa/jasa/article/107/1/368/550525/Objective-and-subjective-evaluations-of-twenty)

Critical caveat, stated in the abstract: all 23 houses **were measured unoccupied**.
In Table I only `RT_occ,M` and `BR_occ` are occupied quantities, and most of those were
*computed* from unoccupied RTs by the empirical transform of Hidaka et al. (1998); the
rest came from stop-chords recorded during performances. C80,3, G_M, [1−IACC_E3] and
ITDG in Table I are **unoccupied, hall-averaged, omnidirectional source at stage
position S₀**. Anything you calibrate against Table I must respect that.

### Hidaka & Beranek 2000, Table I (verbatim values, source at S₀)

Columns: V (m³) | N | V/S_T (m) | RT_occ,M (s) | EDT_unocc,M (s) | BR_occ | C80,3 (dB) | G_M (dB) | 1−IACC_E3 | ITDG (ms) | stage set

| Hall | V | N | V/S_T | RT_occ,M | EDT_unocc,M | BR_occ | C80,3 | G_M | BQI | ITDG | set |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Amsterdam, Music Theater (AM) | 10 000 | 1689 | – | 1.30 | 1.30 | 1.30 | 1.9 | 1.7 | 0.55 | 32 | n |
| Berlin, Deutsche Oper (BD) | 10 800 | 1900 | 7.5 | 1.36 | 1.60 | 1.30 | 0.7 | 1.2 | 0.39 | 33 | n |
| Berlin, Komische Oper (BK) | 7 000 | 1222 | 7.1 | 1.25 | 1.23 | 1.30 | 3.1 | 6.0 | 0.62 | 20 | y |
| Budapest, Erkel Theater (BE) | 17 000 | 2340 | – | 1.30 | 1.40 | 1.14 | 3.8 | 3.3 | 0.45 | 17 | y |
| Budapest, Staatsoper (BS) | 8 900 | 1450 | – | 1.34 | 1.37 | 1.14 | 1.9 | 4.4 | 0.65 | 15 | y |
| Buenos Aires, Teatro Colón (BA) | 20 570 | 2487 | 9.6 | 1.56 | 1.72 | 1.23 | 1.1 | 2.4 | 0.65 | 18 | y |
| Chicago, Civic Opera House (CC) | 23 000 | 3563 | 9.1 | 1.51 | 1.49 | 1.32 | 2.1 | 0.3 | 0.53 | 41 | n |
| Dresden, Semperoper (DS) | 12 480 | 1300 | 10.3 | 1.60 | 1.83 | 1.23 | 0.8 | 2.7 | 0.72 | 20 | n |
| Essen, Opera House (EO) | 8 800 | 1125 | – | 1.61 | 1.90 | 1.31 | 1.3 | −0.4 | 0.54 | 16 | n |
| Hamburg, Staatsoper (HS) | 11 000 | 1679 | 7.4 | 1.23 | 1.35 | 1.12 | 2.2 | 1.3 | 0.46 | 34 | y |
| London, Royal Opera House (LO) ᵃ | 12 250 | 2120 | 7.7 | 1.10 | 1.04 | 1.07 | 4.5 | 0.7 | 0.53 | 18 | n |
| Milan, Teatro alla Scala (MS) | 11 252 | 2289 | 6.9 | 1.24 | 1.14 | 1.26 | 3.6 | −0.3 | 0.48 | 16 | y |
| New York, Metropolitan Opera (NM) | 24 724 | 3816 | 9.1 | 1.47 | 1.62 | 1.07 | 1.7 | 0.5 | 0.62 | 18 | n |
| Paris, Opéra Garnier (PG) | 10 000 | 2131 | 6.9 | 1.18 | 1.16 | 1.31 | 4.6 | 0.7 | 0.50 | 15 | y |
| Prague, Staatsoper (PS) | 8 000 | 1554 | – | 1.23 | 1.17 | 1.29 | 3.1 | 2.2 | 0.64 | 16 | y |
| Rochester, Eastman Theater (RE) | 23 970 | 3347 | 10.2 | 1.63 | 1.90 | 1.32 | 0.8 | 3.6 | 0.54 | 22 | y |
| Salzburg, Festspielhaus (SF) | 14 020 | 2158 | 8.9 | 1.50 | 1.80 | 1.11 | 1.5 | 1.2 | 0.40 | 27 | n |
| Seattle, Opera House (SO) | 22 000 | 3099 | 11.2 | 2.02 | 2.50 | 1.26 | −0.4 | 2.7 | 0.48 | 25 | n |
| Tokyo, Bunka Kaikan (TB) | 16 250 | 2303 | 9.8 | 1.51 | 1.75 | 1.18 | 1.1 | 0.3 | 0.56 | 14 | n |
| Tokyo, New National Theater (TN) | 14 500 | 1810 | 9.9 | 1.49 | 1.70 | 1.07 | 1.6 | 1.7 | 0.65 | 20 | n |
| Tokyo, Nissei Theater (NT) | 7 500 | 1340 | 7.4 | 1.11 | 1.06 | 1.24 | 4.4 | 5.3 | 0.58 | 17 | y |
| Vienna, Staatsoper (VS) | 10 665 | 1709 | 7.3 | 1.36 | 1.43 | 1.19 | 2.7 | 2.8 | 0.60 | 17 | y |
| Washington, JFK Center Opera (WJ) | 13 027 | 2142 | 8.2 | 1.28 | 1.27 | 1.21 | 4.3 | 3.1 | 0.53 | 15 | y |

ᵃ LO: steel shutter behind main stage closed; its IACC_E3 was converted from LF_E4.

### Hidaka & Beranek 2000, explicit recommended ranges (Conclusions §V)

| Parameter | Recommendation | Condition |
|---|---|---|
| RT_M | 1.4–1.6 s optimum; 1.1–1.3 s judged "too dry" | occupied |
| C80,3 | between 1 and 3 dB throughout the audience | **unoccupied**, source S₀ |
| C80,3 (pit source) | negative values desired for orchestral music | unoccupied |
| BQI = 1−IACC_E3 | should exceed 0.6 | occupied or unoccupied |
| ITDG | 20 ms or less near centre of main floor | – |
| G_M | 1–4 dB | **unoccupied**, hall-averaged, source S₀ |
| BR | larger than 1.05 | occupied |
| Texture | ~15 significant reflections in first 80 ms in best houses | – |

Also from the same paper (numbers, not recommendations):
- C80,3 over 21 houses, source S₀: **mean +2.3 dB, sd 1.2 dB**. Source in pit:
  **mean −1.2 dB, sd 1.0 dB**. Acceptable for singers +1 to +5 dB; for orchestra
  0 to −3 dB.
- Closed/room-tight stage set raises G_M by **about 3 dB** vs a sparse set opening into
  a dead stage house (Fig. 8 lines A vs B differ 2–4 dB).
- Moving the source from stage to pit shifts lines A/B **≈1.0 dB left** (i.e. −1 dB),
  except Vienna where G_M *increases* by 1.2 dB.
- EDT_unocc / RT_occ ≈ **1.1** for the halls in this study.
- BR_occ distribution 1.07–1.32 (narrower than concert halls' 0.92–1.45).
- Simplified Sabine for opera houses: RT_M = K·V/S_T, **K_mid = 0.16** (lower group 0.17,
  upper group 0.15; concert halls 0.14). Mean line usually within 0.1 s of measurement.

---

## 1. Parameter-by-parameter tables

### 1.1 Reverberation time, mid frequencies

| Hall / set | RT_M | Occ? | Band | Seat region | Source |
|---|---|---|---|---|---|
| 23 opera houses (H&B Table I) | 1.10–2.02 s, most 1.23–1.63 | occupied (mostly derived) | 500/1k | hall avg | RG H&B 2000 (above) |
| H&B recommendation | 1.4–1.6 s | occupied | 500/1k | hall avg | same |
| Barron review | "typically 1.3–1.8 seconds" for opera houses | (unstated) | mid | hall avg | http://documentacion.sea-acustica.es/storage/publicaciones/publicaciones_4355fw030.pdf |
| Beranek/Hidaka/Masuda design targets (NNT) | best houses 1.3–1.6 s; design goal 1.5 s | occupied | mid | hall avg | https://www.researchgate.net/publication/12672198_Acoustical_design_of_the_opera_house_of_the_New_National_Theatre_Tokyo_Japan |
| Tokyo NNT (Table III) | stage src 1.5; pit src 1.4–1.5 | **occupied** | 500/1k | 3 stage + 4 pit src positions | RG H&B 2000 |
| Tokyo NNT (Table III) | 1.8 (mid), 1.6–1.7 (low) | **unoccupied** | – | same | RG H&B 2000 |
| Tokyo NNT (Table VI) | 2.26 fire curtain closed / 1.79 nothing / 1.49 reflecting set+occupied | mixed | 500/1k | hall avg | RG H&B 2000 |
| Semperoper Dresden (Arup benchmark) | 1.61 s | occupied | mid | hall avg | https://www.acoustics.asn.au/conference_proceedings/ICA2010/cdrom-ISRA2010/Papers/O4a.pdf |
| Teatro Colón (Arup benchmark) | 1.60 s | occupied | mid | hall avg | same |
| 50 Italian historical houses, Group A (empty/light stage) | T30_M 1.30–1.96 | unoccupied | 500/1k | stalls+boxes avg | https://iris.unife.it/retrieve/handle/11392/2330360/237147/11392_2330360_postprint_PRODI.pdf |
| 50 Italian historical houses, Group B (typical) | T30_M 0.77–1.30 | unoccupied | 500/1k | stalls+boxes avg | same |
| La Scala (Prodi Table II) | T30_M 1.25 | unoccupied | 500/1k | – | same |
| San Carlo Naples (Prodi Table II) | T30_M 1.15 | unoccupied | 500/1k | – | same |
| La Fenice (Prodi Table I) | T30_M 1.60 | unoccupied | 500/1k | – | same |
| La Fenice, pre-fire (Farina/Fausti) | T30 ≈ 1.8 s average over frequency | unoccupied | broad | 27 pts, stalls + balconies | https://angelofarina.it/Public/papers/105-JAES97.PDF |
| Margravial OH Bayreuth | 1.29 ± 0.02 (mid), 1.67 ± 0.11 (low) | unoccupied | 500/1k, 125/250 | stalls | https://arxiv.org/pdf/1905.13578 |
| 11 Emilia-Romagna houses, stalls | T30 500 Hz 0.84–1.91 across halls/sources | unoccupied | per band | stalls | https://cris.unibo.it/bitstream/11585/525525/4/PP%20Acoustic%20measurements%20in%20eleven%20Italian.pdf |

Occupancy effect on RT:
- Tokyo NNT: unoccupied 1.79 → occupied 1.49 s (Δ ≈ 0.30 s), modern lightly-absorbent chairs.
- Italian houses with heavy upholstery: audience reduces RT "less than 0.1 s at
  midfrequencies" (Fausti & Farina, La Fenice paper, https://angelofarina.it/Public/papers/105-JAES97.PDF).
- Farina & Fausti measurement-technique study, 700 people in an 800-seat house:
  max differences 0.3 s for T15 and 1.1 dB for C80
  (https://www.angelofarina.it/Public/papers/141-JSV00.PDF).

### 1.2 Early decay time

| Hall / set | EDT_M | Occ? | Seat region | Source |
|---|---|---|---|---|
| 23 opera houses (H&B Table I) | 1.04–2.50 s; 1.14–1.90 excluding Seattle | unoccupied | hall avg | RG H&B 2000 |
| H&B relation | EDT_unocc/RT_occ ≈ 1.1 | – | hall avg | RG H&B 2000 |
| Beranek/Hidaka/Masuda rule | EDT unoccupied usually 0.1–0.2 s higher than RT occupied, proscenium open | – | hall avg | RG NNT paper |
| Tokyo NNT (Table III) | stage src 1.3–1.4 (occ); 1.6 (unocc) | both | hall avg | RG H&B 2000 |
| Arup benchmarks | EDT/RT = 123% (Dresden), 120% (Colón) | unoccupied EDT / occupied RT | hall avg | ISRA2010 O4a.pdf |
| Arup design target (GNO) | EDT/RT ≥ 85% | – | hall avg | same |
| Italian historical, Group A | EDT_M 0.90–1.79; ≈13% below T30 | unoccupied | stalls+boxes | Prodi JASA 2015 postprint |
| Italian historical, Group B | EDT_M 0.78–1.32; ≈6% below T30 | unoccupied | stalls+boxes | same |
| Italian *modern* theatres (Prodi Table III) | 0.63–1.80 | unoccupied | hall avg | same |
| Regression (modern) | EDT_M = 0.084·V^0.30 | unoccupied | – | same |
| Margravial OH Bayreuth | 1.12 ± 0.15 | unoccupied | stalls | arXiv 1905.13578 |
| 11 Italian houses, stalls @500 Hz | 0.73–1.69 across halls/sources | unoccupied | stalls | Garai et al. B&E 2015 |

Note: in historical horseshoe houses EDT < T30 ("cliff-type" decay from strong early
reflections off the proscenium arch and vault) —
http://www.ica2016.org.ar/ica2016proceedings/ica2016/ICA2016-0729.pdf

### 1.3 Clarity C80

| Hall / set | C80 | Occ? | Band | Seat region | Source |
|---|---|---|---|---|---|
| 23 opera houses, source S₀ | −0.4 to +4.6 dB; **mean +2.3, sd 1.2** | unoccupied | 500/1k/2k (C80,3) | hall avg | RG H&B 2000 |
| Same, source in pit (13 houses) | −2.6 to +2.1 dB; **mean −1.2, sd 1.0** | unoccupied | C80,3 | hall avg | RG H&B 2000 Table IV |
| H&B recommendation | +1 to +3 dB (acceptable +1 to +5 for singers) | unoccupied | C80,3 | throughout audience | RG H&B 2000 |
| H&B pit recommendation | 0 to −3 dB favoured for orchestral music | unoccupied | C80,3 | hall avg | RG H&B 2000 |
| Tokyo NNT (Table III) | stage src **1.7–2.7 unocc → 3.3–3.9 occ**; pit src −2.6–0.3 unocc → 0.1–1.6 occ | both | C80,3 | hall avg | RG H&B 2000 |
| Teatro Colón, pit source | −2.6 dB | unoccupied | C80,3 | hall avg | H&B Table IV; also quoted by Arup ISRA2010 |
| Vienna Staatsoper, pit source | −0.5 dB | unoccupied | C80,3 | hall avg | H&B Table IV |
| NY Met, pit source | −2.3 dB | unoccupied | C80,3 | hall avg | H&B Table IV |
| 50 Italian historical houses | C80,3 0.4–7.0 dB (Group B mostly 2.5–7) | unoccupied | 500/1k/2k | stalls+boxes | Prodi JASA 2015 postprint |
| Prodi regression (modern theatres) | C80,3 = −6.15·ln(EDT_M) + 4.8, R²=0.86 | unoccupied | – | – | same |
| Margravial OH Bayreuth | 0.5–3.2 across positions; stalls mean 1.9 ± 0.6 | unoccupied | – | stalls | arXiv 1905.13578 |
| La Fenice pre-fire | C80 ≈ 3.8 dB, C50 ≈ 0.24 dB | unoccupied | – | 27 pts | angelofarina 105-JAES97 |
| Arup GNO design target | C80_pit −2.0 to +2.0 dB (balconies), −4.0 to 0.0 dB (stalls) | – | – | by region | ISRA2010 O4a.pdf |

### 1.4 Strength G

| Hall / set | G_M | Occ? | Seat region | Source |
|---|---|---|---|---|
| 23 opera houses, source S₀ | **−0.4 to +6.0 dB** | unoccupied | hall avg | RG H&B 2000 Table I |
| Large houses only (V ≥ 20,000 m³) | Chicago 0.3, NY Met 0.5, Seattle 2.7, Rochester 3.6, Colón 2.4 | unoccupied | hall avg | same |
| H&B recommendation | 1–4 dB | unoccupied | hall avg | same |
| Source in pit (13 houses) | −2.1 to +4.0 dB | unoccupied | hall avg | H&B Table IV |
| Stage-set effect | closed room-tight set ≈ **+3 dB** vs sparse set into dead stage house (lines A/B differ 2–4 dB) | unoccupied | hall avg | same |
| Pit vs stage source | ≈ **−1.0 dB** (Vienna is the exception, +1.2 dB) | unoccupied | hall avg | same |
| Tokyo NNT (Table III) | stage 0.3–1.7 unocc → **−0.4 to +0.4 occ**; pit 1.7–2.9 unocc → −1.9 to 0.0 occ | both | hall avg | same |
| Dresden Semperoper / Colón (Arup) | G_stage 2.5 / 2.4 dB; G_pit (Colón) 1.9 dB | – | hall avg | ISRA2010 O4a.pdf |
| Arup GNO target | G_stage ≥ 1.0 dB, G_pit −2 to +2 dB, G_diff −0.5 to +1.5 dB | – | audience avg | same |
| Cirillo/Ando-Beranek preferred | G_mid 1–8 dB | – | – | http://pro.unibz.it/library/bupress/publications/fulltext/9788860461766_20.pdf |
| 50 Italian historical houses (small!) | G_M −2.0 (La Scala) to 13.4 dB (810 m³ house) | unoccupied | stalls+boxes | Prodi JASA 2015 postprint |
| 11 Italian houses, stalls @500 Hz | 8.3–17.3 dB (these are 630–3,360 m³ halls) | unoccupied | stalls | Garai et al. B&E 2015 |

**Boxes vs stalls:** box receivers sit "about 2 dB less" than stalls receivers at the same
source distance (Prodi et al. Fig. 10, four Apulian houses). Rear stalls in horseshoe
houses are *boosted* above Barron-theory prediction by focused reflections from the
curved rear wall, widening the stalls-vs-boxes gap.

**Inside a box:** moving from the box opening to the second row costs "about 5 dB" in
level (Prodi et al. §IV, from Ref. 25).

### 1.5 IACC_E3 / BQI

| Hall | IACC_E3 (0.5–2k) | BQI = 1−IACC_E3 | Occ? | Region | Source |
|---|---|---|---|---|---|
| 23 opera houses (H&B) | – | **0.39–0.72** | unoccupied | hall avg | RG H&B 2000 Table I |
| H&B recommendation | – | > 0.60 | either | hall avg | same |
| Pit source, 13 houses | – | 0.54–0.71 (nearly equal in all but lowest-rated) | unoccupied | hall avg | H&B Table IV |
| Tokyo NNT | 0.37–0.43 unocc (stage), 0.42–0.51 occ | 0.57–0.63 unocc → 0.49–0.58 occ | both | hall avg | H&B Table III |
| Tokyo NNT (Beranek 2004 data) | 0.35 unocc / 0.46 occ | 0.65 / 0.54 | both | hall avg | https://www.akutek.info/binaural_project_files/IACC_data.htm |
| NY Metropolitan Opera | 0.38 | 0.62 | unoccupied | hall avg | akutek (from Beranek 2004) |
| Teatro Colón | 0.35 | 0.65 | unoccupied | hall avg | akutek |
| Vienna Staatsoper | 0.40 (stage), 0.35 (pit) | 0.60 / 0.65 | unoccupied | hall avg | akutek |
| Paris Opéra Garnier | 0.50 (stage), 0.35 (pit) | 0.50 / 0.65 | unoccupied | hall avg | akutek |
| Dresden Semperoper | 0.33 | 0.67 (Arup quote 0.72) | unoccupied | hall avg | akutek / ISRA2010 |
| Milan Teatro alla Scala | 0.52 | 0.48 | unoccupied | hall avg | akutek |
| **La Scala, boxes vs main floor** | – | **0.63 boxes (4 pts, 2 levels) vs 0.38 main floor (6 pts)** | unoccupied | by region | RG H&B 2000 §III I |
| 50 Italian historical houses | IACC_E3 0.17–0.85 | BQI 0.15–0.83 | unoccupied | stalls+boxes | Prodi JASA 2015 |
| 11 Italian houses, stalls | IACC_E3 0.25–0.66, IACC_L 0.17–0.27 | – | unoccupied | stalls/boxes/gallery | Garai et al. B&E 2015 |
| 51-hall corpus mean (Beranek 2004) | IACC_E3 mean 0.43, sd 0.13 | BQI mean 0.57 | mostly unocc | hall avg | akutek |
| Cirillo/Beranek preferred | – | > 0.7 | – | – | unibz bupress PDF |

H&B: "in over half of the opera houses measured spaciousness is lower on the main floors
than in the balconies (boxes)" — the balcony fascia in classical horseshoe houses do not
send early lateral energy to the main floor. Local opera-goers reported to the authors
that sound is superior in the upper tiers.

### 1.6 ITDG t_I

| Hall | ITDG (ms) | Source |
|---|---|---|
| H&B Table VIII, 19 houses (avg of positions 101,102 near centre main floor) | Washington 15, Budapest Staatsoper 15, Garnier 15, La Scala 16, Prague 16, Vienna 17, Budapest Erkel 17, NY Met 18, Colón 18, Berlin Komische 20, Tokyo NNT 20, Dresden 20, Seattle 25, Rochester 26, Tokyo Bunka 26, Amsterdam 32, Berlin Deutsche 33, Hamburg 34, **Chicago 41** | RG H&B 2000 |
| H&B / NNT target | ≤ 20 ms (NNT paper says < 25 ms for an opera house) | RG H&B 2000; RG NNT |
| 50 Italian historical houses | 5–28 ms | Prodi JASA 2015 |
| La Fenice pre-fire | 7 ms near walls → 25 ms mid-hall | angelofarina 105-JAES97 |
| **SF War Memorial** | **51 ms** (Beranek 1996 p160) | repo `data/house_geometry.json` |

### 1.7 Lateral fraction LF

| Set | LF | Region | Source |
|---|---|---|---|
| 4 British opera houses (950–2350 seats, all pre-1910) | **house means 0.18–0.25**; large spread within some houses | pit source; stalls vs upper levels split | Barron JSV 232, 79–100 (2000), https://www.researchgate.net/profile/Mike-Barron/publication/222286895_.../Measured-early-lateral-energy-fractions-in-concert-halls-and-opera-houses.pdf |
| Same | **Stalls generally higher than elsewhere** — the pit rail obscures direct sound from the pit, raising LF | stalls vs tiers | same |
| Same | balcony overhangs have "no particular effect on lateral fractions" | under-balcony | same |
| 17 British concert halls, 189 positions | mean LF 0.19, sd 0.085 | all | same |
| 13 North American concert halls, 138 positions | mean LF 0.15, sd 0.056 | all | same |
| Diffuse-field reference | 0.33 | – | same |
| Two Italian houses post-refurbishment | criterion LF > 0.25 met across bands (except 4 kHz in Ravenna) | stalls+balcony | https://www.mdpi.com/2624-599X/3/2/22 |

Barron's own caution: overlap between halls is so large that describing a hall by its
mean LF is "questionable".

### 1.8 Bass ratio

| Set | BR | Occ? | Source |
|---|---|---|---|
| 23 opera houses (H&B) | **1.07–1.32**, grand average 1.21 | occupied | RG H&B 2000 |
| H&B recommendation | > 1.05 | occupied | same |
| 50 Italian historical houses | **grand average ≈ 1.30**, range 1.0–1.8 | unoccupied | Prodi JASA 2015 |
| 11 Emilia-Romagna houses, stalls | 1.22 (RUS) to 1.74 (CER) | unoccupied | Garai et al. B&E 2015 |
| Margravial OH Bayreuth | 1.29 | unoccupied | arXiv 1905.13578 |
| Cirillo/Beranek preferred | 1.05–1.25 occupied | occupied | unibz bupress PDF |
| Concert halls, for contrast | 0.92–1.45 | occupied | RG H&B 2000 |

### 1.9 ISO 3382-1 just-noticeable differences (for judging model error)

| Parameter | JND |
|---|---|
| EDT | 5% |
| T20, T30 | 5% |
| C50, C80 | 1 dB |
| D50 | 0.05 |
| Ts | 10 ms |
| G | 1 dB |

Source: https://www.odeon.dk/pdf/ISRA2013_Paper_The%20ISO%203382%20parameters_Can%20we%20simulate%20them_Can%20we%20measure%20them_24July2013.pdf
(Table 1, reproducing ISO 3382-1 Annex A). LF JND is 0.05 in the same standard.

---

## 2. Plausible occupied ranges for a 20,900 m³ plaster opera house

Two independent routes to each number: (a) the H&B peer group of large houses
(V 20,000–25,000 m³: Colón, Chicago, NY Met, Seattle, Rochester) and (b) the physics
relations H&B themselves published.

**Peer group by V/N.** SF WMOH V/N ≈ 6.4–6.6 m³/seat, which sits with Chicago Civic
(6.5), NY Met (6.5) and Salzburg (6.5) — i.e. densely seated for its volume, not a
Colón-like 8.3.

| Parameter | Plausible occupied range | Best single estimate | Reasoning |
|---|---|---|---|
| **RT_M (occupied)** | **1.40–1.65 s** | **1.50 s** | Simplified Sabine RT = K·V/S_T, K = 0.16 (range 0.15–0.17). Back out S_T/N from the H&B peer halls (V/S_T ÷ V/N): Chicago 0.71, NY Met 0.71, Rochester 0.70, Seattle 0.63, Colón 0.86 m² of acoustical audience area (incl. edge correction and open proscenium) per seat. SF's density (V/N 6.5) matches Chicago/Met/Rochester, so take S_T/N ≈ 0.70 → S_T ≈ 2,240 m² → V/S_T ≈ 9.3 m → **RT = 0.16 × 9.3 = 1.49 s**; the full S_T/N 0.65–0.80 and K 0.15–0.17 envelope spans 1.23–1.70 s. Peer group agrees: Chicago 1.51, NY Met 1.47, Rochester 1.63, Colón 1.56, Seattle 2.02 (adjustable-louvre multipurpose outlier). H&B's optimum band 1.4–1.6 s brackets it. The repo's assumed 1.55 s is defensible; 1.5 s is the centroid. |
| **RT_L / RT 125 Hz (occupied)** | 1.6–1.9 s | 1.75 s | BR_occ 1.07–1.32 in H&B; a plaster house with boxes sits high in that band. Repo's assumed 1.9 at 125 Hz implies BR ≈ 1.23 — inside the H&B range but near the top; BR 1.15–1.25 is the safer band. |
| **RT 4 kHz (occupied)** | 1.05–1.25 s | 1.15 s | Air absorption plus occupied-audience α ≈ 0.9. Tokyo NNT measured occupied 1.32 at 4 kHz in a 14,500 m³ house; SF's larger volume and air path pull it similar or slightly lower. |
| **EDT_M (unoccupied)** | 1.55–1.80 s | 1.65 s | EDT_unocc ≈ RT_occ + 0.1–0.2 s (NNT design paper) and EDT_unocc/RT_occ ≈ 1.1 (H&B). Peers: Colón 1.72, Met 1.62, Rochester 1.90, Chicago 1.49. |
| **EDT_M (occupied)** | 1.30–1.55 s | 1.40 s | Tokyo NNT occupied EDT_M 1.3–1.4 s against occupied RT_M 1.5 s; in most houses occupied EDT runs slightly *below* occupied RT. |
| **RT_M (unoccupied)** | 1.65–1.95 s | 1.80 s | H&B's Tokyo NNT went 1.79 unocc → 1.49 occ (Δ 0.30 s) with modern chairs. SF's heavily upholstered seating should give a smaller Δ (0.15–0.30 s). Italian houses with velvet seats show Δ < 0.1 s — that is a lower bound, not a prediction for SF. |
| **C80,3 (unoccupied, stage source, hall avg)** | **+1 to +3 dB** | **+2 dB** | H&B corpus mean +2.3, sd 1.2; H&B optimum band is exactly 1–3 dB. Prodi's modern-theatre regression with EDT_M 1.65 gives C80,3 = −6.15·ln(1.65) + 4.8 = **+1.7 dB** — independent agreement. |
| **C80,3 (occupied, stage source, hall avg)** | **+2 to +4 dB** | **+3 dB** | Occupancy raised NNT's C80,3 from 1.7–2.7 to 3.3–3.9 dB, i.e. **+1.3 to +1.5 dB**. Apply that offset to the unoccupied estimate. |
| **C80,3 (occupied, pit source, hall avg)** | **−2 to +1 dB** | **−1 dB** | H&B pit-source corpus mean −1.2 dB, sd 1.0, unoccupied; occupancy adds ~+1 dB (NNT went −2.6–0.3 → 0.1–1.6). Large houses run to the negative end: Colón −2.6, Met −2.3. |
| **G_M (unoccupied, stage source, hall avg)** | **−0.5 to +2.5 dB** | **+1.0 dB** | Volume is the dominant term. The 20,000–25,000 m³ H&B houses without a room-tight set sit at 0.3–0.5 dB (Chicago, Met); those with a closed set or reverberant tower reach 2.4–3.6 (Colón, Rochester). Which one SF looks like depends entirely on the production's stage set. |
| **G_M (occupied, stage source, hall avg)** | **−1.5 to +1.5 dB** | **0 dB** | Occupancy took NNT from 0.3–1.7 to −0.4 to +0.4 dB, i.e. ≈ −1.0 dB. This is the number most likely to surprise: a full opera house at 500/1k Hz is roughly *0 dB* strength, far below a concert hall's 4–6 dB. |
| **G_M (pit source)** | ≈1 dB below the stage-source value | −1 dB occupied | H&B: pit shifts the G lines 1.0 dB left. |
| **BQI = 1−IACC_E3 (hall avg)** | **0.45–0.65** | **0.55** | Large horseshoe houses cluster low on the main floor: Chicago 0.53, Rochester 0.54, Seattle 0.48, La Scala 0.48, Garnier 0.50; Met 0.62 and Colón 0.65 are the top of the class. A wide house with a 51 ms main-floor ITDG will not deliver H&B's ≥0.6 on the main floor. Expect main floor ≈ 0.40–0.50, boxes/tiers ≈ 0.55–0.70. |
| **ITDG (centre main floor)** | measured 51 ms | 51 ms | Given, not predicted. It exceeds every value in H&B's 19-house Table VIII (max Chicago 41 ms) — a genuine outlier for this hall class and a strong constraint on any geometric model. If the model returns ≈20 ms at the centre of the main floor, the model is wrong. |
| **LF (mid, pit source)** | 0.15–0.30, house mean ≈ 0.20 | 0.20 | Barron's four British houses gave house means 0.18–0.25; stalls above tiers. |
| **BR (occupied)** | **1.10–1.30** | **1.20** | H&B corpus 1.07–1.32, grand average 1.21. A plaster horseshoe with boxes belongs in the upper half: 1.20–1.25. |
| **Texture** | ~11–15 significant reflections in first 80 ms | 13 | H&B counted 15 for the best houses (Milan, Colón, NNT, Budapest, Berlin Deutsche) and 11 for the worst (Hamburg, Seattle, Prague, Rochester). |

**Sanity anchors, phrased as failure conditions for the model:**
- Occupied mid RT outside 1.35–1.70 s → wrong.
- Hall-mean occupied C80,3 outside +1 to +5 dB (stage source) → wrong.
- Hall-mean occupied G_M above +4 dB or below −3 dB → wrong (you have accidentally
  built a concert hall or lost the direct sound).
- Hall-mean BQI above 0.75 or below 0.35 → wrong.
- BR outside 1.05–1.40 → wrong.
- Predicted ITDG at main-floor centre far from 51 ms → geometry is wrong.

---

## 3. Within-hall, seat-to-seat variation — the evidence

### 3.1 How much does C80 vary within one house?

- **Garai, Morandi, D'Orazio, De Cesaris & Loreti, Building & Environment 94(2)
  900–912 (2015)**, 11 Italian historical opera houses, >50,000 impulse responses.
  Their Tables 6 and 7 give per-hall mean/sd/skew over *stalls positions only*:
  **C80 standard deviation within the stalls is 1.0–2.5 dB per octave band**
  (typical 1.2–1.8 dB at 500 Hz, rising with frequency), with consistently **positive
  skew** (a few very-clear seats pull the tail). EDT sd within stalls 0.10–0.29 s;
  T30 sd only 0.02–0.09 s; G sd 0.8–2.5 dB.
  https://cris.unibo.it/bitstream/11585/525525/4/PP%20Acoustic%20measurements%20in%20eleven%20Italian.pdf
  Their own summary: reverberation times are homogeneous in space, while the
  early-reflection-dependent criteria vary strongly with position.
- **Fausti & Farina, JSV (2000)**, Teatro Comunale Ferrara: between three positions in
  the same hall, C80 differed **by up to 8 dB at 250 Hz**, while T15 differed by only
  0.3 dB-equivalent (0.3 s at 125 Hz). Their conclusion: for clarity, position matters
  more than audience presence or any measurement variable.
  https://www.angelofarina.it/Public/papers/141-JSV00.PDF
- **H&B 2000** give the *between-hall* sd of hall-averaged C80,3 as 1.2 dB. Combining:
  the within-hall seat-to-seat spread (sd ≈ 1.5 dB, range ≈ 8 dB) is **larger than the
  entire spread between famous opera houses**. Any per-seat model must produce a
  distribution at least this wide or it is under-dispersed.

### 3.2 Boxes and upper tiers vs stalls

| Effect | Magnitude | Source |
|---|---|---|
| G in boxes vs stalls at equal source distance | **≈ 2 dB lower in boxes** | Prodi et al. 2015 Fig. 10 (BA, BT, RO, LU) |
| Level at second row inside a box vs box opening | **≈ 5 dB lower** | Prodi et al. §IV (from Ref. 25) |
| C80 in centre boxes vs mid-stalls | centre boxes **higher** C80 than stalls centre rows, across the spectrum | Prodi et al. Fig. 11 (Bari, Lucera) |
| C80 in side / high boxes | **lowest clarity in the house**, with significant drops in the high-frequency bands | same |
| EDT in boxes vs stalls | box EDT **depressed at mid frequencies** (box absorption eats early sound); stalls show the 125 Hz seat-dip, boxes do not; T20 differences stalls-vs-boxes are not significant | Prodi et al. Fig. 9 (Modena) |
| BQI boxes vs main floor | **La Scala: 0.63 in boxes vs 0.38 on the main floor** | H&B 2000 §III I |
| BQI, general | in >half of 23 houses, spaciousness is lower on the main floor than in balconies/boxes | H&B 2000 Fig. 12 |
| Rear stalls of a horseshoe | G is **boosted above Barron-theory prediction** by strong, sometimes focused, reflections off the curved rear wall | Prodi et al. §IV |
| Reflection directionality in a side box (2nd tier) | loudest reflections arrive only from the front within **±45°**; reflections from inside the box, from below, and from the soffit are weak/irrelevant | Prodi et al. Fig. 12a (Ambisonic mapping) |
| LF, stalls vs upper levels (pit source) | **stalls higher** — the pit rail obscures the direct sound, raising the lateral fraction | Barron JSV 2000 §6 |
| Sound in the boxes generally | box volume with drapes acts as a low-frequency resonator and a high-frequency absorber; no seat-dip effect | Prodi et al. §IV |

### 3.3 Under-balcony / overhang

**Barron, "Balcony overhangs in concert auditoria", JASA 98(5) Pt.1, 2580–2589 (1995)**
— 7 halls, overhang depth/height ratios 1.1–3.1. Concert halls, but this is the only
quantified overhang dataset and Barron applies the same treatment in the opera chapter of
*Auditorium Acoustics and Architectural Design*.
https://www.researchgate.net/publication/243518823_Balcony_overhangs_in_concert_auditoria

| Quantity under the overhang | Mean change | Mean vs revised theory |
|---|---|---|
| Early sound level (0–80 ms) | **−0.3 dB** | −0.2 dB |
| Late sound level | **−2.5 dB** | −2.8 dB |
| Total level (G) | **−1.3 dB** (range −2.6 to +0.7 dB) | −1.4 dB |
| Early-to-late index (C80) | – | **+2.6 dB** |
| EDT ratio (overhung / mean exposed) | **0.84 mean, 0.65 minimum** | – |

Mechanism, per Barron: the overhang blocks the ceiling reflection and much of the diffuse
late field, but the soffit and rear wall supply local early reflections that grow toward
the back rows — so *within* an overhung block, excess early level and C80 both **increase**
as you move further under, while late level stays roughly constant. EDT falls
progressively as the vertical angle of view narrows (r = 0.57, significant at 5%).
Beranek's design guide (via Barron) is a depth/height ratio D/H limit at the opening.

Barron also notes (JSV 2000) that a balcony above a measurement position has only a small
influence on **LF**, because both the ceiling and cornice reflections it blocks are
non-lateral anyway.

### 3.4 Within-stalls trends with distance

- EDT vs distance from source in the stalls is **not monotonic**: in some historical
  houses EDT drops sharply in the rear stalls, in others it increases with distance;
  the source position changes the absolute value but not the trend.
  https://dael.euracoustics.org/confs/acoustics2008/data/fa2005-budapest/paper/636-0.pdf
- Barron's revised theory with V = V_hall (cavea only, *excluding* the fly tower) fits
  measured G vs distance for mid-sized Italian houses when the source is on the forestage;
  for small halls the fit degrades because r approaches the critical distance.
  http://www.ica2016.org.ar/ica2016proceedings/ica2016/ICA2016-0729.pdf
  For a 20,900 m³ house with a large fly tower, this says: use the audience-chamber
  volume in the revised-theory tail, not V_hall + V_stage.

---

## 4. Source quality and conflicts

### Tier 1 — primary, peer-reviewed, directly usable
1. **Hidaka & Beranek, JASA 107(1) 368–383 (2000).** The reference dataset for this hall
   class. 23 houses, one instrument team (Takenaka R&D), consistent method. Full text
   recovered. **Limitation: all measurements unoccupied**; the occupied RT column is
   largely a computed transform (Hidaka et al. 1998), and the paper itself warns that
   literature occupied RTs from stop chords are "expected to be off by ±0.1 s".
   Beranek explicitly asks that the subjective rank-ordering not be used to claim one
   hall superior to another.
2. **Beranek, Hidaka & Masuda, JASA 107(1) 355–367 (2000)** (NNT Tokyo). Design-target
   rationale plus the only opera house in the corpus with a full occupied/unoccupied
   parameter pair. https://www.researchgate.net/publication/12672198_...
3. **Prodi, Pompoli, Martellotta & Sato, JASA 138(2) 769 (2015),** "Acoustics of Italian
   Historical Opera Houses." 50 houses, plus the box/stalls/gallery physics. Postprint:
   https://iris.unife.it/retrieve/handle/11392/2330360/237147/11392_2330360_postprint_PRODI.pdf
4. **Garai, Morandi, D'Orazio, De Cesaris & Loreti, Building & Environment 94(2), 900–912
   (2015).** 11 houses, separate ISO 3382 tables for **stalls / boxes / gallery** and
   per-hall sd and skew. The best source in this collection for within-hall spread.
5. **Barron, JASA 98(5) 2580 (1995)** balcony overhangs; **Barron, JSV 232, 79–100 (2000)**
   lateral fractions incl. four British opera houses.
6. **Fausti & Farina, JSV (2000)**, measurement-technique and position/occupancy effects.

### Tier 2 — usable with care
- **akutek.info IACC compilation** (https://www.akutek.info/binaural_project_files/IACC_data.htm):
  a transcription of Beranek 2004 tables plus Bradley/Takenaka data. Convenient and
  matches H&B where they overlap, but it is a third-party transcription, not the book.
- **Arup / Greek National Opera, ISRA 2010** (O4a.pdf): design targets and Dresden/Colón
  benchmarks. Its Dresden/Colón numbers are Beranek's, re-quoted — treat as the same
  source, not independent confirmation. Its BQI for Dresden (0.72) matches H&B Table I;
  its Colón 0.65 matches too.
- **Krauss et al., arXiv:1905.13578** (Margravial Opera House Bayreuth). Careful and
  self-aware, but the sources were **bursting balloons and hand-claps**, not ISO 3382
  sweeps, and only the stalls were characterised. Explicitly flags that loge/box C80
  was not measured. Good for a Baroque-house sanity point, not for a 20,900 m³ house.
- **ICA 2016 PROMETHEE paper** (ICA2016-0502.pdf): its data tables are images that did
  not survive extraction; useful only for its restatement of H&B's parameter set.

### Tier 3 — do not calibrate against these
- The **Italian historical house corpus** as a whole (Prodi Group A/B, Garai, small-house
  papers). These are 800–13,700 m³ rooms with T30_M around 1.0–1.2 s and G_M up to
  13 dB. Prodi's own conclusion: "regular" historical opera houses are dry compared to
  modern houses and only rarely fall inside the H&B suggested range. Using their C80
  (often 4–7 dB) or G (often 8–13 dB) to check a 20,900 m³ house would be a category
  error. Use them **only** for stalls/boxes/gallery *relative* differences and for
  within-hall spread.

### Explicit conflicts found
1. **Occupied vs unoccupied is inconsistently reported across the literature.** H&B
   report C80,3, G_M, BQI and ITDG unoccupied but RT and BR occupied, in the same table.
   Prodi et al. are all-unoccupied. Any calibration table that omits the occupancy state
   is unusable. Concretely: C80,3 moves by **+1.3 to +1.5 dB** and G_M by **−1.0 dB** on
   going from unoccupied to occupied (Tokyo NNT, H&B Table III).
2. **How much does the audience change RT?** Tokyo NNT: 1.79 → 1.49 s (Δ 0.30 s).
   Fausti & Farina for Italian houses with heavy upholstery: **"less than 0.1 s"** at mid
   frequencies. Both are true; the difference is chair absorption. NNT's own occupied
   mid-frequency audience α was 0.61, versus ~0.80 in most houses (H&B Table V note) —
   so even the "modern" figure is chair-specific. For SF, assume Δ 0.15–0.30 s and carry
   the uncertainty.
3. **La Fenice disagrees with itself across campaigns.** Fausti/Farina (1995, pre-fire,
   gunshot + dummy head, 27 points): T30 ≈ 1.8 s, EDT ≈ 1.25 s, C80 ≈ 3.8 dB, IACC50
   ≈ 0.2–0.3. Prodi et al. Table I (PRIN dataset): T30_M = 1.60, EDT_M = 1.45,
   C80,3 = 0.8, IACC_E3 = 0.52. Different states of the room and different methods.
   Treat single-hall literature values as ±0.2 s / ±2 dB unless the campaign is named.
4. **Dresden Semperoper BQI: 0.72 (H&B Table I / Arup) vs 0.67 (akutek from Beranek
   2004, IACC_E3 = 0.33).** Small, but it shows the book and the paper are not identical.
5. **BQI target ≥0.6 (H&B) vs >0.7 (Cirillo et al. 2011, quoted in the unibz chapter).**
   The stricter number is a preference-model target, not a survey-derived range; 0.6 is
   the defensible threshold.
6. **Barron on the value of mean LF.** He publishes opera-house LF means (0.18–0.25) and
   then argues the between-hall overlap makes a hall's mean LF a questionable descriptor.
   Use LF per-seat, not as a hall figure of merit.
7. **SF War Memorial's own ITDG of 51 ms is outside the entire H&B sample** (14–41 ms).
   Either Beranek's t_I for this hall reflects a genuinely unusual main-floor geometry
   (wide house, distant side walls, high/remote ceiling) — in which case the model must
   reproduce it and should predict a *below-average* main-floor BQI — or the measurement
   position differed from H&B's 101/102 convention. It is worth flagging as the single
   most distinctive published number about this hall.
8. **No measured RT, C80, G, or IACC for SF War Memorial Opera House was found** in any
   accessible source. It is not in the H&B 23. Beranek 1996 p160 supplies V, N, and t_I
   only. Every RT/C80/G figure for this hall in the repo is therefore an inference, and
   the ranges in §2 above are the honest bounds on that inference.

---

## Appendix — full source list (all scraped this session)

| # | Source | URL | Local scrape |
|---|---|---|---|
| 1 | Hidaka & Beranek, JASA 107(1) 368 (2000), full text | https://www.researchgate.net/publication/12672199_Objective_and_subjective_evaluations_of_twenty-three_opera_houses_in_Europe_Japan_and_the_Americas | p_rg_hb2000.md |
| 2 | Same, publisher abstract | https://pubs.aip.org/asa/jasa/article/107/1/368/550525/Objective-and-subjective-evaluations-of-twenty | p_aip_hb2000.md |
| 3 | Beranek, Hidaka & Masuda, JASA 107(1) 355 (2000), NNT Tokyo | https://www.researchgate.net/publication/12672198_Acoustical_design_of_the_opera_house_of_the_New_National_Theatre_Tokyo_Japan | p_rg_nnt.md |
| 4 | Prodi, Pompoli, Martellotta & Sato, JASA 138(2) 769 (2015) | https://iris.unife.it/retrieve/handle/11392/2330360/237147/11392_2330360_postprint_PRODI.pdf | p_8c4775b8.md |
| 5 | Garai et al., Build. Environ. 94(2) 900 (2015), 11 Italian houses | https://cris.unibo.it/bitstream/11585/525525/4/PP%20Acoustic%20measurements%20in%20eleven%20Italian.pdf | p_eleven.md |
| 6 | Barron, JASA 98(5) 2580 (1995), balcony overhangs | https://www.researchgate.net/publication/243518823_Balcony_overhangs_in_concert_auditoria | p_rg_balcony.md |
| 7 | Barron, JSV 232, 79 (2000), early lateral energy fractions | https://www.researchgate.net/profile/Mike-Barron/publication/222286895_Measured_early_lateral_energy_fractions_in_concert_halls_and_opera_houses/links/5c3e1df5a6fdccd6b5aef647/Measured-early-lateral-energy-fractions-in-concert-halls-and-opera-houses.pdf | p_barron_lf.md |
| 8 | Barron, "Current state of acoustic design of concert halls and opera houses" | http://documentacion.sea-acustica.es/storage/publicaciones/publicaciones_4355fw030.pdf | p_seaacust.md |
| 9 | Fausti & Farina, JSV (2000), measurements in opera houses | https://www.angelofarina.it/Public/papers/141-JSV00.PDF | p_7ab25855.md |
| 10 | Farina/Fausti, La Fenice pre-fire (JAES 1997) | https://angelofarina.it/Public/papers/105-JAES97.PDF | p_fenice.md |
| 11 | Krauss et al., arXiv:1905.13578, Margravial OH Bayreuth | https://arxiv.org/pdf/1905.13578 | p_68699932.md |
| 12 | Beranek 2004 IACC compilation (akutek) | https://www.akutek.info/binaural_project_files/IACC_data.htm | p_ee9f4488.md |
| 13 | Arup / Greek National Opera, ISRA 2010 design targets | https://www.acoustics.asn.au/conference_proceedings/ICA2010/cdrom-ISRA2010/Papers/O4a.pdf | p_greece.md |
| 14 | ICA 2016 — sound energy distribution in Italian opera houses | http://www.ica2016.org.ar/ica2016proceedings/ica2016/ICA2016-0729.pdf | p_energydist.md |
| 15 | ICA 2016 — rank-ordering opera houses (PROMETHEE II) | http://www.ica2016.org.ar/ica2016proceedings/ica2016/ICA2016-0502.pdf | p_adecf09f.md |
| 16 | Acoustical characterisation of small Italian opera houses | https://dael.euracoustics.org/confs/acoustics2008/data/fa2005-budapest/paper/636-0.pdf | p_smallital.md |
| 17 | Ranking Italian historical opera houses (unibz, preference criteria) | http://pro.unibz.it/library/bupress/publications/fulltext/9788860461766_20.pdf | p_rankital.md |
| 18 | ISO 3382 parameters & JNDs (ODEON, ISRA 2013) | https://www.odeon.dk/pdf/ISRA2013_Paper_The%20ISO%203382%20parameters_Can%20we%20simulate%20them_Can%20we%20measure%20them_24July2013.pdf | p_iso3382.md |
| 19 | Refurbishment of two Italian opera theatres (Acoustics MDPI) | https://www.mdpi.com/2624-599X/3/2/22 | p_refurb.md |
| 20 | Italian-style opera houses: a historical review (Appl. Sci. MDPI) | https://www.mdpi.com/2076-3417/10/13/4613 | p_mdpi_ital.md |
| 21 | Height dimension of concert halls and opera houses (DAGA 2025) | https://pub.dega-akustik.de/DAS-DAGA_2025/files/upload/paper/4.pdf | p_daga_height.md |
| 22 | Barron LF publication landing page (abstract + citing snippets) | https://www.researchgate.net/publication/222286895_Measured_early_lateral_energy_fractions_in_concert_halls_and_opera_houses | p_rg_lf.md |

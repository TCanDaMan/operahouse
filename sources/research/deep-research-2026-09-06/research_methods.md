# Methodology review: hybrid image-source + statistical-tail room models
### For a seat-by-seat opera-house model (V ≈ 20,000 m³, coarse surface set, ISM order 1–2, diffuse tail = 4/R)

Research date 2026-09-06. Sources scraped with Firecrawl unless marked. Quality notes are per-item.
Working assumptions used in the arithmetic below (they mirror the model under review):
**V = 20,000 m³, S = 8,000 m², mean free path 4V/S = 10 m (29.2 ms/order), RT_mid ≈ 1.4–1.6 s.**

---

## Q1. Mixing time / transition time

### 1.1 The four families of estimator, with formulas

Reflection density from the mirror-source model of a rectangular room (Kuttruff):

```
dN/dt = 4π c₀³ t² / V          [reflections per second]
```

**(a) Polack √V rule.** Set dN/dt = 400 s⁻¹ (10 reflections inside the 24 ms auditory
time-resolution window) and solve for t:

```
t_mix ≈ √V   [ms, V in m³]
```

Derivation and the ergodic/billiard justification are given in Lindau et al. §1.1 and in the
AES paper below. → **141 ms** for V = 20,000 m³.
Source (primary, JAES 60(11), full text): https://d-nb.info/1252736983/34 — high quality.
Secondary with the same derivation: https://suonoevita.it/media/medialibrary/2020/04/2012_paper_AES_mixingTime.pdf — AES convention paper, medium quality (small-room focus).

**(b) Rubak & Johansen / mean-free-path rule.** Four mean free paths:

```
t_mix ≈ 4·l_m/c₀ = 4·(4V/S)/c₀ ≈ 47·V/S   [ms]
```

→ **118 ms**. Same source (Lindau et al. Eq. 4).

**(c) Lindau, Kosanke & Weinzierl 2012 — *perceptual* mixing time.** Nine shoebox rooms
(V = 182 → 8,500 m³), dynamic binaural auralisation, adaptive forced-choice test with expert
listeners. Best predictors:

```
t_mp50 = 20·(V/S) + 12    [ms]   R² = 81.5 %      (average listener)
t_mp50 = 0.58·√V + 21.2   [ms]   R² = 78.6 %
t_mp95 = 0.0117·V + 50.1  [ms]   R² = 78.7 %      (95 % point, "close to authentic")
signal-based: t_mp50 = 0.8·t_mix(Abel&Huang, criterion I) − 8   [ms]  R² = 74.7 %
```

→ t_mp50 = **62 ms** (V/S form) or **103 ms** (√V form); t_mp95 = 284 ms but that is a large
extrapolation beyond their 8,500 m³ ceiling and should not be trusted for an opera house.
Their headline conclusion: about **two mean free paths / two reflection orders**, and a
reflection density of **< 200 s⁻¹**, already sounds diffuse to trained listeners — far below the
400–10,000 s⁻¹ values previously assumed in the literature. In their earlier auditorium study
(V = 8,500 m³, RT 2 s) the measured perceptual mixing time reached **140 ms**.
Source (primary): https://d-nb.info/1252736983/34 (JAES preprint/full text, retrieved via WebFetch + pdftotext) — **highest quality item in this section**.
Record page: https://depositonce.tu-berlin.de/items/47045cb9-0ae3-489e-9e87-b175e0f5ae02

**(d) Abel & Huang echo-density profile (signal-based).** Sliding window (≈ 20–30 ms;
1024 samples typical), count the fraction of taps outside one window standard deviation,
normalise by erfc(1/√2) = 0.3173; mixing time = first time η(t) reaches 1.

```
η(t) = (1/0.3173)·(1/(δ+1))·Σ_{τ=t}^{t+δ} 1{|h(τ)| > σ},   σ = √( (1/(δ+1))·Σ h²(τ) )
```

Sources: https://suonoevita.it/media/medialibrary/2020/04/2012_paper_AES_mixingTime.pdf (full formulas, medium quality);
https://research.aalto.fi/en/publications/a-simple-robust-measure-of-reverberation-echo-density (record for Abel & Huang AES 121, 2006).

**(e) Hidaka "transition time" t_L (JASA 122(1), 326, 2007).** Defines the boundary as the time
at which the energy correlation between the direct-plus-initial sound and the subsequent
decaying sound first drops to a specified low value. Fitted over **59 concert halls**:

```
t_m,500Hz = 80 · RT_500Hz   [ms]
```

→ **112–128 ms** for RT 1.4–1.6 s. In Lindau's evaluation this frequency-domain estimator was
the weakest perceptual predictor (R² ≈ 56–57 % at 500 Hz/1 kHz), but it is the only estimator
fitted on *halls* rather than shoeboxes and lecture rooms.
Abstract: https://pubs.aip.org/asa/jasa/article/122/1/326/812777/A-new-definition-of-boundary-point-between-early — primary but paywalled (abstract only); the regression is quoted verbatim in Lindau et al. Eq. 5.

### 1.2 Summary table for this hall (V = 20,000 m³, S = 8,000 m², RT 1.4–1.6 s)

| Estimator | Value |
|---|---|
| Polack √V | 141 ms |
| Lindau t_mp50 = 20·V/S + 12 | **62 ms** |
| Lindau t_mp50 = 0.58√V + 21.2 | 103 ms |
| Rubak & Johansen 47·V/S | 118 ms |
| Hidaka 80·RT (RT 1.4 / 1.6 s) | 112 / 128 ms |
| 2 mean free paths | 58 ms |
| 4 mean free paths | 117 ms |
| Lindau t_mp95 (extrapolated, unreliable) | 284 ms |

Reflection density in this hall (dN/dt = 4πc³t²/V): 10 s⁻¹ at 20 ms, **162 s⁻¹ at 80 ms**,
254 s⁻¹ at 100 ms, 365 s⁻¹ at 120 ms. Density reaches Lindau's just-audible 171 s⁻¹ at 82 ms
and the classical 400 s⁻¹ at 126 ms.
**Defensible band for this hall: 60–140 ms, central estimate ≈ 100–120 ms.**

### 1.3 Where the tail should start: at the direct sound, at the first reflection, or cross-faded

This is the single most consequential answer in the review, and it is **empirical**, not a matter of taste.

Barron's revised theory rests on assumption (2): *significant reflected energy arrives from the
moment after the direct sound arrives*. Vorländer proposed the alternative — start integrating
reflected energy at the arrival of the first reflection, whose mean delay is 4V/cS. Barron
tested both against **170 measurements in 16 halls** (mean ITDG 20 ms):

| Measure | Theory using direct sound: mean / rms error | Theory using first-reflection arrival: mean / rms |
|---|---|---|
| Early | 0.2 / 1.30 dB | **0.9 / 1.61 dB** |
| Total | 0.2 / 1.02 dB | 0.3 / 1.11 dB |
| Early-to-late (C80) | 0.1 / 1.41 dB | **1.3** / 1.28 dB |

"In all but one case the errors are smaller … based on the direct sound start time." Using the
first-reflection start reduced predicted early sound by **1.1 dB** and total level by **0.5 dB**;
C80 bias moved by 1.2 dB. Barron's stated reason: early reflections are discrete events that
produce stepped integrated decays, so the integration limit should *assume the smearing of
discrete reflection energy*.
Source (primary, JASA 137(6), 2015): https://www.akutek.info/Papers/MB_ConcertHall_SoundLevels.pdf — **high quality, full text, Table VII §V A**.

**Practical conclusion.** For an *energy/metric* model whose explicit early reflections are
incomplete, the statistical reflected energy must be integrated from the direct-sound arrival
(t₀ = r/c), not from a mixing time. The mixing time is the right crossover only for an
*auralisation* model whose deterministic part is genuinely complete up to that time
(ODEON/CATT/RAVEN-class, transition order 2–3 with full geometry, or Lehmann–Johansson's ISM
truncated at t_c). Cross-fading is a perceptual smoothing device, not an energy fix — DAFx-25
explicitly reports "no crossfade or smoothing is applied" once the tail's energy decay and
echo-density profile match the deterministic part.
Source: https://eprints.whiterose.ac.uk/id/eprint/237877/1/DAFx25_paper_17.pdf §2.3, §3.4 — recent peer-reviewed conference paper, good quality.

---

## Q2. Energy accounting: avoiding double-counting, tail level, build-up shape, Barron–Lee

### 2.1 How the established hybrids avoid double counting

**ODEON (Naylor/Rindel).** Image sources are enumerated up to a *transition order* (TO);
above TO the same rays that generated those images continue and become secondary sources on
the surfaces. The energy is conserved by construction because the ray carries the residual
energy — there is no separately-normalised statistical tail. "Only 500 to 1000 rays are
sufficient … an optimum transition order has been found to be **two or three**." The two
processes deliberately overlap in time: the last image-source arrival is later than the first
secondary-source arrival.
Sources: https://odeon.dk/pdf/ASA_1992_Naylor.pdf and https://www.odeon.dk/pdf/AustralAc_1995_Rindel.pdf — primary-author papers, high quality.
Confirmed in the ODEON ISO-3382 paper: image sources "up to a transition order, typically up to 2nd order", then Fibonacci-spiral ray shooting with reflection- and vector-based scattering:
https://www.odeon.dk/pdf/ISRA2013_Paper_The%20ISO%203382%20parameters_Can%20we%20simulate%20them_Can%20we%20measure%20them_24July2013.pdf

**Wayverb (explicit statement of both rules).** Two independent mechanisms:
1. *Order rule* — the stochastic ray tracer records specular and diffuse contributions
   separately, and **specular ray contributions are only added above the highest image-source
   order**. Otherwise "this will lead to a duplication of energy".
2. *Scattering rule* — image-source reflectance is multiplied by **(1 − s)** per reflection
   (s = scattering coefficient), so image sources die away faster and the "missing" energy is
   supplied by the ray tracer's diffuse output. This lets the two overlap in time without
   double counting.
   Also: image-source depth beyond 5–6 is pointless because specular→scattered conversion is
   unidirectional (Kuttruff 2009, p. 126).
Source: https://reuk.github.io/wayverb/hybrid.html — thesis-quality documentation with citations; medium-high quality (not peer reviewed, but the rules match the literature).

**Lehmann & Johansson (JASA 124(1) 269, 2008; IEEE TASLP 2010) — "hybrid reverberation" done
subtractively.** The ISM is computed only up to a transition time t_c defined as the time at
which the *energy decay curve* has fallen by a room-dependent Δ_c dB (not a fixed 80 ms; they
note the literature range 50–150 ms). After t_c the ISM output is **replaced**, not augmented,
by decaying noise shaped to a predicted EDC. Crucially, the tail level is *calibrated to the
already-computed explicit early energy*: the ISM part is cut into K frames of length T, and

```
λ_k = T·ĥ_P(k) / ∫_{kT−T}^{kT} h²(ξ) dξ ,     λ̂ = mean over k
```

with "the first few frames … typically discarded" to avoid the bias caused by strong discrete
early reflections. **This is the directly transferable recipe for setting a tail level from an
incomplete explicit set.**
Sources: https://pubs.aip.org/asa/jasa/article/124/1/269/903076/Prediction-of-energy-decay-in-room-impulse (abstract) and full method text at https://www.researchgate.net/publication/224608383_Diffuse_Reverberation_Model_for_Efficient_Image-Source_Simulation_of_Room_Impulse_Responses — primary, high quality.

**Savioja & Xiang (Acoustics Today 2020) overview** confirms the general architecture: ISM for
direct + early, "the late part is gathered from precomputed responses or exploiting its random
nature by artificial approximation".
Source: https://acousticstoday.org/wp-content/uploads/2020/12/Simulation-Based-Auralization-of-Room-Acoustics-Lauri-Savioja-and-Ning-Xiang.pdf — review article, high quality.

### 2.2 Should the tail be the full diffuse 4/R from t = 0, or reduced?

Two separate corrections apply, and they pull in opposite directions.

**(i) The classical 4/R is itself wrong for a hall — it should decay with distance.**
Barron & Lee (JASA 84, 618, 1988) revised theory. In a diffuse field the spatial-average
reflected energy density is w = 4W/cA, i.e. p̄²/ρc = 4W/A. Revised theory keeps that *constant*
but integrates the decay from the direct-sound arrival t₀ = r/c, which multiplies it by
e^(−13.82·t₀/T) = e^(−0.04r/T). Relative to the direct sound at 10 m:

```
d   = 100/r²                                                        (direct)
e_r = (31200·T/V)·e^(−0.04r/T)·(1 − e^(−1.11/T))                     (early reflected, 0–80 ms)
l   = (31200·T/V)·e^(−0.04r/T)·e^(−1.11/T)                           (late, >80 ms)
C80 = 10 log[(d + e_r)/l]        G = 10 log(d + e_r + l)   [dB]
Total reflected level = 10 log(31200 T/V) − 0.174·r/T   [dB]
```

The term **0.174·r/T dB** is exactly the amount by which a position-independent 4/R tail
over-predicts reflected energy. For T = 1.5 s: **1.2 dB at r = 10 m, 2.3 dB at 20 m, 3.5 dB at
30 m, 4.6 dB at 40 m.** This is a first-order defect of the model under review and it is
seat-position-dependent, i.e. it directly distorts the seat ranking.
Related: Nijs & Rychtáriková's equivalent form y′(t₀) = 100/r² + (31200T/V)(1−ᾱ)^(r/mfp) makes
the link to the classical (1−ᾱ)·4W/A explicit — the reflected level equals the classical mean
exactly when r = mean free path, is higher nearer and lower farther.
Vorländer's alternative correction (mean SPL = SWL + 10 log(4/S) − 4.34·A/S, plus Waterhouse) is
a *position-independent* level reduction of similar average magnitude (≈ 1.5 dB at ᾱ = 0.3),
which Barron shows is the inferior choice for a hall because it lacks the distance dependence.
Source: https://www.akutek.info/Papers/MB_ConcertHall_SoundLevels.pdf §II — primary, high quality.

**(ii) Double-count with the explicit taps.** If explicit taps carry a fraction f of the
reflected energy and the tail carries the full reflected energy, total energy is over-counted by
10 log(1+f) dB — only **0.17–0.68 dB** for f = 4–17 %. That is a second-order problem. The much
larger problem is the reverse: with f only 4–17 %, the model's *explicit early set is far too
sparse*, as §2.4 shows.

### 2.3 Reverberation build-up: t² reflection density vs exponential ramp

The physically correct statement is that **reflection density** rises as t² (dN/dt = 4πc³t²/V),
**not** that **energy density** ramps. Statistical theory and Barron's assumptions (2) and (3)
both hold energy density constant-then-exponentially-decaying from the direct arrival; the t²
law describes how that same energy is *packaged* into discrete arrivals. Barron's Fig. 3
(measured integrated decays) shows real early decays are stepped, not smooth, but "when measured
early levels within 80 ms are compared with theory no consistent disagreement emerges", and the
whole-dataset rms error for early level is 1.29 dB.

Consequence for the model under review: **an energy ramp on the tail onset is not physical and
is quantitatively dangerous.** Any ramp that (a) delays diffuse energy and (b) renormalises the
total afterwards moves energy from the 0–80 ms window into the >80 ms window and drops C80
roughly one-for-one — which is precisely the ≈ 3 dB C80 collapse the project already observed
with a 25 ms ramp. A short (≤ 5 ms) ramp used purely to avoid a click in the rendered audio is
fine, provided the *metric* integrates the un-ramped envelope, or the ramp is energy-preserving
(shift, not delete).
Sources: reflection-density law — https://suonoevita.it/media/medialibrary/2020/04/2012_paper_AES_mixingTime.pdf Eq. 1 and https://d-nb.info/1252736983/34 Eq. 1; decay shape — https://www.akutek.info/Papers/MB_ConcertHall_SoundLevels.pdf §II, §IV.
Recent methods that *do* shape the emergence of the diffuse field use time-dependent envelopes
or scattering-based energy redistribution rather than a blanket ramp:
https://eprints.whiterose.ac.uk/id/eprint/237877/1/DAFx25_paper_17.pdf §2.3.

### 2.4 Accuracy of Barron–Lee revised theory, and its verdict on this model

Barron 2015, **212 measurements in 19 unoccupied concert spaces** (mean of 500/1000/2000 Hz):

| Measure | Mean error (meas − theory) | rms error | Regression r |
|---|---|---|---|
| Early level | 0.1 dB | **1.29 dB** | 0.88 |
| Late level | 0.3 dB | **1.19 dB** | 0.91 |
| Total (G) | 0.1 dB | **1.02 dB** | 0.92 |
| Early-to-late (C80) | 0.1 dB | **1.36 dB** | 0.62 |
| (diffuse scale model, reflected level) | 0.1 dB | 0.72 dB | 0.68 |

RT vs EDT in the formulas: no general advantage to EDT (C80 rms 1.36 → 1.13 dB, the only
measure that improves), but a clear advantage in halls with EDT/RT < 0.95 — in half of those
halls C80 was better predicted with EDT. In Christchurch Town Hall (EDT/RT = 0.82) using the
hall-mean EDT cut the C80 error from 2.61 to 1.51 dB rms.
Source: https://www.akutek.info/Papers/MB_ConcertHall_SoundLevels.pdf Tables II, IV, VII–X — primary, high quality.

**Applied to this hall as an anchor** (V = 20,000 m³):

| r (m) | T = 1.4 s: C80 / G | T = 1.6 s: C80 / G |
|---|---|---|
| 10 | +4.1 / +4.2 dB | +3.1 / +4.7 dB |
| 20 | +2.2 / +1.7 dB | +1.2 / +2.5 dB |
| 30 | +1.7 / +0.2 dB | +0.8 / +1.1 dB |
| 40 | +1.5 / −1.2 dB | +0.6 / −0.1 dB |

Revised theory says the early (0–80 ms) share of the reflected energy in this hall is
**1 − e^(−1.11/T) = 50–55 %**. A complete order-1–2 image-source set should carry roughly
1 − (1−ᾱ)² = **36 % (ᾱ = 0.2) to 51 % (ᾱ = 0.3)** of the reflected energy — i.e. very nearly all
of the early reflected energy, since 2 orders ≈ 58 ms ≈ the 80 ms window. The model's explicit
paths carry **4–17 %**, a factor 3–10 short. That is a geometry/completeness problem, not a
tail-tuning problem, and it explains why the house-median C80 (−0.9 dB) sits ~2–3 dB below the
revised-theory expectation (+0.6 to +2.2 dB in the stalls) for this volume and RT.

**Barron's revised theory has been validated in opera houses specifically.** Eleven Italian
historical opera houses, >50,000 IRs: measured G matches Eq. (1) when **V = V_cavea** (main hall
only, excluding fly tower, boxes and gallery) and the source is on the fore-stage; the theory
"seems no more applicable" when the source is at centre stage behind the proscenium.
Source: http://www.ica2016.org.ar/ica2016proceedings/ica2016/ICA2016-0729.pdf — peer-reviewed ICA conference paper, good quality. **Directly relevant: a singer downstage and a singer upstage should not share one volume constant.**

---

## Q3. Prediction accuracy of GA models for C80, G, EDT

### 3.1 JND baseline (ISO 3382-1 / Bork)

C80 **1 dB**, C50 1 dB, G 1 dB, EDT 5 %, T30 5 %, T_s 10 ms.
Source: https://www.odeon.dk/pdf/ISRA2013_Paper_The%20ISO%203382%20parameters_Can%20we%20simulate%20them_Can%20we%20measure%20them_24July2013.pdf Table 1 — good quality.

### 3.2 The four round robins

| RR | Room | Year / pub | Outcome |
|---|---|---|---|
| RR1 (Vorländer 1995) | PTB lecture hall, V = 1,800 m³, 274 seats, 16 submissions (2 ISM, 7 ray, 7 hybrid), 1 kHz only | 1993–94 / 1995 | Discrepancies so large that "a safe prediction … seemed to be impossible"; only 3 programs judged reliable. **A named cause of deviation was neglect of attenuation at grazing incidence over seat rows (seat dip).** |
| RR2 (Bork 2000) | ELMIA hall, V = 11,000 m³, 1,100 seats, 16→13 submissions, 6 octaves | 1996–98 / 2000 | Phase II RT and EDT still deviated ≈ **2 JND** on average; **systematic over-estimation of clarity and definition at 125 Hz.** |
| RR3 (Bork 2005) | PTB recording studio, V = 400 m³, 21 submissions, 6 programs in phases II–III | 1999–2002 / 2005 | "good agreement with measured values" for position-variable parameters such as **clarity**; RT deviations still consistently **> 2 JND even at 1 kHz**, attributed to missing diffraction modelling and inability to handle complex wall impedances. |
| RR4 (Brinkmann, Aspöck, Ackermann, Lepa, Vorländer, Weinzierl, JASA 145(4) 2746, 2019) | 9 scenes incl. concert hall & 8,657 m³ auditorium; 6 participants, uninformed | 2016–17 / 2019 | Acceptable results in the mid-frequency range for complex scenes; **C80 deviations are position-dependent and inconsistent** — at one source-receiver pair almost all simulations fell outside the 1 dB JND, at another they matched. Largest errors at 125 Hz throughout. Only one participant modelled finite reflector size; **no software reproduced a reflector's contribution at receivers with no specular path.** |

Sources: https://publications.rwth-aachen.de/record/808553/files/808553.pdf (Aspöck thesis §1.2, §4 — the best single consolidated account, high quality); https://www.ptb.de/cms/ptb/fachabteilungen/abt1/fb-16/ag-163/round-robin-in-room-acoustics.html (PTB's own summary + raw result spreadsheets for RR2 and RR3, primary data).

**Katz round robin on *analysis*, not simulation**: substantial variation between implementations
computing parameters from the *same* measured IRs — worst at 125 Hz but "with variations close
to the subjective difference limen in the 1 kHz frequency band". Cabrera et al. later found the
spread had narrowed. Cited in the same thesis §1.2.

### 3.3 What C80 error is typical, and how sensitive C80 is to boundary handling

- **Barron–Lee revised theory: 1.36 dB rms for C80** across 212 hall measurements (1.4 JND) —
  and this is a two-parameter analytic model with no geometry at all. Any geometric model that
  does not beat ~1.4 dB rms is not earning its complexity.
- **A calibrated GA model in a real auditorium**: agreement "within 0.5 JND for most parameters"
  at 1 kHz; deviations > 1 JND only at 125 and 250 Hz. In a coupled/complex space (Hagia Sophia)
  C80 error ranged **0.47–4.66 JND, mean 2.27 JND**, and the authors conclude C80 "is probably
  not a good [parameter] … in coupled spaces". An opera house with boxes and a fly tower is a
  coupled space.
  Source: https://www.odeon.dk/pdf/ISRA2013_Paper_The%20ISO%203382%20parameters… (as above).
- **Sensitivity to boundary handling is the dominant term.** Same ODEON paper: careless onset
  detection produced measured C80 values "off by more than 12 dB"; "for prediction of C80 it is
  important that the onset time is well defined." Simulations have an advantage here because
  the onset is defined by geometry.
- Barron's own boundary experiment (Table VII, §1.3 above) shifts C80 bias by **1.2 dB** simply
  by moving the integration start from the direct sound to the first reflection — i.e. a JND-plus
  systematic error from a single modelling choice, with no change to the geometry.
- RWTH thesis: even after calibrating absorption to match measured T30, C80 deviations of
  **> 3 dB remained at 125 and 250 Hz**; "calibration of one room acoustic parameter does not
  automatically lead to low deviations of other parameters".

**Bottom line: 1–2 dB rms is the realistic target for C80 in the mid bands; 3–5 dB is normal at
125–250 Hz and in coupled volumes; and the early/late boundary treatment alone can move C80 by
more than 1 dB, i.e. more than a JND.**

---

## Q4. The concave dome: focusing, faceting, and whether 36 facets suffice

Geometry as stated: R = 16 m, chord 16 m, rise ≈ 2 m, 22 m above the floor.
Self-consistency check: R(1 − cos θ_m) with θ_m = asin(8/16) = **30°** gives rise = **2.14 m** —
the stated numbers describe a genuine spherical cap of half-angle 30°, cap area **215 m²**.

### 4.1 Does it focus? Yes, over essentially the whole audio band.

Vercammen's criterion (wave-theoretical, Acta Acustica, "Sound Reflections from Concave
Spherical Surfaces, Part II"): focusing occurs when the reflector depth v_m = R(1 − cos θ_m)
exceeds a wavelength; **for v_m < λ/4 there is no focusing, only diffraction**.

```
v_m = 2.14 m  →  focusing for f > c/v_m ≈ 160 Hz ; no focusing only below ≈ 40 Hz
```

So this dome focuses at every frequency that matters. Vercammen also warns that "the possible
reduction of the focussing effect by absorbers or diffusers is not enough to eliminate" it.
Focal-region size (−3 dB half-width) x_A ≈ ± λ/(4 sin θ_m) = ± λ (here sin θ_m = 0.5), so the
focal spot is roughly one wavelength across — 0.34 m at 1 kHz, 1.4 m at 250 Hz. Because the
low-frequency spot is much bigger, "focussing problems are mostly perceived as rather low or
middle frequency problems."
Source: https://dael.euracoustics.org/bin/EAA/aaua_dl?document_id=64913 — primary journal paper; **OCR is partly garbled (ligature substitution) but the equations and criteria are legible. Quality: high content, medium transcription.**
Companion: https://research.tue.nl/en/publications/sound-concentration-caused-by-curved-surfaces/

### 4.2 Where the focus is, and how strong the reflection is

Mirror equation 1/a₁ + 1/a₂ = 2/R. With the source ≈ 20.5 m below the dome:
**a₂ = 13.1 m below the dome = 8.9 m above the floor** — a mid-air focus roughly 7.7 m above ear
height. Listeners are ≈ 8 m *past* the focus, well outside the wavelength-scale focal spot, so
**geometrical acoustics is valid at the seats** — but the beam is still strongly converged
relative to a flat ceiling.

Rindel's curvature term (the term ODEON, CATT and Arup's Strutt all implement):

```
a* = 2·a₁·a₂/(a₁+a₂)                                    (characteristic distance)
ΔL_curv = −10 log|1 + a*/(R cos θ)|   dB                (R negative for concave)
double-curved surface: apply once per principal direction (i.e. −20 log|…| for a sphere)
```

With a₁ ≈ 20.5 m, a₂ ≈ 20.8 m → a* = 20.6 m, cos θ ≈ 1, R = −16 m:
**ΔL_curv = +5.4 dB (single curvature) → +10.7 dB for a true sphere.**
So a real dome of this curvature delivers a **5–11 dB louder** ceiling reflection than a flat
ceiling in the same place, concentrated into a limited footprint, and *removes* the ceiling
reflection from the rest of the house. The current model, which drops the flat-ceiling
reflection for 144 of 264 Grand Tier seats and returns it to only some via facets with no
curvature gain, is wrong in both directions.
Source: https://strutt.arup.com/help/Auditorium_Acoustics/Rindel_Reflector_Theory.pdf (Arup's transcription of Rindel 1985/1986 with worked examples) and https://strutt.arup.com/help/Auditorium_Acoustics/Reflector.htm (the implemented equations, citing the ODEON technical manual p. 6-76) — secondary but authoritative and unambiguous; high quality.
Extension to arbitrary shapes and reflection orders (differential ray tracing, ΔL_curv = 10 log(dx_flat/dx_curv)): https://kahle.be/articles/b_ISRA2013_TW_differential_raytracing_P100.pdf — Kahle Acoustics ISRA 2013, good quality.

### 4.3 Are 36 flat facets adequate? **No — and the failure mode is at low frequency.**

Two independent tests.

**(a) Angular subdivision.** ODEON's own modelling guidance: "Curved surfaces should be
subdivided into smaller planar surfaces. Subdivisions about every **10° to 30°** are
recommended." The dome spans 60° of arc in each direction. A 6 × 6 grid of 36 facets gives
10° per facet — **just inside** the recommendation, so the *geometry* is marginally acceptable.
Source: https://odeon.dk/learn/making-models/ — vendor documentation, medium-high quality.

**(b) Facet size vs the Fresnel zone — this is where 36 facets fail.** Rindel's diffraction
cut-off for a finite reflector:

```
f_limit = 0.5·c·a* / (S cos θ)      [Hz]   (S = facet area)
below f_limit the reflection rolls off at 6 dB/octave (3 dB/oct between the two edge cut-offs)
```

| Treatment | facet side | S | f_limit |
|---|---|---|---|
| whole dome as one surface | 16 m | 256 m² | **14 Hz** |
| 36 facets | 2.67 m | 7.1 m² | **498 Hz** |
| 144 facets | 1.33 m | 1.8 m² | **1992 Hz** |

An intact 16 m dome reflects efficiently across the whole band. Split into 36 facets, **each
facet is too small to reflect efficiently below ≈ 500 Hz** — 12 dB down at 125 Hz if the size
correction is applied, and physically wrong (too loud, with a false arrival structure) if it is
not. Finer faceting makes this *worse*, not better. This is the classic trap: faceting a curved
surface for an image-source model trades one error for another, and the round-robin evidence
(RR4) is that only one of six commercial packages even applies the finite-reflector correction.

**Recommended treatment for this model** (in order of increasing fidelity):
1. Treat the dome as **one surface**: find the specular point on the true sphere (Newton
   iteration on the sphere), build one image source from the local tangent plane at that point,
   and apply `ΔL_curv = −20 log|1 + a*/(R cos θ)|` (spherical → both principal directions) plus
   Rindel's diffraction term with S = 215 m². This gives the correct level, the correct arrival
   time, and the correct limited footprint, with no low-frequency artefact.
2. Or, treat the dome as a **diffusing flat patch** at the chord plane (specular energy scaled
   by (1 − s), the rest fed to the tail) — defensible while the ceiling is unmeasured, and it is
   what the project's own HANDOFF already suggests. It will *understate* the seats inside the
   convergence zone by 5–10 dB.
3. Faceting is only correct if every facet is large enough that f_limit is below the band of
   interest, which for a* ≈ 21 m means facets of ≥ 30 m² (≈ 5.5 m across, i.e. **at most ~9
   facets** for this dome) — and 9 facets over 60° violates the 10–30° rule from the other side.
   **The two constraints are incompatible for this geometry: do not facet it.**

**Real-world precedent:** the Royal Albert Hall's elliptical plan and large concave dome created
"a massive echo delayed about 170 ms", suppressed only by a combination of absorptive treatment
and 134 suspended reflecting saucers.
Source: https://www.akutek.info/Papers/MB_Objective_Assessment_2013.pdf §6 — primary, high quality.

---

## Q5. Seat dip, balcony-edge diffraction, and under-balcony coupling

### 5.1 Seat-dip magnitude — much larger and much broader-band than usually modelled

The canonical picture (Schultz & Watters 1964; Sessler & West 1964) is a narrow dip at
**80–300 Hz** with nothing above 800 Hz. Recent work shows that is wrong:

- Meyer et al., and v. Békésy (1933) before them: unupholstered seats at grazing incidence
  cause **broadband attenuation of ≈ 0.7–1.5 dB per metre in excess of spherical spreading**.
- 1:20 scale-model measurements (Rummler/Kahle, Forum Acusticum Euronoise 2025): the distinct
  ~100 Hz dip is present, but so is **8–10 dB of broadband attenuation** by row 12 at 5° source
  elevation, with a row-to-row offset of **≈ 0.7 dB/m**.
- Elevation-dependence (Audience Related Transfer Functions): attenuation at 1 kHz reaches
  **up to 16 dB between 400 Hz and 3 kHz at 0° source elevation**, decreasing monotonically with
  source elevation and reaching **≈ 0 dB above 15° elevation**.
- Mommertz (1993) and Bradley confirm the effect up to 10 kHz (the "head dip", 2–10 kHz).
Source: https://kahle.be/articles/2025-ForumAcusticumEuronoise2025-ForgetAboutTheSeatDipEffect.pdf — recent conference paper with new scale-model data, good quality. Open-access mirror: https://dael.euracoustics.org/confs/fa2025/data/articles/000409.pdf

Dip frequency ≈ where seat height is λ/4 (RWTH BRAS RS7: 0.24 m beams → theoretical 357 Hz,
measured 350–400 Hz; dip frequency rises with incidence angle).
Source: https://publications.rwth-aachen.de/record/808553/files/808553.pdf §3 (BRAS scene RS7).

**Modelling status:** seat dip is a multiple-diffraction wave phenomenon that GA cannot produce,
because GA applies absorption coefficients as if valid at all incidence angles. Wave solvers
(FDTD/BEM/Treble) reproduce it; GA models must inject it as an empirical filter.
Source: https://docs.treble.tech/validation/fundamental-effects/RS7 — vendor validation page against the BRAS RS7 benchmark; medium quality but the physical statement is standard.
It is worth stressing that **neglect of grazing-incidence attenuation over seat rows was named
as a cause of deviation in Round Robin 1** (§3.2).

**Practical recipe for this model:** apply, to the *direct sound and to any grazing early
reflection*, an elevation-dependent attenuation A(f, φ, n_rows) with
(i) a notch of 8–12 dB centred where the seat back height = λ/4 (typically 100–160 Hz for real
seating), and (ii) a broadband term ≈ 0.7 dB per metre of audience traversed, both scaled by a
factor that goes from 1 at 0° source elevation to 0 at ≥ 15° elevation. For an opera house this
matters most for the stalls (singer at ≈ 1.5 m, ear at 1.2 m → near-0° elevation for the rear
stalls) and hardly at all for boxes and the upper tiers.

### 5.2 Edge diffraction at balcony/tier fronts and soffits

- **Svensson's secondary-source (Biot–Tolstoy–Medwin) formulation** is the reference solution;
  Keller's GTD, Pierce's 2–3 term and Kouyoumjian–Pathak's 4-term UTD are the asymptotic
  approximations used in real-time GA.
- Magnitudes from a controlled double-edge study: energy transmitted into the **single shadow
  zone ≈ −7 dB**, into the **double shadow zone −16 to −10 dB**, relative to the free field.
  Modern filter approximations (UDFA) reach **< 0.87 dB average relative error in the double
  shadow zone and 0.70–1.22 dB in the single shadow zone** re. 2nd-order BTMS, "perceptually
  small"; the cruder sequential/single-edge approach errs by **up to 5 dB** for narrow edges.
Source: https://acta-acustica.edpsciences.org/articles/aacus/full_html/2024/01/aacus240016/aacus240016.html — peer-reviewed Acta Acustica, high quality.
- The RR4 finding is directly relevant: only one of six packages accounted for **finite
  reflector size**, and none produced a correct reflection where no specular path existed.
Source: https://publications.rwth-aachen.de/record/808553/files/808553.pdf §4.

**Implication for the model's "fixed attenuation" diffraction:** a fixed broadband number is
defensible only as a placeholder. A 6 dB/octave high-pass whose corner is set by Rindel's
f_limit for the occluding soffit, plus a −7 dB (single shadow) / −13 dB (double shadow)
floor, is cheap and reproduces the published magnitudes to ~1–2 dB.

### 5.3 Under-balcony behaviour (Barron 1995, JASA 98, 2580)

Seven halls analysed. Findings, all consistent across sources:

- **The dominant effect is a reduction of late sound, not early sound.** Early-sound behaviour
  under overhangs is "haphazard"; late sound is consistently reduced.
- Consequences: **EDT down, C80 up, G slightly down**; the perceived change is reduced
  reverberance and reduced envelopment.
- The controlling geometric parameter is the **vertical angle of view θ** (Fig. 1 of the 2015
  paper); Barron's criterion is **θ ≥ 40°** for acceptable overhangs.
- Local reflections from the back wall and soffit inside the overhung volume partly restore the
  level — which is why measured late levels sometimes turn *up* again at the very back of an
  overhang.
- Barron explicitly recommends that hall-mean EDT and C80 be computed **omitting overhung
  seats**, and that they be displayed separately, because their statistics are different.
- Extreme case (Colston Hall, Bristol, boxes stepping down the side walls): the late sound
  splits into **two distinct populations** — stalls on a steep line, balcony on the
  revised-theory line — "in late energy terms we have a subdivided acoustic space", with several
  positions above C80 = +2 dB despite a 2.4 s occupied RT.
Sources: https://www.akutek.info/Papers/MB_Objective_Assessment_2013.pdf §5.2, §6 and https://www.jstage.jst.go.jp/article/ast/26/2/26_2_162/_pdf §6.8 — both primary Barron, high quality. Abstract of the 1995 paper: https://pubs.aip.org/asa/jasa/article-abstract/98/5/2580/797951/ (WebSearch fallback; paywalled).

**Coupling.** An opera house with boxes, a gallery and a fly tower is a multiply-coupled volume.
The ICA 2016 opera-house study resolves the question of which volume to put in Barron's
equation: **V = V_cavea (main hall only)**, excluding fly tower, boxes and gallery, matches
measured G for a fore-stage source; the coupled-volume decays are "cliff-type" with EDT < T30,
and EDT (not T30) is the parameter that discriminates stalls / boxes / gallery.
Source: http://www.ica2016.org.ar/ica2016proceedings/ica2016/ICA2016-0729.pdf — good quality.
The RWTH BRAS database includes an explicitly coupled scene (Konzerthaus Berlin chamber hall
with a ~1000 m³ coupled volume) precisely because "if and how a simulation software should
account for this coupled volume" is unsettled; a Weber & Katz round robin found GA and
wave-based tools *can* reproduce coupled-room effects.
Source: https://publications.rwth-aachen.de/record/808553/files/808553.pdf §1.2, §3.

---

## Q6. Occupied vs unoccupied conversion

**Hidaka, Nishihara & Beranek (JASA 109(3) 2001, "Relation of acoustical parameters with and
without audiences in concert halls and a simple method for simulating the occupied state").**
RT, EDT, C80, G and IACC measured with identical procedures with and without audience in six
concert and opera halls; unoccupied RT in 15 further halls. Results:
1. Occupied RT predicted from unoccupied RT by a regression of the form **y = a − b·exp(x)**,
   accurate at low and mid frequencies.
2. **Occupied C80 predicted accurately from unoccupied C80** by a newly proposed equation.
3. Occupied and unoccupied **G** are related by a first-degree linear regression.
4. **IACC is essentially unchanged** by occupancy.
5. A cloth seat covering can be used to simulate occupancy in measurements.
Source: https://pubmed.ncbi.nlm.nih.gov/11303917/ (abstract; full text paywalled) — primary, high quality; the numeric coefficients are in the paper, not the abstract.

**Barron's quantification of the same data (17 halls, Vienna Musikverein excluded for its hard
seating):**

| Quantity | Unoccupied | Occupied | Change |
|---|---|---|---|
| RT_mid (mean of 17 halls) | 2.32 s | 1.85 s | ratio **0.80** ≈ **4 JND** |
| EDT | — | — | ≈ 4 JND (EDT/RT ratio is independent of RT) |
| C80 | — | — | **max +1.5 dB** occupied (at r = 10 m) ≈ 1.5 JND |
| G | — | — | **max −1.6 dB** occupied ≈ 1.5 JND |
| L_F, IACC | — | — | little affected — do not correct |

Direction: occupied halls have **shorter RT and EDT, higher C80, lower G**. Barron computes the
C80/G shifts from revised theory for that RT change, so they are internally consistent with the
Barron–Lee formulas in §2.2 — meaning a model that already uses Barron's equations gets the
occupancy conversion for free by substituting the occupied RT.
Source: https://www.jstage.jst.go.jp/article/ast/26/2/26_2_162/_pdf §3.2, §6.1 — primary Barron, high quality.
Barron notes three equivalent correction techniques (Hidaka et al., Bradley, Barron 2010 p. 419)
and that accuracy degrades for large RT changes.

Two further stage/occupancy effects worth carrying:
- Adding **50 moderately upholstered chairs on stage** reduced audience G by **1.0 dB** at mid
  frequencies in a 2,210-seat hall — "'Musicians' should therefore be included in models".
- Absorbing material in the stage area affects early *and* late sound roughly uniformly, beyond
  its effect on RT, because it subtends a large solid angle at the source.
Both from https://www.akutek.info/Papers/MB_Objective_Assessment_2013.pdf.

**Opera-house reference values for sanity checking:** Teatro dell'Opera di Roma (ISO 3382-1),
**C80 between −2 and +2 dB across the whole band**, EDT ≈ 1.5 s, T_mid ≈ 1.6 s.
Source: https://cris.unibo.it/retrieve/90411652-a478-4063-b043-6cd6326c5233/full_paper_638_20240512192954818.pdf — conference paper, medium-good quality.

---

## Recommended changes to the described model, ranked by expected effect on C80 / G accuracy

Ranked by the magnitude of the systematic error each one removes, largest first. Effects are
octave-band, mid-frequency, for V = 20,000 m³ and T ≈ 1.5 s.

**1. Make the diffuse tail's total energy decay with source–receiver distance (Barron–Lee).
Effect: 0 → 4.6 dB on late level, hence up to ±4.6 dB on C80 and 1–3 dB on G, monotonic with
distance — i.e. it changes the seat *ranking*, not just the absolute numbers.**
Replace the position-independent 4/R with

```
E_refl(r) = (31200·T/V)·e^(−0.04·r/T)      [relative to direct sound at 10 m]
```

equivalently multiply the current 4/R tail energy by `exp(−0.04·r/T)`. The correction is
`0.174·r/T` dB: 1.2 dB at 10 m, 2.3 dB at 20 m, 3.5 dB at 30 m, 4.6 dB at 40 m. Barron's rms
errors against 212 hall measurements are 1.19 dB (late), 1.02 dB (total), 1.36 dB (C80). This is
one line of code and it is the highest-value change in the list.
Validated for opera houses with **V = V_cavea**, source on the fore-stage. For a source at
centre stage (upstage singer, or the pit under the proscenium) the theory breaks down — use a
separate, larger effective volume or an explicit coupling term rather than the same constant.

**2. Start the diffuse tail at the direct-sound arrival, not at a mixing time, and remove the
onset ramp from the metric. Effect: 2–4 dB on C80.**
Barron's 170-measurement test: direct-sound start beats first-reflection start on early level
(rms 1.30 vs 1.61 dB) and on C80 bias (0.1 vs 1.3 dB). With the explicit taps carrying only
4–17 % of the reflected energy, a tail that begins at 60–120 ms leaves the 0–80 ms window almost
empty of reflected energy, which is exactly the observed C80 collapse. Keep a ≤ 5 ms
click-suppression ramp in the *renderer* only, and integrate the un-ramped envelope in the
*metric* (or make the ramp energy-preserving). The mixing time remains the right crossover for
the auralisation's *fine structure* (deterministic taps → noise), just not for the *energy*.
For this hall the defensible mixing time is 60–140 ms (central 100–120 ms; Lindau
`t_mp50 = 20·V/S + 12 = 62 ms`, Hidaka `80·RT = 112–128 ms`, Polack `√V = 141 ms`).

**3. Fix the double count properly once (2) is in place, by *subtracting* the explicit early
energy from the diffuse envelope rather than adding on top. Effect: 0.2–0.7 dB now, but grows to
1.5–2.5 dB once the explicit set is enriched (item 4).**
Two acceptable schemes:
- *Subtractive (recommended here, Barron-consistent):* the diffuse envelope represents **all**
  reflected energy. In each time frame, subtract the energy already placed by explicit taps from
  the envelope before generating noise, flooring at zero. Calibrate as Lehmann & Johansson do —
  frame-wise λ_k = T·ĥ_P(k)/∫h², averaged, discarding the first few frames.
- *Order-partitioned (ODEON/Wayverb):* explicit taps carry orders ≤ 2; the tail carries only
  orders > 2, i.e. energy scaled by (1−ᾱ)² and onset at ≈ 3·mfp/c ≈ 88 ms. **Only valid if the
  explicit order-1–2 set is complete** — it is not (item 4) — so do not adopt this yet.
Additionally, multiply explicit image-source reflectances by **(1 − s)** per bounce so scattered
energy is handed to the tail rather than counted twice (Wayverb's rule).

**4. Enrich the explicit early set until it carries ~35–50 % of the reflected energy, not 4–17 %.
Effect: 2–3 dB on C80, and it is the difference between a geometric model and a dressed-up
statistical one.**
Revised theory says 50–55 % of the reflected energy arrives inside 80 ms in this hall, and a
*complete* order-1–2 set should carry 36 % (ᾱ = 0.2) to 51 % (ᾱ = 0.3). At 4–17 % the coarse
surface set is missing a factor 3–10. Candidates for the missing paths: proscenium splays and
reveals, box fronts and box side walls (each box front is a metre-scale reflector at
5–15 m — check Rindel's f_limit before including), tier soffits at grazing angles, the side-wall
segments between box tiers, the orchestra-pit rail, and stage-house returns for an upstage
source. Sanity target: house-median C80 should land near **+0.6 to +2.2 dB** (Barron for this V
and T), not −0.9 dB.

**5. Treat the dome as one curved surface with Rindel's curvature term; delete the 36 facets.
Effect: 5–11 dB for seats in the convergence footprint; removes a spurious −12 dB
low-frequency hole for every dome-served seat.**
- The dome focuses at every frequency above ≈ 160 Hz (v_m = 2.14 m > λ).
- The geometric focus is 13.1 m below the dome = **8.9 m above the floor** — in mid-air, above
  the audience — so seats are ~8 m past the focus and geometrical acoustics is valid there.
- `ΔL_curv = −20 log|1 + a*/(R cos θ)| = +10.7 dB` for a spherical cap with a* = 20.6 m,
  R = −16 m (+5.4 dB if you treat it as singly curved).
- 36 facets of 7.1 m² have a Rindel diffraction cut-off of **498 Hz**; 144 facets, 1992 Hz; the
  intact 16 m dome, 14 Hz. Faceting *creates* the low-frequency error. The facet size needed to
  avoid it (≥ 30 m², ~9 facets) contradicts ODEON's 10–30° subdivision guidance, so the two
  constraints cannot both be met — **do not facet this dome.**
- Interim fallback (defensible while the ceiling is unmeasured): a single flat diffusing patch at
  the chord plane with specular energy scaled by (1 − s). It understates the convergence-zone
  seats by 5–10 dB — say so in the output.
- Precedent for the risk: the Royal Albert Hall dome produced a 170 ms echo requiring 134
  suspended saucers plus absorption to suppress.

**6. Add an elevation-dependent seat-dip filter to the direct sound and to grazing early
reflections. Effect: up to 16 dB at 400 Hz–3 kHz for 0° elevation rear-stalls seats; ~0 dB above
15° elevation, so it mostly re-orders stalls vs tiers.**
Combine (i) a λ/4 notch of 8–12 dB near 100–160 Hz, (ii) a broadband excess attenuation of
≈ 0.7 dB per metre of audience traversed, both scaled from 1 at 0° source elevation to 0 at
≥ 15°. This was a named cause of failure in Round Robin 1 and is the reason GA models
systematically over-predict direct and early energy in the rear stalls. Note the effect applies
**with and without audience** (grazing reflection coefficient → −1 regardless of upholstery).

**7. Give under-balcony and under-box seats a *late*-energy penalty rather than an early one, and
report them separately. Effect: 1–3 dB on the late term at deeply overhung seats, hence EDT down
and C80 up — the correct sign, which a uniform occlusion attenuation gets wrong.**
Barron: overhangs reduce **late** sound consistently while early sound behaves haphazardly.
Drive the penalty off the **vertical angle of view θ** (criterion θ ≥ 40°), not off a slab
occlusion test. Add back a local soffit + rear-wall reflection inside the overhung volume, which
is what keeps level up at the very back. Follow Barron and exclude overhung seats from
house-mean statistics, or at least flag them.

**8. Replace fixed-attenuation diffraction with a Rindel/UTD-style filter at tier fronts and
soffit edges. Effect: 1–5 dB in shadow zones, band-dependent.**
Target magnitudes: **−7 dB** single shadow zone, **−16 to −10 dB** double shadow zone; a 6 dB/oct
roll-off below `f_limit = 0.5·c·a*/(S cos θ)` for each finite occluder. Filter approximations of
this class reach ~1 dB of the BTMS reference; the naive sequential approach errs by up to 5 dB
for narrow edges. Also apply the **finite-reflector size correction to every explicit reflector**
(RR4 showed almost no commercial package does this, and it is the main reason small-panel
reflections are over-predicted).

**9. Use EDT rather than RT in the revised-theory exponent where EDT/RT < 0.95. Effect: C80 rms
1.36 → 1.13 dB in general; 2.61 → 1.51 dB in the one hall where the ratio is 0.82.**
Opera houses have "cliff-type" decays with EDT clearly below T30, so this hall is likely a
candidate. Barron's method (3) — RT in the first term (total absorption), EDT in the exponential
— was best for C80 and late level.

**10. Publish occupied numbers, converted from the unoccupied assumption. Effect: C80 +1 to
+1.5 dB, G −1.5 to −1.6 dB, RT ×0.80, EDT ×~0.80; IACC and L_F unchanged.**
Because items 1 and 9 put the model on Barron's equations, occupancy conversion reduces to
substituting the occupied RT — the C80 and G shifts then fall out consistently. Do **not**
correct spatial measures. Add stage occupancy: ~1.0 dB of G for chairs and musicians on stage.
Reference band for a validated opera house: C80 −2 to +2 dB, EDT ≈ 1.5 s.

**11. Report a per-seat uncertainty, not a point value.** The best analytic model in the
literature has 1.0–1.4 dB rms against real halls; calibrated GA reaches 0.5 JND at 1 kHz but
2.3 JND for C80 in coupled spaces, and > 3 dB at 125–250 Hz even after T30-matched calibration.
An opera house *is* a coupled space. A ±1.5 dB mid-band / ±3 dB low-band band on C80 and ±1.5 dB
on G is honest; anything tighter is not supportable without measured IRs. C80's JND is 1 dB, so
seat ranking differences below ~1.5 dB are noise.

### Two things worth *not* doing

- **Do not add a long energy build-up ramp to the tail.** The t² law is about reflection
  *density*, not energy density; both statistical theory and Barron's measured early levels
  support constant-then-decaying energy from t₀. A ramp with post-hoc renormalisation moves
  energy across the 80 ms boundary and is the mechanism behind the observed 3 dB C80 collapse.
- **Do not refine the dome facet mesh.** Finer facets raise Rindel's diffraction cut-off
  (498 Hz at 36 facets → 1992 Hz at 144) and make the low-frequency error worse. The fix is
  fewer surfaces plus an explicit curvature term, not more surfaces.

---

## Source list (with quality notes)

**Primary journal / thesis, high quality**
- Barron, *Theory and measurement of early, late and total sound levels in concert spaces*, JASA 137(6), 2015 — https://www.akutek.info/Papers/MB_ConcertHall_SoundLevels.pdf (revised-theory derivation, Tables II/IV/VII–X: rms errors, start-time test, RT-vs-EDT test)
- Barron, *Objective assessment of concert hall acoustics*, 2013 — https://www.akutek.info/Papers/MB_Objective_Assessment_2013.pdf (Temporal Energy Analysis; balcony overhangs; Royal Albert Hall dome; stage-chair 1.0 dB)
- Barron, *Using the standard on objective measures … ISO 3382*, Acoust. Sci. Technol. 26(2), 2005 — https://www.jstage.jst.go.jp/article/ast/26/2/26_2_162/_pdf (occupancy corrections: RT 2.32→1.85 s, C80 1.5 dB, G 1.6 dB; §6.8 overhangs)
- Lindau, Kosanke & Weinzierl, *Perceptual evaluation of model- and signal-based predictors of the mixing time in BRIRs*, JAES 60(11), 2012 — https://d-nb.info/1252736983/34 (all mixing-time formulas; retrieved via WebFetch + pdftotext after Firecrawl credits ran out)
- Aspöck, *Validation of room acoustic simulation models*, RWTH thesis — https://publications.rwth-aachen.de/record/808553/files/808553.pdf (consolidated round-robin history RR1–RR4; BRAS database; seat-dip scene RS7; C80 calibration limits)
- Lehmann & Johansson, *Prediction of energy decay in room impulse responses…*, JASA 124(1), 2008 — https://pubs.aip.org/asa/jasa/article/124/1/269/903076/ ; method text at https://www.researchgate.net/publication/224608383_Diffuse_Reverberation_Model_for_Efficient_Image-Source_Simulation_of_Room_Impulse_Responses
- Hidaka, Yamada & Nakagawa, *A new definition of boundary point between early reflections and late reverberation*, JASA 122(1) 326, 2007 — https://pubs.aip.org/asa/jasa/article/122/1/326/812777/ (abstract only; the 80·RT regression is quoted in Lindau et al.)
- Hidaka, Nishihara & Beranek, *Relation of acoustical parameters with and without audiences…*, JASA 109(3), 2001 — https://pubmed.ncbi.nlm.nih.gov/11303917/ (abstract only)
- Vercammen, *Sound reflections from concave spherical surfaces, Part II: geometrical acoustics* — https://dael.euracoustics.org/bin/EAA/aaua_dl?document_id=64913 (focusing criteria; OCR partly garbled but equations legible)
- Kirsch & Ewert, higher-order edge-diffraction filters, Acta Acustica 8, 2024 — https://acta-acustica.edpsciences.org/articles/aacus/full_html/2024/01/aacus240016/aacus240016.html
- Barron, *Balcony overhangs in concert auditoria*, JASA 98(5) 2580, 1995 — https://pubs.aip.org/asa/jasa/article-abstract/98/5/2580/797951/ (paywalled; content via Barron's later reviews + WebSearch)

**Conference / vendor / documentation, medium-high quality**
- Naylor, ODEON hybrid method, ASA 1992 — https://odeon.dk/pdf/ASA_1992_Naylor.pdf
- Rindel, *Computer simulation techniques for acoustical design of rooms*, 1995 — https://www.odeon.dk/pdf/AustralAc_1995_Rindel.pdf (transition order 2–3; 500–1000 rays)
- Christensen et al., *The ISO 3382 parameters: can we simulate them? can we measure them?*, ISRA 2013 — https://www.odeon.dk/pdf/ISRA2013_Paper_The%20ISO%203382%20parameters_Can%20we%20simulate%20them_Can%20we%20measure%20them_24July2013.pdf (JNDs; onset sensitivity; Hagia Sophia C80 2.27 JND)
- Rindel reflector theory as implemented in Arup Strutt — https://strutt.arup.com/help/Auditorium_Acoustics/Rindel_Reflector_Theory.pdf and https://strutt.arup.com/help/Auditorium_Acoustics/Reflector.htm (ΔL_curv, ΔL_diffr, f_limit, worked examples)
- Kahle Acoustics, differential ray tracing on curved geometries, ISRA 2013 — https://kahle.be/articles/b_ISRA2013_TW_differential_raytracing_P100.pdf
- Rummler et al., *Forget about the seat dip effect*, Forum Acusticum Euronoise 2025 — https://kahle.be/articles/2025-ForumAcusticumEuronoise2025-ForgetAboutTheSeatDipEffect.pdf
- DAFx-25, hybrid ray-tracing / FDN with Abel-Huang crossover — https://eprints.whiterose.ac.uk/id/eprint/237877/1/DAFx25_paper_17.pdf
- Savioja & Xiang, *Simulation-based auralization of room acoustics*, Acoustics Today 2020 — https://acousticstoday.org/wp-content/uploads/2020/12/Simulation-Based-Auralization-of-Room-Acoustics-Lauri-Savioja-and-Ning-Xiang.pdf
- ICA 2016, *Sound energy distribution in Italian opera houses* (Barron theory in 11 opera houses) — http://www.ica2016.org.ar/ica2016proceedings/ica2016/ICA2016-0729.pdf
- PTB round-robin archive incl. raw RR2/RR3 result spreadsheets — https://www.ptb.de/cms/ptb/fachabteilungen/abt1/fb-16/ag-163/round-robin-in-room-acoustics.html
- ODEON model-building guidance (10–30° subdivision of curved surfaces) — https://odeon.dk/learn/making-models/
- Wayverb hybrid-model documentation (order rule, (1−s) rule) — https://reuk.github.io/wayverb/hybrid.html and https://reuk.github.io/wayverb/image_source.html
- Treble validation, BRAS RS7 seat-dip — https://docs.treble.tech/validation/fundamental-effects/RS7
- AES, *Measuring mixing time in non-Sabinian rooms* — https://suonoevita.it/media/medialibrary/2020/04/2012_paper_AES_mixingTime.pdf
- Teatro dell'Opera di Roma ISO 3382-1 survey — https://cris.unibo.it/retrieve/90411652-a478-4063-b043-6cd6326c5233/full_paper_638_20240512192954818.pdf
- Defrance et al., matching pursuit for mixing time — https://www.institut-langevin.espci.fr/IMG/pdf/defrance2009.pdf
- Acta Acustica 2020, seating-area design and enclosure — https://acta-acustica.edpsciences.org/articles/aacus/pdf/2020/04/aacus200013.pdf

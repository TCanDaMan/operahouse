# Primary measured room-acoustic data — San Francisco War Memorial Opera House (WMOH)

Research date: 2026-09-06. Angle: published *measured* numbers only, with provenance.

Headline: **exactly one published measured acoustic dataset exists** for this hall —
Beranek's own occupied octave-band reverberation time, measured by the stopped-chord
method in 2001, printed in the Beranek 2004 appendix. Everything else in the literature
is geometry (surveyed, not measured) or subjective conductor ratings. There is **no
published EDT, C80, G, IACC/BQI, LF or unoccupied RT** for WMOH.

---

## 1. Table of every number found

Legend for **Kind**: `Q` = direct quote/transcription from the source; `D` = derived by me
by arithmetic from quoted values; `I` = inference (assignment or interpretation on my part).

### 1a. Measured acoustics

| Quantity | Value | Source | Page | Kind | Notes |
|---|---|---|---|---|---|
| RT, **occupied**, 125 Hz | 1.59 s | Beranek 2004, Appendix 3 (RT tables) via Google Books snippet — https://books.google.com/books?id=_jLTBwAAQBAJ&q=%22WAR+MEMORIAL+OPERA+HOUSE+(+Opened%22 | p. 592 | Q | row header reads `22. SAN FRANCISCO, WAR MEMORIAL OPERA HOUSE (Opened 1932, 3,252 seats)`; method line reads `RT, occupied  Beranek, stop cords  2001` |
| RT, occupied, 250 Hz | 1.58 s | same | 592 | Q | |
| RT, occupied, 500 Hz | 1.53 s | same | 592 | Q | |
| RT, occupied, 1 kHz | 1.46 s | same | 592 | Q | |
| RT, occupied, 2 kHz | 1.39 s | same | 592 | Q | |
| RT, occupied, 4 kHz | 1.26 s | same | 592 | Q | |
| RT_mid, occupied (500/1k avg) | **1.495 s ≈ 1.50 s** | derived from above | 592 | D | Beranek's own RT_mid definition |
| Bass ratio BR = (RT125+RT250)/(RT500+RT1k) | **1.060** | derived from above | 592 | D | 3.17/2.99 |
| Treble ratio (RT2k+RT4k)/(RT500+RT1k) | 0.886 | derived | 592 | D | |
| Measurement method | stopped chords during performance, 2001, by Beranek | same | 592 | Q | `stop cords` is the book's/OCR's abbreviation for stopped chords |
| RT, **unoccupied** | **not published** | Beranek 2004 index lists WMOH at pp. "141, 592" only | 661 | Q | the p. 592 block contains a single row (occupied) for this hall |
| EDT, C80, G, G125, BQI/IACC, LF | **not published** | Beranek 2004 index (WMOH → 141, 592 only); Hidaka & Beranek 2000 explicitly excludes it | 661 / JASA 107(1) p. 369 | Q | see §3 |
| ITDG / initial-time-delay gap, **t_I** | **51 msec** | Beranek 1996, *Concert and Opera Halls: How They Sound*, "Technical details" box — local scan `sources/research/beranek1996/p160.png` | p. 160 | Q | printed `t_I = 51 msec`. Confirmed identical in Beranek 2004 via Google Books snippet `... SA / N = 6.53 ft2 ( 0.61 m2 ) ITDG = 51 msec` (https://books.google.com/books?id=_jLTBwAAQBAJ&q=%22SA+%2F+N+%3D+6.53%22) |

**Caveat on the 2001 RT:** the appendix row still carries the pre-renovation seat count
(3,252) even though the measurement post-dates the 1992–97 seismic renovation and
re-seating. Beranek did not update N for the appendix header. Treat the RT as valid for
the post-renovation hall, the seat count as stale.

### 1b. Geometry / technical details (Beranek's survey, "Opera" configuration)

All of the following are printed in a single boxed table. **Primary evidence: local page
scan `sources/research/beranek1996/p160.png` (Beranek 1996, p. 160), read directly.**
Independently reconfirmed field-by-field from Beranek 2004 (pp. 141/144) via Google Books
snippets — identical values, so the data did not change between editions.

| Symbol | Value (US) | Value (SI) | Kind |
|---|---|---|---|
| V (volume, opera config.) | 738,600 ft³ | 20,900 m³ | Q |
| S_o (orchestra **pit** area) | 760 ft² | 70.6 m² | Q |
| S_p (stage area) | 2,500 ft² | 232 m² | Q |
| S_a (seating area) | 16,500 ft² | 1,518 m² *(as printed 1996; 2004 prints 1,533 m²)* | Q |
| S_A (acoustical audience area) | 21,240 ft² | 1,973 m² | Q |
| S_T (total acoustical absorbing area) | 24,500 ft² | 2,276 m² | Q |
| N (seats) | 3,252 | — | Q |
| H (ceiling height) | 73 ft | 22.2 m | Q |
| W (width) | 104 ft | 31.7 m | Q |
| L (length) | 120 ft | 36.6 m | Q |
| D (stage-to-farthest-seat) | 122 ft | 37.2 m | Q |
| V/N | 227 ft³ | 6.43 m³ | Q |
| S_A/N | 6.53 ft² | 0.61 m² | Q |
| V/S_A | 34.8 ft | 10.6 m | Q |
| V/S_T | 30.1 ft | 9.19 m | Q |
| H/W | 0.70 | — | Q |
| L/W | 1.15 | — | Q |
| t_I (ITDG) | 51 msec | — | Q |

Internal consistency checks I ran (all pass, so the assignment to WMOH is secure):
V/N = 738,600/3,252 = 227.1 ✓; S_A/N = 21,240/3,252 = 6.53 ✓; V/S_A = 738,600/21,240 = 34.8 ✓;
V/S_T = 738,600/24,500 = 30.1 ✓; H/W = 73/104 = 0.702 ✓; L/W = 120/104 = 1.154 ✓;
S_T = S_A + S_p + S_o = 21,240 + 2,500 + 760 = 24,500 ✓.

Google Books URLs used for the 2004 reconfirmation (all volume id `_jLTBwAAQBAJ`):
- https://books.google.com/books?id=_jLTBwAAQBAJ&q=%22738%2C600+ft3%22
- https://books.google.com/books?id=_jLTBwAAQBAJ&q=%22Sp+%3D+2%2C500+ft2%22
- https://books.google.com/books?id=_jLTBwAAQBAJ&q=%22S1+%3D+24%2C500%22
- https://books.google.com/books?id=_jLTBwAAQBAJ&q=%22V+%2F+N+%3D+227%22

### 1c. Seating breakdown (Beranek's own diagram)

| Level | Seats | Source | Kind |
|---|---|---|---|
| (1) main floor / orchestra | 1,300 | Beranek 1996 p. 159 seating diagram — local scan `sources/research/beranek1996/p159.png`; same diagram in Beranek 2004 p. 143 (Google Books PA143) | Q |
| (2) boxes | 192 | same | Q |
| (3) (grand tier / dress circle band) | 852 | same | Q |
| (4) (balcony band) | 908 + 300 standees | same | Q |
| Total | **3,252** | same | Q |

### 1d. Surface materials relevant to absorption (Beranek 1996 p. 160, "Architectural and structural details")

All `Q` from the local scan `sources/research/beranek1996/p160.png`:
- Ceiling: plaster except the centre domed section, which the architect says is **acoustic plaster**.
- Walls: plaster with some wood trim.
- Floors: entire floor area carpeted **except** in the upper part of the top balcony, where carpet is only in the aisles.
- Stage: wood over air space. Pit: wooden floor on elevator; wooden rear and front walls with 1 ft (30 cm) of velvet over an open railing.
- Stage height: 40 in (102 cm) above floor level at the first row of seats.
- Added absorptive material: velvet draperies above the rails of cross aisles (book prints "about 1 ft (2.5 cm)" — an internal typo; 2.5 cm = 1 **in**).
- Seating: main floor fully upholstered, four 1-in (2.5 cm) holes in the underseat; balcony upholstered **but with hard backs**.
- Orchestra (stage) enclosure: canvas throughout except ¼-in plywood covering the walls up to 10 ft (3 m).
- Architect: Arthur Brown, Jr. Collaborating architect: G. Albert Lansburgh.
- Beranek's note: `Details verified by the author during a visit and by management (1993)`.

### 1e. Stage / pit dimensions (venue's own technical specifications)

`Q` from the repo's own copy, `sources/wmoh-technical-specs.pdf` (SF War Memorial &
Performing Arts Center, "War Memorial Opera House technical specifications", p. 8):

| Item | Value |
|---|---|
| Proscenium opening | 52 ft wide |
| Height of permanent valence at centreline | 31 ft 6 in |
| Grid height | 116 ft |
| Stage height from house floor | 3 ft 6 in |
| Curtain line to pit (apron edge) | 4 ft 4 in |
| Curtain line to back wall | 64 ft |
| Stage sidewall to sidewall | 123 ft |
| Torm towers opening | 41 ft 4 in to 48 ft 8 in |
| Balcony rail to footlights | 80 ft |
| Orchestra pit playing positions (below stage level) | 6 ft 8 in, 7 ft 11 in, or 8 ft 2 in |
| Orchestra pit maximum capacity | 90 musicians |
| Orchestra pit width at centre line | 19 ft 10 in |
| Auditorium capacity (this document) | 3,146-seat auditorium; 3,126 seated on the chart |

### 1f. 1932 primary source (design-stage, qualitative only)

Clifford M. Swan, Consulting Acoustical Engineer, "The Acoustics of the San Francisco
Opera House," *The Architect and Engineer* **111**, pp. 44 & 59 (November 1932).
Full text already in the repo at `sources/research/ae1932/AE_1932_text.txt` (lines ~10136–10250 and ~11647–11700).

- **No measured or calculated RT value is printed.** Swan writes only that `The degree of
  reverberation was calculated` and adjusted to "its optimum value". `Q`
- Same issue, unsigned stage article: total building volume `about 6,000,000 cubic feet`; proscenium
  approx. 50 ft soffit-to-floor × 52 ft side-to-side; gridiron 116 ft; stage wall-to-wall approx. 135 ft;
  back wall approx. 90 ft from proscenium. `Q`
- Beranek cites this article as his own reference: B. J. S. Cahill, "The San Francisco War
  Memorial Group," *The Architect and Engineer* 111, 11–44, 59 (Nov 1932). `Q` from Beranek 1996 p. 160.

### 1g. Subjective (not measured, included for completeness)

| Item | Value | Source | Kind |
|---|---|---|---|
| Conductor ratings, Beranek 1996 | seven conductors interviewed; `Each rated it good` from both conductor and listener positions | Beranek 1996 p. 157 (`sources/research/beranek1996/p157.png`) | Q |
| Balcony vs main floor | several conductors said `the audience hears much better in the balcony` | Beranek 1996 p. 157 | Q |
| ITDG, subjective | Beranek: ITDG `somewhat too long` for listeners in the forward main floor | Beranek 1996 p. 157 | Q |
| Hidaka & Beranek 2000 questionnaire | WMOH included, hall code **SO**; rated in Fig. 3 (21 halls) | https://www.researchgate.net/publication/12672199_… (full text of JASA 107(1) 368–383), p. 369 | Q |
| Rating spread | WMOH among halls with the largest s.d., `0.9 to 1.0` | same, p. 369 | Q |
| Beranek 2004 conductor-ratings figure | `San Francisco, War Memorial` appears in the "Quality ratings by 21 conductors" chart | Beranek 2004 p. 555, Google Books snippet https://books.google.com/books?id=N6ZxI6Zqmv0C&q=%22SAN+FRANCISCO+%2C+WAR+MEMORIAL%22 | Q |

---

## 2. Source-quality notes

1. **Beranek 1996 pp. 157/159/160 — page scans already in this repo** (`sources/research/beranek1996/`).
   This is the strongest evidence in the whole set: it is the printed page, read directly, not OCR.
   It supplies the complete technical-details box including t_I = 51 msec. **Highest confidence.**
2. **Beranek 2004 via Google Books snippet view** (volume ids `_jLTBwAAQBAJ` — good OCR reading
   order — and `N6ZxI6Zqmv0C` — column-scrambled OCR). Snippets are genuine OCR of the printed
   page, but Google's "page" units cover two-page spreads, so **two halls' technical-details boxes
   are interleaved in one snippet**. I resolved every field by arithmetic self-consistency
   (see §1b) and by cross-checking against the 1996 printed scan. **High confidence for the values
   I list; do not trust a raw snippet read without the ratio checks.**
3. **Hidaka & Beranek, JASA 107(1), 368–383 (2000)** — full text is mirrored on ResearchGate
   (https://www.researchgate.net/publication/12672199_Objective_and_subjective_evaluations_of_twenty-three_opera_houses_in_Europe_Japan_and_the_Americas).
   The publisher page (https://pubs.aip.org/asa/jasa/article/107/1/368/550525/) returns HTTP 403.
   **Authoritative for the negative result** (§3).
4. **JASA 103(5) Pt. 2, p. 2861 (May 1998)** — 16th ICA / 135th ASA meeting programme, scanned copy
   at https://backend.orbit.dtu.dk/ws/files/4084227/Leif.pdf. Contains abstract **2pAAa6**,
   "Acoustic conditions of the San Francisco War Memorial Opera House and its renovation",
   Dennis Paoletti, Kurt Graffy, Larry Tedford, Red Wetherill (Paoletti Assoc., 40 Gold St., SF).
   **Abstract contains zero numbers** — it is a history-and-renovation talk. It is nonetheless the
   single most important lead for unpublished measured data. Also 2pAAa7 (Ewart A. Wetherill,
   Paoletti Assoc.) on the Civic Auditorium substitute venue during the 1995–97 closure.
5. **u-s-history.com/pages/h2581.html** — secondary, but corroborates the consultant:
   `Auerbach also hired the firm of Paoletti and Associates to test reverberation time and background noise`.
   Low authority; useful only as confirmation that measurements were made.
6. **`sources/wmoh-technical-specs.pdf`** — the venue's own rental technical spec. Authoritative
   for stage/pit geometry, not for acoustics.
7. **proaudioencyclopedia.com** "Comments on Leo L. Beranek's Three Concert-Hall-Opera-House Books"
   (http://proaudioencyclopedia.com/comments-on-leo-l-beraneks-three-concert-hall-opera-house-books-and-suspended-sound-reflecting-panels-in-concert-halls/)
   tabulates Beranek's hall data but **omits WMOH by design**: `Opera Houses not regularly used for
   orchestral concerts are omitted`. Scraped (66 KB) — zero WMOH mentions.
8. **ICA 2016 paper 0502** (http://www.ica2016.org.ar/ica2016proceedings/ica2016/ICA2016-0502.pdf),
   PROMETHEE II rank-ordering of the Hidaka–Beranek opera houses. Downloaded and read: WMOH does not
   appear anywhere in it. Useful only as confirmation of the Hidaka–Beranek hall set.
9. **Unreachable / rejected**: archive.org lending copies of both Beranek books
   (`concertoperahall0000bera`, `concerthallsoper0000bera`) — the `fulltext/inside.php` search-inside
   endpoint returns "Item not available" without a logged-in borrow. Google Books API — anonymous
   quota is 0. HathiTrust — Cloudflare 403. vdoc.pub / pdfcoffee full-book PDFs — blocked by
   copyright notice / 403; not pursued further.
10. A Facebook post surfaced claiming `The reverberation time has been measured at 1.4 seconds`.
    **Unsourced, uncorroborated, and inconsistent with Beranek's 1.50 s.** Do not use.

---

## 3. Conflicts and contradictions between sources

1. **The 850,000 ft³ / 24,070 m³ trap.** Google Books' OCR of Beranek 2004 places
   `TECHNICAL DETAILS V = 850,000 ft3 ( 24,070 m3 )` immediately after the running head
   `San Francisco War Memorial Opera House` on page PA140. **That volume is Davies Symphony
   Hall's, not WMOH's.** Proof: Beranek 2004's own summary table at p. 622 reads
   `San Francisco , Davies Hall  2,743  24,070 ...` (https://books.google.com/books?id=_jLTBwAAQBAJ&q=%2224%2C070%22).
   The trailing "TECHNICAL DETAILS" block in each Google page belongs to the *facing* page, i.e.
   the *next* hall. WMOH's own box, which opens `TECHNICAL DETAILS Opera V = 738,600 ft3 ( 20,900 m3 )`,
   appears at the end of page 140 and belongs to page 141. Confirmed against the 1996 printed scan.
   **Anyone scraping Beranek's WMOH volume from Google Books will get this wrong.**
2. **Seat count.** Beranek (both editions, and the 2001 RT row header): **3,252**.
   SF Opera today: **3,006** (https://www.sfopera.com/about/war-memorial-opera-house/).
   SFWMPAC technical spec: **3,146-seat auditorium**, chart total **3,126 seated**.
   Wikipedia: 3,146 plus standing room for 200. These are four different numbers for four
   different definitions/eras. Beranek's V/N = 227 ft³ and S_A/N = 6.53 ft² are computed on 3,252
   and must be recomputed if you use 3,006 (V/N → 246 ft³ / 6.96 m³; S_A/N → 7.07 ft² / 0.656 m²) `D`.
3. **S_a in m².** Beranek 1996 p. 160 prints `S_a = 16,500 ft² (1,518 m²)`; the 2004 OCR gives
   `1,533 m²`. 16,500 ft² = 1,532.9 m², so **1,533 is arithmetically correct** and 1,518 is either a
   1996 typo or my misread of the scan. Low impact (1%).
4. **Draperies dimension.** Beranek 1996 p. 160 prints `about 1 ft (2.5 cm)`. 2.5 cm is 1 **inch**.
   Book-internal typo.
5. **"1.4 seconds"** (Facebook, unsourced) vs Beranek's measured 1.50 s mid-frequency occupied.
   Discard the former.
6. **Is WMOH one of the Hidaka–Beranek 23? No.** JASA 107(1) p. 369 lists the halls added to the
   conductor questionnaire but not measured: Munich, Naples San Carlo, Rome, **San Francisco War
   Memorial**, Paris Bastille, Amsterdam Stadtsschouwburg, Tokyo NHK Hall —
   `for which we have no acoustical data`. This is a direct, explicit negative from the authors.
   The 2004 book's index independently confirms it (WMOH → pp. 141, 592 only; the measured-parameter
   tables live at pp. 512–517 and 562–563).

---

## 4. What could not be found, and where it most likely lives

| Missing quantity | Most likely location |
|---|---|
| **Unoccupied octave-band RT, EDT, C80, G, G125, LF/LEF, IACC/BQI** | Do not exist in the open literature. The only measurement campaign that would have produced them is **Paoletti Associates'** work for the 1992–97 renovation. Their public trace is ASA abstract **2pAAa6**, JASA 103(5) Pt. 2, p. 2861 (16th ICA/135th ASA, Seattle, June 1998) — abstract only, no data, no full paper in the proceedings. Next step: contact **Kurt Graffy** (later at Arup SF) or **Dennis Paoletti** (Paoletti Associates → Stantec) directly, or file a records request with the **San Francisco War Memorial Board of Trustees**, who commissioned the studies. The venue's Historic Structure Report (repo has `sources/research/hsr1993/`) is another candidate. |
| Whether **Beranek 1996** printed a pre-2001 occupied RT for WMOH | Beranek 1996 *Concert and Opera Halls: How They Sound*, **Appendix 3** (RT-vs-frequency tables, roughly pp. 610–640 of that edition). The repo scan set stops at pp. 157/159/160 (the hall entry). The 1996 book has **no Google Books preview** (volume `5i1UAAAAMAAJ` = no snippets), and the archive.org copy `concertoperahall0000bera` is lending-restricted. Get it via a library borrow of the archive.org item, or a physical copy. Note the 2004 appendix's only RT source for WMOH is dated **2001**, so it is quite likely the 1996 edition carried **no** measured RT at all for this hall. |
| The 2001 stopped-chord protocol (how many chords, mic positions, which performance) | Beranek 2004, **Appendix 3 preamble**, roughly pp. 585–591, and/or Beranek's methodology chapters. Not captured in the snippets I could pull. |
| Post-1997 total surface area / volume change | Never published. Beranek's 738,600 ft³ was `verified … during a visit and by management (1993)`, i.e. **pre-renovation**, and he did not revise it for the 2004 edition despite re-measuring RT in 2001. |
| Audience area consistent with the current 3,006 seats | Not published. Beranek's S_A = 21,240 ft² (1,973 m²) is on the 3,252-seat layout. |

---

## 5. Bottom-line numbers to use

```
Occupied RT (measured, Beranek stopped chords, 2001), octave bands 125–4k Hz:
    1.59, 1.58, 1.53, 1.46, 1.39, 1.26  seconds
    RT_mid (500/1k) = 1.50 s     Bass ratio = 1.06
ITDG t_I = 51 ms   (Beranek, surveyed)
V = 738,600 ft3 = 20,900 m3      (opera configuration, pre-1997 survey)
S_a = 16,500 ft2 (1,533 m2)  S_A = 21,240 ft2 (1,973 m2)  S_T = 24,500 ft2 (2,276 m2)
S_o pit = 760 ft2 (70.6 m2)      S_p stage = 2,500 ft2 (232 m2)
H = 73 ft (22.2 m)  W = 104 ft (31.7 m)  L = 120 ft (36.6 m)  D = 122 ft (37.2 m)
N = 3,252 (Beranek era) / 3,006 (current SF Opera)
No published EDT, C80, G, IACC/BQI, LF, or unoccupied RT exists for this hall.
```

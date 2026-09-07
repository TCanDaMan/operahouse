"""Geometric room acoustics for every seat.

Early sound: image-source reflections (first and second order) against the
modelled surfaces of the house -- ceiling profile, side walls, rear walls,
tier soffits, tier fronts, stage and orchestra floors. Every path segment is
checked through the proscenium opening and against the tier slabs, so a
seat under a balcony loses the ceiling and gets its soffit instead, and a
seat far to the side loses whatever the proscenium jamb hides.

Late sound: a statistical tail from the published volume and an assumed
occupied reverberation time (data/house_geometry.json > acoustics). Under an
overhang the tail is scaled by how much of the room the seat can see.

Frame: feet, x across, y up, z toward the rear; curtain line at z = 0.
Everything here is a model. Confidence of each input is recorded in
house_geometry.json; the seat-to-seat *differences* are the useful output.
"""
import math

C_FT = 1125.3                    # speed of sound, ft/s
FT = 0.3048
BANDS = ("125", "500", "2k", "4k")
BAND_HZ = (125.0, 500.0, 2000.0, 4000.0)
MID = (1, 2)                     # 500 Hz and 2 kHz columns
HI = 3
EARLY_MS = 80.0
MAX_ORDER = 2
# Onset ramp of the statistical tail, shared by the C80 accounting and the
# renderer (exported as tail_rise_s). An anti-click device only: Barron's
# 170-measurement test (JASA 137, 2015, Table VII) shows reflected energy is
# best integrated from the direct-sound arrival, and a long ramp with the tail
# renormalised afterwards moved ~3 dB of energy past 80 ms in this model.
TAIL_RISE_S = 0.002
# Barron & Lee revised theory: total reflected energy relative to the direct
# sound at 10 m is (31200 T / V) exp(-0.04 r / T), r in metres. The exponential
# is the empirical distance decay the flat Sabine 4/R lacks (0.174 r/T dB, so
# 3.5 dB at 30 m); rms error against 212 measurements in 19 halls 1.0 dB (G),
# 1.4 dB (C80). Validated for opera houses with a fore-stage source; the pit
# source under the proscenium is outside that validation.
BARRON_K = 31200.0
BARRON_DECAY = 0.04
TAIL_FLOOR = 0.25   # the tail never drops below this fraction of Barron's total

# --------------------------------------------------------------- context
K = {}   # filled by configure(): geometry callables and constants

def configure(**kw):
    K.clear()
    K.update(kw)
    A = K["G"]["acoustics"]
    K["alpha"] = A["absorption"]["value"]
    K["air"] = A["air_absorption_db_per_100ft"]["value"]
    K["rt"] = [A["rt_occupied_s"]["value"][b] for b in BANDS]
    K["V"] = A["volume_m3"]["value"]
    K["rear_db"] = A["voice_directivity_db_at_rear"]["value"]
    _build_surfaces()
    _build_slab_grid()
    # Sabine: A = 0.161 V / RT, room constant R = A / (1 - mean alpha)
    S_total = 8000.0            # m2, rough interior surface of a 20,900 m3 house
    K["R"] = []
    for rt in K["rt"]:
        Ab = 0.161 * K["V"] / rt
        K["R"].append(Ab / max(0.2, 1 - Ab / S_total))

# --------------------------------------------------------------- vectors
def sub(a, b): return (a[0]-b[0], a[1]-b[1], a[2]-b[2])
def add(a, b): return (a[0]+b[0], a[1]+b[1], a[2]+b[2])
def mul(a, s): return (a[0]*s, a[1]*s, a[2]*s)
def dot(a, b): return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
def norm(a):
    l = math.sqrt(dot(a, a)) or 1.0
    return (a[0]/l, a[1]/l, a[2]/l)
def length(a): return math.sqrt(dot(a, a))

class Plane:
    """A bounded planar reflector. inside(p) says whether a point on the
    plane is within the surface; material picks the absorption row."""
    def __init__(self, name, code, point, normal, material, inside, order2=True, dims=None):
        self.name, self.code, self.p0 = name, code, point
        self.n = norm(normal)
        self.material, self.inside, self.order2 = material, inside, order2
        self.dims = dims     # (height, width) in ft for finite reflectors; None = effectively infinite
    def mirror(self, p):
        d = dot(sub(p, self.p0), self.n)
        return sub(p, mul(self.n, 2 * d))
    def hit(self, a, b):
        """Intersection of segment a->b with the plane, strictly inside it."""
        da, db = dot(sub(a, self.p0), self.n), dot(sub(b, self.p0), self.n)
        if da * db >= 0:
            return None
        t = da / (da - db)
        if t < 1e-4 or t > 1 - 1e-4:
            return None
        p = add(a, mul(sub(b, a), t))
        return p if self.inside(p) else None
    def side(self, p):
        return dot(sub(p, self.p0), self.n)

# -------------------------------------------------------------- surfaces
SURFACES = []

def interior_profile():
    c = K["G"]["interior_ceiling"]["value"]
    return [[0, c["main_y"]], [c["main_end"], c["main_y"]]] + [p for p in K["ceiling_profile"] if p[0] > c["main_end"]]

def ceiling_y_at(z):
    prof = interior_profile()
    if z <= prof[0][0]:
        return prof[0][1]
    for (z0, y0), (z1, y1) in zip(prof, prof[1:]):
        if z <= z1:
            return y0 + (y1 - y0) * (z - z0) / (z1 - z0)
    return prof[-1][1]

def _build_surfaces():
    SURFACES.clear()
    hb, prof = K["half_breadth"], interior_profile()
    depth = K["depth_balcony"]
    c = K["G"]["interior_ceiling"]["value"]
    def in_dome(p):
        return (p[0]/c["dome_radius"])**2 + ((p[2]-c["dome_z"])/(c["dome_radius"]*c["dome_aspect"]))**2 < 1
    # The dome footprint is a flat acoustic-plaster patch in the ceiling plane.
    # Beranek 1996 p160: the centre domed section is acoustic plaster; Swan
    # 1932: focusing surfaces were deliberately avoided. Flat facets were
    # rejected: 36 facets of ~7 m2 have a Rindel diffraction cut-off near
    # 500 Hz, so faceting creates a low-frequency hole and patchy coverage.
    # A true curved-surface treatment (specular point on the sphere plus the
    # curvature gain) would raise the return by 5-10 dB in the convergence
    # footprint; until the dome is measured this patch understates that.
    for i, ((z0, y0), (z1, y1)) in enumerate(zip(prof, prof[1:])):
        n = norm((0.0, -(z1 - z0), (y1 - y0)))     # points down into the room
        if n[1] > 0: n = mul(n, -1)
        SURFACES.append(Plane(f"ceiling {i}", "C", (0.0, y0, z0), n, "plaster",
                              lambda p, z0=z0, z1=z1, hb=hb: z0 - 0.01 <= p[2] <= z1 + 0.01 and abs(p[0]) <= hb and not in_dome(p)))
        SURFACES.append(Plane("main dome (acoustic plaster patch)", "C", (0.0, y0, z0), n, "acoustic_plaster",
                              lambda p, z0=z0, z1=z1, hb=hb: z0 - 0.01 <= p[2] <= z1 + 0.01 and abs(p[0]) <= hb and in_dome(p),
                              order2=False))
    # side walls. Above the box zone the upper walls fan out from the
    # proscenium (HSR 1993 balcony and attic plans; tour photos show the
    # three organ-loft arches converging on the proscenium). Those bays are
    # open grilles with heavy curtains behind, so the splays are partly
    # absorptive ("arch_wall"). Below the box zone and behind the splay the
    # walls stay at the published half breadth.
    sw = K["side_wall_plan"]          # [[z, half_width], ...] from the proscenium outward
    y_splay = K["splay_bottom_y"]
    z_full = sw[-1][0]
    for sgn in (-1, 1):
        SURFACES.append(Plane("side wall " + ("L" if sgn < 0 else "R"), "W", (sgn*hb, 0.0, 0.0), (-sgn, 0.0, 0.0), "plaster",
                              lambda p, z_full=z_full, y_splay=y_splay: 0 <= p[2] <= depth and 0 <= p[1] <= ceiling_y_at(p[2])
                              and (p[2] >= z_full or p[1] <= y_splay)))
        for (z0, w0), (z1, w1) in zip(sw, sw[1:]):
            dz, dw = z1 - z0, w1 - w0
            n = (-sgn * dz, 0.0, sgn * dw)          # inward-facing normal of the splayed bay
            n = norm(n)
            if n[0] * sgn > 0: n = mul(n, -1)
            p0 = (sgn * w0, 0.0, z0)
            def inside(p, z0=z0, z1=z1, y_splay=y_splay):
                return z0 - 0.01 <= p[2] <= z1 + 0.01 and y_splay <= p[1] <= ceiling_y_at(p[2])
            SURFACES.append(Plane(f"side wall splay {'L' if sgn < 0 else 'R'} {z0:.0f}-{z1:.0f}", "W", p0, n, "arch_wall", inside))
    # rear walls, one per level
    for name, z, ylo, yhi, mat in K["rear_walls"]:
        SURFACES.append(Plane(name, "R", (0.0, 0.0, z), (0.0, 0.0, -1.0), mat,
                              lambda p, ylo=ylo, yhi=yhi, hb=hb: ylo(p) <= p[1] <= yhi(p) and abs(p[0]) <= hb, order2=False))
    # tier fronts: the traced horseshoe curves as vertical planar segments,
    # each facing into the house. The side runs face inward and give the
    # main floor and boxes lateral reflections the rectangular walls cannot
    # (Hidaka & Beranek 2000 on parapets in horseshoe houses). Fascia
    # heights are small, so each carries Rindel's finite-reflector cut-off.
    for name, curve, ylo, yhi in K["tier_fronts"]:
        h = yhi - ylo
        for sgn in (1, -1):
            pts = [(sgn * x, z) for x, z in curve]
            for (xa, za), (xb, zb) in zip(pts, pts[1:]):
                dx, dz = xb - xa, zb - za
                w = math.hypot(dx, dz)
                if w < 1.0:
                    continue
                n = (dz, 0.0, -dx)
                mid = ((xa + xb) / 2, (ylo + yhi) / 2, (za + zb) / 2)
                if dot(sub((0.0, mid[1], 40.0), mid), n) < 0:
                    n = mul(n, -1)
                def inside(p, xa=xa, za=za, dx=dx, dz=dz, w=w, ylo=ylo, yhi=yhi):
                    t = ((p[0] - xa) * dx + (p[2] - za) * dz) / (w * w)
                    return ylo <= p[1] <= yhi and -0.02 <= t <= 1.02
                SURFACES.append(Plane(name, "T", mid, n, "plaster", inside, order2=False, dims=(h, w)))
    # stage floor (wood) and orchestra floor (audience)
    st = K["stage"]
    SURFACES.append(Plane("stage floor", "F", (0.0, st["y"], 0.0), (0.0, 1.0, 0.0), "wood",
                          lambda p, st=st: st["back_wall_z"] <= p[2] <= K["pit_front_z"] and abs(p[0]) <= 40, order2=False))
    # The audience floor is not modelled as a reflector: sound grazing the
    # seated audience is absorbed and scattered (the seat-dip effect is
    # flagged separately), and a flat plane there produced a spurious
    # first reflection a fraction of a millisecond after the direct sound.

# ------------------------------------------------------ slab occlusion grid
GRID = {}
CELL = 2.0

def _build_slab_grid():
    GRID.clear()
    hb = K["half_breadth"]
    xs = int(hb / CELL) + 1
    zs = int(K["depth_balcony"] / CELL) + 2
    for ix in range(-xs, xs + 1):
        for iz in range(-5, zs + 1):
            x, z = ix * CELL, iz * CELL
            slabs = []
            for o, top in K["overhangs"]:
                if o.contains(x, z):
                    lo = o.soffit(x, z)
                    hi = top(x, z)
                    if hi > lo:
                        slabs.append((lo, hi))
            if slabs:
                GRID[(ix, iz)] = slabs

def in_slab(p):
    slabs = GRID.get((round(p[0] / CELL), round(p[2] / CELL)))
    if not slabs:
        return False
    return any(lo <= p[1] <= hi for lo, hi in slabs)

def through_proscenium(a, b):
    """A segment crossing the curtain line must pass through the opening."""
    if (a[2] < 0) == (b[2] < 0):
        return True
    t = a[2] / (a[2] - b[2])
    x = a[0] + (b[0] - a[0]) * t
    y = a[1] + (b[1] - a[1]) * t
    st = K["stage"]
    return abs(x) <= st["prosc_w"] / 2 and st["y"] <= y <= st["y"] + st["prosc_h"]

def segment_clear(a, b, skip_start=0.0):
    if not through_proscenium(a, b):
        return False
    d = sub(b, a)
    L = length(d)
    n = max(1, int(L / 2.0))
    for k in range(n):
        t = (k + 0.5) / n
        if t * L < skip_start:
            continue
        p = add(a, mul(d, t))
        if in_slab(p):
            return False
    return True

# --------------------------------------------------------------- source
def directivity_db(src, forward, to_pt):
    """Level relative to on-axis for a source facing `forward`."""
    if forward is None:
        return 0.0
    d = norm(sub(to_pt, src))
    c = max(-1.0, min(1.0, dot(d, forward)))
    return K["rear_db"] * (1 - c) / 2

def path_amplitude(src, forward, points, surfaces, listener):
    """Per-band pressure amplitude relative to 1 at 1 ft on axis."""
    pts = [src] + points + [listener]
    L = sum(length(sub(b, a)) for a, b in zip(pts, pts[1:]))
    d_db = directivity_db(src, forward, pts[1])
    # Rindel finite-reflector cut-off for each bounded panel: below
    # f_g = c a* / (2 S cos(theta)), a* = 2 a1 a2 / (a1 + a2), the reflection
    # falls at 6 dB/octave. S is taken as the smaller dimension squared, the
    # conservative reading for long thin fascias. Big walls and ceilings carry
    # no dims and are treated as infinite.
    cut = []
    for i, s in enumerate(surfaces):
        if not s.dims:
            continue
        a1, a2 = length(sub(pts[i + 1], pts[i])) * FT, length(sub(pts[i + 2], pts[i + 1])) * FT
        a_star = 2 * a1 * a2 / max(a1 + a2, 1e-6)
        inc = norm(sub(pts[i + 1], pts[i]))
        cos_t = max(0.2, abs(dot(inc, s.n)))
        S = (min(s.dims) * FT) ** 2
        cut.append(343.0 * a_star / (2 * S * cos_t))
    amps = []
    for b in range(4):
        g = 10 ** (d_db * (0.15, 0.5, 1.0, 1.2)[b] / 20) / max(L, 0.1)
        for s in surfaces:
            g *= math.sqrt(max(0.0, 1 - K["alpha"][s.material][b]))
        for f_g in cut:
            g *= min(1.0, BAND_HZ[b] / f_g)
        g *= 10 ** (-K["air"][b] * L / 100 / 20)
        amps.append(g)
    return L, amps

# ------------------------------------------------------------ reflections
def find_paths(src, forward, listener, surfaces, direct_blocked):
    """Valid first- and second-order image-source paths."""
    out = []
    for s1 in surfaces:
        # source and listener must be on the same side of the reflector;
        # local soffit planes are inclined stand-ins, so hit() alone judges them
        if s1.code != "S" and s1.side(src) * s1.side(listener) < 0:
            continue
        i1 = s1.mirror(src)
        p1 = s1.hit(listener, i1)
        if p1 is not None and segment_clear(src, p1) and segment_clear(p1, listener, skip_start=3.0):
            L, amps = path_amplitude(src, forward, [p1], [s1], listener)
            out.append({"pts": [p1], "surf": [s1], "L": L, "amps": amps})
        if MAX_ORDER < 2 or not s1.order2:
            continue
        for s2 in surfaces:
            if s2 is s1 or not s2.order2:
                continue
            i2 = s2.mirror(i1)
            p2 = s2.hit(listener, i2)
            if p2 is None:
                continue
            p1b = s1.hit(p2, i1)
            if p1b is None:
                continue
            if not (segment_clear(src, p1b) and segment_clear(p1b, p2) and segment_clear(p2, listener, skip_start=3.0)):
                continue
            L, amps = path_amplitude(src, forward, [p1b, p2], [s1, s2], listener)
            out.append({"pts": [p1b, p2], "surf": [s1, s2], "L": L, "amps": amps})
    return out

def arrival_angles(listener, look, frm):
    """Azimuth (deg, + = right) and elevation of sound arriving from `frm`
    for a listener facing `look` (a horizontal unit vector)."""
    d = norm(sub(frm, listener))
    fwd = (look[0], 0.0, look[2])
    right = (-fwd[2], 0.0, fwd[0])
    az = math.degrees(math.atan2(dot(d, right), dot(d, fwd)))
    el = math.degrees(math.asin(max(-1.0, min(1.0, d[1]))))
    return az, el

# ---------------------------------------------------------------- per seat
SCATTER = Plane("overhang edge", "S", (0.0, 0.0, 0.0), (0.0, -1.0, 0.0), "plaster", lambda p: True, order2=False)
SCALE = 4 * math.pi * FT ** 2   # model energy (1/ft^2 on axis) -> 1/(4 pi r_m^2)

def seat_dip_db(elev_deg, audience_m):
    """Excess attenuation of a direct sound that grazes the seated audience.
    Kahle et al. (Forum Acusticum 2025) and Round Robin 1: ~0.7 dB per metre of
    audience traversed across 400 Hz-3 kHz at 0 degrees source elevation, plus a
    quarter-wave notch near 100-160 Hz, falling to nothing above ~15 degrees.
    Returned per band (125 Hz, 500 Hz, 2 kHz, 4 kHz), capped at 16 dB."""
    scale = max(0.0, min(1.0, 1.0 - elev_deg / 15.0))
    if scale <= 0 or audience_m <= 0:
        return [0.0] * 4
    broad = min(16.0, 0.7 * audience_m) * scale
    return [min(10.0, 0.5 * audience_m) * scale, broad, broad, 0.5 * broad]

def seat_acoustics(eye, direct_blocked_fn, soffit_planes_fn, pit_visible, grazing, oh, lip=None):
    """Compute the acoustic picture at one listening position.
    oh  = fraction of the room's late sound reaching a seat under an overhang
          (Barron 1995: overhangs cut late sound consistently, early sound
          haphazardly, so it multiplies the tail only).
    grazing = (elevation of the singer in degrees, metres of audience the
          direct sound skims) or None when the seat does not graze.
    lip = (x, y, z) of the overhang edge in front of the seat, if any: the
          fascia and soffit edge scatter sound down to the seats beneath."""
    singer, pit = K["singer"], K["pit_src"]
    look = norm((singer[0] - eye[0], 0.0, singer[2] - eye[2]))
    local = soffit_planes_fn(eye)          # soffit planes valid around this seat
    surfaces = SURFACES + local
    res = {}
    aur = {}
    direct_blocked = direct_blocked_fn(eye, singer)
    for key, src, fwd, blocked in (
            ("singer", singer, (0.0, 0.0, 1.0), direct_blocked),
            ("pit", pit, None, pit_visible < 0.1)):
        Ld = length(sub(eye, src))
        t0 = Ld / C_FT * 1000
        _, damps = path_amplitude(src, fwd, [], [], eye)
        if blocked:                          # diffraction over the lip / rail
            damps = [a * 10 ** (-(5 if key == "pit" else 12) / 20) for a in damps]
        dip = seat_dip_db(*grazing) if grazing else [0.0] * 4   # both sources skim the same rows
        damps = [a * 10 ** (-d / 20) for a, d in zip(damps, dip)]
        paths = find_paths(src, fwd, eye, surfaces, blocked)
        taps = []
        for p in paths:
            t = p["L"] / C_FT * 1000 - t0
            az, el = arrival_angles(eye, look, p["pts"][-1])
            taps.append({"t": t, "amps": p["amps"], "az": az, "el": el,
                         "code": "".join(s.code for s in p["surf"]),
                         "pt": p["pts"], "surf": [s.name for s in p["surf"]]})
        if lip is not None and segment_clear(src, lip) and segment_clear(lip, eye, skip_start=3.0):
            # diffuse scatter from the overhang edge: a specular-strength path
            # via the lip point, 6 dB down, spread over the soffit lowpass
            L, amps = path_amplitude(src, fwd, [lip], [SCATTER], eye)
            az, el = arrival_angles(eye, look, lip)
            taps.append({"t": L / C_FT * 1000 - t0, "amps": [a * 0.5 for a in amps], "az": az, "el": el,
                         "code": "S", "pt": [lip], "surf": ["overhang edge (scattered)"]})
        taps.sort(key=lambda q: q["t"])
        aur[key] = (t0, damps, taps, Ld)
    # ---- energies (mid band, metric distances), voice source
    t0, damps, taps, Ld = aur["singer"]
    mid = lambda amps: (amps[1] ** 2 + amps[2] ** 2) / 2      # pressure^2, relative
    e_dir = mid(damps)
    e_early = sum(mid(q["amps"]) for q in taps if q["t"] <= EARLY_MS)
    e_late_refl = sum(mid(q["amps"]) for q in taps if q["t"] > EARLY_MS)
    lateral = sum(mid(q["amps"]) * math.sin(math.radians(q["az"])) ** 2
                  for q in taps if 5 <= q["t"] <= EARLY_MS)
    # Statistical tail, Barron & Lee revised theory, per source and band. The
    # total reflected energy at this distance is the target; the explicit
    # image-source paths carry part of it and the tail carries the rest, so
    # nothing is counted twice. The tail starts at the direct arrival (Barron
    # 2015) and decays with the measured band RT. Equal source power is assumed
    # for singer and pit, not a measured orchestral balance. Model units: the
    # on-axis direct sound is 1/L_ft^2; Barron's unit is the direct sound at
    # 10 m, i.e. 1/(4 pi 100) in metric intensity.
    tails = {}
    for key in ("singer", "pit"):
        _t0, _d, ktaps, kLd = aur[key]
        r_m = kLd * FT
        total = [BARRON_K * K["rt"][b] / K["V"] * math.exp(-BARRON_DECAY * r_m / K["rt"][b])
                 / (4 * math.pi * 100) * SCALE * oh for b in range(4)]
        explicit = [sum(q["amps"][b] ** 2 for q in ktaps) for b in range(4)]
        tails[key] = [max(total[b] - explicit[b], TAIL_FLOOR * total[b]) for b in range(4)]
    tail_energy = tails["singer"]
    e_late = (tail_energy[1] + tail_energy[2]) / 2
    sig = [q for q in taps if mid(q["amps"]) >= e_dir * 10 ** (-15 / 10) and q["code"] not in ("F", "S")]
    itdg = sig[0]["t"] if sig else None
    rise = TAIL_RISE_S
    late_tail = sum(tail_energy[b] * tail_fraction_after(EARLY_MS / 1000, K["rt"][b], rise)
                    for b in MID) / 2
    early_total = e_dir + e_early + e_late - late_tail
    late_total = late_tail + e_late_refl
    c80 = 10 * math.log10(early_total / max(late_total, 1e-12))
    # G: total level relative to the same source in the free field at 10 m
    e_ref = SCALE / (4 * math.pi * 10 ** 2)
    g = 10 * math.log10((e_dir + e_early + e_late + e_late_refl) / e_ref)
    lf = lateral / max(e_dir + e_early, 1e-12)
    rev_db = 10 * math.log10(e_late / max(e_dir, 1e-12))
    # voice vs pit balance from direct sound alone
    tp, pamps, _, _ = aur["pit"]
    balance = 10 * math.log10(mid(damps) / max(mid(pamps), 1e-12))
    res.update({
        "itdg_ms": round(itdg, 1) if itdg is not None else None,
        "c80_db": round(c80, 1), "strength_db": round(g, 1), "lateral_fraction": round(lf, 3),
        "reverb_vs_direct_db": round(rev_db, 1), "voice_over_pit_db": round(balance, 1),
        "early_reflections": len([q for q in taps if q["t"] <= EARLY_MS]),
        "first_reflection_from": sig[0]["surf"][-1] if sig else None,
        "direct_path_blocked": bool(direct_blocked),
        "seat_dip": bool(grazing) and seat_dip_db(*grazing)[1] >= 3.0,
        "seat_dip_db": round(seat_dip_db(*grazing)[1], 1) if grazing else 0.0,
    })
    res["sound_score"] = round(sound_score(res), 1)
    # ---- compact auralization record
    def tap_rec(q):
        a = q["amps"]
        return [round(q["t"], 1), round((a[1] + a[2]) / 2, 5), round(a[3], 5),
                round(q["az"]), round(q["el"]), q["code"],
                [[round(v, 1) for v in pt] for pt in q["pt"]],
                [round(v, 8) for v in a]]
    rec = {}
    for key in ("singer", "pit"):
        t0, damps, taps, Ld = aur[key]
        strong = list(taps)  # retain all validated paths: no strongest-N truncation
        strong.sort(key=lambda q: q["t"])
        az, el = arrival_angles(eye, look, K[key if key == "singer" else "pit_src"])
        rec[key] = {"t0": round(t0, 1), "d": [round((damps[1] + damps[2]) / 2, 5), round(damps[3], 5), round(az), round(el)],
                    "r": [tap_rec(q) for q in strong],
                    "bands": [round(v, 8) for v in damps],
                    "tail_energy": tails[key],
                    "tail_start_ms": 0.0,
                    "tail_rise_s": rise}
    rec["version"] = 2
    rec["rev_db"] = round(rev_db, 1)
    rec["rt"] = K["rt"]
    rec["oh"] = round(oh, 2)
    res["aur"] = rec
    return res

def tail_fraction_after(t, rt, rise=TAIL_RISE_S):
    """Integral of [(1-exp(-t/rise))*exp(-3 ln(10)t/RT)]^2.
    Matches the renderer's smooth late-field onset, including the ramp energy."""
    t = max(0.0, t)
    k = 6 * math.log(10) / rt
    rates = (k, k + 1 / rise, k + 2 / rise)
    return sum(w * math.exp(-r*t) / r for w, r in zip((1, -2, 1), rates)) / sum(w/r for w, r in zip((1, -2, 1), rates))

def sound_score(m):
    """0-100 listening score. Weights are opinions, like view_score. Centred on
    the occupied opera-house ranges from Hidaka & Beranek 2000 and Barron:
    strength G about 0 dB (-1.5..+1.5), stage-source C80 +2..+4 dB."""
    s = 94.0
    s -= max(0.0, 0.0 - m["strength_db"]) * 5            # weak, distant sound
    s += min(2.0, max(0.0, m["strength_db"])) * 1.5      # presence: up to +3 for G of +2 dB
    s -= max(0.0, abs(m["c80_db"] - 2.5) - 2.0) * 6      # muddy or dry
    if m["itdg_ms"] is not None:
        # Hidaka & Beranek 2000 recommend t_I <= 20 ms; their 19 measured houses span 14-41 ms
        s -= min(15.0, max(0.0, m["itdg_ms"] - 20) * 0.35)
    s += min(m["lateral_fraction"], 0.30) * 40 - 4        # envelopment: LF 0.10 is neutral, 0.30 earns +8
    s -= max(0.0, m["reverb_vs_direct_db"] - 12) * 1.5    # the room swamps the voice: distant
    s -= max(0.0, -m["voice_over_pit_db"] - 2) * 3       # the pit covers the voice
    s -= min(8.0, 0.5 * m.get("seat_dip_db", 0.0))       # direct sound thinned by grazing the audience
    if m["direct_path_blocked"]:
        s -= 15
    return max(0.0, min(100.0, s))

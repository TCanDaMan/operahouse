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
MID = (1, 2)                     # 500 Hz and 2 kHz columns
HI = 3
EARLY_MS = 80.0
MAX_ORDER = 2
# Onset ramp of the statistical tail, shared by the C80 accounting and the
# renderer (exported as tail_rise_s). Kept short: it is an anti-click device,
# not a physical build-up claim. A 25 ms ramp with the tail energy renormalised
# afterwards moved ~3 dB of tail energy past 80 ms and dropped house-median C80
# to -3..-6 dB, outside the -4..+4 dB range reported for opera houses. The
# coarse image-source set carries only 4-17% of the reflected energy, so the
# tail must stand in for the early reflected energy it does not resolve.
TAIL_RISE_S = 0.005

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
    def __init__(self, name, code, point, normal, material, inside, order2=True):
        self.name, self.code, self.p0 = name, code, point
        self.n = norm(normal)
        self.material, self.inside, self.order2 = material, inside, order2
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
    # Main flat surface has a real hole for the dome; rear matches the viewer.
    for i, ((z0, y0), (z1, y1)) in enumerate(zip(prof, prof[1:])):
        n = norm((0.0, -(z1 - z0), (y1 - y0)))     # points down into the room
        if n[1] > 0: n = mul(n, -1)
        SURFACES.append(Plane(f"ceiling {i}", "C", (0.0, y0, z0), n, "plaster",
                              lambda p, z0=z0, z1=z1, hb=hb: z0 - 0.01 <= p[2] <= z1 + 0.01 and abs(p[0]) <= hb and not in_dome(p)))
    _dome_surfaces(c)
    # side walls
    for sgn in (-1, 1):
        SURFACES.append(Plane("side wall " + ("L" if sgn < 0 else "R"), "W", (sgn*hb, 0.0, 0.0), (-sgn, 0.0, 0.0), "plaster",
                              lambda p: 0 <= p[2] <= depth and 0 <= p[1] <= ceiling_y_at(p[2])))
    # rear walls, one per level
    for name, z, ylo, yhi, mat in K["rear_walls"]:
        SURFACES.append(Plane(name, "R", (0.0, 0.0, z), (0.0, 0.0, -1.0), mat,
                              lambda p, ylo=ylo, yhi=yhi, hb=hb: ylo(p) <= p[1] <= yhi(p) and abs(p[0]) <= hb, order2=False))
    # tier fronts (vertical faces toward the stage), centre portion only
    for name, z, ylo, yhi, xmax in K["tier_fronts"]:
        SURFACES.append(Plane(name, "T", (0.0, 0.0, z), (0.0, 0.0, -1.0), "plaster",
                              lambda p, ylo=ylo, yhi=yhi, xmax=xmax: ylo <= p[1] <= yhi and abs(p[0]) <= xmax, order2=False))
    # stage floor (wood) and orchestra floor (audience)
    st = K["stage"]
    SURFACES.append(Plane("stage floor", "F", (0.0, st["y"], 0.0), (0.0, 1.0, 0.0), "wood",
                          lambda p, st=st: st["back_wall_z"] <= p[2] <= K["pit_front_z"] and abs(p[0]) <= 40, order2=False))
    # The audience floor is not modelled as a reflector: sound grazing the
    # seated audience is absorbed and scattered (the seat-dip effect is
    # flagged separately), and a flat plane there produced a spurious
    # first reflection a fraction of a millisecond after the direct sound.

def _dome_surfaces(c):
    """Bounded triangle approximation of the displayed spherical cap.
    First-order only: avoid pretending this coarse mesh resolves dome focusing."""
    radius, rise = c["dome_radius"], c["dome_rise"]
    sphere = (radius*radius + rise*rise)/(2*rise)
    def point(r, a):
        return (r*math.cos(a), c["main_y"]+rise-sphere+math.sqrt(sphere*sphere-r*r),
                c["dome_z"]+c["dome_aspect"]*r*math.sin(a))
    rings = [[point(radius*f, i*math.tau/12) for i in range(12)] for f in (0, 0.5, 1)]
    def triangle(a,b,cpt):
        u,v=sub(b,a),sub(cpt,a)
        n=(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
        if n[1]>0: n=mul(n,-1)
        def inside(p):
            w=sub(p,a); uu,vv,uv=dot(u,u),dot(v,v),dot(u,v); d=uu*vv-uv*uv
            s=(vv*dot(w,u)-uv*dot(w,v))/d; t=(uu*dot(w,v)-uv*dot(w,u))/d
            # Half-open seams avoid double counting shared edges.
            return s>=0 and t>=0 and s+t<1
        SURFACES.append(Plane("main dome", "C", a,n,"plaster",inside,order2=False))
    for i in range(12):
        j=(i+1)%12
        triangle(rings[0][i],rings[1][i],rings[1][j])
        triangle(rings[1][i],rings[2][i],rings[2][j])
        triangle(rings[1][i],rings[2][j],rings[1][j])

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
    amps = []
    for b in range(4):
        g = 10 ** (d_db * (0.15, 0.5, 1.0, 1.2)[b] / 20) / max(L, 0.1)
        for s in surfaces:
            g *= math.sqrt(max(0.0, 1 - K["alpha"][s.material][b]))
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

def seat_acoustics(eye, direct_blocked_fn, soffit_planes_fn, pit_visible, grazing, oh, lip=None):
    """Compute the acoustic picture at one listening position.
    oh  = fraction of the room's late sound reaching a seat under an overhang.
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
    # statistical tail: 4/R (per unit source power, metric) brought into the
    # model's units, where the on-axis direct sound is 1/L_ft^2
    # One exported tail law drives both the metrics and the rendered response.
    # Total pressure-squared energy per frequency band; equal source-power
    # assumption for singer and pit, not a measured orchestral balance.
    tail_energy = [4 / r * SCALE * oh for r in K["R"]]
    e_late = (tail_energy[1] + tail_energy[2]) / 2
    sig = [q for q in taps if mid(q["amps"]) >= e_dir * 10 ** (-15 / 10) and q["code"] not in ("F", "S")]
    itdg = sig[0]["t"] if sig else None
    # Do not synthesize diffuse room sound before its first valid room return.
    room_taps = [q["t"] for q in taps if q["code"] != "F"]
    t_mix = max(20.0, min(room_taps) if room_taps else 80.0) / 1000
    rise = TAIL_RISE_S
    late_tail = sum(tail_energy[b] * tail_fraction_after(EARLY_MS / 1000 - t_mix, K["rt"][b], rise)
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
        "seat_dip": bool(grazing),
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
                    "tail_energy": tail_energy,
                    "tail_start_ms": max(20.0, min((q["t"] for q in taps if q["code"] != "F"), default=80.0)),
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
    """0-100 listening score. Weights are opinions, like view_score."""
    s = 100.0
    s -= max(0.0, 2.0 - m["strength_db"]) * 5            # weak, distant sound
    s -= max(0.0, abs(m["c80_db"] - 1.5) - 2.0) * 6      # muddy or dry
    if m["itdg_ms"] is not None:
        s -= min(20.0, max(0.0, m["itdg_ms"] - 35) * 0.5)  # a long gap before the room answers
    s += min(m["lateral_fraction"], 0.30) * 40 - 6        # envelopment: LF 0.15 is neutral
    s -= max(0.0, m["reverb_vs_direct_db"] - 10) * 1.5    # the room swamps the voice: distant
    s -= max(0.0, -m["voice_over_pit_db"] - 2) * 3       # the pit covers the voice
    if m["seat_dip"]:
        s -= 6
    if m["direct_path_blocked"]:
        s -= 15
    return max(0.0, min(100.0, s))

#!/usr/bin/env python3
"""Generate data/seats.json and data/seats.csv from the seat inventory and
house geometry, then inject the data into web/index.html.

Coordinate frame (feet): x across the house (+ = even / Carriage Lobby side),
y up (0 = orchestra floor at row A), z toward the rear (0 = curtain line).

House topology (calibrated against the War Memorial virtual tour and SF Opera
seat photos, see sources/CALIBRATION.md):
  orchestra  -> rear rows under the box ring
  boxes      -> horseshoe ring; rear boxes under the Grand Tier
  lower tier -> Grand Tier AA-EE, cross-aisle, Dress Circle A-L: one slab;
                the Balcony lip lands over Dress Circle row A
  upper tier -> Balcony Circle AA-EE + Balcony A-L, one open tier under the dome

Run:  python3 scripts/build_seats.py
"""
import csv
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "data"))
import seating_spec as S  # noqa: E402

with open(os.path.join(ROOT, "data", "house_geometry.json")) as f:
    G = json.load(f)

def P(*path):
    node = G
    for k in path:
        node = node[k]
    return node["value"]

# ----------------------------------------------------------------- geometry
SEAT_W = P("seating", "seat_width_ft")
BAL_SEAT_W = P("seating", "balcony_seat_width_ft")
PITCH = P("seating", "row_pitch_ft")
TIER_PITCH = P("seating", "tier_row_pitch_ft")
AISLE = P("seating", "aisle_width_ft")
CENTER_HALF = P("seating", "center_aisle_half_ft")
CROSS = P("seating", "cross_aisle_ft")
EYE = P("seating", "eye_height_seated_ft")

STAGE_Y = P("published", "stage_height_above_house_ft")
PROSC_W = P("published", "proscenium_width_ft")
PROSC_H = P("published", "proscenium_valence_height_ft")
PIT_FRONT_Z = P("published", "curtain_to_pit_apron_ft")
PIT_BACK_Z = PIT_FRONT_Z + P("published", "pit_depth_at_centerline_ft")
PIT_FLOOR_Y = STAGE_Y - P("published", "pit_floor_below_stage_ft")
PIT_RAIL_Y = P("orchestra", "pit_rail_height_ft")
CEILING_Y = P("published", "auditorium_height_ft")
HALF_BREADTH = P("published", "auditorium_breadth_ft") / 2

ORCH_A_Z = P("orchestra", "row_a_z_ft")
ORCH_RISE = P("orchestra", "rise_total_ft")
ORCH_EXP = P("orchestra", "rise_exponent")
ORCH_CC = P("orchestra", "curve_center_z_ft")

BOX_Y = P("boxes", "floor_y_ft")
BOX_RX = P("boxes", "rail_radius_x_ft")
BOX_RZ = P("boxes", "rail_radius_z_ft")
BOX_CZ = P("boxes", "ring_center_z_ft")
BOX_LEG_FRONT = P("boxes", "leg_front_z_ft")
BOX_PITCH = P("seating", "box_row_pitch_ft")
BOX_SOFFIT = BOX_Y - P("boxes", "soffit_drop_ft")
BOX_SOFFIT_LEGS = P("boxes", "soffit_at_legs_ft")
BOX_LEG_INNER_X = P("boxes", "leg_inner_x_ft")
SLIP_INNER_X = P("lower_tier", "side_slip_inner_x_ft")
SLIP_FRONT_Z = P("lower_tier", "side_slip_front_z_ft")
SLIP_SOFFIT = P("lower_tier", "side_slip_floor_y_ft") - P("lower_tier", "soffit_drop_ft")

SINGER = (0.0, STAGE_Y + P("stage_picture", "singer_mouth_height_above_stage_ft"),
          P("stage_picture", "singer_z_ft"))
PIT_SRC = (0.0, PIT_FLOOR_Y + 3.5, P("stage_picture", "pit_source_z_ft"))
PROSC_TOP = (0.0, STAGE_Y + PROSC_H, 0.0)
UPSTAGE_Z = P("stage_picture", "upstage_reference_z_ft")

# ------------------------------------------------------------- floor curves
def orch_row_z(zc, x):
    r = zc - ORCH_CC
    return ORCH_CC + math.sqrt(max(r * r - x * x, 0.0))

def orch_floor_y(z):
    span = (len(S.ORCH_ROWS) - 1) * PITCH
    t = max(0.0, min(1.0, (z - ORCH_A_Z) / span))
    return ORCH_RISE * t ** ORCH_EXP

CURVES = G["plan_curves"]
RING = CURVES["box_ring_rail"]["value"]
GT_FRONT = CURVES["grand_tier_front"]["value"]
BAL_FRONT = CURVES["balcony_front"]["value"]
BAL_SWEEP = CURVES["balcony_sweep"]["value"]   # [z, |x|, floor_y], front to rear order irrelevant

def interp_by_x(curve, x):
    """z on a symmetric front curve given lateral position x (clamped)."""
    ax = abs(x)
    if ax <= curve[0][0]:
        return curve[0][1]
    for (x0, z0), (x1, z1) in zip(curve, curve[1:]):
        if ax <= x1:
            return z0 + (z1 - z0) * (ax - x0) / (x1 - x0)
    return curve[-1][1]

def interp_by_z(curve3, z):
    """(|x|, floor_y) on the balcony sweep at depth z, or None outside it."""
    pts = sorted(curve3)
    if z < pts[0][0] or z > pts[-1][0]:
        return None
    for (z0, x0, y0), (z1, x1, y1) in zip(pts, pts[1:]):
        if z <= z1:
            t = (z - z0) / (z1 - z0)
            return x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
    return None

def crescent_end(curve):
    """|x| where the front stops being a crescent and turns into the side slip
    (first point where z drops by more than 5 ft between samples)."""
    for (x0, z0), (x1, z1) in zip(curve, curve[1:]):
        if z0 - z1 > 5:
            return x0
    return curve[-1][0]

class Tier:
    """A raked slab behind a front curve F(x) (plan_curves). rows = list of
    (z_center, floor_y); row i runs along z = F(x) + (z_center - F(0))."""
    def __init__(self, name, front, rows, soffit_lip_y, slope):
        self.name, self.front, self.rows = name, front, rows
        self.soffit_lip_y, self.slope = soffit_lip_y, slope
        self.rail_z = front[0][1]
        self.x_end = crescent_end(front)
        self.lip_ahead = 0.0
    def lip_z(self, x):
        return interp_by_x(self.front, x)
    def row_z(self, z_center, x):
        return self.lip_z(min(abs(x), self.x_end)) + (z_center - self.rail_z)
    def floor_at(self, z):
        if z <= self.rows[0][0]:
            return self.rows[0][1]
        for (z0, y0), (z1, y1) in zip(self.rows, self.rows[1:]):
            if z <= z1:
                return y0 + (y1 - y0) * (z - z0) / (z1 - z0)
        return self.rows[-1][1]

def make_tiers():
    tiers = {}
    L = G["lower_tier"]
    rz, off = GT_FRONT[0][1], L["first_row_offset_ft"]["value"]
    y0, r1, r2 = L["floor_y_ft"]["value"], L["grand_tier_rise_per_row_ft"]["value"], L["dress_circle_rise_per_row_ft"]["value"]
    rows = [(rz + off + i * TIER_PITCH, y0 + i * r1) for i in range(5)]
    base_z, base_y = rows[-1][0] + CROSS + TIER_PITCH, rows[-1][1] + L["cross_aisle_rise_ft"]["value"]
    rows += [(base_z + j * TIER_PITCH, base_y + j * r2) for j in range(11)]
    tiers["lower_tier"] = Tier("lower_tier", GT_FRONT, rows, y0 - L["soffit_drop_ft"]["value"], r1 / TIER_PITCH)
    tiers["lower_tier"].lip_ahead = L["soffit_lip_ahead_of_rail_ft"]["value"]
    u = G["upper_tier"]
    rz, off = BAL_FRONT[0][1], u["first_row_offset_ft"]["value"]
    y0, r1, r2 = u["floor_y_ft"]["value"], u["balcony_circle_rise_per_row_ft"]["value"], u["balcony_rise_per_row_ft"]["value"]
    rows = [(rz + off + i * TIER_PITCH, y0 + i * r1) for i in range(5)]
    base_z, base_y = rows[-1][0] + CROSS + TIER_PITCH, rows[-1][1] + u["cross_aisle_rise_ft"]["value"]
    rows += [(base_z + j * TIER_PITCH, base_y + j * r2) for j in range(11)]
    tiers["upper_tier"] = Tier("upper_tier", BAL_FRONT, rows, y0 - u["soffit_drop_ft"]["value"], r1 / TIER_PITCH)
    return tiers

TIERS = make_tiers()

def arc_point(center_z, radius, s):
    phi = s / radius
    return radius * math.sin(phi), center_z + radius * math.cos(phi)

# ----------------------------------------------------------- overhang model
# Each overhang is a region of the plan with a soffit height that can vary
# with position. The box ring is a horseshoe: an elliptical rear arc plus two
# legs along the side walls up to the proscenium. The Grand Tier slab has the
# same shape: a nearly straight crescent across the house plus side slips
# along the walls. The Balcony is a crescent only (its floor edge along the
# walls rises toward the rear and does not overhang anything in front of the
# rail). Sightlines are ray-marched in plan against these regions.
def box_ring_lip_z(x):
    """z of the ring's rail (rear arc + legs) at lateral position x."""
    return interp_by_x(RING, x)

def box_floor_at(z):
    return BOX_Y + 0.5 * min(2, max(0, (z - RING[0][1]) / BOX_PITCH))

def lower_lip_z(x):
    t = TIERS["lower_tier"]
    return t.lip_z(x) - (t.lip_ahead if abs(x) < t.x_end else 0.0)

class Overhang:
    def __init__(self, name, contains, soffit, floor_below):
        self.name, self.contains, self.soffit, self.floor_below = name, contains, soffit, floor_below

def _box_contains(x, z):
    return z > box_ring_lip_z(x)

def _box_soffit(x, z):
    f = min(1.0, abs(x) / RING[-1][0])
    return BOX_SOFFIT + (BOX_SOFFIT_LEGS - BOX_SOFFIT) * f

def _lower_contains(x, z):
    return z > lower_lip_z(x)

def _lower_soffit(x, z):
    t = TIERS["lower_tier"]
    if abs(x) >= t.x_end:
        return SLIP_SOFFIT
    return t.soffit_lip_y + t.slope * (z - lower_lip_z(x))

def _sweep(x, z):
    sw = interp_by_z(BAL_SWEEP, z)
    if sw is None:
        return None
    sx, fy = sw
    return fy if abs(x) > sx else None

def _upper_contains(x, z):
    t = TIERS["upper_tier"]
    if abs(x) <= t.x_end and z > t.lip_z(x):
        return True
    return _sweep(x, z) is not None

def _upper_soffit(x, z):
    t = TIERS["upper_tier"]
    fy = _sweep(x, z)
    if abs(x) <= t.x_end and z > t.lip_z(x):
        return t.soffit_lip_y + t.slope * (z - t.lip_z(x))
    return fy - G["upper_tier"]["soffit_drop_ft"]["value"]

OVERHANGS = [
    Overhang("boxes", _box_contains, _box_soffit, lambda x, z: orch_floor_y(z)),
    Overhang("grand_tier", _lower_contains, _lower_soffit,
             lambda x, z: box_floor_at(z) if _box_contains(x, z) else orch_floor_y(z)),
    Overhang("upper_tier", _upper_contains, _upper_soffit,
             lambda x, z: TIERS["lower_tier"].floor_at(z)),
]

def lowest_over(x, z, y_eye=None):
    """(overhang, soffit) with the lowest soffit over the point, or None."""
    best = None
    for o in OVERHANGS:
        if not o.contains(x, z):
            continue
        sy = o.soffit(x, z)
        if y_eye is not None and sy <= y_eye + 0.5:
            continue
        if best is None or sy < best[1]:
            best = (o, sy)
    return best

STEP_FT = 0.5

def overhang_for(x, y_eye, z, target=None):
    """Lowest overhang over the eye, with the lip taken where the eye-to-
    target ray (default: the singer) leaves that overhang's region in plan."""
    here = lowest_over(x, z, y_eye)
    if here is None:
        return None
    o, soffit_here = here
    tx, tz = (SINGER[0], SINGER[2]) if target is None else (target[0], target[2])
    dx, dz = tx - x, tz - z
    length = math.hypot(dx, dz)
    n = max(1, int(length / STEP_FT))
    lx, lz = x, z
    for k in range(1, n + 1):
        px, pz = x + dx * k / n, z + dz * k / n
        if not o.contains(px, pz):
            break
        lx, lz = px, pz
    depth = math.hypot(lx - x, lz - z)
    lip_y = o.soffit(lx, lz)
    return {"name": o.name, "lip_x": lx, "lip_z": lz, "lip_y": lip_y,
            "soffit_here": soffit_here,
            "opening_h": lip_y - o.floor_below(lx, lz), "depth": depth}

def ray_blocked(eye, target):
    """True if the straight line from eye to target rises through the soffit
    of an overhang the eye sits under. Overhangs the eye is not under (its own
    tier's slab, tiers below it) cannot block a ray toward the stage."""
    cands = [o for o in OVERHANGS
             if o.contains(eye[0], eye[2]) and eye[1] < o.soffit(eye[0], eye[2])]
    if not cands:
        return False
    dx, dy, dz = target[0] - eye[0], target[1] - eye[1], target[2] - eye[2]
    length = math.hypot(dx, dz)
    n = max(1, int(length / STEP_FT))
    for k in range(1, n + 1):
        t = k / n
        px, py, pz = eye[0] + dx * t, eye[1] + dy * t, eye[2] + dz * t
        for o in cands:
            if o.contains(px, pz) and py >= o.soffit(px, pz):
                return True
    return False

def ray_clears_lip(eye, target, oh=None):
    return not ray_blocked(eye, target)

# ----------------------------------------------------------------- metrics
def elev(from_pt, to_pt):
    dx = to_pt[0] - from_pt[0]
    dy = to_pt[1] - from_pt[1]
    dz = to_pt[2] - from_pt[2]
    return math.degrees(math.atan2(dy, math.hypot(dx, dz)))

def dist(a, b):
    return math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(3)))

def ray_clears_lip(eye, target, oh):
    if oh is None:
        return True
    zl = oh["lip_z"]
    if (eye[2] - zl) * (target[2] - zl) >= 0:
        return True
    t = (zl - eye[2]) / (target[2] - eye[2])
    y_at_lip = eye[1] + t * (target[1] - eye[1])
    return y_at_lip < oh["lip_y"]

def pit_visible_fraction(eye):
    n, seen = 12, 0
    for k in range(n):
        z = PIT_FRONT_Z + (k + 0.5) / n * (PIT_BACK_Z - PIT_FRONT_Z)
        target = (eye[0] * 0.3, PIT_FLOOR_Y + 2.0, z)
        if eye[2] <= PIT_BACK_Z:
            continue
        t = (PIT_BACK_Z - eye[2]) / (target[2] - eye[2])
        y_at_rail = eye[1] + t * (target[1] - eye[1])
        if y_at_rail > PIT_RAIL_Y:
            seen += 1
    return seen / n

def stage_width_fraction(eye):
    ex, ez = eye[0], eye[2]
    half = PROSC_W / 2
    def x_at_upstage(edge_x):
        t = (UPSTAGE_Z - ez) / (0.0 - ez)
        return ex + t * (edge_x - ex)
    lo, hi = sorted((x_at_upstage(-half), x_at_upstage(half)))
    lo, hi = max(lo, -half), min(hi, half)
    return max(0.0, (hi - lo) / PROSC_W)

def ceiling_reflection_ok(eye, src):
    img = (src[0], 2 * CEILING_Y - src[1], src[2])
    t = (CEILING_Y - img[1]) / (eye[1] - img[1])
    refl = (img[0] + t * (eye[0] - img[0]), CEILING_Y, img[2] + t * (eye[2] - img[2]))
    return (not ray_blocked(eye, refl)) and refl[2] > 0

def view_score(m):
    """0-100 experience score. Weights are opinions; see README."""
    d = m["dist_singer_ft"]
    s = 100 - max(0.0, d - 35) * (60 / 125)
    s -= max(0.0, m["horiz_angle_deg"] - 15) * 1.0
    s -= (1.0 - m["stage_width_visible"]) * 60
    if m["overhang"] != "none":
        s -= max(0.0, 25 - m["opening_angle_deg"]) * 1.0
        s -= (PROSC_H - m["visible_prosc_height_ft"]) * 2
        s -= max(0.0, 6 - m["headroom_ft"]) * 2.0      # a ceiling right over your head
        if not m["ceiling_reflection_singer"]:
            s -= 6
    s += m["pit_visible"] * 8
    if m["elev_to_singer_deg"] < -30:
        s -= (-30 - m["elev_to_singer_deg"]) * 0.8
    return max(0.0, min(100.0, s))

def metrics(eye):
    m = {}
    m["dist_singer_ft"] = round(dist(eye, SINGER), 1)
    m["dist_pit_ft"] = round(dist(eye, PIT_SRC), 1)
    m["horiz_angle_deg"] = round(math.degrees(math.atan2(abs(eye[0]), eye[2] - SINGER[2])), 1)
    m["elev_to_singer_deg"] = round(elev(eye, SINGER), 1)
    m["elev_to_prosc_top_deg"] = round(elev(eye, PROSC_TOP), 1)
    oh = overhang_for(eye[0], eye[1], eye[2])
    if oh:
        lip_e = elev(eye, (oh["lip_x"], oh["lip_y"], oh["lip_z"]))
        m["overhang"] = oh["name"]
        m["overhang_depth_ft"] = round(oh["depth"], 1)
        m["overhang_opening_ft"] = round(oh["opening_h"], 1)
        m["overhang_d_over_h"] = round(oh["depth"] / max(oh["opening_h"], 0.1), 2)
        m["headroom_ft"] = round(oh["soffit_here"] - eye[1], 1)
        m["lip_elev_deg"] = round(lip_e, 1)
        m["opening_angle_deg"] = round(lip_e - m["elev_to_singer_deg"], 1)
        clipped = ray_blocked(eye, PROSC_TOP)
        m["prosc_top_clipped"] = clipped
        if clipped:
            # highest visible point on the proscenium plane: the ray through the lip edge
            oh2 = overhang_for(eye[0], eye[1], eye[2], PROSC_TOP) or oh
            t = (0.0 - eye[2]) / (oh2["lip_z"] - eye[2]) if oh2["lip_z"] != eye[2] else 0.0
            y_on_prosc = eye[1] + t * (oh2["lip_y"] - eye[1])
            m["visible_prosc_height_ft"] = round(max(0.0, min(PROSC_H, y_on_prosc - STAGE_Y)), 1)
        else:
            m["visible_prosc_height_ft"] = PROSC_H
    else:
        m["overhang"] = "none"
        m["overhang_depth_ft"] = 0.0
        m["overhang_opening_ft"] = None
        m["overhang_d_over_h"] = 0.0
        m["headroom_ft"] = round(CEILING_Y - eye[1], 1)
        m["lip_elev_deg"] = None
        m["opening_angle_deg"] = round(90.0 - m["elev_to_singer_deg"], 1)
        m["prosc_top_clipped"] = False
        m["visible_prosc_height_ft"] = PROSC_H
    m["pit_visible"] = round(pit_visible_fraction(eye), 2)
    m["stage_width_visible"] = round(stage_width_fraction(eye), 2)
    m["ceiling_reflection_singer"] = ceiling_reflection_ok(eye, SINGER)
    m["ceiling_reflection_pit"] = ceiling_reflection_ok(eye, PIT_SRC)
    ref = dist((0.0, EYE, ORCH_A_Z), SINGER)
    m["direct_level_db"] = round(20 * math.log10(ref / m["dist_singer_ft"]), 1)
    m["score"] = round(view_score(m), 1)
    return m

# ------------------------------------------------------------ seat placing
seats = []

def add(level, section, row, number, x, floor_y, z, zone, flags=None):
    eye = (x, floor_y + EYE, z)
    rec = {
        "id": f"{level}:{row}:{number}",
        "level": level, "section": section, "row": row, "seat": number,
        "zone": zone, "zone_name": S.ZONES[zone], "price": S.ZONE_PRICES[zone],
        "x": round(x, 2), "y": round(eye[1], 2), "z": round(z, 2),
        "floor_y": round(floor_y, 2),
    }
    if flags:
        rec["flags"] = flags
    rec.update(metrics(eye))
    seats.append(rec)

def lateral_center_split(n, w):
    k = (n - 101) // 2
    s = (k + 0.5) * w
    return -s if n % 2 else s

def lateral_center_consecutive(n, count, w):
    return (n - 101 - (count - 1) / 2) * w

def lateral_side(n, inner_edge, w):
    k = (n - 1) // 2
    s = inner_edge + (k + 0.5) * w
    return -s if n % 2 else s

def lateral_far(n, first, inner_edge, w):
    k = (n - first) // 2
    s = inner_edge + (k + 0.5) * w
    return -s if n % 2 else s

def place_orchestra():
    radius0 = ORCH_A_Z - ORCH_CC
    side_edge = CENTER_HALF + 12 * SEAT_W + AISLE
    for row in S.orchestra_rows():
        i = row["index"]
        zc = ORCH_A_Z + i * PITCH
        radius = radius0 + i * PITCH
        floor_y = orch_floor_y(zc)
        for block, nums in row["blocks"].items():
            for n in nums:
                if block.startswith("center"):
                    k = (n - 101) // 2
                    s = CENTER_HALF + (k + 0.5) * SEAT_W
                    s = -s if n % 2 else s
                else:
                    s = lateral_side(n, side_edge, SEAT_W)
                x, z = arc_point(ORCH_CC, radius, s)
                flags = ["accessible-row"] if row["row"] == "ZZ" else None
                if block.startswith("platform"):
                    flags = ["wheelchair-platform"]
                add("orchestra", block, row["row"], n, x, floor_y, z,
                    S.orchestra_zone(row["row"], block, n), flags)

def ring_path():
    """Full ring rail as a polyline from the left proscenium end round the
    rear to the right end: [(x, z)], plus cumulative lengths."""
    left = [(-x, z) for x, z in reversed(RING)]
    right = [(x, z) for x, z in RING[1:]]
    pts = left + right
    cum = [0.0]
    for (x0, z0), (x1, z1) in zip(pts, pts[1:]):
        cum.append(cum[-1] + math.hypot(x1 - x0, z1 - z0))
    return pts, cum

RING_PATH, RING_CUM = ring_path()

def box_path_point(t):
    """Point on the ring rail at fraction t of its length, with the outward
    (away from the void) unit normal."""
    d = t * RING_CUM[-1]
    for k, (c0, c1) in enumerate(zip(RING_CUM, RING_CUM[1:])):
        if d <= c1 or k == len(RING_CUM) - 2:
            (x0, z0), (x1, z1) = RING_PATH[k], RING_PATH[k + 1]
            u = 0.0 if c1 == c0 else (d - c0) / (c1 - c0)
            x, z = x0 + (x1 - x0) * u, z0 + (z1 - z0) * u
            tx, tz = x1 - x0, z1 - z0
            ln = math.hypot(tx, tz) or 1.0
            nx, nz = tz / ln, -tx / ln          # left-hand normal of the travel direction
            if nx * x + nz * (z - 60) < 0:      # point it away from the house centre
                nx, nz = -nx, -nz
            return x, z, (nx, nz)
    return RING_PATH[-1][0], RING_PATH[-1][1], (1.0, 0.0)

def place_boxes():
    nb = len(S.BOX_LETTERS)
    layout = {1: (0, -1), 2: (0, 0), 3: (0, 1), 4: (1, 1), 5: (1, 0), 6: (1, -1),
              7: (2, -0.9), 8: (2, 0.9)}
    for k, letter in enumerate(S.BOX_LETTERS):
        zone = "CTRBOX" if letter in S.CENTER_BOXES else "BOX"
        x0, z0, (nx, nz) = box_path_point((k + 0.5) / nb)
        tx, tz = -nz, nx
        for n in range(1, S.BOX_SEATS[letter] + 1):
            r, c = layout[n]
            depth = 1.5 + r * BOX_PITCH
            x = x0 + nx * depth + tx * c * 1.9
            z = z0 + nz * depth + tz * c * 1.9
            add("boxes", "center_box" if zone == "CTRBOX" else "side_box",
                letter, n, x, BOX_Y + r * 0.5, z, zone)

def place_tier_rows(level, tier, rows_spec, row_index_offset, w, layout):
    for row in rows_spec:
        i = row["index"] + row_index_offset
        zc, floor_y = tier.rows[i]
        for block, nums in row["blocks"].items():
            for n in nums:
                s = layout(block, n, len(nums), w)
                x, z = s, tier.row_z(zc, s)
                flags = ["accessible-row"] if (level == "dress_circle" and row["row"] == "L") else None
                add(level, block, row["row"], n, x, floor_y, z, ZONE_FN[level](row["row"], block, n), flags)

ZONE_FN = {
    "grand_tier": lambda r, b, n: S.grand_tier_zone(b, n),
    "dress_circle": S.dress_circle_zone,
    "balcony_circle": lambda r, b, n: S.balcony_circle_zone(b, n),
    "balcony": S.balcony_zone,
}

def layout_gt(block, n, count, w):
    if block == "center":
        return lateral_center_consecutive(n, count, w)
    if block.startswith("side"):
        return lateral_side(n, 7 * w + AISLE, w)
    return lateral_far(n, 29, 7 * w + AISLE + 14 * w + AISLE, w)

def layout_dc(block, n, count, w):
    if block.startswith("center"):
        return lateral_center_split(n, w)
    return lateral_side(n, 14 * w + AISLE, w)

def layout_bc(block, n, count, w):
    if block == "center":
        return lateral_center_consecutive(n, count, w)
    if block.startswith("side"):
        return lateral_side(n, 7 * w + AISLE, w)
    return lateral_far(n, 25, 7 * w + AISLE + 12 * w + AISLE, w)

def layout_bal(block, n, count, w):
    if block.startswith("center"):
        return lateral_center_split(n, w)
    if block.startswith("side"):
        return lateral_side(n, 14 * w + AISLE, w)
    return lateral_far(n, 21, 14 * w + AISLE + 10 * w + AISLE, w)

place_orchestra()
place_boxes()
place_tier_rows("grand_tier", TIERS["lower_tier"], S.grand_tier_rows(), 0, SEAT_W, layout_gt)
place_tier_rows("dress_circle", TIERS["lower_tier"], S.dress_circle_rows(), 5, SEAT_W, layout_dc)
place_tier_rows("balcony_circle", TIERS["upper_tier"], S.balcony_circle_rows(), 0, SEAT_W, layout_bc)
place_tier_rows("balcony", TIERS["upper_tier"], S.balcony_rows(), 5, BAL_SEAT_W, layout_bal)

# ------------------------------------------------------------ house shell
def front_polyline(curve, x_max, n=40):
    """Mirrored polyline of a front curve out to |x| = x_max."""
    pts = []
    for k in range(n + 1):
        x = -x_max + 2 * x_max * k / n
        pts.append([round(x, 2), round(interp_by_x(curve, x), 2)])
    return pts

def tier_shell(tier, half_w):
    xe = min(tier.x_end, half_w)
    rows = [{"z": round(z, 2), "y": round(y, 2),
             "arc": [[x, round(zz + (z - tier.rail_z), 2)] for x, zz in front_polyline(tier.front, xe)]}
            for z, y in tier.rows]
    rail = {"z": round(tier.rail_z, 2), "y": round(tier.rows[0][1], 2), "arc": front_polyline(tier.front, xe)}
    full = front_polyline(tier.front, tier.front[-1][0], 80)
    return {"name": tier.name, "rows": rows, "rail": rail, "front": full,
            "soffit_lip_y": tier.soffit_lip_y, "x_end": xe}

shell = {
    "ceiling_y": CEILING_Y,
    "half_breadth": HALF_BREADTH,
    "depth_orchestra": P("published", "depth_orchestra_level_ft"),
    "depth_balcony": P("published", "depth_balcony_level_ft"),
    "stage": {"y": STAGE_Y, "prosc_w": PROSC_W, "prosc_h": PROSC_H,
              "back_wall_z": -P("published", "curtain_to_back_wall_ft"),
              "singer": SINGER, "rock_h": P("stage_picture", "walkure_rock_top_height_above_stage_ft")},
    "pit": {"front_z": PIT_FRONT_Z, "back_z": PIT_BACK_Z, "floor_y": PIT_FLOOR_Y,
            "rail_y": PIT_RAIL_Y, "half_w": PROSC_W / 2 + 4, "source": PIT_SRC},
    "orchestra": {"rows": [{"z": round(ORCH_A_Z + i * PITCH, 2),
                             "y": round(orch_floor_y(ORCH_A_Z + i * PITCH), 2),
                             "arc": [[round(x, 2), round(orch_row_z(ORCH_A_Z + i * PITCH, x), 2)]
                                     for x in [-48 + 96 * k / 24 for k in range(25)]]}
                            for i in range(len(S.ORCH_ROWS))]},
    "boxes": {"floor_y": BOX_Y, "soffit_y": BOX_SOFFIT,
              "rail": [[round(v, 2) for v in box_path_point(t / 60)[:2]] for t in range(61)],
              "outer": [[round(box_path_point(t / 60)[0] + box_path_point(t / 60)[2][0] * 9, 2),
                         round(box_path_point(t / 60)[1] + box_path_point(t / 60)[2][1] * 9, 2)] for t in range(61)]},
    "tiers": [tier_shell(TIERS["lower_tier"], 54), tier_shell(TIERS["upper_tier"], 56)],
    "side_slips": {"inner_x": TIERS["lower_tier"].x_end, "front_z": GT_FRONT[-1][1],
                   "path": front_polyline(GT_FRONT, GT_FRONT[-1][0], 80),
                   "floor_y": P("lower_tier", "side_slip_floor_y_ft"), "soffit_y": SLIP_SOFFIT},
    "balcony_sweep": {"path": [[round(x, 2), round(z, 2), round(y, 2)] for z, x, y in sorted(BAL_SWEEP)],
                      "soffit_drop": P("upper_tier", "soffit_drop_ft")},
}

# ------------------------------------------------------------------ output
out = {
    "generated_from": ["data/house_geometry.json", "data/seating_spec.py"],
    "zones": S.ZONES, "zone_prices": S.ZONE_PRICES,
    "shell": shell, "seats": seats,
}
with open(os.path.join(ROOT, "data", "seats.json"), "w") as f:
    json.dump(out, f, separators=(",", ":"))

fields = ["id", "level", "section", "row", "seat", "zone", "price", "x", "y", "z",
          "dist_singer_ft", "dist_pit_ft", "horiz_angle_deg", "elev_to_singer_deg",
          "overhang", "overhang_depth_ft", "overhang_opening_ft", "overhang_d_over_h",
          "headroom_ft", "opening_angle_deg", "prosc_top_clipped", "visible_prosc_height_ft",
          "pit_visible", "stage_width_visible", "ceiling_reflection_singer",
          "ceiling_reflection_pit", "direct_level_db", "score"]
with open(os.path.join(ROOT, "data", "seats.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
    w.writeheader()
    for s in seats:
        w.writerow(s)

tpl_path = os.path.join(ROOT, "web", "template.html")
if os.path.exists(tpl_path):
    with open(tpl_path) as f:
        html = f.read()
    html = html.replace("/*__SEATS_JSON__*/null", json.dumps(out, separators=(",", ":")))
    with open(os.path.join(ROOT, "web", "index.html"), "w") as f:
        f.write(html)

# ----------------------------------------------------------------- summary
from collections import Counter
by_level = Counter(s["level"] for s in seats)
print("seats per level:", dict(by_level), "total", len(seats))
under = Counter((s["level"], s["overhang"]) for s in seats)
for k in sorted(under):
    print(f"  {k[0]:15s} {k[1]:13s} {under[k]}")

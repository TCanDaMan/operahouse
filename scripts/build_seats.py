#!/usr/bin/env python3
"""Generate data/seats.json and data/seats.csv from the seat inventory and
house geometry, then inject the data into web/index.html.

Coordinate frame (feet): x across the house (+ = even / Carriage Lobby side),
y up (0 = orchestra floor at row A), z toward the rear (0 = curtain line).

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

LT_FRONT_Z = P("lower_tier", "front_z_ft")
LT_CC = P("lower_tier", "curve_center_z_ft")
LT_FRONT_Y = P("lower_tier", "front_y_ft")
LT_GT_RISE = P("lower_tier", "grand_tier_rise_per_row_ft")
LT_AISLE_Y = P("lower_tier", "cross_aisle_y_ft")
LT_DC_RISE = P("lower_tier", "dress_circle_rise_per_row_ft")
LT_SOFFIT_DROP = P("lower_tier", "soffit_drop_ft")

UT_FRONT_Z = P("upper_tier", "front_z_ft")
UT_CC = P("upper_tier", "curve_center_z_ft")
UT_FRONT_Y = P("upper_tier", "front_y_ft")
UT_BC_RISE = P("upper_tier", "balcony_circle_rise_per_row_ft")
UT_AISLE_Y = P("upper_tier", "cross_aisle_y_ft")
UT_BAL_RISE = P("upper_tier", "balcony_rise_per_row_ft")
UT_SOFFIT_DROP = P("upper_tier", "soffit_drop_ft")

SINGER = (0.0, STAGE_Y + P("stage_picture", "singer_mouth_height_above_stage_ft"),
          P("stage_picture", "singer_z_ft"))
PIT_SRC = (0.0, PIT_FLOOR_Y + 3.5, P("stage_picture", "pit_source_z_ft"))
PROSC_TOP = (0.0, STAGE_Y + PROSC_H, 0.0)
UPSTAGE_Z = P("stage_picture", "upstage_reference_z_ft")

# ------------------------------------------------------------- floor curves
def orch_floor_y(z):
    span = (len(S.ORCH_ROWS) - 1) * PITCH
    t = max(0.0, min(1.0, (z - ORCH_A_Z) / span))
    return ORCH_RISE * t ** ORCH_EXP

def lower_tier_row(i):
    """(z at center, floor y) for lower-tier row index i (0..15)."""
    if i < 5:
        return LT_FRONT_Z + i * TIER_PITCH, LT_FRONT_Y + i * LT_GT_RISE
    j = i - 5
    return LT_FRONT_Z + 5 * TIER_PITCH + CROSS + j * TIER_PITCH, \
        LT_AISLE_Y + 1.5 + j * LT_DC_RISE

def upper_tier_row(i):
    if i < 5:
        return UT_FRONT_Z + i * TIER_PITCH, UT_FRONT_Y + i * UT_BC_RISE
    j = i - 5
    return UT_FRONT_Z + 5 * TIER_PITCH + CROSS + j * TIER_PITCH, \
        UT_AISLE_Y + 2.0 + j * UT_BAL_RISE

def arc_point(center_z, radius, s):
    """Point on an arc of given radius centred on the axis at z=center_z,
    s = lateral distance along the arc (signed)."""
    phi = s / radius
    return radius * math.sin(phi), center_z + radius * math.cos(phi)

# ----------------------------------------------------------- overhang model
# Each overhang: lip z as a function of x (arc), soffit y at the lip, and the
# soffit slope going rearward (follows the tier rake).
def lip_z_arc(center_z, radius, x):
    x = max(-radius + 0.1, min(radius - 0.1, x))
    return center_z + math.sqrt(radius * radius - x * x)

def box_ring_lip_z(x):
    # rear half-ellipse of the box rail
    if abs(x) >= BOX_RX:
        return None
    return BOX_CZ + BOX_RZ * math.sqrt(1 - (x / BOX_RX) ** 2)

OVERHANGS = [
    # name, lip_z(x), soffit_y_at_lip, slope (ft per ft rearward), floor_under_lip(x)
    {"name": "boxes",
     "lip_z": box_ring_lip_z, "soffit_y": BOX_SOFFIT, "slope": 0.0,
     "floor_at_lip": lambda x: orch_floor_y(box_ring_lip_z(x) or 0)},
    {"name": "lower_tier",
     "lip_z": lambda x: lip_z_arc(LT_CC, LT_FRONT_Z - LT_CC, x),
     "soffit_y": LT_FRONT_Y - LT_SOFFIT_DROP,
     "slope": LT_GT_RISE / TIER_PITCH,
     "floor_at_lip": lambda x: max(orch_floor_y(lip_z_arc(LT_CC, LT_FRONT_Z - LT_CC, x)), BOX_Y if abs(x) < 50 else 0)},
    {"name": "upper_tier",
     "lip_z": lambda x: lip_z_arc(UT_CC, UT_FRONT_Z - UT_CC, x),
     "soffit_y": UT_FRONT_Y - UT_SOFFIT_DROP,
     "slope": UT_BC_RISE / TIER_PITCH,
     "floor_at_lip": lambda x: lower_tier_row(2)[1]},
]

def overhang_for(x, y_eye, z):
    """Lowest overhang whose lip is in front of the seat and whose soffit is
    above the eye. Returns dict or None."""
    best = None
    for o in OVERHANGS:
        lz = o["lip_z"](x)
        if lz is None or z <= lz:
            continue
        soffit_here = o["soffit_y"] + o["slope"] * (z - lz)
        if soffit_here <= y_eye + 0.5:
            continue  # this overhang is below us (we sit on it)
        if best is None or o["soffit_y"] < best["lip_y"]:
            best = {"name": o["name"], "lip_z": lz, "lip_y": o["soffit_y"],
                    "soffit_here": soffit_here,
                    "opening_h": o["soffit_y"] - o["floor_at_lip"](x),
                    "depth": z - lz}
    return best

# ----------------------------------------------------------------- metrics
def elev(from_pt, to_pt):
    dx = to_pt[0] - from_pt[0]
    dy = to_pt[1] - from_pt[1]
    dz = to_pt[2] - from_pt[2]
    horiz = math.hypot(dx, dz)
    return math.degrees(math.atan2(dy, horiz))

def dist(a, b):
    return math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(3)))

def ray_clears_lip(eye, target, oh):
    """Does the straight line eye->target pass below the overhang lip?"""
    if oh is None:
        return True
    zl = oh["lip_z"]
    if (eye[2] - zl) * (target[2] - zl) >= 0:
        return True  # both on the same side of the lip
    t = (zl - eye[2]) / (target[2] - eye[2])
    y_at_lip = eye[1] + t * (target[1] - eye[1])
    return y_at_lip < oh["lip_y"]

def pit_visible_fraction(eye):
    """Fraction of the pit floor (front to back at the seat's x) visible over
    the pit rail."""
    n, seen = 12, 0
    for k in range(n):
        z = PIT_FRONT_Z + (k + 0.5) / n * (PIT_BACK_Z - PIT_FRONT_Z)
        target = (eye[0] * 0.3, PIT_FLOOR_Y + 2.0, z)  # music stands
        # rail sits at the rear edge of the pit (audience side)
        if eye[2] <= PIT_BACK_Z:
            continue
        t = (PIT_BACK_Z - eye[2]) / (target[2] - eye[2])
        y_at_rail = eye[1] + t * (target[1] - eye[1])
        if y_at_rail > PIT_RAIL_Y:
            seen += 1
    return seen / n

def stage_width_fraction(eye):
    """How much of the stage width at the upstage reference depth is visible
    through the proscenium opening from this seat (0..1)."""
    ex, ez = eye[0], eye[2]
    half = PROSC_W / 2
    # lines from eye through the proscenium edges, extended to z = UPSTAGE_Z
    def x_at_upstage(edge_x):
        t = (UPSTAGE_Z - ez) / (0.0 - ez)
        return ex + t * (edge_x - ex)
    lo, hi = sorted((x_at_upstage(-half), x_at_upstage(half)))
    lo, hi = max(lo, -half), min(hi, half)
    return max(0.0, (hi - lo) / PROSC_W)

def ceiling_reflection_ok(eye, src):
    """Image-source check: does the first-order ceiling reflection from src
    reach the eye without hitting an overhang?"""
    img = (src[0], 2 * CEILING_Y - src[1], src[2])
    # reflection point on the ceiling
    t = (CEILING_Y - img[1]) / (eye[1] - img[1])
    refl = (img[0] + t * (eye[0] - img[0]), CEILING_Y, img[2] + t * (eye[2] - img[2]))
    oh = overhang_for(eye[0], eye[1], eye[2])
    return ray_clears_lip(eye, refl, oh) and refl[2] > 0

def metrics(eye, floor_y):
    m = {}
    m["dist_singer_ft"] = round(dist(eye, SINGER), 1)
    m["dist_pit_ft"] = round(dist(eye, PIT_SRC), 1)
    m["horiz_angle_deg"] = round(math.degrees(math.atan2(abs(eye[0]), eye[2] - SINGER[2])), 1)
    m["elev_to_singer_deg"] = round(elev(eye, SINGER), 1)
    m["elev_to_prosc_top_deg"] = round(elev(eye, PROSC_TOP), 1)
    oh = overhang_for(eye[0], eye[1], eye[2])
    if oh:
        lip_pt = (eye[0], oh["lip_y"], oh["lip_z"])
        lip_e = elev(eye, lip_pt)
        m["overhang"] = oh["name"]
        m["overhang_depth_ft"] = round(oh["depth"], 1)
        m["overhang_opening_ft"] = round(oh["opening_h"], 1)
        m["overhang_d_over_h"] = round(oh["depth"] / max(oh["opening_h"], 0.1), 2)
        m["headroom_ft"] = round(oh["soffit_here"] - eye[1], 1)
        m["lip_elev_deg"] = round(lip_e, 1)
        m["opening_angle_deg"] = round(lip_e - m["elev_to_singer_deg"], 1)
        clipped = lip_e < m["elev_to_prosc_top_deg"]
        m["prosc_top_clipped"] = clipped
        if clipped:
            # height on the proscenium plane where the lip line lands
            t = (0.0 - eye[2]) / (oh["lip_z"] - eye[2])
            y_on_prosc = eye[1] + t * (oh["lip_y"] - eye[1])
            m["visible_prosc_height_ft"] = round(max(0.0, y_on_prosc - STAGE_Y), 1)
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
    # direct-sound level relative to orchestra row A center (inverse square)
    ref = dist((0.0, EYE, ORCH_A_Z), SINGER)
    m["direct_level_db"] = round(20 * math.log10(ref / m["dist_singer_ft"]), 1)
    m["score"] = round(view_score(m), 1)
    return m

def view_score(m):
    """0-100 experience score. Weights are opinions; see README."""
    d = m["dist_singer_ft"]
    s = 100 - max(0.0, d - 35) * (60 / 125)          # 100 at 35 ft, 40 at 160 ft
    s -= max(0.0, m["horiz_angle_deg"] - 15) * 1.0    # off-axis
    s -= (1.0 - m["stage_width_visible"]) * 60        # proscenium cuts the stage
    if m["overhang"] != "none":
        s -= max(0.0, 25 - m["opening_angle_deg"]) * 1.2   # boxed-in feel under a lip
        s -= (PROSC_H - m["visible_prosc_height_ft"]) * 3   # top of the picture clipped
        if not m["ceiling_reflection_singer"]:
            s -= 6
    s += m["pit_visible"] * 8                         # seeing the players
    if m["elev_to_singer_deg"] > 30:
        s -= (m["elev_to_singer_deg"] - 30) * 0.8     # looking down on heads
    return max(0.0, min(100.0, s))

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
    rec.update(metrics(eye, floor_y))
    seats.append(rec)

def lateral_center_split(n, w):
    """Odd numbers 101.. on the negative side, even 102.. on the positive side,
    meeting at the center line."""
    k = (n - 101) // 2
    s = (k + 0.5) * w
    return -s if n % 2 else s

def lateral_center_consecutive(n, count, w):
    return (n - 101 - (count - 1) / 2) * w

def lateral_side(n, inner_edge, w):
    k = (n - 1) // 2
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
                elif block.startswith("platform"):
                    s = lateral_side(n, side_edge, SEAT_W)
                else:
                    s = lateral_side(n, side_edge, SEAT_W)
                x, z = arc_point(ORCH_CC, radius, s)
                zone = S.orchestra_zone(row["row"], block, n)
                flags = ["accessible-row"] if row["row"] == "ZZ" else None
                if block.startswith("platform"):
                    flags = ["wheelchair-platform"]
                add("orchestra", block, row["row"], n, x, floor_y, z, zone, flags)

def box_path_point(t):
    """t in [0,1] along the ring from Grove-side front (t=0) around the rear
    to Carriage-side front (t=1). Returns (x, z, outward unit vector)."""
    leg = BOX_CZ - BOX_LEG_FRONT
    # approximate half-ellipse perimeter
    a, b = BOX_RX, BOX_RZ
    arc_len = math.pi * (3 * (a + b) - math.sqrt((3 * a + b) * (a + 3 * b))) / 2
    total = 2 * leg + arc_len
    d = t * total
    if d < leg:
        x, z = -BOX_RX, BOX_LEG_FRONT + d
        return x, z, (-1.0, 0.0)
    d -= leg
    if d < arc_len:
        theta = math.pi * (d / arc_len)          # 0 at Grove side, pi at Carriage side
        x = -BOX_RX * math.cos(theta)
        z = BOX_CZ + BOX_RZ * math.sin(theta)
        nx, nz = -math.cos(theta) / BOX_RX, math.sin(theta) / BOX_RZ
        ln = math.hypot(nx, nz)
        return x, z, (nx / ln, nz / ln)
    d -= arc_len
    x, z = BOX_RX, BOX_CZ - d
    return x, z, (1.0, 0.0)

def place_boxes():
    nb = len(S.BOX_LETTERS)
    for k, letter in enumerate(S.BOX_LETTERS):
        count = S.BOX_SEATS[letter]
        zone = "CTRBOX" if letter in S.CENTER_BOXES else "BOX"
        layout = {1: (0, -1), 2: (0, 0), 3: (0, 1), 4: (1, 1), 5: (1, 0), 6: (1, -1),
                  7: (2, -0.9), 8: (2, 0.9)}
        for n in range(1, count + 1):
            r, c = layout[n]
            # sample path slightly before/after the box centre for the across offset
            tc = (k + 0.5) / nb
            x0, z0, (nx, nz) = box_path_point(tc)
            # tangent = rotate normal
            tx, tz = -nz, nx
            depth = 1.5 + r * BOX_PITCH
            across = c * 1.9
            x = x0 + nx * depth + tx * across
            z = z0 + nz * depth + tz * across
            floor_y = BOX_Y + r * 0.5
            add("boxes", "center_box" if zone == "CTRBOX" else "side_box",
                letter, n, x, floor_y, z, zone)

def place_lower_tier():
    radius0 = LT_FRONT_Z - LT_CC
    # Grand Tier
    for row in S.grand_tier_rows():
        i = row["index"]
        zc, floor_y = lower_tier_row(i)
        radius = radius0 + (zc - LT_FRONT_Z)
        for block, nums in row["blocks"].items():
            for n in nums:
                if block == "center":
                    s = lateral_center_consecutive(n, len(nums), SEAT_W)
                elif block.startswith("side"):
                    s = lateral_side(n, 7 * SEAT_W + AISLE, SEAT_W)
                else:  # far sides 29+/30+
                    k = (n - 29) // 2
                    s = 7 * SEAT_W + AISLE + 14 * SEAT_W + AISLE + (k + 0.5) * SEAT_W
                    s = -s if n % 2 else s
                x, z = arc_point(LT_CC, radius, s)
                add("grand_tier", block, row["row"], n, x, floor_y, z,
                    S.grand_tier_zone(block, n))
    # Dress Circle
    for row in S.dress_circle_rows():
        i = row["index"] + 5
        zc, floor_y = lower_tier_row(i)
        radius = radius0 + (zc - LT_FRONT_Z)
        for block, nums in row["blocks"].items():
            for n in nums:
                if block.startswith("center"):
                    s = lateral_center_split(n, SEAT_W)
                else:
                    s = lateral_side(n, 14 * SEAT_W + AISLE, SEAT_W)
                x, z = arc_point(LT_CC, radius, s)
                flags = ["accessible-row"] if row["row"] == "L" else None
                add("dress_circle", block, row["row"], n, x, floor_y, z,
                    S.dress_circle_zone(row["row"], block, n), flags)

def place_upper_tier():
    radius0 = UT_FRONT_Z - UT_CC
    w = SEAT_W
    for row in S.balcony_circle_rows():
        i = row["index"]
        zc, floor_y = upper_tier_row(i)
        radius = radius0 + (zc - UT_FRONT_Z)
        for block, nums in row["blocks"].items():
            for n in nums:
                if block == "center":
                    s = lateral_center_consecutive(n, len(nums), w)
                elif block.startswith("side"):
                    s = lateral_side(n, 7 * w + AISLE, w)
                else:
                    k = (n - 25) // 2
                    s = 7 * w + AISLE + 12 * w + AISLE + (k + 0.5) * w
                    s = -s if n % 2 else s
                x, z = arc_point(UT_CC, radius, s)
                add("balcony_circle", block, row["row"], n, x, floor_y, z,
                    S.balcony_circle_zone(block, n))
    w = BAL_SEAT_W
    for row in S.balcony_rows():
        i = row["index"] + 5
        zc, floor_y = upper_tier_row(i)
        radius = radius0 + (zc - UT_FRONT_Z)
        for block, nums in row["blocks"].items():
            for n in nums:
                if block.startswith("center"):
                    s = lateral_center_split(n, w)
                elif block.startswith("side"):
                    s = lateral_side(n, 14 * w + AISLE, w)
                else:
                    k = (n - 21) // 2
                    s = 14 * w + AISLE + 10 * w + AISLE + (k + 0.5) * w
                    s = -s if n % 2 else s
                x, z = arc_point(UT_CC, radius, s)
                add("balcony", block, row["row"], n, x, floor_y, z,
                    S.balcony_zone(row["row"], block, n))

place_orchestra()
place_boxes()
place_lower_tier()
place_upper_tier()

# ------------------------------------------------------------ house shell
# Geometry the viewer draws: floors, tier fronts, overhang lips, stage, pit.
def arc_polyline(center_z, radius, half_width, n=24):
    pts = []
    for k in range(n + 1):
        s = -half_width + 2 * half_width * k / n
        x, z = arc_point(center_z, radius, s)
        pts.append([round(x, 2), round(z, 2)])
    return pts

def tier_outline(front_z, cc, row_fn, n_rows, half_w):
    rows = []
    for i in range(n_rows):
        zc, y = row_fn(i)
        rows.append({"z": round(zc, 2), "y": round(y, 2),
                     "arc": arc_polyline(cc, front_z - cc + (zc - front_z), half_w)})
    return rows

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
                             "arc": arc_polyline(ORCH_CC, ORCH_A_Z - ORCH_CC + i * PITCH, 48)}
                            for i in range(len(S.ORCH_ROWS))]},
    "boxes": {"floor_y": BOX_Y, "soffit_y": BOX_SOFFIT,
              "rail": [[round(v, 2) for v in box_path_point(t / 60)[:2]] for t in range(61)],
              "outer": [[round(box_path_point(t / 60)[0] + box_path_point(t / 60)[2][0] * 9, 2),
                         round(box_path_point(t / 60)[1] + box_path_point(t / 60)[2][1] * 9, 2)] for t in range(61)]},
    "lower_tier": {"rows": tier_outline(LT_FRONT_Z, LT_CC, lower_tier_row, 16, 54),
                   "soffit_lip_y": LT_FRONT_Y - LT_SOFFIT_DROP, "aisle_after_row": 4},
    "upper_tier": {"rows": tier_outline(UT_FRONT_Z, UT_CC, upper_tier_row, 16, 56),
                   "soffit_lip_y": UT_FRONT_Y - UT_SOFFIT_DROP, "aisle_after_row": 4},
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

# inject into the viewer
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
    print(f"  {k[0]:15s} {k[1]:11s} {under[k]}")

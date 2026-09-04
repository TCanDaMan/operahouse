#!/usr/bin/env python3
"""Generate data/seats.json and data/seats.csv from the seat inventory and
house geometry, then inject the data into web/index.html.

Coordinate frame (feet): x across the house (+ = even / Carriage Lobby side),
y up (0 = orchestra floor at row A), z toward the rear (0 = curtain line).

House topology (calibrated against the War Memorial virtual tour and SF Opera
seat photos, see sources/CALIBRATION.md):
  orchestra  -> rear rows under the box ring
  boxes      -> horseshoe ring; rear boxes under the Grand Tier
  grand_tier -> 5 rows on its own slab, low soffit of the Dress Circle above
  dress_circle -> 11 rows on its own slab, Balcony above rows B-L
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

class Tier:
    """A raked slab: rail at rail_z, rows behind it, curved in plan about
    (0, curve_cz). rows = list of (z_center, floor_y)."""
    def __init__(self, name, rail_z, curve_cz, rows, soffit_lip_y, slope):
        self.name, self.rail_z, self.cz = name, rail_z, curve_cz
        self.rows, self.soffit_lip_y, self.slope = rows, soffit_lip_y, slope
        self.radius0 = rail_z - curve_cz
    def radius(self, z):
        return self.radius0 + (z - self.rail_z)
    def lip_z(self, x):
        r = self.radius0
        x = max(-r + 0.1, min(r - 0.1, x))
        return self.cz + math.sqrt(r * r - x * x)
    def floor_at(self, z):
        """floor height on this tier at depth z (clamped to its rows)"""
        if z <= self.rows[0][0]:
            return self.rows[0][1]
        for (z0, y0), (z1, y1) in zip(self.rows, self.rows[1:]):
            if z <= z1:
                return y0 + (y1 - y0) * (z - z0) / (z1 - z0)
        return self.rows[-1][1]

def make_tiers():
    tiers = {}
    g = G["grand_tier"]
    rz, off = g["rail_z_ft"]["value"], g["first_row_offset_ft"]["value"]
    rows = [(rz + off + i * TIER_PITCH, g["floor_y_ft"]["value"] + i * g["rise_per_row_ft"]["value"]) for i in range(5)]
    tiers["grand_tier"] = Tier("grand_tier", rz, g["curve_center_z_ft"]["value"], rows,
                               g["floor_y_ft"]["value"] - g["soffit_drop_ft"]["value"],
                               g["rise_per_row_ft"]["value"] / TIER_PITCH)
    d = G["dress_circle"]
    rz, off = d["rail_z_ft"]["value"], d["first_row_offset_ft"]["value"]
    rows = [(rz + off + i * TIER_PITCH, d["floor_y_ft"]["value"] + i * d["rise_per_row_ft"]["value"]) for i in range(11)]
    tiers["dress_circle"] = Tier("dress_circle", rz, d["curve_center_z_ft"]["value"], rows,
                                 d["floor_y_ft"]["value"] - d["soffit_drop_ft"]["value"],
                                 d["rise_per_row_ft"]["value"] / TIER_PITCH)
    u = G["upper_tier"]
    rz, off = u["rail_z_ft"]["value"], u["first_row_offset_ft"]["value"]
    y0, r1, r2 = u["floor_y_ft"]["value"], u["balcony_circle_rise_per_row_ft"]["value"], u["balcony_rise_per_row_ft"]["value"]
    rows = [(rz + off + i * TIER_PITCH, y0 + i * r1) for i in range(5)]
    base_z, base_y = rows[-1][0] + CROSS, rows[-1][1] + u["cross_aisle_rise_ft"]["value"]
    rows += [(base_z + j * TIER_PITCH, base_y + j * r2) for j in range(11)]
    tiers["upper_tier"] = Tier("upper_tier", rz, u["curve_center_z_ft"]["value"], rows,
                               y0 - u["soffit_drop_ft"]["value"], r1 / TIER_PITCH)
    return tiers

TIERS = make_tiers()

def arc_point(center_z, radius, s):
    phi = s / radius
    return radius * math.sin(phi), center_z + radius * math.cos(phi)

# ----------------------------------------------------------- overhang model
def box_ring_lip_z(x):
    if abs(x) >= BOX_RX:
        return None
    return BOX_CZ + BOX_RZ * math.sqrt(1 - (x / BOX_RX) ** 2)

def box_floor_at(z):
    return BOX_Y + 0.5 * min(2, max(0, (z - (box_ring_lip_z(0) or 0)) / BOX_PITCH))

OVERHANGS = [
    {"name": "boxes", "lip_z": box_ring_lip_z, "soffit_y": BOX_SOFFIT, "slope": 0.0,
     "floor_below": lambda x, z: orch_floor_y(z)},
    {"name": "grand_tier", "lip_z": TIERS["grand_tier"].lip_z,
     "soffit_y": TIERS["grand_tier"].soffit_lip_y, "slope": TIERS["grand_tier"].slope,
     "floor_below": lambda x, z: box_floor_at(z) if abs(x) < BOX_RX + 8 else orch_floor_y(z)},
    {"name": "dress_circle", "lip_z": TIERS["dress_circle"].lip_z,
     "soffit_y": TIERS["dress_circle"].soffit_lip_y, "slope": TIERS["dress_circle"].slope,
     "floor_below": lambda x, z: TIERS["grand_tier"].floor_at(z)},
    {"name": "upper_tier", "lip_z": TIERS["upper_tier"].lip_z,
     "soffit_y": TIERS["upper_tier"].soffit_lip_y, "slope": TIERS["upper_tier"].slope,
     "floor_below": lambda x, z: TIERS["dress_circle"].floor_at(z)},
]

def overhang_for(x, y_eye, z):
    """Lowest overhang whose lip is in front of the seat and whose soffit is
    above the eye at the seat. Returns dict or None."""
    best = None
    for o in OVERHANGS:
        lz = o["lip_z"](x)
        if lz is None or z <= lz:
            continue
        soffit_here = o["soffit_y"] + o["slope"] * (z - lz)
        if soffit_here <= y_eye + 0.5:
            continue
        if best is None or soffit_here < best["soffit_here"]:
            best = {"name": o["name"], "lip_z": lz, "lip_y": o["soffit_y"],
                    "soffit_here": soffit_here,
                    "opening_h": o["soffit_y"] - o["floor_below"](x, lz),
                    "depth": z - lz}
    return best

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
    oh = overhang_for(eye[0], eye[1], eye[2])
    return ray_clears_lip(eye, refl, oh) and refl[2] > 0

def view_score(m):
    """0-100 experience score. Weights are opinions; see README."""
    d = m["dist_singer_ft"]
    s = 100 - max(0.0, d - 35) * (60 / 125)
    s -= max(0.0, m["horiz_angle_deg"] - 15) * 1.0
    s -= (1.0 - m["stage_width_visible"]) * 60
    if m["overhang"] != "none":
        s -= max(0.0, 25 - m["opening_angle_deg"]) * 1.2
        s -= (PROSC_H - m["visible_prosc_height_ft"]) * 3
        s -= max(0.0, 6 - m["headroom_ft"]) * 2.5      # a ceiling right over your head
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
        lip_e = elev(eye, (eye[0], oh["lip_y"], oh["lip_z"]))
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

def box_path_point(t):
    leg = BOX_CZ - BOX_LEG_FRONT
    a, b = BOX_RX, BOX_RZ
    arc_len = math.pi * (3 * (a + b) - math.sqrt((3 * a + b) * (a + 3 * b))) / 2
    total = 2 * leg + arc_len
    d = t * total
    if d < leg:
        return -BOX_RX, BOX_LEG_FRONT + d, (-1.0, 0.0)
    d -= leg
    if d < arc_len:
        theta = math.pi * (d / arc_len)
        x = -BOX_RX * math.cos(theta)
        z = BOX_CZ + BOX_RZ * math.sin(theta)
        nx, nz = -math.cos(theta) / BOX_RX, math.sin(theta) / BOX_RZ
        ln = math.hypot(nx, nz)
        return x, z, (nx / ln, nz / ln)
    d -= arc_len
    return BOX_RX, BOX_CZ - d, (1.0, 0.0)

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
        radius = tier.radius(zc)
        for block, nums in row["blocks"].items():
            for n in nums:
                s = layout(block, n, len(nums), w)
                x, z = arc_point(tier.cz, radius, s)
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
place_tier_rows("grand_tier", TIERS["grand_tier"], S.grand_tier_rows(), 0, SEAT_W, layout_gt)
place_tier_rows("dress_circle", TIERS["dress_circle"], S.dress_circle_rows(), 0, SEAT_W, layout_dc)
place_tier_rows("balcony_circle", TIERS["upper_tier"], S.balcony_circle_rows(), 0, SEAT_W, layout_bc)
place_tier_rows("balcony", TIERS["upper_tier"], S.balcony_rows(), 5, BAL_SEAT_W, layout_bal)

# ------------------------------------------------------------ house shell
def arc_polyline(center_z, radius, half_width, n=24):
    pts = []
    for k in range(n + 1):
        s = -half_width + 2 * half_width * k / n
        x, z = arc_point(center_z, radius, s)
        pts.append([round(x, 2), round(z, 2)])
    return pts

def tier_shell(tier, half_w):
    rows = [{"z": round(z, 2), "y": round(y, 2), "arc": arc_polyline(tier.cz, tier.radius(z), half_w)}
            for z, y in tier.rows]
    rail = {"z": round(tier.rail_z, 2), "y": round(tier.rows[0][1], 2),
            "arc": arc_polyline(tier.cz, tier.radius0, half_w)}
    return {"name": tier.name, "rows": rows, "rail": rail, "soffit_lip_y": tier.soffit_lip_y}

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
    "tiers": [tier_shell(TIERS["grand_tier"], 54), tier_shell(TIERS["dress_circle"], 53),
              tier_shell(TIERS["upper_tier"], 56)],
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

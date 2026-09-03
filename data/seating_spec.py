"""Seat inventory of the War Memorial Opera House, transcribed from the
War Memorial seat-numbered chart (sources/wmoh-seat-chart.pdf) and the
SF Opera price-zone map (sources/sfopera-price-zone-map.pdf).

Conventions
  odd seat numbers  = Grove Street side  (x < 0 in the model)
  even seat numbers = Carriage Lobby side (x > 0 in the model)
  center blocks     = 101+ (orchestra/dress circle/balcony: odd 101.. and
                      even 102.. meeting at the center; grand tier and
                      balcony circle: 101..114 consecutive)

Each row entry lists the seat numbers present. Blocks are keyed so the
build script can place them laterally.
"""

def odd(lo, hi):
    return list(range(lo, hi + 1, 2))

def even(lo, hi):
    return list(range(lo, hi + 1, 2))

# ---------------------------------------------------------------- orchestra
ORCH_ROWS = ["A","B","C","D","E","F","G","H","J","K","L","M","N","O","P",
             "R","S","T","U","V","W","X","Y","Z","ZZ"]

def _orch_center(i):
    # center blocks alternate 12 / 11 seats, starting with 12 in row A
    hi_odd = 123 if i % 2 == 0 else 121
    hi_even = 124 if i % 2 == 0 else 122
    return odd(101, hi_odd), even(102, hi_even)

_ORCH_SIDE_HI = {  # highest odd number on the Grove side; even side is +1
    "A":15,"B":15,"C":17,"D":17,"E":19,"F":19,"G":19,
    "H":21,"J":21,"K":21,"L":21,"M":21,"N":21,"O":21,"P":23,
    "R":3,"S":3,"T":3,
    "U":23,"V":23,"W":23,"X":23,"Y":23,"Z":23,"ZZ":23,
}

def orchestra_rows():
    rows = []
    for i, r in enumerate(ORCH_ROWS):
        c_odd, c_even = _orch_center(i)
        hi = _ORCH_SIDE_HI[r]
        row = {
            "row": r, "index": i,
            "blocks": {
                "center_odd": c_odd, "center_even": c_even,
                "side_odd": odd(1, hi), "side_even": even(2, hi + 1),
            },
        }
        if r == "S":  # wheelchair platforms, sold as seats when not needed
            row["blocks"]["platform_odd"] = odd(5, 19)
            row["blocks"]["platform_even"] = even(6, 20)
        rows.append(row)
    return rows

# ------------------------------------------------------------------- boxes
BOX_LETTERS = ["A","B","C","D","E","F","G","H","J","K","L","M","N","O","P",
               "Q","R","S","T","U","V","W","X","Y","Z"]
# Box A is at the Grove-side front near the proscenium; the ring runs around
# the rear to Z at the Carriage-side front. Boxes E-V are the center boxes.
BOX_SEATS = {b: (6 if b in ("A","B","Y","Z") else 8) for b in BOX_LETTERS}
CENTER_BOXES = set("EFGHJKLMNOPQRSTUV")

# ------------------------------------------------------- lower tier (GT+DC)
GT_ROWS = ["AA","BB","CC","DD","EE"]
DC_ROWS = ["A","B","C","D","E","F","G","H","J","K","L"]

def grand_tier_rows():
    rows = []
    for i, r in enumerate(GT_ROWS):
        center = list(range(101, 115)) if i % 2 == 0 else list(range(101, 114))
        far_hi = 39 if r != "EE" else 35
        rows.append({"row": r, "index": i, "blocks": {
            "center": center,
            "side_odd": odd(1, 27), "side_even": even(2, 28),
            "far_odd": odd(29, far_hi), "far_even": even(30, far_hi + 1),
        }})
    return rows

def dress_circle_rows():
    rows = []
    for i, r in enumerate(DC_ROWS):
        if r == "K":      # sound/lighting position occupies the center
            c_odd = odd(101, 109) + odd(117, 125)
            c_even = even(102, 110) + even(118, 126)
        elif r == "L":    # accessible row at the 3rd-floor doors
            c_odd = odd(101, 111) + odd(117, 125)
            c_even = even(102, 112) + even(118, 126)
        else:
            c_odd = odd(101, 127 if i % 2 == 0 else 125)
            c_even = even(102, 128 if i % 2 == 0 else 126)
        side_hi = 27 if r != "L" else 17
        rows.append({"row": r, "index": i, "blocks": {
            "center_odd": c_odd, "center_even": c_even,
            "side_odd": odd(1, side_hi), "side_even": even(2, side_hi + 1),
        }})
    return rows

# ------------------------------------------------------ upper tier (BC+Bal)
BC_ROWS = ["AA","BB","CC","DD","EE"]
BAL_ROWS = ["A","B","C","D","E","F","G","H","J","K","L"]

def balcony_circle_rows():
    rows = []
    for i, r in enumerate(BC_ROWS):
        center = list(range(101, 115)) if i % 2 == 0 else list(range(101, 114))
        rows.append({"row": r, "index": i, "blocks": {
            "center": center,
            "side_odd": odd(1, 23), "side_even": even(2, 24),
            "far_odd": odd(25, 41), "far_even": even(26, 42),
        }})
    return rows

def balcony_rows():
    rows = []
    for i, r in enumerate(BAL_ROWS):
        if r in ("A", "B"):   # followspot / projection position in the middle
            c_odd = odd(101, 115) + [125, 127]
            c_even = even(102, 116) + [126, 128]
        elif r == "L":
            c_odd = odd(101, 125)
            c_even = even(102, 126)
        else:
            c_odd = odd(101, 127 if i % 2 == 0 else 125)
            c_even = even(102, 128 if i % 2 == 0 else 126)
        far_hi = 29 if r != "L" else 27
        rows.append({"row": r, "index": i, "blocks": {
            "center_odd": c_odd, "center_even": c_even,
            "side_odd": odd(1, 19), "side_even": even(2, 20),
            "far_odd": odd(21, far_hi), "far_even": even(22, far_hi + 1),
        }})
    return rows

# ------------------------------------------------------------- price zones
# SF Opera zone codes, from the price-zone map. Seat-level boundaries on the
# side blocks are read off the colored map and are approximate.
ZONES = {
    "ORP":  "Orchestra Premium",
    "ORP2": "Orchestra Premium 2",
    "ORC3": "Orchestra 3",
    "ORC4": "Orchestra 4",
    "CTRBOX": "Center Box (E-V)",
    "BOX":  "Box",
    "GTP":  "Grand Tier Premium",
    "GTP2": "Grand Tier Premium 2",
    "GT":   "Grand Tier",
    "DCP":  "Dress Circle Premium",
    "DC":   "Dress Circle",
    "DC2":  "Dress Circle 2",
    "BC1":  "Balcony Circle 1",
    "BC2":  "Balcony Circle 2",
    "BAL1": "Balcony 1",
    "BAL2": "Balcony 2",
    "BAL3": "Balcony 3",
}

# Placeholder single-ticket prices. The Nov 27 2026 Figaro listing showed
# Orchestra $72-310, Boxes $377-405, Grand Tier/Dress Circle $30-310,
# Balcony Circle/Balcony $30-112. Edit to the prices of the performance you
# are actually pricing; the viewer reads these.
ZONE_PRICES = {
    "ORP": 310, "ORP2": 260, "ORC3": 180, "ORC4": 110,
    "CTRBOX": 405, "BOX": 377,
    "GTP": 310, "GTP2": 260, "GT": 180,
    "DCP": 220, "DC": 150, "DC2": 95,
    "BC1": 112, "BC2": 80,
    "BAL1": 72, "BAL2": 48, "BAL3": 30,
}

def orchestra_zone(row, block, n):
    i = ORCH_ROWS.index(row)
    inner = n <= 4               # seats 1-4 / 2-4 next to the inner aisle
    mid = n in (5, 6)
    if block.startswith("center"):
        if i <= 8:  return "ORP"      # A-J
        if i <= 17: return "ORP2"     # K-T
        if i <= 23: return "ORC3"     # U-Z
        return "ORC4"                 # ZZ
    if block.startswith("platform"):
        return "ORC3"
    if row == "ZZ":
        return "ORC4"
    if i <= 8:                        # A-J sides
        return "ORP" if inner else ("ORC3" if mid else "ORC4")
    if i <= 17:                       # K-T sides
        return "ORP2" if inner else ("ORC3" if mid else "ORC4")
    return "ORC3" if inner else "ORC4"

def grand_tier_zone(block, n):
    if block == "center": return "GTP"
    if block.startswith("far"): return "GT"
    return "GTP" if n <= 18 else "GTP2"

def dress_circle_zone(row, block, n):
    i = DC_ROWS.index(row)
    if block.startswith("center"):
        return "DCP" if i <= 1 else "DC"
    if i <= 2:
        return "DCP" if n <= 8 else "DC"
    if i == 3:
        return "DC"
    return "DC" if n <= 8 else "DC2"

def balcony_circle_zone(block, n):
    return "BC2" if block.startswith("far") else "BC1"

def balcony_zone(row, block, n):
    i = BAL_ROWS.index(row)
    if block.startswith("far"): return "BAL3"
    if block.startswith("center"):
        return "BAL1" if i <= 3 else "BAL2"
    return "BAL1" if (i <= 3 and n <= 10) else "BAL2"

"""Single data model for the Courtyard Bungalow, Garo Hills.
All set-out coordinates are wall CENTRE LINES in feet, origin at the
north-west corner of the main block, x running east, y running south.
"""
from fractions import Fraction

# ---------------------------------------------------------------- formatting
def fi(inches, step=3):
    """Format inches as ft-in. step=3 rounds to nearest 3 in; step=0 exact."""
    v = Fraction(inches).limit_denominator(8)
    if step:
        v = Fraction(round(v / step) * step)
    neg = v < 0
    v = abs(v)
    ft = int(v // 12)
    rem = v - ft * 12
    whole = int(rem)
    frac = rem - whole
    fr = {Fraction(1, 4): "¼", Fraction(1, 2): "½", Fraction(3, 4): "¾",
          Fraction(1, 8): "⅛", Fraction(3, 8): "⅜", Fraction(5, 8): "⅝",
          Fraction(7, 8): "⅞"}.get(frac, "")
    ins = f"{whole}{fr}" if (whole or fr) else "0"
    s = f"{ft} ft {ins} in" if ft else f"{ins} in"
    return ("-" if neg else "") + s


def ff(feet, step=3):
    return fi(Fraction(feet).limit_denominator(8) * 12, step)


def r3(inches):
    return Fraction(round(Fraction(inches) / 3) * 3)


def lakh(rupees):
    return f"{rupees / 1e5:,.2f} lakh"


def money(rupees):
    if rupees >= 1e7:
        return f"₹ {rupees / 1e7:.2f} crore"
    return f"₹ {rupees / 1e5:,.2f} lakh"


# ---------------------------------------------------------------- walls
EXT, INT = 9, Fraction(9, 2)   # inches
# (x0, y0, x1, y1, thickness_in, kind)
WALLS = [
    (0, 0, 98, 0, EXT, "external, north face (between study and airlock it is the acoustic wall)"),
    (0, 40, 98, 40, EXT, "external, south face"),
    (0, -27, 0, 40, EXT, "external, west face (creative wing and main block, one line)"),
    (98, 0, 98, 40, EXT, "external, east face"),
    (0, -27, 18, -27, EXT, "external, north face of creative wing"),
    (18, -27, 18, 40, EXT, "external east face of creative wing, then party wall of resident suite"),
    (0, -7, 18, -7, EXT, "acoustic wall, studio / airlock"),
    (0, 13, 18, 13, EXT, "acoustic wall, study / resident suite"),
    (80, 17, 80, 40, EXT, "party wall, guest suite to kitchen"),
    (8, 13, 8, 22, INT, "partition, bath 1 / dressing 1"),
    (0, 22, 18, 22, INT, "partition, bath and dressing 1 / bedroom 1"),
    (18, 13, 32, 13, INT, "partition, library / sitting hall"),
    (32, 0, 32, 13, INT, "partition, library / foyer"),
    (50, 0, 50, 13, INT, "partition, foyer / crockery alcove"),
    (62, 0, 62, 13, INT, "partition, crockery alcove / store"),
    (72, 0, 72, 13, INT, "partition, store / utility"),
    (82, 0, 82, 13, INT, "partition, utility / wash lobby"),
    (88, 0, 88, 13, INT, "partition, wash lobby / shared toilet and bathroom"),
    (88, 6.5, 98, 6.5, INT, "partition, shared toilet / shared bathroom"),
    (62, 13, 98, 13, INT, "partition, service strip / passage and bath 2"),
    (62, 17, 90, 17, INT, "partition, passage / kitchen and dressing 2"),
    (90, 13, 90, 24, INT, "partition, dressing 2 / bath 2"),
    (80, 24, 98, 24, INT, "partition, dressing and bath 2 / bedroom 2"),
]

# RCC columns 12 in x 18 in (CL positions, ft)
COLUMNS = [(x, 0) for x in (0, 18, 32, 50, 62, 80, 98)] + \
          [(x, 40) for x in (0, 18, 34, 50, 62, 80, 98)] + \
          [(0, -27), (18, -27), (0, -7), (18, -7), (0, 13), (0, 22), (98, 13), (98, 24),
           (18, 13), (50, 13), (62, 13), (62, 17), (80, 13), (80, 17), (80, 24), (32, 13)]


def _half(line_axis, coord, a, b):
    """Half-thickness (in) of the wall lying on a room side, 0 if open."""
    best = 0
    for x0, y0, x1, y1, t, _ in WALLS:
        if line_axis == "x" and x0 == x1 == coord:
            lo, hi = sorted((y0, y1))
        elif line_axis == "y" and y0 == y1 == coord:
            lo, hi = sorted((x0, x1))
        else:
            continue
        if min(hi, b) - max(lo, a) > 0.5:
            best = max(best, Fraction(t) / 2)
    return best


# ---------------------------------------------------------------- rooms
# key, name, x0, x1, y0, y1, ceiling (ft-in text), habitable, circulation
ROOMS = [
    ("STU", "Music studio (inside acoustic lining)", 0, 18, -27, -7, "12 ft 0 in", True, False),
    ("AIRL", "Studio airlock and gear lobby", 0, 18, -7, 0, "10 ft 0 in", False, False),
    ("STDY", "Study", 0, 18, 0, 13, "12 ft 0 in", True, False),
    ("LIB", "Library", 18, 32, 0, 13, "12 ft 0 in", True, False),
    ("BTH1", "Bathroom 1 (attached)", 0, 8, 13, 22, "10 ft 0 in", False, False),
    ("DRS1", "Dressing 1 (entry lobby to bedroom 1)", 8, 18, 13, 22, "10 ft 0 in", False, False),
    ("BED1", "Master bedroom 1 (resident)", 0, 18, 22, 40, "12 ft 3 in", True, False),
    ("FOY", "Entrance foyer", 32, 50, 0, 13, "12 ft 3 in", False, True),
    ("HALL", "Sitting hall", 18, 50, 13, 40, "12 ft 3 in at walls, 16 ft 0 in at centre", True, False),
    ("DIN", "Dining", 50, 62, 13, 40, "12 ft 3 in", True, False),
    ("ALC", "Crockery and bar alcove", 50, 62, 0, 13, "12 ft 3 in", True, False),
    ("KIT", "Kitchen with breakfast table", 62, 80, 17, 40, "12 ft 3 in", True, False),
    ("STR", "Store", 62, 72, 0, 13, "10 ft 0 in", False, False),
    ("UTL", "Utility", 72, 82, 0, 13, "10 ft 0 in", False, False),
    ("PAS", "Service passage", 62, 90, 13, 17, "9 ft 0 in", False, True),
    ("WLB", "Wash lobby (shared basin counter)", 82, 88, 0, 13, "10 ft 0 in", False, True),
    ("SWC", "Shared toilet (WC), north-east corner", 88, 98, 0, 6.5, "10 ft 0 in", False, False),
    ("SBT", "Shared bathroom (walk-in shower + basin)", 88, 98, 6.5, 13, "10 ft 0 in", False, False),
    ("DRS2", "Dressing 2 (entry lobby to bedroom 2)", 80, 90, 17, 24, "10 ft 0 in", False, False),
    ("BTH2", "Bathroom 2 (attached)", 90, 98, 13, 24, "10 ft 0 in", False, False),
    ("BED2", "Master bedroom 2 (guest)", 80, 98, 24, 40, "12 ft 3 in", True, False),
]


def room_clear(r):
    key, name, x0, x1, y0, y1 = r[:6]
    w = (x1 - x0) * 12 - _half("x", x0, y0, y1) - _half("x", x1, y0, y1)
    d = (y1 - y0) * 12 - _half("y", y0, x0, x1) - _half("y", y1, x0, x1)
    if key == "STU":
        w -= 2 * LINING
        d -= 2 * LINING
    return r3(w), r3(d)


def room_table():
    out = []
    for r in ROOMS:
        w, d = room_clear(r)
        area = float(w * d / 144)
        out.append(dict(key=r[0], name=r[1], x0=r[2], x1=r[3], y0=r[4], y1=r[5],
                        w=w, d=d, area=round(area), ceil=r[6], hab=r[7], circ=r[8]))
    return out


# Detached garage + studio block (own CL grid, ft, origin at its NW corner)
GARAGE_ROOMS = [
    ("GAR", "Garage, two cars", 0, 21, 0, 23, 9, 9, 9, 4.5, "10 ft 0 in"),
    ("TWB", "Two-wheeler bay", 21, 30, 0, 23, 4.5, 9, 9, 9, "10 ft 0 in"),
    ("TST", "Tool, garden kit and fuel store", 30, 41, 0, 13, 9, 9, 9, 4.5, "10 ft 0 in"),
    ("GEN", "Generator and pump room", 30, 41, 13, 23, 9, 9, 4.5, 9, "10 ft 0 in"),
]
LINING = Fraction(13, 2)   # 4.5 in independent stud lining + 2 in air gap


def garage_table():
    out = []
    for k, n, x0, x1, y0, y1, tw, te, tn, ts, c in GARAGE_ROOMS:
        w = (x1 - x0) * 12 - Fraction(tw) / 2 - Fraction(te) / 2
        d = (y1 - y0) * 12 - Fraction(tn) / 2 - Fraction(ts) / 2
        if k == "STU":
            w -= 2 * LINING
            d -= 2 * LINING
        w, d = r3(w), r3(d)
        out.append(dict(key=k, name=n, w=w, d=d, area=round(float(w * d / 144)), ceil=c,
                        x0=x0, x1=x1, y0=y0, y1=y1))
    return out


# ---------------------------------------------------------------- areas
MAIN_OUT = ((98 * 12 + 9) / 12, (40 * 12 + 9) / 12)          # outer face size, ft
WING_OUT = ((18 * 12 + 9) / 12, 27.0)                          # creative wing beyond main north face
GARAGE_OUT_AREA = (41 * 12 + 9) * (23 * 12 + 9) / 144
VERANDAS = [  # name, length ft, depth ft
    ("South veranda (9 ft 0 in deep to column line)", 99, 9),
    ("North veranda, library to alcove", 44, 8),
    ("Entrance porch (car porch)", 20, 14),
    ("Covered link walk, garage to north veranda", 6, 88),
]
FIREHOUSE = dict(size=20, platform=24)


def areas():
    rt = room_table()
    gt = garage_table()
    carpet_house = sum(r["area"] for r in rt)
    carpet_gar = sum(r["area"] for r in gt)
    circ = sum(r["area"] for r in rt if r["circ"])
    built_house = round(MAIN_OUT[0] * MAIN_OUT[1] + WING_OUT[0] * WING_OUT[1])
    built_gar = round(GARAGE_OUT_AREA)
    ver = [(n, l, d, l * d) for n, l, d in VERANDAS]
    ver_total = sum(v[3] for v in ver)
    fire = FIREHOUSE["size"] ** 2
    return dict(rt=rt, gt=gt, carpet_house=carpet_house, carpet_gar=carpet_gar,
                carpet=carpet_house + carpet_gar, circ=circ,
                circ_pct=100 * circ / carpet_house,
                built_house=built_house, built_gar=built_gar,
                built=built_house + built_gar, ver=ver, ver_total=ver_total,
                fire=fire, super=built_house + built_gar + ver_total + fire)


# ---------------------------------------------------------------- climate
LAT = 25.5   # Tura, West Garo Hills
SUN = dict(winter=90 - LAT - 23.44, equinox=90 - LAT, summer=90 - LAT + 23.44)
RAIN_ANNUAL_IN = 130          # about 3,300 mm a year
RAIN_DESIGN_IN_HR = 5         # design storm, about 125 mm an hour
ROOF_AREA = 6000              # plan area of all roofs on the house, sq ft
SQFT_PER_DOWNPIPE = 500
TANK = dict(l=20, b=12, depth=9)  # water depth, ft


def rain():
    q_cfs = ROOF_AREA * RAIN_DESIGN_IN_HR / 12 / 3600
    pipes = -(-ROOF_AREA // SQFT_PER_DOWNPIPE)
    vol_cuft = TANK["l"] * TANK["b"] * TANK["depth"]
    litres = vol_cuft * 28.317
    annual_cuft = ROOF_AREA * RAIN_ANNUAL_IN / 12 * 0.85
    fill_in = vol_cuft / (ROOF_AREA * 0.85) * 12
    return dict(q_cfs=q_cfs, q_lps=q_cfs * 28.317, pipes=pipes, vol=vol_cuft,
                litres=litres, annual_litres=annual_cuft * 28.317, fill_in=fill_in,
                days=litres / 400)

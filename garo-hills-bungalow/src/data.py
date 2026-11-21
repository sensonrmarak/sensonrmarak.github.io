"""Single data model for the budget Courtyard Bungalow, Garo Hills.
Every length is in FEET (decimal). Set-out coordinates are wall CENTRE LINES,
origin at the north-west corner, x running east, y running south."""
import math

EXT = 0.75     # external wall thickness, ft (one brick)
INT = 0.375    # internal partition thickness, ft (half brick)


# ---------------------------------------------------------------- formatting
def ft(v, dp=2):
    return f"{v:,.{dp}f} ft"


def sq(v, dp=2):
    return f"{v:,.{dp}f} sq ft"


def cu(v, dp=1):
    return f"{v:,.{dp}f} cu ft"


def lakh(rupees):
    return f"{rupees / 1e5:,.2f} lakh"


def money(rupees):
    return f"₹ {rupees / 1e5:,.2f} lakh"


def thick(t):
    return "0.75 ft" if t == EXT else "0.375 ft"


# ---------------------------------------------------------------- walls
# (x0, y0, x1, y1, thickness_ft, description)
WALLS = [
    (0, 0, 46, 0, EXT, "external, north face"),
    (0, 28, 46, 28, EXT, "external, south face"),
    (0, 0, 0, 28, EXT, "external, west face"),
    (46, 0, 46, 28, EXT, "external, east face"),
    (14, 0, 14, 28, INT, "partition, west rooms / sitting and dining"),
    (30, 0, 30, 28, INT, "partition, sitting and dining / wash lobby, kitchen, bedroom 2"),
    (0, 10, 14, 10, INT, "partition, library-study / bath 1 and dressing 1"),
    (6, 10, 6, 17, INT, "partition, bath 1 / dressing 1"),
    (0, 17, 14, 17, INT, "partition, bath 1 and dressing 1 / bedroom 1"),
    (30, 7, 46, 7, INT, "partition, wash lobby and shared toilet-bath / kitchen"),
    (34, 0, 34, 7, INT, "partition, wash lobby / shared toilet-bath"),
    (30, 16, 46, 16, INT, "partition, kitchen / bedroom 2 and bath 2"),
    (40.5, 16, 40.5, 28, INT, "partition, bedroom 2 / bath 2 and wardrobe 2"),
    (40.5, 22, 46, 22, INT, "partition, bath 2 / wardrobe 2"),
]

# RCC columns 0.75 ft x 1.00 ft at wall junctions (CL positions, ft)
COLUMNS = [(0, 0), (14, 0), (30, 0), (46, 0), (0, 28), (14, 28), (30, 28), (46, 28), (22, 0), (22, 28),
           (0, 10), (0, 17), (14, 10), (14, 17), (30, 7), (30, 16), (46, 7), (46, 16)]


def _half(axis, c, a, b):
    best = 0.0
    for x0, y0, x1, y1, t, _ in WALLS:
        if axis == "x" and x0 == x1 == c:
            lo, hi = sorted((y0, y1))
        elif axis == "y" and y0 == y1 == c:
            lo, hi = sorted((x0, x1))
        else:
            continue
        if min(hi, b) - max(lo, a) > 0.25:
            best = max(best, t / 2)
    return best


# ---------------------------------------------------------------- rooms
# key, name, x0, x1, y0, y1, ceiling height ft, habitable, circulation
ROOMS = [
    ("LIB", "Library and study", 0, 14, 0, 10, 12.0, True, False),
    ("BTH1", "Bath 1 (attached)", 0, 6, 10, 17, 10.0, False, False),
    ("DRS1", "Dressing 1 (entry lobby)", 6, 14, 10, 17, 10.0, False, True),
    ("BED1", "Bedroom 1 (resident)", 0, 14, 17, 28, 12.0, True, False),
    ("LIV", "Sitting and dining", 14, 30, 0, 28, 12.0, True, False),
    ("WLB", "Wash lobby (basin)", 30, 34, 0, 7, 10.0, False, True),
    ("SWB", "Shared toilet and bathroom (NE corner)", 34, 46, 0, 7, 10.0, False, False),
    ("KIT", "Kitchen", 30, 46, 7, 16, 12.0, True, False),
    ("BED2", "Bedroom 2 (guest)", 30, 40.5, 16, 28, 12.0, True, False),
    ("BTH2", "Bath 2 (attached)", 40.5, 46, 16, 22, 10.0, False, False),
    ("WRD2", "Wardrobe 2", 40.5, 46, 22, 28, 10.0, False, False),
]


def room_clear(r):
    key, name, x0, x1, y0, y1 = r[:6]
    hw0, hw1 = _half("x", x0, y0, y1), _half("x", x1, y0, y1)
    hd0, hd1 = _half("y", y0, x0, x1), _half("y", y1, x0, x1)
    return (x1 - x0) - hw0 - hw1, (y1 - y0) - hd0 - hd1, (x1 - x0, hw0, hw1), (y1 - y0, hd0, hd1)


def room_table():
    out = []
    for r in ROOMS:
        w, d, wx, dy = room_clear(r)
        out.append(dict(key=r[0], name=r[1], x0=r[2], x1=r[3], y0=r[4], y1=r[5], w=w, d=d, area=w * d,
                        wx=wx, dy=dy, ceil=r[6], hab=r[7], circ=r[8]))
    return out


def working(cl, h0, h1):
    """e.g. '14.00 - 0.375 - 0.1875 = 13.44'."""
    parts = [f"{cl:.2f}"] + [f"{h:g}" for h in (h0, h1) if h]
    return " − ".join(parts) + f" = {cl - h0 - h1:.2f}"


# ---------------------------------------------------------------- areas
OUT_W, OUT_D = 46 + EXT, 28 + EXT            # outer face size, ft
VERANDA = (OUT_W, 8.0)                        # south veranda, full length, 8 ft deep
PORCH = (10.0, 6.0)                           # covered entrance porch on the north
CARPORT = (18.0, 20.0)
FIREHOUSE = 12.0                              # square pavilion on post centres


def areas():
    rt = room_table()
    carpet = sum(r["area"] for r in rt)
    circ = sum(r["area"] for r in rt if r["circ"])
    built = OUT_W * OUT_D
    ver = VERANDA[0] * VERANDA[1]
    porch = PORCH[0] * PORCH[1]
    return dict(rt=rt, carpet=carpet, circ=circ, circ_pct=100 * circ / carpet, built=built,
                ver=ver, porch=porch, covered=ver + porch, super=built + ver + porch,
                carport=CARPORT[0] * CARPORT[1], fire=FIREHOUSE ** 2)


# ---------------------------------------------------------------- climate (all in feet)
LAT = 25.5
SUN = dict(winter=90 - LAT - 23.44, equinox=90 - LAT, summer=90 - LAT + 23.44)
RAIN_ANNUAL_FT = 10.83          # about 130 in a year
RAIN_DESIGN_FT_HR = 0.417       # design storm, 5 in an hour
ROOF = dict(main=(46 + 6, 28 + 3), veranda=(OUT_W + 6, 9.0), porch=(11.0, 7.0))
SQFT_PER_DOWNPIPE = 500
TANK = dict(dia=10.0, depth=4.5)


def rain():
    parts = {k: w * d for k, (w, d) in ROOF.items()}
    area = sum(parts.values())
    q = area * RAIN_DESIGN_FT_HR / 3600
    pipes = math.ceil(area / SQFT_PER_DOWNPIPE)
    vol = math.pi * (TANK["dia"] / 2) ** 2 * TANK["depth"]
    annual = area * RAIN_ANNUAL_FT * 0.85
    fill = vol / (area * 0.85)
    demand = 14.0
    return dict(parts=parts, area=area, q=q, pipes=pipes, vol=vol, annual=annual, fill=fill,
                demand=demand, days=vol / demand)


# ---------------------------------------------------------------- budget (everything on the plot)
def budget():
    a = areas()
    plot_side = 328.08
    fence_len = 4 * plot_side - 60 - 12 - 3.5
    drive_area = 12 * 120
    turn_area = math.pi * 20 ** 2
    groups = [
        ("House", [
            ("Main house, enclosed", a["built"], "sq ft", 2150,
             f"{OUT_W:.2f} × {OUT_D:.2f} = {a['built']:,.2f} sq ft"),
            ("South veranda and entrance porch", a["covered"], "sq ft", 950,
             f"{VERANDA[0]:.2f} × {VERANDA[1]:.2f} + {PORCH[0]:.2f} × {PORCH[1]:.2f} = {a['covered']:,.2f} sq ft"),
            ("Septic tank 6.00 × 4.00 × 5.00 ft and soak pit", 1, "lump sum", 100000, ""),
            ("Water: spring or well line, pump, overhead tank 4.00 ft dia × 3.00 ft", 1, "lump sum", 120000, ""),
            ("Electrical service connection and earthing", 1, "lump sum", 60000, ""),
            ("Rainwater tank, ferrocement, 10.00 ft dia × 4.50 ft deep", 1, "lump sum", 60000, ""),
        ]),
        ("Carport", [
            ("Carport, steel posts, charcoal sheet roof", a["carport"], "sq ft", 550,
             f"{CARPORT[0]:.2f} × {CARPORT[1]:.2f} = {a['carport']:,.2f} sq ft"),
        ]),
        ("Firehouse", [
            ("Pavilion 12.00 × 12.00 ft, four timber posts, pyramid roof", a["fire"], "sq ft", 700,
             f"12.00 × 12.00 = {a['fire']:,.2f} sq ft"),
            ("Stone fire pit 4.00 ft dia and stone benches", 1, "lump sum", 35000, ""),
        ]),
        ("Gate and boundary", [
            ("Stone wall either side of gate, 4.00 ft high", 60, "running ft", 1200, "30.00 + 30.00 = 60.00 ft"),
            ("Chain-link fence 5.00 ft on RCC posts at 10.00 ft, 2 barbed strands", round(fence_len, 2), "running ft", 180,
             f"4 × 328.08 − 60.00 − 12.00 − 3.50 = {fence_len:,.2f} ft"),
            ("Steel gate 12.00 ft in two leaves, wicket 3.50 ft, two stone piers", 1, "lump sum", 60000, ""),
        ]),
        ("Landscape", [
            ("Gravel drive 12.00 ft wide × 120.00 ft", drive_area, "sq ft", 70, f"12.00 × 120.00 = {drive_area:,.2f} sq ft"),
            ("Gravel turning circle 40.00 ft dia", round(turn_area, 2), "sq ft", 70, f"3.1416 × 20.00 × 20.00 = {turn_area:,.2f} sq ft"),
            ("Saplings (orchard and grove), kitchen-garden beds, swales dug by hand", 1, "lump sum", 120000, ""),
        ]),
    ]
    rows, subs = [], []
    total = 0
    for g, items in groups:
        st = 0
        for name, q, unit, rate, work in items:
            amt = q * rate
            st += amt
            rows.append((g, name, q, unit, rate, amt, work))
        subs.append((g, st))
        total += st
    fees = 40000
    cont = round(0.05 * (total + fees))
    grand = total + fees + cont
    return dict(rows=rows, subs=subs, works=total, fees=fees, cont=cont, grand=grand)

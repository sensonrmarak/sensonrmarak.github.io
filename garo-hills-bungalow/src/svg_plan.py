"""Plan drawings: main house ground floor, garage block."""
import math
from fractions import Fraction
from data import WALLS, COLUMNS, room_table, garage_table, fi, ff
from openings import MAIN, GARAGE, SCHEDULE
from furniture import furnish


def ftin(inches):
    v = int(round(float(inches)))
    return f"{v // 12}'{v % 12}\""


SERIF = "Georgia, 'Times New Roman', serif"


def label(cx, cy, name, dims, fs=7):
    w = len(name) * fs * 0.62
    return (f'<text x="{cx:.1f}" y="{cy:.1f}" font-size="{fs}" font-weight="bold" fill="#1f1f1f" text-anchor="middle" font-family="{SERIF}" letter-spacing="0.3">{name}</text>'
            f'<line x1="{cx-w/2:.1f}" y1="{cy+1.6:.1f}" x2="{cx+w/2:.1f}" y2="{cy+1.6:.1f}" stroke="#1f1f1f" stroke-width="0.6"/>'
            f'<text x="{cx:.1f}" y="{cy+fs+1.5:.1f}" font-size="{fs*0.8:.1f}" fill="#1f1f1f" text-anchor="middle" font-family="{SERIF}">{dims}</text>')


NAME = {"STDY": "STUDY", "LIB": "LIBRARY", "BTH1": "BATH 1",
        "DRS1": "DRESS 1", "BED1": "BEDROOM #1", "FOY": "FOYER", "HALL": "SITTING HALL", "DIN": "DINING",
        "ALC": "BAR ALCOVE", "KIT": "KITCHEN", "STR": "STORE", "UTL": "UTILITY", "WLB": "WASH",
        "SWC": "TOILET", "SBT": "BATH", "DRS2": "DRESS 2", "BTH2": "BATH 2", "BED2": "BEDROOM #2"}
LABEL_AT = {"STDY": (9, 8.2, 7), "LIB": (25.2, 11.2, 6.4),
            "BTH1": (5.6, 18.6, 5), "DRS1": (13, 19.3, 5.6), "BED1": (5.6, 29.5, 7.5), "FOY": (41, 7.5, 7),
            "HALL": (34, 17.2, 9), "DIN": (56, 15.6, 7), "ALC": (56, 7.4, 6.4), "KIT": (71, 22.6, 7.5),
            "STR": (67.8, 8.5, 6), "UTL": (77, 8.5, 6), "WLB": (86.3, 11.6, 4.6),
            "SWC": (92.6, 4.4, 5), "SBT": (91.3, 9.2, 5), "DRS2": (86, 21.0, 5.4), "BTH2": (91.8, 18.8, 5),
            "BED2": (92.2, 29.8, 7.5)}

INK = "#2b2b2b"
WALLC = "#3a3a3a"
FILL = "#fbf8f1"


def _f(v):
    return f"{float(v):.2f}"


def draw_walls(walls, S, ox, oy):
    out = []
    for x0, y0, x1, y1, t, _ in walls:
        h = Fraction(t) / 12 / 2      # half thickness in ft
        if y0 == y1:
            xa, xb = min(x0, x1) - h, max(x0, x1) + h
            out.append(f'<rect x="{_f(ox+xa*S)}" y="{_f(oy+(y0-h)*S)}" width="{_f((xb-xa)*S)}" height="{_f(2*h*S)}" fill="{WALLC}"/>')
        else:
            ya, yb = min(y0, y1) - h, max(y0, y1) + h
            out.append(f'<rect x="{_f(ox+(x0-h)*S)}" y="{_f(oy+ya*S)}" width="{_f(2*h*S)}" height="{_f((yb-ya)*S)}" fill="{WALLC}"/>')
    return out


def wall_t(walls, ori, c, a):
    for x0, y0, x1, y1, t, _ in walls:
        if ori == "h" and y0 == y1 == c and min(x0, x1) <= a <= max(x0, x1):
            return Fraction(t) / 12
        if ori == "v" and x0 == x1 == c and min(y0, y1) <= a <= max(y0, y1):
            return Fraction(t) / 12
    return Fraction(3, 4)


def draw_openings(ops, walls, S, ox, oy):
    out = []
    for mark, ori, c, a, side in ops:
        w = SCHEDULE[mark][2] / 12
        t = float(wall_t(walls, ori, c, a))
        door = mark.startswith(("D", "FD", "SD", "GD"))
        a0, a1 = a - w / 2, a + w / 2
        # cut the wall
        if ori == "h":
            out.append(f'<rect x="{_f(ox+a0*S)}" y="{_f(oy+(c-t/2)*S-0.6)}" width="{_f(w*S)}" height="{_f(t*S+1.2)}" fill="{FILL}"/>')
        else:
            out.append(f'<rect x="{_f(ox+(c-t/2)*S-0.6)}" y="{_f(oy+a0*S)}" width="{_f(t*S+1.2)}" height="{_f(w*S)}" fill="{FILL}"/>')
        if not door or mark == "SL1":
            # window: three parallel lines through wall
            for k in (-0.5, 0, 0.5):
                if ori == "h":
                    yy = oy + (c + k * t * 0.8) * S
                    out.append(f'<line x1="{_f(ox+a0*S)}" y1="{_f(yy)}" x2="{_f(ox+a1*S)}" y2="{_f(yy)}" stroke="{INK}" stroke-width="0.7"/>')
                else:
                    xx = ox + (c + k * t * 0.8) * S
                    out.append(f'<line x1="{_f(xx)}" y1="{_f(oy+a0*S)}" x2="{_f(xx)}" y2="{_f(oy+a1*S)}" stroke="{INK}" stroke-width="0.7"/>')
            continue
        if mark.startswith("GD"):
            if ori == "h":
                out.append(f'<line x1="{_f(ox+a0*S)}" y1="{_f(oy+c*S)}" x2="{_f(ox+a1*S)}" y2="{_f(oy+c*S)}" stroke="{INK}" stroke-width="0.8" stroke-dasharray="4 3"/>')
            continue
        leaves = [(a0, w / 2, 1), (a1, w / 2, -1)] if mark in ("FD1", "D5") else [(a0, w, 1)]
        for hinge, lw, dirn in leaves:
            off = side * (t / 2)
            if ori == "h":
                hx, hy = ox + hinge * S, oy + (c + off) * S
                ex, ey = hx, hy + side * lw * S
                ax, ay = hx + dirn * lw * S, hy
                sweep = 1 if (side * dirn) > 0 else 0
                out.append(f'<line x1="{_f(hx)}" y1="{_f(hy)}" x2="{_f(ex)}" y2="{_f(ey)}" stroke="{INK}" stroke-width="1"/>')
                out.append(f'<path d="M {_f(ex)} {_f(ey)} A {_f(lw*S)} {_f(lw*S)} 0 0 {sweep} {_f(ax)} {_f(ay)}" fill="none" stroke="{INK}" stroke-width="0.5" stroke-dasharray="2 2"/>')
            else:
                hx, hy = ox + (c + off) * S, oy + hinge * S
                ex, ey = hx + side * lw * S, hy
                ax, ay = hx, hy + dirn * lw * S
                sweep = 0 if (side * dirn) > 0 else 1
                out.append(f'<line x1="{_f(hx)}" y1="{_f(hy)}" x2="{_f(ex)}" y2="{_f(ey)}" stroke="{INK}" stroke-width="1"/>')
                out.append(f'<path d="M {_f(ex)} {_f(ey)} A {_f(lw*S)} {_f(lw*S)} 0 0 {sweep} {_f(ax)} {_f(ay)}" fill="none" stroke="{INK}" stroke-width="0.5" stroke-dasharray="2 2"/>')
    return out


def tag(x, y, text, size=8, weight="normal", fill=INK, anchor="middle"):
    return f'<text x="{_f(x)}" y="{_f(y)}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" font-family="Helvetica, Arial, sans-serif">{text}</text>'


SHORT = {"SWC": "TOILET", "SBT": "BATH", "STU": "MUSIC STUDIO", "AIRL": "AIRLOCK", "STDY": "STUDY", "DRS1": "DRESS 1", "WLB": "WASH",
         "BED1": "BEDROOM 1", "WIC1": "DRESS 1", "BTH1": "BATH 1", "LIB": "LIBRARY", "FOY": "FOYER",
         "HALL": "SITTING HALL", "DIN": "DINING", "ALC": "ALCOVE", "KIT": "KITCHEN", "STR": "STORE",
         "UTL": "UTILITY", "PAS": "PASSAGE", "SWC": "WC", "SBT": "SHARED BATH", "DRS2": "DRESS 2",
         "BTH2": "BATH 2", "BED2": "BEDROOM 2"}


def dim_h(x0, x1, y, S, ox, oy, label):
    X0, X1, Y = ox + x0 * S, ox + x1 * S, oy + y * S
    return [f'<line x1="{_f(X0)}" y1="{_f(Y)}" x2="{_f(X1)}" y2="{_f(Y)}" stroke="#8a6d3b" stroke-width="0.6"/>',
            f'<line x1="{_f(X0)}" y1="{_f(Y-3)}" x2="{_f(X0)}" y2="{_f(Y+3)}" stroke="#8a6d3b" stroke-width="0.6"/>',
            f'<line x1="{_f(X1)}" y1="{_f(Y-3)}" x2="{_f(X1)}" y2="{_f(Y+3)}" stroke="#8a6d3b" stroke-width="0.6"/>',
            tag((X0 + X1) / 2, Y - 2.5, label, 6.2, fill="#7a5a20")]


def dim_v(y0, y1, x, S, ox, oy, label):
    Y0, Y1, X = oy + y0 * S, oy + y1 * S, ox + x * S
    cx, cy = X - 2.5, (Y0 + Y1) / 2
    return [f'<line x1="{_f(X)}" y1="{_f(Y0)}" x2="{_f(X)}" y2="{_f(Y1)}" stroke="#8a6d3b" stroke-width="0.6"/>',
            f'<line x1="{_f(X-3)}" y1="{_f(Y0)}" x2="{_f(X+3)}" y2="{_f(Y0)}" stroke="#8a6d3b" stroke-width="0.6"/>',
            f'<line x1="{_f(X-3)}" y1="{_f(Y1)}" x2="{_f(X+3)}" y2="{_f(Y1)}" stroke="#8a6d3b" stroke-width="0.6"/>',
            f'<text x="{_f(cx)}" y="{_f(cy)}" font-size="6.2" fill="#7a5a20" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" transform="rotate(-90 {_f(cx)} {_f(cy)})">{label}</text>']


def main_plan():
    S = 8.4
    ox, oy = 46, 290
    W, H = ox + 98 * S + 40, oy + 40 * S + 190
    o = [f'<svg viewBox="0 0 {W:.0f} {H:.0f}" xmlns="http://www.w3.org/2000/svg" class="dwg">',
         f'<rect width="{W:.0f}" height="{H:.0f}" fill="{FILL}"/>']
    # verandas and porch: blue, as decks on a presentation plan
    BLUE, BLUE_E = "#b9dcf2", "#7fb3d8"
    o.append(f'<rect x="{_f(ox-0.5*S)}" y="{_f(oy+40*S)}" width="{_f(99*S)}" height="{_f(9*S)}" fill="{BLUE}" stroke="{BLUE_E}" stroke-width="0.6"/>')
    o.append(f'<rect x="{_f(ox+18*S)}" y="{_f(oy-8*S)}" width="{_f(44*S)}" height="{_f(8*S)}" fill="{BLUE}" stroke="{BLUE_E}" stroke-width="0.6"/>')
    o.append(f'<rect x="{_f(ox+31*S)}" y="{_f(oy-22*S)}" width="{_f(20*S)}" height="{_f(14*S)}" fill="#d6e9f5" stroke="{BLUE_E}" stroke-width="0.6"/>')
    for i in range(8):
        o.append(f'<line x1="{_f(ox+16*S)}" y1="{_f(oy+(49.4+i*1.0)*S)}" x2="{_f(ox+34*S)}" y2="{_f(oy+(49.4+i*1.0)*S)}" stroke="#7fae6a" stroke-width="0.8"/>')
    o.append(f'<rect x="{_f(ox+16*S)}" y="{_f(oy+49*S)}" width="{_f(18*S)}" height="{_f(8.4*S)}" fill="#cfe5c0" fill-opacity="0.55" stroke="#7fae6a" stroke-width="0.8"/>')
    o.append(f'<rect x="{_f(ox+62*S)}" y="{_f(oy-12*S)}" width="{_f(20*S)}" height="{_f(12*S)}" fill="#f1efe9" stroke="#9a8f7a" stroke-width="1.2" stroke-dasharray="5 3"/>')
    o.append(tag(ox + 72 * S, oy - 6 * S, "UTILITY YARD", 6.5, fill="#6b6253"))
    o.append(tag(ox + 72 * S, oy - 6 * S + 8, "6'6\" screen wall", 5.5, fill="#6b6253"))
    for x in range(0, 99, 11):
        o.append(f'<rect x="{_f(ox+(x-0.6)*S)}" y="{_f(oy+(49-0.6)*S)}" width="{_f(1.2*S)}" height="{_f(1.2*S)}" fill="#111"/>')
    for x in (18, 29, 40, 51, 62):
        o.append(f'<rect x="{_f(ox+(x-0.6)*S)}" y="{_f(oy-8.6*S)}" width="{_f(1.2*S)}" height="{_f(1.2*S)}" fill="#111"/>')
    for x, y in ((31, -22), (51, -22), (31, -15), (51, -15)):
        o.append(f'<rect x="{_f(ox+(x-0.6)*S)}" y="{_f(oy+(y-0.6)*S)}" width="{_f(1.2*S)}" height="{_f(1.2*S)}" fill="#111"/>')
    o.append(label(ox + 49 * S, oy + 47.2 * S, "SOUTH VERANDA", "98'0\" X 9'0\"", 8))
    o.append(tag(ox + 25 * S, oy + 56.0 * S, "8 steps down to garden", 5.6, fill="#3d5a2a"))
    o.append(label(ox + 41 * S, oy - 18.6 * S, "CAR PORCH", "20'0\" X 14'0\"", 7.5))
    o.append(label(ox + 24.5 * S, oy - 3.6 * S, "NORTH VERANDA", "44'0\" X 8'0\"", 6.4))
    # floor fill for rooms (warm yellow, as on a presentation plan)
    for r in room_table():
        o.append(f'<rect x="{_f(ox+r["x0"]*S)}" y="{_f(oy+r["y0"]*S)}" width="{_f((r["x1"]-r["x0"])*S)}" height="{_f((r["y1"]-r["y0"])*S)}" fill="#f8efbf"/>')
    o += furnish(S, ox, oy)
    o += draw_walls(WALLS, S, ox, oy)
    for x, y in COLUMNS:
        vert = x in (0, 98, 18) or (x, y) in ((62, 17), (80, 17), (80, 24))
        cw, ch = (1.0, 1.5) if vert else (1.5, 1.0)
        o.append(f'<rect x="{_f(ox+(x-cw/2)*S)}" y="{_f(oy+(y-ch/2)*S)}" width="{_f(cw*S)}" height="{_f(ch*S)}" fill="#000"/>')
    o.append(f'<rect x="{_f(ox-1.4*S)}" y="{_f(oy-1.6*S)}" width="{_f(34.8*S)}" height="{_f(16*S)}" fill="none" stroke="#7b5ea7" stroke-width="1.4" stroke-dasharray="7 4"/>')
    o.append(tag(ox + 9 * S, oy - 2.4 * S, "LIBRARY + STUDY SUITE", 6.4, "bold", "#7b5ea7"))
    o.append(f'<rect x="{_f(ox+80.6*S)}" y="{_f(oy-1.6*S)}" width="{_f(18.8*S)}" height="{_f(16*S)}" fill="none" stroke="#1d7a8c" stroke-width="1.4" stroke-dasharray="7 4"/>')
    o.append(tag(ox + 90 * S, oy - 2.4 * S, "WET CORNER: TOILET + BATH", 6.4, "bold", "#1d7a8c"))
    o += draw_openings(MAIN, WALLS, S, ox, oy)
    # labels: underlined room name, clear size below
    for r in room_table():
        if r["key"] not in LABEL_AT:
            continue
        lx, ly, fs = LABEL_AT[r["key"]]
        o.append(label(ox + lx * S, oy + ly * S, NAME[r["key"]], f'{ftin(r["w"])} X {ftin(r["d"])}', fs))
    o.append(tag(ox + 76 * S, oy + 15.4 * S, "PASSAGE 3'6\"", 5.6, "bold"))
    # grid dimensions, centre line
    xs = [0, 8, 18, 32, 50, 62, 72, 82, 88, 90, 98]
    for a, b in zip(xs, xs[1:]):
        o += dim_h(a, b, -27, S, ox, oy, ff(b - a, 0))
    o += dim_h(0, 98, -30.5, S, ox, oy, "98 ft 0 in overall on centre lines (outer face 98 ft 9 in)")
    ys = [0, 13, 22, 40]
    for a, b in zip(ys, ys[1:]):
        o += dim_v(a, b, -2.6, S, ox, oy, ff(b - a, 0))
    o += dim_v(0, 40, -4.6, S, ox, oy, "40 ft 0 in CL")
    for x in (0, 18, 32, 50, 62, 80, 98):
        o.append(tag(ox + x * S, oy + 60 * S, f"{x}", 6.5, "bold", "#1d4e89"))
    o.append(tag(ox + 49 * S, oy + 62.5 * S, "Grid line offsets in feet, measured east from the west wall centre line. Black = 9 in wall, grey = 4½ in partition shown at true thickness; black squares = RCC columns 12 in x 18 in.", 6.2, fill="#333"))
    o.append(tag(ox + 49 * S, oy + 64 * S + 3, "FFL +2 ft 6 in above finished ground at the north porch. Bath, WC, utility, store floors 1 in below room FFL with 1 in 60 falls to floor traps.", 6.2, fill="#333"))
    # north arrow
    nx, ny = W - 34, 40
    o.append(f'<path d="M {nx} {ny-16} L {nx-7} {ny+8} L {nx} {ny+3} L {nx+7} {ny+8} Z" fill="{INK}"/>')
    o.append(tag(nx, ny - 20, "N", 9, "bold"))
    o.append("</svg>")
    return "\n".join(o)


GARAGE_WALLS = [
    (0, 0, 41, 0, 9, ""), (0, 23, 41, 23, 9, ""), (0, 0, 0, 23, 9, ""), (41, 19, 41, 23, 9, ""),
    (41, 0, 41, 19, 9, ""),
    (21, 0, 21, 23, 4.5, ""), (30, 0, 30, 23, 9, ""), (30, 13, 41, 13, 4.5, ""),
]


def garage_plan():
    S = 7.2
    ox, oy = 40, 70
    W, H = ox + 41 * S + 60, oy + 23 * S + 70
    o = [f'<svg viewBox="0 0 {W:.0f} {H:.0f}" xmlns="http://www.w3.org/2000/svg" class="dwg">',
         f'<rect width="{W:.0f}" height="{H:.0f}" fill="{FILL}"/>']
    for r in garage_table():
        o.append(f'<rect x="{_f(ox+r["x0"]*S)}" y="{_f(oy+r["y0"]*S)}" width="{_f((r["x1"]-r["x0"])*S)}" height="{_f((r["y1"]-r["y0"])*S)}" fill="#f3efe6"/>')
    o += draw_walls(GARAGE_WALLS, S, ox, oy)
    o += draw_openings(GARAGE, GARAGE_WALLS, S, ox, oy)
    for r in garage_table():
        cx = ox + (r["x0"] + r["x1"]) / 2 * S
        cy = oy + (r["y0"] + r["y1"]) / 2 * S
        nm = {"GAR": "GARAGE (2 CARS)", "TWB": "2-WHEELER", "TST": "TOOL STORE", "GEN": "GENERATOR"}[r["key"]]
        o.append(tag(cx, cy - 2, nm, 7, "bold"))
        o.append(tag(cx, cy + 7, f'{fi(r["w"])} x {fi(r["d"])}', 5.8))
    xs = [0, 21, 30, 41]
    for a, b in zip(xs, xs[1:]):
        o += dim_h(a, b, -3, S, ox, oy, ff(b - a, 0))
    o += dim_v(0, 23, -3, S, ox, oy, "23 ft 0 in CL")
    o.append(tag(ox + 35.5 * S, oy + 26.6 * S, "covered link walk 6 ft wide to north veranda of house", 6, fill="#5b4a2a"))
    o.append(tag(ox + 10.5 * S, oy - 5.4 * S, "drive apron, falls 1 in 60 away from door", 6, fill="#5b4a2a"))
    o.append("</svg>")
    return "\n".join(o)

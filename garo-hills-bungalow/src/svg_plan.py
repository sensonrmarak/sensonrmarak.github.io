"""Plan drawings: main house ground floor, garage + studio block."""
import math
from fractions import Fraction
from data import WALLS, COLUMNS, room_table, garage_table, fi, ff
from openings import MAIN, GARAGE, SCHEDULE

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
    ox, oy = 46, 335
    W, H = ox + 98 * S + 40, oy + 40 * S + 160
    o = [f'<svg viewBox="0 0 {W:.0f} {H:.0f}" xmlns="http://www.w3.org/2000/svg" class="dwg">',
         f'<rect width="{W:.0f}" height="{H:.0f}" fill="{FILL}"/>']
    # verandas and porch (light tint, columns as white circles)
    o.append(f'<rect x="{_f(ox-0.5*S)}" y="{_f(oy+40*S)}" width="{_f(99*S)}" height="{_f(9*S)}" fill="#efe6d2" stroke="#c8b892" stroke-width="0.5"/>')
    o.append(f'<rect x="{_f(ox+18*S)}" y="{_f(oy-8*S)}" width="{_f(44*S)}" height="{_f(8*S)}" fill="#efe6d2" stroke="#c8b892" stroke-width="0.5"/>')
    o.append(f'<rect x="{_f(ox+31*S)}" y="{_f(oy-22*S)}" width="{_f(20*S)}" height="{_f(14*S)}" fill="#e8dcc0" stroke="#c8b892" stroke-width="0.5"/>')
    o.append(f'<rect x="{_f(ox+62*S)}" y="{_f(oy-12*S)}" width="{_f(18*S)}" height="{_f(12*S)}" fill="none" stroke="#9a8f7a" stroke-width="1.2" stroke-dasharray="5 3"/>')
    o.append(tag(ox + 71 * S, oy - 6 * S, "UTILITY YARD", 6.5, fill="#6b6253"))
    o.append(tag(ox + 71 * S, oy - 6 * S + 8, "6 ft 6 in screen wall", 5.5, fill="#6b6253"))
    for x in range(0, 99, 11):
        o.append(f'<circle cx="{_f(ox+x*S)}" cy="{_f(oy+49*S)}" r="{_f(0.67*S)}" fill="#fff" stroke="{INK}" stroke-width="0.8"/>')
    for x in (18, 29, 40, 51, 62):
        o.append(f'<circle cx="{_f(ox+x*S)}" cy="{_f(oy-8*S)}" r="{_f(0.67*S)}" fill="#fff" stroke="{INK}" stroke-width="0.8"/>')
    for x, y in ((31, -22), (51, -22), (31, -15), (51, -15)):
        o.append(f'<circle cx="{_f(ox+x*S)}" cy="{_f(oy+y*S)}" r="{_f(0.67*S)}" fill="#fff" stroke="{INK}" stroke-width="0.8"/>')
    o.append(tag(ox + 49 * S, oy + 45.4 * S, "SOUTH VERANDA, 9 ft 0 in deep to column line, 8 risers down to garden", 7, "bold", "#5b4a2a"))
    o.append(tag(ox + 41 * S, oy - 18.3 * S, "CAR PORCH 20 ft 0 in x 14 ft 0 in", 7, "bold", "#5b4a2a"))
    o.append(tag(ox + 41 * S, oy - 17 * S + 4, "drive passes under, east to west", 6, fill="#5b4a2a"))
    o.append(tag(ox + 24 * S, oy - 3.4 * S, "NORTH VERANDA 8 ft 0 in", 6.5, "bold", "#5b4a2a"))
    # floor tint for rooms
    for r in room_table():
        o.append(f'<rect x="{_f(ox+r["x0"]*S)}" y="{_f(oy+r["y0"]*S)}" width="{_f((r["x1"]-r["x0"])*S)}" height="{_f((r["y1"]-r["y0"])*S)}" fill="{"#f3efe6" if r["hab"] else "#eef1f2"}"/>')
    o += draw_walls(WALLS, S, ox, oy)
    for x, y in COLUMNS:
        vert = x in (0, 98, 18) or (x, y) in ((62, 17), (80, 17), (80, 24))
        cw, ch = (1.0, 1.5) if vert else (1.5, 1.0)
        o.append(f'<rect x="{_f(ox+(x-cw/2)*S)}" y="{_f(oy+(y-ch/2)*S)}" width="{_f(cw*S)}" height="{_f(ch*S)}" fill="#000"/>')
    L = 13 / 24
    pts = [(L, -27 + L), (18 - L - 0.9, -27 + L), (18 - L, -7 - L), (L, -7 - L - 0.7)]
    o.append('<polygon points="' + " ".join(f"{_f(ox+x*S)},{_f(oy+y*S)}" for x, y in pts) + '" fill="none" stroke="#8a4b2a" stroke-width="1.2" stroke-dasharray="3 2"/>')
    o.append(f'<rect x="{_f(ox-1.4*S)}" y="{_f(oy-28.4*S)}" width="{_f(34.8*S)}" height="{_f(42.8*S)}" fill="none" stroke="#7b5ea7" stroke-width="1.4" stroke-dasharray="7 4"/>')
    o.append(tag(ox + 25 * S, oy - 24.5 * S, "CREATIVE SUITE", 7.5, "bold", "#7b5ea7"))
    o.append(tag(ox + 25 * S, oy - 24.5 * S + 9, "studio + study + library", 6.2, "normal", "#7b5ea7"))
    o.append(f'<rect x="{_f(ox+80.6*S)}" y="{_f(oy-1.6*S)}" width="{_f(18.8*S)}" height="{_f(16*S)}" fill="none" stroke="#1d7a8c" stroke-width="1.4" stroke-dasharray="7 4"/>')
    o.append(tag(ox + 90 * S, oy - 2.4 * S, "WET CORNER", 7, "bold", "#1d7a8c"))
    o += draw_openings(MAIN, WALLS, S, ox, oy)
    # labels
    for r in room_table():
        cx = ox + (r["x0"] + r["x1"]) / 2 * S
        cy = oy + (r["y0"] + r["y1"]) / 2 * S
        if r["key"] == "PAS":
            o.append(tag(cx + 30, cy + 2.5, "PASSAGE 3 ft 6 in clear", 5.6, "bold"))
            continue
        big = r["key"] in ("HALL", "BED1", "BED2", "KIT", "DIN", "STU")
        fs = 8 if big else 6
        if r["key"] in ("WLB", "BTH2"):
            o.append(f'<g transform="rotate(-90 {_f(cx)} {_f(cy)})">{tag(cx, cy - 1, SHORT[r["key"]], 6, "bold")}{tag(cx, cy + 6.5, fi(r["w"]) + " x " + fi(r["d"]), 5)}</g>')
            continue
        o.append(tag(cx, cy - 2, SHORT[r["key"]], fs, "bold"))
        o.append(tag(cx, cy + fs, f'{fi(r["w"])} x {fi(r["d"])}', fs - 1.5))
        if big:
            o.append(tag(cx, cy + 2 * fs + 1, f'{r["area"]} sq ft', fs - 2, fill="#7a5a20"))
    o.append(tag(ox + 34 * S, oy + 30 * S, "open to dining and kitchen: no partitions,", 5.8, fill="#555"))
    o.append(tag(ox + 34 * S, oy + 30 * S + 7, "spaces defined by columns, rug and vaulted ceiling", 5.8, fill="#555"))
    o.append(tag(ox + 71 * S, oy + 37.6 * S, "island 8 ft 0 in x 3 ft 6 in", 5.6, fill="#555"))
    o.append(f'<rect x="{_f(ox+67*S)}" y="{_f(oy+32.5*S)}" width="{_f(8*S)}" height="{_f(3.5*S)}" fill="none" stroke="#777" stroke-width="0.7"/>')
    o.append(f'<rect x="{_f(ox+62.4*S)}" y="{_f(oy+17.4*S)}" width="{_f(17.2*S)}" height="{_f(2*S)}" fill="none" stroke="#777" stroke-width="0.6"/>')
    o.append(tag(ox + 71 * S, oy + 18.9 * S, "counter 2 ft 0 in deep, hob + chimney", 5.2, fill="#555"))
    # grid dimensions, centre line
    xs = [0, 8, 18, 32, 50, 62, 72, 80, 86, 90, 98]
    for a, b in zip(xs, xs[1:]):
        o += dim_h(a, b, -33, S, ox, oy, ff(b - a, 0))
    o += dim_h(0, 98, -36.5, S, ox, oy, "98 ft 0 in overall on centre lines (outer face 98 ft 9 in)")
    ys = [-27, -7, 0, 13, 22, 40]
    for a, b in zip(ys, ys[1:]):
        o += dim_v(a, b, -2.6, S, ox, oy, ff(b - a, 0))
    o += dim_v(-27, 40, -4.6, S, ox, oy, "67 ft 0 in CL, west face")
    for x in (0, 18, 32, 50, 62, 80, 98):
        o.append(tag(ox + x * S, oy + 52.5 * S, f"{x}", 6.5, "bold", "#1d4e89"))
    o.append(tag(ox + 49 * S, oy + 55 * S, "Grid line offsets in feet, measured east from the west wall centre line. Black = 9 in wall, grey = 4½ in partition shown at true thickness; black squares = RCC columns 12 in x 18 in.", 6.2, fill="#333"))
    o.append(tag(ox + 49 * S, oy + 56.5 * S + 3, "FFL +2 ft 6 in above finished ground at the north porch. Bath, WC, utility, store floors 1 in below room FFL with 1 in 60 falls to floor traps.", 6.2, fill="#333"))
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

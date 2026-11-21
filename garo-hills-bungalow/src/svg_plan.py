"""Furnished presentation plan of the budget house. All dimensions in decimal feet."""
from data import WALLS, COLUMNS, room_table, VERANDA, PORCH
from openings import MAIN, SCHEDULE
from furniture import furnish

INK = "#2b2b2b"
WALLC = "#2a2a2a"
FILL = "#fbf8f1"
SERIF = "Georgia, 'Times New Roman', serif"


def _f(v):
    return f"{float(v):.2f}"


def tag(x, y, text, size=8, weight="normal", fill=INK, anchor="middle"):
    return f'<text x="{_f(x)}" y="{_f(y)}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" font-family="Helvetica, Arial, sans-serif">{text}</text>'


def label(cx, cy, name, dims, fs=7):
    w = len(name) * fs * 0.62
    return (f'<text x="{cx:.1f}" y="{cy:.1f}" font-size="{fs}" font-weight="bold" fill="#1f1f1f" text-anchor="middle" font-family="{SERIF}" letter-spacing="0.3">{name}</text>'
            f'<line x1="{cx-w/2:.1f}" y1="{cy+1.6:.1f}" x2="{cx+w/2:.1f}" y2="{cy+1.6:.1f}" stroke="#1f1f1f" stroke-width="0.6"/>'
            f'<text x="{cx:.1f}" y="{cy+fs+1.5:.1f}" font-size="{fs*0.8:.1f}" fill="#1f1f1f" text-anchor="middle" font-family="{SERIF}">{dims}</text>')


def draw_walls(walls, S, ox, oy):
    out = []
    for x0, y0, x1, y1, t, _ in walls:
        h = t / 2
        if y0 == y1:
            xa, xb = min(x0, x1) - h, max(x0, x1) + h
            out.append(f'<rect x="{_f(ox+xa*S)}" y="{_f(oy+(y0-h)*S)}" width="{_f((xb-xa)*S)}" height="{_f(2*h*S)}" fill="{WALLC}"/>')
        else:
            ya, yb = min(y0, y1) - h, max(y0, y1) + h
            out.append(f'<rect x="{_f(ox+(x0-h)*S)}" y="{_f(oy+ya*S)}" width="{_f(2*h*S)}" height="{_f((yb-ya)*S)}" fill="{WALLC}"/>')
    return out


def wall_t(ori, c, a):
    for x0, y0, x1, y1, t, _ in WALLS:
        if ori == "h" and y0 == y1 == c and min(x0, x1) <= a <= max(x0, x1):
            return t
        if ori == "v" and x0 == x1 == c and min(y0, y1) <= a <= max(y0, y1):
            return t
    return 0.75


def draw_openings(S, ox, oy, floor="#f8efbf"):
    out = []
    for mark, ori, c, a, side in MAIN:
        w = SCHEDULE[mark][2]
        t = wall_t(ori, c, a)
        a0, a1 = a - w / 2, a + w / 2
        if ori == "h":
            out.append(f'<rect x="{_f(ox+a0*S)}" y="{_f(oy+(c-t/2)*S-0.6)}" width="{_f(w*S)}" height="{_f(t*S+1.2)}" fill="{floor}"/>')
        else:
            out.append(f'<rect x="{_f(ox+(c-t/2)*S-0.6)}" y="{_f(oy+a0*S)}" width="{_f(t*S+1.2)}" height="{_f(w*S)}" fill="{floor}"/>')
        if mark == "OP":
            continue
        if mark.startswith("W"):
            for k in (-0.5, 0, 0.5):
                if ori == "h":
                    yy = oy + (c + k * t * 0.8) * S
                    out.append(f'<line x1="{_f(ox+a0*S)}" y1="{_f(yy)}" x2="{_f(ox+a1*S)}" y2="{_f(yy)}" stroke="{INK}" stroke-width="0.7"/>')
                else:
                    xx = ox + (c + k * t * 0.8) * S
                    out.append(f'<line x1="{_f(xx)}" y1="{_f(oy+a0*S)}" x2="{_f(xx)}" y2="{_f(oy+a1*S)}" stroke="{INK}" stroke-width="0.7"/>')
            continue
        leaves = [(a0, w / 2, 1), (a1, w / 2, -1)] if mark == "FD1" else [(a0, w, 1)]
        for hinge, lw, dirn in leaves:
            off = side * (t / 2)
            if ori == "h":
                hx, hy = ox + hinge * S, oy + (c + off) * S
                ex, ey = hx, hy + side * lw * S
                ax, ay = hx + dirn * lw * S, hy
                sweep = 1 if (side * dirn) > 0 else 0
            else:
                hx, hy = ox + (c + off) * S, oy + hinge * S
                ex, ey = hx + side * lw * S, hy
                ax, ay = hx, hy + dirn * lw * S
                sweep = 0 if (side * dirn) > 0 else 1
            out.append(f'<line x1="{_f(hx)}" y1="{_f(hy)}" x2="{_f(ex)}" y2="{_f(ey)}" stroke="{INK}" stroke-width="1"/>')
            out.append(f'<path d="M {_f(ex)} {_f(ey)} A {_f(lw*S)} {_f(lw*S)} 0 0 {sweep} {_f(ax)} {_f(ay)}" fill="none" stroke="{INK}" stroke-width="0.5" stroke-dasharray="2 2"/>')
    return out


def dim_h(x0, x1, y, S, ox, oy, text):
    X0, X1, Y = ox + x0 * S, ox + x1 * S, oy + y * S
    c = "#8a6d3b"
    return [f'<line x1="{_f(X0)}" y1="{_f(Y)}" x2="{_f(X1)}" y2="{_f(Y)}" stroke="{c}" stroke-width="0.6"/>',
            f'<line x1="{_f(X0)}" y1="{_f(Y-3)}" x2="{_f(X0)}" y2="{_f(Y+3)}" stroke="{c}" stroke-width="0.6"/>',
            f'<line x1="{_f(X1)}" y1="{_f(Y-3)}" x2="{_f(X1)}" y2="{_f(Y+3)}" stroke="{c}" stroke-width="0.6"/>',
            tag((X0 + X1) / 2, Y - 2.5, text, 6.4, fill="#7a5a20")]


def dim_v(y0, y1, x, S, ox, oy, text):
    Y0, Y1, X = oy + y0 * S, oy + y1 * S, ox + x * S
    c = "#8a6d3b"
    cx, cy = X - 2.5, (Y0 + Y1) / 2
    return [f'<line x1="{_f(X)}" y1="{_f(Y0)}" x2="{_f(X)}" y2="{_f(Y1)}" stroke="{c}" stroke-width="0.6"/>',
            f'<line x1="{_f(X-3)}" y1="{_f(Y0)}" x2="{_f(X+3)}" y2="{_f(Y0)}" stroke="{c}" stroke-width="0.6"/>',
            f'<line x1="{_f(X-3)}" y1="{_f(Y1)}" x2="{_f(X+3)}" y2="{_f(Y1)}" stroke="{c}" stroke-width="0.6"/>',
            f'<text x="{_f(cx)}" y="{_f(cy)}" font-size="6.4" fill="#7a5a20" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" transform="rotate(-90 {_f(cx)} {_f(cy)})">{text}</text>']


NAME = {"LIB": "LIBRARY + STUDY", "BTH1": "BATH 1", "DRS1": "DRESS 1", "BED1": "BEDROOM #1", "LIV": "SITTING + DINING",
        "WLB": "WASH", "SWB": "TOILET + BATH", "KIT": "KITCHEN", "BED2": "BEDROOM #2", "BTH2": "BATH 2", "WRD2": "WARDROBE"}
LABEL_AT = {"LIB": (9.2, 6.2, 7.2), "BTH1": (2.4, 14.6, 5.0), "DRS1": (10.0, 15.6, 5.6), "BED1": (4.2, 24.2, 7.5),
            "LIV": (19.0, 14.9, 8.4), "WLB": (32.0, 6.0, 4.6), "SWB": (38.8, 5.4, 5.6), "KIT": (36.4, 13.0, 7.5),
            "BED2": (34.0, 24.6, 6.8), "BTH2": (41.9, 21.4, 4.4), "WRD2": (42.0, 25.6, 4.4)}


def main_plan():
    S = 17.0
    ox, oy = 70, 300
    W, H = ox + 46 * S + 140, oy + 28 * S + 360
    o = [f'<svg viewBox="0 0 {W:.0f} {H:.0f}" xmlns="http://www.w3.org/2000/svg" class="dwg">',
         f'<rect width="{W:.0f}" height="{H:.0f}" fill="{FILL}"/>']
    BLUE, EDGE = "#b9dcf2", "#7fb3d8"
    o.append(f'<rect x="{_f(ox-0.375*S)}" y="{_f(oy+28.375*S)}" width="{_f(VERANDA[0]*S)}" height="{_f(VERANDA[1]*S)}" fill="{BLUE}" stroke="{EDGE}" stroke-width="0.6"/>')
    o.append(f'<rect x="{_f(ox+17*S)}" y="{_f(oy-6.375*S)}" width="{_f(PORCH[0]*S)}" height="{_f(PORCH[1]*S)}" fill="{BLUE}" stroke="{EDGE}" stroke-width="0.6"/>')
    for i in range(4):
        o.append(f'<line x1="{_f(ox+18.5*S)}" y1="{_f(oy-(6.9+i*1.0)*S)}" x2="{_f(ox+25.5*S)}" y2="{_f(oy-(6.9+i*1.0)*S)}" stroke="#7fae6a" stroke-width="0.8"/>')
    o.append(f'<rect x="{_f(ox+18.5*S)}" y="{_f(oy-10.4*S)}" width="{_f(7*S)}" height="{_f(4*S)}" fill="#cfe5c0" fill-opacity="0.55" stroke="#7fae6a" stroke-width="0.8"/>')
    o.append(tag(ox + 22 * S, oy - 10.9 * S, "4 steps up from the drive", 6, fill="#3d5a2a"))
    for i in range(5):
        o.append(f'<line x1="{_f(ox+3*S)}" y1="{_f(oy+(36.6+i*1.0)*S)}" x2="{_f(ox+12*S)}" y2="{_f(oy+(36.6+i*1.0)*S)}" stroke="#7fae6a" stroke-width="0.8"/>')
    o.append(f'<rect x="{_f(ox+3*S)}" y="{_f(oy+36.4*S)}" width="{_f(9*S)}" height="{_f(5.2*S)}" fill="#cfe5c0" fill-opacity="0.55" stroke="#7fae6a" stroke-width="0.8"/>')
    o.append(tag(ox + 7.5 * S, oy + 42.6 * S, "5 steps down to garden", 6, fill="#3d5a2a"))
    for x in (0, 11.5, 23, 34.5, 46):
        o.append(f'<rect x="{_f(ox+(x-0.5)*S)}" y="{_f(oy+(36.375-0.5)*S)}" width="{_f(1.0*S)}" height="{_f(1.0*S)}" fill="#111"/>')
    for x in (17, 27):
        o.append(f'<rect x="{_f(ox+(x-0.4)*S)}" y="{_f(oy-6.8*S)}" width="{_f(0.8*S)}" height="{_f(0.8*S)}" fill="#111"/>')
    o.append(label(ox + 30 * S, oy + 33.4 * S, "SOUTH VERANDA", f"{VERANDA[0]:.2f} X {VERANDA[1]:.2f}", 8))
    o.append(label(ox + 22 * S, oy - 3.4 * S, "ENTRY PORCH", f"{PORCH[0]:.2f} X {PORCH[1]:.2f}", 6.6))
    for r in room_table():
        o.append(f'<rect x="{_f(ox+r["x0"]*S)}" y="{_f(oy+r["y0"]*S)}" width="{_f((r["x1"]-r["x0"])*S)}" height="{_f((r["y1"]-r["y0"])*S)}" fill="#f8efbf"/>')
    o += furnish(S, ox, oy)
    o += draw_walls(WALLS, S, ox, oy)
    for x, y in COLUMNS:
        vert = x in (0, 46, 14, 30)
        cw, ch = (0.75, 1.0) if vert else (1.0, 0.75)
        o.append(f'<rect x="{_f(ox+(x-cw/2)*S)}" y="{_f(oy+(y-ch/2)*S)}" width="{_f(cw*S)}" height="{_f(ch*S)}" fill="#000"/>')
    o += draw_openings(S, ox, oy)
    o.append(f'<rect x="{_f(ox+29.4*S)}" y="{_f(oy-1.0*S)}" width="{_f(17.4*S)}" height="{_f(8.6*S)}" fill="none" stroke="#1d7a8c" stroke-width="1.4" stroke-dasharray="7 4"/>')
    o.append(tag(ox + 40 * S, oy - 1.6 * S, "WET CORNER", 6.6, "bold", "#1d7a8c"))
    for r in room_table():
        lx, ly, fs = LABEL_AT[r["key"]]
        o.append(label(ox + lx * S, oy + ly * S, NAME[r["key"]], f'{r["w"]:.2f} X {r["d"]:.2f}', fs))
    xs = [0, 6, 14, 22, 30, 34, 40.5, 46]
    for a, b in zip(xs, xs[1:]):
        o += dim_h(a, b, -13.2, S, ox, oy, f"{b-a:.2f}")
    o += dim_h(0, 46, -15.6, S, ox, oy, "46.00 ft on centre lines (outer face 46.75 ft)")
    ys = [0, 7, 10, 16, 17, 22, 28]
    for a, b in zip(ys, ys[1:]):
        o += dim_v(a, b, 49.4, S, ox, oy, f"{b-a:.2f}")
    o += dim_v(0, 28, 52.0, S, ox, oy, "28.00 ft CL (outer 28.75 ft)")
    o.append(tag(ox + 23 * S, oy + 45.5 * S, "All sizes in feet. Room sizes are clear (wall face to wall face). Black walls: 0.75 ft external, 0.375 ft internal, true thickness.", 7, fill="#333"))
    o.append(tag(ox + 23 * S, oy + 46.8 * S + 4, "Black squares are RCC columns 0.75 ft x 1.00 ft. Floor level +2.50 ft above ground at the porch. Hall and dining are one open room.", 7, fill="#333"))
    nx, ny = W - 34, 40
    o.append(f'<path d="M {nx} {ny-16} L {nx-7} {ny+8} L {nx} {ny+3} L {nx+7} {ny+8} Z" fill="{INK}"/>')
    o.append(tag(nx, ny - 20, "N", 9, "bold"))
    o.append("</svg>")
    return "\n".join(o)

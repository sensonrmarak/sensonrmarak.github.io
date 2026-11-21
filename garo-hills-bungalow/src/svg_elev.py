"""North elevation, sun section, firehouse and gate drawings."""
import math
from svg_plan import tag, _f, INK, FILL
from openings import MAIN, SCHEDULE
from data import SUN

K = math.tan(math.radians(25))
PLATE = 15.0          # wall plate above FFL, ft
EAVE_NEW = PLATE - 3 * K
VER_LEDGER, VER_EAVE, VER_PROJ = 14 + 2 / 12, 12 + 5 / 12, 10.0
RIDGE = 24.25
CREAM, STONE, ROOF, BLACK, WHITE = "#efe4cc", "#b9ab92", "#3b3d40", "#1c1c1c", "#ffffff"


def _stone(o, x, y, w, h, pid):
    o.append(f'<defs><pattern id="{pid}" width="14" height="8" patternUnits="userSpaceOnUse">'
             f'<rect width="14" height="8" fill="{STONE}"/><path d="M0 4 H14 M7 0 V4 M0 4 V8 M14 4 V8" stroke="#8f8370" stroke-width="0.6"/></pattern></defs>')
    o.append(f'<rect x="{_f(x)}" y="{_f(y)}" width="{_f(w)}" height="{_f(h)}" fill="url(#{pid})" stroke="#7d725f" stroke-width="0.5"/>')


def north_elevation():
    S = 6.6
    ox, base = 34, 230          # base = screen y of FFL
    W, H = ox * 2 + 104 * S, base + 2.5 * S + 46
    X = lambda x: ox + (101 - x) * S        # viewed from north: east on left
    Y = lambda h: base - h * S
    o = [f'<svg viewBox="0 0 {W:.0f} {H:.0f}" xmlns="http://www.w3.org/2000/svg" class="dwg">',
         f'<rect width="{W:.0f}" height="{H:.0f}" fill="#f6f2ea"/>']
    # roof
    pts = [(-3, EAVE_NEW), (21, RIDGE), (77, RIDGE), (101, EAVE_NEW)]
    o.append('<polygon points="' + " ".join(f"{_f(X(x))},{_f(Y(h))}" for x, h in pts) + f'" fill="{ROOF}"/>')
    for x in range(0, 101, 2):
        pass
    o.append(f'<rect x="{_f(X(101))}" y="{_f(Y(EAVE_NEW)-1)}" width="{_f(104*S)}" height="{_f(0.6*S)}" fill="#222"/>')
    # wall + stone base
    o.append(f'<rect x="{_f(X(98.4))}" y="{_f(Y(EAVE_NEW))}" width="{_f(98.8*S)}" height="{_f((EAVE_NEW+2.5)*S)}" fill="{CREAM}"/>')
    _stone(o, X(98.4), Y(1.5), 98.8 * S, 4 * S, "st1")
    o.append(f'<rect x="{_f(X(98.4))}" y="{_f(Y(1.5)-2)}" width="{_f(98.8*S)}" height="3" fill="#d8ccb4"/>')
    # openings on north wall
    for mark, ori, c, a, side in MAIN:
        if ori != "h" or c != 0:
            continue
        _, _, w, h, sill, lintel, *_ = SCHEDULE[mark]
        w, h, sill = w / 12, h / 12, sill / 12
        x0 = X(a + w / 2)
        dark = mark in ("D1", "D4")
        o.append(f'<rect x="{_f(x0)}" y="{_f(Y(sill+h))}" width="{_f(w*S)}" height="{_f(h*S)}" fill="{"#4a2f22" if dark else "#9fb2bd"}" stroke="{BLACK}" stroke-width="2.2"/>')
        if not dark:
            o.append(f'<line x1="{_f(x0+w*S/2)}" y1="{_f(Y(sill+h))}" x2="{_f(x0+w*S/2)}" y2="{_f(Y(sill))}" stroke="{BLACK}" stroke-width="1.4"/>')
            for f in (0.33, 0.66):
                o.append(f'<line x1="{_f(x0)}" y1="{_f(Y(sill+h*f))}" x2="{_f(x0+w*S)}" y2="{_f(Y(sill+h*f))}" stroke="{BLACK}" stroke-width="0.9"/>')
        else:
            o.append(f'<rect x="{_f(x0+0.6*S)}" y="{_f(Y(sill+h-0.8))}" width="{_f((w-1.2)*S)}" height="{_f(2.2*S)}" fill="#9fb2bd" stroke="#222" stroke-width="0.6"/>')
        o.append(f'<rect x="{_f(x0-0.3*S)}" y="{_f(Y(8.25))}" width="{_f((w+0.6)*S)}" height="{_f(0.25*S)}" fill="#fff" stroke="#999" stroke-width="0.4"/>')
        if mark in ("W1",):
            o.append(f'<rect x="{_f(x0)}" y="{_f(Y(11))}" width="{_f(w*S)}" height="{_f(2*S)}" fill="#9fb2bd" stroke="{BLACK}" stroke-width="2"/>')
            o.append(f'<rect x="{_f(x0-0.3*S)}" y="{_f(Y(11.25))}" width="{_f((w+0.6)*S)}" height="{_f(0.25*S)}" fill="#fff" stroke="#999" stroke-width="0.4"/>')
    # north veranda columns, porch
    for x in (18, 29, 40, 51, 62):
        o.append(f'<rect x="{_f(X(x+0.67))}" y="{_f(Y(12.4))}" width="{_f(1.33*S)}" height="{_f(12.4*S)}" fill="{WHITE}" stroke="#999" stroke-width="0.6"/>')
    o.append(f'<rect x="{_f(X(62.7))}" y="{_f(Y(13.2))}" width="{_f(45.4*S)}" height="{_f(0.9*S)}" fill="#fff" stroke="#999" stroke-width="0.6"/>')
    pr = [(29.5, 11.0), (41, 11 + 11.5 * K), (52.5, 11.0)]
    o.append(f'<rect x="{_f(X(52.5))}" y="{_f(Y(11.0))}" width="{_f(23*S)}" height="{_f(1.2*S)}" fill="#fff" stroke="#999" stroke-width="0.6"/>')
    o.append('<polygon points="' + " ".join(f"{_f(X(x))},{_f(Y(h))}" for x, h in pr) + f'" fill="#45484c" stroke="#222"/>')
    for x in (31, 51):
        o.append(f'<rect x="{_f(X(x+0.75))}" y="{_f(Y(11))}" width="{_f(1.5*S)}" height="{_f(13.5*S)}" fill="{WHITE}" stroke="#888" stroke-width="0.7"/>')
        o.append(f'<rect x="{_f(X(x+1.2))}" y="{_f(Y(-2.5))}" width="{_f(2.4*S)}" height="{_f(1*S)}" fill="{STONE}" stroke="#7d725f" stroke-width="0.5"/>')
        o.append(f'<rect x="{_f(X(x+1.0))}" y="{_f(Y(11.3))}" width="{_f(2*S)}" height="{_f(0.5*S)}" fill="#fff" stroke="#888" stroke-width="0.5"/>')
    lx = X(41)
    o.append(f'<line x1="{_f(lx)}" y1="{_f(Y(11))}" x2="{_f(lx)}" y2="{_f(Y(9.2))}" stroke="#222"/>')
    o.append(f'<rect x="{_f(lx-4)}" y="{_f(Y(9.2))}" width="8" height="12" fill="#e9c46a" stroke="#222"/>')
    # ground and levels
    o.append(f'<line x1="0" y1="{_f(Y(-2.5))}" x2="{W:.0f}" y2="{_f(Y(-2.5))}" stroke="#4d5b3a" stroke-width="2"/>')
    for h, t in ((RIDGE, "ridge +24 ft 3 in"), (PLATE, "wall plate +15 ft 0 in"), (8.0, "lintel band +8 ft 0 in"),
                 (1.5, "stone base to sill +1 ft 6 in"), (0, "FFL ±0"), (-2.5, "ground -2 ft 6 in")):
        o.append(f'<line x1="{_f(W-ox-6)}" y1="{_f(Y(h))}" x2="{_f(W-4)}" y2="{_f(Y(h))}" stroke="#1d4e89" stroke-width="0.6"/>')
        o.append(tag(W - 6, Y(h) - 2, t, 5.6, "normal", "#1d4e89", "end"))
    o.append(tag(W / 2, H - 14, "NORTH (APPROACH) ELEVATION. Cream lime render, stone base to sill level, charcoal 25° hipped roof with 3 ft 0 in overhang, black slim windows with white drip moulds, white columns.", 7, fill="#333"))
    o.append("</svg>")
    return "\n".join(o)


def sun_section():
    S = 6.2
    ox, base = 70, 210
    W, H = ox + 64 * S + 40, base + 6 * S + 40
    X = lambda y: ox + (y + 8) * S          # section north (left) to south (right)
    Y = lambda h: base - h * S
    o = [f'<svg viewBox="0 0 {W:.0f} {H:.0f}" xmlns="http://www.w3.org/2000/svg" class="dwg">',
         f'<rect width="{W:.0f}" height="{H:.0f}" fill="#f6f2ea"/>']
    # ground: north -2.5, south -5.0 after terracing
    o.append(f'<polygon points="{_f(X(-10))},{_f(Y(-2.5))} {_f(X(0))},{_f(Y(-2.5))} {_f(X(49.5))},{_f(Y(-5))} {_f(X(58))},{_f(Y(-5))} {_f(X(58))},{_f(Y(-8))} {_f(X(-10))},{_f(Y(-8))}" fill="#cdbf9f"/>')
    o.append(f'<rect x="{_f(X(-0.4))}" y="{_f(Y(0))}" width="{_f(49.8*S)}" height="{_f(0.5*S)}" fill="#999"/>')
    # plinth & veranda steps
    o.append(f'<rect x="{_f(X(-0.4))}" y="{_f(Y(0))}" width="{_f(0.75*S)}" height="{_f(2.5*S)}" fill="#7d725f"/>')
    for i in range(8):
        o.append(f'<rect x="{_f(X(49.5+i))}" y="{_f(Y(-i*7.5/12))}" width="{_f(1*S)}" height="{_f(7.5/12*S)}" fill="#bbb" stroke="#888" stroke-width="0.3"/>')
    # walls
    for y in (0, 40):
        o.append(f'<rect x="{_f(X(y-0.375))}" y="{_f(Y(PLATE))}" width="{_f(0.75*S)}" height="{_f(PLATE*S)}" fill="#4a4a4a"/>')
    o.append(f'<rect x="{_f(X(13-0.19))}" y="{_f(Y(12.25))}" width="{_f(0.38*S)}" height="{_f(1*S)}" fill="#4a4a4a"/>')
    # glazing in south wall (French door) & north wall
    o.append(f'<rect x="{_f(X(39.8))}" y="{_f(Y(8))}" width="{_f(0.4*S)}" height="{_f(8*S)}" fill="#9fb2bd"/>')
    # ceilings
    o.append(f'<polyline points="{_f(X(0))},{_f(Y(12.25))} {_f(X(13))},{_f(Y(12.25))} {_f(X(26.5))},{_f(Y(16))} {_f(X(40))},{_f(Y(12.25))}" fill="none" stroke="#8a6d3b" stroke-width="2"/>')
    # roof
    rp = [(-3, EAVE_NEW), (20, RIDGE), (41.5, PLATE - 1.5 * K)]
    o.append('<polyline points="' + " ".join(f"{_f(X(y))},{_f(Y(h))}" for y, h in rp) + f'" fill="none" stroke="{ROOF}" stroke-width="4"/>')
    o.append(f'<line x1="{_f(X(40))}" y1="{_f(Y(VER_LEDGER))}" x2="{_f(X(40+VER_PROJ))}" y2="{_f(Y(VER_EAVE))}" stroke="{ROOF}" stroke-width="3.5"/>')
    o.append(f'<rect x="{_f(X(48.33))}" y="{_f(Y(VER_EAVE-0.25))}" width="{_f(1.33*S)}" height="{_f((VER_EAVE-0.25)*S)}" fill="#fff" stroke="#888"/>')
    o.append(f'<line x1="{_f(X(-8))}" y1="{_f(Y(13.2))}" x2="{_f(X(-0.4))}" y2="{_f(Y(14.4))}" stroke="{ROOF}" stroke-width="3"/>')
    o.append(f'<rect x="{_f(X(-8.6))}" y="{_f(Y(12.6))}" width="{_f(1.33*S)}" height="{_f(12.6*S)}" fill="#fff" stroke="#888"/>')
    # sun rays from veranda eave
    ex, eh = 40 + VER_PROJ, VER_EAVE
    leg = []
    for key, col in (("winter", "#e07a2f"), ("equinox", "#d4a017"), ("summer", "#b33")):
        ang = SUN[key]
        t = math.tan(math.radians(ang))
        hit = eh - (ex - 40) * t
        if hit > 0:
            yend = 40 - hit / t
            o.append(f'<line x1="{_f(X(ex+12/t if t<5 else ex+1))}" y1="{_f(Y(eh+12))}" x2="{_f(X(yend))}" y2="{_f(Y(0))}" stroke="{col}" stroke-width="1.4" stroke-dasharray="5 2"/>')
            leg.append((col, f"Winter noon sun {ang:.0f}°: lights the lower {hit:.1f} ft of the south glass and {40-yend:.1f} ft of hall floor"))
        else:
            dx = 13 / t
            o.append(f'<line x1="{_f(X(ex+dx))}" y1="{_f(Y(eh+13))}" x2="{_f(X(ex))}" y2="{_f(Y(eh))}" stroke="{col}" stroke-width="1.4" stroke-dasharray="5 2"/>')
            o.append(f'<line x1="{_f(X(ex))}" y1="{_f(Y(eh))}" x2="{_f(X(ex-eh/t))}" y2="{_f(Y(0))}" stroke="{col}" stroke-width="0.8" stroke-dasharray="1 2"/>')
            leg.append((col, f"{key.capitalize()} noon sun {ang:.0f}°: south glass fully shaded"))
    for txt, y, h in (("roof 25°, ridge +24 ft 3 in", 20, RIDGE + 1.2), ("vaulted hall ceiling to +16 ft 0 in", 26.5, 16.8),
                      ("ceiling +12 ft 3 in", 6.5, 11.2), ("veranda roof 1 in 6, eave +12 ft 5 in", 46, 17.2),
                      ("FFL ±0", 6, 0.8), ("plinth 2 ft 6 in", -5, -1.4), ("8 risers of 7½ in", 54, -4)):
        o.append(tag(X(y), Y(h), txt, 6.2, "normal", "#333"))
    for i, (col, t) in enumerate(leg):
        o.append(f'<line x1="12" y1="{18+i*12}" x2="34" y2="{18+i*12}" stroke="{col}" stroke-width="1.6" stroke-dasharray="5 2"/>')
        o.append(tag(40, 21 + i * 12, t, 6.6, "bold", col, "start"))
    o.append(tag(X(-3.5), Y(-6.6), "NORTH", 7, "bold"))
    o.append(tag(X(53), Y(-6.6), "SOUTH", 7, "bold"))
    o.append(tag(W / 2, H - 10, "SECTION THROUGH SITTING HALL, looking east, with noon sun angles at latitude 25.5° N (Tura)", 7, fill="#333"))
    o.append("</svg>")
    return "\n".join(o)


def firehouse():
    S = 9
    W, H = 640, 318
    o = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" class="dwg">',
         f'<rect width="{W}" height="{H}" fill="#f6f2ea"/>']
    # plan
    ox, oy = 30, 40
    P = lambda x, y: (ox + (x + 2) * S, oy + (y + 2) * S)
    a, b = P(-2, -2)
    o.append(f'<rect x="{_f(a)}" y="{_f(b)}" width="{_f(24*S)}" height="{_f(24*S)}" fill="#e3d7bd" stroke="#9c8f74"/>')
    a, b = P(-0.375, 19.625)
    o.append(f'<rect x="{_f(a)}" y="{_f(b)}" width="{_f(20.75*S)}" height="{_f(0.75*S)}" fill="#5a5048"/>')
    for x, y in ((0, 0), (20, 0), (0, 20), (20, 20), (0, 10), (20, 10)):
        a, b = P(x, y)
        o.append(f'<rect x="{_f(a-0.5*S)}" y="{_f(b-0.5*S)}" width="{_f(S)}" height="{_f(S)}" fill="#fff" stroke="#333"/>')
    cx, cy = P(10, 10)
    o.append(f'<path d="M {_f(cx + 7.5*S*math.cos(math.radians(150)))} {_f(cy - 7.5*S*math.sin(math.radians(150)))} A {_f(7.5*S)} {_f(7.5*S)} 0 1 0 {_f(cx + 7.5*S*math.cos(math.radians(30)))} {_f(cy - 7.5*S*math.sin(math.radians(30)))}" fill="none" stroke="#7a4e2d" stroke-width="{_f(1.5*S)}"/>')
    o.append(f'<circle cx="{_f(cx)}" cy="{_f(cy)}" r="{_f(2.75*S)}" fill="#a49884" stroke="#555"/>')
    o.append(f'<circle cx="{_f(cx)}" cy="{_f(cy)}" r="{_f(2*S)}" fill="#e07a2f"/>')
    a, b = P(-0.4, 17.6)
    o.append(f'<rect x="{_f(a)}" y="{_f(b)}" width="{_f(5*S)}" height="{_f(2*S)}" fill="#ddd" stroke="#555"/>')
    o.append(tag(*P(2.1, 18.9), "counter + sink", 5.2))
    o.append(tag(cx, cy + 1, "fire pit", 6, "bold", "#fff"))
    o.append(tag(cx, cy + 9, "4 ft 0 in dia", 5.2, "normal", "#fff"))
    o.append(tag(*P(10, 22.6), "bench: fixed hardwood on stone plinth, 240° arc, 34 ft long, seats 10", 5.6, "bold", "#5b3a1f"))
    o.append(tag(*P(10, 21.4), "solid back wall to the south-west monsoon wind", 6, "bold"))
    o.append(tag(*P(10, -2.8), "open to house (north), east and west", 6, "bold"))
    o.append(tag(*P(10, 24.4), "PLAN: 20 ft 0 in x 20 ft 0 in on column centres, 24 ft 0 in platform", 6.4, "bold", "#333"))
    # elevation
    ex, base = 300, 270
    X = lambda x: ex + (x + 3) * 11
    Y = lambda h: base - h * 11
    o.append(f'<line x1="{ex-10}" y1="{_f(Y(-1.5))}" x2="{W-5}" y2="{_f(Y(-1.5))}" stroke="#4d5b3a" stroke-width="2"/>')
    _stone(o, X(-2), Y(0), 24 * 11, 1.5 * 11, "st2")
    _stone(o, X(-0.4), Y(3), 20.8 * 11, 3 * 11, "st3")
    o.append(f'<rect x="{_f(X(-0.4))}" y="{_f(Y(9))}" width="{_f(20.8*11)}" height="{_f(6*11)}" fill="{CREAM}" opacity="0.65"/>')
    for x in (0, 10, 20):
        o.append(f'<rect x="{_f(X(x)-5.5)}" y="{_f(Y(9))}" width="11" height="{_f(9*11)}" fill="#fff" stroke="#888"/>')
    o.append(f'<rect x="{_f(X(-0.6))}" y="{_f(Y(9.9))}" width="{_f(21.2*11)}" height="11" fill="#fff" stroke="#888"/>')
    apex = 9.9 + 13 * K
    o.append(f'<polygon points="{_f(X(-3))},{_f(Y(9.9))} {_f(X(8.5))},{_f(Y(9.9+11.5*K))} {_f(X(11.5))},{_f(Y(9.9+11.5*K))} {_f(X(23))},{_f(Y(9.9))}" fill="{ROOF}"/>')
    o.append(f'<rect x="{_f(X(8.5))}" y="{_f(Y(9.9+11.5*K+2.5))}" width="33" height="{_f(2.5*11)}" fill="#55585c" stroke="#222"/>')
    for i in range(4):
        o.append(f'<line x1="{_f(X(8.6))}" y1="{_f(Y(9.9+11.5*K+0.5+i*0.5))}" x2="{_f(X(11.4))}" y2="{_f(Y(9.9+11.5*K+0.5+i*0.5))}" stroke="#999"/>')
    o.append(f'<polygon points="{_f(X(7.8))},{_f(Y(9.9+11.5*K+2.5))} {_f(X(10))},{_f(Y(9.9+11.5*K+3.6))} {_f(X(12.2))},{_f(Y(9.9+11.5*K+2.5))}" fill="{ROOF}"/>')
    o.append(f'<circle cx="{_f(X(10))}" cy="{_f(Y(1.2))}" r="9" fill="#e07a2f" opacity="0.85"/>')
    o.append(tag(X(10), Y(9.9 + 11.5 * K + 4.6), "louvred smoke lantern 3 ft 0 in square, top +17 ft 6 in", 6, "bold"))
    o.append(tag(X(10), Y(-2.4) + 4, "ELEVATION FROM THE HOUSE: platform +1 ft 6 in, eave +9 ft 6 in, roof 25°", 6.4, "bold", "#333"))
    o.append("</svg>")
    return "\n".join(o)


def gate():
    S = 11
    W, H = 640, 200
    base = 170
    Y = lambda h: base - h * S
    o = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" class="dwg">',
         f'<rect width="{W}" height="{H}" fill="#f6f2ea"/>']
    x0 = 70
    X = lambda x: x0 + x * S
    # compound wall either side
    for xa, xb in ((-6, -2.5), (22, 30)):
        _stone(o, X(xa), Y(2.5), (xb - xa) * S, 2.5 * S, "sw" + str(xa))
        o.append(f'<rect x="{_f(X(xa))}" y="{_f(Y(5))}" width="{_f((xb-xa)*S)}" height="{_f(2.5*S)}" fill="{CREAM}" stroke="#bbb" stroke-width="0.5"/>')
        o.append(f'<polygon points="{_f(X(xa))},{_f(Y(5))} {_f(X(xb))},{_f(Y(5))} {_f(X(xb))},{_f(Y(5.25))} {_f(X(xa))},{_f(Y(5.15))}" fill="#999"/>')
        o.append(f'<line x1="{_f(X(xa))}" y1="{_f(Y(7.25))}" x2="{_f(X(xb))}" y2="{_f(Y(7.25))}" stroke="{BLACK}" stroke-width="1.6"/>')
        x = xa + 0.4
        while x < xb:
            o.append(f'<line x1="{_f(X(x))}" y1="{_f(Y(5.25))}" x2="{_f(X(x))}" y2="{_f(Y(7.5))}" stroke="{BLACK}" stroke-width="1"/>')
            x += 5 / 12
    # piers
    for xa in (-2.5, 14, 20):
        w = 2.5 if xa != 20 else 2.0
        _stone(o, X(xa), Y(9.5), w * S, 9.5 * S, f"pp{int(xa*10)}")
        o.append(f'<rect x="{_f(X(xa)-3)}" y="{_f(Y(9.8))}" width="{_f(w*S+6)}" height="{_f(0.3*S)}" fill="#ccc" stroke="#888"/>')
        cx = X(xa + w / 2)
        o.append(f'<rect x="{_f(cx-6)}" y="{_f(Y(11.6))}" width="12" height="{_f(1.6*S)}" fill="#e9c46a" stroke="{BLACK}" stroke-width="1.5"/>')
        o.append(f'<polygon points="{_f(cx-8)},{_f(Y(11.6))} {_f(cx)},{_f(Y(12.3))} {_f(cx+8)},{_f(Y(11.6))}" fill="{BLACK}"/>')
    # main leaves 0..14, arched top 7.5 -> 9.0
    def top(x):
        return 7.5 + 1.5 * math.sin(math.pi * x / 14)
    o.append('<polyline points="' + " ".join(f"{_f(X(x/4))},{_f(Y(top(x/4)))}" for x in range(57)) + f'" fill="none" stroke="{BLACK}" stroke-width="2.4"/>')
    for h in (0.33, 2.0, 6.0):
        o.append(f'<line x1="{_f(X(0))}" y1="{_f(Y(h))}" x2="{_f(X(14))}" y2="{_f(Y(h))}" stroke="{BLACK}" stroke-width="2"/>')
    x = 5 / 24
    while x < 14:
        o.append(f'<line x1="{_f(X(x))}" y1="{_f(Y(0.33))}" x2="{_f(X(x))}" y2="{_f(Y(top(x)+0.35))}" stroke="{BLACK}" stroke-width="1.1"/>')
        o.append(f'<polygon points="{_f(X(x)-2)},{_f(Y(top(x)+0.35))} {_f(X(x))},{_f(Y(top(x)+0.65))} {_f(X(x)+2)},{_f(Y(top(x)+0.35))}" fill="{BLACK}"/>')
        o.append(f'<line x1="{_f(X(x+5/24))}" y1="{_f(Y(0.33))}" x2="{_f(X(x+5/24))}" y2="{_f(Y(2.0))}" stroke="{BLACK}" stroke-width="0.8"/>')
        x += 5 / 12
    for i in range(14):
        cx = X(0.5 + i)
        o.append(f'<path d="M {_f(cx-4)} {_f(Y(6.8))} q 4 -7 8 0 M {_f(cx-4)} {_f(Y(6.8))} q 4 7 8 0" fill="none" stroke="{BLACK}" stroke-width="1"/>')
    o.append(f'<line x1="{_f(X(7))}" y1="{_f(Y(0))}" x2="{_f(X(7))}" y2="{_f(Y(9))}" stroke="{BLACK}" stroke-width="2.4"/>')
    # wicket
    o.append(f'<rect x="{_f(X(16.5))}" y="{_f(Y(7))}" width="{_f(3.5*S)}" height="{_f(7*S)}" fill="none" stroke="{BLACK}" stroke-width="2"/>')
    xw = 16.5 + 5 / 24
    while xw < 20:
        o.append(f'<line x1="{_f(X(xw))}" y1="{_f(Y(0.33))}" x2="{_f(X(xw))}" y2="{_f(Y(7))}" stroke="{BLACK}" stroke-width="1"/>')
        xw += 5 / 12
    o.append(tag(X(18.25), Y(7.4), "wicket 3 ft 6 in", 6))
    o.append(f'<line x1="0" y1="{_f(Y(0))}" x2="{W}" y2="{_f(Y(0))}" stroke="#4d5b3a" stroke-width="2"/>')
    o.append(tag(6, Y(-1.1), "GATE 14 ft 0 in clear, two leaves of 7 ft 0 in; 1 in square bars at 4 in clear (5 in centres), spear finials; dog bars to 2 ft 0 in", 6.3, "bold", anchor="start"))
    o.append(tag(6, Y(-1.1) + 9, "leaf height 7 ft 6 in at hinge rising to 9 ft 0 in at centre; C-scroll band between 6 ft 0 in and top rail; piers 2 ft 6 in square x 9 ft 6 in, stone clad, lanterns", 6, "normal", anchor="start"))
    o.append(tag(X(26), Y(10.2), "compound wall 7 ft 3 in total", 6, "bold"))
    o.append(tag(X(25.2), Y(10.2) + 8, "railing 2 ft 0 in / coping 3 in", 5.6))
    o.append(tag(X(25.2), Y(10.2) + 15, "render 2 ft 6 in / stone 2 ft 6 in", 5.6))
    o.append("</svg>")
    return "\n".join(o)

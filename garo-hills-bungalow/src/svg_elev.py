"""North elevation, sun section, firehouse and gate for the budget house (decimal feet)."""
import math
from svg_plan import tag, _f
from openings import MAIN, SCHEDULE
from data import SUN

K = math.tan(math.radians(25))
PLATE = 13.0                       # wall plate (roof band top) above floor, ft
EAVE = PLATE - 3 * K               # main roof eave with 3.00 ft overhang
RIDGE = EAVE + 16.25 * K           # hip roof over 32.50 ft depth
VER_LEDGER, VER_PROJ = 12.9, 9.0   # veranda roof at wall, projection from wall line
VER_EAVE = VER_LEDGER - VER_PROJ / 6
CREAM, STONE, ROOF, BLACK, WHITE = "#efe4cc", "#b9ab92", "#3b3d40", "#1c1c1c", "#ffffff"


def _stone(o, x, y, w, h, pid):
    o.append(f'<defs><pattern id="{pid}" width="14" height="8" patternUnits="userSpaceOnUse">'
             f'<rect width="14" height="8" fill="{STONE}"/><path d="M0 4 H14 M7 0 V4 M0 4 V8 M14 4 V8" stroke="#8f8370" stroke-width="0.6"/></pattern></defs>')
    o.append(f'<rect x="{_f(x)}" y="{_f(y)}" width="{_f(w)}" height="{_f(h)}" fill="url(#{pid})" stroke="#7d725f" stroke-width="0.5"/>')


def _level(o, W, ox, Y, h, text):
    o.append(f'<line x1="{_f(W-ox-4)}" y1="{_f(Y(h))}" x2="{_f(W-4)}" y2="{_f(Y(h))}" stroke="#1d4e89" stroke-width="0.6"/>')
    o.append(tag(W - 6, Y(h) - 2, text, 6, "normal", "#1d4e89", "end"))


def north_elevation():
    S = 12.0
    ox, base = 30, 290
    W, H = ox * 2 + 52 * S + 130, base + 2.5 * S + 46
    X = lambda x: ox + (49 - x) * S          # seen from the north, east is on the left
    Y = lambda h: base - h * S
    o = [f'<svg viewBox="0 0 {W:.0f} {H:.0f}" xmlns="http://www.w3.org/2000/svg" class="dwg">',
         f'<rect width="{W:.0f}" height="{H:.0f}" fill="#f6f2ea"/>']
    pts = [(-3, EAVE), (13.25, RIDGE), (32.75, RIDGE), (49, EAVE)]
    o.append('<polygon points="' + " ".join(f"{_f(X(x))},{_f(Y(h))}" for x, h in pts) + f'" fill="{ROOF}"/>')
    o.append(f'<rect x="{_f(X(46.375))}" y="{_f(Y(EAVE))}" width="{_f(46.75*S)}" height="{_f((EAVE+2.5)*S)}" fill="{CREAM}"/>')
    _stone(o, X(46.375), Y(1.5), 46.75 * S, 4 * S, "st1")
    for mark, ori, c, a, side in MAIN:
        if ori != "h" or c != 0:
            continue
        _, _, w, h, sill, lintel, *_ = SCHEDULE[mark]
        x0 = X(a + w / 2)
        dark = mark == "D1"
        o.append(f'<rect x="{_f(x0)}" y="{_f(Y(sill+h))}" width="{_f(w*S)}" height="{_f(h*S)}" fill="{"#4a2f22" if dark else "#9fb2bd"}" stroke="{BLACK}" stroke-width="2"/>')
        if not dark:
            o.append(f'<line x1="{_f(x0+w*S/2)}" y1="{_f(Y(sill+h))}" x2="{_f(x0+w*S/2)}" y2="{_f(Y(sill))}" stroke="{BLACK}" stroke-width="1.2"/>')
        o.append(f'<rect x="{_f(x0-0.25*S)}" y="{_f(Y(lintel+0.25))}" width="{_f((w+0.5)*S)}" height="{_f(0.25*S)}" fill="#fff" stroke="#999" stroke-width="0.4"/>')
    for x in (17, 27):
        o.append(f'<rect x="{_f(X(x+0.4))}" y="{_f(Y(10.0))}" width="{_f(0.8*S)}" height="{_f(12.5*S)}" fill="{WHITE}" stroke="#888" stroke-width="0.7"/>')
    pr = [(16.5, 10.0), (22, 10.0 + 5.5 * K), (27.5, 10.0)]
    o.append('<polygon points="' + " ".join(f"{_f(X(x))},{_f(Y(h))}" for x, h in pr) + f'" fill="#45484c" stroke="#222"/>')
    for i in range(4):
        o.append(f'<rect x="{_f(X(25.5))}" y="{_f(Y(-0.625*i))}" width="{_f(7*S)}" height="{_f(0.625*S)}" fill="{STONE}" stroke="#7d725f" stroke-width="0.4"/>')
    o.append(f'<line x1="0" y1="{_f(Y(-2.5))}" x2="{W:.0f}" y2="{_f(Y(-2.5))}" stroke="#4d5b3a" stroke-width="2"/>')
    for h, t in ((RIDGE, f"ridge +{RIDGE:.2f} ft"), (PLATE, f"wall plate +{PLATE:.2f} ft"), (8.0, "lintel band +8.00 ft"),
                 (1.5, "stone base to sill +1.50 ft"), (0, "floor ±0.00"), (-2.5, "ground −2.50 ft")):
        _level(o, W, 120, Y, h, t)
    o.append(tag(W / 2 - 50, H - 14, "NORTH (APPROACH) ELEVATION: cream render, stone base to sill, charcoal 25° hipped roof, 3.00 ft overhang, black steel windows, white drip moulds.", 7, fill="#333"))
    o.append("</svg>")
    return "\n".join(o)


def sun_section():
    S = 9.0
    ox, base = 70, 230
    W, H = ox + 45 * S + 40, base + 6 * S + 40
    X = lambda y: ox + (y + 5) * S
    Y = lambda h: base - h * S
    o = [f'<svg viewBox="0 0 {W:.0f} {H:.0f}" xmlns="http://www.w3.org/2000/svg" class="dwg">',
         f'<rect width="{W:.0f}" height="{H:.0f}" fill="#f6f2ea"/>']
    o.append(f'<polygon points="{_f(X(-6))},{_f(Y(-2.5))} {_f(X(0))},{_f(Y(-2.5))} {_f(X(36.4))},{_f(Y(-4.0))} {_f(X(41))},{_f(Y(-4.0))} {_f(X(41))},{_f(Y(-7))} {_f(X(-6))},{_f(Y(-7))}" fill="#cdbf9f"/>')
    o.append(f'<rect x="{_f(X(-0.4))}" y="{_f(Y(0))}" width="{_f(36.8*S)}" height="{_f(0.4*S)}" fill="#999"/>')
    for y in (0, 28):
        o.append(f'<rect x="{_f(X(y-0.375))}" y="{_f(Y(PLATE))}" width="{_f(0.75*S)}" height="{_f(PLATE*S)}" fill="#4a4a4a"/>')
    o.append(f'<rect x="{_f(X(27.8))}" y="{_f(Y(7.5))}" width="{_f(0.4*S)}" height="{_f(7.5*S)}" fill="#9fb2bd"/>')
    o.append(f'<line x1="{_f(X(0))}" y1="{_f(Y(12))}" x2="{_f(X(28))}" y2="{_f(Y(12))}" stroke="#8a6d3b" stroke-width="2"/>')
    rp = [(-3, EAVE), (13.0, RIDGE), (29.5, PLATE - 1.5 * K)]
    o.append('<polyline points="' + " ".join(f"{_f(X(y))},{_f(Y(h))}" for y, h in rp) + f'" fill="none" stroke="{ROOF}" stroke-width="4"/>')
    o.append(f'<line x1="{_f(X(28))}" y1="{_f(Y(VER_LEDGER))}" x2="{_f(X(28+VER_PROJ))}" y2="{_f(Y(VER_EAVE))}" stroke="{ROOF}" stroke-width="3.5"/>')
    o.append(f'<rect x="{_f(X(35.9))}" y="{_f(Y(VER_EAVE-0.2))}" width="{_f(0.9*S)}" height="{_f((VER_EAVE-0.2)*S)}" fill="#fff" stroke="#888"/>')
    for i in range(5):
        o.append(f'<rect x="{_f(X(36.8+i*0.9))}" y="{_f(Y(-i*0.5))}" width="{_f(0.9*S)}" height="{_f(0.5*S)}" fill="#bbb" stroke="#888" stroke-width="0.3"/>')
    ex, eh = 28 + VER_PROJ, VER_EAVE
    leg = []
    for key, col in (("winter", "#e07a2f"), ("equinox", "#d4a017"), ("summer", "#b33")):
        ang = SUN[key]
        t = math.tan(math.radians(ang))
        hit = eh - (ex - 28) * t
        if hit > 0:
            yend = 28 - hit / t
            o.append(f'<line x1="{_f(X(ex+10/t))}" y1="{_f(Y(eh+10))}" x2="{_f(X(yend))}" y2="{_f(Y(0))}" stroke="{col}" stroke-width="1.4" stroke-dasharray="5 2"/>')
            leg.append((col, f"Winter noon sun {ang:.2f}°: {eh:.2f} − {VER_PROJ:.2f} × tan {ang:.2f}° = {hit:.2f} ft of glass in sun; sun patch {28-yend:.2f} ft into the room"))
        else:
            dx = 10 / t
            o.append(f'<line x1="{_f(X(ex+dx))}" y1="{_f(Y(eh+10))}" x2="{_f(X(ex))}" y2="{_f(Y(eh))}" stroke="{col}" stroke-width="1.4" stroke-dasharray="5 2"/>')
            leg.append((col, f"{key.capitalize()} noon sun {ang:.2f}°: {eh:.2f} − {VER_PROJ:.2f} × tan {ang:.2f}° = {hit:.2f} ft (below floor): glass fully shaded"))
    for i, (col, t) in enumerate(leg):
        o.append(f'<line x1="12" y1="{16+i*12}" x2="34" y2="{16+i*12}" stroke="{col}" stroke-width="1.6" stroke-dasharray="5 2"/>')
        o.append(tag(40, 19 + i * 12, t, 6.4, "bold", col, "start"))
    for txt, y, h in ((f"roof 25°, ridge +{RIDGE:.2f} ft", 13, RIDGE + 1.0), ("ceiling +12.00 ft", 14, 11.0),
                      (f"veranda roof 1:6, eave +{VER_EAVE:.2f} ft", 33, VER_LEDGER + 1.6), ("floor ±0.00", 6, 0.8),
                      ("plinth 2.50 ft", -2.6, -1.4)):
        o.append(tag(X(y), Y(h), txt, 6.4, "normal", "#333"))
    o.append(tag(X(-2.5), Y(-6), "NORTH", 7, "bold"))
    o.append(tag(X(38), Y(-6), "SOUTH", 7, "bold"))
    o.append(tag(W / 2, H - 10, "SECTION THROUGH SITTING AND DINING, looking east, with noon sun angles at latitude 25.50° N", 7, fill="#333"))
    o.append("</svg>")
    return "\n".join(o)


def firehouse():
    S = 14
    W, H = 600, 260
    o = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" class="dwg">',
         f'<rect width="{W}" height="{H}" fill="#f6f2ea"/>']
    ox, oy = 40, 28
    P = lambda x, y: (ox + (x + 1) * S, oy + (y + 1) * S)
    a, b = P(-1, -1)
    o.append(f'<rect x="{_f(a)}" y="{_f(b)}" width="{_f(14*S)}" height="{_f(14*S)}" fill="#e3d7bd" stroke="#9c8f74"/>')
    for x, y in ((0, 0), (12, 0), (0, 12), (12, 12)):
        a, b = P(x, y)
        o.append(f'<rect x="{_f(a-0.25*S)}" y="{_f(b-0.25*S)}" width="{_f(0.5*S)}" height="{_f(0.5*S)}" fill="#7a5a3a"/>')
    cx, cy = P(6, 6)
    o.append(f'<path d="M {_f(cx + 4.6*S*math.cos(math.radians(150)))} {_f(cy - 4.6*S*math.sin(math.radians(150)))} A {_f(4.6*S)} {_f(4.6*S)} 0 1 0 {_f(cx + 4.6*S*math.cos(math.radians(30)))} {_f(cy - 4.6*S*math.sin(math.radians(30)))}" fill="none" stroke="#8f8370" stroke-width="{_f(1.25*S)}"/>')
    o.append(f'<circle cx="{_f(cx)}" cy="{_f(cy)}" r="{_f(2.5*S)}" fill="#a49884" stroke="#555"/>')
    o.append(f'<circle cx="{_f(cx)}" cy="{_f(cy)}" r="{_f(2.0*S)}" fill="#e07a2f"/>')
    o.append(tag(cx, cy + 3, "4.00 ft pit", 6, "bold", "#fff"))
    o.append(tag(*P(6, 13.6), "PLAN: 12.00 x 12.00 ft on post centres; stone bench on a 240° arc", 6.4, "bold", "#333"))
    ex, base = 300, 225
    X = lambda x: ex + (x + 2) * 14
    Y = lambda h: base - h * 14
    o.append(f'<line x1="{ex-10}" y1="{_f(Y(-1))}" x2="{W-5}" y2="{_f(Y(-1))}" stroke="#4d5b3a" stroke-width="2"/>')
    _stone(o, X(-1), Y(0), 14 * 14, 1.0 * 14, "st2")
    for x in (0, 12):
        o.append(f'<rect x="{_f(X(x)-3.5)}" y="{_f(Y(8.5))}" width="7" height="{_f(8.5*14)}" fill="#7a5a3a"/>')
    o.append(f'<rect x="{_f(X(-0.3))}" y="{_f(Y(9.1))}" width="{_f(12.6*14)}" height="{_f(0.6*14)}" fill="#7a5a3a"/>')
    o.append(f'<polygon points="{_f(X(-2))},{_f(Y(9.1))} {_f(X(5.5))},{_f(Y(9.1+7.5*K))} {_f(X(6.5))},{_f(Y(9.1+7.5*K))} {_f(X(14))},{_f(Y(9.1))}" fill="{ROOF}"/>')
    o.append(f'<rect x="{_f(X(5.25))}" y="{_f(Y(9.1+7.5*K+1.5))}" width="{_f(1.5*14)}" height="{_f(1.5*14)}" fill="#55585c" stroke="#222"/>')
    o.append(f'<circle cx="{_f(X(6))}" cy="{_f(Y(0.9))}" r="9" fill="#e07a2f" opacity="0.85"/>')
    o.append(tag(X(6), Y(9.1 + 7.5 * K + 2.3), f"smoke vent 1.50 ft square, top +{9.1 + 7.5 * K + 1.5:.2f} ft", 6.2, "bold"))
    o.append(tag(X(6), Y(-1) + 13, "ELEVATION: platform +1.00 ft, eave +9.10 ft, roof 25°, 2.00 ft overhang", 6.4, "bold", "#333"))
    o.append("</svg>")
    return "\n".join(o)


def gate():
    S = 14
    W, H = 600, 200
    base = 165
    Y = lambda h: base - h * S
    x0 = 80
    X = lambda x: x0 + x * S
    o = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" class="dwg">',
         f'<rect width="{W}" height="{H}" fill="#f6f2ea"/>']
    for xa, xb in ((-5, -2), (19.5, 26)):
        _stone(o, X(xa), Y(4.0), (xb - xa) * S, 4.0 * S, "sw" + str(int(xa * 10)))
        o.append(f'<rect x="{_f(X(xa))}" y="{_f(Y(4.25))}" width="{_f((xb-xa)*S)}" height="{_f(0.25*S)}" fill="#bbb" stroke="#888"/>')
    for xa in (-2, 12, 17.5):
        _stone(o, X(xa), Y(6.0), 2.0 * S, 6.0 * S, f"pp{int(xa*10)}")
    for i in range(30):
        x = i * 5 / 12
        if x > 12:
            break
        o.append(f'<line x1="{_f(X(x))}" y1="{_f(Y(0.3))}" x2="{_f(X(x))}" y2="{_f(Y(5.5))}" stroke="#1c1c1c" stroke-width="1.1"/>')
    for h in (0.3, 2.75, 5.5):
        o.append(f'<line x1="{_f(X(0))}" y1="{_f(Y(h))}" x2="{_f(X(12))}" y2="{_f(Y(h))}" stroke="#1c1c1c" stroke-width="2"/>')
    o.append(f'<line x1="{_f(X(6))}" y1="{_f(Y(0))}" x2="{_f(X(6))}" y2="{_f(Y(5.5))}" stroke="#1c1c1c" stroke-width="2.4"/>')
    o.append(f'<rect x="{_f(X(14))}" y="{_f(Y(5.5))}" width="{_f(3.5*S)}" height="{_f(5.5*S)}" fill="none" stroke="#1c1c1c" stroke-width="2"/>')
    for i in range(9):
        x = 14 + i * 5 / 12
        o.append(f'<line x1="{_f(X(x))}" y1="{_f(Y(0.3))}" x2="{_f(X(x))}" y2="{_f(Y(5.5))}" stroke="#1c1c1c" stroke-width="1"/>')
    o.append(f'<line x1="0" y1="{_f(Y(0))}" x2="{W}" y2="{_f(Y(0))}" stroke="#4d5b3a" stroke-width="2"/>')
    o.append(tag(8, Y(-1.1), "GATE: 12.00 ft clear in two leaves of 6.00 ft, 5.50 ft high; 0.08 ft square bars at 0.42 ft centres; wicket 3.50 ft clear.", 6.4, "bold", anchor="start"))
    o.append(tag(8, Y(-1.1) + 10, "Stone piers 2.00 ft square x 6.00 ft high. Stone wall 4.00 ft high for 30.00 ft each side, then chain-link fence 5.00 ft high.", 6.2, anchor="start"))
    o.append("</svg>")
    return "\n".join(o)

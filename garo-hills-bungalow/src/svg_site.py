"""Site plan (one hectare) and roof drainage plan for the budget house. Feet throughout."""
import math, random
from svg_plan import tag, _f, INK, FILL
from data import rain

PLOT = 328.08
HX, HY = 141, 165          # house CL origin on site (house is 46 x 28)
RING = (164, 135, 20)      # gravel turning circle centre x, y, radius
FX, FY = 158, 236          # firehouse post-centre origin (12 x 12)
CP = (113, 122, 18, 20)    # carport x, y, w, d


def site_plan():
    S = 2.15
    ox, oy = 30, 30
    W = ox * 2 + PLOT * S + 150
    H = oy * 2 + PLOT * S + 10
    P = lambda x, y: (ox + x * S, oy + y * S)
    o = [f'<svg viewBox="0 0 {W:.0f} {H:.0f}" xmlns="http://www.w3.org/2000/svg" class="dwg">',
         f'<rect width="{W:.0f}" height="{H:.0f}" fill="{FILL}"/>']

    def rect(x0, y0, w, h, col, stroke="none", sw=0.6, dash=None):
        a, b = P(x0, y0)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o.append(f'<rect x="{_f(a)}" y="{_f(b)}" width="{_f(w*S)}" height="{_f(h*S)}" fill="{col}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def lab(x, y, t, fs=7, w="bold", c="#3d4a2a", anchor="middle"):
        o.append(tag(*P(x, y), t, fs, w, c, anchor))
    rect(0, 0, PLOT, PLOT, "#e4ecd6")
    rect(0, 0, 70, PLOT, "#c9dbb4"); lab(35, 160, "GROVE")
    rect(258, 0, 70.08, PLOT, "#c9dbb4"); lab(293, 160, "GROVE")
    rect(0, 268, PLOT, 60.08, "#c9dbb4"); lab(164, 312, "GROVE AND BUFFER (native trees, left to grow)")
    rect(70, 262, 188, 6, "#c9dbb4")
    rect(70, 236, 188, 26, "#dfe8c0"); lab(110, 252, "ORCHARD: orange, jackfruit, banana", 6.4)
    rect(200, 160, 50, 55, "#efe7c4"); lab(225, 185, "KITCHEN"); lab(225, 192, "GARDEN")
    lab(225, 210, "pineapple bed", 5.5, "normal")
    for y in (222, 258, 300):
        a, b = P(72, y)
        c, d = P(256, y + 4)
        o.append(f'<path d="M {_f(a)} {_f(b)} Q {_f((a+c)/2)} {_f(b+10)} {_f(c)} {_f(d)}" fill="none" stroke="#2c6fa8" stroke-width="1.3" stroke-dasharray="6 3"/>')
    lab(258, 226, "swale on contour", 5.5, "normal", "#2c6fa8", "start")
    px, py = P(100, 300)
    o.append(f'<ellipse cx="{_f(px)}" cy="{_f(py)}" rx="{_f(15*S)}" ry="{_f(9*S)}" fill="#b9d6ee" stroke="#2c6fa8"/>')
    lab(100, 302, "POND", 6, "bold", "#1d4e89")
    a, b = P(164, 0)
    rect(158, 0, 12, 115, "#d9d2c3", "#9c927f")
    cx, cy, r = RING
    a, b = P(cx, cy)
    o.append(f'<circle cx="{_f(a)}" cy="{_f(b)}" r="{_f(r*S)}" fill="#d9d2c3" stroke="#9c927f" stroke-width="0.6"/>')
    o.append(f'<circle cx="{_f(a)}" cy="{_f(b)}" r="{_f(6*S)}" fill="#bcd3a0" stroke="#6d8a4a"/>')
    lab(164, 137, "Champak", 4.6, "bold", "#2f4a1a")
    lab(173, 60, "GRAVEL DRIVE 12.00 ft", 6, "bold", "#444", "start")
    lab(186, 125, "turning circle 40.00 ft dia", 5.5, "normal", "#444", "start")
    rect(CP[0], CP[1], CP[2], CP[3], "#8d8d8d", "#222"); lab(122, 134, "CARPORT", 5.2, "bold", "#fff")
    rect(131, 127, 13, 8, "#d9d2c3", "#9c927f")
    rect(HX - 0.375, HY + 28.375, 46.75, 8, "#efe6d2", "#c8b892")
    rect(HX + 17, HY - 6.4, 10, 6, "#efe6d2", "#c8b892")
    rect(HX - 0.375, HY - 0.375, 46.75, 28.75, "#5a5a5a", "#222")
    lab(HX + 23, HY + 14, "HOUSE", 7, "bold", "#fff")
    lab(HX + 23, HY + 21, "46.75 x 28.75 ft", 5.2, "normal", "#fff")
    rect(161, HY + 36.4, 6, FY - HY - 37.4, "#d9d2c3")
    rect(FX - 1, FY - 1, 14, 14, "#e8dcc0"); rect(FX, FY, 12, 12, "#8a6a50", "#222")
    a, b = P(FX + 6, FY + 6)
    o.append(f'<circle cx="{_f(a)}" cy="{_f(b)}" r="{_f(2*S)}" fill="#e07a2f"/>')
    lab(FX + 6, FY + 19, "FIREHOUSE", 6, "bold", "#3d2a1a")
    lab(150, 222, "lawn", 5.5, "normal")
    a, b = P(198, 172)
    o.append(f'<circle cx="{_f(a)}" cy="{_f(b)}" r="{_f(5*S)}" fill="#b9d6ee" stroke="#2c6fa8"/>')
    lab(206, 172, "rain tank 10.00 ft dia", 5, "normal", "#1d4e89", "start")
    rect(118, 186, 6, 4, "#bbb", "#666"); lab(116, 196, "septic + soak pit", 5, "normal", "#444", "start")
    a, b = P(0, 0)
    o.append(f'<rect x="{_f(a)}" y="{_f(b)}" width="{_f(PLOT*S)}" height="{_f(PLOT*S)}" fill="none" stroke="#555" stroke-width="1.4" stroke-dasharray="6 3"/>')
    for x0, x1 in ((128, 158), (173.5, 203.5)):
        a, b = P(x0, 0)
        o.append(f'<rect x="{_f(a)}" y="{_f(b-3)}" width="{_f((x1-x0)*S)}" height="6" fill="#9c8f74" stroke="#333"/>')
    a, b = P(158, 0)
    o.append(f'<rect x="{_f(a)}" y="{_f(b-3)}" width="{_f(12*S)}" height="6" fill="#fff" stroke="#000"/>')
    lab(164, -4, "GATE 12.00 ft + wicket 3.50 ft; stone wall 30.00 ft each side; chain-link fence elsewhere", 6.2, "bold", "#000")
    random.seed(4)
    for _ in range(140):
        x, y = random.uniform(5, PLOT - 5), random.uniform(5, PLOT - 5)
        if x < 66 or x > 262 or y > 272:
            a, b = P(x, y)
            o.append(f'<circle cx="{_f(a)}" cy="{_f(b)}" r="{_f(random.uniform(4,7))}" fill="#7da35a" opacity="0.55"/>')
    for x in range(84, 250, 18):
        a, b = P(x, 244)
        o.append(f'<circle cx="{_f(a)}" cy="{_f(b)}" r="4" fill="#e3a43a" opacity="0.8"/>')
        a, b = P(x + 9, 256)
        o.append(f'<circle cx="{_f(a)}" cy="{_f(b)}" r="4" fill="#6f9a3f" opacity="0.8"/>')
    lx0 = ox + PLOT * S + 14
    for i, (c, t) in enumerate([("#c9dbb4", "Grove"), ("#dfe8c0", "Orchard"), ("#efe7c4", "Kitchen garden"),
                                ("#d9d2c3", "Gravel"), ("#b9d6ee", "Water")]):
        o.append(f'<rect x="{_f(lx0)}" y="{_f(oy+40+i*16)}" width="12" height="10" fill="{c}" stroke="#888" stroke-width="0.4"/>')
        o.append(tag(lx0 + 17, oy + 49 + i * 16, t, 7, anchor="start"))
    o.append(tag(lx0, oy + 150, "Ground falls north", 7, "bold", anchor="start"))
    o.append(tag(lx0, oy + 160, "to south, 1:15", 7, anchor="start"))
    nx, ny = lx0 + 40, oy + 220
    o.append(f'<path d="M {nx} {ny-18} L {nx-8} {ny+8} L {nx} {ny+3} L {nx+8} {ny+8} Z" fill="{INK}"/>')
    o.append(tag(nx, ny - 22, "N", 9, "bold"))
    sy = oy + 270
    o.append(f'<rect x="{_f(lx0)}" y="{_f(sy)}" width="{_f(50*S)}" height="5" fill="none" stroke="#000"/>')
    o.append(f'<rect x="{_f(lx0)}" y="{_f(sy)}" width="{_f(25*S)}" height="5" fill="#000"/>')
    o.append(tag(lx0, sy + 15, "0", 6.5, anchor="start"))
    o.append(tag(lx0 + 50 * S, sy + 15, "50 ft", 6.5, anchor="end"))
    o.append(tag(lx0, sy + 40, "Plot 328.08 x 328.08 ft", 7, "bold", anchor="start"))
    o.append(tag(lx0, sy + 50, "= 1,07,636 sq ft = 1 ha", 7, anchor="start"))
    o.append("</svg>")
    return "\n".join(o)


def roof_plan():
    S = 11.0
    ox, oy = 50, 130
    W, H = ox * 2 + 52 * S + 20, oy + 41 * S + 50
    P = lambda x, y: (ox + (x + 3) * S, oy + y * S)
    o = [f'<svg viewBox="0 0 {W:.0f} {H:.0f}" xmlns="http://www.w3.org/2000/svg" class="dwg">',
         f'<rect width="{W:.0f}" height="{H:.0f}" fill="{FILL}"/>']

    def poly(pts, fill):
        o.append('<polygon points="' + " ".join(f"{_f(P(x, y)[0])},{_f(P(x, y)[1])}" for x, y in pts) + f'" fill="{fill}" stroke="#222" stroke-width="0.8"/>')
    poly([(-3, 29), (49.375, 29), (49.375, 38), (-3, 38)], "#8d8d8d")
    poly([(-3, -3), (49, -3), (49, 29.5), (-3, 29.5)], "#5c5c5c")
    poly([(16.5, -7), (27.5, -7), (27.5, -3), (16.5, -3)], "#6c6c6c")
    for (x0, y0), (x1, y1) in [((-3, -3), (13.25, 13.25)), ((49, -3), (32.75, 13.25)), ((-3, 29.5), (13.25, 13.25)),
                               ((49, 29.5), (32.75, 13.25)), ((13.25, 13.25), (32.75, 13.25))]:
        a, b = P(x0, y0)
        c, d = P(x1, y1)
        o.append(f'<line x1="{_f(a)}" y1="{_f(b)}" x2="{_f(c)}" y2="{_f(d)}" stroke="#ddd" stroke-width="1"/>')
    for pts in ([(-3, -3), (16.5, -3)], [(27.5, -3), (49, -3)], [(-3, 38), (49.375, 38)], [(16.5, -7), (27.5, -7)],
                [(-3, -3), (-3, 29)], [(49, -3), (49, 29)]):
        a, b = P(*pts[0])
        c, d = P(*pts[1])
        o.append(f'<line x1="{_f(a)}" y1="{_f(b)}" x2="{_f(c)}" y2="{_f(d)}" stroke="#2c6fa8" stroke-width="2.6"/>')
    dps = [(2, -3), (44, -3), (2, 38), (23, 38), (44, 38), (49, 13)]
    for x, y in dps:
        a, b = P(x, y)
        o.append(f'<circle cx="{_f(a)}" cy="{_f(b)}" r="4.2" fill="#fff" stroke="#1d4e89" stroke-width="1.6"/>')
    r = rain()
    o.append(tag(*P(23, 6), "MAIN ROOF 52.00 x 32.50 ft, 25° hipped, charcoal profile sheet", 7.4, "bold", "#fff"))
    o.append(tag(*P(23, 34), "VERANDA ROOF 52.38 x 9.00 ft at 1:6", 7, "bold", "#fff"))
    o.append(tag(*P(22, -4.6), "PORCH", 6, "bold", "#fff"))
    o.append(tag(*P(23, 40.6), f"Roof area {r['area']:,.2f} sq ft ÷ {500} sq ft per pipe = {r['area']/500:.2f}, so {r['pipes']} needed; {len(dps)} downpipes of 0.33 ft dia provided", 7, "bold", "#1d4e89"))
    o.append(tag(*P(23, -9.5), "Gutters 0.50 ft wide x 0.33 ft deep, laid 1:200 to the outlets. 3.00 ft overhang on north, east and west.", 6.8, fill="#333"))
    o.append("</svg>")
    return "\n".join(o)

"""Site plan (one hectare) and roof drainage plan."""
import math
from svg_plan import tag, _f, INK, FILL

PLOT = 328.08          # ft, square plot = 1 ha
HX, HY = 115, 120      # house CL origin on site
GX, GY = 186, 44       # garage block origin on site
FX, FY = 139, 207      # firehouse CL origin (20 x 20)
RING = (156, 84, 24, 9)  # forecourt centre x, y, outer r, island r


def site_plan():
    S = 2.15
    ox, oy = 30, 30
    W = ox * 2 + PLOT * S + 150
    H = oy * 2 + PLOT * S + 10
    P = lambda x, y: (ox + x * S, oy + y * S)
    o = [f'<svg viewBox="0 0 {W:.0f} {H:.0f}" xmlns="http://www.w3.org/2000/svg" class="dwg">',
         f'<rect width="{W:.0f}" height="{H:.0f}" fill="{FILL}"/>']
    # zones
    def zone(x0, y0, x1, y1, col, label, lx=None, ly=None):
        a, b = P(x0, y0)
        o.append(f'<rect x="{_f(a)}" y="{_f(b)}" width="{_f((x1-x0)*S)}" height="{_f((y1-y0)*S)}" fill="{col}"/>')
        if label:
            cx, cy = P(lx if lx is not None else (x0 + x1) / 2, ly if ly is not None else (y0 + y1) / 2)
            o.append(tag(cx, cy, label, 7, "bold", "#3d4a2a"))
    zone(0, 0, PLOT, PLOT, "#e4ecd6", None)
    zone(0, 0, 70, PLOT, "#c9dbb4", "GROVE", 35, 160)
    zone(258, 0, PLOT, PLOT, "#c9dbb4", "GROVE", 293, 160)
    zone(0, 268, PLOT, PLOT, "#c9dbb4", "GROVE AND BUFFER (native trees)", 164, 312)
    zone(70, 236, 258, 268, "#dfe8c0", "ORCHARD: orange, jackfruit, areca, banana", 164, 254)
    zone(196, 176, 258, 236, "#efe7c4", "KITCHEN", 227, 202)
    o.append(tag(*P(227, 209), "GARDEN", 7, "bold", "#3d4a2a"))
    zone(70, 176, 196, 236, "#d6e6c4", None)
    o.append(tag(*P(110, 200), "PRIVATE", 7, "bold", "#3d4a2a"))
    o.append(tag(*P(110, 207), "GARDEN", 7, "bold", "#3d4a2a"))
    # pineapple terraces & bamboo
    o.append(tag(*P(227, 230), "pineapple terraces", 5.5, fill="#3d4a2a"))
    o.append(tag(*P(35, 20), "bamboo screen", 5.5, fill="#3d4a2a"))
    # swales (contours) and pond
    for y in (172, 232, 266):
        a, b = P(72, y)
        c, d = P(256, y + 4)
        o.append(f'<path d="M {_f(a)} {_f(b)} Q {_f((a+c)/2)} {_f(b+10)} {_f(c)} {_f(d)}" fill="none" stroke="#2c6fa8" stroke-width="1.3" stroke-dasharray="6 3"/>')
    o.append(tag(*P(262, 238), "swale on contour", 5.5, "normal", "#2c6fa8", "start"))
    px, py = P(96, 292)
    o.append(f'<ellipse cx="{_f(px)}" cy="{_f(py)}" rx="{_f(22*S)}" ry="{_f(12*S)}" fill="#b9d6ee" stroke="#2c6fa8"/>')
    o.append(tag(px, py + 2, "RETENTION POND", 6, "bold", "#1d4e89"))
    for sx in (130, 150):
        a, b = P(sx, 296)
        o.append(f'<circle cx="{_f(a)}" cy="{_f(b)}" r="{_f(3*S)}" fill="none" stroke="#2c6fa8" stroke-width="1"/>')
    o.append(tag(*P(140, 304), "soakaways", 5.5, fill="#1d4e89"))
    a, b = P(118, 300)
    c, d = P(118, PLOT)
    o.append(f'<line x1="{_f(a)}" y1="{_f(b)}" x2="{_f(c)}" y2="{_f(d)}" stroke="#2c6fa8" stroke-width="1.3" stroke-dasharray="3 2"/>')
    o.append(tag(*P(121, 324), "overflow to natural stream", 5.5, "normal", "#1d4e89", "start"))
    # drive, forecourt, spur, visitor bay
    def poly(pts, fill, stroke="#9c927f"):
        o.append('<polygon points="' + " ".join(f"{_f(P(x, y)[0])},{_f(P(x, y)[1])}" for x, y in pts) + f'" fill="{fill}" stroke="{stroke}" stroke-width="0.6"/>')
    poly([(150, 0), (162, 0), (162, 62), (150, 62)], "#d9d2c3")
    poly([(162, 30), (244, 30), (244, 44), (162, 44)], "#d9d2c3")
    poly([(118, 70), (134, 70), (134, 88), (118, 88)], "#d9d2c3")
    cx, cy, R, r = RING
    a, b = P(cx, cy)
    o.append(f'<circle cx="{_f(a)}" cy="{_f(b)}" r="{_f(R*S)}" fill="#d9d2c3" stroke="#9c927f" stroke-width="0.6"/>')
    o.append(f'<circle cx="{_f(a)}" cy="{_f(b)}" r="{_f(r*S)}" fill="#bcd3a0" stroke="#6d8a4a"/>')
    o.append(f'<circle cx="{_f(a)}" cy="{_f(b)}" r="{_f(6*S)}" fill="#7da35a" opacity="0.8"/>')
    o.append(tag(a, b + 2, "Champak", 5, "bold", "#fff"))
    o.append(tag(*P(126, 80), "visitor", 5, fill="#444"))
    o.append(tag(*P(126, 85), "bay", 5, fill="#444"))
    o.append(tag(*P(167, 18), "DRIVE 12 ft 0 in", 6, "bold", "#444", "start"))
    o.append(tag(*P(167, 25), "pavers, camber 1 in 50", 5.5, "normal", "#444", "start"))
    o.append(tag(*P(200, 39), "garage spur", 5.5, "normal", "#444", "middle"))
    o.append(tag(*P(cx - 46, cy + 30), "forecourt ring 48 ft dia", 5.5, "normal", "#444", "start"))
    # house, verandas, porch
    poly([(HX - 0.5, HY + 40), (HX + 98.5, HY + 40), (HX + 98.5, HY + 49), (HX - 0.5, HY + 49)], "#efe6d2")
    poly([(HX + 18, HY - 8), (HX + 62, HY - 8), (HX + 62, HY), (HX + 18, HY)], "#efe6d2")
    poly([(HX + 31, HY - 22), (HX + 51, HY - 22), (HX + 51, HY - 8), (HX + 31, HY - 8)], "#e8dcc0")
    poly([(HX, HY), (HX + 98, HY), (HX + 98, HY + 40), (HX, HY + 40)], "#5a5a5a", "#222")
    o.append(tag(*P(HX + 49, HY + 22), "MAIN HOUSE", 8, "bold", "#fff"))
    o.append(tag(*P(HX + 49, HY + 30), "FFL +2 ft 6 in", 5.5, fill="#fff"))
    poly([(HX + 62, HY - 12), (HX + 80, HY - 12), (HX + 80, HY), (HX + 62, HY)], "#ece6da")
    o.append(tag(*P(HX + 71, HY - 5), "yard", 5, fill="#444"))
    # garage block and covered link
    poly([(GX, GY), (GX + 41, GY), (GX + 41, GY + 23), (GX, GY + 23)], "#6a6a6a", "#222")
    poly([(GX + 41, GY), (GX + 58, GY), (GX + 58, GY + 19), (GX + 41, GY + 19)], "#7a5a48", "#222")
    o.append(tag(*P(GX + 20, GY + 13), "GARAGE", 6, "bold", "#fff"))
    o.append(tag(*P(GX + 49.5, GY + 11), "STUDIO", 5.5, "bold", "#fff"))
    lx = GX + 35.5
    poly([(lx - 3, GY + 23), (lx + 3, GY + 23), (lx + 3, HY - 10), (HX + 62, HY - 10), (HX + 62, HY - 16), (lx - 3, HY - 16)], "#efe6d2")
    o.append(tag(*P(lx + 6, GY + 44), "covered link", 5.5, "normal", "#5b4a2a", "start"))
    # firehouse and path
    poly([(HX + 31, HY + 49), (HX + 37, HY + 49), (HX + 37, FY - 2), (HX + 31, FY - 2)], "#d9d2c3")
    poly([(FX - 2, FY - 2), (FX + 22, FY - 2), (FX + 22, FY + 22), (FX - 2, FY + 22)], "#e8dcc0")
    poly([(FX, FY), (FX + 20, FY), (FX + 20, FY + 20), (FX, FY + 20)], "#8a6a50", "#222")
    fx, fy = P(FX + 10, FY + 10)
    o.append(f'<circle cx="{_f(fx)}" cy="{_f(fy)}" r="{_f(2*S)}" fill="#e07a2f"/>')
    o.append(tag(fx, fy + 15 * S, "FIREHOUSE", 6.5, "bold", "#3d2a1a"))
    o.append(tag(*P(HX + 40, HY + 70), "lawn", 5.5, "normal", "#3d4a2a", "start"))
    # RWH sump
    poly([(222, 132), (242, 132), (242, 144), (222, 144)], "#b9d6ee", "#2c6fa8")
    o.append(tag(*P(232, 140), "RWH", 5.5, "bold", "#1d4e89"))
    o.append(tag(*P(232, 151), "sump 61,000 L", 5, "normal", "#1d4e89"))
    # compound wall + gate
    a, b = P(0, 0)
    o.append(f'<rect x="{_f(a)}" y="{_f(b)}" width="{_f(PLOT*S)}" height="{_f(PLOT*S)}" fill="none" stroke="#3a3a3a" stroke-width="2.4"/>')
    g0, gy = P(149, 0)
    o.append(f'<rect x="{_f(g0)}" y="{_f(gy-3)}" width="{_f(14*S)}" height="6" fill="#fff" stroke="#000"/>')
    o.append(tag(*P(156, -4), "MAIN GATE 14 ft + wicket 3 ft 6 in", 6.5, "bold", "#000"))
    # trees in grove
    import random
    random.seed(4)
    for _ in range(140):
        x, y = random.uniform(5, PLOT - 5), random.uniform(5, PLOT - 5)
        inside = (x < 66 or x > 262 or y > 272)
        if inside:
            a, b = P(x, y)
            o.append(f'<circle cx="{_f(a)}" cy="{_f(b)}" r="{_f(random.uniform(4,7)*S/2.15)}" fill="#7da35a" opacity="0.55"/>')
    for x in range(84, 250, 18):
        a, b = P(x, 244)
        o.append(f'<circle cx="{_f(a)}" cy="{_f(b)}" r="4" fill="#e3a43a" opacity="0.8"/>')
        a, b = P(x + 9, 260)
        o.append(f'<circle cx="{_f(a)}" cy="{_f(b)}" r="4" fill="#6f9a3f" opacity="0.8"/>')
    # legend, slope, north, scale
    lx0 = ox + PLOT * S + 14
    items = [("#c9dbb4", "Grove and buffer"), ("#dfe8c0", "Orchard"), ("#efe7c4", "Kitchen garden"),
             ("#d6e6c4", "Private garden"), ("#d9d2c3", "Drive and paving"), ("#b9d6ee", "Water")]
    for i, (c, t) in enumerate(items):
        o.append(f'<rect x="{_f(lx0)}" y="{_f(oy+40+i*16)}" width="12" height="10" fill="{c}" stroke="#888" stroke-width="0.4"/>')
        o.append(tag(lx0 + 17, oy + 49 + i * 16, t, 7, anchor="start"))
    o.append(f'<line x1="{_f(lx0)}" y1="{_f(oy+150)}" x2="{_f(lx0+26)}" y2="{_f(oy+150)}" stroke="#2c6fa8" stroke-width="1.3" stroke-dasharray="6 3"/>')
    o.append(tag(lx0 + 30, oy + 153, "Swale", 7, anchor="start"))
    o.append(tag(lx0, oy + 185, "Ground falls", 7, "bold", anchor="start"))
    o.append(tag(lx0, oy + 195, "north to south,", 7, anchor="start"))
    o.append(tag(lx0, oy + 205, "about 1 in 15", 7, anchor="start"))
    o.append(f'<path d="M {_f(lx0+60)} {_f(oy+175)} L {_f(lx0+60)} {_f(oy+215)}" stroke="#555" stroke-width="1.5" marker-end="url(#ar)"/>')
    o.append('<defs><marker id="ar" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#555"/></marker></defs>')
    nx, ny = lx0 + 40, oy + 270
    o.append(f'<path d="M {nx} {ny-18} L {nx-8} {ny+8} L {nx} {ny+3} L {nx+8} {ny+8} Z" fill="{INK}"/>')
    o.append(tag(nx, ny - 22, "N", 9, "bold"))
    sy = oy + 320
    o.append(f'<rect x="{_f(lx0)}" y="{_f(sy)}" width="{_f(50*S)}" height="5" fill="none" stroke="#000"/>')
    o.append(f'<rect x="{_f(lx0)}" y="{_f(sy)}" width="{_f(25*S)}" height="5" fill="#000"/>')
    o.append(tag(lx0, sy + 15, "0", 6.5, anchor="start"))
    o.append(tag(lx0 + 50 * S, sy + 15, "50 ft", 6.5, anchor="end"))
    o.append(tag(lx0, sy + 40, "Plot 328 ft x 328 ft", 7, "bold", anchor="start"))
    o.append(tag(lx0, sy + 50, "= 1,07,639 sq ft", 7, anchor="start"))
    o.append(tag(lx0, sy + 60, "= 1 hectare", 7, anchor="start"))
    o.append("</svg>")
    return "\n".join(o)


def roof_plan():
    S = 5.6
    ox, oy = 40, 160
    W, H = ox * 2 + 104 * S + 10, oy + 54 * S + 40
    P = lambda x, y: (ox + (x + 3) * S, oy + y * S)
    o = [f'<svg viewBox="0 0 {W:.0f} {H:.0f}" xmlns="http://www.w3.org/2000/svg" class="dwg">',
         f'<rect width="{W:.0f}" height="{H:.0f}" fill="{FILL}"/>']

    def poly(pts, fill, sw=0.8):
        o.append('<polygon points="' + " ".join(f"{_f(P(x, y)[0])},{_f(P(x, y)[1])}" for x, y in pts) + f'" fill="{fill}" stroke="#222" stroke-width="{sw}"/>')
    poly([(-3, 40), (101, 40), (101, 50), (-3, 50)], "#8d8d8d")          # veranda roof 1 in 6
    poly([(-3, -3), (101, -3), (101, 40), (-3, 40)], "#5c5c5c")               # main roof
    poly([(29.5, -23.5), (52.5, -23.5), (52.5, -3), (29.5, -3)], "#6c6c6c")   # porch roof
    for (x0, y0), (x1, y1) in [((-3, -3), (18.5, 18.5)), ((101, -3), (79.5, 18.5)), ((-3, 40), (18.5, 18.5)),
                               ((101, 40), (79.5, 18.5)), ((18.5, 18.5), (79.5, 18.5)),
                               ((29.5, -23.5), (41, -12)), ((52.5, -23.5), (41, -12)), ((41, -12), (41, -3))]:
        a, b = P(x0, y0)
        c, d = P(x1, y1)
        o.append(f'<line x1="{_f(a)}" y1="{_f(b)}" x2="{_f(c)}" y2="{_f(d)}" stroke="#ddd" stroke-width="1"/>')
    # gutters
    for pts in ([(-3, -3), (29.5, -3)], [(52.5, -3), (101, -3)], [(-3, 50), (101, 50)],
                [(29.5, -23.5), (52.5, -23.5)], [(-3, -3), (-3, 40)], [(101, -3), (101, 40)]):
        a, b = P(*pts[0])
        c, d = P(*pts[1])
        o.append(f'<line x1="{_f(a)}" y1="{_f(b)}" x2="{_f(c)}" y2="{_f(d)}" stroke="#2c6fa8" stroke-width="2.6"/>')
    dps = [(5, -3), (24, -3), (60, -3), (80, -3), (96, -3), (29.5, -23.5), (52.5, -23.5),
           (5, 50), (28, 50), (50, 50), (72, 50), (95, 50), (-3, 20), (101, 20)]
    for x, y in dps:
        a, b = P(x, y)
        o.append(f'<circle cx="{_f(a)}" cy="{_f(b)}" r="4.2" fill="#fff" stroke="#1d4e89" stroke-width="1.6"/>')
    o.append(tag(*P(49, 9), "MAIN HIPPED ROOF, 25° pitch, charcoal standing-seam steel", 7.5, "bold", "#fff"))
    o.append(tag(*P(49, 30), "hip ridge about 58 ft long, +24 ft 3 in above FFL; wall plate +15 ft 0 in", 6.5, fill="#fff"))
    o.append(tag(*P(49, 46.6), "VERANDA ROOF, 1 in 6 (9½°), eave 12 ft 5 in above FFL", 6.8, "bold", "#fff"))
    o.append(tag(*P(41, -15), "PORCH", 6, "bold", "#fff"))
    o.append(tag(*P(49, 56.5), f"{len(dps)} downpipes of 4 in dia (12 needed at 500 sq ft each), 7 in x 5 in box gutters laid 1 in 200 to outlets", 7, "bold", "#1d4e89"))
    o.append(tag(*P(49, -27), "3 ft 0 in overhang on north, east and west faces; south face oversails the veranda roof by 1 ft 6 in with a lead-free flashing apron", 6.5, fill="#333"))
    o.append("</svg>")
    return "\n".join(o)

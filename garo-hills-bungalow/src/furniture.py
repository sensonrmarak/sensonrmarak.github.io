"""Furniture and fixture symbols for presentation plans (coordinates in feet)."""
import math

LN = "#3a3a3a"


class F:
    def __init__(self, S, ox, oy):
        self.S, self.ox, self.oy, self.o = S, ox, oy, []

    def X(self, x):
        return self.ox + x * self.S

    def Y(self, y):
        return self.oy + y * self.S

    def rect(self, x, y, w, h, fill="#fff", sw=0.7, rx=0, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.o.append(f'<rect x="{self.X(x):.1f}" y="{self.Y(y):.1f}" width="{w*self.S:.1f}" height="{h*self.S:.1f}" rx="{rx*self.S:.1f}" fill="{fill}" stroke="{LN}" stroke-width="{sw}"{d}/>')

    def circ(self, x, y, r, fill="#fff", sw=0.7):
        self.o.append(f'<circle cx="{self.X(x):.1f}" cy="{self.Y(y):.1f}" r="{r*self.S:.1f}" fill="{fill}" stroke="{LN}" stroke-width="{sw}"/>')

    def line(self, x1, y1, x2, y2, sw=0.6, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.o.append(f'<line x1="{self.X(x1):.1f}" y1="{self.Y(y1):.1f}" x2="{self.X(x2):.1f}" y2="{self.Y(y2):.1f}" stroke="{LN}" stroke-width="{sw}"{d}/>')

    # ---- symbols
    def bed(self, x, y, w, l, head="N"):
        """Bed with headboard on side `head`. (x,y) top-left of footprint."""
        if head in "NS":
            self.rect(x, y, w, l, "#fff", 0.8, 0.3)
            py = y + 0.4 if head == "N" else y + l - 2.0
            self.rect(x + 0.4, py, w / 2 - 0.6, 1.6, "#f3f3f3", 0.6, 0.4)
            self.rect(x + w / 2 + 0.2, py, w / 2 - 0.6, 1.6, "#f3f3f3", 0.6, 0.4)
            fy = y + l * 0.45 if head == "N" else y
            self.line(x, fy if head == "N" else y + l * 0.55, x + w, fy if head == "N" else y + l * 0.55, 0.6)
        else:
            self.rect(x, y, l, w, "#fff", 0.8, 0.3)
            px = x + 0.4 if head == "W" else x + l - 2.0
            self.rect(px, y + 0.4, 1.6, w / 2 - 0.6, "#f3f3f3", 0.6, 0.4)
            self.rect(px, y + w / 2 + 0.2, 1.6, w / 2 - 0.6, "#f3f3f3", 0.6, 0.4)
            fx = x + l * 0.45 if head == "W" else x + l * 0.55
            self.line(fx, y, fx, y + w, 0.6)

    def nightstand(self, x, y):
        self.rect(x, y, 1.6, 1.6, "#fff", 0.6, 0.15)
        self.circ(x + 0.8, y + 0.8, 0.45, "#fff", 0.5)

    def sofa(self, x, y, w, d=3.0, back="N"):
        if back in "NS":
            self.rect(x, y, w, d, "#fff", 0.8, 0.4)
            by = y if back == "N" else y + d - 0.8
            self.rect(x, by, w, 0.8, "#eee", 0.6, 0.3)
            self.rect(x, y, 0.8, d, "#eee", 0.6, 0.3)
            self.rect(x + w - 0.8, y, 0.8, d, "#eee", 0.6, 0.3)
            n = max(2, round(w / 2.6))
            for i in range(1, n):
                xx = x + 0.8 + (w - 1.6) * i / n
                self.line(xx, y + (0.8 if back == "N" else 0), xx, y + d - (0 if back == "N" else 0.8), 0.5)
        else:
            self.rect(x, y, d, w, "#fff", 0.8, 0.4)
            bx = x if back == "W" else x + d - 0.8
            self.rect(bx, y, 0.8, w, "#eee", 0.6, 0.3)
            self.rect(x, y, d, 0.8, "#eee", 0.6, 0.3)
            self.rect(x, y + w - 0.8, d, 0.8, "#eee", 0.6, 0.3)

    def chair(self, x, y, s=2.6, back="N"):
        self.rect(x, y, s, s, "#fff", 0.7, 0.4)
        if back == "N":
            self.rect(x, y, s, 0.6, "#eee", 0.5, 0.2)
        elif back == "S":
            self.rect(x, y + s - 0.6, s, 0.6, "#eee", 0.5, 0.2)
        elif back == "W":
            self.rect(x, y, 0.6, s, "#eee", 0.5, 0.2)
        else:
            self.rect(x + s - 0.6, y, 0.6, s, "#eee", 0.5, 0.2)

    def table(self, x, y, w, l, seats_long=0, seats_end=0, vertical=True):
        if vertical:
            self.rect(x, y, w, l, "#fff", 0.8, 0.15)
            for i in range(seats_long):
                yy = y + l * (i + 0.5) / seats_long - 0.75
                self.rect(x - 1.7, yy, 1.4, 1.5, "#fff", 0.6, 0.3)
                self.rect(x + w + 0.3, yy, 1.4, 1.5, "#fff", 0.6, 0.3)
            if seats_end:
                self.rect(x + w / 2 - 0.75, y - 1.7, 1.5, 1.4, "#fff", 0.6, 0.3)
                self.rect(x + w / 2 - 0.75, y + l + 0.3, 1.5, 1.4, "#fff", 0.6, 0.3)
        else:
            self.rect(x, y, l, w, "#fff", 0.8, 0.15)
            for i in range(seats_long):
                xx = x + l * (i + 0.5) / seats_long - 0.75
                self.rect(xx, y - 1.7, 1.5, 1.4, "#fff", 0.6, 0.3)
                self.rect(xx, y + w + 0.3, 1.5, 1.4, "#fff", 0.6, 0.3)

    def round_table(self, x, y, r, n):
        self.circ(x, y, r, "#fff", 0.8)
        for i in range(n):
            a = 2 * math.pi * i / n + math.pi / 4
            cx, cy = x + (r + 1.0) * math.cos(a), y + (r + 1.0) * math.sin(a)
            self.rect(cx - 0.7, cy - 0.7, 1.4, 1.4, "#fff", 0.6, 0.3)

    def rug(self, x, y, w, h):
        self.rect(x, y, w, h, "none", 0.6, 0, "3 2")

    def wc(self, x, y, facing="S"):
        """x,y = centre of cistern against wall; bowl projects in `facing`."""
        if facing in "NS":
            s = 1 if facing == "S" else -1
            self.rect(x - 0.8, y - (0 if s > 0 else 0.7), 1.6, 0.7, "#fff", 0.7, 0.1)
            cy = y + s * 1.6
            self.o.append(f'<ellipse cx="{self.X(x):.1f}" cy="{self.Y(cy):.1f}" rx="{0.7*self.S:.1f}" ry="{1.0*self.S:.1f}" fill="#fff" stroke="{LN}" stroke-width="0.7"/>')
        else:
            s = 1 if facing == "E" else -1
            self.rect(x - (0 if s > 0 else 0.7), y - 0.8, 0.7, 1.6, "#fff", 0.7, 0.1)
            cx = x + s * 1.6
            self.o.append(f'<ellipse cx="{self.X(cx):.1f}" cy="{self.Y(y):.1f}" rx="{1.0*self.S:.1f}" ry="{0.7*self.S:.1f}" fill="#fff" stroke="{LN}" stroke-width="0.7"/>')

    def basin(self, x, y, w=2.4, d=1.8):
        self.rect(x, y, w, d, "#fff", 0.7, 0.1)
        self.o.append(f'<ellipse cx="{self.X(x+w/2):.1f}" cy="{self.Y(y+d/2):.1f}" rx="{w*0.32*self.S:.1f}" ry="{d*0.3*self.S:.1f}" fill="#fff" stroke="{LN}" stroke-width="0.6"/>')

    def shower(self, x, y, w, h):
        self.rect(x, y, w, h, "#eaf4fb", 0.8)
        self.line(x, y, x + w, y + h, 0.5)
        self.line(x + w, y, x, y + h, 0.5)
        self.circ(x + w / 2, y + h / 2, 0.25, "#fff", 0.6)

    def counter(self, x, y, w, h):
        self.rect(x, y, w, h, "#fff", 0.8)

    def sink(self, x, y, w=2.6, h=1.5):
        self.rect(x, y, w, h, "#fff", 0.7, 0.15)
        self.rect(x + 0.2, y + 0.2, w / 2 - 0.3, h - 0.4, "#fff", 0.5, 0.1)
        self.rect(x + w / 2 + 0.1, y + 0.2, w / 2 - 0.3, h - 0.4, "#fff", 0.5, 0.1)

    def range_(self, x, y, s=2.5):
        self.rect(x, y, s, s * 0.85, "#fff", 0.7)
        for dx in (0.6, 1.9):
            for dy in (0.55, 1.6):
                self.circ(x + dx * s / 2.5, y + dy * s / 2.5 * 0.85, 0.35, "#fff", 0.6)

    def box(self, x, y, w, h, label, fs=4.6):
        self.rect(x, y, w, h, "#fff", 0.7)
        self.o.append(f'<text x="{self.X(x+w/2):.1f}" y="{self.Y(y+h/2)+fs*0.35:.1f}" font-size="{fs}" text-anchor="middle" font-family="Helvetica, Arial" fill="{LN}">{label}</text>')

    def wardrobe(self, x, y, w, h):
        self.rect(x, y, w, h, "#fff", 0.7)
        if w >= h:
            self.line(x + 0.2, y + h / 2, x + w - 0.2, y + h / 2, 0.6, "4 2")
        else:
            self.line(x + w / 2, y + 0.2, x + w / 2, y + h - 0.2, 0.6, "4 2")

    def shelves(self, x, y, w, h):
        self.rect(x, y, w, h, "#efe4cf", 0.7)
        n = int(max(w, h) / 1.5)
        for i in range(1, n):
            if w >= h:
                self.line(x + w * i / n, y, x + w * i / n, y + h, 0.4)
            else:
                self.line(x, y + h * i / n, x + w, y + h * i / n, 0.4)

    def piano(self, x, y):
        p = [(0, 0), (5, 0), (5, 1.6), (4.2, 3.5), (3.0, 6.2), (1.2, 6.8), (0, 6.6)]
        self.o.append('<polygon points="' + " ".join(f"{self.X(x+a):.1f},{self.Y(y+b):.1f}" for a, b in p) + f'" fill="#333" stroke="{LN}" stroke-width="0.7"/>')
        self.rect(x - 1.6, y + 1.6, 1.2, 2.2, "#fff", 0.6, 0.2)

    def drums(self, x, y):
        for dx, dy, r in ((0, 0, 1.1), (1.9, -0.6, 0.6), (-1.8, -0.4, 0.7), (1.6, 1.3, 0.8), (-1.3, 1.5, 0.6)):
            self.circ(x + dx, y + dy, r, "#fff", 0.7)

    def desk(self, x, y, w, d, chair_side="S"):
        self.rect(x, y, w, d, "#fff", 0.8)
        if chair_side == "S":
            self.chair(x + w / 2 - 1.0, y + d + 0.2, 2.0, "S")
        elif chair_side == "N":
            self.chair(x + w / 2 - 1.0, y - 2.2, 2.0, "N")
        elif chair_side == "E":
            self.chair(x + w + 0.2, y + d / 2 - 1.0, 2.0, "E")
        else:
            self.chair(x - 2.2, y + d / 2 - 1.0, 2.0, "W")

    def plant(self, x, y, r=0.9):
        self.circ(x, y, r, "#dcebd0", 0.6)
        for i in range(6):
            a = i * math.pi / 3
            self.line(x, y, x + r * math.cos(a), y + r * math.sin(a), 0.4)


def furnish(S, ox, oy):
    f = F(S, ox, oy)
    # library and study
    f.desk(0.5, 2.6, 2.6, 5.4, "E")
    f.shelves(0.8, 8.4, 9.4, 1.1)
    f.chair(9.0, 1.0, 2.6, "N")
    f.circ(12.2, 2.3, 0.7)
    # bath 1
    f.shower(0.4, 10.4, 3.0, 2.9)
    f.wc(0.4, 15.4, "E")
    f.basin(3.4, 15.3, 2.2, 1.3)
    # dressing 1
    f.wardrobe(6.4, 10.4, 7.2, 1.7)
    # bedroom 1
    f.bed(7.2, 20.0, 5.0, 6.6, "E")
    f.nightstand(12.2, 18.2)
    f.nightstand(12.2, 25.2)
    f.chair(1.0, 17.8, 2.6, "W")
    # dining (north part of the hall)
    f.table(22.5, 5.6, 3.5, 7.0, 3, 1)
    # sitting
    f.rug(16.0, 15.5, 12.0, 10.0)
    f.sofa(17.5, 16.0, 9.0, 3.0, "N")
    f.chair(16.8, 22.0, 2.6, "S")
    f.chair(24.6, 22.0, 2.6, "S")
    f.rect(19.6, 20.0, 5.0, 1.8, "#fff", 0.8, 0.2)
    f.plant(28.8, 1.4)
    # wash lobby
    f.basin(30.5, 0.4, 3.0, 1.6)
    # shared toilet and bathroom, NE corner
    f.wc(39.0, 0.4, "S")
    f.shower(42.6, 0.4, 3.0, 6.2)
    f.basin(35.0, 0.4, 2.0, 1.4)
    # kitchen
    f.counter(33.6, 7.4, 12.0, 2.0)
    f.range_(36.0, 7.5, 2.5)
    f.sink(40.0, 7.6, 2.6, 1.6)
    f.counter(43.6, 9.4, 2.0, 6.2)
    f.box(30.4, 7.4, 2.6, 2.6, "REF", 4.2)
    f.box(30.4, 13.4, 2.2, 2.2, "PANTRY", 3.6)
    f.round_table(41.0, 13.2, 1.4, 2)
    # bedroom 2
    f.bed(34.5, 16.4, 5.0, 6.6, "N")
    f.nightstand(32.7, 16.4)
    f.chair(37.6, 25.0, 2.4, "S")
    # bath 2
    f.shower(42.9, 16.4, 2.7, 2.8)
    f.wc(44.2, 21.6, "N")
    f.basin(40.9, 16.4, 1.7, 1.4)
    # wardrobe 2
    f.wardrobe(43.6, 22.4, 2.0, 5.2)
    # veranda
    for x in (2.0, 15.0, 20.5, 29.0, 41.0):
        f.chair(x, 29.4, 2.4, "N")
    f.rect(24.0, 29.4, 4.0, 1.8, "#fff", 0.7, 0.3)
    return f.o

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
    # study
    f.desk(1, 3.5, 2.6, 6, "E")
    f.shelves(5, 11.3, 8, 1.3)
    f.chair(12.5, 2.5, 2.8, "N")
    f.plant(16.5, 2)
    # library
    f.shelves(30.6, 0.7, 1.0, 11.6)
    f.shelves(19, 0.7, 8, 1.0)
    f.chair(21, 5.5, 2.8, "W")
    f.chair(25.5, 5.5, 2.8, "E")
    f.circ(24.4, 6.9, 0.8)
    # bath 1
    f.shower(0.4, 13.4, 3.6, 3.6)
    f.wc(0.4, 20, "E")
    f.basin(5.2, 21.2, 2.4, 0.4 + 1.2)
    # dressing 1
    f.wardrobe(9.0, 13.4, 8.6, 2.0)
    # bedroom 1
    f.bed(11.2, 28, 6.4, 6.8, "E")
    f.nightstand(16.0, 26.2)
    f.nightstand(16.0, 34.6)
    f.chair(2.0, 35.5, 2.8, "W")
    f.chair(5.4, 35.5, 2.8, "E")
    f.rect(1, 23, 6, 1.8, "#fff", 0.7)
    # foyer
    f.rect(33, 1, 6, 1.6, "#fff", 0.7)
    f.plant(48.4, 1.6)
    # sitting hall
    f.rug(22, 20, 22, 14)
    f.sofa(24.5, 21, 15, 3.2, "N")
    f.sofa(22.5, 25, 7, 3.0, "W")
    f.chair(37.5, 30, 3.0, "E")
    f.chair(33.5, 30, 3.0, "S")
    f.rect(28, 26, 6, 3, "#fff", 0.8, 0.2)
    f.rect(19, 30, 1.2, 8, "#fff", 0.6)
    f.plant(47.5, 37.5)
    # alcove sideboard
    f.rect(51, 0.8, 10, 1.8, "#fff", 0.7)
    # dining
    f.table(54.0, 20.5, 4.0, 10.0, 4, 1)
    f.o.append(f'<line x1="{f.X(50):.1f}" y1="{f.Y(13):.1f}" x2="{f.X(50):.1f}" y2="{f.Y(40):.1f}" stroke="#666" stroke-width="0.6" stroke-dasharray="5 4"/>')
    # kitchen
    f.counter(62.4, 17.4, 15.4, 2.0)
    f.range_(68.5, 17.5, 2.6)
    f.counter(77.6, 17.4, 2.0, 12.6)
    f.sink(77.8, 21.5, 1.6, 2.8)
    f.box(77.8, 25.0, 1.6, 2.0, "DW", 4)
    f.box(62.6, 17.6, 2.6, 2.6, "REF", 4.2)
    f.rect(66.5, 25, 8, 3.5, "#fff", 0.8)
    for i in range(3):
        f.rect(67.6 + i * 2.4, 29, 1.4, 1.4, "#fff", 0.6, 0.3)
    f.round_table(73.5, 35.5, 1.8, 4)
    # store and utility
    f.shelves(62.8, 0.7, 8.4, 1.4)
    f.shelves(62.8, 2.4, 1.4, 9.8)
    f.box(72.6, 0.6, 2.6, 2.6, "W", 4.6)
    f.box(75.4, 0.6, 2.6, 2.6, "D", 4.6)
    f.sink(78.4, 0.7, 3.0, 1.9)
    # wash lobby
    f.counter(82.4, 1.0, 2.0, 8)
    f.basin(82.5, 2.0, 1.8, 2.2)
    f.basin(82.5, 5.6, 1.8, 2.2)
    # shared toilet + bath (NE corner)
    f.wc(97.6, 3.2, "W")
    f.basin(91.2, 0.4, 2.2, 1.5)
    f.shower(94.0, 7.0, 3.6, 5.6)
    f.basin(90.0, 11.0, 2.4, 1.6)
    # dressing 2
    f.wardrobe(80.4, 17.4, 2.0, 6.2)
    # bath 2
    f.shower(93.8, 13.4, 3.8, 3.8)
    f.wc(97.6, 20.2, "W")
    f.basin(90.5, 21.8, 2.4, 1.8)
    # bedroom 2
    f.bed(80.4, 30, 6.0, 6.8, "W")
    f.nightstand(80.4, 28.2)
    f.nightstand(80.4, 36.2)
    f.chair(93.5, 35.5, 2.8, "S")
    f.rect(90.5, 24.4, 6, 1.8, "#fff", 0.7)
    # verandas
    for x in (4, 20, 36, 66, 80, 92):
        f.chair(x, 42.6, 2.6, "N")
    f.rect(25, 42.6, 6, 2.2, "#fff", 0.7, 0.3)
    f.rect(71, 42.6, 6, 2.2, "#fff", 0.7, 0.3)
    f.chair(36, -6.2, 2.4, "N")
    f.chair(55, -6.2, 2.4, "N")
    return f.o

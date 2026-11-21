"""Render views of the bungalow with Blender (bpy). Usage: python b_render.py VIEW OUT.png [samples]"""
import math, random, sys
import bpy
from mathutils import Vector
import b_geo as G
import furniture

VIEW = sys.argv[1] if len(sys.argv) > 1 else "front"
OUT = sys.argv[2] if len(sys.argv) > 2 else "/tmp/r.png"
SAMPLES = int(sys.argv[3]) if len(sys.argv) > 3 else 48
INTERIOR = VIEW in ("hall", "kitchen", "bed1", "library")
CUT = VIEW == "cutaway"


# ------------------------------------------------------------------ 3D furniture
class F3D:
    """Same calls as furniture.F, building 3D objects instead of SVG."""
    def __init__(self, *a):
        self.o = []

    def X(self, x):
        return x

    def Y(self, y):
        return y

    def rect(self, x, y, w, h, fill="#fff", sw=0, rx=0, dash=None):
        G.box(x, x + w, y, y + h, 0, 1.6, "timber", "furn")

    def circ(self, x, y, r, fill="#fff", sw=0):
        G.cyl(x, y, 0, 1.9, r, "timber", 20, "sidetable")

    def line(self, *a, **k):
        pass

    def rug(self, x, y, w, h):
        G.box(x, x + w, y, y + h, 0.02, 0.06, "rug", "rug")

    def bed(self, x, y, w, l, head="N"):
        if head in "NS":
            x1, y1 = x + w, y + l
        else:
            x1, y1 = x + l, y + w
        G.box(x, x1, y, y1, 0, 1.2, "timber", "bedbase")
        G.box(x + 0.1, x1 - 0.1, y + 0.1, y1 - 0.1, 1.2, 2.0, "bedding", "mattress")
        hb = {"N": (x, x1, y, y + 0.3), "S": (x, x1, y1 - 0.3, y1), "W": (x, x + 0.3, y, y1), "E": (x1 - 0.3, x1, y, y1)}[head]
        G.box(*hb, 0, 4.2, "timber", "headboard")
        if head in "EW":
            px = x + 0.5 if head == "W" else x1 - 2.1
            for py in (y + 0.5, y + w / 2 + 0.2):
                G.box(px, px + 1.6, py, py + w / 2 - 0.7, 2.0, 2.5, "bedding", "pillow")
            tx0, tx1 = (x + l * 0.6, x1) if head == "W" else (x, x + l * 0.4)
            G.box(tx0, tx1, y - 0.05, y1 + 0.05, 1.95, 2.1, "fabric_red", "throw")
        else:
            py = y + 0.5 if head == "N" else y1 - 2.1
            for px in (x + 0.5, x + w / 2 + 0.2):
                G.box(px, px + w / 2 - 0.7, py, py + 1.6, 2.0, 2.5, "bedding", "pillow")

    def nightstand(self, x, y):
        G.box(x, x + 1.6, y, y + 1.6, 0, 2.0, "timber", "night")
        G.cyl(x + 0.8, y + 0.8, 2.0, 2.9, 0.15, "brass", 12, "lampstem")
        G.cyl(x + 0.8, y + 0.8, 2.9, 3.6, 0.5, "lamp", 16, "lampshade")

    def sofa(self, x, y, w, d=3.0, back="N"):
        mat = "fabric_red"
        if back in "NS":
            G.box(x, x + w, y, y + d, 0, 1.45, mat, "sofa")
            by = (y, y + 0.8) if back == "N" else (y + d - 0.8, y + d)
            G.box(x, x + w, *by, 0, 2.8, mat, "sofaback")
            G.box(x, x + 0.8, y, y + d, 0, 2.1, mat, "arm")
            G.box(x + w - 0.8, x + w, y, y + d, 0, 2.1, mat, "arm")
            for i in range(int(w // 3)):
                cx = x + 1.2 + i * 3
                G.box(cx, cx + 1.6, by[0] + (0.8 if back == "N" else -0.5), by[0] + (1.3 if back == "N" else 0), 1.45, 2.6, "fabric_linen", "cushion")
        else:
            G.box(x, x + d, y, y + w, 0, 1.45, mat, "sofa")
            bx = (x, x + 0.8) if back == "W" else (x + d - 0.8, x + d)
            G.box(*bx, y, y + w, 0, 2.8, mat, "sofaback")
            G.box(x, x + d, y, y + 0.8, 0, 2.1, mat, "arm")
            G.box(x, x + d, y + w - 0.8, y + w, 0, 2.1, mat, "arm")

    def chair(self, x, y, s=2.6, back="N"):
        G.box(x, x + s, y, y + s, 0, 1.5, "fabric_grey", "chair")
        b = {"N": (x, x + s, y, y + 0.5), "S": (x, x + s, y + s - 0.5, y + s), "W": (x, x + 0.5, y, y + s), "E": (x + s - 0.5, x + s, y, y + s)}[back]
        G.box(*b, 0, 3.0, "fabric_grey", "chairback")

    def _dchair(self, x, y, w, h, back):
        G.box(x, x + w, y, y + h, 1.45, 1.6, "timber", "dseat")
        for lx, ly in ((x, y), (x + w - 0.12, y), (x, y + h - 0.12), (x + w - 0.12, y + h - 0.12)):
            G.box(lx, lx + 0.12, ly, ly + 0.12, 0, 1.45, "timber", "leg")
        b = {"N": (x, x + w, y, y + 0.12), "S": (x, x + w, y + h - 0.12, y + h), "W": (x, x + 0.12, y, y + h), "E": (x + w - 0.12, x + w, y, y + h)}[back]
        G.box(*b, 1.6, 3.2, "timber", "dback")

    def table(self, x, y, w, l, seats_long=0, seats_end=0, vertical=True):
        if not vertical:
            w, l = l, w
        G.box(x, x + w, y, y + l, 2.35, 2.5, "timber", "tabletop")
        for lx, ly in ((x + 0.2, y + 0.2), (x + w - 0.45, y + 0.2), (x + 0.2, y + l - 0.45), (x + w - 0.45, y + l - 0.45)):
            G.box(lx, lx + 0.25, ly, ly + 0.25, 0, 2.35, "timber", "leg")
        for i in range(seats_long):
            yy = y + l * (i + 0.5) / seats_long - 0.75
            self._dchair(x - 1.7, yy, 1.4, 1.5, "W")
            self._dchair(x + w + 0.3, yy, 1.4, 1.5, "E")
        if seats_end:
            self._dchair(x + w / 2 - 0.75, y - 1.7, 1.5, 1.4, "N")
            self._dchair(x + w / 2 - 0.75, y + l + 0.3, 1.5, 1.4, "S")

    def round_table(self, x, y, r, n):
        G.cyl(x, y, 2.35, 2.5, r, "timber", 32, "rtable")
        G.cyl(x, y, 0, 2.35, 0.2, "timber", 12, "rleg")
        for i in range(n):
            a = 2 * math.pi * i / n + math.pi / 4
            cx, cy = x + (r + 1.0) * math.cos(a), y + (r + 1.0) * math.sin(a)
            self._dchair(cx - 0.7, cy - 0.7, 1.4, 1.4, "N" if cy < y else "S")

    def wc(self, x, y, facing="S"):
        if facing in "EW":
            s = 1 if facing == "E" else -1
            G.box(min(x, x + s * 0.7), max(x, x + s * 0.7), y - 0.8, y + 0.8, 0, 3.0, "porcelain", "cistern")
            G.box(min(x, x + s * 2.4), max(x, x + s * 2.4), y - 0.6, y + 0.6, 0, 1.4, "porcelain", "bowl")
        else:
            s = 1 if facing == "S" else -1
            G.box(x - 0.8, x + 0.8, min(y, y + s * 0.7), max(y, y + s * 0.7), 0, 3.0, "porcelain", "cistern")
            G.box(x - 0.6, x + 0.6, min(y, y + s * 2.4), max(y, y + s * 2.4), 0, 1.4, "porcelain", "bowl")

    def basin(self, x, y, w=2.4, d=1.8):
        G.box(x, x + w, y, y + d, 0, 2.7, "timber", "vanity")
        G.box(x + 0.1, x + w - 0.1, y + 0.1, y + d - 0.1, 2.7, 2.85, "porcelain", "basin")

    def shower(self, x, y, w, h):
        G.box(x, x + w, y, y + h, 0.0, 0.03, "stone", "showerfloor")
        G.box(x + w - 0.04, x + w, y, y + h * 0.7, 0, 6.8, "glass", "screen")
        G.cyl(x + 0.4, y + 0.4, 0, 6.8, 0.04, "brass", 8, "riser")

    def counter(self, x, y, w, h):
        G.box(x, x + w, y, y + h, 0, 2.9, "cabinet", "cab")
        G.box(x - 0.05, x + w + 0.05, y - 0.05, y + h + 0.05, 2.9, 3.0, "granite", "top")

    def sink(self, x, y, w=2.6, h=1.5):
        G.box(x + 0.1, x + w - 0.1, y + 0.1, y + h - 0.1, 2.95, 3.02, "porcelain", "sink")

    def range_(self, x, y, s=2.5):
        G.box(x, x + s, y, y + s * 0.85, 0, 3.02, "black", "range")
        G.box(x, x + s, y, y + 1.6, 6.0, 7.4, "black", "hood")
        G.box(x + s / 2 - 0.4, x + s / 2 + 0.4, y, y + 0.8, 7.4, 12.0, "black", "flue")

    def box(self, x, y, w, h, label, fs=4.6):
        if label == "REF":
            G.box(x, x + w, y, y + h, 0, 6.2, "porcelain", "fridge")
        elif label in ("W", "D"):
            G.box(x, x + w, y, y + h, 0, 2.9, "porcelain", "laundry")
        elif label == "DW":
            pass
        elif label == "PANTRY":
            G.box(x, x + w, y, y + h, 0, 7.0, "cabinet", "pantry")
        elif label == "amp":
            G.box(x, x + w, y, y + h, 0, 2.2, "black", "amp")
        else:
            G.box(x, x + w, y, y + h, 2.6, 3.6, "black", "monitor")

    def wardrobe(self, x, y, w, h):
        G.box(x, x + w, y, y + h, 0, 7.6, "cabinet", "wardrobe")

    def shelves(self, x, y, w, h):
        G.box(x, x + w, y, y + h, 0, 7.6, "timber", "shelf")
        n = 6
        for i in range(n):
            z = 0.6 + i * 1.15
            ins = 0.12
            mats = ["fabric_red", "fabric_green", "fabric_linen", "fabric_grey"]
            if w >= h:
                G.box(x + 0.1, x + w - 0.1, y - ins, y + 0.02, z, z + 0.85, mats[i % 4], "books")
                G.box(x + 0.1, x + w - 0.1, y + h - 0.02, y + h + ins, z, z + 0.85, mats[(i + 1) % 4], "books")
            else:
                G.box(x - ins, x + 0.02, y + 0.1, y + h - 0.1, z, z + 0.85, mats[i % 4], "books")
                G.box(x + w - 0.02, x + w + ins, y + 0.1, y + h - 0.1, z, z + 0.85, mats[(i + 1) % 4], "books")

    def piano(self, x, y):
        G.box(x, x + 5, y, y + 6.6, 2.0, 3.3, "piano", "piano")
        G.box(x + 0.3, x + 4.7, y, y + 0.6, 0, 2.0, "piano", "pianofront")
        G.box(x - 1.6, x - 0.4, y + 1.6, y + 3.8, 0, 1.6, "piano", "bench")

    def drums(self, x, y):
        for dx, dy, r in ((0, 0, 1.1), (1.9, -0.6, 0.6), (-1.8, -0.4, 0.7), (1.6, 1.3, 0.8), (-1.3, 1.5, 0.6)):
            G.cyl(x + dx, y + dy, 0.6 if r < 1 else 0, 2.0 if r < 1 else 1.6, r, "porcelain", 20, "drum")

    def desk(self, x, y, w, d, chair_side="S"):
        G.box(x, x + w, y, y + d, 2.4, 2.55, "timber", "desk")
        G.box(x, x + 0.2, y, y + d, 0, 2.4, "timber", "deskleg")
        G.box(x + w - 0.2, x + w, y, y + d, 0, 2.4, "timber", "deskleg")
        cs = {"S": (x + w / 2 - 1.0, y + d + 0.2, "S"), "N": (x + w / 2 - 1.0, y - 2.2, "N"),
              "E": (x + w + 0.2, y + d / 2 - 1.0, "E"), "W": (x - 2.2, y + d / 2 - 1.0, "W")}[chair_side]
        self.chair(cs[0], cs[1], 2.0, cs[2])

    def plant(self, x, y, r=0.9):
        G.cyl(x, y, 0, 1.6, r * 0.6, "porcelain", 16, "pot")
        G.sphere(x, y, 2.8, r * 1.1, "leaf", 1, 1, 1.3, "plantleaf")


# ------------------------------------------------------------------ site
def tree(x, y, s=1.0, kind="broad"):
    if kind == "palm":
        G.cyl(x, y, -2.5, -2.5 + 34 * s, 0.45 * s, "trunk", 8, "palm")
        for i in range(10):
            a = i * 2 * math.pi / 10
            fr = G.sphere(x + 4.0 * s * math.cos(a), y + 4.0 * s * math.sin(a), -2.5 + 33.5 * s - 1.2 * s, 4.2 * s, "leaf", 1.0, 0.18, 0.08, "frond")
            fr.rotation_euler = (0, math.radians(18), -a)
    elif kind == "bamboo":
        for i in range(14):
            dx, dy = random.uniform(-3, 3) * s, random.uniform(-3, 3) * s
            G.cyl(x + dx, y + dy, -2.5, -2.5 + random.uniform(25, 38) * s, 0.18 * s, "leaf_dark", 6, "culm")
        G.sphere(x, y, -2.5 + 30 * s, 9 * s, "leaf", 0.9, 0.9, 1.4, "bamboo_leaf")
    else:
        h = 28 * s
        G.cyl(x, y, -2.5, -2.5 + h * 0.55, 1.0 * s, "trunk", 10, "trunk")
        for i in range(26):
            a = random.uniform(0, 2 * math.pi)
            rr = random.uniform(0, 9) * s
            G.sphere(x + rr * math.cos(a), y + rr * math.sin(a), -2.5 + h * random.uniform(0.55, 1.0),
                     random.uniform(3.0, 5.0) * s, random.choice(["leaf", "leaf_dark"]), 1, 1, 0.75, "crown")


def shrub(x, y, r=1.6):
    G.sphere(x, y, -2.5 + r * 0.7, r, "leaf_dark", 1, 1, 0.75, "shrub")


def build_site():
    """Site in house coordinates: site x - 141, site y - 165 (see svg_site)."""
    G.box(-600, 700, -700, 600, -2.6, -2.5, "grass", "ground")
    G.cyl(23, -30, -2.52, -2.44, 20, "gravel", 64, "turning_circle")
    G.cyl(23, -30, -2.5, -1.9, 6, "grass", 48, "island")
    tree(23, -30, 0.35, "broad")
    G.box(17, 29, -165, -48, -2.52, -2.44, "gravel", "drive")
    G.box(18.5, 25.5, -12, -9.8, -2.52, -2.44, "gravel", "porch_apron")
    # carport: steel posts and a sheet roof
    for x, y in ((-28, -43), (-10, -43), (-28, -23), (-10, -23)):
        G.box(x - 0.2, x + 0.2, y - 0.2, y + 0.2, -2.5, 6.5, "black", "cp_post")
    G.mesh([(-29, -44, 7.2), (-9, -44, 7.2), (-9, -22, 6.4), (-29, -22, 6.4)], [(0, 1, 2, 3)], "roof", "cp_roof", solid=0.15)
    G.box(-28, -10, -43, -23, -2.52, -2.44, "gravel", "cp_floor")
    # firehouse 12 x 12 ft on four timber posts
    G.box(16, 30, 70, 84, -2.5, -1.5, "stone", "fh_platform")
    for x, y in ((17, 71), (29, 71), (17, 83), (29, 83)):
        G.box(x - 0.25, x + 0.25, y - 0.25, y + 0.25, -1.5, 7.6, "timber", "fh_post")
    G.box(16.7, 29.3, 70.7, 83.3, 7.6, 8.2, "timber", "fh_beam")
    G.hip_roof(15, 31, 69, 85, 8.2, along="x", name="roof_fh")
    G.cyl(23, 77, -1.5, -0.5, 2.5, "stone", 32, "firepit")
    G.sphere(23, 77, 0.0, 1.0, "fire", 1, 1, 1.0, "fire")
    G.box(20, 26, 41.9, 70, -4.02, -3.94, "paving", "fh_path") if False else G.box(20, 26, 37, 70, -2.52, -2.44, "paving", "fh_path")
    # rain tank and planting
    G.cyl(57, 7, -2.5, 2.0, 5, "stone", 32, "rain_tank")
    random.seed(7)
    for x in range(2, 46, 4):
        if not 16 < x < 28:
            shrub(x + random.uniform(-0.5, 0.5), -1.8, random.uniform(1.2, 1.7))
        if not 2 < x < 13:
            shrub(x + random.uniform(-0.5, 0.5), 38.4, random.uniform(1.1, 1.6))
    for y in range(2, 28, 4):
        shrub(-2.0, y, random.uniform(1.1, 1.6))
        shrub(48.0, y, random.uniform(1.1, 1.6))
    for (x, y, s, k) in [(-50, -20, 1.1, "broad"), (-40, 30, 1.2, "broad"), (-30, 65, 1.0, "palm"), (-14, 90, 0.9, "palm"),
                         (85, -25, 1.1, "broad"), (90, 25, 1.0, "palm"), (78, 70, 0.95, "palm"), (70, 105, 1.2, "broad"),
                         (-60, -80, 1.4, "bamboo"), (110, -80, 1.2, "bamboo"), (45, 125, 1.3, "broad"), (-5, 130, 1.2, "broad")]:
        tree(x, y, s, k)
    for i in range(60):
        a = random.uniform(0, 2 * math.pi)
        r = random.uniform(150, 280)
        tree(23 + r * math.cos(a), 14 + r * math.sin(a), random.uniform(1.0, 1.6), random.choice(["broad", "broad", "palm"]))
    for (x, y, sx, sz) in [(-500, -500, 3.5, 0.5), (300, -600, 4, 0.55), (700, -100, 3, 0.45), (-600, 300, 3.5, 0.5), (200, 650, 4.5, 0.5), (-200, -650, 3, 0.4)]:
        G.sphere(x, y, -60, 160, "leaf_dark", sx, sx, sz, "hill")


# ------------------------------------------------------------------ world, lights, camera
def setup_world(sun_elev, sun_az, strength=1.0):
    w = bpy.data.worlds.new("w")
    bpy.context.scene.world = w
    w.use_nodes = True
    nt = w.node_tree
    bg = nt.nodes["Background"]
    sky = nt.nodes.new("ShaderNodeTexSky")
    items = [e.identifier for e in sky.bl_rna.properties["sky_type"].enum_items]
    for pref in ("MULTIPLE_SCATTERING", "NISHITA", "SINGLE_SCATTERING", "HOSEK_WILKIE"):
        if pref in items:
            sky.sky_type = pref
            break
    for attr, val in (("sun_disc", False), ("sun_elevation", math.radians(sun_elev)), ("sun_rotation", math.radians(sun_az)),
                      ("air_density", 1.2), ("dust_density", 2.5), ("altitude", 300.0)):
        try:
            setattr(sky, attr, val)
        except Exception:
            pass
    nt.links.new(sky.outputs["Color"], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = strength
    sun = bpy.data.lights.new("sun", "SUN")
    sun.energy = 5.5
    sun.angle = math.radians(1.2)
    t = max(0, min(1, (sun_elev - 5) / 30))
    sun.color = (1.0, 0.72 + 0.2 * t, 0.48 + 0.4 * t)
    so = bpy.data.objects.new("sun", sun)
    bpy.context.collection.objects.link(so)
    # Blender sun points down -Z; rotate so light comes FROM azimuth (0 = north, 90 = east)
    so.rotation_euler = (math.radians(90 - sun_elev), 0, math.radians(180 - sun_az))


def area_light(x, y, z, size, energy, color=(1, 0.85, 0.65)):
    l = bpy.data.lights.new("a", "AREA")
    l.size = size
    l.energy = energy
    l.color = color
    o = bpy.data.objects.new("a", l)
    o.location = (x, -y, z)
    bpy.context.collection.objects.link(o)


def camera(px, py, pz, tx, ty, tz, lens=28):
    c = bpy.data.cameras.new("cam")
    c.lens = lens
    c.clip_end = 5000
    o = bpy.data.objects.new("cam", c)
    bpy.context.collection.objects.link(o)
    o.location = (px, -py, pz)
    d = Vector((tx, -ty, tz)) - Vector((px, -py, pz))
    o.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = o


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    G.make_materials()
    G.build_house(cut=8.5 if CUT else None)
    G.build_floors_ceilings(with_ceiling=not CUT)
    if not CUT:
        G.build_roofs()
    G.build_verandas()
    build_site()
    furniture.F = F3D
    furniture.furnish(1, 0, 0)
    sc = bpy.context.scene
    views = {
        "front": dict(cam=(62, -52, 4.6, 20, 0, 6.0, 24), sun=(11, 300)),
        "rear": dict(cam=(56, 100, 3.6, 18, 24, 6.0, 22), sun=(14, 238)),
        "aerial": dict(cam=(105, 100, 72, 20, 10, 0, 30), sun=(38, 225)),
        "cutaway": dict(cam=(66, 62, 64, 23, 13, 0, 30), sun=(55, 200)),
        "hall": dict(cam=(15.0, 27.0, 5.0, 29, 4, 4.5, 16), sun=(24, 190)),
        "kitchen": dict(cam=(33.6, 15.0, 5.2, 45, 8.5, 3.6, 16), sun=(24, 160)),
        "bed1": dict(cam=(0.9, 17.9, 5.0, 13, 27, 3.0, 16), sun=(18, 250)),
        "library": dict(cam=(13.2, 9.3, 5.0, 1, 2, 4.4, 16), sun=(30, 250)),
    }
    v = views[VIEW]
    setup_world(v["sun"][0], v["sun"][1], 0.45)
    camera(*v["cam"][:6], lens=v["cam"][6])
    if INTERIOR:
        for (x, y) in ((22, 6), (22, 20), (35, 11.5), (41, 11.5), (35, 11.5), (7, 5), (7, 22), (35, 22)):
            area_light(x, y, 11.6, 4, 260)
        for (x, y, e) in ((38, 12, 1800), (22, 8, 1500), (22, 21, 1500), (7, 5, 900), (35, 22, 900), (7, 22, 900)):
            pl = bpy.data.lights.new("pt", "POINT")
            pl.energy = e
            pl.color = (1, 0.88, 0.72)
            po = bpy.data.objects.new("pt", pl)
            po.location = (x, -y, 9.0)
            bpy.context.collection.objects.link(po)
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = SAMPLES
    sc.cycles.use_adaptive_sampling = True
    sc.cycles.max_bounces = 6
    try:
        sc.cycles.use_denoising = True
        sc.cycles.denoiser = "OPENIMAGEDENOISE"
    except Exception:
        pass
    sc.render.resolution_x, sc.render.resolution_y = 1600, 900
    sc.render.resolution_percentage = 100
    try:
        sc.view_settings.view_transform = "AgX"
        sc.view_settings.look = "AgX - Punchy"
    except Exception:
        pass
    sc.view_settings.exposure = {"library": 1.0, "hall": 0.9, "kitchen": 1.2}.get(VIEW, 0.6) if INTERIOR else 0.0
    sc.render.filepath = OUT
    bpy.ops.render.render(write_still=True)
    print("WROTE", OUT)


main()

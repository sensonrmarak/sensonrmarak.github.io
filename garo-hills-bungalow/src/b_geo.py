"""Blender geometry: materials, walls with real openings, roofs, verandas.
Units are feet. Plan x -> Blender X (east), plan y (south) -> Blender -Y, z up, FFL = 0."""
import math
import bpy
from data import WALLS
from openings import MAIN, SCHEDULE

K25 = math.tan(math.radians(25))
MATS = {}


# ------------------------------------------------------------------ materials
def _bsdf(name, color, rough=0.6, metal=0.0, spec=0.4):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    MATS[name] = m
    return m, b


def _noise_color(m, b, c1, c2, scale=8.0, detail=6.0, voronoi=False, bump=0.0):
    nt = m.node_tree
    tc = nt.nodes.new("ShaderNodeTexCoord")
    if voronoi:
        tx = nt.nodes.new("ShaderNodeTexVoronoi")
        tx.inputs["Scale"].default_value = scale
        out = tx.outputs["Distance"]
    else:
        tx = nt.nodes.new("ShaderNodeTexNoise")
        tx.inputs["Scale"].default_value = scale
        tx.inputs["Detail"].default_value = detail
        out = tx.outputs["Fac"]
    nt.links.new(tc.outputs["Object"], tx.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (*c1, 1)
    ramp.color_ramp.elements[1].color = (*c2, 1)
    nt.links.new(out, ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    if bump:
        bp = nt.nodes.new("ShaderNodeBump")
        bp.inputs["Strength"].default_value = bump
        nt.links.new(out, bp.inputs["Height"])
        nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])


def make_materials():
    m, b = _bsdf("render", (0.80, 0.70, 0.52), 0.9)
    _noise_color(m, b, (0.80, 0.66, 0.44), (0.88, 0.75, 0.52), 2.5, bump=0.05)
    m, b = _bsdf("stone", (0.45, 0.42, 0.37), 0.9)
    _noise_color(m, b, (0.16, 0.15, 0.13), (0.50, 0.45, 0.37), 2.4, voronoi=True, bump=1.2)
    _bsdf("roof", (0.05, 0.052, 0.055), 0.62, 0.15)
    _bsdf("soffit", (0.18, 0.11, 0.07), 0.6)
    _bsdf("white", (0.82, 0.81, 0.77), 0.5)
    _bsdf("black", (0.02, 0.02, 0.02), 0.35, 0.3)
    m, b = _bsdf("glass", (0.8, 0.85, 0.9), 0.02)
    b.inputs["Transmission Weight"].default_value = 1.0
    b.inputs["IOR"].default_value = 1.45
    m, b = _bsdf("hardwood_door", (0.16, 0.08, 0.04), 0.45)
    m, b = _bsdf("grass", (0.14, 0.28, 0.06), 0.9)
    _noise_color(m, b, (0.035, 0.09, 0.012), (0.09, 0.19, 0.03), 0.35, bump=0.3)
    m, b = _bsdf("gravel", (0.55, 0.52, 0.47), 0.95)
    _noise_color(m, b, (0.40, 0.38, 0.35), (0.72, 0.69, 0.63), 9, bump=0.4)
    m, b = _bsdf("paving", (0.62, 0.58, 0.52), 0.8)
    _noise_color(m, b, (0.50, 0.47, 0.42), (0.70, 0.66, 0.58), 0.9, voronoi=True, bump=0.2)
    m, b = _bsdf("terrazzo", (0.84, 0.80, 0.72), 0.25)
    _noise_color(m, b, (0.78, 0.74, 0.66), (0.92, 0.89, 0.83), 30, bump=0.05)
    m, b = _bsdf("wood_floor", (0.35, 0.20, 0.10), 0.4)
    _noise_color(m, b, (0.25, 0.14, 0.07), (0.45, 0.27, 0.13), 3, detail=12)
    _bsdf("wall_int", (0.88, 0.84, 0.74), 0.9)
    _bsdf("ceiling", (0.90, 0.88, 0.82), 0.95)
    m, b = _bsdf("timber", (0.55, 0.36, 0.18), 0.5)
    _noise_color(m, b, (0.58, 0.40, 0.22), (0.74, 0.55, 0.33), 4, detail=10)
    _bsdf("fabric_linen", (0.78, 0.74, 0.66), 0.95)
    _bsdf("fabric_red", (0.33, 0.07, 0.09), 0.95)
    _bsdf("fabric_grey", (0.38, 0.38, 0.37), 0.95)
    _bsdf("fabric_green", (0.30, 0.38, 0.30), 0.95)
    _bsdf("bedding", (0.93, 0.92, 0.89), 0.95)
    _bsdf("granite", (0.10, 0.10, 0.10), 0.25)
    _bsdf("cabinet", (0.42, 0.47, 0.40), 0.5)
    _bsdf("porcelain", (0.95, 0.95, 0.94), 0.15)
    _bsdf("rug", (0.45, 0.20, 0.14), 1.0)
    m, b = _bsdf("leaf", (0.10, 0.25, 0.06), 0.8)
    _noise_color(m, b, (0.03, 0.09, 0.015), (0.12, 0.24, 0.04), 1.5, bump=1.0)
    m, b = _bsdf("leaf_dark", (0.05, 0.15, 0.04), 0.8)
    _noise_color(m, b, (0.015, 0.05, 0.01), (0.06, 0.13, 0.03), 1.5, bump=1.0)
    _bsdf("trunk", (0.20, 0.14, 0.10), 0.9)
    _bsdf("brass", (0.75, 0.55, 0.25), 0.3, 1.0)
    _bsdf("water", (0.2, 0.3, 0.35), 0.05)
    _bsdf("piano", (0.01, 0.01, 0.01), 0.1)
    m, b = _bsdf("lamp", (1, 0.85, 0.6), 0.5)
    b.inputs["Emission Color"].default_value = (1.0, 0.75, 0.45, 1)
    b.inputs["Emission Strength"].default_value = 12.0
    m, b = _bsdf("fire", (1, 0.5, 0.1), 0.5)
    b.inputs["Emission Color"].default_value = (1.0, 0.45, 0.1, 1)
    b.inputs["Emission Strength"].default_value = 60.0


# ------------------------------------------------------------------ primitives
def box(x0, x1, y0, y1, z0, z1, mat, name="box"):
    """Axis box in PLAN coordinates (y south)."""
    if x1 < x0:
        x0, x1 = x1, x0
    if y1 < y0:
        y0, y1 = y1, y0
    if z1 - z0 <= 1e-4 or x1 - x0 <= 1e-4 or y1 - y0 <= 1e-4:
        return None
    me = bpy.data.meshes.new(name)
    X0, X1, Y0, Y1 = x0, x1, -y1, -y0
    v = [(X0, Y0, z0), (X1, Y0, z0), (X1, Y1, z0), (X0, Y1, z0),
         (X0, Y0, z1), (X1, Y0, z1), (X1, Y1, z1), (X0, Y1, z1)]
    f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    me.from_pydata(v, [], f)
    me.update()
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(MATS[mat])
    bpy.context.collection.objects.link(ob)
    return ob


def mesh(verts_plan, faces, mat, name="mesh", solid=0.0):
    me = bpy.data.meshes.new(name)
    me.from_pydata([(x, -y, z) for x, y, z in verts_plan], [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(MATS[mat])
    bpy.context.collection.objects.link(ob)
    if solid:
        mo = ob.modifiers.new("s", "SOLIDIFY")
        mo.thickness = solid
    return ob


_CACHE = {}


def _proto(kind, verts):
    key = (kind, verts)
    if key not in _CACHE:
        import bmesh
        me = bpy.data.meshes.new(f"{kind}{verts}")
        bm = bmesh.new()
        if kind == "cyl":
            bmesh.ops.create_cone(bm, cap_ends=True, segments=verts, radius1=1, radius2=1, depth=1)
        elif kind == "cone":
            bmesh.ops.create_cone(bm, cap_ends=True, segments=verts, radius1=1, radius2=0, depth=1)
        else:
            bmesh.ops.create_icosphere(bm, subdivisions=verts, radius=1)
        bm.to_mesh(me)
        bm.free()
        for p in me.polygons:
            p.use_smooth = True
        _CACHE[key] = me
    return _CACHE[key]


def _inst(kind, verts, loc, scale, mat, name):
    me = _proto(kind, verts)
    ob = bpy.data.objects.new(name, me)
    ob.location = loc
    ob.scale = scale
    ob.material_slots and None
    bpy.context.collection.objects.link(ob)
    ob.active_material_index = 0
    if not me.materials:
        me.materials.append(None)
    slot = ob.material_slots[0]
    slot.link = "OBJECT"
    slot.material = MATS[mat]
    return ob


def cyl(x, y, z0, z1, r, mat, verts=24, name="cyl"):
    return _inst("cyl", verts, (x, -y, (z0 + z1) / 2), (r, r, z1 - z0), mat, name)


def sphere(x, y, z, r, mat, sx=1, sy=1, sz=1, name="sph"):
    return _inst("sph", 2, (x, -y, z), (r * sx, r * sy, r * sz), mat, name)


def cone(x, y, z0, h, r, mat, name="cone"):
    return _inst("cone", 16, (x, -y, z0 + h / 2), (r, r, h), mat, name)


def hip_roof(x0, x1, y0, y1, ze, mat="roof", along="x", name="roof"):
    """Hipped roof over plan rectangle, eaves at ze, 25 degree pitch."""
    if along == "x":
        h = (y1 - y0) / 2
        zr = ze + h * K25
        ym = (y0 + y1) / 2
        v = [(x0, y0, ze), (x1, y0, ze), (x1, y1, ze), (x0, y1, ze), (x0 + h, ym, zr), (x1 - h, ym, zr)]
        f = [(0, 1, 5, 4), (2, 3, 4, 5), (1, 2, 5), (3, 0, 4)]
    else:
        h = (x1 - x0) / 2
        zr = ze + h * K25
        xm = (x0 + x1) / 2
        v = [(x0, y0, ze), (x1, y0, ze), (x1, y1, ze), (x0, y1, ze), (xm, y0 + h, zr), (xm, y1 - h, zr)]
        f = [(3, 0, 4, 5), (1, 2, 5, 4), (0, 1, 4), (2, 3, 5)]
    ob = mesh(v, f, mat, name, solid=0.35)
    # dark timber soffit under the eaves
    mesh([(x0, y0, ze - 0.05), (x1, y0, ze - 0.05), (x1, y1, ze - 0.05), (x0, y1, ze - 0.05)], [(0, 1, 2, 3)], "soffit", name + "_soffit")
    return ob


# ------------------------------------------------------------------ walls (all in feet)
OUTER = [((0, 0), (0, 28)), ((0, 28), (46, 28)), ((46, 28), (46, 0)), ((46, 0), (0, 0))]
EAVE = 13.0 - 3 * K25


def _ops_on(ori, c, a0, a1):
    out = []
    for mark, o, cc, a, side in MAIN:
        if o == ori and abs(cc - c) < 1e-6 and a0 - 0.01 <= a <= a1 + 0.01:
            out.append((mark, a))
    return sorted(out, key=lambda t: t[1])


def wall_pieces(x0, y0, x1, y1, t, top):
    ori = "h" if y0 == y1 else "v"
    c = y0 if ori == "h" else x0
    a0, a1 = (min(x0, x1), max(x0, x1)) if ori == "h" else (min(y0, y1), max(y0, y1))
    ops = _ops_on(ori, c, a0, a1)
    e0, e1 = a0 - t / 2 + 0.03, a1 + t / 2 - 0.03
    mat = "render" if t >= 0.75 else "wall_int"

    def seg(b0, b1, z0, z1):
        if ori == "h":
            box(b0, b1, c - t / 2, c + t / 2, z0, z1, mat, "wall")
        else:
            box(c - t / 2, c + t / 2, b0, b1, z0, z1, mat, "wall")

    cur = e0
    specs = []
    for mark, a in ops:
        w, h, sill = SCHEDULE[mark][2], SCHEDULE[mark][3], SCHEDULE[mark][4]
        o0, o1 = a - w / 2, a + w / 2
        seg(cur, o0, 0, top)
        if sill > 0:
            seg(o0, o1, 0, sill)
        seg(o0, o1, sill + h, top)
        specs.append((mark, ori, c, a, w, sill, sill + h, t))
        cur = o1
    seg(cur, e1, 0, top)
    return specs


def window(mark, ori, c, a, w, z0, z1, t):
    if mark in ("D2", "D3", "OP"):
        return
    fw = 0.17
    X0, X1, Yc = a - w / 2, a + w / 2, c
    if ori == "h":
        B = lambda u0, u1, z0_, z1_, d=0.18, mat="black": box(u0, u1, Yc - d / 2, Yc + d / 2, z0_, z1_, mat, "frame")
    else:
        B = lambda u0, u1, z0_, z1_, d=0.18, mat="black": box(Yc - d / 2, Yc + d / 2, u0, u1, z0_, z1_, mat, "frame")
    if mark == "D1":
        B(X0, X1, z0, z1, 0.15, "hardwood_door")
        B(X0 + 0.5, X1 - 0.5, z1 - 3.2, z1 - 0.8, 0.17, "glass")
        B(X1 - 0.5, X1 - 0.4, 3.2, 4.6, 0.3, "brass")
        return
    B(X0, X1, z0, z0 + fw)
    B(X0, X1, z1 - fw, z1)
    B(X0, X0 + fw, z0, z1)
    B(X1 - fw, X1, z0, z1)
    B(X0 + fw, X1 - fw, z0 + fw, z1 - fw, 0.04, "glass")
    mid = (X0 + X1) / 2
    B(mid - 0.05, mid + 0.05, z0, z1, 0.12)
    if z1 - z0 > 4:
        for f in (0.36, 0.68):
            zz = z0 + (z1 - z0) * f
            B(X0, X1, zz - 0.04, zz + 0.04, 0.1)
    if t >= 0.7:
        if ori == "h":
            box(X0 - 0.3, X1 + 0.3, c - t / 2 - 0.15, c + t / 2 + 0.15, 8.05, 8.3, "white", "drip")
        else:
            box(c - t / 2 - 0.15, c + t / 2 + 0.15, X0 - 0.3, X1 + 0.3, 8.05, 8.3, "white", "drip")


def build_house(cut=None):
    top = 13.0 if cut is None else cut
    for x0, y0, x1, y1, t, _ in WALLS:
        for sp in wall_pieces(x0, y0, x1, y1, t, top):
            window(*sp)
    box(-0.4, 46.4, -0.4, 28.4, -2.5, 0, "stone", "plinth")
    for (ax, ay), (bx, by) in OUTER:
        if ay == by:
            out = 1 if ay == 28 else -1
            yy = ay + out * (0.375 + 0.06)
            box(min(ax, bx) - 0.5, max(ax, bx) + 0.5, yy - 0.06, yy + 0.06, -2.5, 1.5, "stone", "clad")
        else:
            out = -1 if ax == 0 else 1
            xx = ax + out * (0.375 + 0.06)
            box(xx - 0.06, xx + 0.06, min(ay, by) - 0.5, max(ay, by) + 0.5, -2.5, 1.5, "stone", "clad")


def build_floors_ceilings(with_ceiling=True):
    from data import room_table
    wood = {"BED1", "BED2", "LIB", "DRS1", "WRD2"}
    for r in room_table():
        mat = "wood_floor" if r["key"] in wood else "terrazzo"
        box(r["x0"], r["x1"], r["y0"], r["y1"], -0.05, 0.02, mat, "floor_" + r["key"])
        if with_ceiling:
            ch = r["ceil"]
            box(r["x0"], r["x1"], r["y0"], r["y1"], ch, ch + 0.1, "timber" if r["key"] == "LIV" else "ceiling", "ceil_" + r["key"])
            if r["key"] == "LIV":
                for y in range(3, 28, 5):
                    box(14, 30, y - 0.25, y + 0.25, ch - 0.6, ch, "timber", "beam")


def build_roofs():
    hip_roof(-3, 49, -3, 29.5, EAVE, along="x", name="roof_main")
    hip_roof(16.5, 27.5, -7, -0.5, 10.0, along="x", name="roof_porch")
    mesh([(-3, 29.0, 12.9), (49.375, 29.0, 12.9), (49.375, 38.0, 11.4), (-3, 38.0, 11.4)], [(0, 1, 2, 3)], "roof", "ver_s", solid=0.25)


def build_verandas():
    box(-0.4, 46.4, 28.4, 36.9, -2.5, -0.05, "stone", "ver_s_base")
    box(-0.4, 46.4, 28.4, 36.9, -0.08, 0, "paving", "ver_s_floor")
    for i in range(5):
        box(3, 12, 36.9 + i, 37.9 + i, -4.0, -(i + 1) * 0.5 + 0.0 - 0.0, "stone", "step")
    for x in (0, 11.5, 23, 34.5, 46):
        cyl(x, 36.375, 0, 11.3, 0.45, "white", name="col_s")
        box(x - 0.6, x + 0.6, 35.8, 36.95, 0, 0.5, "white", "col_base")
    box(-0.4, 46.4, 35.9, 36.85, 11.3, 11.9, "white", "beam_s")
    box(17, 27, -6.4, -0.4, -2.5, 0, "stone", "porch_base")
    box(17, 27, -6.4, -0.4, -0.08, 0, "paving", "porch_floor")
    for i in range(4):
        box(18.5, 25.5, -6.4 - (i + 1), -6.4 - i, -2.5, -(i + 1) * 0.625, "stone", "pstep")
    for x in (17, 27):
        cyl(x, -6.4, 0, 9.6, 0.4, "white", name="col_p")
    box(16.6, 27.4, -6.8, -6.0, 9.6, 10.0, "white", "beam_p")
    box(21.6, 22.4, -4.2, -3.4, 8.2, 9.4, "lamp", "lantern")

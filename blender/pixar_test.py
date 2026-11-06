# Pixar-style test scene: run with  blender -b -P pixar_test.py -- [still|anim]
import bpy, sys, math
mode = sys.argv[-1] if sys.argv[-1] in ("still", "anim") else "still"
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

def mat(name, color, rough=0.5, sss=0.0, emit=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    if sss:
        b.inputs["Subsurface Weight"].default_value = sss
        b.inputs["Subsurface Radius"].default_value = (0.3, 0.15, 0.1)
        b.inputs["Subsurface Scale"].default_value = 0.1
    if emit:
        b.inputs["Emission Color"].default_value = (*color, 1); b.inputs["Emission Strength"].default_value = emit
    return m

def smooth(o, lvl=2):
    o.modifiers.new("s", "SUBSURF").levels = lvl
    o.modifiers["s"].render_levels = lvl
    for p in o.data.polygons: p.use_smooth = True
    return o

def sphere(loc, scale, m, name="o"):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, location=loc)
    o = bpy.context.object; o.name = name; o.scale = scale; o.data.materials.append(m)
    for p in o.data.polygons: p.use_smooth = True
    return o

fur = mat("fur", (0.85, 0.45, 0.2), 0.6, sss=0.3)
belly = mat("belly", (0.98, 0.88, 0.72), 0.6, sss=0.3)
white = mat("eyewhite", (0.97, 0.97, 0.97), 0.15)
iris = mat("iris", (0.25, 0.5, 0.15), 0.2)
black = mat("pupil", (0.01, 0.01, 0.01), 0.05)
nose = mat("nose", (0.15, 0.06, 0.05), 0.2)
grass = mat("grass", (0.25, 0.55, 0.18), 0.8)
wood = mat("wood", (0.4, 0.22, 0.1), 0.7)
cap = mat("cap", (0.8, 0.12, 0.08), 0.35, sss=0.2)
stem = mat("stem", (0.95, 0.9, 0.8), 0.5, sss=0.3)

# Character: a little fox-like critter "Oaky"
root = bpy.data.objects.new("Oaky", None); sc.collection.objects.link(root)
parts = [
    sphere((0, 0, 0.75), (0.55, 0.5, 0.6), fur, "body"),
    sphere((0, -0.33, 0.65), (0.35, 0.2, 0.4), belly, "belly"),
    sphere((0, 0, 1.55), (0.62, 0.55, 0.52), fur, "head"),
    sphere((0, -0.38, 1.4), (0.3, 0.25, 0.2), belly, "muzzle"),
    sphere((0, -0.62, 1.47), (0.08, 0.06, 0.06), nose, "nose"),
]
for x in (-0.22, 0.22):
    parts += [sphere((x, -0.4, 1.7), (0.17, 0.12, 0.2), white, "eye"),
              sphere((x * 0.95, -0.51, 1.68), (0.1, 0.04, 0.12), iris, "iris"),
              sphere((x * 0.95, -0.545, 1.68), (0.055, 0.02, 0.07), black, "pupil"),
              sphere((x * 0.95 + 0.03, -0.56, 1.73), (0.02, 0.01, 0.025), white, "glint")]
    bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=0.2, depth=0.5, location=(x * 1.6, 0.05, 2.1))
    e = bpy.context.object; e.rotation_euler = (0, x * 1.2, 0); e.data.materials.append(fur); smooth(e, 1); parts.append(e)
    parts.append(sphere((x * 1.4, -0.15, 0.2), (0.17, 0.25, 0.12), fur, "foot"))
    parts.append(sphere((x * 2.4, -0.1, 0.85), (0.12, 0.12, 0.28), fur, "arm"))
tail = sphere((0, 0.6, 0.6), (0.25, 0.5, 0.25), fur, "tail"); tail.rotation_euler = (0.8, 0, 0); parts.append(tail)
for p in parts: p.parent = root
root.location = (0, 0, 0); root.rotation_euler = (0, 0, math.radians(-15))

# Ground + mushrooms + trees
bpy.ops.mesh.primitive_plane_add(size=60); g = bpy.context.object; g.data.materials.append(grass)
def mushroom(x, y, s):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.12 * s, depth=0.5 * s, location=(x, y, 0.25 * s)); bpy.context.object.data.materials.append(stem); smooth(bpy.context.object, 1)
    c = sphere((x, y, 0.5 * s), (0.35 * s, 0.35 * s, 0.22 * s), cap)
    for i in range(5):
        a = i * 1.3; sphere((x + math.cos(a) * 0.2 * s, y + math.sin(a) * 0.2 * s, 0.62 * s), (0.05 * s,) * 3, white)
for x, y, s in [(-1.6, -0.3, 1.2), (-2.1, 0.6, 0.8), (1.7, 0.4, 1.4), (2.3, -0.6, 0.7)]: mushroom(x, y, s)
for x, y in [(-4, 4), (3.5, 5), (0.5, 7), (-6, 8), (6, 3)]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=3, location=(x, y, 1.5)); bpy.context.object.data.materials.append(wood)
    sphere((x, y, 3.6), (1.6, 1.6, 1.4), mat("leaf", (0.15, 0.4, 0.12), 0.8, sss=0.2))

# Lighting: warm key, cool fill, rim, sky
world = bpy.data.worlds.new("w"); sc.world = world; world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.75, 1.0, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.6
def light(t, loc, energy, color, size=2):
    d = bpy.data.lights.new("l", t); d.energy = energy; d.color = color
    if t == "AREA": d.size = size
    o = bpy.data.objects.new("l", d); o.location = loc; sc.collection.objects.link(o)
    tc = o.constraints.new("TRACK_TO"); tc.target = root; return o
light("SUN", (5, -5, 8), 3.5, (1.0, 0.9, 0.75)).data.angle = 0.15
light("AREA", (-4, -3, 2), 300, (0.6, 0.75, 1.0), 4)
light("AREA", (0, 4, 3), 500, (1.0, 0.85, 0.6), 2)

# Camera with shallow depth of field
cd = bpy.data.cameras.new("cam"); cd.lens = 55; cd.dof.use_dof = True; cd.dof.aperture_fstop = 2.2
cam = bpy.data.objects.new("cam", cd); sc.collection.objects.link(cam); sc.camera = cam
cam.location = (1.2, -6.5, 1.9); cam.rotation_euler = (math.radians(86), 0, math.radians(10))
cd.dof.focus_object = parts[2]

# Animation: bounce, head tilt, blink-ish ear wiggle, slow camera push
sc.frame_start, sc.frame_end, sc.render.fps = 1, 72, 24
for f, z, rz in [(1, 0, -15), (18, 0.25, -5), (36, 0, 10), (54, 0.25, -5), (72, 0, -15)]:
    root.location.z = z; root.rotation_euler.z = math.radians(rz)
    root.keyframe_insert("location", frame=f); root.keyframe_insert("rotation_euler", frame=f)
cam.keyframe_insert("location", frame=1); cam.location = (0.9, -5.6, 1.85); cam.keyframe_insert("location", frame=72)

r = sc.render; r.engine = "CYCLES"; sc.cycles.device = "CPU"
sc.cycles.samples = 64 if mode == "anim" else 256; sc.cycles.use_denoising = False  # this Blender build lacks OpenImageDenoise; set True with the official build
r.resolution_x, r.resolution_y = (960, 540) if mode == "anim" else (1280, 720)
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Medium High Contrast"
import os; out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
if mode == "still":
    sc.frame_set(18); r.filepath = out + "/pixar_still.png"; bpy.ops.render.render(write_still=True)
else:
    r.image_settings.file_format = "FFMPEG"; r.ffmpeg.format = "MPEG4"; r.ffmpeg.codec = "H264"
    r.filepath = out + "/pixar_clip.mp4"; bpy.ops.render.render(animation=True)

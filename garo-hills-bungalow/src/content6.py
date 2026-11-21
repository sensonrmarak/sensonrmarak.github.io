"""Views: photo-style render and 3D model renders, embedded in the PDF."""
import base64, io, os
from PIL import Image
from content1 import band

RD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "renders")

VIEWS = [
    ("render_front.png", "Approach from the north-west: car porch, front door and the long north face with its tall windows."),
    ("render_rear.png", "Garden side at a winter sunset: the 9 ft south veranda, with the firehouse in the foreground."),
    ("render_aerial.png", "Aerial view: house, forecourt ring, garage block, firehouse and planting."),
    ("render_cutaway.png", "Cut-away at 8 ft 6 in, furnished: library and study at top left, open hall and dining in the middle, the walled kitchen, and the guest suite and wet corner on the right."),
    ("render_hall.png", "Sitting hall under the timber-lined vault, looking east to the dining area and the kitchen wall."),
    ("render_kitchen.png", "Kitchen with island and breakfast table, behind its own wall, opening onto the veranda."),
    ("render_bed1.png", "Bedroom 1 (resident): bed against the party wall, armchairs at the south French door."),
    ("render_library.png", "Library looking through the glazed doors into the study."),
]


def _b64(path, width):
    im = Image.open(path).convert("RGB")
    im.thumbnail((width, width))
    b = io.BytesIO()
    im.save(b, "JPEG", quality=80)
    return base64.b64encode(b.getvalue()).decode()


def views():
    out = [band("Views of the house", "b8")]
    ai = os.path.join(RD, "ai_front_exterior.png")
    if os.path.exists(ai):
        out.append(f'<figure class="hero"><img src="data:image/jpeg;base64,{_b64(ai, 1500)}"/>'
                   '<figcaption>Photo-style impression of the approach (AI image generated from this design brief). '
                   'It shows the intended mood and materials. Exact positions and sizes are in the 3D model views and drawings that follow.</figcaption></figure>')
    cells = []
    for f, cap in VIEWS:
        p = os.path.join(RD, f)
        if os.path.exists(p):
            cells.append(f'<figure><img src="data:image/jpeg;base64,{_b64(p, 1100)}"/><figcaption>{cap}</figcaption></figure>')
    if cells:
        out.append('<p class="note">The views below are rendered from a 3D model built from the same centre-line data as the plan, so every wall, window, door and column sits exactly where the drawings put it. Furniture is shown in simplified form.</p>')
        out.append('<div class="gallery">' + "".join(cells) + "</div>")
    return "\n".join(out)

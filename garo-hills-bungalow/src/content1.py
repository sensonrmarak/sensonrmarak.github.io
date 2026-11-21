"""Part 1: cover, design statement, climate response, look references."""
import base64, io
from PIL import Image
from data import areas, rain, SUN, fi

UP = "/root/.claude/uploads/fda5ed2a-b36c-5948-8deb-d3e25e819390/"
REFS = [("7915857b-image.jpg", "Reference 1: stone cottage with black trim"),
        ("8f65904c-image.jpg", "Reference 2: arched stone porch, deep landscape"),
        ("792c5725-image.jpg", "Reference 3: compact two-bedroom plan")]


def img64(name, width=520):
    try:
        im = Image.open(UP + name).convert("RGB")
    except OSError:
        return None
    im.thumbnail((width, width * 2))
    b = io.BytesIO()
    im.save(b, "JPEG", quality=72)
    return base64.b64encode(b.getvalue()).decode()


def hl(t):
    return f'<span class="hl">{t}</span>'


def band(title, cls="b1"):
    return f'<h2 class="{cls}">{title}</h2>'


def cover():
    a = areas()
    return f"""
<section class="cover">
  <div class="kicker">Design report for one resident</div>
  <h1>Courtyard Bungalow</h1>
  <div class="sub">Garo Hills, Meghalaya &nbsp;|&nbsp; one hectare (1,07,639 sq ft) &nbsp;|&nbsp; Seismic Zone V</div>
  <table class="keyfacts">
    <tr><td>Main house carpet area</td><td>{hl(f"{a['carpet_house']:,} sq ft")}</td></tr>
    <tr><td>Main house built-up area</td><td>{hl(f"{a['built_house']:,} sq ft")}</td></tr>
    <tr><td>Rooms</td><td>2 master bedrooms with dressing and bath; sitting hall, dining, kitchen with utility and store; library and study opening into each other; shared toilet and shared bathroom in the north-east corner</td></tr>
    <tr><td>Ceilings</td><td>{hl("12 ft 3 in")} in every habitable room (library 12 ft 0 in, hall vault to 16 ft 0 in)</td></tr>
    <tr><td>Plinth</td><td>{hl("2 ft 6 in")} above finished ground at the porch</td></tr>
    <tr><td>Structure</td><td>RCC frame, 12 in x 18 in columns, plinth, lintel and roof bands, brick infill</td></tr>
    <tr><td>Firehouse</td><td>20 ft 0 in x 20 ft 0 in open pavilion with 4 ft 0 in stone fire pit</td></tr>
    <tr><td>Garage block</td><td>2 cars (20 ft 3 in x 22 ft 6 in clear), two-wheeler bay, tool store, generator and pump room</td></tr>
  </table>
  <p class="note">All lengths are in feet and inches, all areas in sq ft, all money in lakh and crore. Room sizes are clear sizes, wall face to wall face, rounded to the nearest 3 in. Set-out dimensions are wall centre lines and are exact.</p>
</section>"""


def statement():
    return f"""
{band("1. The idea of the house", "b1")}
<p>Think of this house as one long, calm room with two quiet ends. In the middle, the sitting hall and the dining area are one open space, defined by a column, a change of ceiling and the furniture, so the room stays generous when you are alone and stretches when friends arrive. The kitchen sits behind a proper wall, with its own door to the dining area, so cooking smells, noise and the working mess stay out of the living rooms. At the west end is your own bedroom suite. At the east end, as far away as the plan allows, is the guest suite. A guest and you never share a passage at night, and the guest has a shared bathroom and washroom right beside their door for friends who stay late.</p>
<p>The house faces south. In the Garo Hills that one decision does most of the climate work. The long south face takes the low winter sun into the sitting hall and both bedrooms, while a deep veranda with a carefully set roof edge blocks the high summer and monsoon sun completely. The service rooms, bathrooms, utility and store, are lined up along the north edge on one continuous plumbing line, where they shield the living rooms from the cold north side and keep every pipe on an outside wall you can reach.</p>
<p>The library and the study sit together at the west end, next to the front door. The library takes the steady north light it needs, then opens through a pair of glazed doors into the study, which has north and west windows of its own. The shared toilet and bathroom sit together in the north-east corner of the house, each with outside walls and windows. A covered walk links the garage to the front door, so you can come and go in a monsoon downpour without an umbrella.</p>
<p>Behind the house, across a lawn of about 36 ft, the firehouse closes the garden. It is a smaller cousin of the house, with the same white columns, charcoal roof and stone base, built around a real fire. Beyond it the land steps down through an orchard and a kitchen garden into a grove of native trees that is cheap to keep and right for the hills. The building takes up under 7 per cent of the hectare. The rest is garden, orchard and grove.</p>
"""


def climate():
    r = rain()
    return f"""
{band("2. How the climate and the ground have been answered", "b2")}
<table class="t">
<tr><th style="width:24%">Condition</th><th>How it is handled</th></tr>
<tr><td><b>Very heavy monsoon</b> (about 130 in a year, design storm {hl("5 in an hour")})</td>
<td>Main roof pitched at {hl("25°")} so water clears fast. Overhang {hl("3 ft 0 in")} on north, east and west; 9 ft 0 in veranda on the south. Roofs total about 6,000 sq ft, which in the design storm sheds {r['q_lps']:.1f} litres a second ({r['q_cfs']:.2f} cu ft a second). That needs 12 downpipes at 500 sq ft each; {hl("14 downpipes of 4 in diameter")} are provided, fed by {hl("7 in x 5 in box gutters")} laid 1 in 200, outlets no more than 26 ft apart. All downpipes discharge to a 6 in underground storm line, then silt trap, then the rainwater sump.</td></tr>
<tr><td><b>Ground drainage</b></td>
<td>A 3 ft 0 in wide stone apron round the house falls 1 in 30 away from the plinth into an open stone-lined drain {hl("12 in wide x 12 in deep")} under the eave drip line. Uphill of the house a cut-off drain 15 in x 18 in intercepts hill water before it reaches the platform. See the site plan for where the water goes in a cloudburst.</td></tr>
<tr><td><b>Seismic Zone V</b></td>
<td>RCC framed structure, M25 concrete, Fe 500D bars, ductile detailing to IS 13920. Columns {hl("12 in x 18 in")} on the grid shown on the plan (no span over 18 ft 0 in on the walls). Isolated footings 5 ft 0 in below natural ground on firm strata, tied by a {hl("plinth beam 12 in x 18 in")}. A continuous {hl("lintel band at +8 ft 0 in")} (all doors and windows share this head height) and a {hl("roof band at +15 ft 0 in")}. 9 in walls are infill only and carry no load. 4½ in partitions have 2 bars of 6 mm in every fourth course and are tied to columns with dowels. The roof is light standing-seam steel on galvanised steel trusses, which keeps mass off the top of the building.</td></tr>
<tr><td><b>Humidity and fungus</b></td>
<td>Plinth {hl("2 ft 6 in")} with a damp-proof course of 1½ in plum concrete with waterproofing compound at plinth beam top. Every habitable room has windows on two faces or a window plus a high-level vent. Top-hung clerestory vents (V1) above every tall window let warm wet air out at ceiling level while the lower sashes take air in. Deep verandas keep rain off the walls. Lime render breathes; cement paint is not used on the outside.</td></tr>
<tr><td><b>Cold winter mornings</b></td>
<td>Long axis east to west, living rooms on the south. At latitude 25.5° N the noon sun is {SUN['winter']:.0f}° high in December, {SUN['equinox']:.0f}° at the equinoxes and {SUN['summer']:.0f}° in June. The veranda roof eave is set at {hl("+12 ft 5 in")} and {hl("10 ft 0 in")} out from the wall, so winter sun reaches the glass and floor (see section) while equinox and summer sun never touch the glass. Bedroom 1 also has two west windows for afternoon warmth; bedroom 2 has east windows for the morning.</td></tr>
</table>
"""


def references():
    cells = []
    for f, cap in REFS:
        b = img64(f)
        if b:
            cells.append(f'<figure><img src="data:image/jpeg;base64,{b}"/><figcaption>{cap}</figcaption></figure>')
    return f"""
{band("3. What has been taken from your reference images", "b3")}
<div class="refs">{''.join(cells)}</div>
<ul>
<li><b>Reference 1</b>: the dark charcoal roof, black window frames, white columns at the entrance and the hanging lantern under the porch. The full stone walls are kept only as a stone base up to sill level, as your brief asks, with cream lime render above.</li>
<li><b>Reference 2</b>: the deep entrance with paired columns and planters either side of the door, and the idea of a house that sits in a large landscape rather than a lawn.</li>
<li><b>Reference 3</b>: the honest single-storey plan with bedrooms at the ends and living space in the middle. This design keeps that idea but makes it larger, moves the bathroom out of the middle to the north edge, and drops the tub in favour of walk-in showers.</li>
<li><b>Your cottage plan reference</b> (a small two-bed plan with a front stoop): the furnished floor plan is now drawn the same way. Rooms are warm yellow, verandas blue and walls solid black. Every room shows its furniture and fixtures, and each name is underlined with its size given as 17'3" X 17'6". Like that plan, the kitchen is open to the living space, marked only by a dashed line, and corridors are kept to a minimum. Its bathtub is not carried over, because your brief rules tubs out.</li>
</ul>
"""

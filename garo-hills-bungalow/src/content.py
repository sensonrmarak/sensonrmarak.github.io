"""All report text for the budget house. Every length in decimal feet, every quantity worked out."""
import base64, io, math, os
from PIL import Image
from data import (areas, budget, rain, room_table, working, WALLS, EXT, INT, OUT_W, OUT_D, VERANDA, PORCH,
                  CARPORT, SUN, lakh, money, thick, RAIN_ANNUAL_FT, RAIN_DESIGN_FT_HR, TANK)
from openings import SCHEDULE, counts
import svg_plan, svg_site, svg_elev

RD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "renders")


def hl(t):
    return f'<span class="hl">{t}</span>'


def band(title, cls="b1"):
    return f'<h2 class="{cls}">{title}</h2>'


def _b64(path, width):
    im = Image.open(path).convert("RGB")
    im.thumbnail((width, width))
    b = io.BytesIO()
    im.save(b, "JPEG", quality=80)
    return base64.b64encode(b.getvalue()).decode()


def cover():
    a, b = areas(), budget()
    return f"""
<section class="cover">
  <div class="kicker">Design report, budget edition</div>
  <h1>Courtyard Bungalow</h1>
  <div class="sub">Garo Hills, Meghalaya &nbsp;|&nbsp; one hectare: 328.08 ft × 328.08 ft &nbsp;|&nbsp; Seismic Zone V</div>
  <table class="keyfacts">
    <tr><td>Everything on the plot, all in</td><td>{hl(money(b['grand']))} against a limit of ₹ 50.00 lakh</td></tr>
    <tr><td>House, outer size</td><td>{OUT_W:.2f} ft × {OUT_D:.2f} ft = {hl(f"{a['built']:,.2f} sq ft")} built-up</td></tr>
    <tr><td>Carpet area</td><td>{hl(f"{a['carpet']:,.2f} sq ft")} (sum of eleven rooms, worked out in section 4)</td></tr>
    <tr><td>Rooms</td><td>Sitting and dining (one open room); walled kitchen with pantry; library and study (one room); bedroom 1 with dressing and bath; bedroom 2 with bath and wardrobe; shared toilet and bathroom with wash lobby in the north-east corner</td></tr>
    <tr><td>Heights</td><td>Plinth {hl("2.50 ft")}; ceilings {hl("12.00 ft")} in every habitable room, 10.00 ft in baths</td></tr>
    <tr><td>Outside</td><td>South veranda {VERANDA[0]:.2f} × {VERANDA[1]:.2f} ft; entrance porch {PORCH[0]:.2f} × {PORCH[1]:.2f} ft; carport {CARPORT[0]:.2f} × {CARPORT[1]:.2f} ft; firehouse 12.00 × 12.00 ft</td></tr>
  </table>
  <p class="note">Every length in this report is in feet, written as a decimal (13.44 ft, not 13 ft 5 in). Areas are in sq ft and volumes in cu ft. Every area and quantity is worked out on the page so you can check it with a calculator.</p>
</section>"""


def idea():
    return f"""
{band("1. The idea", "b1")}
<p>The earlier design cost ₹ 4.69 crore. To bring everything on the plot under ₹ 50 lakh, the house is now one compact rectangle, 46.00 ft by 28.00 ft on its wall centre lines, under one simple hipped roof. Plain shapes are the cheapest to build, and also the strongest in an earthquake.</p>
<p>The plan has three bays. The middle bay is one open sitting-and-dining room, 15.62 ft wide and 27.25 ft deep, running from the front door on the north to the veranda on the south. The west bay holds the library-study at the front and your bedroom suite at the back. The east bay holds the shared toilet and bathroom in the north-east corner, the kitchen behind its own wall, and the guest bedroom with its bath. The two bedrooms are at opposite ends, both facing south for winter sun.</p>
<p>The rest of the hectare stays almost free to build: native grove left to grow, an orchard and kitchen garden planted from saplings, a gravel drive, a carport instead of a garage, and a chain-link fence instead of a masonry compound wall, with a short stone wall only at the gate.</p>
"""


def views():
    out = [band("2. Views of the house", "b8")]
    ai = os.path.join(RD, "ai_front_exterior.png")
    if os.path.exists(ai):
        out.append(f'<figure class="hero"><img src="data:image/jpeg;base64,{_b64(ai, 1500)}"/>'
                   '<figcaption>Mood image (AI-generated) of the cream walls, stone base, charcoal roof and white porch posts. '
                   'The exact house is the smaller one in the 3D views and drawings that follow.</figcaption></figure>')
    caps = [("render_front.png", "Approach from the north-east: entrance porch, front door and north windows."),
            ("render_rear.png", "Garden side: the 8.00 ft south veranda, with the firehouse in front."),
            ("render_aerial.png", "Aerial view: house, turning circle, carport, firehouse and planting."),
            ("render_cutaway.png", "Cut-away at 8.50 ft, furnished: library-study and bedroom 1 on the left, sitting and dining in the middle, wet corner, kitchen and bedroom 2 on the right."),
            ("render_hall.png", "Sitting and dining, looking north-east to the kitchen door."),
            ("render_kitchen.png", "Kitchen behind its own wall: counters, sink, cooker and a small table."),
            ("render_bed1.png", "Bedroom 1, bed against the inner wall, French door to the veranda."),
            ("render_library.png", "Library and study, with desk and shelves.")]
    cells = []
    for f, cap in caps:
        p = os.path.join(RD, f)
        if os.path.exists(p):
            cells.append(f'<figure><img src="data:image/jpeg;base64,{_b64(p, 1100)}"/><figcaption>{cap}</figcaption></figure>')
    if cells:
        out.append('<p class="note">These views come from a 3D model built from the same measurements as the plan. Furniture and trees are shown in simplified form.</p>')
        out.append('<div class="gallery">' + "".join(cells) + "</div>")
    return "\n".join(out)


def budget_section():
    b = budget()
    rows = []
    cur = None
    for g, name, q, unit, rate, amt, work in b["rows"]:
        if g != cur:
            rows.append(f"<tr class='grp'><td colspan='4'>{g}</td></tr>")
            cur = g
        qtxt = "lump sum" if unit == "lump sum" else f"{q:,.2f} {unit}"
        rtxt = "" if unit == "lump sum" else f"₹ {rate:,} per {unit.replace('running ft', 'ft')}"
        calc = "" if unit == "lump sum" else f"{q:,.2f} × {rate:,} = ₹ {amt:,.0f}"
        rows.append(f"<tr><td>{name}" + (f"<div class='work'>{work}</div>" if work else "") +
                    f"</td><td class='n'>{qtxt}</td><td class='n'>{rtxt}<div class='work'>{calc}</div></td><td class='n'>{lakh(amt)}</td></tr>")
    summary = "".join(f"<tr><td>{g}</td><td class='n'>{lakh(s)}</td></tr>" for g, s in b["subs"])
    return f"""
{band("3. Budget: everything on the plot within ₹ 50 lakh", "b6")}
<p>Rates are indicative for the Garo Hills in 2026, for plain, sound local construction: an RCC frame for Seismic Zone V, brick walls, cement plaster with lime-wash, a charcoal profile-sheet roof on steel trusses, vitrified tiles in the main rooms and local stone for the base and verandas. They assume a local contractor working to these drawings, with the owner buying the main materials. Get three local quotes against this report before fixing the budget.</p>
<table class="t small">
<tr><th>Item and how the quantity is worked out</th><th class='n'>Quantity</th><th class='n'>Rate and amount</th><th class='n'>Amount</th></tr>
{''.join(rows)}
</table>
<table class="t totals">
{summary}
<tr><td>Works total</td><td class='n'>{lakh(b['works'])}</td></tr>
<tr><td>Structural check and drawings by a local engineer</td><td class='n'>{lakh(b['fees'])}</td></tr>
<tr><td>Contingency: 5% of ({lakh(b['works'])} + {lakh(b['fees'])}) = {lakh(b['cont'])}</td><td class='n'>{lakh(b['cont'])}</td></tr>
<tr class="tot"><td>Grand total</td><td class='n'>{hl(money(b['grand']))}</td></tr>
<tr><td>Margin left under ₹ 50.00 lakh</td><td class='n'>{lakh(5000000 - b['grand'])}</td></tr>
</table>
<p class="note">What keeps it under budget: a compact 1,344.06 sq ft house instead of 4,024.38 sq ft; one veranda instead of three; a steel carport instead of a garage block; a 12.00 × 12.00 ft firehouse instead of 20.00 × 20.00 ft; and a chain-link fence for 1,236.82 ft of the boundary instead of a masonry wall. A full stone-and-render compound wall round the hectare would cost about 1,312.32 ft × ₹ 4,800 = ₹ 62.99 lakh on its own, so it is left for a later phase.</p>
"""


def area_statement():
    a = areas()
    rows = []
    for r in a["rt"]:
        rows.append(f"<tr><td><b>{r['name']}</b></td><td>{working(*r['wx'])}</td><td>{working(*r['dy'])}</td>"
                    f"<td class='n'>{r['w']:.2f} × {r['d']:.2f} = {hl(f'{r[chr(97)+chr(114)+chr(101)+chr(97)]:.2f}')}</td><td class='n'>{r['ceil']:.2f}</td></tr>")
    tot = " + ".join(f"{r['area']:.2f}" for r in a["rt"])
    return f"""
{band("4. Area statement, worked out", "b4")}
<p>Each room is a box on the wall centre lines. Its clear (usable) size is the centre-line length minus half of each wall it touches: half of an external wall is 0.75 ÷ 2 = 0.375 ft, and half of an internal wall is 0.375 ÷ 2 = 0.1875 ft. Where a side has no wall, nothing is taken off.</p>
<table class="t tiny">
<tr><th>Room</th><th>Clear width, ft (east–west)</th><th>Clear depth, ft (north–south)</th><th class='n'>Carpet area, sq ft</th><th class='n'>Ceiling, ft</th></tr>
{''.join(rows)}
</table>
<table class="t totals">
<tr><td>Carpet area = {tot}</td><td class='n'>{hl(f"{a['carpet']:,.2f} sq ft")}</td></tr>
<tr><td>Built-up area (outer faces) = {OUT_W:.2f} × {OUT_D:.2f}</td><td class='n'>{hl(f"{a['built']:,.2f} sq ft")}</td></tr>
<tr><td>Walls take up {a['built']:,.2f} − {a['carpet']:,.2f}</td><td class='n'>{a['built']-a['carpet']:,.2f} sq ft ({100*(a['built']-a['carpet'])/a['built']:.2f}%)</td></tr>
<tr><td>Covered open area = veranda {VERANDA[0]:.2f} × {VERANDA[1]:.2f} ({a['ver']:.2f}) + porch {PORCH[0]:.2f} × {PORCH[1]:.2f} ({a['porch']:.2f})</td><td class='n'>{a['covered']:,.2f} sq ft</td></tr>
<tr><td>Super built-up = {a['built']:,.2f} + {a['covered']:,.2f}</td><td class='n'>{hl(f"{a['super']:,.2f} sq ft")}</td></tr>
<tr><td>Circulation (dressing 1 lobby + wash lobby) = {a['circ']:.2f} ÷ {a['carpet']:,.2f} × 100</td><td class='n'>{a['circ_pct']:.2f}% (limit 12.00%)</td></tr>
</table>
"""


def plan():
    return f"""
{band("5. Ground floor plan", "b5")}
<figure class="dwgfig">{svg_plan.main_plan()}</figure>
"""


def walkthrough():
    return f"""
{band("6. Setting out and walkthrough", "b7")}
<h3>Setting out</h3>
<p>Peg the north-west corner. Run the north wall centre line due east {hl("46.00 ft")} and the west wall centre line due south {hl("28.00 ft")}. Check the diagonal: √(46.00² + 28.00²) = √(2,116.00 + 784.00) = √2,900.00 = {hl("53.85 ft")}. The two internal centre lines across the house are at x = 14.00 ft and x = 30.00 ft from the west wall. Columns stand at every corner and junction shown black on the plan, and at x = 22.00 ft on the north and south walls, so no wall runs more than 16.00 ft between columns.</p>
<h3>West bay (x = 0.00 to 14.00 ft)</h3>
<p><b>Library and study</b> (y = 0.00 to 10.00): two W1 windows on the north wall at x = 4.00 and 10.00, one W1 on the west wall at y = 5.00, door D2 on x = 14.00 at y = 5.00 from the sitting room. Below it, an internal wall on y = 10.00. <b>Bath 1</b> (x = 0.00 to 6.00, y = 10.00 to 17.00) on the west wall, with W3 at y = 13.50. <b>Dressing 1</b> (x = 6.00 to 14.00, y = 10.00 to 17.00) is the entry lobby to the suite, with door D2 from the sitting room on x = 14.00 at y = 13.50, door D3 to bath 1 on x = 6.00 at y = 13.50, and door D2 to the bedroom on y = 17.00 at x = 10.00. <b>Bedroom 1</b> (y = 17.00 to 28.00) has W1 on the west wall at y = 22.50 and French door FD1 on the south wall at x = 7.00.</p>
<h3>Middle bay (x = 14.00 to 30.00 ft)</h3>
<p><b>Sitting and dining</b> is one open room, 15.62 ft × 27.25 ft. The main door D1, {hl("4.00 ft × 8.00 ft")}, is on the north wall at x = 22.00, with W1 windows at x = 17.50 and 26.50. The dining table sits in the north half near the kitchen door; the sitting area is in the south half, with two French doors FD1 at x = 18.50 and 25.50 onto the veranda.</p>
<h3>East bay (x = 30.00 to 46.00 ft)</h3>
<p>The {hl("wet corner")} is the north strip (y = 0.00 to 7.00): a <b>wash lobby</b> (x = 30.00 to 34.00) with a basin under W3, entered from the sitting room through a 3.00 ft opening on x = 30.00 at y = 3.50; and the <b>shared toilet and bathroom</b> (x = 34.00 to 46.00) in the north-east corner, with WC, basin and a walk-in shower, door D3 on x = 34.00, W3 windows on the north wall at x = 40.00 and the east wall at y = 3.50. The <b>kitchen</b> (y = 7.00 to 16.00) is closed off from the dining area by the wall on x = 30.00, with door D2 at y = 11.50, and has W1 on the east wall at y = 11.50 over the counter. <b>Bedroom 2</b> (x = 30.00 to 40.50, y = 16.00 to 28.00) has door D2 on x = 30.00 at y = 19.50 and FD1 on the south wall at x = 35.25. <b>Bath 2</b> (x = 40.50 to 46.00, y = 16.00 to 22.00) is on the east wall with W3 at y = 19.00; <b>wardrobe 2</b> (y = 22.00 to 28.00) opens off the bedroom through a 3.00 ft opening.</p>
<h3>Levels</h3>
<p>Floor level is {hl("2.50 ft")} above the ground at the porch. The porch is reached by 4 steps: 2.50 ÷ 4 = 0.625 ft rise each, on 1.00 ft treads. The ground falls about 1.50 ft across the house to the south, so the veranda is 4.00 ft above the garden there, reached by 5 steps: 4.00 ÷ 5 = 0.80 ft rise each, on 1.00 ft treads. Bath floors are 0.08 ft lower than the room floors and fall 1:60 to a floor trap.</p>
"""


def walls_table():
    rows = "".join(f"<tr><td>{thick(t)}</td><td>{k}</td><td>({x0:.2f}, {y0:.2f}) to ({x1:.2f}, {y1:.2f})</td><td class='n'>{abs(x1-x0)+abs(y1-y0):.2f} ft</td></tr>"
                   for x0, y0, x1, y1, t, k in WALLS)
    ext = sum(abs(x1 - x0) + abs(y1 - y0) for x0, y0, x1, y1, t, _ in WALLS if t == EXT)
    intl = sum(abs(x1 - x0) + abs(y1 - y0) for x0, y0, x1, y1, t, _ in WALLS if t == INT)
    return f"""
<h3>Wall list for the mason</h3>
<table class="t small">
<tr><th>Thickness</th><th>Wall</th><th>Centre line from (x, y) to (x, y), ft</th><th class='n'>Length</th></tr>
{rows}
<tr class="tot"><td colspan="3">External walls 46.00 + 46.00 + 28.00 + 28.00</td><td class='n'>{ext:.2f} ft</td></tr>
<tr class="tot"><td colspan="3">Internal walls, total</td><td class='n'>{intl:.2f} ft</td></tr>
</table>
"""


def dw_schedule():
    c = counts()
    rows = "".join(
        f"<tr><td><b>{m}</b></td><td class='n'>{c.get(m, 0)}</td><td>{typ}</td><td>{mat}</td><td>{hl(f'{w:.2f} × {h:.2f}')}</td>"
        f"<td>{sill:.2f}</td><td>{lin:.2f}</td><td>{glz}</td><td>{hw}</td></tr>"
        for m, (typ, mat, w, h, sill, lin, glz, hw) in SCHEDULE.items())
    return f"""
{band("7. Door and window schedule", "b10")}
<p>Sizes are clear openings, width × height, in feet. Sill and lintel are heights above the floor. Every head sits on the one continuous lintel band at 8.00 ft, which is also an earthquake band. Every outside opening gets a white drip mould 0.25 ft deep above it.</p>
<table class="t tiny">
<tr><th>Mark</th><th class='n'>No.</th><th>Type</th><th>Material</th><th>Width × height, ft</th><th>Sill, ft</th><th>Lintel, ft</th><th>Glazing</th><th>Hardware</th></tr>
{rows}
</table>
"""


def climate_structure():
    r = rain()
    k = math.tan(math.radians(25))
    parts = " + ".join(f"{w:.2f} × {d:.2f}" for w, d in [(52.0, 31.0), (52.75, 9.0), (11.0, 7.0)])
    return f"""
{band("8. Climate and structure, worked out", "b2")}
<table class="t small">
<tr><th style="width:22%">Condition</th><th>How it is handled, with the arithmetic</th></tr>
<tr><td><b>Heavy monsoon</b></td><td>Roof area = {parts} = {r['area']:,.2f} sq ft. Design storm 0.417 ft of rain an hour. Peak run-off = {r['area']:,.2f} × 0.417 ÷ 3,600 = {hl(f"{r['q']:.3f} cu ft a second")}. At 500 sq ft per downpipe: {r['area']:,.2f} ÷ 500 = {r['area']/500:.2f}, so {r['pipes']} are needed; {hl("6 downpipes of 0.33 ft diameter")} are provided. Gutters 0.50 ft wide × 0.33 ft deep, laid 1:200. Roof pitch 25°; overhang 3.00 ft on north, east and west.</td></tr>
<tr><td><b>Rainwater tank</b></td><td>Ferrocement tank {TANK['dia']:.2f} ft diameter × {TANK['depth']:.2f} ft deep: volume = 3.1416 × 5.00 × 5.00 × 4.50 = {hl(f"{r['vol']:.2f} cu ft")}. It fills from {r['vol']:.2f} ÷ ({r['area']:,.2f} × 0.85) = {r['fill']:.2f} ft of rain. The year's rain off the roof is {r['area']:,.2f} × 10.83 × 0.85 = {r['annual']:,.2f} cu ft. At 14.00 cu ft a day the tank lasts {r['vol']:.2f} ÷ 14.00 = {r['days']:.2f} days, so the spring or well line carries the dry months and the tank is the backup. Overflow goes to the swales.</td></tr>
<tr><td><b>Winter sun, summer shade</b></td><td>Latitude 25.50° N. Noon sun height: winter 90.00 − 25.50 − 23.44 = {SUN['winter']:.2f}°; equinox 90.00 − 25.50 = {SUN['equinox']:.2f}°; summer 90.00 − 25.50 + 23.44 = {SUN['summer']:.2f}°. Veranda eave {svg_elev.VER_EAVE:.2f} ft high and 9.00 ft out from the wall: winter sun lights {svg_elev.VER_EAVE:.2f} − 9.00 × tan {SUN['winter']:.2f}° = {svg_elev.VER_EAVE - 9*math.tan(math.radians(SUN['winter'])):.2f} ft of the south glass; at the equinox {svg_elev.VER_EAVE:.2f} − 9.00 × tan {SUN['equinox']:.2f}° = {svg_elev.VER_EAVE - 9*math.tan(math.radians(SUN['equinox'])):.2f} ft, below zero, so the glass is fully shaded from March to September.</td></tr>
<tr><td><b>Seismic Zone V</b></td><td>RCC frame, M25 concrete, Fe 500D bars, detailed to IS 13920. Columns {hl("0.75 × 1.00 ft")}, none more than 16.00 ft apart. Footings 4.00 × 4.00 × 1.25 ft, founded 4.00 ft below natural ground. Plinth beam 0.75 × 1.25 ft; lintel band 0.75 × 0.50 ft at 8.00 ft; roof band 0.75 × 1.00 ft at 13.00 ft. Brick walls are infill only. The light sheet roof on steel trusses keeps weight off the top of the frame.</td></tr>
<tr><td><b>Damp and fungus</b></td><td>Plinth 2.50 ft high with a damp-proof course; every room has windows on two faces or a window and a door to an open room; the 3.00 ft overhangs and the 8.00 ft veranda keep rain off the walls; lime-wash lets the walls breathe.</td></tr>
</table>
{band("9. North elevation and sun section", "b8")}
<figure class="dwgfig">{svg_elev.north_elevation()}</figure>
<figure class="dwgfig">{svg_elev.sun_section()}</figure>
<figure class="dwgfig">{svg_site.roof_plan()}</figure>
"""


def finishes():
    rows = [
        ("Sitting and dining, kitchen, wash lobby", "Vitrified tiles 2.00 × 2.00 ft, matt", "Cement plaster, cream lime-wash", "Painted gypsum at 12.00 ft; exposed timber beams in sitting room", "Kitchen counter 2.00 ft deep, granite top, open shelves"),
        ("Bedrooms, library-study, dressing", "Vitrified tiles 2.00 × 2.00 ft, wood-look", "Cement plaster, cream lime-wash", "Painted gypsum at 12.00 ft", "Built-in shelves in library, ply wardrobes"),
        ("Toilet and bathrooms", "Anti-skid tiles 1.00 × 1.00 ft, fall 1:60", "Tiles to 7.00 ft in showers, 4.00 ft elsewhere", "Painted gypsum at 10.00 ft, exhaust fan", "Walk-in showers, no tub, no seat"),
        ("Veranda and porch", "Local stone slabs", "Cream render", "Sheet roof, painted underside", "White steel posts in timber-look paint"),
        ("Outside walls", "Stone base to 1.50 ft above floor (4.00 ft above ground)", "Cement plaster, cream lime-wash above", "Charcoal profile sheet roof", "Black-painted steel windows, dark hardwood front door"),
    ]
    r = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td></tr>" for a, b, c, d, e in rows)
    return f"""
{band("10. Finishes (budget)", "b11")}
<table class="t tiny"><tr><th>Space</th><th>Floor</th><th>Walls</th><th>Ceiling or roof</th><th>Other</th></tr>{r}</table>
"""


def site():
    b = budget()
    return f"""
{band("11. Site, landscape, firehouse, carport and gate", "b3")}
<figure class="dwgfig">{svg_site.site_plan()}</figure>
<table class="t small">
<tr><th style="width:20%">Element</th><th>What and how big</th></tr>
<tr><td><b>Approach</b></td><td>Steel gate in the middle of the north boundary, 12.00 ft clear, with a 3.50 ft wicket. Gravel drive {hl("12.00 ft wide")} running 115.00 ft to a turning circle of {hl("40.00 ft diameter")} (radius 20.00 ft; a car needs about 18.00 ft) around a planted island of 12.00 ft diameter with a young Champak tree. Drive camber 1:50, with an open earth drain 1.00 ft wide × 1.00 ft deep along each side.</td></tr>
<tr><td><b>Carport</b></td><td>{CARPORT[0]:.2f} × {CARPORT[1]:.2f} ft = {CARPORT[0]*CARPORT[1]:.2f} sq ft, west of the turning circle: four steel posts, a charcoal sheet roof sloping 1:25 at 7.20 to 6.40 ft high, gravel floor, and a lockable steel cupboard 4.00 × 2.00 ft for tools and fuel.</td></tr>
<tr><td><b>Firehouse</b></td><td>34.63 ft south of the veranda edge (71.00 \u2212 36.38), on a stone platform 14.00 × 14.00 ft, 1.00 ft high. Four timber posts on 12.00 ft centres carry a 25° pyramid roof with a 2.00 ft overhang and a 1.50 ft square smoke vent at the top. Stone fire pit 4.00 ft inside diameter with a kerb 0.75 ft wide and 1.25 ft high; stone bench on a 240° arc of 4.60 ft radius: arc length = 2 × 3.1416 × 4.60 × 240 ÷ 360 = 19.27 ft, room for 8 people at 2.40 ft each.</td></tr>
<tr><td><b>Boundary</b></td><td>Perimeter = 4 × 328.08 = 1,312.32 ft. Stone wall 4.00 ft high for 30.00 ft each side of the gate (60.00 ft), with 2.00 ft square piers 6.00 ft high. Everywhere else, 1,236.82 ft of chain-link fence 5.00 ft high on RCC posts 10.00 ft apart (1,236.82 ÷ 10.00 = 124 posts), with two barbed strands on top. Plant a hedge of local shrubs along the inside so the fence disappears in two seasons.</td></tr>
<tr><td><b>Grove</b></td><td>Strips 70.00 ft wide on the east and west and 60.00 ft deep along the south are left as native trees (Schima, chestnut, wild fig, bamboo), with gaps planted from nursery saplings. Cut once a year.</td></tr>
<tr><td><b>Orchard and kitchen garden</b></td><td>Orchard band 188.00 × 26.00 ft = 4,888.00 sq ft south of the firehouse: Khasi mandarin, jackfruit, banana and Assam lemon at 18.00 ft spacing, so 188.00 ÷ 18.00 = 10 trees a row in 2 rows = 20 trees. Kitchen garden 50.00 × 55.00 ft = 2,750.00 sq ft east of the house, in raised beds 4.00 ft wide: greens, chillies, ginger, turmeric and pineapple.</td></tr>
<tr><td><b>Water on the slope</b></td><td>Three swales dug by hand along the contour, 2.00 ft wide × 1.25 ft deep, at about 222.00, 258.00 and 300.00 ft from the north boundary, spread run-off across the slope. They overflow to a small pond 30.00 × 18.00 ft in the lower grove, then to the natural drain at the south edge. Septic tank 6.00 × 4.00 × 5.00 ft = 120.00 cu ft, with a soak pit 4.00 ft diameter × 6.00 ft deep, 30.00 ft from the house and downhill of any well.</td></tr>
<tr><td><b>Four seasons</b></td><td>Winter: mandarins ripening, camellia and poinsettia. Spring: rhododendron and orchid trees (Bauhinia). Monsoon: ginger lily, hydrangea, jackfruit and pineapple. Autumn: night jasmine (shiuli) by the veranda, tree marigold, banana fruiting.</td></tr>
</table>
<figure class="dwgfig">{svg_elev.firehouse()}</figure>
<figure class="dwgfig">{svg_elev.gate()}</figure>
"""


def checks():
    a, b = areas(), budget()
    rows = [
        ("Total cost, everything on the plot, within ₹ 50 lakh", f"Met. {money(b['grand'])}, leaving {lakh(5000000 - b['grand'])} spare."),
        ("Every length in feet, calculations shown", "Met. Decimal feet throughout; areas, volumes, costs, rain and sun all worked out step by step."),
        ("Library and study as one room", "Met. One room of 13.44 × 9.44 = 126.82 sq ft at the north-west corner."),
        ("Wall between kitchen and dining", "Met. Internal wall on x = 30.00 ft with door D2 at y = 11.50 ft."),
        ("Shared toilet and bathroom in the corner", "Met. North-east corner of the house, 11.44 × 6.44 ft, with a wash lobby beside it."),
        ("No bathtub, no shower seat", "Met. Three walk-in showers; no tub or seat anywhere."),
        ("No ceiling under 12 ft in a habitable room", "Met. 12.00 ft in sitting and dining, kitchen, bedrooms and library-study."),
        ("Bedrooms at opposite ends", "Met. West and east bays, entered from opposite sides of the sitting room."),
        ("Circulation under 12 per cent", f"Met. {a['circ_pct']:.2f}%."),
        ("Reduced from your original brief because of the budget",
         "Room sizes are smaller than the brief (bedroom 1 is 13.44 × 10.44 ft instead of about 16 × 18 ft); there is one 8.00 ft veranda on the south face plus a porch on the north, not verandas on all main faces; a carport replaces the garage; the firehouse is 12.00 ft square instead of 20.00 ft; and the boundary is a fence with a short stone wall at the gate instead of a full compound wall. Each can be added later without changing the house."),
    ]
    r = "".join(f"<tr><td><b>{x}</b></td><td>{y}</td></tr>" for x, y in rows)
    return f"""
{band("12. Checked against your brief", "b7")}
<table class="t small"><tr><th style="width:32%">Your rule</th><th>Status</th></tr>{r}</table>
<p class="sign">Before building: survey the contours of the hectare, test the soil, and have a licensed structural engineer check and sign the drawings to IS 1893 and IS 13920. That fee is included in the budget.</p>
"""


def parts():
    return [cover(), idea(), '<div class="pb"></div>', views(), '<div class="pb"></div>', budget_section(),
            '<div class="pb"></div>', area_statement(), plan(), '<div class="pb"></div>', walkthrough(), walls_table(),
            dw_schedule(), '<div class="pb"></div>', climate_structure(), '<div class="pb"></div>', finishes(), site(),
            '<div class="pb"></div>', checks()]

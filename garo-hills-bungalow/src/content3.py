"""Part 3: elevation + section, structure, door/window and finishes schedules."""
from data import fi
from openings import SCHEDULE, counts
from content1 import band, hl
import svg_elev


def elevation_section():
    return f"""
{band("8. North elevation and the sun section", "b8")}
<figure class="dwgfig">{svg_elev.north_elevation()}</figure>
<figure class="dwgfig">{svg_elev.sun_section()}</figure>
<p class="note">The section is the reason the veranda roof is a separate, flatter roof at 1 in 6 rather than a continuation of the 25° main roof: carried down at 25° the veranda eave would sit near 9 ft 6 in and shut out the winter sun. At +12 ft 5 in it lets the December sun in and still stops every ray from the equinox to the June solstice.</p>
"""


def structure():
    rows = [
        ("Footings", "Isolated RCC footings, 6 ft 0 in x 6 ft 0 in x 1 ft 6 in deep under grid columns (to be confirmed by soil test, safe bearing assumed 1.5 ton per sq ft), founded 5 ft 0 in below natural ground; stepped with the slope, never on fill"),
        ("Plinth beam (tie level 1)", "12 in x 18 in, continuous on every wall line, top at FFL less 4 in"),
        ("Columns", "12 in x 18 in, M25, 6 bars of 16 mm, 8 mm ties at 4 in centres for 2 ft 0 in at top and bottom of every column and through every joint (IS 13920)"),
        ("Lintel band (tie level 2)", "9 in wide x 6 in deep, continuous at +8 ft 0 in through all walls, 4 bars of 10 mm; it is the head of every door and window"),
        ("Roof band and ring beam (tie level 3)", "12 in x 21 in at +15 ft 0 in, carries the steel trusses on cast-in base plates with anchor bolts"),
        ("Beams over open plan lines", "12 in x 24 in at +12 ft 3 in soffit between columns (32, 13) to (50, 13), (50, 13) to (50, 40), and over the passage opening (62, 13) to (62, 17)"),
        ("Infill walls", "9 in brick in 1:4 cement mortar on external and party walls; 4½ in brick in 1:3 with 2 bars of 6 mm every fourth course on partitions; all infill gapped ¾ in below beams and packed with compressible filler so it cannot stiffen the frame"),
        ("Roof", "Galvanised tubular steel trusses at 6 ft 0 in centres (scissor trusses over the hall), Z purlins, 50 mm PIR insulated sandwich panel with 0.5 mm charcoal standing-seam top skin"),
    ]
    r = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td></tr>" for a, b in rows)
    return f"""
{band("9. Structure: columns, beams and the three tie levels", "b9")}
<table class="t small"><tr><th style="width:26%">Element</th><th>Size and specification</th></tr>{r}</table>
"""


def dw_schedule():
    c = counts()
    rows = []
    for m, (typ, mat, w, h, sill, lintel, glz, hw) in SCHEDULE.items():
        rows.append(f"<tr><td><b>{m}</b></td><td class='n'>{c.get(m, 0)}</td><td>{typ}</td><td>{mat}</td><td>{hl(fi(w, 0) + ' x ' + fi(h, 0))}</td>"
                    f"<td>{fi(sill, 0) if sill else 'floor'}</td><td>{fi(lintel, 0)}</td><td>{glz}</td><td>{hw}</td></tr>")
    return f"""
{band("10. Door and window schedule", "b10")}
<p>All sizes are clear opening, width x height. Heights and sills are above finished floor. Every opening has a {hl("drip mould")} 3 in deep in cement-lime render above it, projecting 1½ in with a throated underside. V1 vents sit in the band between the lintel band (+8 ft 0 in) and the roof band; their own head is a 4 in RCC sub-lintel at +11 ft 0 in.</p>
<table class="t tiny">
<tr><th>Mark</th><th class='n'>No.</th><th>Type</th><th>Material</th><th>Clear width x height</th><th>Sill</th><th>Lintel</th><th>Glazing</th><th>Hardware</th></tr>
{''.join(rows)}
</table>
"""


def finishes():
    rows = [
        ("Sitting hall, dining, foyer, alcove", "Grey-green Garo Hills stone or cream terrazzo with brass strips at column lines, 24 in x 24 in, honed", "Lime wash, warm cream, matt", "Hall: timber boarding (local pine, oiled) on scissor trusses; elsewhere gypsum, matt cream", "4 in stone skirting"),
        ("Kitchen", "Terrazzo, honed, same as hall", "Lime plaster; 2 ft 0 in high stone backsplash behind counters", "Gypsum, washable matt", "Counters 1¼ in local granite, cabinets marine ply with hardwood fronts"),
        ("Bedrooms 1 and 2", "Hardwood strip (teak or local hollock) 4 in wide on screed with moisture barrier", "Lime wash, cream", "Gypsum, matt", "Timber skirting 4 in"),
        ("Library", "Hardwood strip", "Lime wash; full-height timber shelving on south and east walls", "Timber boarded, oiled", "UV film on W2 glass"),
        ("Bathrooms, shared washroom", "Anti-skid matt vitrified tile 24 in x 24 in, or local stone, falls 1 in 60", "Full height glazed tile in the shower, waist height elsewhere, lime plaster above", "Moisture-resistant gypsum, exhaust fan 6 in on timer", "Walk-in shower, frameless glass screen, no tray, no tub, no seat"),
        ("Utility, store, passage", "Kota or local stone", "Cement plaster, washable paint", "Gypsum", "Floor trap in utility"),
        ("Verandas and porch", "Flamed local stone 1¼ in, falls 1 in 80 outwards", "Cream lime render on stone base", "Exposed timber boarding under roof", "White rendered columns 1 ft 4 in diameter, plain capital and base"),
        ("Exterior walls", "Stone base: random rubble Garo Hills stone to +1 ft 6 in (sill)", "Above: 3-coat lime render, cream lime wash", "Roof soffit: timber boarding, dark stain", "Black aluminium windows, dark hardwood doors"),
    ]
    r = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td></tr>" for a, b, c, d, e in rows)
    return f"""
{band("11. Finishes schedule", "b11")}
<table class="t tiny"><tr><th>Space</th><th>Floor</th><th>Walls</th><th>Ceiling</th><th>Other</th></tr>{r}</table>
"""

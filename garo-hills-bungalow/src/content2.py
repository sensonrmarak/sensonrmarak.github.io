"""Part 2: plan, area statement, room schedule, written walkthrough."""
from data import areas, fi, ff, WALLS
from content1 import band, hl
import svg_plan

WHY = {
    "BED1": "Bettered: 17 ft 3 in x 17 ft 6 in against 16 x 18, with two armchairs at the south French door.",
    "STU": "Bettered: 16 ft 3 in x 18 ft 3 in inside the acoustic lining against 14 x 16, so a grand piano and a drum kit fit together.",
    "BED2": "15 ft 6 in x 17 ft 3 in against 14 x 17: same proportion, a little more room for the bed.",
    "HALL": "Bettered: 31 ft 6 in x 26 ft 6 in against 24 x 32, deeper so seating can face both the south view and the foyer.",
    "KIT": "Bettered: 17 ft 6 in x 22 ft 6 in against 16 x 20, room for an island and a breakfast table in the sun.",
    "LIB": "13 ft 6 in x 12 ft 6 in against 12 x 14: same area, wider wall for north windows.",
    "UTL": "7 ft 6 in x 12 ft 6 in against 8 x 10: slightly longer for a washer, dryer and a deep sink in a row.",
}


def area_statement():
    a = areas()
    rows = "".join(
        f"<tr><td>{r['name']}</td><td>{fi(r['w'])} x {fi(r['d'])}</td><td class='n'>{r['area']:,}</td><td>{r['ceil']}</td></tr>"
        for r in a["rt"])
    grows = "".join(
        f"<tr><td>{r['name']}</td><td>{fi(r['w'])} x {fi(r['d'])}</td><td class='n'>{r['area']:,}</td><td>{r['ceil']}</td></tr>"
        for r in a["gt"])
    vrows = "".join(f"<tr><td>{n}</td><td>{l} ft 0 in x {d} ft 0 in</td><td class='n'>{ar:,}</td><td>open sided</td></tr>" for n, l, d, ar in a["ver"])
    return f"""
{band("4. Area statement", "b4")}
<table class="t small">
<tr><th>Space</th><th>Clear size (rounded to 3 in)</th><th class='n'>Carpet, sq ft</th><th>Floor to ceiling</th></tr>
<tr class="grp"><td colspan="4">Main house</td></tr>
{rows}
<tr class="tot"><td colspan="2">Carpet area, main house</td><td class='n'>{hl(f"{a['carpet_house']:,}")}</td><td></td></tr>
<tr class="grp"><td colspan="4">Garage and studio block</td></tr>
{grows}
<tr class="tot"><td colspan="2">Carpet area, garage and studio block</td><td class='n'>{a['carpet_gar']:,}</td><td></td></tr>
<tr class="grp"><td colspan="4">Covered open spaces</td></tr>
{vrows}
<tr><td>Firehouse pavilion</td><td>20 ft 0 in x 20 ft 0 in on column centres</td><td class='n'>{a['fire']:,}</td><td>eave 9 ft 6 in</td></tr>
</table>
<table class="t totals">
<tr><td>Total carpet area (house + garage block)</td><td class='n'>{hl(f"{a['carpet']:,} sq ft")}</td></tr>
<tr><td>Built-up area: house {a['built_house']:,} (outer face 98 ft 9 in x 40 ft 9 in) + garage block {a['built_gar']:,}</td><td class='n'>{hl(f"{a['built']:,} sq ft")}</td></tr>
<tr><td>Super built-up area: built-up + verandas, porch, link walk ({a['ver_total']:,}) + firehouse ({a['fire']:,})</td><td class='n'>{hl(f"{a['super']:,} sq ft")}</td></tr>
<tr><td>Circulation (foyer + service passage) as share of house carpet: {a['circ']} sq ft</td><td class='n'>{hl(f"{a['circ_pct']:.1f} per cent")} (limit 12)</td></tr>
</table>
<p class="note">An independent house has no common areas, so super built-up here means everything you pay to build under a roof: enclosed area plus all covered open areas at full area.</p>
"""


def plan_pages():
    return f"""
{band("5. Ground floor plan, main house", "b5")}
<figure class="dwgfig">{svg_plan.main_plan()}</figure>
<p class="note">The drawing is generated from the same centre-line model as every table in this report, so a size on the plan and a size in a table can never disagree. Every wall ends on another wall or on a column; where the plan is open (foyer to hall, hall to dining, dining to kitchen and passage) the line is carried by a beam between columns at +12 ft 3 in.</p>
"""


def room_schedule():
    a = areas()
    rows = []
    for r in a["rt"]:
        rows.append(f"<tr><td><b>{r['name']}</b></td><td>{fi(r['w'])} x {fi(r['d'])}</td><td class='n'>{r['area']}</td>"
                    f"<td>x {r['x0']} to {r['x1']} ft, y {r['y0']} to {r['y1']} ft</td><td>{r['ceil']}</td></tr>")
        if r["key"] in WHY:
            rows.append(f"<tr class='why'><td colspan='5'>{WHY[r['key']]}</td></tr>")
    return f"""
{band("6. Room by room schedule", "b6")}
<p>Set-out box gives the four wall centre lines of each room, in feet, measured east (x) from the west wall centre line and south (y) from the north wall centre line. Clear sizes deduct half of each bounding wall: 4½ in for a 9 in wall, 2¼ in for a 4½ in partition, nothing on an open side (measured to the column line).</p>
<table class="t small">
<tr><th>Room</th><th>Clear size</th><th class='n'>sq ft</th><th>Set-out box (centre lines)</th><th>Ceiling</th></tr>
{''.join(rows)}
</table>
"""


def walls_table():
    rows = "".join(
        f"<tr><td>{'9 in' if t == 9 else '4½ in'}</td><td>{k}</td><td>({x0}, {y0}) to ({x1}, {y1})</td><td class='n'>{ff(abs(x1-x0)+abs(y1-y0), 0)}</td></tr>"
        for x0, y0, x1, y1, t, k in WALLS)
    return f"""
<h3>Wall list for the mason</h3>
<table class="t small">
<tr><th>Thickness</th><th>Wall</th><th>Centre line, from (x, y) to (x, y), ft</th><th class='n'>CL length</th></tr>
{rows}
</table>
"""


def walkthrough():
    return f"""
{band("7. Layout walkthrough, zone by zone", "b7")}
<p>Read this with the plan. All positions are on centre lines. The main block is a rectangle {hl("98 ft 0 in x 40 ft 0 in")} on centre lines (98 ft 9 in x 40 ft 9 in outer face), long side east to west, the south face looking at the garden and the firehouse.</p>
<h3>Setting out</h3>
<p>Peg the north-west corner of the main block. Run the north wall centre line due east 98 ft 0 in and the west wall centre line due south 40 ft 0 in; check the diagonal at {hl("105 ft 10¼ in")}. The creative wing continues the west wall line 27 ft 0 in further north, 18 ft 0 in wide. Peg column centres on the north line at 0, 18, 32, 50, 62, 80 and 98 ft; on the south line at 0, 18, 34, 50, 62, 80 and 98 ft; at the wing corners (0, -27), (18, -27), (0, -7), (18, -7); on the west line at 13 and 22 ft; on the east line at 13 and 24 ft; and the internal columns at (18, 13), (32, 13), (50, 13), (62, 13), (62, 17), (80, 13), (80, 17), (80, 24).</p>
<h3>Zone A: entrance, north face</h3>
<p>The car porch, {hl("20 ft 0 in x 14 ft 0 in")}, stands on four columns at x 31 and 51, y -22 and -15 (north of the house), and the drive passes under it east to west. Behind it the north veranda, 8 ft 0 in deep, runs from x 18 to x 62 on columns at 11 ft centres. Five risers of 6 in take you from the porch floor up to the veranda at FFL. The main door D1, {hl("4 ft 0 in x 8 ft 0 in")}, is centred at x 41 on the north wall, with its side light SL1 to the east at x 44. Two W1 windows at x 35.5 and x 47.5 light the foyer.</p>
<h3>Zone B: foyer, the creative suite and the alcove</h3>
<p>The foyer runs x 32 to 50, y 0 to 13, and opens straight into the sitting hall with no wall on y 13: a beam spans from column (32, 13) to column (50, 13). West of the foyer is the {hl("creative suite")}, three rooms in a row that work as one:</p>
<ul>
<li><b>Library</b> (x 18 to 32, y 0 to 13): behind a 4½ in partition on x 32. Its door D2 is on its south wall at x 29, opening from the hall, and two W2 north-light windows sit at x 22.5 and 27.5.</li>
<li><b>Study</b> (x 0 to 18, y 0 to 13): reached from the library through a {hl("pair of glazed doors D5, 5 ft 0 in x 8 ft 0 in")} centred at y 6.5 on x 18. It has a W1 on the west wall at y 6.5. Its south wall on y 13 is a 9 in acoustic wall, so the resident's bedroom suite is screened from it.</li>
<li><b>Music studio</b> (x 0 to 18, y -27 to -7): in its own wing projecting north. You enter from the study through acoustic door SD1 at x 9 on y 0, cross the airlock and gear lobby (y -7 to 0), and go through a second SD1 at x 9 on y -7. Inside the 9 in walls an independent lining stands 6½ in clear; two of its walls and the ceiling are splayed, so no two surfaces are parallel. Windows: W1 on the west wall at y -17, W1 on the east wall at y -17, W2 on the north wall at x 9, all double glazed.</li>
</ul>
<p>East of the foyer, a 4½ in partition on x 50 forms the crockery and bar alcove (x 50 to 62), open on its south side to the dining area, with one W1 at x 56.</p>
<h3>Zone C: sitting hall, dining, kitchen</h3>
<p>One continuous room from x 18 to x 80, y 13 to 40. Its west side is the 9 in party wall on x 18 (resident suite behind it). The sitting hall (x 18 to 50) has a vaulted ceiling rising from 12 ft 3 in at the walls to 16 ft 0 in at y 26.5, set on the bottom chords of scissor trusses. Two French doors FD1 open to the veranda at x 25 and x 43, with W1 windows at x 30 and x 38 either side of the south column at x 34. At x 50 the floor stays level but the ceiling drops to a flat 12 ft 3 in: that line and the columns at (50, 13) and (50, 40) are all that mark the dining area (x 50 to 62), which has its own FD1 at x 56. At x 62 the kitchen begins (x 62 to 80, y 17 to 40) with an 8 ft 0 in x 3 ft 6 in island, the hob counter along the north wall on y 17, a W1 at x 66.5 and an FD1 at x 74 to the veranda for the breakfast table.</p>
<h3>Zone D: service strip and the wet corner</h3>
<p>East of the alcove, the north band from x 62 to x 98 holds every service room against the north wall, on one plumbing line: store (x 62 to 72), utility (x 72 to 82, back door D4 at x 77 to the walled service yard), a wash lobby with two basins (x 82 to 88), and the {hl("wet corner")} at the north-east corner of the house (x 88 to 98). The wet corner is split by a 4½ in partition on y 6.5: the {hl("shared toilet")} takes the corner itself, with outside walls on the north and the east, and the {hl("shared bathroom")} with its walk-in shower sits directly below it on the east wall. Both open off the wash lobby through doors D3 on x 88, at y 3.25 and y 9.75. The wash lobby, store and utility open off a {hl("3 ft 6 in clear")} service passage on y 13 to 17. That passage starts at the dining area (x 62) and ends at x 90. The kitchen has its own door D3 into the passage at x 70, opposite the store and utility. None of these rooms is in the middle of the house: each has an outside wall and an outside window.</p>
<h3>Zone E: guest suite, east end</h3>
<p>A 9 in party wall on x 80 (y 17 to 40) separates kitchen from guest suite. The suite is entered from the end of the service passage through door D2 at x 85 into dressing 2 (x 80 to 90, y 17 to 24), which acts as a sound lobby. Bathroom 2 (x 90 to 98, y 13 to 24) is off the dressing, on the east outside wall, door at y 20.5. Bedroom 2 (x 80 to 98, y 24 to 40) is reached through door D2 at x 85 on y 24, has two W1 windows on the east wall at y 29 and 35.5 and an FD1 to the veranda at x 89.</p>
<h3>Zone F: resident suite, west end</h3>
<p>Behind the 9 in party wall on x 18, laid out exactly like the guest suite. Door D2 at y 17.5 on x 18 opens from the hall into dressing 1 (x 8 to 18, y 13 to 22), which acts as a sound lobby. Bathroom 1 (x 0 to 8, y 13 to 22) is off the dressing, on the west outside wall, with a W3 at y 17.5. Bedroom 1 (x 0 to 18, y 22 to 40) is reached through door D2 at x 13 on y 22. It has two W1 windows on the west wall at y 28 and 35 and an FD1 at x 9 to the veranda.</p>
<h3>Level changes</h3>
<p>FFL is one level throughout the house, {hl("+2 ft 6 in")} above finished ground at the porch. Bath, washroom, utility and store floors are set {hl("1 in")} lower with falls of 1 in 60 to floor traps, and shower areas a further ½ in lower behind a flush stone threshold, so there is no kerb to step over. The south veranda is at FFL less 1 in, falling 1 in 80 outwards. Because the ground falls about 2 ft 6 in from north to south across the house, the south veranda stands 5 ft 0 in above the garden and is reached by {hl("8 risers of 7½ in")} on 12 in treads, the full 18 ft 0 in width in front of the hall.</p>
"""

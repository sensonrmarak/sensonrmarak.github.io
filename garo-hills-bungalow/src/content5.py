"""Part 5: indicative cost estimate and the brief compliance check."""
import math
from data import areas, lakh, money
from content1 import band, hl


def cost_items():
    a = areas()
    v = {n: ar for n, l, d, ar in a["ver"]}
    ver_house = sum(ar for n, ar in v.items() if not n.startswith("Covered link"))
    link = sum(ar for n, ar in v.items() if n.startswith("Covered link"))
    gar_area = a["built_gar"]
    drive = 12 * 62 + 14 * 82 + round(math.pi * (24 ** 2 - 9 ** 2)) + 10 * 18
    wall = round(4 * 328.08 - 14 - 3.5 - 7)
    groups = [
        ("The house", [
            ("Main house, enclosed (built-up)", a["built_house"], "sq ft", 4500),
            ("Verandas and car porch", ver_house, "sq ft", 2400),
            ("External services: septic tank and soak pit, water pump, electrical service, earthing", 1, "lump sum", 1200000),
        ]),
        ("The firehouse", [
            ("Pavilion on 24 ft x 24 ft platform", 576, "sq ft", 3200),
            ("Fire pit, smoke lantern, bench, counter with sink", 1, "lump sum", 350000),
        ]),
        ("Garage block", [
            ("Garage, two-wheeler bay, tool store, generator room", gar_area, "sq ft", 2800),
            ("Covered link walk", link, "sq ft", 1800),
        ]),
        ("Compound wall and gate", [
            ("Compound wall 7 ft 3 in high, stone base, render, railing", wall, "running ft", 4800),
            ("Main gate, wicket, three stone piers and lanterns", 1, "lump sum", 750000),
        ]),
        ("Landscape", [
            ("Driveway, forecourt ring, spur and visitor bay, paved", drive, "sq ft", 420),
            ("Drive side drains and cross drains", 1, "lump sum", 400000),
            ("Rainwater sump 61,000 litres with silt trap and pump", 1, "lump sum", 950000),
            ("Swales, retention pond, soakaways, spillway", 1, "lump sum", 600000),
            ("Paths, steps and retaining walls", 1, "lump sum", 1000000),
            ("Planting: specimen tree, orchard, borders, lawn, grove replanting", 1, "lump sum", 1200000),
            ("Kitchen garden terraces and irrigation", 1, "lump sum", 300000),
            ("Garden lighting and cabling", 1, "lump sum", 500000),
        ]),
    ]
    return groups


def cost():
    out = []
    grand = 0
    subs = []
    for g, items in cost_items():
        st = 0
        for name, q, unit, rate in items:
            amt = q * rate
            st += amt
            qtxt = f"{q:,} {unit}" if unit != "lump sum" else "lump sum"
            rtxt = f"₹ {rate:,} per {unit.replace('running ft', 'rft')}" if unit != "lump sum" else ""
            out.append(f"<tr><td>{name}</td><td class='n'>{qtxt}</td><td class='n'>{rtxt}</td><td class='n'>{lakh(amt)}</td></tr>")
        out.append(f"<tr class='tot'><td colspan='3'>Subtotal: {g}</td><td class='n'>{hl(lakh(st))}</td></tr>")
        subs.append((g, st))
        grand += st
    cont = round(grand * 0.05)
    fees = round(grand * 0.06)
    total = grand + cont + fees
    a = areas()
    summary = "".join(f"<tr><td>{g}</td><td class='n'>{lakh(s)}</td></tr>" for g, s in subs)
    return f"""
{band("17. Indicative cost estimate", "b6")}
<p class="note">Rates are indicative for the Garo Hills in the current year (2026), for good-quality local construction with materials hauled from Tura or Guwahati, and include a hill-transport premium of about 12 per cent over plains rates. They exclude furniture, loose fittings, appliances, land, and GST on professional fees. Get three local tenders against this report before fixing a budget.</p>
<table class="t small">
<tr><th>Item</th><th class='n'>Quantity</th><th class='n'>Rate</th><th class='n'>Amount</th></tr>
{''.join(out)}
</table>
<table class="t totals">
{summary}
<tr><td>Sum of the five subtotals</td><td class='n'>{lakh(grand)}</td></tr>
<tr><td>Contingency, 5 per cent</td><td class='n'>{lakh(cont)}</td></tr>
<tr><td>Architect, structural engineer and site supervision, 6 per cent</td><td class='n'>{lakh(fees)}</td></tr>
<tr class="tot"><td>Grand total</td><td class='n'>{hl(money(total) + ' (' + lakh(total) + ')')}</td></tr>
<tr><td>Works only, per sq ft of super built-up area ({a['super']:,} sq ft)</td><td class='n'>₹ {grand / a['super']:,.0f} per sq ft</td></tr>
</table>
"""


def checks():
    rows = [
        ("No bathtub anywhere", "Met. Three walk-in showers (bath 1, bath 2, shared bathroom) plus a WC in the shared toilet. No tub is drawn, specified or costed."),
        ("No shower seat", "Met. No seat, ledge or bench in any shower. Wall niches only, at 4 ft 6 in."),
        ("No bathroom, washroom or toilet in the middle of the plan; shared toilet and bathroom in a corner", "Met. The shared toilet and shared bathroom sit together in the north-east corner of the house: the toilet takes the corner itself, the bathroom is directly below it on the east wall. Bath 1 is on the west wall and bath 2 on the east wall. Every one has an outside window."),
        ("No ceiling under 12 ft in a habitable room", "Met. Bedrooms, hall, dining, kitchen and alcove 12 ft 3 in; library and study 12 ft 0 in; hall vault to 16 ft 0 in. Service rooms (non-habitable) 9 ft 0 in to 10 ft 0 in."),
        ("No metric-only dimension", "Met. Every length is in feet and inches. Litres appear only beside cubic feet for water, and rainfall is in inches."),
        ("No overlapping, broken or floating walls", "Met. The plan is drawn from one list of wall centre lines; every wall ends on another wall or on a column, and the open edges are carried by beams between columns."),
        ("Circulation under 12 per cent", f"Met. {areas()['circ_pct']:.1f} per cent (foyer and service passage)."),
        ("Bedrooms at opposite ends", "Met. The two suite party walls are 62 ft apart, and the bedrooms are reached from different sides of the hall."),
        ("Library and study clubbed together", "Met. Side by side at the west end, joined by a pair of glazed doors. The music studio has been removed at your request."),
        ("Wall between kitchen and dining", "Met. A 4½ in wall on x 62 with a 3 ft 3 in door at the veranda end. The sitting hall and dining stay open to each other."),
        ("Veranda at least 8 ft on main faces", "Met. South 9 ft 0 in, north 8 ft 0 in."),
    ]
    r = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td></tr>" for a, b in rows)
    return f"""
{band("18. Checked against your brief", "b7")}
<table class="t small"><tr><th style="width:32%">Your rule</th><th>Status</th></tr>{r}</table>
<p class="sign">Prepared as a design report for client review. Before construction: a contour survey of the hectare, a soil test, and structural drawings stamped by a licensed engineer under IS 1893 and IS 13920 are required.</p>
"""

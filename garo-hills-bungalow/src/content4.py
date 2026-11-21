"""Part 4: firehouse, garage and approach, landscape and water, gate and wall."""
from data import rain, TANK
from content1 import band, hl
import svg_elev, svg_plan, svg_site


def firehouse():
    return f"""
{band("12. The firehouse", "b1")}
<figure class="dwgfig">{svg_elev.firehouse()}</figure>
<ul>
<li><b>Position</b>: on the axis of the sitting hall, 36 ft south of the veranda steps, reached by a 6 ft 0 in wide stone path across the lawn. Platform {hl("24 ft 0 in x 24 ft 0 in")}, 1 ft 6 in above the lawn, 3 risers of 6 in.</li>
<li><b>Frame</b>: 6 columns 12 in x 12 in, white rendered, at the corners and the middle of the east and west sides, on {hl("20 ft 0 in x 20 ft 0 in")} centres; ring beam at +9 ft 6 in. Roof 25° hipped, charcoal standing seam, {hl("3 ft 0 in")} overhang all round, so rain blown at 30° still stops at the platform edge.</li>
<li><b>Back wall</b>: 9 in stone-faced wall on the south side, facing the south-west monsoon wind, stone to +3 ft 0 in and cream render above.</li>
<li><b>Fire pit</b>: {hl("4 ft 0 in")} inside diameter, firebrick lined, set in a stone kerb 9 in wide and {hl("1 ft 6 in")} high (outer diameter 5 ft 6 in), on a 6 in gravel drain bed with a 3 in outlet so rain cannot pool in the ash.</li>
<li><b>Smoke</b>: open apex with a louvred lantern 3 ft 0 in square, rising 2 ft 6 in above the roof, top at +17 ft 6 in. The fire is 7 ft 6 in clear of the bench and 8 ft 0 in below the ceiling boards, which are fire-retardant treated.</li>
<li><b>Seating</b>: fixed bench in 2 in hardwood on a stone plinth, 1 ft 6 in deep, seat at 1 ft 5 in, set on a 240° arc of 8 ft 3 in radius from the pit centre, {hl("34 ft long, seats 10")} at 3 ft each. The open 120° faces the house.</li>
<li><b>Service counter</b>: 5 ft 0 in x 2 ft 0 in, top at 3 ft 0 in, local granite, with a 15 in bar sink and a covered power point, in the south-west corner against the back wall. Water and drain run in a duct from the kitchen garden line.</li>
</ul>
"""


def garage():
    return f"""
{band("13. Garage, studio block and approach", "b2")}
<figure class="dwgfig">{svg_plan.garage_plan()}</figure>
<ul>
<li><b>Garage</b>: two cars, {hl("20 ft 3 in x 22 ft 6 in")} clear, sectional door GD1 16 ft 0 in x 7 ft 6 in. <b>Two-wheeler bay</b> 8 ft 6 in x 22 ft 3 in. <b>Tool, garden kit and fuel store</b> {hl("10 ft 3 in x 12 ft 6 in")}, with its own outside door, fuel kept in a ventilated steel cabinet against the outer wall.</li>
<li><b>Music studio</b> at the east end: shell 16 ft 3 in x 18 ft 3 in, inside its independent lining {hl("15 ft 3 in x 17 ft 3 in")} (bettered from 14 x 16 so a grand piano and a drum kit fit together). Floating floor, two splayed walls and a splayed ceiling so no two surfaces are parallel, and a {hl("double-door airlock")} (SD1 + SD1) through the 10 ft 3 in x 9 ft 6 in gear lobby. About 80 ft from bedroom 2.</li>
<li><b>Porch</b>: the car porch at the front door, 20 ft 0 in x 14 ft 0 in, 11 ft 0 in clear height, so you step from the car to the veranda under cover.</li>
<li><b>Covered link</b>: a 6 ft 0 in wide covered walk from the airlock door to the east end of the north veranda, 88 ft long, so garage, studio and front door are all connected in the rain. It also screens the service yard from the approach.</li>
<li><b>Driveway</b>: {hl("12 ft 0 in")} wide, 3 in interlocking concrete pavers on 2 in sand bed on 6 in compacted granular sub-base and 6 in hard core; laid along the contour where possible, steepest grade 1 in 12. {hl("Camber 1 in 50")} from the centre line. Both sides have an open stone-lined drain {hl("12 in wide x 15 in deep")} with a cross drain of 9 in pipe every 60 ft on the slope; pavers are edged with 6 in x 12 in stone kerbs.</li>
<li><b>Turning</b>: the forecourt is a ring of {hl("48 ft 0 in outer diameter")} round an 18 ft 0 in planted island, giving a 15 ft 0 in lane. A car needs an outer turning radius of about 18 ft 0 in; the ring gives 24 ft 0 in, so any car or a small van turns without reversing. Visitor hard standing: {hl("10 ft 0 in x 18 ft 0 in")} beside the ring.</li>
</ul>
"""


def landscape():
    r = rain()
    return f"""
{band("14. Landscape: the larger half of the project", "b3")}
<figure class="dwgfig">{svg_site.site_plan()}</figure>
<h3>The zones</h3>
<table class="t small">
<tr><th style="width:18%">Zone</th><th>What happens there</th></tr>
<tr><td><b>Arrival</b></td><td>Wrought iron gate in the middle of the north boundary; a straight drive of 60 ft to the forecourt ring; a specimen <b>Champak</b> (<i>Magnolia champaca</i>, scented, evergreen, native to the North East) in the centre of the ring as the tree that announces the house; low clipped hedges of <i>Murraya</i> along the drive.</td></tr>
<tr><td><b>Private garden</b></td><td>The ground between the south veranda and the firehouse: a lawn of local carpet grass 60 ft wide, edged by borders of ginger lily, hydrangea and camellia, with two <i>Michelia</i> trees for evening shade. Low path lights only, so stars are visible from the firehouse.</td></tr>
<tr><td><b>Productive</b></td><td>Kitchen garden east of the firehouse on terraces 18 in high: local leafy greens (mustard, amaranth, <i>jaluk</i> and colocasia), chillies, ginger, turmeric, and pineapple on the lowest terrace. Below the third swale, an orchard of Khasi mandarin orange, jackfruit, areca, banana and Assam lemon, planted on contour at 20 ft spacing.</td></tr>
<tr><td><b>Grove and buffer</b></td><td>The west and east strips about 70 ft wide and the whole southern edge: native trees left or replanted (<i>Schima wallichii</i>, chestnut <i>Castanopsis</i>, <i>Gmelina</i>, wild fig, Indian rosewood), with bamboo clumps on the north-west for a wind screen. Cut once a year; no lawn, no watering.</td></tr>
<tr><td><b>Water</b></td><td>See below. Three swales follow the contour; a retention pond and soakaways sit in the lower grove.</td></tr>
</table>
<h3>Water and the cloudburst route</h3>
<p>Rainwater sump: underground RCC tank {hl(f"{TANK['l']} ft 0 in x {TANK['b']} ft 0 in x {TANK['depth']} ft 0 in water depth")} = {r['vol']:,} cu ft = {hl(f"{r['litres']:,.0f} litres")}. At 400 litres a day for one resident, guests and the kitchen garden in the dry months, that is {r['days']:.0f} days, which covers November to March, the dry season. The roofs fill it with only {r['fill_in']:.1f} in of rain; the year's rain off the roofs is about {r['annual_litres']/1e5:.1f} lakh litres, so most of it goes on to recharge the ground.</p>
<p><b>In a cloudburst</b>: roofs to gutters to downpipes to the 6 in storm line, then to a 3 ft x 3 ft silt trap and the sump. When the sump is full, the overflow and all paved-area run-off go to the first swale (2 ft 0 in wide x 1 ft 6 in deep, on contour, with a 1 ft 0 in bund on the downhill side), which spreads it along the slope. The swales step down to the retention pond (about 44 ft x 24 ft, 4 ft 0 in deep), then to two soakaway pits 6 ft 0 in diameter x 8 ft 0 in deep filled with graded stone, and finally through a stone-lined spillway to the natural stream on the south boundary. Nothing is sent to the neighbours or across the drive.</p>
<h3>Four-season planting note</h3>
<table class="t small">
<tr><th>Season</th><th>Colour and scent</th></tr>
<tr><td><b>Winter</b> (Dec to Feb, dry, cool)</td><td>Khasi mandarins ripening orange; camellia and poinsettia in flower; wild Himalayan cherry (<i>Prunus cerasoides</i>) pink in the grove; scent of <i>Murraya</i> along the drive.</td></tr>
<tr><td><b>Spring</b> (Mar to Apr, short, bright)</td><td>Rhododendron arboreum and orchid trees (<i>Bauhinia</i>) in the borders; the champak starts to flower; new pale leaves on the chestnut grove.</td></tr>
<tr><td><b>Monsoon</b> (May to Sep, very wet)</td><td>Ginger lily (<i>Hedychium</i>, intensely scented), hydrangeas, heliconia, wild ferns and mosses; jackfruit and pineapple harvest; champak scent at its height.</td></tr>
<tr><td><b>Autumn</b> (Oct to Nov, mild)</td><td>Night jasmine (<i>Nyctanthes</i>, <i>shiuli</i>) scenting the veranda; tree marigolds; areca and banana fruiting; the grass at its greenest.</td></tr>
</table>
<h3>Lighting, paths, steps and retaining walls</h3>
<table class="t small">
<tr><th>Item</th><th>Material and size</th></tr>
<tr><td>Garden paths</td><td>Flamed local stone 2 in thick, 4 ft 0 in wide (6 ft 0 in to the firehouse), on 4 in lean concrete, falls 1 in 40 to one side</td></tr>
<tr><td>Garden steps</td><td>Solid stone blocks, risers 6 in, treads 15 in, landings every 10 risers, 4 ft 0 in wide</td></tr>
<tr><td>Retaining walls (terraces and house platform)</td><td>Dry stone walls up to 3 ft 0 in high, battered 1 in 6, 18 in thick at top; above 3 ft 0 in, RCC cantilever wall with stone facing and 3 in weep holes at 5 ft 0 in centres on two rows</td></tr>
<tr><td>Path and step lights</td><td>Low bollards 2 ft 6 in high, warm white 2,700 K LED, 12 ft 0 in apart; step lights recessed in risers every third step</td></tr>
<tr><td>Feature lights</td><td>Uplight on the champak; two wall lanterns on the gate piers and two on the porch columns; one lantern hanging in the porch</td></tr>
</table>
"""


def roof_and_gate():
    return f"""
{band("15. Roof drainage plan", "b4")}
<figure class="dwgfig">{svg_site.roof_plan()}</figure>
{band("16. Main gate and compound wall", "b5")}
<figure class="dwgfig">{svg_elev.gate()}</figure>
<ul>
<li><b>Main gate</b>: ornamental wrought iron in the same black as the windows, {hl("14 ft 0 in clear")} in two leaves of 7 ft 0 in, leaves 7 ft 6 in high at the hinge rising in an arc to 9 ft 0 in at the meeting stile. Frame 2 in x 2 in hollow section; {hl("bars 1 in square at 4 in clear (5 in centres)")} with spear finials; lower panel to 2 ft 0 in with intermediate dog bars at 2 in clear; a band of C-scrolls between the 6 ft 0 in rail and the top rail. Hung on heavy pin hinges with a ground bolt and a central drop latch.</li>
<li><b>Wicket</b>: {hl("3 ft 6 in")} clear x 7 ft 0 in, same bar pattern, beside the main gate between its own pier and the east main pier, self-closing.</li>
<li><b>Piers</b>: 2 ft 6 in square (wicket pier 2 ft 0 in), {hl("9 ft 6 in")} high, stone clad, with a stone cap and a black lantern on each.</li>
<li><b>Compound wall</b>: total height {hl("7 ft 3 in")}: stone base 2 ft 6 in, rendered brick 2 ft 6 in, a 3 in stone coping weathered to the outside with a throated drip, and a 2 ft 0 in black iron railing of ¾ in square bars at 4¼ in clear. Piers every 10 ft 0 in; footing 2 ft 6 in wide at 3 ft 0 in depth; 3 in weep holes at 6 ft 0 in centres at ground level so the wall never dams the hill water.</li>
</ul>
"""

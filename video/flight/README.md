# How an aircraft flies — Modus & Raison

A 6 min 53 s explainer, written entirely in code (three.js 3D, rendered frame by frame).

## Files

| File | What it is |
|---|---|
| `out/how-aircraft-fly-4k.mp4` | Final video, 3840×2160, 24 fps, narration + music |
| `out/stills/*.png` | 13 key frames as 2560×1440 PNG graphics |
| `script.json` | Narration script, scene by scene |
| `timings.json` | Scene and sentence timings measured from the narration audio |
| `film.html`, `film.js`, `model.js` | The film: scenes, overlays and the 3D aircraft |
| `build_audio.py` | Narration (Piper TTS), music bed and mix |
| `render.js`, `stills.js`, `snap.js` | 4K renderer, PNG stills, preview contact sheets |

To re-render: serve `video/` on port 8765 (`python3 -m http.server 8765`), then `node flight/render.js 4 24`. Preview in a browser at `http://localhost:8765/flight/film.html?play`.

## Chapters

1. Hook — 79 tonnes, nothing holding it up
2. The four forces — weight, lift, thrust, drag
3. How a wing makes lift — airfoil, angle of attack, downwash, pressure
4. A famous myth — "equal transit time"
5. How much lift? — the lift equation, liftoff speed
6. The stall
7. Thrust — the turbofan: suck, squeeze, bang, blow; bypass air
8. Beating drag — streamlining, sweep, winglets
9. Steering — roll, pitch, yaw; flaps, slats, spoilers
10. Every part, section by section (below)
11. One flight, start to finish — takeoff, climb, cruise, jet stream, GAGAN, descent, landing
12. The whole picture — mind map
13. End card — banner, like, subscribe

## Every visible part, in nine sections

| # | Section | Parts | Shape | Colour (in the video) | Material (real aircraft) |
|---|---|---|---|---|---|
| 1 | Nose and cockpit | Radome, weather radar, windshield (6 panes), flight deck, pitot probes | Rounded, pointed cone | White skin, light-grey radome, dark tinted glass | Glass-fibre composite radome (radar passes through it); laminated glass and acrylic windshield |
| 2 | Fuselage | Pressure cabin, passenger and cargo doors, windows, cargo hold, frames and stringers, belly fairing | Long tube about 4 m wide, tapering to an upswept tail cone | White with a gold cheatline, dark windows | Aluminium alloy (A320); carbon-fibre composite (787, A350) |
| 3 | Wings | Wing box, spars, ribs, skin panels, winglets | Swept back about 25°, tapered, airfoil cross-section, tips turned up | Light grey, gold winglets | Aluminium alloy; carbon-fibre composite on newer jets |
| 4 | Moving surfaces | Slats (front edge), flaps (rear edge), ailerons (outer rear edge), spoilers (top) | Thin hinged panels along both wing edges | Mid grey | Mostly carbon-fibre composite |
| 5 | Engines | Nacelle (cowl), intake lip, fan and spinner, compressor, combustor, turbine, exhaust nozzle, pylon | Barrel; fan about 2 m across (LEAP-1A) | Navy cowl, silver lip, dark fan, white pylon | Carbon-composite fan blades with titanium leading edges; nickel superalloy turbine |
| 6 | Tail (empennage) | Vertical fin, rudder, horizontal stabiliser, elevators, APU in the tail cone | Swept fins, like small wings | Navy fin with a gold band, gold rudder, grey stabiliser | Carbon-fibre composite |
| 7 | Landing gear | Nose gear (2 wheels), main gear (2 × 2 wheels), shock struts, brakes | Telescopic struts with wheels; folds into the belly | Silver struts and hubs, black tyres | High-strength steel and titanium; carbon brakes; rubber tyres |
| 8 | Fuel tanks | Left and right wing tanks, centre tank, pumps and pipes | The hollow inside of the wing itself | Shown in translucent blue | Sealed aluminium wing structure; Jet A-1 kerosene, about 24,000 litres (A320) |
| 9 | Hidden systems | Hydraulics (3 circuits), electrical generators, avionics, fly-by-wire computers, air conditioning | Pipes, cables and boxes under the floor | Shown in gold (hydraulics), blue (electrics), green (avionics) | Titanium and steel pipes; copper and aluminium wiring |

## Facts and sources

| Fact used in the video | Source |
|---|---|
| Four forces of flight: lift, weight, thrust, drag | NASA Glenn Research Center, Beginner's Guide to Aeronautics |
| Lift equation L = C<sub>L</sub> × ½ρV² × A | NASA Glenn, "Lift Equation" |
| "Equal transit time" is an incorrect theory; lift comes from turning the flow | NASA Glenn, "Incorrect Lift Theory" |
| The fan generates the bulk of a turbofan's thrust | NASA (HyTEC project article); NASA Glenn turbofan pages |
| LEAP-1A bypass ratio about 11:1, fan about 2 m (78 in) | CFM International |
| A320neo: 79 t maximum takeoff weight, 35.8 m wingspan | Airbus A320 Family facts and figures |
| Sharklets cut fuel burn by up to 4% | Airbus |
| Boeing 787 airframe: about 50% composite, 20% aluminium, 15% titanium, 10% steel, 5% other, by weight | Boeing (AERO magazine) |
| About 5 billion passengers expected in 2026 | IATA outlook (5.2 billion forecast in Dec 2025; reports of a revision to 5.1 billion in June 2026) |
| At 35,000 ft: about −54 °C, air density about 31% of sea level | ICAO Standard Atmosphere |
| Jet stream core winds of the order of 150 knots at 12.6 km over northwest India | India Meteorological Department press release, 4 January 2026 |
| GAGAN, built by ISRO and AAI, certified for APV-1 approaches on 21 April 2015 | ISRO / Airports Authority of India / DGCA |
| Critical angle of attack about 15° for a typical airfoil; liftoff around 270 km/h for an A320-class jet | FAA Pilot's Handbook of Aeronautical Knowledge; typical type figures (rounded) |

NASA's own pages could not be opened from the build environment (the host was blocked), so NASA wording was taken from search results quoting those pages.

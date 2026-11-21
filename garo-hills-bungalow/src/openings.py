"""Door and window positions (centre of opening, CL coordinates in feet)."""
from fractions import Fraction as F

# mark -> type, material, clear width (in), clear height (in), sill (in), lintel (in), glazing, hardware
SCHEDULE = {
    "D1": ("Main entrance door, single leaf", "Seasoned teak or local hollock, dark oil finish, 2 in thick panelled", 48, 96, 0, 96,
           "Two vision panels, 6 mm toughened, reeded", "Brass mortice lock, 5-lever; 3 pairs heavy butt hinges; long pull handle; door closer"),
    "SL1": ("Fixed side light to main door", "Same hardwood frame as D1", 18, 96, 0, 96,
            "8 mm toughened, reeded", "None, fixed"),
    "FD1": ("French door, two leaves, opening out to veranda", "Black powder-coated aluminium, slim 2 in sight line", 60, 96, 0, 96,
            "6 mm toughened, clear; lower panel laminated 6.38 mm", "Multipoint lock, tower bolts, wind hooks, mosquito mesh shutter"),
    "D2": ("Room door, single leaf", "Flush hardwood-veneered, 1.5 in, dark stain, in hardwood frame", 39, 96, 0, 96,
           "None", "Mortice lock with lever handle, 3 butt hinges, door stop"),
    "D3": ("Bath / service door, single leaf", "WPC solid core, hardwood veneer, dark stain", 33, 84, 0, 96,
           "Top glass louvre 12 in for ventilation", "Privacy latch, 3 SS hinges, door stop"),
    "D4": ("Utility back door to service yard", "Hardwood ledged frame with MS grille, dark", 36, 90, 0, 96,
           "Upper half 6 mm wired glass", "Barrel bolts inside, padlock hasp outside"),
    "SD1": ("Studio acoustic door (one each side of airlock)", "Solid-core hardwood, 2.5 in, perimeter seals and drop seal", 42, 90, 0, 96,
            "Double-glazed vision panel 9 in x 24 in", "Lift-off hinges, compression latches, automatic drop seal"),
    "W1": ("Tall casement window with fixed clerestory above lintel", "Black powder-coated aluminium, slim frame", 42, 78, 18, 96,
           "6 mm toughened clear; mosquito mesh to opening sashes", "Friction stays, multipoint handle; lower sashes open for cross ventilation"),
    "V1": ("Clerestory top-hung vent above every W1 and FD1", "Black powder-coated aluminium", 42, 24, 108, 132,
           "6 mm toughened clear", "Top-hung, chain winder with pole"),
    "W2": ("North-light library window, tall", "Black powder-coated aluminium", 42, 84, 12, 96,
           "6 mm low-iron clear, UV film", "Side-hung lower sash, fixed upper"),
    "W3": ("Bath / service window, high", "Black powder-coated aluminium", 30, 36, 60, 96,
           "5 mm frosted toughened, louvred top third", "Top-hung with stay"),
    "GD1": ("Garage door, sectional overhead", "Insulated steel, charcoal", 192, 90, 0, 96, "None", "Motorised, manual override"),
    "GD2": ("Two-wheeler bay opening", "Open, MS grille gate in black", 84, 90, 0, 96, "None", "Sliding grille with padlock"),
}

# (mark, orientation of host wall 'h' or 'v', fixed coord, centre along wall, opens to side +1/-1)
MAIN = [
    # north face y = 0
    ("W3", "h", 0, 4, 1), ("W3", "h", 0, 13, 1),
    ("W2", "h", 0, 22.5, 1), ("W2", "h", 0, 27.5, 1),
    ("W1", "h", 0, 35.5, 1), ("D1", "h", 0, 41, 1), ("SL1", "h", 0, 44, 1), ("W1", "h", 0, 47.5, 1),
    ("W1", "h", 0, 56, 1), ("W3", "h", 0, 67, 1), ("D4", "h", 0, 76, 1),
    ("W3", "h", 0, 83, 1), ("W3", "h", 0, 92, 1),
    # south face y = 40
    ("FD1", "h", 40, 9, -1), ("FD1", "h", 40, 25, -1), ("W1", "h", 40, 30, -1),
    ("W1", "h", 40, 38, -1), ("FD1", "h", 40, 43, -1), ("FD1", "h", 40, 56, -1),
    ("W1", "h", 40, 66.5, -1), ("FD1", "h", 40, 74, -1), ("FD1", "h", 40, 89, -1),
    # west face x = 0
    ("W1", "v", 0, 21, 1), ("W1", "v", 0, 32, 1), ("W3", "v", 0, 6.5, 1),
    # east face x = 98
    ("W3", "v", 98, 6.5, -1), ("W3", "v", 98, 18.5, -1), ("W1", "v", 98, 29, -1), ("W1", "v", 98, 35.5, -1),
    # internal doors
    ("D2", "v", 18, 16, -1), ("D2", "h", 13, 13, -1), ("D3", "v", 8, 6.5, -1),
    ("D2", "h", 13, 29, -1), ("D3", "h", 13, 67, -1), ("D3", "h", 13, 76, -1),
    ("D3", "h", 13, 83, -1), ("D3", "h", 13, 88, -1), ("D3", "h", 17, 70, 1),
    ("D2", "h", 17, 85, 1), ("D3", "v", 90, 20.5, 1), ("D2", "h", 24, 85, 1),
]

GARAGE = [("GD1", "h", 0, 10.5, 1), ("GD2", "h", 0, 25.5, 1), ("D4", "h", 0, 35.5, 1),
          ("SD1", "h", 23, 35.5, 1), ("SD1", "v", 41, 16, 1), ("W3", "v", 58, 9.5, -1), ("W3", "v", 0, 11.5, 1)]


def counts():
    c = {}
    for m, *_ in MAIN + GARAGE:
        c[m] = c.get(m, 0) + 1
    # every W1 and FD1 carries a V1 clerestory above it
    c["V1"] = c.get("W1", 0) + c.get("FD1", 0)
    return c

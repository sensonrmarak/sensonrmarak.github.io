"""Door and window positions (centre of opening, CL coordinates) and schedule. All in feet."""

# mark -> type, material, clear width ft, clear height ft, sill ft, lintel ft, glazing, hardware
SCHEDULE = {
    "D1": ("Main entrance door, single leaf", "Local hardwood, dark oil finish, 0.15 ft thick, panelled", 4.0, 8.0, 0.0, 8.0,
           "One vision panel, toughened, reeded", "Mortice lock, 3 pairs butt hinges, pull handle"),
    "FD1": ("French door, two leaves, to the veranda", "Steel frame, black enamel", 5.0, 7.5, 0.0, 8.0,
            "Clear float glass; fixed vent fanlight 0.50 ft above", "Tower bolts, handles, mosquito mesh shutter"),
    "D2": ("Room door, single leaf", "Flush door, hardwood frame, dark stain", 3.0, 7.5, 0.0, 8.0,
           "Fixed vent fanlight 0.50 ft above", "Mortice lock with lever handle, 3 butt hinges"),
    "D3": ("Bath door, single leaf", "PVC or WPC door, hardwood frame", 2.5, 7.0, 0.0, 8.0,
           "Louvred fanlight 1.00 ft above for ventilation", "Privacy latch, 3 hinges"),
    "OP": ("Cased opening, no door", "Plastered reveal with timber lining", 3.0, 7.5, 0.0, 8.0, "None", "None"),
    "W1": ("Tall casement window", "Steel frame, black enamel", 3.0, 6.5, 1.5, 8.0,
           "Clear float glass, mosquito mesh to opening sashes", "Stays and handles; lower sashes open for cross ventilation"),
    "W3": ("High window to bath or lobby", "Steel frame, black enamel", 2.0, 3.0, 5.0, 8.0,
           "Frosted glass, louvred top third", "Top-hung with stay"),
}

# (mark, host wall orientation 'h' or 'v', fixed coordinate, centre along wall, opens to side +1/-1)
MAIN = [
    # north face y = 0
    ("W1", "h", 0, 4, 1), ("W1", "h", 0, 10, 1), ("W1", "h", 0, 17.5, 1), ("D1", "h", 0, 22, 1),
    ("W1", "h", 0, 26.5, 1), ("W3", "h", 0, 32, 1), ("W3", "h", 0, 40, 1),
    # south face y = 28
    ("FD1", "h", 28, 7, -1), ("FD1", "h", 28, 18.5, -1), ("FD1", "h", 28, 25.5, -1), ("FD1", "h", 28, 35.25, -1),
    # west face x = 0
    ("W1", "v", 0, 5, 1), ("W3", "v", 0, 13.5, 1), ("W1", "v", 0, 22.5, 1),
    # east face x = 46
    ("W3", "v", 46, 3.5, -1), ("W1", "v", 46, 11.5, -1), ("W3", "v", 46, 19, -1),
    # internal
    ("D2", "v", 14, 5, -1), ("D2", "v", 14, 13.5, -1), ("D3", "v", 6, 13.5, -1), ("D2", "h", 17, 10, 1),
    ("OP", "v", 30, 3.5, 1), ("D3", "v", 34, 3.5, 1), ("D2", "v", 30, 11.5, 1), ("D2", "v", 30, 19.5, 1),
    ("D3", "v", 40.5, 19, 1), ("OP", "v", 40.5, 25, 1),
]


def counts():
    c = {}
    for m, *_ in MAIN:
        c[m] = c.get(m, 0) + 1
    return c

"""Why the Earth's tilt causes seasons. Render:
    manimgx render seasons.py Seasons -r 1920x1080 --fps 30 -o seasons.mp4
"""
import numpy as np
import manimgx as m

TILT = np.radians(23.5)
AXIS = np.array([np.sin(TILT), np.cos(TILT), 0.0])     # the axis always points the same way in space
SUN_POS = np.array([0.0, -0.4, 0.0])
ORBIT_W, ORBIT_H = 9.0, 3.4
EARTH_R = 0.34


def orbit_point(a: float) -> np.ndarray:
    return SUN_POS + np.array([ORBIT_W / 2 * np.cos(a), ORBIT_H / 2 * np.sin(a), 0.0])


def earth_at(p: np.ndarray) -> m.VGroup:
    to_sun = SUN_POS - p
    ang = np.arctan2(to_sun[1], to_sun[0])
    night = m.Circle(radius=EARTH_R, color=m.BLUE_E, fill_opacity=1, stroke_width=2).move_to(p)
    day = m.Sector(radius=EARTH_R, angle=np.pi, start_angle=ang - np.pi / 2,
                   color=m.BLUE_B, fill_opacity=1, stroke_width=0).shift(p)
    equator = m.Line(p - EARTH_R * np.array([AXIS[1], -AXIS[0], 0]), p + EARTH_R * np.array([AXIS[1], -AXIS[0], 0]),
                     color=m.GREEN_B, stroke_width=2)
    axis = m.Line(p - 0.62 * AXIS, p + 0.62 * AXIS, color=m.WHITE, stroke_width=3)
    n = m.Text("N", font_size=20).move_to(p + 0.62 * AXIS + np.array([-0.2 * np.sign(to_sun[0] or 1), 0.0, 0]))
    return m.VGroup(night, day, equator, axis, n)


class Seasons(m.Scene):
    def construct(self) -> None:
        title = m.Text("Why does Earth's tilt cause seasons?", font_size=44).to_edge(m.UP)
        self.play(m.Write(title))

        # ---- the orbit, with an axis that never changes direction ----
        orbit = m.Ellipse(width=ORBIT_W, height=ORBIT_H, color=m.GREY_B, stroke_width=2).move_to(SUN_POS)
        glow = m.Circle(radius=0.85, color=m.YELLOW, fill_opacity=0.18, stroke_width=0).move_to(SUN_POS)
        sun = m.Circle(radius=0.55, color=m.YELLOW, fill_opacity=1).move_to(SUN_POS)
        sun_lbl = m.Text("Sun", font_size=24, color=m.BLACK).move_to(SUN_POS)
        self.play(m.Create(orbit), m.FadeIn(glow, sun, sun_lbl))

        t = m.ValueTracker(np.pi)            # start on the left: June
        earth = m.always_redraw(lambda: earth_at(orbit_point(t.get_value())))
        self.play(m.FadeIn(earth))
        tilt_note = m.Text("Earth's axis is tilted 23.5° and always points the same way", font_size=26).to_edge(m.DOWN)
        self.play(m.Write(tilt_note))
        self.wait(1.5)

        june = m.Text("June: the North tilts TOWARD the Sun\nSummer in the north, winter in the south",
                      font_size=26, color=m.YELLOW).to_edge(m.DOWN)
        self.play(m.ReplacementTransform(tilt_note, june))
        self.play(m.Indicate(earth, scale_factor=1.15))
        self.wait(2)

        self.play(m.FadeOut(june))
        self.play(t.animate.set_value(2 * np.pi), run_time=4, rate_func=m.linear)
        dec = m.Text("December: the North tilts AWAY from the Sun\nWinter in the north, summer in the south",
                     font_size=26, color=m.BLUE_B).to_edge(m.DOWN)
        self.play(m.Write(dec))
        self.play(m.Indicate(earth, scale_factor=1.15))
        self.wait(2)

        myth = m.Text("It's NOT distance: Earth is closest to the Sun in early January!",
                      font_size=26, color=m.RED_B).to_edge(m.DOWN)
        self.play(m.ReplacementTransform(dec, myth))
        self.play(t.animate.set_value(3 * np.pi), run_time=4, rate_func=m.linear)
        self.wait(1.5)
        self.play(m.FadeOut(orbit, glow, sun, sun_lbl, earth, myth))

        # ---- why the angle matters: the same sunlight, spread over more ground ----
        sub = m.Text("The same sunlight, at two angles", font_size=34).next_to(title, m.DOWN, buff=0.4)
        self.play(m.Write(sub))

        def beam(center_x: float, angle_deg: float, colour) -> m.VGroup:
            ground_y = -2.2
            a = np.radians(angle_deg)                       # angle of the sun above the horizon
            width = 1.2                                     # beam width
            spread = width / np.sin(a)                      # length of ground it covers
            d = np.array([np.cos(a), np.sin(a), 0])         # direction back toward the sun
            left = np.array([center_x - spread / 2, ground_y, 0])
            right = np.array([center_x + spread / 2, ground_y, 0])
            far = 3.0
            poly = m.Polygon(left, right, right + far * d, left + far * d, color=m.YELLOW,
                             fill_opacity=0.35, stroke_width=1)
            patch = m.Line(left, right, color=colour, stroke_width=12)
            ground = m.Line([center_x - 2.0, ground_y, 0], [center_x + 2.0, ground_y, 0], color=m.GREY_B)
            return m.VGroup(poly, ground, patch)

        summer = beam(-4.0, 75, m.ORANGE)
        winter = beam(2.0, 28, m.BLUE_B)
        s_lbl = m.Text("Summer: high Sun\nsmall patch, strong heating", font_size=24, color=m.ORANGE).next_to(summer, m.DOWN, buff=0.25)
        w_lbl = m.Text("Winter: low Sun\nspread out, weak heating", font_size=24, color=m.BLUE_B).next_to(winter, m.DOWN, buff=0.25)
        self.play(m.FadeIn(summer), m.FadeIn(winter))
        self.play(m.Write(s_lbl), m.Write(w_lbl))
        self.wait(3)
        self.play(m.FadeOut(summer, winter, s_lbl, w_lbl, sub))

        # ---- summary ----
        summary = m.VGroup(
            m.Text("Tilted toward the Sun:", font_size=32, color=m.YELLOW),
            m.Text("1. Sunlight hits more directly, so it heats more", font_size=28),
            m.Text("2. Days are longer, so there is more time to heat", font_size=28),
            m.Text("That's summer. Tilted away, it's winter.", font_size=32, color=m.BLUE_B),
        ).arrange(m.DOWN, buff=0.4).next_to(title, m.DOWN, buff=0.8)
        for line in summary:
            self.play(m.FadeIn(line, shift=0.2 * m.UP))
        self.wait(3)

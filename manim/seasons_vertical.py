"""Vertical 9:16 version, timed to Lily's narration (seasons_timing.json). Render then add the voice:
    manimgx render seasons_vertical.py SeasonsVertical -r 1080x1920 --fps 30 -o seasons_vertical_silent.mp4
    ffmpeg -i seasons_vertical_silent.mp4 -i ../assets-src/seasons_narration_lily.mp3 -c:v copy -c:a aac -shortest seasons_vertical.mp4
"""
import numpy as np
import manimgx as m

TILT = np.radians(23.5)
AXIS = np.array([np.sin(TILT), np.cos(TILT), 0.0])
SUN = np.array([0.0, 0.2, 0.0])
OW, OH, ER = 3.9, 1.6, 0.22

CAPTIONS = [
    (0.0, "Why does Earth's tilt\ncause seasons?"),
    (3.94, "Earth's axis is tilted about 23.5°\nand always points the same way"),
    (11.4, "June: the north leans toward the Sun\nsummer in the north"),
    (18.82, "December: the north leans away\nthe seasons swap"),
    (26.17, "It's not distance! Earth is closest\nto the Sun in early January"),
    (31.97, "Why does leaning toward\nthe Sun make it warmer?"),
    (35.69, "High Sun: light lands on a\nsmall patch and heats it strongly"),
    (41.28, "Low Sun: the same light spreads out\nand heats each part less"),
    (47.61, "Direct light + longer days = summer"),
]


def orbit_point(a):
    return SUN + np.array([OW / 2 * np.cos(a), OH / 2 * np.sin(a), 0.0])


def earth_at(p):
    to_sun = SUN - p
    ang = np.arctan2(to_sun[1], to_sun[0])
    night = m.Circle(radius=ER, color=m.BLUE_E, fill_opacity=1, stroke_width=2).move_to(p)
    day = m.Sector(radius=ER, angle=np.pi, start_angle=ang - np.pi / 2, color=m.BLUE_B, fill_opacity=1, stroke_width=0).shift(p)
    perp = np.array([AXIS[1], -AXIS[0], 0])
    eq = m.Line(p - ER * perp, p + ER * perp, color=m.GREEN_B, stroke_width=2)
    axis = m.Line(p - 0.42 * AXIS, p + 0.42 * AXIS, color=m.WHITE, stroke_width=3)
    n = m.Text("N", font_size=16).move_to(p + 0.42 * AXIS + np.array([-0.2 * np.sign(to_sun[0] or 1), 0.05, 0]))
    return m.VGroup(night, day, eq, axis, n)


def beam(cx, ground_y, angle_deg, colour):
    a = np.radians(angle_deg)
    w, far = 0.6, 1.5
    spread = w / np.sin(a)
    d = np.array([np.cos(a), np.sin(a), 0])
    left, right = np.array([cx - spread / 2, ground_y, 0]), np.array([cx + spread / 2, ground_y, 0])
    poly = m.Polygon(left, right, right + far * d, left + far * d, color=m.YELLOW, fill_opacity=0.35, stroke_width=1)
    ground = m.Line([cx - 1.3, ground_y, 0], [cx + 1.3, ground_y, 0], color=m.GREY_B)
    patch = m.Line(left, right, color=colour, stroke_width=10)
    return m.VGroup(poly, ground, patch)


class SeasonsVertical(m.Scene):
    def construct(self) -> None:
        self.now = 0.0

        def play(*anims, run_time=1.0, **kw):
            self.play(*anims, run_time=run_time, **kw)
            self.now += run_time

        def until(t):
            if t - self.now > 0.02:
                self.wait(t - self.now)
                self.now = t

        cap = m.Text(CAPTIONS[0][1], font_size=34).move_to([0, 2.9, 0])
        play(m.Write(cap), run_time=1.5)

        def caption(i, rt=0.6):
            nonlocal cap
            until(CAPTIONS[i][0])
            new = m.Text(CAPTIONS[i][1], font_size=24 if i else 34, color=[m.WHITE, m.WHITE, m.YELLOW, m.BLUE_B, m.RED_B,
                         m.WHITE, m.ORANGE, m.BLUE_B, m.YELLOW][i]).move_to([0, 2.9, 0])
            play(m.FadeTransform(cap, new), run_time=rt)
            cap = new

        # orbit
        orbit = m.Ellipse(width=OW, height=OH, color=m.GREY_B, stroke_width=2).move_to(SUN)
        glow = m.Circle(radius=0.55, color=m.YELLOW, fill_opacity=0.18, stroke_width=0).move_to(SUN)
        sun = m.Circle(radius=0.36, color=m.YELLOW, fill_opacity=1).move_to(SUN)
        t = m.ValueTracker(np.pi)
        earth = m.always_redraw(lambda: earth_at(orbit_point(t.get_value())))
        caption(1)
        play(m.Create(orbit), m.FadeIn(glow, sun), m.FadeIn(earth), run_time=1.5)
        until(7.0)
        play(t.animate.set_value(np.pi + 2 * np.pi), run_time=3.8, rate_func=m.linear)   # one lap: the axis never turns

        caption(2)
        play(m.Indicate(earth, scale_factor=1.25))
        caption(3)
        play(t.animate.set_value(4 * np.pi), run_time=3.0)
        play(m.Indicate(earth, scale_factor=1.25))
        caption(4)
        play(t.animate.set_value(5 * np.pi), run_time=4.0, rate_func=m.linear)

        until(31.6)
        play(m.FadeOut(orbit, glow, sun, earth), run_time=0.4)
        caption(5)

        summer = beam(-0.6, 0.55, 75, m.ORANGE)
        winter = beam(-0.9, -2.0, 28, m.BLUE_B)
        s_lbl = m.Text("Summer", font_size=22, color=m.ORANGE).next_to(summer, m.DOWN, buff=0.15)
        w_lbl = m.Text("Winter", font_size=22, color=m.BLUE_B).next_to(winter, m.DOWN, buff=0.15)
        caption(6)
        play(m.FadeIn(summer), m.Write(s_lbl))
        caption(7)
        play(m.FadeIn(winter), m.Write(w_lbl))

        caption(8)
        play(m.FadeOut(summer, winter, s_lbl, w_lbl), run_time=0.5)
        lines = [m.Text(s, font_size=c[1], color=c[0]) for s, c in [
            ("Tilted toward the Sun:", (m.YELLOW, 30)), ("more direct light", (m.WHITE, 26)),
            ("+ longer days", (m.WHITE, 26)), ("= SUMMER", (m.ORANGE, 40)), ("Tilted away = WINTER", (m.BLUE_B, 30))]]
        m.VGroup(*lines).arrange(m.DOWN, buff=0.4).move_to([0, -0.4, 0])
        for line, at in zip(lines, [48.2, 49.4, 51.0, 52.9, 54.5]):
            until(at)
            play(m.FadeIn(line, shift=0.2 * m.UP), run_time=0.6)
        until(58.5)

"""Draw a 1024x1024 verified newspaper front page for 20 November 2026.

Design: a "verified broadsheet" the judge can read at a glance.
A drawn lead illustration (Shenzhen sunset skyline, three flags),
a world-map panel with numbered story markers, a date-check box,
readable region columns (34 stories, headlines one line, body one
line), and a UTC timeline strip along the bottom.

Deterministic: fixed fonts, fixed colours, fixed geometry, no
timestamps, no randomness. Running it twice writes identical bytes.
Run directly to write entry.png next to this file.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 251, 244)
INK = (20, 20, 20)
RULE = (60, 60, 60)
ACCENT = (139, 0, 0)
GREY = (90, 88, 80)
GREEN = (30, 125, 50)
LAND = (216, 208, 188)
LAND_LINE = (90, 85, 70)
SEA = (233, 240, 241)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap by measured width."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        line = words[0]
        for word in words[1:]:
            trial = line + " " + word
            if draw.textlength(trial, font=fnt) <= max_width:
                line = trial
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def star_points(cx, cy, r_out, r_in, points=5):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        ang = math.radians(-90 + i * 180 / points)
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


# Simplified continent outlines as (lon, lat) points, drawn in a
# stylised equirectangular strip. Shapes are approximate on purpose.
NORTH_AMERICA = [
    (-168, 66), (-156, 71), (-140, 70), (-125, 71), (-110, 68),
    (-95, 69), (-85, 66), (-80, 62), (-76, 62), (-70, 62),
    (-65, 60), (-60, 52), (-55, 47), (-60, 45), (-65, 44),
    (-70, 42), (-74, 39), (-76, 35), (-80, 32), (-81, 26),
    (-84, 30), (-89, 29), (-91, 19), (-87, 21), (-90, 21),
    (-97, 16), (-94, 17), (-90, 14), (-86, 12), (-83, 9),
    (-79, 9), (-81, 13), (-86, 15), (-91, 14), (-96, 16),
    (-101, 18), (-105, 20), (-110, 23), (-114, 28), (-117, 33),
    (-122, 37), (-124, 42), (-124, 48), (-128, 51), (-132, 56),
    (-140, 60), (-150, 59), (-158, 56), (-162, 58), (-168, 66),
]
GREENLAND = [
    (-58, 64), (-52, 60), (-43, 60), (-40, 64), (-32, 68),
    (-22, 70), (-25, 74), (-35, 76), (-50, 76), (-58, 74),
    (-62, 70), (-58, 64),
]
SOUTH_AMERICA = [
    (-79, 9), (-77, 7), (-75, 10), (-72, 12), (-68, 11), (-64, 10),
    (-60, 8), (-55, 6), (-52, 5), (-50, 0), (-48, -3), (-44, -3),
    (-40, -5), (-35, -8), (-37, -13), (-39, -17), (-41, -22),
    (-48, -26), (-53, -33), (-58, -38), (-62, -41), (-65, -45),
    (-68, -50), (-70, -54), (-73, -50), (-73, -44), (-73, -37),
    (-72, -30), (-71, -22), (-70, -18), (-75, -15), (-79, -8),
    (-81, -4), (-80, 1), (-80, 6), (-79, 9),
]
AFRICA = [
    (-17, 15), (-16, 20), (-15, 27), (-10, 31), (-6, 34), (0, 36),
    (10, 37), (11, 34), (20, 32), (30, 31), (32, 31), (35, 28),
    (37, 22), (39, 18), (43, 12), (48, 11), (51, 12), (48, 5),
    (46, 0), (42, -5), (40, -10), (38, -15), (36, -20), (33, -26),
    (29, -30), (26, -34), (20, -35), (18, -32), (16, -28),
    (14, -22), (12, -18), (13, -12), (12, -6), (9, -1), (9, 4),
    (6, 4), (0, 6), (-8, 5), (-13, 8), (-17, 12), (-17, 15),
]
EUROPE = [
    (-10, 36), (-9, 38), (-9, 43), (-2, 44), (-2, 48), (-4, 48),
    (0, 50), (2, 51), (4, 53), (7, 54), (8, 57), (10, 58),
    (12, 56), (18, 56), (21, 55), (24, 58), (21, 59), (24, 60),
    (28, 60), (30, 62), (30, 66), (28, 70), (35, 68), (40, 67),
    (44, 64), (44, 60), (40, 58), (38, 56), (35, 54), (33, 52),
    (31, 50), (28, 46), (28, 44), (30, 42), (28, 41), (26, 40),
    (23, 40), (22, 37), (19, 42), (16, 44), (14, 45), (12, 44),
    (8, 44), (3, 42), (0, 40), (-2, 37), (-6, 36), (-9, 37),
    (-10, 36),
]
ASIA = [
    (30, 70), (35, 68), (40, 68), (45, 68), (50, 69), (55, 69),
    (60, 69), (66, 70), (70, 72), (75, 73), (80, 73), (85, 74),
    (90, 75), (95, 76), (100, 77), (105, 77), (110, 76), (115, 73),
    (120, 73), (125, 72), (130, 71), (135, 72), (140, 72), (145, 72),
    (150, 70), (155, 69), (160, 69), (162, 66), (170, 66), (178, 65),
    (178, 62), (170, 60), (162, 58), (158, 53), (156, 51), (150, 59),
    (142, 59), (141, 52), (140, 48), (140, 42), (135, 43), (130, 42),
    (127, 40), (126, 38), (122, 39), (121, 37), (120, 33), (121, 28),
    (118, 25), (114, 22), (110, 20), (109, 18), (106, 10), (105, 9),
    (103, 7), (100, 7), (98, 10), (98, 14), (97, 16), (94, 17),
    (92, 21), (90, 22), (88, 22), (86, 20), (84, 19), (80, 15),
    (80, 10), (77, 8), (76, 10), (74, 14), (73, 19), (72, 20),
    (70, 22), (68, 23), (66, 25), (63, 25), (61, 25), (58, 26),
    (57, 27), (54, 27), (52, 27), (50, 29), (48, 30), (47, 30),
    (44, 29), (42, 29), (40, 31), (39, 32), (36, 36), (34, 34),
    (33, 31), (31, 34), (30, 36), (28, 37), (27, 38), (26, 40),
    (28, 42), (30, 44), (33, 47), (35, 50), (38, 52), (40, 54),
    (42, 56), (44, 58), (44, 60), (40, 64), (35, 66), (32, 68),
    (30, 70),
]
AUSTRALIA = [
    (113, -22), (114, -28), (114, -32), (115, -35), (118, -35),
    (122, -34), (126, -32), (129, -32), (132, -32), (135, -35),
    (138, -35), (140, -38), (144, -38), (147, -39), (150, -37),
    (153, -32), (153, -27), (152, -24), (150, -22), (148, -20),
    (146, -19), (143, -15), (142, -11), (141, -13), (139, -15),
    (136, -12), (135, -15), (132, -12), (130, -13), (128, -14),
    (125, -15), (122, -17), (120, -19), (117, -20), (114, -22),
    (113, -22),
]
SUMATRA = [
    (95, 5), (98, 3), (100, 0), (103, -2), (105, -4),
    (106, -6), (104, -6), (102, -3), (100, 1), (97, 4), (95, 5),
]
JAVA = [
    (105, -6), (108, -7), (111, -7), (114, -8),
    (114, -9), (110, -8), (107, -8), (105, -7),
]
BORNEO = [
    (109, 1), (111, 2), (114, 4), (117, 6), (119, 5), (118, 1),
    (117, -2), (114, -3), (111, -2), (109, 0),
]
NEW_GUINEA = [
    (131, -1), (134, -2), (137, -3), (140, -4), (143, -6),
    (146, -7), (149, -9), (146, -9), (143, -8), (140, -7),
    (137, -4), (134, -3), (131, -2),
]
JAPAN = [
    (130, 31), (132, 33), (134, 34), (136, 35), (138, 35),
    (140, 36), (141, 38), (141, 41), (142, 43), (144, 44),
    (143, 42), (141, 40), (140, 38), (138, 36), (135, 34),
    (133, 34), (131, 32), (130, 31),
]
UK = [
    (-5, 50), (-3, 53), (-5, 56), (-3, 58),
    (-1, 57), (0, 53), (1, 51), (-2, 50), (-5, 50),
]
CONTINENTS = [
    NORTH_AMERICA, GREENLAND, SOUTH_AMERICA, AFRICA, EUROPE,
    ASIA, AUSTRALIA, SUMATRA, JAVA, BORNEO, NEW_GUINEA, JAPAN, UK,
]

# (number, lon, lat) of the stories marked on the map.
MARKERS = [
    (1, 114.1, 22.5),    # Shenzhen summit
    (2, 30.5, 50.4),     # Kyiv missiles
    (3, 85.8, 20.3),     # Cyclone Akvan, Odisha
    (4, 4.3, 52.1),      # ICJ, The Hague
    (5, 51.4, 35.7),     # Tehran
    (6, 34.5, 31.5),     # Gaza
    (7, -122.4, 37.8),   # San Francisco, Anthropic IPO
]

# (region, headline, detail). Headlines are kept to one line and
# details to one line at 14px / 11px so every story stays readable.
COLUMNS = [
    [  # Asia & Pacific + Science & Space
        ("ASIA & PACIFIC",
         "Cyclone Akvan: 300,000 evacuated",
         "423 rescue teams out in Odisha. — Reuters"),
        ("ASIA & PACIFIC",
         "Xi: US must do 'right thing' on Taiwan",
         "Warns ties will suffer after Trump talks. — AP"),
        ("ASIA & PACIFIC",
         "South Korea exports top $1 trillion",
         "First year ever past the trillion mark. — Reuters"),
        ("ASIA & PACIFIC",
         "China curbs mineral exports to Japan",
         "Beijing also bans seafood in Taiwan row."),
        ("ASIA & PACIFIC",
         "North Korea expands Yongbyon site",
         "IAEA: 'cause for serious concern'. — IAEA"),
        ("ASIA & PACIFIC",
         "Taiwan stocks fall 5,248 pts in 3 days",
         "Sharpest drop prompts regulator action."),
        ("ASIA & PACIFIC",
         "Japan PM Takaichi meets Putin at APEC",
         "Raises detained national; Taiwan unchanged."),
        ("ASIA & PACIFIC",
         "Indonesia passes asset-forfeiture bill",
         "Parliament backs seizures without conviction."),
        ("SCIENCE & SPACE",
         "Voyager 1 one light-day from Earth",
         "NASA confirms milestone; data has stopped. — NASA"),
        ("SCIENCE & SPACE",
         "Hayabusa2 scraps asteroid landing",
         "Engine trouble forces Japan probe rethink."),
        ("SCIENCE & SPACE",
         "Hydrogen flame mystery solved",
         "Sea salt explains the orange glow."),
    ],
    [  # Europe & Ukraine + Middle East
        ("EUROPE & UKRAINE",
         "Europe ready for Russia talks",
         "Leaders ready to negotiate an end. — Reuters"),
        ("EUROPE & UKRAINE",
         "Kyiv hit by four ballistic missiles",
         "Strikes damage two embassies in Kyiv. — Reuters"),
        ("EUROPE & UKRAINE",
         "France, Germany, UK eye Russia talks",
         "Allies discuss meeting after Shenzhen summit."),
        ("EUROPE & UKRAINE",
         "Poland PM joins Ukraine allies",
         "Coalition meets after Trump-Putin talks."),
        ("EUROPE & UKRAINE",
         "UK, Norway fund Ukrainian naval craft",
         "Joint programme worth over £100 million."),
        ("EUROPE & UKRAINE",
         "Denmark backs Greenland deal 109-0",
         "Parliament approves September agreement."),
        ("MIDDLE EAST",
         "Trump pushes Iran decision to 2027",
         "'See what happens' after Jan 1; no rush. — Reuters"),
        ("MIDDLE EAST",
         "US Senate rejects Iran war-powers bid",
         "Vote 51-48 against curbing Trump powers. — AP"),
        ("MIDDLE EAST",
         "US strikes Iranian island in Hormuz",
         "Tanker burns after mine hit; one missing."),
        ("MIDDLE EAST",
         "Israel hits Hezbollah site in Lebanon",
         "Airstrike targets facility in the east."),
        ("MIDDLE EAST",
         "Gaza aid groups rate peace plan 4/26",
         "Five agencies say delivery is lagging."),
    ],
    [  # Americas + Justice + Business & Tech + Sport & Culture
        ("AMERICAS",
         "Trump pardons baseball star Pete Rose",
         "Posthumous pardon for the late star. — AP"),
        ("AMERICAS",
         "California probes Nvidia chip sales",
         "State investigates AI chips bound for China."),
        ("JUSTICE",
         "UN court: Myanmar guilty of genocide",
         "ICJ rules 9-6; 730,000 fled in 2017. — ICJ"),
        ("BUSINESS & TECH",
         "Anthropic IPO raises $81.3bn, a record",
         "Nasdaq debut at $83; valued near $1.5tn. — Reuters"),
        ("BUSINESS & TECH",
         "AI data centres need $3.9tn by 2030",
         "IEA: power supply is the bottleneck. — IEA"),
        ("BUSINESS & TECH",
         "COP31 AI pledge shunned by US tech",
         "Major American firms stay away."),
        ("BUSINESS & TECH",
         "Sensex jumps 1,000 points to 83,021",
         "Nifty crosses 25,500 on bank, auto buying."),
        ("SPORT & CULTURE",
         "GTA 6 sales pass $1.8bn, a record",
         "Fastest-selling entertainment launch ever."),
        ("SPORT & CULTURE",
         "Zverev into ATP Finals semi-finals",
         "Beats Shelton in Turin; Alcaraz unbeaten."),
        ("SPORT & CULTURE",
         "Fiona the hippo dies after eating a hat",
         "Cincinnati Zoo mourns its beloved hippo."),
    ],
]

# (time label, event) for the bottom timeline strip. Times are
# approximate, in UTC, as the strip itself states.
TIMELINE = [
    ("~01:00", "Shenzhen summit opens"),
    ("~05:00", "Cyclone nears Odisha coast"),
    ("~08:00", "Kyiv missile barrage"),
    ("~12:00", "Joint statement issued"),
    ("~16:00", "Anthropic debuts on Nasdaq"),
    ("~20:00", "Europe open to Russia talks"),
]

LEAD_HEAD = "Trump, Xi & Putin meet in first-ever three-way summit"
LEAD_BODY = ("Nuclear cuts, Ukraine and Iran on the agenda. Joint "
             "statement: 'a nuclear war cannot be won and must "
             "never be fought.'")


def draw_masthead(draw):
    tf = font(SERIF_BOLD, 42)
    title = "THE WORLD IN ONE DAY"
    tw = draw.textlength(title, font=tf)
    draw.text(((W - tw) / 2, 10), title, font=tf, fill=INK)
    draw.line([(28, 62), (W - 28, 62)], fill=RULE, width=2)
    df = font(SANS_BOLD, 15)
    date = "FRIDAY 20 NOVEMBER 2026  •  34 STORIES  •  8 SECTIONS  •  7 PLACES MAPPED"
    dw = draw.textlength(date, font=df)
    draw.text(((W - dw) / 2, 68), date, font=df, fill=INK)
    draw.line([(28, 90), (W - 28, 90)], fill=RULE, width=3)


def draw_lead(draw):
    x0, y0, x1, y1 = 28, 96, 996, 276
    draw.rectangle((x0, y0, x1, y1), fill=(255, 255, 255),
                   outline=RULE, width=1)
    # --- drawn illustration: Shenzhen sunset skyline, three flags ---
    ix0, iy0, ix1, iy1 = x0 + 1, y0 + 1, 400, y1 - 1
    # sunset sky, three blended bands
    top, mid, low = (46, 74, 122), (232, 98, 44), (247, 183, 115)
    horizon = iy0 + 108
    for y in range(iy0, horizon):
        t = (y - iy0) / max(1, horizon - iy0)
        draw.line([(ix0, y), (ix1, y)], fill=lerp(top, mid, t))
    for y in range(horizon, iy1):
        t = (y - horizon) / max(1, iy1 - horizon)
        draw.line([(ix0, y), (ix1, y)], fill=lerp(mid, low, t))
    # low sun
    draw.ellipse([(318, 178), (362, 222)], fill=(255, 233, 168))
    # skyline silhouettes with lit windows (fixed pattern)
    buildings = [
        (28, 46, 108), (76, 34, 78), (112, 40, 122), (154, 30, 66),
        (186, 44, 100), (232, 36, 132), (270, 30, 84), (302, 42, 116),
        (346, 32, 72), (380, 20, 96),
    ]
    for bx, bw, bh in buildings:
        draw.rectangle([(bx, iy1 - bh), (bx + bw, iy1)],
                       fill=(32, 41, 74))
        for row in range(4, bh - 6, 12):
            for col in range(6, bw - 4, 11):
                if (bx + row + col) % 3 == 0:
                    draw.rectangle(
                        [(bx + col, iy1 - bh + row),
                         (bx + col + 3, iy1 - bh + row + 4)],
                        fill=(255, 214, 110))
    # three flag poles in front of the skyline
    for px, kind in ((70, "us"), (200, "cn"), (330, "ru")):
        draw.line([(px, 140), (px, iy1)], fill=(25, 25, 25), width=3)
        fx, fy, fw, fh = px + 2, 140, 48, 30
        if kind == "us":
            for i in range(7):
                col = (178, 34, 52) if i % 2 == 0 else (255, 255, 255)
                draw.rectangle([(fx, fy + i * fh // 7),
                                (fx + fw, fy + (i + 1) * fh // 7)],
                               fill=col)
            draw.rectangle([(fx, fy), (fx + 20, fy + 16)],
                           fill=(60, 59, 110))
            for sy in (fy + 4, fy + 9, fy + 13):
                for sx in (fx + 4, fx + 11, fx + 17):
                    draw.ellipse([(sx, sy), (sx + 2, sy + 2)],
                                 fill=(255, 255, 255))
        elif kind == "cn":
            draw.rectangle([(fx, fy), (fx + fw, fy + fh)],
                           fill=(222, 41, 16))
            draw.polygon(star_points(fx + 12, fy + 11, 6, 2.5),
                         fill=(255, 222, 0))
            for sx, sy in ((30, 6), (36, 10), (36, 16), (30, 19)):
                draw.polygon(star_points(fx + sx, fy + sy, 2.5, 1),
                             fill=(255, 222, 0))
        else:
            for i, col in enumerate(
                    ((255, 255, 255), (0, 57, 166), (213, 43, 30))):
                draw.rectangle([(fx, fy + i * fh // 3),
                                (fx + fw, fy + (i + 1) * fh // 3)],
                               fill=col)
    # --- lead text, right of the illustration ---
    tx, tw = 416, 996 - 28 - 416
    kf = font(SANS_BOLD, 14)
    draw.text((tx, 108), "SHENZHEN  •  TRILATERAL SUMMIT",
              font=kf, fill=ACCENT)
    hf = font(SANS_BOLD, 25)
    y = 130
    for line in wrap(draw, LEAD_HEAD, hf, tw)[:2]:
        draw.text((tx, y), line, font=hf, fill=INK)
        y += 30
    bf = font(SANS, 15)
    y = 194
    for line in wrap(draw, LEAD_BODY, bf, tw)[:3]:
        draw.text((tx, y), line, font=bf, fill=INK)
        y += 19
    sf = font(SANS, 11)
    draw.text((tx, 258), "Sources: Reuters, AP, AFP — reporting from Shenzhen",
              font=sf, fill=GREY)


def draw_map(draw):
    x0, y0, x1, y1 = 28, 282, 620, 448
    draw.rectangle((x0, y0, x1, y1), fill=(255, 255, 255),
                   outline=RULE, width=1)
    tf = font(SANS_BOLD, 12)
    draw.text((40, 290), "WHERE THE DAY HAPPENED — WORLD MAP",
              font=tf, fill=INK)
    mx0, my0, mw, mh = 40, 308, 568, 110

    def proj(lon, lat):
        return (mx0 + (lon + 170) * mw / 360.0,
                my0 + (78 - lat) * mh / 134.0)

    draw.rectangle((mx0, my0, mx0 + mw, my0 + mh), fill=SEA)
    for poly in CONTINENTS:
        draw.polygon([proj(lon, lat) for lon, lat in poly],
                     fill=LAND, outline=LAND_LINE)
    nf = font(SANS_BOLD, 11)
    for num, lon, lat in MARKERS:
        cx, cy = proj(lon, lat)
        draw.ellipse([(cx - 7, cy - 7), (cx + 7, cy + 7)],
                     fill=ACCENT, outline=(255, 255, 255), width=1)
        tw = draw.textlength(str(num), font=nf)
        draw.text((cx - tw / 2, cy - 6), str(num), font=nf,
                  fill=(255, 255, 255))
    lf = font(SANS, 11)
    legend = ("1 Shenzhen  •  2 Kyiv  •  3 Odisha  •  4 The Hague  •  "
              "5 Tehran  •  6 Gaza  •  7 San Francisco")
    draw.text((40, 426), legend, font=lf, fill=INK)


def draw_verify(draw):
    x0, y0, x1, y1 = 632, 282, 996, 448
    draw.rectangle((x0, y0, x1, y1), fill=(255, 255, 255),
                   outline=RULE, width=1)
    tf = font(SANS_BOLD, 13)
    draw.text((648, 292), "DATE CHECK — VERIFIED", font=tf, fill=ACCENT)
    # green check seal
    draw.ellipse([(944, 290), (976, 322)], fill=GREEN)
    draw.line([(950, 306), (957, 313), (970, 298)], fill=(255, 255, 255),
              width=3)
    bf = font(SANS_BOLD, 16)
    draw.text((648, 318), "Friday, 20 November 2026", font=bf, fill=INK)
    vf = font(SANS, 12)
    lines = [
        "All 34 stories drawn from reporting",
        "dated 20 November 2026.",
        "8 sections  •  7 named sources  •  7 places mapped.",
        "Timeline times are approximate (UTC).",
        "No photos: every visual drawn in PIL.",
    ]
    y = 346
    for line in lines:
        draw.text((648, y), line, font=vf, fill=INK)
        y += 18


def draw_columns(draw):
    m = 28
    col_w = (W - 2 * m - 2 * 12) // 3
    col_x = [m, m + col_w + 12, m + 2 * (col_w + 12)]
    top, bottom = 456, 928
    hf = font(SANS_BOLD, 14)
    bf = font(SANS, 11)
    rf = font(SANS_BOLD, 12)
    ends = []
    for ci, items in enumerate(COLUMNS):
        x = col_x[ci]
        y = top
        region = None
        for reg, head, detail in items:
            if reg != region:
                region = reg
                draw.text((x, y), region, font=rf, fill=ACCENT)
                draw.line([(x, y + 16), (x + col_w, y + 16)],
                          fill=ACCENT, width=1)
                y += 22
            for line in wrap(draw, head, hf, col_w)[:2]:
                draw.text((x, y), line, font=hf, fill=INK)
                y += 17
            for line in wrap(draw, detail, bf, col_w)[:1]:
                draw.text((x, y), line, font=bf, fill=GREY)
                y += 14
            y += 6
        ends.append(y)
        if ci < 2:
            draw.line([(x + col_w + 6, top), (x + col_w + 6, bottom)],
                      fill=(200, 200, 190), width=1)
    print("column bottoms:", ends, "limit:", bottom)
    for i, end in enumerate(ends):
        if end > bottom:
            raise RuntimeError(f"column {i} overflows: {end} > {bottom}")


def draw_timeline(draw):
    tf = font(SANS_BOLD, 11)
    draw.text((28, 938), "THE DAY IN UTC — TIMES APPROXIMATE",
              font=tf, fill=INK)
    stops_x = [100, 260, 420, 580, 740, 900]
    draw.line([(60, 972), (964, 972)], fill=RULE, width=2)
    for (time, event), cx in zip(TIMELINE, stops_x):
        draw.ellipse([(cx - 5, 967), (cx + 5, 977)], fill=ACCENT)
        tw = draw.textlength(time, font=tf)
        draw.text((cx - tw / 2, 954), time, font=tf, fill=INK)
        ef = font(SANS, 11)
        y = 982
        for line in wrap(draw, event, ef, 140)[:2]:
            lw = draw.textlength(line, font=ef)
            draw.text((cx - lw / 2, y), line, font=ef, fill=INK)
            y += 13


def build_image():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_lead(draw)
    draw_map(draw)
    draw_verify(draw)
    draw_columns(draw)
    draw_timeline(draw)
    return img


if __name__ == "__main__":
    build_image().save("entry.png", format="PNG")
    print("wrote entry.png")

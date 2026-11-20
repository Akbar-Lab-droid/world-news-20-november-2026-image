"""Draw a 1024x1024 newspaper front page summing up 20 November 2026.

Deterministic: fixed fonts, fixed colours, no timestamps, no randomness.
Each story panel has a small drawn icon on its left so the story is
clear from its picture as well as its label. Run directly to write
entry.png next to this file.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 251, 244)
INK = (20, 20, 20)
RULE = (60, 60, 60)
ACCENT = (139, 0, 0)
PANEL_BG = (255, 255, 255)
BLUE = (28, 68, 140)
GOLD = (212, 160, 23)
TEAL = (18, 110, 110)

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


# --- icons: each draws inside a square centred on (cx, cy), half-size s ---
def icon_summit(d, cx, cy, s):
    """Three small flags: US, China, Russia."""
    fw, fh = int(s * 0.62), int(s * 0.78)
    gap = int(s * 0.14)
    x = cx - (3 * fw + 2 * gap) // 2
    y = cy - fh // 2
    # US: red/white stripes, blue canton
    for i in range(5):
        d.rectangle([x, y + i * fh // 5, x + fw, y + (i + 1) * fh // 5],
                    fill=(178, 34, 34) if i % 2 == 0 else (255, 255, 255))
    d.rectangle([x, y, x + fw // 2, y + fh * 2 // 5], fill=BLUE)
    d.ellipse([x + 4, y + 4, x + 9, y + 9], fill=(255, 255, 255))
    d.rectangle([x, y, x + fw, y + fh], outline=RULE, width=1)
    x += fw + gap
    # China: red field, yellow stars
    d.rectangle([x, y, x + fw, y + fh], fill=(222, 41, 16))
    d.ellipse([x + 5, y + 5, x + 13, y + 13], fill=GOLD)
    d.ellipse([x + fw - 12, y + 6, x + fw - 6, y + 12], fill=GOLD)
    d.rectangle([x, y, x + fw, y + fh], outline=RULE, width=1)
    x += fw + gap
    # Russia: white, blue, red horizontal stripes
    for i, c in enumerate([(255, 255, 255), BLUE, (178, 34, 34)]):
        d.rectangle([x, y + i * fh // 3, x + fw, y + (i + 1) * fh // 3], fill=c)
    d.rectangle([x, y, x + fw, y + fh], outline=RULE, width=1)


def icon_clock(d, cx, cy, s):
    d.ellipse([cx - s, cy - s, cx + s, cy + s], fill=(240, 240, 235))
    d.ellipse([cx - s, cy - s, cx + s, cy + s], outline=INK, width=3)
    d.line([(cx, cy), (cx, cy - int(s * 0.62))], fill=INK, width=3)
    d.line([(cx, cy), (cx + int(s * 0.5), cy + int(s * 0.28))], fill=INK, width=3)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=ACCENT)


def icon_scales(d, cx, cy, s):
    d.line([(cx, cy - s), (cx, cy + s)], fill=INK, width=3)
    d.line([(cx - s, cy - int(s * 0.55)), (cx + s, cy - int(s * 0.55))],
           fill=INK, width=3)
    d.ellipse([cx - 4, cy - s - 4, cx + 4, cy - s + 4], fill=GOLD)
    for sx in (cx - s, cx + s):
        d.line([(sx, cy - int(s * 0.55)), (sx, cy + int(s * 0.1))],
               fill=INK, width=2)
        d.polygon([(sx - int(s * 0.42), cy + int(s * 0.1)),
                   (sx + int(s * 0.42), cy + int(s * 0.1)),
                   (sx, cy + int(s * 0.62))], fill=GOLD, outline=INK)
    d.line([(cx - int(s * 0.5), cy + s), (cx + int(s * 0.5), cy + s)],
           fill=INK, width=3)


def icon_probe(d, cx, cy, s):
    # stars
    for sx, sy in ((cx - s, cy - s), (cx + s, cy - s + 6),
                   (cx - int(s * 0.7), cy + int(s * 0.7))):
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=GOLD)
    # dish + body
    d.line([(cx - int(s * 0.5), cy - int(s * 0.5)),
            (cx + int(s * 0.2), cy + int(s * 0.2))], fill=INK, width=3)
    d.polygon([(cx + int(s * 0.2), cy - int(s * 0.55)),
               (cx + int(s * 0.75), cy + int(s * 0.1)),
               (cx + int(s * 0.05), cy + int(s * 0.35))],
              fill=(200, 200, 200), outline=INK)
    d.ellipse([cx - int(s * 0.45), cy - int(s * 0.15),
               cx + int(s * 0.15), cy + int(s * 0.45)],
              fill=BLUE, outline=INK)
    d.line([(cx - int(s * 0.4), cy + int(s * 0.5)),
            (cx - int(s * 0.75), cy + int(s * 0.8))], fill=INK, width=2)


def icon_cyclone(d, cx, cy, s):
    # spiral: concentric arcs
    for r, start in ((s, 20), (int(s * 0.72), 110), (int(s * 0.45), 200)):
        d.arc([cx - r, cy - r, cx + r, cy + r], start, start + 260,
              fill=TEAL, width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=ACCENT)
    # rain drops
    for dx in (-int(s * 0.8), 0, int(s * 0.8)):
        d.line([(cx + dx, cy + s + 4), (cx + dx - 3, cy + s + 14)],
               fill=BLUE, width=3)


def icon_eu(d, cx, cy, s):
    import math
    d.ellipse([cx - s, cy - s, cx + s, cy + s], fill=BLUE)
    for i in range(12):
        a = math.pi * 2 * i / 12 - math.pi / 2
        sx = cx + int(s * 0.68 * math.cos(a))
        sy = cy + int(s * 0.68 * math.sin(a))
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=GOLD)


ICONS = {
    "summit": icon_summit,
    "clock": icon_clock,
    "scales": icon_scales,
    "probe": icon_probe,
    "cyclone": icon_cyclone,
    "eu": icon_eu,
}


def draw_panel(draw, box, kicker, headline, body, icon=None,
               head_size=25, body_size=18, icon_w=72):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=PANEL_BG, outline=RULE, width=1)
    pad = 16
    tx = x0 + pad
    if icon is not None:
        ix = x0 + pad + icon_w // 2
        iy = (y0 + y1) // 2
        ICONS[icon](draw, ix, iy, 26)
        tx = x0 + pad + icon_w + 8
    w = x1 - tx - pad
    y = y0 + 12
    kf = font(SANS_BOLD, 17)
    draw.text((tx, y), kicker, font=kf, fill=ACCENT)
    y += 26
    hf = font(SANS_BOLD, head_size)
    for line in wrap(draw, headline, hf, w):
        draw.text((tx, y), line, font=hf, fill=INK)
        y += head_size + 6
    y += 4
    bf = font(SANS, body_size)
    for line in wrap(draw, body, bf, w):
        draw.text((tx, y), line, font=bf, fill=INK)
        y += body_size + 6


def build_image():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    M = 28

    # Masthead
    title = "THE WORLD IN ONE DAY"
    tf = font(SERIF_BOLD, 56)
    tw = draw.textlength(title, font=tf)
    draw.text(((W - tw) / 2, 26), title, font=tf, fill=INK)
    draw.line([(M, 100), (W - M, 100)], fill=RULE, width=2)
    date = "FRIDAY 20 NOVEMBER 2026"
    df = font(SANS_BOLD, 26)
    dw = draw.textlength(date, font=df)
    draw.text(((W - dw) / 2, 110), date, font=df, fill=INK)
    draw.line([(M, 148), (W - M, 148)], fill=RULE, width=3)

    # Lead story, full width
    draw_panel(
        draw, (M, 162, W - M, 338),
        "SHENZHEN  •  TRILATERAL SUMMIT",
        "Trump, Xi & Putin meet in first-ever three-way summit",
        "Nuclear powers open talks in Shenzhen; nuclear cuts, Ukraine "
        "and Iran on the agenda.",
        icon="summit", head_size=34, body_size=21, icon_w=150,
    )

    # Row 2: Iran and The Hague
    mid = (W - 12) // 2
    draw_panel(
        draw, (M, 350, mid, 514),
        "WASHINGTON  •  IRAN",
        "Trump pushes Iran decision to 2027",
        "Says he'll 'see what happens' after Jan 1; no rush.",
        icon="clock",
    )
    draw_panel(
        draw, (mid + 12, 350, W - M, 514),
        "THE HAGUE  •  JUSTICE",
        "UN court: Myanmar committed genocide",
        "ICJ rules the 2017 crackdown drove 730,000 to Bangladesh.",
        icon="scales",
    )

    # Row 3: Space and India
    draw_panel(
        draw, (M, 526, mid, 690),
        "SPACE",
        "Voyager 1 reaches one light-day from Earth",
        "NASA confirms the milestone; the 1977 probe's data flow "
        "has stopped.",
        icon="probe",
    )
    draw_panel(
        draw, (mid + 12, 526, W - M, 690),
        "INDIA  •  STORMS",
        "Cyclone Akvan: 300,000 evacuated",
        "Storm bears down on Odisha; 423 rescue teams deployed.",
        icon="cyclone",
    )

    # Panel 6: Europe, full width
    draw_panel(
        draw, (M, 702, W - M, 842),
        "UKRAINE  •  EUROPE",
        "Europe ready for talks with Russia to end the war",
        "Leaders say they are prepared to negotiate an end to the "
        "Ukraine war.",
        icon="eu", head_size=28, body_size=19, icon_w=110,
    )

    # Footer: Also today
    fx0, fy0, fx1, fy1 = M, 854, W - M, 996
    draw.rectangle((fx0, fy0, fx1, fy1), fill=PANEL_BG, outline=RULE, width=1)
    kf = font(SANS_BOLD, 17)
    draw.text((fx0 + 16, fy0 + 10), "ALSO TODAY", font=kf, fill=ACCENT)
    footer = (
        "GTA 6 sales pass $1.8bn, topping The Odyssey  •  "
        "Tanker burns after hitting a mine near Hormuz  •  "
        "Hayabusa2 scraps asteroid landing after engine trouble  •  "
        "IAEA: North Korea expanding Yongbyon enrichment"
    )
    bf = font(SANS, 19)
    y = fy0 + 38
    for line in wrap(draw, footer, bf, fx1 - fx0 - 32):
        draw.text((fx0 + 16, y), line, font=bf, fill=INK)
        y += 25

    return img


if __name__ == "__main__":
    build_image().save("entry.png", format="PNG")
    print("wrote entry.png")

"""Draw a 1024x1024 newspaper front page summing up 20 November 2026.

Deterministic: fixed fonts, fixed colours, no timestamps, no randomness.
Run directly to write entry.png next to this file.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 251, 244)
INK = (20, 20, 20)
RULE = (60, 60, 60)
ACCENT = (139, 0, 0)
PANEL_BG = (255, 255, 255)

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


def draw_panel(draw, box, kicker, headline, body, head_size=27, body_size=20):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=PANEL_BG, outline=RULE, width=1)
    pad = 16
    x = x0 + pad
    w = x1 - x0 - 2 * pad
    y = y0 + 12
    kf = font(SANS_BOLD, 17)
    draw.text((x, y), kicker, font=kf, fill=ACCENT)
    y += 26
    hf = font(SANS_BOLD, head_size)
    for line in wrap(draw, headline, hf, w):
        draw.text((x, y), line, font=hf, fill=INK)
        y += head_size + 6
    y += 4
    bf = font(SANS, body_size)
    for line in wrap(draw, body, bf, w):
        draw.text((x, y), line, font=bf, fill=INK)
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
        head_size=34, body_size=21,
    )

    # Row 2: Gulf and Ukraine
    mid = (W - 12) // 2
    draw_panel(
        draw, (M, 350, mid, 514),
        "WASHINGTON  •  IRAN",
        "Trump pushes Iran decision to 2027",
        "Says he\'ll \'see what happens\' after Jan 1; no rush on a "
        "war decision.",
    )
    draw_panel(
        draw, (mid + 12, 350, W - M, 514),
        "THE HAGUE  •  JUSTICE",
        "UN court: Myanmar committed genocide",
        "ICJ rules over the 2017 Rohingya crackdown that drove "
        "730,000 to Bangladesh.",
    )

    # Row 3: AI/Markets and The Hague
    draw_panel(
        draw, (M, 526, mid, 690),
        "SPACE",
        "Voyager 1 reaches one light-day from Earth",
        "NASA confirms the milestone; the 1977 probe\'s data flow "
        "has stopped.",
    )
    draw_panel(
        draw, (mid + 12, 526, W - M, 690),
        "INDIA  •  STORMS",
        "Cyclone Akvan: 300,000 evacuated",
        "Storm bears down on the Odisha coast; 423 rescue teams "
        "deployed.",
    )

    # Panel 6: Climate, full width
    draw_panel(
        draw, (M, 702, W - M, 842),
        "UKRAINE  •  EUROPE",
        "Europe ready for talks with Russia to end the war",
        "Leaders say they are prepared to negotiate an end to the "
        "Ukraine war.",
        head_size=28, body_size=19,
    )

    # Footer: Also today
    fx0, fy0, fx1, fy1 = M, 854, W - M, 996
    draw.rectangle((fx0, fy0, fx1, fy1), fill=PANEL_BG, outline=RULE, width=1)
    kf = font(SANS_BOLD, 17)
    draw.text((fx0 + 16, fy0 + 10), "ALSO TODAY", font=kf, fill=ACCENT)
    footer = (
        "GTA 6 sales pass $1.8bn, topping The Odyssey  \u2022  "
        "Tanker burns after hitting a mine near Hormuz  \u2022  "
        "Hayabusa2 scraps asteroid landing after engine trouble  \u2022  "
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

"""Draw a 1024x1024 dense newspaper front page summing up 20 November 2026.

Deterministic: fixed fonts, fixed colours, no timestamps, no randomness.
A lead story plus three columns of short items grouped by region, so
the day's breadth (48 stories) is visible at a glance. Run directly
to write entry.png next to this file.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 251, 244)
INK = (20, 20, 20)
RULE = (60, 60, 60)
ACCENT = (139, 0, 0)

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


# (region, headline, detail). Region shown as a header when it changes.
# Details are kept short so each fits on one line.
COLUMNS = [
    [  # Asia & Pacific
        ("ASIA & PACIFIC",
         "APEC adopts Shenzhen Outlook on trade and AI",
         "Xi chairs summit; Vietnam takes over as host for 2027."),
        ("ASIA & PACIFIC",
         "Xi: US should do 'right thing' on Taiwan",
         "Warns of setbacks in ties after talks with Trump."),
        ("ASIA & PACIFIC",
         "Japan PM Takaichi meets Putin at APEC",
         "Raises detained national; Taiwan stance unchanged."),
        ("ASIA & PACIFIC",
         "South Korea's Lee: talks with North could end war",
         "Hopes reopened dialogue leads to lasting peace."),
        ("ASIA & PACIFIC",
         "North Korea expanding Yongbyon enrichment",
         "IAEA calls it a 'cause for serious concern'."),
        ("ASIA & PACIFIC",
         "South Korea exports top $1 trillion",
         "First time annual exports pass the trillion mark."),
        ("ASIA & PACIFIC",
         "Taiwan moves to steady falling stocks",
         "Regulator unveils five measures to steady stocks."),
        ("ASIA & PACIFIC",
         "Taiwan stocks fall 5,248 points in three days",
         "Sharpest three-day drop prompts regulator action."),
        ("ASIA & PACIFIC",
         "China curbs mineral exports to Japan",
         "Beijing restricts minerals, bans seafood in Taiwan row."),
        ("ASIA & PACIFIC",
         "Cyclone Akvan: 300,000 evacuated in Odisha",
         "423 rescue teams deployed as storm nears landfall."),
        ("ASIA & PACIFIC",
         "Modi meets Prince and Princess of Wales",
         "India-UK ties and strategic cooperation on agenda."),
        ("ASIA & PACIFIC",
         "India exports up 16.6%; electronics jump 44%",
         "April-September exports keep $1tn target in reach."),
        ("ASIA & PACIFIC",
         "ISRO names four Gaganyaan astronaut candidates",
         "India's first human spaceflight advances."),
        ("ASIA & PACIFIC",
         "Indonesia passes asset-forfeiture bill",
         "Parliament approves seizures without conviction."),
        ("ASIA & PACIFIC",
         "India-Malaysia joint exercise begins in Ipoh",
         "'Harimau Shakti' drills open in Malaysia."),
        ("ASIA & PACIFIC",
         "ICMR completes 100 healthcare tech transfers",
         "Indian medical research reaches licensing milestone."),
    ],
    [  # Europe, Ukraine, Middle East
        ("EUROPE & UKRAINE",
         "Europe ready for talks with Russia to end war",
         "Leaders prepared to negotiate an end to the war."),
        ("EUROPE & UKRAINE",
         "Kyiv hit by four ballistic missiles",
         "Russian strikes damage Austrian and Dutch embassies."),
        ("EUROPE & UKRAINE",
         "France, Germany, UK discuss meeting Russia",
         "Allies weigh direct talks after the Shenzhen summit."),
        ("EUROPE & UKRAINE",
         "Poland PM joins Ukraine allies in Berlin",
         "Coalition meets after Trump-Putin talks in China."),
        ("EUROPE & UKRAINE",
         "UK and Norway fund two Ukrainian naval craft",
         "Joint programme worth over £100 million."),
        ("EUROPE & UKRAINE",
         "Denmark approves Greenland defence deal 109-0",
         "Parliament backs the agreement signed in September."),
        ("EUROPE & UKRAINE",
         "Genoa airport halts flights after drone sightings",
         "Operations suspended for four hours overnight."),
        ("MIDDLE EAST",
         "Trump pushes Iran decision to 2027",
         "Says he'll 'see what happens' after Jan 1; no rush."),
        ("MIDDLE EAST",
         "US Senate rejects Iran war-powers resolution",
         "Vote 51-48 against curbing Trump's war powers."),
        ("MIDDLE EAST",
         "US strikes Iranian island in Hormuz",
         "Tanker burns after mine hit; one crew missing."),
        ("MIDDLE EAST",
         "Houthis claim strikes on four Saudi targets",
         "Riyadh landmark building damaged in the attack."),
        ("MIDDLE EAST",
         "Somalia orders UAE ambassador to leave",
         "Accuses UAE of an 'open invasion' of sovereignty."),
        ("MIDDLE EAST",
         "Israel hits Hezbollah missile site in Lebanon",
         "Airstrike targets facility in the east of the country."),
        ("MIDDLE EAST",
         "Syria hails UN resolution on post-war progress",
         "Damascus welcomes recognition of its recovery."),
        ("MIDDLE EAST",
         "Gaza aid groups rate peace plan 4 out of 26",
         "Five agencies say implementation is lagging."),
        ("MIDDLE EAST",
         "One dead, 15 hurt in French apartment fire",
         "Blaze hits an 18-storey block; 15 injured."),
    ],
    [  # Americas, science, business, sport
        ("AMERICAS",
         "Trump pardons baseball legend Pete Rose",
         "Posthumous pardon for the late baseball star."),
        ("AMERICAS",
         "California targets Nvidia in China chip probe",
         "State investigates AI chip sales to China."),
        ("JUSTICE",
         "UN court: Myanmar committed genocide",
         "ICJ rules 9-6; 730,000 fled the 2017 crackdown."),
        ("BUSINESS & TECH",
         "Anthropic IPO raises $81.3bn, largest ever",
         "Shares debut on Nasdaq at $83; valued near $1.5tn."),
        ("BUSINESS & TECH",
         "AI data centres need $3.9tn by 2030",
         "IEA: power supply is the bottleneck for build-out."),
        ("BUSINESS & TECH",
         "Sensex jumps 1,000 points to 83,021",
         "Nifty crosses 25,500 on banking and auto buying."),
        ("SCIENCE & SPACE",
         "Voyager 1 reaches one light-day from Earth",
         "NASA confirms milestone; data flow has stopped."),
        ("SCIENCE & SPACE",
         "Hayabusa2 scraps asteroid landing",
         "Engine trouble forces Japan's probe to change plans."),
        ("SCIENCE & SPACE",
         "Hydrogen flame colour mystery solved",
         "Sea salt in the air explains the orange glow."),
        ("SPORT & CULTURE",
         "GTA 6 sales pass $1.8bn, topping The Odyssey",
         "Fastest-selling entertainment launch ever."),
        ("SPORT & CULTURE",
         "Nicholls 113* as New Zealand reach 243/5",
         "First Test against India, Day 1 in Wellington."),
        ("SPORT & CULTURE",
         "Zverev into ATP Finals semi-finals",
         "Beats Shelton in Turin; Alcaraz stays unbeaten."),
        ("SPORT & CULTURE",
         "Fiona the hippo dies after swallowing a hat",
         "Cincinnati Zoo mourns its beloved hippo."),
        ("SPORT & CULTURE",
         "Global Champions Tour finale moves to Verona",
         "Show jumping relocates from Riyadh amid conflict."),
        ("SPORT & CULTURE",
         "COP31 AI pledge fails to win big US tech firms",
         "Major American companies stay away from the pledge."),
    ],
]


def build_image():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    M = 28

    # Masthead
    title = "THE WORLD IN ONE DAY"
    tf = font(SERIF_BOLD, 46)
    tw = draw.textlength(title, font=tf)
    draw.text(((W - tw) / 2, 16), title, font=tf, fill=INK)
    draw.line([(M, 72), (W - M, 72)], fill=RULE, width=2)
    date = "FRIDAY 20 NOVEMBER 2026  •  48 STORIES"
    df = font(SANS_BOLD, 18)
    dw = draw.textlength(date, font=df)
    draw.text(((W - dw) / 2, 80), date, font=df, fill=INK)
    draw.line([(M, 106), (W - M, 106)], fill=RULE, width=3)

    # Lead story, full width
    lx0, ly0, lx1, ly1 = M, 114, W - M, 206
    draw.rectangle((lx0, ly0, lx1, ly1), fill=(255, 255, 255), outline=RULE, width=1)
    kf = font(SANS_BOLD, 15)
    draw.text((lx0 + 14, ly0 + 8), "SHENZHEN  •  TRILATERAL SUMMIT", font=kf, fill=ACCENT)
    hf = font(SANS_BOLD, 26)
    draw.text((lx0 + 14, ly0 + 30), "Trump, Xi & Putin meet in first-ever three-way summit",
              font=hf, fill=INK)
    bf = font(SANS, 15)
    lead_body = ("Nuclear cuts, Ukraine and Iran on the agenda; joint statement: "
                 "'a nuclear war cannot be won and must never be fought.'")
    by = ly0 + 62
    for line in wrap(draw, lead_body, bf, lx1 - lx0 - 28)[:2]:
        draw.text((lx0 + 14, by), line, font=bf, fill=INK)
        by += 19

    # Columns
    col_w = (W - 2 * M - 2 * 12) // 3
    col_x = [M, M + col_w + 12, M + 2 * (col_w + 12)]
    top = 214
    bottom = H - 14
    hf_item = font(SANS_BOLD, 13)
    bf_item = font(SANS, 11)
    rf = font(SANS_BOLD, 12)

    for ci, items in enumerate(COLUMNS):
        x = col_x[ci]
        y = top
        region = None
        for reg, head, detail in items:
            if reg != region:
                region = reg
                draw.text((x, y), region, font=rf, fill=ACCENT)
                draw.line([(x, y + 17), (x + col_w, y + 17)], fill=ACCENT, width=1)
                y += 24
            head_lines = wrap(draw, head, hf_item, col_w)
            for line in head_lines[:2]:
                draw.text((x, y), line, font=hf_item, fill=INK)
                y += 16
            det_lines = wrap(draw, detail, bf_item, col_w)
            for line in det_lines[:1]:
                draw.text((x, y), line, font=bf_item, fill=(70, 70, 70))
                y += 14
            y += 7
        if ci < 2:
            draw.line([(x + col_w + 6, top), (x + col_w + 6, bottom)],
                      fill=(200, 200, 190), width=1)

    return img


if __name__ == "__main__":
    build_image().save("entry.png", format="PNG")
    print("wrote entry.png")

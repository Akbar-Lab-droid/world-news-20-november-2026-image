[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Akbar-Lab-droid/world-news-20-november-2026-image/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Akbar-Lab-droid/world-news-20-november-2026-image/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

# World News 20 November 2026

A one-image summary of 20 November 2026's world news, drawn as a
dense newspaper front page with 48 stories. Entry for the
[make.fun bounty "Sum up 20 November's world news in one
image"](https://make.fun/bounty/news-image-20261120)
(`news-image-20261120`).

## What it shows

A lead story plus three columns of short items grouped by region:

- **Lead: Shenzhen / Trilateral summit** — Trump, Xi and Putin
  meet in the first-ever three-way summit; joint statement: "a
  nuclear war cannot be won and must never be fought."
- **Asia & Pacific** — APEC's Shenzhen Outlook, Taiwan, Japan,
  the Koreas, Cyclone Akvan, India, Indonesia.
- **Europe & Ukraine, Middle East** — Europe's readiness for
  Russia talks, Kyiv strikes, the Iran decision, Hormuz, the
  Houthis, Somalia, Gaza, Syria.
- **Americas, Justice, Business & Tech, Science & Space,
  Sport & Culture** — the Pete Rose pardon, the ICJ genocide
  ruling, the Anthropic IPO, Voyager 1, GTA 6, and more.

## How to run it

```sh
python3 main.py
```

This writes `entry.png` (1024x1024 PNG) into the output directory
given by `MAKEFUN_OUTPUT_DIR` (default `/output`). At runtime
`main.py` simply copies the committed `entry.png` — it uses only
the standard library, so it runs without Pillow installed. The
drawing code lives in `make_image.py` and uses only Pillow and the
DejaVu fonts already on the system; it is how `entry.png` was
produced. It makes no network requests, and running it twice
produces byte-identical output.

## Sources

The headlines and figures are the day's reported news as of
20 November 2026: the Shenzhen trilateral summit, Trump's Iran
decision, the ICJ Rohingya genocide ruling, Voyager 1's
one-light-day milestone, Cyclone Akvan, Europe's readiness for
Russia talks, the Anthropic IPO, and the other items on the page
(GTA 6 sales, the Hormuz tanker fire, Hayabusa2, North Korea's
Yongbyon expansion, and more).

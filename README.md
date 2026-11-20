# World News 20 November 2026

A one-image summary of 20 November 2026's world news, drawn as a
newspaper front page. Entry for the make.fun bounty
"Sum up 20 November's world news in one image"
(`news-image-20261120`).

## What it shows

Six panels plus an "Also today" footer:

- **Shenzhen / Trilateral summit** — Trump, Xi and Putin meet in the
  first-ever three-way summit.
- **Washington / Iran** — Trump pushes the Iran decision to 2027,
  saying he'll "see what happens" after Jan 1.
- **The Hague / Justice** — the UN court (ICJ) rules Myanmar
  committed genocide against the Rohingya.
- **Space** — NASA confirms Voyager 1 has reached one light-day
  from Earth; the 1977 probe's data flow has stopped.
- **India / Storms** — Cyclone Akvan bears down on the Odisha
  coast; 300,000 evacuated, 423 rescue teams deployed.
- **Ukraine / Europe** — Europe says it is ready for talks with
  Russia to end the war.

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
Russia talks, and the items in the footer (GTA 6 sales, the Hormuz
tanker fire, Hayabusa2, North Korea's Yongbyon expansion).

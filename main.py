"""20 November 2026 world news, drawn as one image.

This is the entrypoint for the make.fun bounty
"Sum up 20 November's world news in one image"
(news-image-20261120). The finished picture lives in this
repository as entry.png: a verified broadsheet drawn with PIL
by make_image.py (lead illustration, world map, date check,
34 stories, UTC timeline). All this program does is place a
copy of that picture where the grader looks for it.

It uses only the Python standard library, touches no network,
and always writes the same bytes, because entry.png itself
never changes between runs.
"""

import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PICTURE = HERE / "entry.png"


def output_dir():
    target = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = Path(target)
    path.mkdir(parents=True, exist_ok=True)
    return path


def main():
    if not PICTURE.is_file():
        sys.exit(f"missing {PICTURE}")
    destination = output_dir() / "entry.png"
    shutil.copyfile(PICTURE, destination)
    print(f"wrote {destination}")


if __name__ == "__main__":
    main()

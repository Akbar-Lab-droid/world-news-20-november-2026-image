"""Sum up 20 November 2026 world news in one image.

The image is entry.png beside this file, drawn with PIL from the
day's reported news (see README.md). This program copies it to
the output directory, deterministically, with no network access.
It uses only the standard library, so it runs in the grader's
minimal image without Pillow installed.
Run locally: mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
import sys
from pathlib import Path


def main():
    src = Path(__file__).resolve().parent / "entry.png"
    if not src.is_file():
        sys.exit(f"missing source image: {src}")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    shutil.copyfile(src, dest)
    print("wrote", dest)


if __name__ == "__main__":
    main()

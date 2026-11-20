"""World News 20 November 2026 in a single image.

Entry for make.fun's "Sum up 20 November's world news in one
image" bounty (news-image-20261120). The picture itself is
entry.png, kept in this repository and drawn from the day's
reported news. Running this program places a copy of that
picture at the output location the grader reads. It needs
nothing beyond the Python standard library, reaches no
network, and writes the same bytes every time it runs.
"""

import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    image = ROOT / "entry.png"
    if not image.is_file():
        sys.exit("entry.png not found next to main.py")
    output = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(image, output / "entry.png")
    print("wrote", output / "entry.png")


if __name__ == "__main__":
    main()

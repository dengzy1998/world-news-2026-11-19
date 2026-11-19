#!/usr/bin/env python3
"""Competition entry point for make.fun bounty news-image-20261119.

Copies this repository's pre-rendered front page (entry.png, drawn in code
by make_image.py) to /output/entry.png. Standard library only — the grader
image has no Pillow, so this program must not import it.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST_DIR = "/output"
DST = os.path.join(DST_DIR, "entry.png")


def main():
    if not os.path.isfile(SRC):
        print("error: entry.png not found next to main.py", file=sys.stderr)
        return 1
    os.makedirs(DST_DIR, exist_ok=True)
    shutil.copyfile(SRC, DST)
    print("wrote", DST, os.path.getsize(DST), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())

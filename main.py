#!/usr/bin/env python3
"""news-image-20261120 entry (Python 3.13, standard library only).

The image is the entry.png beside this file: a newspaper front page summing
up the world's news of Friday 20 November 2026, drawn with PIL at build
time (see draw.py) and committed to the repository. The program copies it to
/output/entry.png (MAKEFUN_OUTPUT_DIR stands in for /output outside the
grader's container), so both runs write the same bytes.

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    # A plain copy: no network, no clock, no randomness, so the two graded
    # runs write byte-identical files.
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "entry.png"),
                    os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()

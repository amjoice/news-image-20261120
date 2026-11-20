#!/usr/bin/env python3
"""Deliver the finished front page for Friday 20 November 2026.

The artwork itself already exists in this repository as entry.png.
This program's only job is to carry that finished image, unchanged,
into the directory the harness asks for, so the run's output is the
front page and nothing else.

Nothing here reaches the network, reads the clock, or rolls any dice:
the same input always yields the same output, byte for byte.
"""

import os
import sys
from pathlib import Path

# Name of the finished artwork that ships with this repository.
ARTWORK_NAME = "entry.png"

# Where to put the output when the harness does not say otherwise.
DEFAULT_OUTPUT_DIR = "/output"


def artwork_path():
    """Return the path of the artwork sitting next to this program."""
    return Path(__file__).resolve().parent / ARTWORK_NAME


def destination_path():
    """Return where the artwork should land for this run."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT_DIR
    return Path(chosen) / ARTWORK_NAME


def carry_artwork(source, target):
    """Move the artwork's bytes from source to target, untouched.

    The bytes are read in full and then written out again, so the file
    that lands in the output directory is an exact copy of the one
    that ships in the repository.
    """
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = source.read_bytes()
    target.write_bytes(payload)
    return len(payload)


def main():
    source = artwork_path()
    if not source.is_file():
        print(f"missing artwork: {source}", file=sys.stderr)
        return 1
    target = destination_path()
    size = carry_artwork(source, target)
    print(f"published {ARTWORK_NAME} ({size} bytes) to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

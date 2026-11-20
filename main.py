"""Entrypoint for the news-image-20261120 entry.

Renders the day's front page with build_image.render and writes it to
the harness output directory as entry.png. The drawing is pure PIL
with fixed inputs, so two runs produce byte-identical files.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_image import render


def output_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        return os.path.join(out_dir, "entry.png")
    if os.path.isdir("/output") and os.access("/output", os.W_OK):
        return "/output/entry.png"
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, "entry.png")


def main():
    path = output_path()
    render(path)
    size = os.path.getsize(path)
    print(f"wrote {path} ({size} bytes)")


if __name__ == "__main__":
    main()

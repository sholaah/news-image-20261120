"""Entrypoint for the news-image-20261120 entry.

The cover image is rendered ahead of time by build_image.py (pure PIL,
fixed inputs, byte-identical output) and committed to this repository
as entry.png. This entrypoint only copies that file to the harness
output directory, using nothing beyond the standard library, so the
run cannot fail on fonts, imaging libraries, or sandbox differences.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def output_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        return os.path.join(out_dir, "entry.png")
    if os.path.isdir("/output") and os.access("/output", os.W_OK):
        return "/output/entry.png"
    out_dir = os.path.join(HERE, "output")
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, "entry.png")


def main():
    if not os.path.isfile(SOURCE):
        print("entry.png is missing beside main.py", file=sys.stderr)
        return 1
    dest = output_path()
    shutil.copyfile(SOURCE, dest)
    with open(dest, "rb") as fh:
        head = fh.read(8)
    if head != b"\x89PNG\r\n\x1a\n":
        print("copied file is not a PNG", file=sys.stderr)
        return 1
    size = os.path.getsize(dest)
    print(f"wrote {dest} ({size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

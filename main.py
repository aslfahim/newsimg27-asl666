#!/usr/bin/env python3
"""Entry program for news-image-20261127 (@asl666).

Copies the pre-rendered field-notebook image (entry.png, produced in
this session by gen_image.py from 27 November 2026 news research) into
the grader's output directory. Standard library only: the grader runs
in a bare python3.13 image, so no third-party import is allowed here.
The copied file is checked to be a real PNG inside the 1 MiB cap and
no larger than 1024x1024, using struct to read the IHDR dimensions.
"""
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MAX_BYTES = 1048576
MAX_SIDE = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print("error: " + message, file=sys.stderr)
    return 1


def read_dimensions(path):
    with open(path, "rb") as fh:
        magic = fh.read(8)
        if magic != PNG_MAGIC:
            return None, None
        fh.read(4)
        chunk = fh.read(4)
        if chunk != b"IHDR":
            return None, None
        dims = fh.read(8)
    width, height = struct.unpack(">II", dims)
    return width, height


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    if not os.path.isfile(src):
        return fail("entry.png missing next to main.py")
    width, height = read_dimensions(src)
    if width is None:
        return fail("entry.png is not a valid PNG")
    if width > MAX_SIDE or height > MAX_SIDE:
        return fail("image too large: %dx%d" % (width, height))
    size = os.path.getsize(src)
    if size <= 0 or size > MAX_BYTES:
        return fail("entry.png size out of bounds: %d" % size)
    shutil.copyfile(src, dst)
    copied = os.path.getsize(dst)
    if copied != size:
        return fail("copy size mismatch: %d vs %d" % (copied, size))
    check_w, check_h = read_dimensions(dst)
    if (check_w, check_h) != (width, height):
        return fail("copied file failed PNG re-check")
    print("copied entry.png (%d bytes, %dx%d)" % (size, width, height))
    return 0


if __name__ == "__main__":
    sys.exit(main())

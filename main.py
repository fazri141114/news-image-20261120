#!/usr/bin/env python3
"""Entrypoint for the make.fun bounty "Sum up 20 November's world news
in one image" (news-image-20261120), second submission.

The entry image is the finished front page shipped in this repository
as entry.png ("THE WORLD IN ONE DAY — Friday 20 November 2026", an
illustrated one-page summary of the day). This program verifies the
file against the bounty's limits and copies it, byte for byte, to the
output path the runner reads:

    python3 main.py [output-dir]        (default output-dir: /output)

Standard library only. Running it twice produces byte-identical
output, because the copy is a pure function of the shipped file.
"""

import hashlib
import os
import struct
import sys

MAX_BYTES = 1_048_576  # 1 MiB
MAX_SIDE = 1024        # pixels, either dimension
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def png_dimensions(data):
    """(width, height) from the IHDR chunk of a PNG byte string."""
    if data[:8] != PNG_SIGNATURE:
        raise ValueError("entry.png is not a PNG file")
    if data[12:16] != b"IHDR":
        raise ValueError("entry.png has no IHDR chunk")
    return struct.unpack(">II", data[16:24])


def verified_bytes(path):
    """Read entry.png and check it against the bounty's limits."""
    with open(path, "rb") as fh:
        data = fh.read()
    if len(data) > MAX_BYTES:
        raise ValueError(f"entry.png is {len(data)} bytes, over the 1 MiB limit")
    width, height = png_dimensions(data)
    if width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError(f"entry.png is {width}x{height}, over the 1024x1024 limit")
    return data


def main(argv):
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = argv[1] if len(argv) > 1 else "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")

    data = verified_bytes(source)
    if os.path.abspath(source) == os.path.abspath(target):
        raise ValueError("output path would overwrite the shipped entry.png")
    with open(target, "wb") as fh:
        fh.write(data)

    # The copy must be exact; fail loudly rather than ship a bad entry.
    digest = hashlib.sha256(data).hexdigest()
    with open(target, "rb") as fh:
        if hashlib.sha256(fh.read()).hexdigest() != digest:
            raise IOError("copied entry.png differs from the source")
    print(f"entry.png verified and copied to {target} "
          f"({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

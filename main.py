#!/usr/bin/env python3
"""
Entry program for the make.fun bounty "Sum up 20 November's world
news in one image" (news-image-20261120), entered by @fazri141114.

The front page itself - WORLD NEWS DAILY, Friday 20 November 2026,
30 stories on one portrait page - was drawn by build_image_20.py
and ships in this repository as entry.png. The contest sandbox
runs this file instead: pure Python 3 standard library, no network,
no third-party imports.

What it does: read entry.png (the copy stored next to this file,
falling back to the working directory), prove it is a complete PNG
inside the contest limits - at most 1 MiB, at most 1024x1024, every
chunk's CRC32 intact, nothing after IEND - then write the identical
bytes to the output directory: $MAKEFUN_OUTPUT_DIR when the grader
sets it, otherwise /output. Every run produces the same bytes.
An optional positional argument names the output directory instead
(it beats the environment variable); the sandbox passes neither.

    python3 main.py [output-dir]
"""

import binascii
import os
import struct
import sys

LIMIT_BYTES = 1024 * 1024
LIMIT_SIDE = 1024
SIGNATURE = b"\x89PNG\r\n\x1a\n"


def png_chunks(blob):
    """Yield (type, payload) for each chunk of a PNG byte string."""
    if blob[:8] != SIGNATURE:
        raise ValueError("missing PNG signature")
    pos = 8
    while pos < len(blob):
        if pos + 12 > len(blob):
            raise ValueError("chunk runs past the end of the file")
        (size,) = struct.unpack(">I", blob[pos:pos + 4])
        ctype = blob[pos + 4:pos + 8]
        payload = blob[pos + 8:pos + 8 + size]
        (crc,) = struct.unpack(">I", blob[pos + 8 + size:pos + 12 + size])
        if len(payload) != size:
            raise ValueError("chunk payload is truncated")
        if binascii.crc32(ctype + payload) & 0xFFFFFFFF != crc:
            raise ValueError(f"CRC32 mismatch in chunk {ctype!r}")
        yield ctype, payload
        pos += 12 + size
    if pos != len(blob):
        raise ValueError("trailing bytes after the last chunk")


def validate(blob):
    """Check the contest limits; return the image's (width, height)."""
    if len(blob) > LIMIT_BYTES:
        raise ValueError(f"{len(blob)} bytes exceeds the 1 MiB limit")
    size = None
    closed = False
    for ctype, payload in png_chunks(blob):
        if ctype == b"IHDR":
            size = struct.unpack(">II", payload[:8])
        elif ctype == b"IEND":
            closed = True
    if size is None:
        raise ValueError("no IHDR chunk")
    if not closed:
        raise ValueError("no IEND chunk")
    if size[0] > LIMIT_SIDE or size[1] > LIMIT_SIDE:
        raise ValueError(f"{size[0]}x{size[1]} exceeds the 1024x1024 limit")
    return size


def entry_bytes():
    """Load entry.png from beside this file, else from the cwd."""
    beside = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    path = beside if os.path.isfile(beside) else os.path.join(os.getcwd(), "entry.png")
    with open(path, "rb") as fh:
        return fh.read()


def run(argv):
    blob = entry_bytes()
    width, height = validate(blob)
    if len(argv) > 1:
        out_dir = argv[1]
    else:
        out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    with open(dest, "wb") as fh:
        fh.write(blob)
    print(f"wrote {dest} ({len(blob)} bytes, {width}x{height})")
    return 0


if __name__ == "__main__":
    sys.exit(run(sys.argv))

#!/usr/bin/env python3
"""news-23 b181 numbers-led entrypoint (stdlib only, no PIL).

Reads entry.png next to this file, validates the PNG header and chunks
(manual parse with struct/zlib), and writes the validated bytes to
$MAKEFUN_OUTPUT_DIR/entry.png. Refuses to write anywhere inside the repo,
to an empty/missing output dir, or over the source file.
"""
import hashlib
import os
import struct
import sys
import zlib

EXPECTED_SHA256 = "1eed0325e539b2c8ea1e03c6d2be1a83c29c6de6c92f4f2c845efa1b40930624"  # filled after the first verified run
EXPECTED_SIZE = 165650

SOURCE_NAME = "entry.png"
PNG_SIG = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024
MIN_BYTES = 10000


def fail(msg):
    print(f"error: {msg}", file=sys.stderr)
    return 1


def parse_png(data):
    """Validate PNG structure; return (width, height) or raise ValueError."""
    if len(data) < 8 or data[:8] != PNG_SIG:
        raise ValueError("bad PNG signature")
    if len(data) < 33:
        raise ValueError("file too small for IHDR")
    length, ctype = struct.unpack(">I4s", data[8:16])
    if ctype != b"IHDR" or length != 13:
        raise ValueError("first chunk must be a 13-byte IHDR")
    ihdr = data[16:29]
    width, height, depth, ctype2, comp, filt, interlace = struct.unpack(
        ">IIBBBBB", ihdr)
    if width != 1024 or height != 1024:
        raise ValueError(f"expected 1024x1024, got {width}x{height}")
    if depth != 8 or ctype2 not in (2, 6):
        raise ValueError(f"unsupported bit depth {depth} / colour type {ctype2}")
    if comp != 0 or filt != 0 or interlace != 0:
        raise ValueError("unsupported compression/filter/interlace")
    if zlib.crc32(b"IHDR" + ihdr) & 0xFFFFFFFF != struct.unpack(
            ">I", data[29:33])[0]:
        raise ValueError("IHDR CRC mismatch")
    # walk chunks
    pos = 8
    idat_total = 0
    seen_iend = False
    while pos < len(data):
        if pos + 8 > len(data):
            raise ValueError("truncated chunk header")
        clen, ctype = struct.unpack(">I4s", data[pos:pos + 8])
        if pos + 12 + clen > len(data):
            raise ValueError(f"truncated chunk {ctype!r}")
        body = data[pos + 8:pos + 8 + clen]
        crc_stored = struct.unpack(">I", data[pos + 8 + clen:pos + 12 + clen])[0]
        if zlib.crc32(ctype + body) & 0xFFFFFFFF != crc_stored:
            raise ValueError(f"CRC mismatch in {ctype!r} chunk")
        if ctype == b"IDAT":
            if clen == 0:
                raise ValueError("empty IDAT chunk")
            idat_total += clen
        if ctype == b"IEND":
            if clen != 0:
                raise ValueError("IEND must be empty")
            if pos + 12 + clen != len(data):
                raise ValueError("trailing data after IEND")
            seen_iend = True
            break
        pos += 12 + clen
    if not seen_iend:
        raise ValueError("missing IEND chunk")
    if idat_total < 1000:
        raise ValueError("IDAT payload too small")
    return width, height


def main():
    here = os.path.dirname(os.path.realpath(__file__))
    src = os.path.join(here, SOURCE_NAME)
    if not os.path.isfile(src):
        return fail(f"source not found: {src}")
    with open(src, "rb") as fh:
        data = fh.read()
    if len(data) < MIN_BYTES:
        return fail(f"file too small: {len(data)} bytes")
    if len(data) > MAX_BYTES:
        return fail(f"file too large: {len(data)} bytes (>1 MiB)")
    try:
        parse_png(data)
    except ValueError as exc:
        return fail(str(exc))
    digest = hashlib.sha256(data).hexdigest()
    if EXPECTED_SHA256 and digest != EXPECTED_SHA256:
        return fail(f"sha256 mismatch: got {digest}")
    if EXPECTED_SIZE and len(data) != EXPECTED_SIZE:
        return fail(f"size mismatch: got {len(data)}")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_real = os.path.realpath(out_dir)
    if out_dir_real == here or out_dir_real.startswith(here + os.sep):
        return fail("MAKEFUN_OUTPUT_DIR must be outside the repo")
    if os.path.exists(out_dir_real) and not os.path.isdir(out_dir_real):
        return fail("MAKEFUN_OUTPUT_DIR is not a directory")
    os.makedirs(out_dir_real, exist_ok=True)
    dst = os.path.join(out_dir_real, "entry.png")
    if os.path.realpath(dst) == os.path.realpath(src):
        return fail("output would overwrite the source")
    with open(dst, "wb") as fh:
        fh.write(data)
    with open(dst, "rb") as fh:
        back = fh.read()
    if back != data:
        return fail("output differs from source after write")
    print(f"ok: wrote {dst} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

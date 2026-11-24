#!/usr/bin/env python3
"""news-image-20261124: deliver the 24 November front page as /output/entry.png.

The picture itself lives in this repository as entry.png (drawn by
render.py from the verified 24 November 2026 stories listed in
README.md). This script is the entrypoint the bounty runs: it checks
the picture thoroughly, then places a verified copy at
/output/entry.png.

Checks (standard library only, no network, deterministic):
  * the eight-byte PNG signature is present;
  * the IHDR chunk declares a 1024 by 1024 picture;
  * every chunk's CRC matches the bytes it covers, so a flipped
    byte anywhere in the file is caught, not just a cut-off tail;
  * the chunk stream ends with an IEND chunk;
  * the file stays within the bounty's one-mebibyte limit.
A failed check prints why to stderr and exits non-zero.
After copying, the copy is checked the same way and its SHA-256
is compared with the source's, so a bad copy cannot slip through.
The copy is left world-readable: make.fun collects it as another user.
"""
import hashlib
import os
import shutil
import struct
import sys
import zlib

BASE = os.path.dirname(os.path.abspath(__file__))
PICTURE = os.path.join(BASE, "entry.png")
TARGET = "/output/entry.png"

SIGNATURE = b"\x89PNG\r\n\x1a\n"
SIDE = 1024
LIMIT = 1024 * 1024


def complain(text):
    """Report a problem on stderr and return the failure exit code."""
    print("rejected: " + text, file=sys.stderr)
    return 1


def walk_chunks(blob):
    """Yield (kind, payload) for each chunk of a PNG byte string.

    Raises ValueError on a short header, a short chunk, or a chunk
    whose stored CRC disagrees with its type and payload.
    """
    if blob[:8] != SIGNATURE:
        raise ValueError("missing PNG signature")
    pos = 8
    while pos < len(blob):
        if pos + 8 > len(blob):
            raise ValueError("truncated chunk header")
        size, kind = struct.unpack(">I4s", blob[pos:pos + 8])
        start = pos + 8
        end = start + size
        if end + 4 > len(blob):
            raise ValueError("truncated chunk %r" % kind.decode("latin1"))
        payload = blob[start:end]
        (stored_crc,) = struct.unpack(">I", blob[end:end + 4])
        actual_crc = zlib.crc32(kind)
        actual_crc = zlib.crc32(payload, actual_crc)
        if stored_crc != (actual_crc & 0xFFFFFFFF):
            raise ValueError("bad CRC in chunk %r" % kind.decode("latin1"))
        yield kind, payload
        pos = end + 4
        if kind == b"IEND":
            break
    else:
        raise ValueError("no IEND chunk")


def inspect(path):
    """Check the PNG at *path*; return (width, height) or None.

    Every failure is reported through complain() before returning None.
    """
    try:
        size = os.path.getsize(path)
    except OSError as exc:
        complain("%s: cannot stat (%s)" % (path, exc))
        return None
    if size > LIMIT:
        complain("%s is %d bytes, over the 1 MiB limit" % (path, size))
        return None
    with open(path, "rb") as handle:
        blob = handle.read()
    try:
        chunks = list(walk_chunks(blob))
    except ValueError as exc:
        complain("%s: %s" % (path, exc))
        return None
    kinds = [kind for kind, _ in chunks]
    if b"IHDR" not in kinds or kinds[0] != b"IHDR":
        complain("%s: first chunk is not IHDR" % path)
        return None
    if kinds[-1] != b"IEND":
        complain("%s: last chunk is not IEND" % path)
        return None
    width, height = struct.unpack(">II", chunks[0][1][:8])
    if (width, height) != (SIDE, SIDE):
        complain("%s is %dx%d, expected %dx%d"
                 % (path, width, height, SIDE, SIDE))
        return None
    return width, height


def fingerprint(path):
    """SHA-256 hex digest of a file, streamed in blocks."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def run():
    if not os.path.exists(PICTURE):
        return complain("entry.png not found next to main.py")
    dims = inspect(PICTURE)
    if dims is None:
        return 1
    width, height = dims
    digest = fingerprint(PICTURE)
    os.makedirs(os.path.dirname(TARGET), exist_ok=True)
    shutil.copyfile(PICTURE, TARGET)
    os.chmod(TARGET, 0o644)
    # Check the copy, not just the source: it must pass the same
    # inspection and be byte-for-byte the file that was checked.
    if inspect(TARGET) is None:
        return complain("copied file %s failed inspection" % TARGET)
    if fingerprint(TARGET) != digest:
        return complain("copied file %s differs from source" % TARGET)
    size = os.path.getsize(TARGET)
    print("OK: %s - %dx%d PNG, %d bytes, sha256 %s (copy verified)"
          % (TARGET, width, height, size, digest))
    return 0


if __name__ == "__main__":
    raise SystemExit(run())

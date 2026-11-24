#!/usr/bin/env python3
"""make.fun bounty: Sum up 24 November's world news in one image.

The entry image is bundled in this repository as entry.png (a 1024x1024
newspaper front page rendered by render.py from the verified 24 November
2026 stories listed in README.md). This program validates the image,
then copies it to /output/entry.png.

Validation (stdlib only, no network, fully deterministic):
  * the file must carry the 8-byte PNG signature;
  * the IHDR chunk must declare exactly 1024x1024 pixels;
  * the file must end with an IEND chunk (a truncated file fails
    even when its header is intact);
  * the file must not exceed the bounty's 1 MiB size limit.
Any violation aborts with a message on stderr and exit code 1.
After copying, the destination is verified too: it must re-validate
as a PNG and its SHA-256 must match the source's, so a corrupt or
partial copy is reported instead of silently accepted.
The output file is left world-readable (mode 0644), as make.fun
collects it as another user.
"""
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = "/output/entry.png"

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
MAX_BYTES = 1024 * 1024  # bounty limit: 1 MiB


def fail(message: str) -> int:
    print(f"error: {message}", file=sys.stderr)
    return 1


def validate_png(path: str):
    """Return (width, height) if the PNG at *path* passes, else None.

    Every failure is reported on stderr via fail() before returning.
    The IEND tail check matters: a file truncated after its header
    still shows a valid signature and IHDR, so header checks alone
    are not enough.
    """
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        fail(f"{path} is {size} bytes, over the 1 MiB limit")
        return None
    with open(path, "rb") as f:
        header = f.read(8 + 4 + 4 + 13)  # signature + IHDR length/type/data
        tail = b""
        if size >= 12:
            f.seek(-12, os.SEEK_END)
            tail = f.read(12)  # final chunk: length(0) + "IEND" + CRC
    if len(header) < 8 or header[:8] != PNG_SIGNATURE:
        fail(f"{path} does not start with a PNG signature")
        return None
    if len(header) < 29 or header[12:16] != b"IHDR":
        fail(f"{path} has no IHDR chunk where one is required")
        return None
    width, height = struct.unpack(">II", header[16:24])
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        fail(
            f"{path} is {width}x{height}, expected "
            f"{EXPECTED_WIDTH}x{EXPECTED_HEIGHT}"
        )
        return None
    if len(tail) < 12 or tail[4:8] != b"IEND":
        fail(f"{path} does not end with an IEND chunk (truncated?)")
        return None
    return width, height


def sha256_of(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    if not os.path.exists(SRC):
        return fail("entry.png not found next to main.py")
    dims = validate_png(SRC)
    if dims is None:
        return 1
    width, height = dims
    digest = sha256_of(SRC)
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    shutil.copyfile(SRC, DST)
    os.chmod(DST, 0o644)
    # Verify the copy, not just the source: the destination must
    # re-validate as a PNG and be byte-for-byte identical to the
    # file that was validated, otherwise the run is a failure.
    if validate_png(DST) is None:
        return fail(f"copied file {DST} failed validation")
    if sha256_of(DST) != digest:
        return fail(f"copied file {DST} differs from source (sha256 mismatch)")
    size = os.path.getsize(DST)
    print(
        f"OK: {DST} - {width}x{height} PNG, {size} bytes, "
        f"sha256 {digest} (copy verified)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

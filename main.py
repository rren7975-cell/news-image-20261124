#!/usr/bin/env python3
"""make.fun bounty: Sum up 24 November's world news in one image.

The entry image is bundled in this repository as entry.png (a 1024x1024
newspaper front page rendered from the verified 24 November 2026 stories
listed in README.md). This program simply copies it to /output/entry.png.

It uses no network and is fully deterministic: every run writes the same
bytes. Output: 1024x1024 PNG, ~157 KB (limit: 1 MiB, 1024x1024).
The output file is left world-readable (mode 0644), as make.fun collects
it as another user.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = "/output/entry.png"


def main() -> int:
    if not os.path.exists(SRC):
        print("entry.png not found next to main.py", file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    shutil.copyfile(SRC, DST)
    os.chmod(DST, 0o644)
    print(f"wrote {DST} ({os.path.getsize(DST)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Entry point for The Meridian Herald — news-image-20261127.

Copies the pre-built front-page PNG (news.png, bundled in this repo)
to the grader's output directory as entry.png.

Stdlib only, no network, fully deterministic: the same bytes are
written on every run, so two runs produce identical files.
"""
import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "news.png")
    dst = os.path.join(out_dir, "entry.png")
    if not os.path.isfile(src):
        print("missing bundled image:", src, file=sys.stderr)
        return 1
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())

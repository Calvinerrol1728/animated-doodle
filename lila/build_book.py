#!/usr/bin/env python3
"""
Build a print-ready children's picture book PDF from page images.

Usage:
    python3 build_book.py [--out princess_lila_and_the_little_dragon.pdf]

Reads page images from ./pages in filename order (00_cover.png, 01_*.png, ...),
fits each onto an 8.5 x 11 in portrait page at 300 DPI, and writes a single PDF.
"""
import argparse
import glob
import os
import sys

from PIL import Image

PAGE_W_IN, PAGE_H_IN = 8.5, 11.0
DPI = 300
PAGE_W = int(PAGE_W_IN * DPI)   # 2550
PAGE_H = int(PAGE_H_IN * DPI)   # 3300
BG = (255, 253, 247)            # warm ivory, matches the book's palette


def fit_to_page(img: Image.Image) -> Image.Image:
    """Scale image to cover the page, center-crop the overflow."""
    img = img.convert("RGB")
    scale = max(PAGE_W / img.width, PAGE_H / img.height)
    new = img.resize(
        (max(1, round(img.width * scale)), max(1, round(img.height * scale))),
        Image.LANCZOS,
    )
    left = (new.width - PAGE_W) // 2
    top = (new.height - PAGE_H) // 2
    new = new.crop((left, top, left + PAGE_W, top + PAGE_H))
    canvas = Image.new("RGB", (PAGE_W, PAGE_H), BG)
    canvas.paste(new, (0, 0))
    return canvas


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", default="lila/pages", help="directory of page images")
    ap.add_argument(
        "--out",
        default="princess_lila_and_the_little_dragon.pdf",
        help="output PDF path",
    )
    args = ap.parse_args()

    files = sorted(
        f
        for ext in ("png", "jpg", "jpeg")
        for f in glob.glob(os.path.join(args.pages, f"*.{ext}"))
    )
    if not files:
        print(f"No page images found in {args.pages}/", file=sys.stderr)
        return 1

    print(f"Assembling {len(files)} pages at {PAGE_W}x{PAGE_H}px ({DPI} DPI)")
    rendered = []
    for f in files:
        print("  +", os.path.basename(f))
        rendered.append(fit_to_page(Image.open(f)))

    rendered[0].save(
        args.out,
        "PDF",
        resolution=DPI,
        save_all=True,
        append_images=rendered[1:],
        title="Princess Lila and the Little Dragon Who Was Afraid to Fly",
        author="A Story About Courage, Friendship, and Trying Again",
    )
    size_mb = os.path.getsize(args.out) / 1e6
    print(f"Wrote {args.out} ({len(rendered)} pages, {size_mb:.1f} MB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

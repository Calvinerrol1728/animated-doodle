#!/usr/bin/env python3
"""
Build the print-ready package for
"Princess Elara and the Secret Garden of Stars".

Outputs (into ./print):
  1. interior_print_bleed.pdf  — 24-page interior, 8.75 x 11.25 in (8.5 x 11 trim
     + 0.125 in bleed on all sides), 300 DPI, front/back matter typeset as vector
     text with embedded fonts.
  2. cover_wrap_print.pdf      — full wrap-around cover (back + spine + front)
     sized from the KDP spine formula, with the barcode zone kept clear.

Specs applied (Amazon KDP / IngramSpark paperback):
  * 0.125" bleed on all four outer edges
  * 300 DPI raster art
  * 24-page interior minimum (KDP paperback)
  * Spine = pages x 0.002347" (color interior) + 0.06"
  * Barcode zone 2" x 1.2", >= 0.25" from trim, lower right of back cover
  * Safe margin: nothing important within 0.5" of trim or spine

Usage:  python3 build_print.py
"""
import os

from PIL import Image
from reportlab.lib.colors import Color, HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as rl_canvas

# ----------------------------------------------------------------------------
# YOUR DETAILS LIVE IN  book_details.txt  — edit that file, not this one.
# ----------------------------------------------------------------------------
def load_details():
    """Read book_details.txt into a dict, with sensible fallbacks."""
    defaults = {
        "author": "[YOUR NAME]",
        "publisher": "[YOUR IMPRINT]",
        "year": "2026",
        "isbn": "",
        "dedication": "For every child who stops to help\nsomething small.",
    }
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "book_details.txt")
    if not os.path.exists(path):
        return defaults
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.split("#", 1)[0].strip()
            if not line or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip().lower()
            if key in defaults:
                defaults[key] = value.strip().replace("\\n", "\n")
    return defaults


_D = load_details()
AUTHOR = _D["author"]
PUBLISHER = _D["publisher"]
YEAR = _D["year"]
ISBN = _D["isbn"]
DEDICATION = _D["dedication"]

# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------
IN = 72.0                       # points per inch
TRIM_W, TRIM_H = 8.5, 11.0
BLEED = 0.125
PAGE_W, PAGE_H = TRIM_W + 2 * BLEED, TRIM_H + 2 * BLEED   # 8.75 x 11.25
DPI = 300
PAPER_PER_PAGE = 0.002347       # KDP color interior
COVER_ALLOWANCE = 0.06
BARCODE_W, BARCODE_H = 2.0, 1.2

IVORY = HexColor("#FFFDF7")
CREAM = HexColor("#FBF5E6")
BROWN = HexColor("#4A3728")
VIOLET = HexColor("#3A3560")
GOLD = HexColor("#C9A227")
SAGE = HexColor("#8AA07C")

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = os.path.join(HERE, "pages")
FONTS = os.path.join(HERE, "fonts")
OUT = os.path.join(HERE, "print")
TMP = os.path.join(OUT, ".tmp")

STORY_PAGES = [
    "03_p01.png", "04_p02.png", "05_p03.png", "06_p04.png", "07_p05.png",
    "08_p06.png", "09_p07.png", "10_p08.png", "11_p09.png", "12_p10.png",
    "13_p11.png", "14_p12.png", "15_p13.png",
]


def register_fonts():
    pairs = [
        ("Serif", "SourceSerifPro-Regular.ttf"),
        ("Serif-Bold", "SourceSerifPro-Bold.ttf"),
        ("Serif-It", "SourceSerifPro-It.ttf"),
        ("Serif-Semi", "SourceSerifPro-Semibold.ttf"),
        ("Story", "FredokaOne-Regular.ttf"),
        ("Hand", "AmaticSC-Bold.ttf"),
    ]
    for name, fn in pairs:
        pdfmetrics.registerFont(TTFont(name, os.path.join(FONTS, fn)))


# ----------------------------------------------------------------------------
# Raster helpers
# ----------------------------------------------------------------------------
def add_bleed(src_path, out_path):
    """Scale art to trim size, then extend the outermost pixels into the bleed.

    Edge replication keeps every drawn element (decorative borders, bubbles)
    safely inside the trim while guaranteeing ink coverage out to the bleed,
    so trimming can never leave a white sliver.
    """
    trim_w, trim_h = int(TRIM_W * DPI), int(TRIM_H * DPI)
    b = int(BLEED * DPI)
    full_w, full_h = trim_w + 2 * b, trim_h + 2 * b

    art = Image.open(src_path).convert("RGB").resize((trim_w, trim_h), Image.LANCZOS)
    canvas = Image.new("RGB", (full_w, full_h))
    canvas.paste(art, (b, b))

    left = art.crop((0, 0, 1, trim_h)).resize((b, trim_h), Image.NEAREST)
    right = art.crop((trim_w - 1, 0, trim_w, trim_h)).resize((b, trim_h), Image.NEAREST)
    canvas.paste(left, (0, b))
    canvas.paste(right, (b + trim_w, b))

    top = canvas.crop((0, b, full_w, b + 1)).resize((full_w, b), Image.NEAREST)
    bot = canvas.crop((0, b + trim_h - 1, full_w, b + trim_h)).resize((full_w, b), Image.NEAREST)
    canvas.paste(top, (0, 0))
    canvas.paste(bot, (0, b + trim_h))

    canvas.save(out_path, "JPEG", quality=94, subsampling=0, dpi=(DPI, DPI))
    return out_path


def cover_fit(src_path, out_path, w_in, h_in):
    """Scale to cover w_in x h_in at 300 DPI and center-crop."""
    tw, th = int(w_in * DPI), int(h_in * DPI)
    im = Image.open(src_path).convert("RGB")
    scale = max(tw / im.width, th / im.height)
    im = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))),
                   Image.LANCZOS)
    l, t = (im.width - tw) // 2, (im.height - th) // 2
    im.crop((l, t, l + tw, t + th)).save(out_path, "JPEG", quality=95, subsampling=0, dpi=(DPI, DPI))
    return out_path


# ----------------------------------------------------------------------------
# Vector text helpers
# ----------------------------------------------------------------------------
def centered(c, text, font, size, y, color=BROWN, cx=None, tracking=0):
    c.setFont(font, size)
    c.setFillColor(color)
    cx = cx if cx is not None else PAGE_W * IN / 2
    c.drawCentredString(cx, y, text)


def wrapped(c, text, font, size, cx, y, max_w, leading, color=BROWN, align="center"):
    c.setFont(font, size)
    c.setFillColor(color)
    words, line, lines = text.split(), "", []
    for w in words:
        t = (line + " " + w).strip()
        if pdfmetrics.stringWidth(t, font, size) <= max_w:
            line = t
        else:
            lines.append(line)
            line = w
    if line:
        lines.append(line)
    for ln in lines:
        if align == "center":
            c.drawCentredString(cx, y, ln)
        else:
            c.drawString(cx, y, ln)
        y -= leading
    return y


def star(c, x, y, r, color=GOLD):
    """Small five-pointed decorative star."""
    import math
    c.setFillColor(color)
    p = c.beginPath()
    for i in range(10):
        ang = math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        px, py = x + rr * math.cos(ang), y + rr * math.sin(ang)
        p.moveTo(px, py) if i == 0 else p.lineTo(px, py)
    p.close()
    c.drawPath(p, fill=1, stroke=0)


def star_rule(c, y, n=5, spacing=26, cx=None, r=5):
    cx = cx if cx is not None else PAGE_W * IN / 2
    start = cx - spacing * (n - 1) / 2
    for i in range(n):
        star(c, start + i * spacing, y, r if i == n // 2 else r * 0.72)


def bg(c, color=IVORY, w=None, h=None):
    c.setFillColor(color)
    c.rect(0, 0, w or PAGE_W * IN, h or PAGE_H * IN, fill=1, stroke=0)


# ----------------------------------------------------------------------------
# Interior matter pages
# ----------------------------------------------------------------------------
def page_half_title(c):
    bg(c)
    cx, top = PAGE_W * IN / 2, PAGE_H * IN
    centered(c, "PRINCESS ELARA", "Story", 26, top - 3.9 * IN, VIOLET)
    centered(c, "and the Secret Garden of Stars", "Serif-It", 15, top - 4.4 * IN, BROWN)
    star_rule(c, top - 5.0 * IN, 5)


def page_blank(c):
    bg(c)


def page_title(c):
    bg(c)
    cx, top = PAGE_W * IN / 2, PAGE_H * IN
    star_rule(c, top - 2.5 * IN, 7, spacing=30)
    centered(c, "PRINCESS ELARA", "Story", 34, top - 3.5 * IN, VIOLET)
    centered(c, "AND THE SECRET", "Story", 22, top - 4.15 * IN, VIOLET)
    centered(c, "GARDEN OF STARS", "Story", 22, top - 4.65 * IN, VIOLET)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.1)
    c.line(cx - 1.7 * IN, top - 5.05 * IN, cx + 1.7 * IN, top - 5.05 * IN)
    centered(c, "A Little Story About Kindness,", "Serif-It", 14, top - 5.5 * IN, BROWN)
    centered(c, "Courage, and Wonder", "Serif-It", 14, top - 5.78 * IN, BROWN)
    centered(c, AUTHOR, "Serif-Semi", 13, top - 7.6 * IN, BROWN)
    centered(c, "Written and illustrated by", "Serif-It", 10.5, top - 7.3 * IN, SAGE)
    star_rule(c, top - 8.4 * IN, 5)


def page_copyright(c):
    bg(c)
    cx = PAGE_W * IN / 2
    y = 5.6 * IN
    lines = [
        ("Princess Elara and the Secret Garden of Stars", "Serif-Semi", 10.5),
        ("A Little Story About Kindness, Courage, and Wonder", "Serif-It", 9.5),
        ("", "Serif", 6),
        (f"Copyright \u00a9 {YEAR} by {AUTHOR}", "Serif", 9.5),
        ("All rights reserved.", "Serif", 9.5),
        ("", "Serif", 6),
    ]
    for txt, f, s in lines:
        if txt:
            centered(c, txt, f, s, y, BROWN)
        y -= s * 1.7

    body = ("No part of this book may be reproduced, stored in a retrieval system, "
            "or transmitted in any form or by any means \u2014 electronic, mechanical, "
            "photocopying, recording, or otherwise \u2014 without the prior written "
            "permission of the copyright holder, except for brief quotations used "
            "in a review.")
    y = wrapped(c, body, "Serif", 8.8, cx, y, 4.6 * IN, 12.4, BROWN)
    y -= 10

    disclosure = ("The illustrations in this book were created with the assistance of "
                  "generative AI tools and were reviewed, selected, and edited by the "
                  "author. The story text is an original work by the author.")
    y = wrapped(c, disclosure, "Serif-It", 8.8, cx, y, 4.6 * IN, 12.4, BROWN)
    y -= 14

    if PUBLISHER:
        centered(c, PUBLISHER, "Serif", 9, y, BROWN)
        y -= 15
    if ISBN:
        centered(c, f"ISBN: {ISBN}", "Serif", 9, y, BROWN)
        y -= 15
    centered(c, "First Edition", "Serif", 9, y, BROWN)
    y -= 15
    centered(c, "Printed in the United States of America", "Serif", 8.5, y, SAGE)
    star_rule(c, 1.5 * IN, 3, spacing=22, r=4)


def page_dedication(c):
    bg(c)
    cx, top = PAGE_W * IN / 2, PAGE_H * IN
    y = top - 5.0 * IN
    for line in DEDICATION.split("\n"):
        centered(c, line, "Serif-It", 15, y, BROWN)
        y -= 24
    star_rule(c, y - 18, 3, spacing=24, r=4.5)


def page_questions(c):
    bg(c)
    cx, top = PAGE_W * IN / 2, PAGE_H * IN
    centered(c, "Let's Talk About It", "Story", 22, top - 2.2 * IN, VIOLET)
    star_rule(c, top - 2.6 * IN, 5)
    qs = [
        "Elara was afraid of the dark thorn hedge, but she went anyway. "
        "Can you think of a time you felt scared and were brave?",
        "Stopping to help the moth cost Elara time. Why do you think "
        "she helped anyway?",
        "The gate said \u201cKindness opens me.\u201d What do you think "
        "that means?",
        "Nobody ever found out what Elara did. Does a kind act still "
        "count if no one sees it?",
        "What is one small kind thing you could do tomorrow?",
    ]
    # hanging numerals with left-aligned question text beside them
    num_x = 1.65 * IN
    text_x = 2.15 * IN
    text_w = 4.95 * IN
    y = top - 3.5 * IN
    for i, q in enumerate(qs, 1):
        c.setFillColor(GOLD)
        c.setFont("Story", 14)
        c.drawString(num_x, y, str(i))
        y = wrapped(c, q, "Serif", 12.5, text_x, y, text_w, 19, BROWN, align="left")
        y -= 20
    star_rule(c, y - 10, 5)


def page_about(c):
    bg(c)
    cx, top = PAGE_W * IN / 2, PAGE_H * IN
    centered(c, "About This Story", "Story", 22, top - 2.4 * IN, VIOLET)
    star_rule(c, top - 2.8 * IN, 5)
    body = ("Princess Elara and the Secret Garden of Stars was written to be read "
            "aloud at bedtime, in the small quiet minutes before sleep.")
    y = wrapped(c, body, "Serif", 12.5, cx, top - 3.6 * IN, 5.0 * IN, 19, BROWN)
    y -= 14
    body2 = ("It is a story about the kind of courage that is quiet, and the kind "
             "of kindness nobody claps for. Elara helps a small creature when "
             "helping is inconvenient, and that choice is the one that saves her. "
             "Children understand this long before they can explain it.")
    y = wrapped(c, body2, "Serif", 12.5, cx, y, 5.0 * IN, 19, BROWN)
    y -= 26
    centered(c, AUTHOR, "Serif-Semi", 12.5, y, BROWN)
    star_rule(c, 2.4 * IN, 3, spacing=24, r=4.5)


def page_end_flourish(c):
    bg(c)
    cx, top = PAGE_W * IN / 2, PAGE_H * IN
    star_rule(c, top - 5.2 * IN, 7, spacing=30)
    centered(c, "Sweet dreams,", "Serif-It", 15, top - 5.9 * IN, BROWN)
    centered(c, "little one.", "Serif-It", 15, top - 6.2 * IN, BROWN)


# ----------------------------------------------------------------------------
# Build interior
# ----------------------------------------------------------------------------
def build_interior():
    os.makedirs(TMP, exist_ok=True)
    path = os.path.join(OUT, "interior_print_bleed.pdf")
    c = rl_canvas.Canvas(path, pagesize=(PAGE_W * IN, PAGE_H * IN))
    c.setTitle("Princess Elara and the Secret Garden of Stars")
    c.setAuthor(AUTHOR)
    c.setSubject("A Little Story About Kindness, Courage, and Wonder")

    def img_page(src):
        bled = add_bleed(os.path.join(PAGES, src), os.path.join(TMP, "b_" + os.path.splitext(src)[0] + ".jpg"))
        c.drawImage(bled, 0, 0, PAGE_W * IN, PAGE_H * IN)
        c.showPage()

    def txt_page(fn):
        fn(c)
        c.showPage()

    # ---- front matter (5) -------------------------------------------------
    txt_page(page_half_title)     # 1
    txt_page(page_blank)          # 2
    txt_page(page_title)          # 3
    txt_page(page_copyright)      # 4
    txt_page(page_dedication)     # 5

    # ---- story (13) -------------------------------------------------------
    for src in STORY_PAGES:       # 6-18
        img_page(src)

    # ---- ending page (1) --------------------------------------------------
    img_page("99_ending.png")     # 19

    # ---- back matter (5) --------------------------------------------------
    txt_page(page_end_flourish)   # 20
    txt_page(page_questions)      # 21
    txt_page(page_about)          # 22
    txt_page(page_blank)          # 23
    txt_page(page_blank)          # 24

    c.save()
    return path


# ----------------------------------------------------------------------------
# Build wrap cover
# ----------------------------------------------------------------------------
def build_cover(page_count):
    os.makedirs(TMP, exist_ok=True)
    spine = page_count * PAPER_PER_PAGE + COVER_ALLOWANCE
    total_w = 2 * TRIM_W + spine + 2 * BLEED
    total_h = TRIM_H + 2 * BLEED
    path = os.path.join(OUT, "cover_wrap_print.pdf")

    c = rl_canvas.Canvas(path, pagesize=(total_w * IN, total_h * IN))
    c.setTitle("Princess Elara and the Secret Garden of Stars — Cover")

    # background so the spine + any gap is never white
    c.setFillColor(VIOLET)
    c.rect(0, 0, total_w * IN, total_h * IN, fill=1, stroke=0)

    panel_w = TRIM_W + BLEED          # back and front panels each incl. outer bleed
    panel_h = TRIM_H + 2 * BLEED

    # --- back cover (left) -------------------------------------------------
    back = cover_fit(os.path.join(OUT, "back_cover_art.png"),
                     os.path.join(TMP, "back_fit.jpg"), panel_w, panel_h)
    c.drawImage(back, 0, 0, panel_w * IN, panel_h * IN)

    back_cx = (BLEED + TRIM_W / 2) * IN   # centre of back cover trim area

    # soft cream blurb panel in the calm middle region
    c.setFillColor(Color(1, 0.996, 0.965, alpha=0.9))
    c.roundRect(back_cx - 3.25 * IN, 3.55 * IN, 6.5 * IN, 4.3 * IN, 14, fill=1, stroke=0)

    y = 7.2 * IN
    c.setFont("Story", 17)
    c.setFillColor(VIOLET)
    c.drawCentredString(back_cx, y, "The stars are going out.")
    y -= 0.42 * IN
    blurb = ("One by one, the stars above Elara's kingdom are quietly "
             "disappearing. When a small star with a bent point tumbles into "
             "her roses, Elara sets out past the thorn hedge to find the "
             "secret garden where stars are grown.")
    y = wrapped(c, blurb, "Serif", 11.5, back_cx, y, 5.6 * IN, 16.5, BROWN)
    y -= 10
    blurb2 = ("On the way she stops to mend a moth's torn wing \u2014 a small "
              "kindness, and a costly one. At the top of the hill waits a "
              "golden gate with no handle and no key, carved with three "
              "words: Kindness opens me.")
    y = wrapped(c, blurb2, "Serif", 11.5, back_cx, y, 5.6 * IN, 16.5, BROWN)
    y -= 14
    c.setFont("Serif-It", 12)
    c.setFillColor(SAGE)
    c.drawCentredString(back_cx, y, "A bedtime story about the kind of courage")
    c.drawCentredString(back_cx, y - 16, "that is quiet \u2014 for ages 3 to 7.")

    star_rule(c, y - 42, 5, cx=back_cx)

    # barcode keep-out zone: 2 x 1.2 in, >= 0.25 in from trim edges, lower right
    bx = (BLEED + TRIM_W - 0.25 - BARCODE_W) * IN
    by = (BLEED + 0.25) * IN
    c.setFillColor(Color(1, 1, 1, alpha=0.92))
    c.rect(bx, by, BARCODE_W * IN, BARCODE_H * IN, fill=1, stroke=0)

    # --- front cover (right) ----------------------------------------------
    front_x = (BLEED + TRIM_W + spine) * IN
    front = cover_fit(os.path.join(PAGES, "00_cover.png"),
                      os.path.join(TMP, "front_fit.jpg"), panel_w, panel_h)
    c.drawImage(front, front_x, 0, panel_w * IN, panel_h * IN)

    # Spine intentionally left blank. At 24 pages it is ~0.116 in wide; KDP only
    # permits spine text above 0.0625 in but requires 79+ pages in practice, and
    # nothing legible fits at this width.

    c.save()
    return path, spine, total_w, total_h


def strip_unembedded_fonts(path):
    """Remove reportlab's default /Helvetica resource entry.

    It is declared on every page but never drawn with; leaving it in place
    trips printer preflight checks that require all fonts to be embedded.
    """
    from pypdf import PdfReader, PdfWriter
    reader = PdfReader(path)
    writer = PdfWriter()
    removed = 0
    for page in reader.pages:
        res = page.get("/Resources")
        if res is not None:
            res = res.get_object()
            fonts = res.get("/Font")
            if fonts is not None:
                fonts = fonts.get_object()
                for key in [k for k in list(fonts.keys())
                            if "Helvetica" in str(fonts[k].get_object().get("/BaseFont"))]:
                    del fonts[key]
                    removed += 1
        writer.add_page(page)
    writer.add_metadata({
        "/Title": "Princess Elara and the Secret Garden of Stars",
        "/Author": AUTHOR,
        "/Subject": "A Little Story About Kindness, Courage, and Wonder",
    })
    with open(path, "wb") as fh:
        writer.write(fh)
    return removed


def main():
    os.makedirs(OUT, exist_ok=True)
    register_fonts()

    if "[YOUR" in AUTHOR or "[YOUR" in PUBLISHER:
        print("\n" + "!" * 68)
        print("!!  HEADS UP: book_details.txt still has placeholder text.")
        print("!!  These files will literally print '[YOUR NAME]' on the")
        print("!!  title page. Edit book_details.txt and run this again")
        print("!!  before uploading anywhere.")
        print("!" * 68 + "\n")

    interior = build_interior()
    strip_unembedded_fonts(interior)
    from pypdf import PdfReader
    n = len(PdfReader(interior).pages)
    print(f"Interior : {os.path.basename(interior)}  {n} pages  "
          f"{PAGE_W}x{PAGE_H} in (trim {TRIM_W}x{TRIM_H} + {BLEED} bleed)")

    cover, spine, cw, ch = build_cover(n)
    strip_unembedded_fonts(cover)
    print(f"Cover    : {os.path.basename(cover)}  {cw:.4f}x{ch:.4f} in  "
          f"spine {spine:.4f} in")
    print(f"KDP min page count 24 -> {'OK' if n >= 24 else 'FAIL'} ({n})")


if __name__ == "__main__":
    main()

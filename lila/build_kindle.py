#!/usr/bin/env python3
"""
Build the Kindle package for
"Princess Elara and the Secret Garden of Stars".

Outputs (into ./kindle):
  1. kindle_cover_1600x2560.jpg — Amazon ebook cover, exactly 1600 x 2560 px (1.6:1)
  2. princess_elara_kindle.epub — fixed-layout EPUB 3, one illustration per page

Why fixed layout: this is a picture book. The words are baked into the artwork,
so the text must never reflow. Fixed layout keeps every page exactly as drawn,
which is what Amazon expects for children's picture books.

Usage:  python3 build_kindle.py
"""
import os
import shutil
import zipfile
from html import escape

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = os.path.join(HERE, "pages")
OUT = os.path.join(HERE, "kindle")
BUILD = os.path.join(OUT, ".epub_build")

TITLE = "Princess Lila and the Little Dragon Who Was Afraid to Fly"
SUBTITLE = "A Story About Courage, Friendship, and Trying Again"
AUTHOR = "Cedric Errol Cajelo"
LANG = "en"
BOOK_ID = "urn:uuid:lila-little-dragon-afraid-to-fly-0001"

# Amazon ebook cover spec
COVER_W, COVER_H = 1600, 2560

# Interior page size for the fixed-layout viewport (8.5 x 11 at 150 ppi)
PAGE_W, PAGE_H = 1275, 1650

PAGE_ORDER = [
    ("00_cover.png", "Cover"),
    ("02_p02.png", "Page 1"), ("03_p03.png", "Page 2"), ("04_p04.png", "Page 3"),
    ("05_p05.png", "Page 4"), ("06_p06.png", "Page 5"), ("07_p07.png", "Page 6"),
    ("08_p08.png", "Page 7"), ("09_p09.png", "Page 8"), ("10_p10.png", "Page 9"),
    ("11_p11.png", "Page 10"), ("12_p12.png", "Page 11"), ("13_p13.png", "Page 12"),
    ("14_p14.png", "Page 13"), ("15_p15.png", "Page 14"), ("16_p16.png", "Page 15"),
    ("99_ending.png", "The End"),
]


def build_cover():
    """Scale to cover 1600x2560 and centre-crop to the exact ratio."""
    src = os.path.join(OUT, "ebook_cover_raw.png")
    im = Image.open(src).convert("RGB")
    scale = max(COVER_W / im.width, COVER_H / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    left = (im.width - COVER_W) // 2
    top = (im.height - COVER_H) // 2
    im = im.crop((left, top, left + COVER_W, top + COVER_H))
    dst = os.path.join(OUT, "kindle_cover_1600x2560.jpg")
    im.save(dst, "JPEG", quality=92, optimize=True, dpi=(300, 300))
    return dst, im.size


def prep_images():
    """Write interior page JPGs sized for the fixed-layout viewport."""
    img_dir = os.path.join(BUILD, "OEBPS", "images")
    os.makedirs(img_dir, exist_ok=True)
    out = []
    for i, (src, label) in enumerate(PAGE_ORDER):
        im = Image.open(os.path.join(PAGES, src)).convert("RGB")
        im = im.resize((PAGE_W, PAGE_H), Image.LANCZOS)
        name = f"page{i:02d}.jpg"
        im.save(os.path.join(img_dir, name), "JPEG", quality=88, optimize=True)
        out.append((name, label))
    # cover image for the ebook itself
    cover = Image.open(os.path.join(OUT, "kindle_cover_1600x2560.jpg")).convert("RGB")
    cover.thumbnail((1600, 2560), Image.LANCZOS)
    cover.save(os.path.join(img_dir, "cover.jpg"), "JPEG", quality=90, optimize=True)
    return out


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def page_xhtml(img, label, w, h):
    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
  <title>{escape(label)}</title>
  <meta name="viewport" content="width={w}, height={h}"/>
  <link rel="stylesheet" type="text/css" href="style.css"/>
</head>
<body>
  <div class="page"><img src="images/{img}" alt="{escape(label)}"/></div>
</body>
</html>
"""


def build_epub():
    if os.path.exists(BUILD):
        shutil.rmtree(BUILD)
    os.makedirs(BUILD)

    pages = prep_images()

    # mimetype must be first and stored uncompressed
    write(os.path.join(BUILD, "mimetype"), "application/epub+zip")

    write(os.path.join(BUILD, "META-INF", "container.xml"),
          """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
""")

    write(os.path.join(BUILD, "OEBPS", "style.css"),
          """@page { margin: 0; padding: 0; }
html, body { margin: 0; padding: 0; height: 100%; background: #ffffff; }
.page { margin: 0; padding: 0; text-align: center; }
.page img { width: 100%; height: 100%; margin: 0; padding: 0; display: block; }
""")

    # page documents
    for img, label in pages:
        write(os.path.join(BUILD, "OEBPS", img.replace(".jpg", ".xhtml")),
              page_xhtml(img, label, PAGE_W, PAGE_H))

    manifest, spine, nav_items = [], [], []
    manifest.append('<item id="cover-image" href="images/cover.jpg" '
                    'media-type="image/jpeg" properties="cover-image"/>')
    manifest.append('<item id="css" href="style.css" media-type="text/css"/>')
    manifest.append('<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" '
                    'properties="nav"/>')

    for i, (img, label) in enumerate(pages):
        doc = img.replace(".jpg", ".xhtml")
        manifest.append(f'<item id="pg{i}" href="{doc}" media-type="application/xhtml+xml"/>')
        manifest.append(f'<item id="im{i}" href="images/{img}" media-type="image/jpeg"/>')
        spine.append(f'<itemref idref="pg{i}"/>')
        nav_items.append(f'<li><a href="{doc}">{escape(label)}</a></li>')

    nl = "\n    "
    write(os.path.join(BUILD, "OEBPS", "content.opf"),
          f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0"
         unique-identifier="bookid" prefix="rendition: http://www.idpf.org/vocab/rendition/#">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="bookid">{BOOK_ID}</dc:identifier>
    <dc:title>{escape(TITLE)}</dc:title>
    <dc:creator>{escape(AUTHOR)}</dc:creator>
    <dc:language>{LANG}</dc:language>
    <dc:description>{escape(SUBTITLE)}</dc:description>
    <meta property="dcterms:modified">2026-08-11T00:00:00Z</meta>
    <meta property="rendition:layout">pre-paginated</meta>
    <meta property="rendition:orientation">portrait</meta>
    <meta property="rendition:spread">auto</meta>
    <meta name="cover" content="cover-image"/>
  </metadata>
  <manifest>
    {nl.join(manifest)}
  </manifest>
  <spine>
    {nl.join(spine)}
  </spine>
</package>
""")

    write(os.path.join(BUILD, "OEBPS", "nav.xhtml"),
          f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><title>Contents</title></head>
<body>
  <nav epub:type="toc" id="toc"><h1>Contents</h1>
    <ol>
    {nl.join(nav_items)}
    </ol>
  </nav>
</body>
</html>
""")

    dst = os.path.join(OUT, "princess_lila_kindle.epub")
    if os.path.exists(dst):
        os.remove(dst)
    with zipfile.ZipFile(dst, "w") as z:
        # mimetype first, uncompressed, no extra fields
        z.write(os.path.join(BUILD, "mimetype"), "mimetype", zipfile.ZIP_STORED)
        for root, _, files in os.walk(BUILD):
            for f in sorted(files):
                if f == "mimetype":
                    continue
                full = os.path.join(root, f)
                rel = os.path.relpath(full, BUILD)
                z.write(full, rel, zipfile.ZIP_DEFLATED)
    shutil.rmtree(BUILD)
    return dst, len(pages)


def main():
    os.makedirs(OUT, exist_ok=True)
    cover, size = build_cover()
    print(f"Cover : {os.path.basename(cover)}  {size[0]}x{size[1]} px  "
          f"ratio {size[1]/size[0]:.4f}  {os.path.getsize(cover)/1e6:.2f} MB")
    epub, n = build_epub()
    print(f"EPUB  : {os.path.basename(epub)}  {n} pages  "
          f"{os.path.getsize(epub)/1e6:.2f} MB  (fixed layout)")


if __name__ == "__main__":
    main()

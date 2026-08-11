#!/usr/bin/env python3
"""
Build listing graphics for "30 Days of Self-Care".

Every graphic is composed here with real vector-quality type drawn over the
hand-painted backdrops, and real rendered journal pages used for the previews —
so what a buyer sees is exactly what they get.

Outputs into ./marketing:
  etsy_hero_2000x2000.jpg          main listing image
  etsy_preview_pages_2000x2000.jpg what's-inside grid
  gumroad_cover_2560x1440.jpg      16:9 product cover
  gumroad_thumbnail_1200x1200.jpg  square thumbnail
  pinterest_pin_1000x1500.jpg      tall pin
  instagram_portrait_1080x1350.jpg 4:5 feed post
"""
import glob
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
MK = os.path.join(HERE, "marketing")
PAGES = os.path.join(os.path.dirname(HERE), "download", "journal")

CREAM = (253, 250, 244)
BROWN = (90, 74, 63)
BROWN_S = (138, 119, 103)
SAGE = (143, 164, 139)
ROSE = (201, 154, 148)
GOLD = (201, 162, 39)


def F(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def center(d, y, text, font, fill, W):
    w = d.textbbox((0, 0), text, font=font)[2]
    d.text(((W - w) / 2, y), text, font=font, fill=fill)
    return d.textbbox((0, 0), text, font=font)[3]


def fit(src, W, H, top_bias=False):
    im = Image.open(src).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))),
                   Image.LANCZOS)
    l = (im.width - W) // 2
    t = 0 if top_bias else (im.height - H) // 2
    return im.crop((l, t, l + W, t + H))


def veil(im, upto, alpha=225):
    """Fade a soft cream veil down from the top so text stays readable."""
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for i in range(upto):
        a = int(alpha * (1 - (i / upto) ** 1.7))
        d.line([(0, i), (im.width, i)], fill=(253, 250, 244, a))
    return Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")


def page(n):
    """Return a rendered journal page by 1-based page number."""
    hits = sorted(glob.glob(os.path.join(PAGES, f"{n:02d}_*.jpg")))
    return Image.open(hits[0]).convert("RGB") if hits else None


def shadowed(canvas, im, x, y, w):
    h = round(im.height * w / im.width)
    im = im.resize((w, h), Image.LANCZOS)
    sh = Image.new("RGBA", (w + 26, h + 26), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle([13, 15, w + 13, h + 15], fill=(90, 74, 63, 60))
    sh = sh.filter(__import__("PIL.ImageFilter", fromlist=["x"]).GaussianBlur(9))
    canvas.paste(sh, (x - 13, y - 13), sh)
    canvas.paste(im, (x, y))
    d = ImageDraw.Draw(canvas)
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=(226, 214, 196), width=1)
    return h


# ---------------------------------------------------------------- graphics
def etsy_hero():
    W = H = 2000
    im = fit(os.path.join(MK, "hero_raw.png"), W, H)
    im = veil(im, 760, 232)
    d = ImageDraw.Draw(im)
    y = 150
    center(d, y, "3 0   D A Y S   O F", F("Lato-Bold.ttf", 42), SAGE, W)
    y += 100
    center(d, y, "SELF-CARE", F("SourceSerifPro-Semibold.ttf", 178), BROWN, W)
    y += 232
    d.line([(W / 2 - 300, y), (W / 2 + 300, y)], fill=ROSE, width=3)
    y += 44
    center(d, y, "A Gentle Journey Back to Yourself",
           F("SourceSerifPro-It.ttf", 60), BROWN_S, W)
    y += 118
    center(d, y, "40-Page Printable Journal  ·  Instant Download",
           F("Lato-Regular.ttf", 42), BROWN, W)

    # badge strip
    by = H - 190
    d.rounded_rectangle([170, by, W - 170, by + 118], 18, fill=(255, 255, 255, 255))
    f = F("Lato-Bold.ttf", 36)
    fs = F("Lato-Regular.ttf", 30)
    cols = [("40", "PAGES"), ("30", "DAY PROMPTS"), ("2", "PAPER SIZES"), ("300", "DPI PRINT")]
    cw = (W - 340) / len(cols)
    for i, (big, small) in enumerate(cols):
        cx = 170 + cw * i + cw / 2
        w1 = d.textbbox((0, 0), big, font=f)[2]
        d.text((cx - w1 / 2, by + 24), big, font=f, fill=ROSE)
        w2 = d.textbbox((0, 0), small, font=fs)[2]
        d.text((cx - w2 / 2, by + 70), small, font=fs, fill=BROWN_S)
    im.save(os.path.join(MK, "etsy_hero_2000x2000.jpg"), quality=92, optimize=True)
    print("etsy_hero_2000x2000.jpg")


def etsy_preview():
    W = H = 2000
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im)
    center(d, 96, "WHAT'S INSIDE", F("SourceSerifPro-Semibold.ttf", 96), BROWN, W)
    center(d, 214, "40 beautifully designed pages",
           F("SourceSerifPro-It.ttf", 46), BROWN_S, W)
    picks = [1, 3, 5, 6, 9, 10, 15, 19, 20, 25, 30, 34, 36, 39, 40]
    cols, pw, gap = 5, 340, 38
    x0 = (W - (cols * pw + (cols - 1) * gap)) // 2
    y = 320
    row_h = round(pw * 11.0 / 8.5) + 46
    for i, n in enumerate(picks):
        p = page(n)
        if p is None:
            continue
        r, c = divmod(i, cols)
        shadowed(im, p, x0 + c * (pw + gap), y + r * row_h, pw)
    fy = y + 3 * row_h - 6
    center(d, fy, "30 daily prompt pages  \u00b7  weekly reflections  \u00b7  bonus toolkit & menu",
           F("Lato-Regular.ttf", 40), BROWN_S, W)
    im.save(os.path.join(MK, "etsy_preview_pages_2000x2000.jpg"),
            quality=90, optimize=True)
    print("etsy_preview_pages_2000x2000.jpg")


def gumroad_cover():
    W, H = 2560, 1440
    im = fit(os.path.join(MK, "hero_raw.png"), W, H)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(ov).rectangle([0, 0, W, H], fill=(253, 250, 244, 120))
    im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
    d = ImageDraw.Draw(im)
    # left text panel
    d.rounded_rectangle([120, 300, 1290, 1150], 26, fill=(255, 253, 248))
    y = 388
    d.text((190, y), "3 0   D A Y S   O F", font=F("Lato-Bold.ttf", 34), fill=SAGE)
    y += 76
    d.text((186, y), "SELF-CARE", font=F("SourceSerifPro-Semibold.ttf", 150),
           fill=BROWN)
    y += 200
    d.line([(190, y), (700, y)], fill=ROSE, width=3)
    y += 40
    d.text((190, y), "A Gentle Journey Back", font=F("SourceSerifPro-It.ttf", 56),
           fill=BROWN_S)
    y += 74
    d.text((190, y), "to Yourself", font=F("SourceSerifPro-It.ttf", 56), fill=BROWN_S)
    y += 116
    d.text((190, y), "40-page printable journal", font=F("Lato-Regular.ttf", 40),
           fill=BROWN)
    y += 58
    d.text((190, y), "US Letter + A4  ·  Instant download",
           font=F("Lato-Regular.ttf", 36), fill=BROWN_S)
    # page peek on the right
    p = page(6)
    if p:
        shadowed(im, p, 1560, 300, 620)
    p2 = page(20)
    if p2:
        shadowed(im, p2, 1980, 430, 480)
    im.save(os.path.join(MK, "gumroad_cover_2560x1440.jpg"), quality=91, optimize=True)
    print("gumroad_cover_2560x1440.jpg")


def gumroad_thumb():
    W = H = 1200
    im = fit(os.path.join(MK, "hero_raw.png"), W, H)
    im = veil(im, 520, 236)
    d = ImageDraw.Draw(im)
    y = 92
    center(d, y, "3 0   D A Y S   O F", F("Lato-Bold.ttf", 30), SAGE, W)
    y += 66
    center(d, y, "SELF-CARE", F("SourceSerifPro-Semibold.ttf", 124), BROWN, W)
    y += 168
    d.line([(W / 2 - 190, y), (W / 2 + 190, y)], fill=ROSE, width=3)
    y += 32
    center(d, y, "A Gentle Journey Back to Yourself",
           F("SourceSerifPro-It.ttf", 38), BROWN_S, W)
    d.rounded_rectangle([150, H - 150, W - 150, H - 60], 14, fill=(255, 255, 255))
    center(d, H - 130, "40-PAGE PRINTABLE JOURNAL", F("Lato-Bold.ttf", 34), BROWN, W)
    im.save(os.path.join(MK, "gumroad_thumbnail_1200x1200.jpg"),
            quality=92, optimize=True)
    print("gumroad_thumbnail_1200x1200.jpg")


def pinterest_pin():
    W, H = 1000, 1500
    im = fit(os.path.join(MK, "pin_raw.png"), W, H)
    # solid cream band behind all the type, then a soft fade into the artwork
    band = 660
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dv = ImageDraw.Draw(ov)
    dv.rectangle([0, 0, W, band - 130], fill=(253, 250, 244, 252))
    for i in range(130):
        a = int(252 * (1 - (i / 130) ** 1.4))
        dv.line([(0, band - 130 + i), (W, band - 130 + i)],
                fill=(253, 250, 244, a))
    im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
    d = ImageDraw.Draw(im)
    y = 92
    center(d, y, "3 0   D A Y S   O F", F("Lato-Bold.ttf", 27), SAGE, W)
    y += 58
    center(d, y, "SELF-CARE", F("SourceSerifPro-Semibold.ttf", 116), BROWN, W)
    y += 156
    d.line([(W / 2 - 170, y), (W / 2 + 170, y)], fill=ROSE, width=3)
    y += 30
    center(d, y, "A Gentle Journey", F("SourceSerifPro-It.ttf", 44), BROWN_S, W)
    y += 56
    center(d, y, "Back to Yourself", F("SourceSerifPro-It.ttf", 44), BROWN_S, W)
    y += 92
    center(d, y, "30 daily prompts for rest,", F("Lato-Regular.ttf", 32), BROWN, W)
    y += 44
    center(d, y, "reflection & self-love", F("Lato-Regular.ttf", 32), BROWN, W)
    # foot banner
    d.rounded_rectangle([70, H - 168, W - 70, H - 62], 16, fill=(255, 253, 248))
    center(d, H - 150, "40-PAGE PRINTABLE JOURNAL", F("Lato-Bold.ttf", 32), BROWN, W)
    center(d, H - 108, "US Letter + A4  ·  Instant Download",
           F("Lato-Regular.ttf", 27), BROWN_S, W)
    im.save(os.path.join(MK, "pinterest_pin_1000x1500.jpg"), quality=92, optimize=True)
    print("pinterest_pin_1000x1500.jpg")


def instagram():
    W, H = 1080, 1350
    im = Image.new("RGB", (W, H), CREAM)
    bg = fit(os.path.join(MK, "pin_raw.png"), W, 760)
    im.paste(bg, (0, H - 760))
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(ov)
    for i in range(300):
        a = int(255 * (1 - (i / 300) ** 2))
        dd.line([(0, H - 760 + i), (W, H - 760 + i)], fill=(253, 250, 244, a))
    im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
    d = ImageDraw.Draw(im)
    y = 118
    center(d, y, "Self-care doesn't have to", F("SourceSerifPro-Semibold.ttf", 62),
           BROWN, W)
    y += 82
    center(d, y, "be complicated.", F("SourceSerifPro-Semibold.ttf", 62), BROWN, W)
    y += 116
    d.line([(W / 2 - 150, y), (W / 2 + 150, y)], fill=ROSE, width=3)
    y += 36
    center(d, y, "Sometimes it's a quiet morning,", F("Lato-Regular.ttf", 34),
           BROWN_S, W)
    y += 48
    center(d, y, "or simply permission to rest.", F("Lato-Regular.ttf", 34),
           BROWN_S, W)
    y += 92
    center(d, y, "A 30-DAY PRINTABLE JOURNAL", F("Lato-Bold.ttf", 34), SAGE, W)
    im.save(os.path.join(MK, "instagram_portrait_1080x1350.jpg"),
            quality=92, optimize=True)
    print("instagram_portrait_1080x1350.jpg")


def main():
    os.makedirs(MK, exist_ok=True)
    etsy_hero()
    etsy_preview()
    gumroad_cover()
    gumroad_thumb()
    pinterest_pin()
    instagram()


if __name__ == "__main__":
    main()

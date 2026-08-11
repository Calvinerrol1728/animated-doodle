#!/usr/bin/env python3
"""
Build "30 Days of Self-Care — A Gentle Journey Back to Yourself".

A premium printable adult journal, 40 pages.

Design decision: every word is drawn as REAL VECTOR TEXT (not AI-rendered
pixels), so spelling is guaranteed exact, the type stays razor sharp at any
print size, and ruled writing lines are perfectly straight. Hand-painted
illustrations are composited in as decoration only.

Outputs into ./out:
  selfcare_journal_US_Letter.pdf   8.5 x 11 in
  selfcare_journal_A4.pdf          210 x 297 mm

Usage: python3 build_journal.py
"""
import os
import sys

from PIL import Image
from reportlab.lib.colors import Color, HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as rl_canvas

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content as C  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
ART = os.path.join(HERE, "art")
BOT = os.path.join(ART, "botanical_hi")
OUT = os.path.join(HERE, "out")

IN = 72.0

# ---------------------------------------------------------------- palette
CREAM      = HexColor("#FDFAF4")   # page background
CREAM_DEEP = HexColor("#F6EFE3")   # panels
BEIGE      = HexColor("#E8DCC8")
ROSE       = HexColor("#C99A94")
ROSE_PALE  = HexColor("#EBD5D0")
SAGE       = HexColor("#8FA48B")
SAGE_PALE  = HexColor("#D5DED1")
BROWN      = HexColor("#5A4A3F")   # body text
BROWN_SOFT = HexColor("#8A7767")
LAVENDER   = HexColor("#B3A8C4")
RULE       = HexColor("#DCD0BE")   # writing lines

# ---------------------------------------------------------------- fonts
def jpeg(im, q=88):
    """Encode an RGB image to JPEG in memory so the PDF stays small."""
    import io
    buf = io.BytesIO()
    im.convert("RGB").save(buf, "JPEG", quality=q, optimize=True,
                           progressive=True)
    buf.seek(0)
    return ImageReader(buf)


def register_fonts():
    for name, fn in [
        ("Serif",       "SourceSerifPro-Regular.ttf"),
        ("Serif-Semi",  "SourceSerifPro-Semibold.ttf"),
        ("Serif-It",    "SourceSerifPro-It.ttf"),
        ("Serif-Light", "SourceSerifPro-Light.ttf"),
        ("Sans",        "Lato-Regular.ttf"),
        ("Sans-Bold",   "Lato-Bold.ttf"),
        ("Sans-Light",  "Lato-Light.ttf"),
        ("Sans-It",     "Lato-Italic.ttf"),
    ]:
        pdfmetrics.registerFont(TTFont(name, os.path.join(FONTS, fn)))


# ---------------------------------------------------------------- helpers
class _Null:
    """Swallows all drawing calls so a layout can be measured without ink."""
    def __getattr__(self, _):
        return lambda *a, **k: None


class Page:
    """One journal page with a running vertical cursor."""

    def __init__(self, c, W, H, margin, dry=False):
        self.real = c
        self.dry = dry
        self.c = _Null() if dry else c
        self.W, self.H, self.M = W, H, margin
        self.y = H - margin
        self.cx = W / 2
        self.gap = 25.0

    def wrap(self, text, font, size, max_w):
        words, line, out = text.split(), "", []
        for w in words:
            t = (line + " " + w).strip()
            if pdfmetrics.stringWidth(t, font, size) <= max_w:
                line = t
            else:
                out.append(line)
                line = w
        if line:
            out.append(line)
        return out

    # ---- primitives ----
    def bg(self):
        self.c.setFillColor(CREAM)
        self.c.rect(0, 0, self.W, self.H, fill=1, stroke=0)

    def frame(self):
        """Subtle inner keyline for a premium editorial feel."""
        m = self.M * 0.52
        self.c.setStrokeColor(BEIGE)
        self.c.setLineWidth(0.7)
        self.c.rect(m, m, self.W - 2 * m, self.H - 2 * m, fill=0, stroke=1)

    def text_c(self, s, font, size, color, dy=0, leading=None):
        self.y -= dy
        self.c.setFont(font, size)
        self.c.setFillColor(color)
        self.c.drawCentredString(self.cx, self.y, s)
        self.y -= (leading or size * 1.35)

    def para_c(self, s, font, size, color, max_w, leading, dy=0):
        self.y -= dy
        self.c.setFillColor(color)
        for ln in self.wrap(s, font, size, max_w):
            self.c.setFont(font, size)
            self.c.drawCentredString(self.cx, self.y, ln)
            self.y -= leading

    def text_l(self, s, font, size, color, dy=0, x=None):
        self.y -= dy
        self.c.setFont(font, size)
        self.c.setFillColor(color)
        self.c.drawString(x if x is not None else self.M, self.y, s)
        self.y -= size * 1.35

    # ---- decorative ----
    def botanical(self, name, x, y, h, alpha=1.0):
        p = os.path.join(BOT, f"{name}.png")
        if not os.path.exists(p):
            return
        im = Image.open(p)
        w = h * im.width / im.height
        if alpha < 1.0:
            im = im.copy()
            a = im.split()[3].point(lambda v: int(v * alpha))
            im.putalpha(a)
        self.c.drawImage(ImageReader(im), x, y, w, h, mask="auto")

    def corner_sprigs(self, a="eucalyptus", b="lavender", size=52, alpha=0.55):
        """Matching decorative sprigs in the top corners of every page."""
        m = self.M * 0.62
        self.botanical(a, m, self.H - m - size, size, alpha)
        self.botanical(b, self.W - m - size * 0.6, self.H - m - size, size, alpha)

    def divider(self, dy=10, w=1.6):
        self.y -= dy
        half = 0.9 * IN
        self.c.setStrokeColor(BEIGE)
        self.c.setLineWidth(w)
        self.c.line(self.cx - half, self.y, self.cx - 14, self.y)
        self.c.line(self.cx + 14, self.y, self.cx + half, self.y)
        self.c.setFillColor(ROSE)
        self.c.circle(self.cx, self.y, 2.4, fill=1, stroke=0)
        self.y -= dy

    # ---- headers ----
    def day_header(self, day, title):
        self.c.setFont("Sans-Bold", 9.5)
        self.c.setFillColor(SAGE)
        self.c.drawCentredString(self.cx, self.y - 4, f"D A Y   {day}")
        self.y -= 30
        for ln in self.wrap(title, "Serif-Semi", 25, self.W - 2 * self.M):
            self.c.setFont("Serif-Semi", 25)
            self.c.setFillColor(BROWN)
            self.c.drawCentredString(self.cx, self.y, ln)
            self.y -= 30
        self.divider(9)

    def page_header(self, title, size=25):
        for ln in self.wrap(title, "Serif-Semi", size, self.W - 2 * self.M):
            self.c.setFont("Serif-Semi", size)
            self.c.setFillColor(BROWN)
            self.c.drawCentredString(self.cx, self.y, ln)
            self.y -= size * 1.2
        self.divider(9)

    # ---- content blocks ----
    def quote(self, s):
        self.y -= 4
        w = self.W - 2 * self.M - 0.5 * IN
        lines = self.wrap(s, "Serif-It", 12.5, w)
        self.c.setFillColor(BROWN_SOFT)
        for ln in lines:
            self.c.setFont("Serif-It", 12.5)
            self.c.drawCentredString(self.cx, self.y, ln)
            self.y -= 17
        self.y -= 8

    def statement(self, s, size=19):
        self.y -= 8
        w = self.W - 2 * self.M - 0.35 * IN
        lines = self.wrap(s, "Serif-Semi", size, w)
        box_h = len(lines) * (size * 1.32) + 26
        self.c.setFillColor(CREAM_DEEP)
        self.c.roundRect(self.M, self.y - box_h + size + 8, self.W - 2 * self.M,
                         box_h, 8, fill=1, stroke=0)
        self.y -= 4
        self.c.setFillColor(BROWN)
        for ln in lines:
            self.c.setFont("Serif-Semi", size)
            self.c.drawCentredString(self.cx, self.y, ln)
            self.y -= size * 1.32
        self.y -= 16

    def subtitle(self, s):
        self.c.setFont("Sans-Bold", 11)
        self.c.setFillColor(SAGE)
        self.c.drawCentredString(self.cx, self.y, s)
        self.y -= 24

    def label(self, s, color=None, font="Sans-Bold", size=10.8):
        self.c.setFont(font, size)
        self.c.setFillColor(color or BROWN)
        self.c.drawString(self.M, self.y, s)
        self.y -= size * 1.75

    def rules(self, n, gap=None, x0=None, x1=None, dashed=False):
        gap = gap or self.gap
        x0 = self.M if x0 is None else x0
        x1 = (self.W - self.M) if x1 is None else x1
        self.c.setStrokeColor(RULE)
        self.c.setLineWidth(0.8)
        if dashed:
            self.c.setDash(1, 3)
        for _ in range(n):
            self.c.line(x0, self.y, x1, self.y)
            self.y -= gap
        if dashed:
            self.c.setDash()

    def prompt(self, text, n, gap=None):
        gap = gap or self.gap
        for ln in self.wrap(text, "Sans-Bold", 10.8, self.W - 2 * self.M):
            self.c.setFont("Sans-Bold", 10.8)
            self.c.setFillColor(BROWN)
            self.c.drawString(self.M, self.y, ln)
            self.y -= 15
        self.y -= 12
        self.rules(n, gap)
        self.y -= 6

    def numbered(self, n, gap=None):
        gap = gap or self.gap
        for i in range(1, n + 1):
            self.c.setFont("Sans", 10)
            self.c.setFillColor(ROSE)
            self.c.drawString(self.M, self.y + 3, f"{i}.")
            self.c.setStrokeColor(RULE)
            self.c.setLineWidth(0.8)
            self.c.line(self.M + 20, self.y, self.W - self.M, self.y)
            self.y -= gap
        self.y -= 4

    def checklist(self, items, gap=None):
        gap = (gap or self.gap) + 2
        for it in items:
            bx, by = self.M + 2, self.y - 1
            self.c.setStrokeColor(SAGE)
            self.c.setLineWidth(1.0)
            self.c.roundRect(bx, by, 11, 11, 2, fill=0, stroke=1)
            self.c.setFont("Sans", 11)
            self.c.setFillColor(BROWN)
            self.c.drawString(bx + 21, by + 2, it)
            self.y -= gap
        self.y -= 6

    def check_rules(self, n, gap=None):
        gap = (gap or self.gap) + 2
        for _ in range(n):
            bx, by = self.M + 2, self.y - 1
            self.c.setStrokeColor(SAGE)
            self.c.setLineWidth(1.0)
            self.c.roundRect(bx, by, 11, 11, 2, fill=0, stroke=1)
            self.c.setStrokeColor(RULE)
            self.c.setLineWidth(0.8)
            self.c.line(bx + 21, by, self.W - self.M, by)
            self.y -= gap
        self.y -= 4

    def boxes(self, titles, rows, gap=None):
        gap = gap or max(20, self.gap - 2)
        """Panels side by side, each with a heading and ruled lines."""
        n = len(titles)
        pad = 12
        total = self.W - 2 * self.M
        bw = (total - pad * (n - 1)) / n
        bh = rows * gap + 40
        top = self.y
        for i, t in enumerate(titles):
            x = self.M + i * (bw + pad)
            self.c.setFillColor(CREAM_DEEP)
            self.c.roundRect(x, top - bh, bw, bh, 7, fill=1, stroke=0)
            self.c.setStrokeColor(BEIGE)
            self.c.setLineWidth(0.7)
            self.c.roundRect(x, top - bh, bw, bh, 7, fill=0, stroke=1)
            # heading
            size = 9.5 if len(t) < 22 else 8.3
            self.c.setFont("Sans-Bold", size)
            self.c.setFillColor(SAGE)
            self.c.drawCentredString(x + bw / 2, top - 20, t.upper())
            # rules
            yy = top - 38
            self.c.setStrokeColor(RULE)
            self.c.setLineWidth(0.7)
            for _ in range(rows):
                self.c.line(x + 10, yy, x + bw - 10, yy)
                yy -= gap
        self.y = top - bh - 16

    def panel(self, title, rows, gap=None):
        gap = gap or self.gap
        pad_top = 34
        bh = rows * gap + pad_top + 8
        top = self.y
        self.c.setFillColor(CREAM_DEEP)
        self.c.roundRect(self.M, top - bh, self.W - 2 * self.M, bh, 7, fill=1, stroke=0)
        self.c.setStrokeColor(BEIGE)
        self.c.setLineWidth(0.7)
        self.c.roundRect(self.M, top - bh, self.W - 2 * self.M, bh, 7, fill=0, stroke=1)
        self.c.setFont("Sans-Bold", 10)
        self.c.setFillColor(SAGE)
        self.c.drawString(self.M + 14, top - 20, title)
        yy = top - pad_top - 6
        self.c.setStrokeColor(RULE)
        self.c.setLineWidth(0.7)
        for _ in range(rows):
            self.c.line(self.M + 14, yy, self.W - self.M - 14, yy)
            yy -= gap
        self.y = top - bh - 14

    def footer_quote(self, s):
        """Pin a closing italic line near the bottom of the page."""
        yy = self.M * 0.92 + 16
        self.c.setFillColor(BROWN_SOFT)
        lines = self.wrap(s, "Serif-It", 10.5, self.W - 2 * self.M - 0.4 * IN)
        yy += (len(lines) - 1) * 14
        for ln in lines:
            self.c.setFont("Serif-It", 10.5)
            self.c.drawCentredString(self.cx, yy, ln)
            yy -= 14


# ---------------------------------------------------------------- pages
def cover(P):
    c = P.c
    art = os.path.join(ART, "hires", "cover.png")
    if os.path.exists(art):
        im = Image.open(art).convert("RGB")
        need_w, need_h = int(P.W / 72 * 320), int(P.H / 72 * 320)
        s = max(need_w / im.width, need_h / im.height)
        im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))),
                       Image.LANCZOS)
        l, t = (im.width - need_w) / 2, (im.height - need_h) / 2
        im = im.crop((int(l), int(t), int(l + need_w), int(t + need_h)))
        c.drawImage(jpeg(im, 86), 0, 0, P.W, P.H)
    # soften the top so the title reads cleanly
    for i in range(120):
        a = 0.85 * (1 - i / 120.0)
        c.setFillColor(Color(0.992, 0.980, 0.957, alpha=a))
        c.rect(0, P.H - (i + 1) * (0.34 * IN) / 8, P.W, (0.34 * IN) / 8 + 1,
               fill=1, stroke=0)

    m = 0.5 * IN
    c.setStrokeColor(HexColor("#C9B79B"))
    c.setLineWidth(1.1)
    c.rect(m, m, P.W - 2 * m, P.H - 2 * m, fill=0, stroke=1)
    c.setLineWidth(0.5)
    c.rect(m + 6, m + 6, P.W - 2 * m - 12, P.H - 2 * m - 12, fill=0, stroke=1)

    y = P.H - 1.42 * IN
    c.setFont("Sans-Bold", 10.5)
    c.setFillColor(SAGE)
    c.drawCentredString(P.cx, y, "3 0   D A Y S   O F")
    y -= 0.62 * IN
    c.setFont("Serif-Semi", 47)
    c.setFillColor(BROWN)
    c.drawCentredString(P.cx, y, "SELF-CARE")
    y -= 0.34 * IN
    c.setStrokeColor(ROSE)
    c.setLineWidth(1.1)
    c.line(P.cx - 1.5 * IN, y, P.cx + 1.5 * IN, y)
    y -= 0.36 * IN
    c.setFont("Serif-It", 16)
    c.setFillColor(BROWN_SOFT)
    c.drawCentredString(P.cx, y, C.SUBTITLE)

    yb = 0.95 * IN
    c.setFillColor(Color(1, 1, 1, alpha=0.72))
    c.roundRect(P.M - 6, yb - 12, P.W - 2 * (P.M - 6), 40, 7, fill=1, stroke=0)
    c.setFont("Sans", 11)
    c.setFillColor(BROWN)
    c.drawCentredString(P.cx, yb + 8, C.TAGLINE)


def belongs(P):
    P.bg(); P.frame(); P.corner_sprigs("rose", "eucalyptus", 58, .6)
    P.y = P.H - 2.5 * IN
    P.page_header(C.BELONGS["title"], 22)
    P.y -= 0.5 * IN
    P.c.setStrokeColor(RULE)
    P.c.setLineWidth(1.0)
    P.c.line(P.M + 0.6 * IN, P.y, P.W - P.M - 0.6 * IN, P.y)
    P.y -= 1.15 * IN
    P.para_c(C.BELONGS["quote"], "Serif-It", 13, BROWN_SOFT,
             P.W - 2 * P.M - 0.7 * IN, 20)
    P.botanical("wildflower", P.cx - 34, P.M + 0.55 * IN, 62, .75)


def welcome(P):
    P.bg(); P.frame(); P.corner_sprigs("lavender", "fern", 56, .55)
    P.y = P.H - 1.55 * IN
    P.page_header(C.WELCOME["title"], 20)
    w = P.W - 2 * P.M - 0.3 * IN
    for b in C.WELCOME["body"]:
        P.para_c(b, "Sans", 11.2, BROWN, w, 17.5, dy=6)
        P.y -= 10
    P.divider(8)
    P.para_c(C.WELCOME["quote"], "Serif-It", 13.5, ROSE, w, 19, dy=6)
    P.y -= 6
    art = os.path.join(ART, "hires", "welcome.png")
    if os.path.exists(art):
        im = Image.open(art).convert("RGB")
        aw = P.W - 2 * P.M
        ah = min(P.y - P.M - 0.35 * IN, aw * 0.82)
        need_w, need_h = int(aw / 72 * 320), int(ah / 72 * 320)
        s = max(need_w / im.width, need_h / im.height)
        im2 = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))),
                        Image.LANCZOS)
        l, t = (im2.width - need_w) / 2, (im2.height - need_h) / 2
        im2 = im2.crop((int(l), int(t), int(l + need_w), int(t + need_h)))
        P.c.drawImage(jpeg(im2, 86), P.M, P.y - ah, aw, ah, mask=None)


def guide(P):
    P.bg(); P.frame(); P.corner_sprigs("olive", "leaves", 54, .55)
    P.y = P.H - 1.6 * IN
    P.page_header(C.GUIDE["title"], 25)
    P.y -= 6
    for i, item in enumerate(C.GUIDE["items"], 1):
        top = P.y
        lines = P.wrap(item, "Sans", 11.5, P.W - 2 * P.M - 0.85 * IN)
        bh = max(46, len(lines) * 16 + 30)
        P.c.setFillColor(CREAM_DEEP)
        P.c.roundRect(P.M, top - bh, P.W - 2 * P.M, bh, 7, fill=1, stroke=0)
        P.c.setFillColor(ROSE_PALE)
        P.c.circle(P.M + 27, top - bh / 2, 14, fill=1, stroke=0)
        P.c.setFont("Serif-Semi", 13)
        P.c.setFillColor(BROWN)
        P.c.drawCentredString(P.M + 27, top - bh / 2 - 4.5, str(i))
        yy = top - bh / 2 + (len(lines) - 1) * 8 - 4
        P.c.setFillColor(BROWN)
        for ln in lines:
            P.c.setFont("Sans", 11.5)
            P.c.drawString(P.M + 52, yy, ln)
            yy -= 16
        P.y = top - bh - 13
    P.footer_quote(C.GUIDE["quote"])


def promise(P):
    P.bg(); P.frame(); P.corner_sprigs("rose", "lavender", 56, .55)
    P.y = P.H - 1.6 * IN
    P.page_header(C.PROMISE["title"], 25)
    P.y -= 4
    for pr in C.PROMISE["prompts"]:
        P.prompt(pr, 3, 25)
    P.botanical("vine", P.cx - 22, P.M * 0.75, 44, .5)


def day_page(P, day, title, blocks, motif):
    P.bg(); P.frame()
    pair = {
        "tea": ("eucalyptus", "lavender"), "flowers": ("rose", "wildflower"),
        "bed": ("leaves", "eucalyptus"), "sun": ("olive", "fern"),
        "leaf": ("fern", "leaves"), "candle": ("lavender", "vine"),
        "wildflower": ("wildflower", "rose"), "plant": ("olive", "eucalyptus"),
        "eucalyptus": ("eucalyptus", "olive"), "mountain": ("fern", "olive"),
        "moon": ("lavender", "vine"), "kitchen": ("wildflower", "olive"),
        "blanket": ("leaves", "lavender"), "window": ("eucalyptus", "rose"),
        "olive": ("olive", "leaves"), "envelope": ("vine", "rose"),
        "sunrise": ("rose", "olive"), "fern": ("fern", "eucalyptus"),
    }.get(motif, ("eucalyptus", "lavender"))
    P.corner_sprigs(pair[0], pair[1], 50, .5)

    P.y = P.H - 1.32 * IN
    P.day_header(day, title)

    footer = None
    for b in blocks:
        k = b[0]
        if k == "quote":
            P.quote(b[1])
        elif k == "statement":
            P.statement(b[1])
        elif k == "subtitle":
            P.subtitle(b[1])
        elif k == "label":
            P.label(b[1])
        elif k == "prompt":
            P.prompt(b[1], b[2])
        elif k == "lines":
            P.rules(b[1])
        elif k == "numbered":
            P.numbered(b[1])
        elif k == "checklist":
            P.checklist(b[1])
        elif k == "panel":
            P.panel(b[1], b[2])
        elif k == "boxes2":
            P.boxes(b[1], b[2])
        elif k == "boxes3":
            P.boxes(b[1], b[2])
        elif k == "footer":
            footer = b[1]
    if footer:
        P.footer_quote(footer)


def render_fitted(make_page, draw, W, H, margin, target_bottom):
    """Draw once invisibly to measure, pick a line gap that fills the page,
    then draw for real. Keeps every page's writing area generous and even."""
    best = 25.0
    for gap in [25 + i * 0.5 for i in range(45)]:  # 25 -> 47
        P = make_page(dry=True)
        P.gap = float(gap)
        draw(P)
        if P.y < target_bottom:
            break
        best = float(gap)
    P = make_page(dry=False)
    P.gap = best
    draw(P)
    return P


def toolkit(P):
    P.bg(); P.frame(); P.corner_sprigs("olive", "eucalyptus", 52, .5)
    P.y = P.H - 1.55 * IN
    P.page_header(C.TOOLKIT["title"], 24)
    P.y -= 4
    for s in C.TOOLKIT["sections"]:
        P.panel(s, 3)


def menu(P):
    P.bg(); P.frame(); P.corner_sprigs("wildflower", "lavender", 52, .5)
    P.y = P.H - 1.55 * IN
    P.page_header(C.MENU["title"], 24)
    P.y -= 8
    for name, rows in C.MENU["sections"]:
        P.c.setFont("Sans-Bold", 11)
        P.c.setFillColor(SAGE)
        P.c.drawString(P.M, P.y, name)
        P.y -= 24
        P.check_rules(rows, 30)
        P.y -= 16
    P.botanical("olive", P.cx - 30, P.M * 0.8, 52, .5)


def remember(P):
    P.bg(); P.frame(); P.corner_sprigs("rose", "fern", 52, .5)
    P.y = P.H - 1.5 * IN
    P.page_header(C.REMEMBER["title"], 24)
    P.y -= 6
    P.numbered(C.REMEMBER["count"], 25)
    P.footer_quote(C.REMEMBER["footer"])


def looking_back(P):
    P.bg(); P.frame(); P.corner_sprigs("eucalyptus", "wildflower", 52, .5)
    P.y = P.H - 1.55 * IN
    P.page_header(C.LOOKING_BACK["title"], 25)
    P.y -= 6
    for pr in C.LOOKING_BACK["prompts"]:
        P.prompt(pr, 2, 25)


def final_page(P):
    c = P.c
    art = os.path.join(ART, "hires", "final.png")
    if os.path.exists(art):
        im = Image.open(art).convert("RGB")
        need_w, need_h = int(P.W / 72 * 320), int(P.H / 72 * 320)
        s = max(need_w / im.width, need_h / im.height)
        im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))),
                       Image.LANCZOS)
        l, t = (im.width - need_w) / 2, (im.height - need_h) / 2
        im = im.crop((int(l), int(t), int(l + need_w), int(t + need_h)))
        c.drawImage(jpeg(im, 86), 0, 0, P.W, P.H)
    # smooth gradient veil: solid at the top, fading out over the artwork
    top_y = P.H
    fade_to = P.H * 0.40
    steps = 190
    band = (top_y - fade_to) / steps
    for i in range(steps):
        yy = top_y - (i + 1) * band
        t = i / float(steps - 1)
        a = 0.90 * (1.0 - t) ** 1.5
        c.setFillColor(Color(0.992, 0.980, 0.957, alpha=a))
        c.rect(0, yy, P.W, band + 1.0, fill=1, stroke=0)

    m = 0.5 * IN
    c.setStrokeColor(HexColor("#C9B79B"))
    c.setLineWidth(1.1)
    c.rect(m, m, P.W - 2 * m, P.H - 2 * m, fill=0, stroke=1)
    c.setLineWidth(0.5)
    c.rect(m + 6, m + 6, P.W - 2 * m - 12, P.H - 2 * m - 12, fill=0, stroke=1)

    # soft cream card so every line stays fully readable over the art
    card_top = P.H - 1.15 * IN
    card_h = 3.05 * IN
    c.setFillColor(Color(1, 0.996, 0.985, alpha=0.93))
    c.roundRect(P.M - 4, card_top - card_h, P.W - 2 * (P.M - 4), card_h,
                10, fill=1, stroke=0)
    c.setStrokeColor(BEIGE)
    c.setLineWidth(0.7)
    c.roundRect(P.M - 4, card_top - card_h, P.W - 2 * (P.M - 4), card_h,
                10, fill=0, stroke=1)

    P.y = P.H - 1.75 * IN
    w = P.W - 2 * P.M - 0.3 * IN
    lines = P.wrap(C.FINAL["statement"], "Serif-Semi", 25, w)
    c.setFillColor(BROWN)
    for ln in lines:
        c.setFont("Serif-Semi", 25)
        c.drawCentredString(P.cx, P.y, ln)
        P.y -= 32
    P.divider(12)
    P.para_c(C.FINAL["body"], "Sans", 11.5, BROWN, w - 0.3 * IN, 18, dy=6)
    P.y -= 14
    P.para_c(C.FINAL["last"], "Serif-It", 14, ROSE, w, 19)

    P.botanical("eucalyptus", P.M + 4, P.M + 0.42 * IN, 62, .6)
    P.botanical("lavender", P.W - P.M - 40, P.M + 0.42 * IN, 62, .6)


# ---------------------------------------------------------------- build
def build(path, W, H):
    margin = 0.85 * IN if W < 8.4 * IN else 0.9 * IN
    c = rl_canvas.Canvas(path, pagesize=(W, H))
    c.setTitle("30 Days of Self-Care \u2014 A Gentle Journey Back to Yourself")
    c.setAuthor("Cedric Errol Cajelo")
    c.setSubject("A 30-Day Journal for Rest, Reflection & Self-Love")

    def P(dry=False):
        return Page(c, W, H, margin, dry)

    # bottom limit content should reach toward (leaves a calm foot margin)
    foot = margin * 1.15

    cover(P()); c.showPage()
    belongs(P()); c.showPage()
    welcome(P()); c.showPage()
    guide(P()); c.showPage()
    render_fitted(P, promise, W, H, margin, foot); c.showPage()
    for day, title, blocks, motif in C.DAYS:
        render_fitted(P, lambda pg, d=day, t=title, b=blocks, m=motif:
                      day_page(pg, d, t, b, m), W, H, margin, foot)
        c.showPage()
    render_fitted(P, toolkit, W, H, margin, foot); c.showPage()
    render_fitted(P, menu, W, H, margin, foot); c.showPage()
    render_fitted(P, remember, W, H, margin, foot); c.showPage()
    render_fitted(P, looking_back, W, H, margin, foot); c.showPage()
    final_page(P()); c.showPage()
    c.save()
    return path


def strip_helvetica(path):
    from pypdf import PdfReader, PdfWriter
    r = PdfReader(path)
    w = PdfWriter()
    for pg in r.pages:
        res = pg.get("/Resources")
        if res is not None:
            res = res.get_object()
            fonts = res.get("/Font")
            if fonts is not None:
                fonts = fonts.get_object()
                for k in [k for k in list(fonts.keys())
                          if "Helvetica" in str(fonts[k].get_object().get("/BaseFont"))]:
                    del fonts[k]
        w.add_page(pg)
    w.add_metadata({
        "/Title": "30 Days of Self-Care \u2014 A Gentle Journey Back to Yourself",
        "/Author": "Cedric Errol Cajelo",
        "/Subject": "A 30-Day Journal for Rest, Reflection & Self-Love",
    })
    with open(path, "wb") as fh:
        w.write(fh)


def main():
    os.makedirs(OUT, exist_ok=True)
    register_fonts()
    a = build(os.path.join(OUT, "selfcare_journal_US_Letter.pdf"), 8.5 * IN, 11 * IN)
    strip_helvetica(a)
    b = build(os.path.join(OUT, "selfcare_journal_A4.pdf"),
              210 / 25.4 * IN, 297 / 25.4 * IN)
    strip_helvetica(b)
    from pypdf import PdfReader
    for f in (a, b):
        r = PdfReader(f)
        p = r.pages[0]
        print(f"{os.path.basename(f)}: {len(r.pages)} pages  "
              f"{float(p.mediabox.width)/72:.2f} x {float(p.mediabox.height)/72:.2f} in  "
              f"{os.path.getsize(f)/1e6:.1f} MB")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Build the MONTHLY BUDGET PLANNER — a premium printable financial planner.

All text and every table rule is drawn as real vector output, so spelling is
exact, columns are perfectly square, and the type stays sharp at any size.
Hand-painted illustrations appear only on the cover and closing page.

Outputs into ./out:
  budget_planner_US_Letter.pdf   8.5 x 11 in
  budget_planner_A4.pdf          210 x 297 mm
  budget_planner_EBOOK.pdf       bookmarked edition (US Letter)
"""
import os
import sys

from PIL import Image, ImageFilter
from reportlab.lib.colors import Color, HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as rl_canvas

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content as C  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(os.path.dirname(HERE), "journal", "fonts")
ART = os.path.join(HERE, "art")
OUT = os.path.join(HERE, "out")
IN = 72.0

CREAM = HexColor("#FDFBF6")
PANEL = HexColor("#F5F0E6")
PANEL2 = HexColor("#EFEADF")
BEIGE = HexColor("#E3D9C6")
LINE = HexColor("#D8CDBA")
SAGE = HexColor("#8B9E86")
SAGE_D = HexColor("#6E8169")
ROSE = HexColor("#C29A94")
BROWN = HexColor("#4E4238")
GREY = HexColor("#8A7F73")
CHAR = HexColor("#3A3430")
FAINT = HexColor("#B9AFA1")


def register_fonts():
    for n, f in [("Serif", "SourceSerifPro-Regular.ttf"),
                 ("Serif-Semi", "SourceSerifPro-Semibold.ttf"),
                 ("Serif-It", "SourceSerifPro-It.ttf"),
                 ("Sans", "Lato-Regular.ttf"),
                 ("Sans-Bold", "Lato-Bold.ttf"),
                 ("Sans-Light", "Lato-Light.ttf"),
                 ("Sans-It", "Lato-Italic.ttf")]:
        pdfmetrics.registerFont(TTFont(n, os.path.join(FONTS, f)))


def jpeg(im, q=88):
    import io
    b = io.BytesIO()
    im.convert("RGB").save(b, "JPEG", quality=q, optimize=True, progressive=True)
    b.seek(0)
    return ImageReader(b)


FIELDS = []          # [{page,x0,y0,x1,y1,kind,name}]
_PAGE = [0]


def rec(g, x0, y0, x1, y1, kind="text", name=None):
    """Record a writing area so the fillable edition can place a form field."""
    if g.dry or x1 - x0 < 8 or y1 - y0 < 6:
        return
    FIELDS.append({"page": _PAGE[0], "x0": x0, "y0": y0, "x1": x1, "y1": y1,
                   "kind": kind, "name": name})


class _Null:
    def __getattr__(self, _):
        return lambda *a, **k: None


class P:
    def __init__(self, c, W, H, M, dry=False):
        self.real, self.dry = c, dry
        self.c = _Null() if dry else c
        self.W, self.H, self.M = W, H, M
        self.y = H - M
        self.cx = W / 2
        self.gap = 24.0

    # ---------- text ----------
    def wrap(self, s, font, size, w):
        out, line = [], ""
        for word in s.split():
            t = (line + " " + word).strip()
            if pdfmetrics.stringWidth(t, font, size) <= w:
                line = t
            else:
                out.append(line)
                line = word
        if line:
            out.append(line)
        return out

    def cstr(self, s, font, size, col, y=None):
        self.c.setFont(font, size)
        self.c.setFillColor(col)
        self.c.drawCentredString(self.cx, self.y if y is None else y, s)

    def lstr(self, s, font, size, col, x=None, y=None):
        self.c.setFont(font, size)
        self.c.setFillColor(col)
        self.c.drawString(self.M if x is None else x, self.y if y is None else y, s)

    def para(self, s, font, size, col, w, lead, center=True):
        for ln in self.wrap(s, font, size, w):
            self.c.setFont(font, size)
            self.c.setFillColor(col)
            if center:
                self.c.drawCentredString(self.cx, self.y, ln)
            else:
                self.c.drawString(self.M, self.y, ln)
            self.y -= lead

    # ---------- chrome ----------
    def bg(self):
        self.c.setFillColor(CREAM)
        self.c.rect(0, 0, self.W, self.H, fill=1, stroke=0)

    def frame(self):
        m = self.M * 0.5
        self.c.setStrokeColor(BEIGE)
        self.c.setLineWidth(0.7)
        self.c.rect(m, m, self.W - 2 * m, self.H - 2 * m, fill=0, stroke=1)

    def header(self, title, sub=None, size=23):
        self.y = self.H - self.M - 12
        for ln in self.wrap(title, "Serif-Semi", size, self.W - 2 * self.M):
            self.cstr(ln, "Serif-Semi", size, BROWN)
            self.y -= size * 1.22
        half = 0.75 * IN
        self.c.setStrokeColor(BEIGE)
        self.c.setLineWidth(1.4)
        self.c.line(self.cx - half, self.y + 6, self.cx - 12, self.y + 6)
        self.c.line(self.cx + 12, self.y + 6, self.cx + half, self.y + 6)
        self.c.setFillColor(ROSE)
        self.c.circle(self.cx, self.y + 6, 2.2, fill=1, stroke=0)
        self.y -= 14
        if sub:
            self.cstr(sub, "Sans", 10, GREY)
            self.y -= 20

    def foot(self, s):
        y = self.M * 0.86 + 12
        for ln in reversed(self.wrap(s, "Serif-It", 10.5,
                                     self.W - 2 * self.M - 0.4 * IN)):
            self.c.setFont("Serif-It", 10.5)
            self.c.setFillColor(GREY)
            self.c.drawCentredString(self.cx, y, ln)
            y += 14

    # ---------- building blocks ----------
    def rules(self, n, gap=None, x0=None, x1=None):
        gap = gap or self.gap
        x0 = self.M if x0 is None else x0
        x1 = (self.W - self.M) if x1 is None else x1
        self.c.setStrokeColor(LINE)
        self.c.setLineWidth(0.7)
        for _ in range(n):
            self.c.line(x0, self.y, x1, self.y)
            rec(self, x0, self.y + 1, x1, self.y + min(gap, 26) - 4)
            self.y -= gap

    def prompt(self, text, n, gap=None):
        for ln in self.wrap(text, "Sans-Bold", 10.5, self.W - 2 * self.M):
            self.lstr(ln, "Sans-Bold", 10.5, BROWN)
            self.y -= 14
        self.y -= 10
        self.rules(n, gap)
        self.y -= 6

    def field(self, label, gap=30, lw=None):
        """Label followed by a rule on the same baseline."""
        self.c.setFont("Sans-Bold", 10.5)
        self.c.setFillColor(BROWN)
        self.c.drawString(self.M, self.y, label)
        x = self.M + pdfmetrics.stringWidth(label, "Sans-Bold", 10.5) + 10
        self.c.setStrokeColor(LINE)
        self.c.setLineWidth(0.7)
        xr = lw or self.W - self.M
        self.c.line(x, self.y - 2, xr, self.y - 2)
        rec(self, x, self.y - 1, xr, self.y + 12, name=label.rstrip(":"))
        self.y -= gap

    def table(self, cols, widths, rows, row_h=None, examples=None,
              zebra=True, head_h=22, fill=True, reserve=0.0, max_h=36.0):
        """A professional ruled table with a filled header band.

        With fill=True the row height expands so the table reaches the
        bottom margin, leaving `reserve` points for anything below it.
        """
        n_rows = rows if isinstance(rows, int) else len(rows)
        if fill:
            avail = self.y - head_h - reserve - self.M * 1.05
            row_h = max(row_h or 24.0, min(max_h, avail / n_rows))
        row_h = row_h or self.gap
        tw = self.W - 2 * self.M
        xs, acc = [], self.M
        for w in widths:
            xs.append(acc)
            acc += tw * w
        xs.append(self.M + tw)
        top = self.y
        # header
        self.c.setFillColor(SAGE)
        self.c.rect(self.M, top - head_h, tw, head_h, fill=1, stroke=0)
        self.c.setFillColor(HexColor("#FFFFFF"))
        for i, name in enumerate(cols):
            cw = xs[i + 1] - xs[i]
            size = 8.2 if len(name) > 14 else 8.8
            self.c.setFont("Sans-Bold", size)
            self.c.drawCentredString(xs[i] + cw / 2, top - head_h + 7.5, name)
        y = top - head_h
        n = n_rows
        for r in range(n):
            if zebra and r % 2 == 1:
                self.c.setFillColor(PANEL)
                self.c.rect(self.M, y - row_h, tw, row_h, fill=1, stroke=0)
            if examples and r < len(examples):
                self.c.setFont("Sans", 9.5)
                self.c.setFillColor(FAINT)
                self.c.drawString(xs[0] + 7, y - row_h + 7, examples[r])
            if not isinstance(rows, int) and rows[r]:
                self.c.setFont("Sans", 9.5)
                self.c.setFillColor(BROWN)
                self.c.drawString(xs[0] + 7, y - row_h + 7, rows[r])
            first = 1 if (not isinstance(rows, int) and rows[r]) else 0
            for ci in range(first, len(widths)):
                rec(self, xs[ci] + 2, y - row_h + 2, xs[ci + 1] - 2, y - 2)
            y -= row_h
        # grid
        self.c.setStrokeColor(LINE)
        self.c.setLineWidth(0.6)
        yy = top - head_h
        for _ in range(n + 1):
            self.c.line(self.M, yy, self.M + tw, yy)
            yy -= row_h
        for x in xs:
            self.c.line(x, top, x, top - head_h - n * row_h)
        self.c.setStrokeColor(BEIGE)
        self.c.setLineWidth(0.9)
        self.c.rect(self.M, top - head_h - n * row_h, tw, head_h + n * row_h,
                    fill=0, stroke=1)
        self.y = top - head_h - n * row_h - 16
        return xs

    def panel(self, title, h, x=None, w=None, y=None, fill=PANEL):
        x = self.M if x is None else x
        w = (self.W - 2 * self.M) if w is None else w
        top = self.y if y is None else y
        self.c.setFillColor(fill)
        self.c.roundRect(x, top - h, w, h, 6, fill=1, stroke=0)
        self.c.setStrokeColor(BEIGE)
        self.c.setLineWidth(0.7)
        self.c.roundRect(x, top - h, w, h, 6, fill=0, stroke=1)
        if title:
            self.c.setFont("Sans-Bold", 9.5)
            self.c.setFillColor(SAGE_D)
            self.c.drawString(x + 12, top - 15, title)
        return top - h

    def panel_lines(self, title, rows, gap=None, x=None, w=None, y=None):
        gap = gap or self.gap
        x = self.M if x is None else x
        w = (self.W - 2 * self.M) if w is None else w
        top = self.y if y is None else y
        h = rows * gap + 34
        self.panel(title, h, x, w, top)
        yy = top - 34
        self.c.setStrokeColor(LINE)
        self.c.setLineWidth(0.7)
        for _ in range(rows):
            self.c.line(x + 12, yy, x + w - 12, yy)
            rec(self, x + 12, yy + 1, x + w - 12, yy + min(gap, 26) - 4)
            yy -= gap
        self.y = top - h - 12
        return self.y

    def space(self, reserve=0.0):
        """Vertical room left above the bottom margin."""
        return self.y - self.M * 1.05 - reserve

    def spread(self, n, reserve=0.0, gap=12.0, lo=40.0, hi=200.0):
        """Panel height so n stacked panels exactly fill the page."""
        return max(lo, min(hi, (self.space(reserve) - gap * (n - 1)) / n))

    def checkbox(self, x, y, s=11):
        self.c.setStrokeColor(SAGE)
        self.c.setLineWidth(1.0)
        self.c.roundRect(x, y, s, s, 2, fill=0, stroke=1)
        rec(self, x, y, x + s, y + s, kind="check")

    def progress_bar(self, x, y, w, h=14, segs=10):
        self.c.setFillColor(PANEL2)
        self.c.roundRect(x, y, w, h, 3, fill=1, stroke=0)
        self.c.setStrokeColor(BEIGE)
        self.c.setLineWidth(0.7)
        self.c.roundRect(x, y, w, h, 3, fill=0, stroke=1)
        self.c.setStrokeColor(HexColor("#FFFFFF"))
        self.c.setLineWidth(0.9)
        for i in range(1, segs):
            xx = x + w * i / segs
            self.c.line(xx, y + 1, xx, y + h - 1)

    def art_full(self, name, veil_to=None):
        p = os.path.join(ART, name)
        if not os.path.exists(p):
            return
        im = Image.open(p).convert("RGB")
        nw, nh = int(self.W / 72 * 300), int(self.H / 72 * 300)
        s = max(nw / im.width, nh / im.height)
        im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))),
                       Image.LANCZOS)
        l, t = (im.width - nw) / 2, (im.height - nh) / 2
        im = im.crop((int(l), int(t), int(l + nw), int(t + nh)))
        self.c.drawImage(jpeg(im, 86), 0, 0, self.W, self.H)


# =============================================================== pages
def p_cover(g):
    c = g.c
    g.art_full("cover.png")
    steps = 200
    band = (g.H - g.H * 0.42) / steps
    for i in range(steps):
        yy = g.H - (i + 1) * band
        a = 0.94 * (1 - i / steps) ** 1.35
        c.setFillColor(Color(0.992, 0.984, 0.965, alpha=a))
        c.rect(0, yy, g.W, band + 1, fill=1, stroke=0)
    m = 0.46 * IN
    c.setStrokeColor(HexColor("#C3B49A"))
    c.setLineWidth(1.1)
    c.rect(m, m, g.W - 2 * m, g.H - 2 * m, fill=0, stroke=1)
    c.setLineWidth(0.5)
    c.rect(m + 6, m + 6, g.W - 2 * m - 12, g.H - 2 * m - 12, fill=0, stroke=1)

    y = g.H - 1.5 * IN
    c.setFont("Sans-Bold", 11)
    c.setFillColor(SAGE_D)
    c.drawCentredString(g.cx, y, "M O N T H L Y")
    y -= 0.66 * IN
    c.setFont("Serif-Semi", 43)
    c.setFillColor(CHAR)
    c.drawCentredString(g.cx, y, "BUDGET")
    y -= 0.56 * IN
    c.setFont("Serif-Semi", 43)
    c.drawCentredString(g.cx, y, "PLANNER")
    y -= 0.32 * IN
    c.setStrokeColor(ROSE)
    c.setLineWidth(1.2)
    c.line(g.cx - 1.6 * IN, y, g.cx + 1.6 * IN, y)
    y -= 0.34 * IN
    c.setFont("Serif-It", 14.5)
    c.setFillColor(BROWN)
    c.drawCentredString(g.cx, y, C.SUBTITLE)

    y -= 0.46 * IN
    pill_w = pdfmetrics.stringWidth(C.TAGLINE, "Sans-Bold", 11) + 46
    c.setFillColor(Color(1, 1, 1, alpha=0.72))
    c.roundRect(g.cx - pill_w / 2, y - 11, pill_w, 30, 15, fill=1, stroke=0)
    c.setStrokeColor(HexColor("#CFC3AC"))
    c.setLineWidth(0.7)
    c.roundRect(g.cx - pill_w / 2, y - 11, pill_w, 30, 15, fill=0, stroke=1)
    c.setFont("Sans-Bold", 11)
    c.setFillColor(SAGE_D)
    c.drawCentredString(g.cx, y - 1, C.TAGLINE)


def p_belongs(g):
    g.bg(); g.frame()
    g.header(C.BELONGS["title"], size=22)
    g.y -= 0.9 * IN
    for f in C.BELONGS["fields"]:
        g.field(f, gap=1.05 * IN)
    g.y -= 0.5 * IN
    g.para(C.BELONGS["quote"], "Serif-It", 12.5, GREY,
           g.W - 2 * g.M - 0.6 * IN, 18)
    g.foot("")


def p_welcome(g):
    g.bg(); g.frame()
    g.header(C.WELCOME["title"], size=19)
    w = g.W - 2 * g.M - 0.2 * IN
    for b in C.WELCOME["body"]:
        g.para(b, "Sans", 10.8, BROWN, w, 16.5)
        g.y -= 10
    g.y -= 6
    for name, desc in C.WELCOME["principles"]:
        top = g.y
        h = 62
        g.panel(None, h)
        g.c.setFont("Serif-Semi", 15)
        g.c.setFillColor(SAGE_D)
        g.c.drawString(g.M + 16, top - 24, name)
        g.c.setFont("Sans", 10.5)
        g.c.setFillColor(BROWN)
        g.c.drawString(g.M + 16, top - 44, desc)
        g.y = top - h - 12
    g.foot(C.WELCOME["quote"])


def p_howto(g):
    g.bg(); g.frame()
    g.header(C.HOWTO["title"])
    g.y -= 8
    h = g.spread(5, reserve=44, gap=14, lo=56, hi=110)
    for i, s in enumerate(C.HOWTO["steps"], 1):
        top = g.y
        g.panel(None, h)
        g.c.setFillColor(HexColor("#E7DFD0"))
        g.c.circle(g.M + 30, top - h / 2, 15, fill=1, stroke=0)
        g.c.setFont("Serif-Semi", 14)
        g.c.setFillColor(BROWN)
        g.c.drawCentredString(g.M + 30, top - h / 2 - 5, str(i))
        g.c.setFont("Sans", 11.5)
        g.c.drawString(g.M + 58, top - h / 2 - 4, s)
        g.y = top - h - 14
    g.foot(C.HOWTO["quote"])


def p_vision(g):
    g.bg(); g.frame()
    g.header(C.VISION["title"])
    g.y -= 6
    for p in C.VISION["prompts"]:
        g.prompt(p, 3)


def p_goals(g):
    g.bg(); g.frame()
    g.header(C.GOALS["title"])
    g.y -= 6
    ph = g.spread(3, gap=14, lo=150, hi=260)
    fgap = (ph - 44) / 4
    for s in C.GOALS["sections"]:
        top = g.y
        h = ph
        g.panel(s, h)
        yy = top - 44
        for f in C.GOALS["fields"]:
            g.c.setFont("Sans-Bold", 9.8)
            g.c.setFillColor(BROWN)
            g.c.drawString(g.M + 14, yy, f)
            x = g.M + 14 + pdfmetrics.stringWidth(f, "Sans-Bold", 9.8) + 8
            g.c.setStrokeColor(LINE)
            g.c.setLineWidth(0.7)
            g.c.line(x, yy - 2, g.W - g.M - 14, yy - 2)
            rec(g, x, yy - 1, g.W - g.M - 14, yy + 11)
            yy -= fgap
        g.y = top - h - 14


def p_year(g):
    g.bg(); g.frame()
    g.header(C.YEAR_VIEW["title"])
    g.gap = 30
    g.table(C.YEAR_VIEW["cols"], [0.16, 0.19, 0.19, 0.19, 0.27],
            C.MONTHS, row_h=30, max_h=50)


def p_month_overview(g):
    g.bg(); g.frame()
    g.header(C.MONTH_OVERVIEW["title"])
    g.y -= 4
    for f in C.MONTH_OVERVIEW["fields"]:
        g.field(f, gap=42)
    g.y -= 8
    avail = g.y - g.M * 1.05
    n = max(7, int((avail - 34) // 30))
    g.panel_lines(C.MONTH_OVERVIEW["calendar_note"], n,
                  gap=(avail - 34) / n)


def p_income(g):
    g.bg(); g.frame()
    g.header(C.INCOME["title"])
    g.table(C.INCOME["cols"], C.INCOME["widths"], C.INCOME["rows"], row_h=27,
            reserve=104)
    g.y -= 4
    for t in C.INCOME["totals"]:
        top = g.y
        g.panel(None, 34, fill=PANEL2)
        g.c.setFont("Sans-Bold", 10.5)
        g.c.setFillColor(BROWN)
        g.c.drawString(g.M + 14, top - 21, t)
        g.c.setStrokeColor(LINE)
        g.c.line(g.M + 200, top - 23, g.W - g.M - 16, top - 23)
        rec(g, g.M + 200, top - 22, g.W - g.M - 16, top - 8)
        g.y = top - 34 - 10


def p_fixed(g):
    g.bg(); g.frame()
    g.header(C.FIXED["title"], "Common examples are shown in grey \u2014 "
                               "write your own amounts beside them.")
    rows = C.FIXED["examples"] + [""] * C.FIXED["extra_rows"]
    g.table(C.FIXED["cols"], C.FIXED["widths"], rows, row_h=30, max_h=44)


def p_variable(g):
    g.bg(); g.frame()
    g.header(C.VARIABLE["title"])
    g.y -= 4
    tw = g.W - 2 * g.M
    for cat in C.VARIABLE["categories"]:
        top = g.y
        h = 62
        g.panel(cat, h)
        cw = (tw - 28) / 3
        for i, f in enumerate(C.VARIABLE["fields"]):
            x = g.M + 14 + i * cw
            g.c.setFont("Sans", 8.6)
            g.c.setFillColor(GREY)
            g.c.drawString(x, top - 36, f)
            g.c.setStrokeColor(LINE)
            g.c.setLineWidth(0.7)
            g.c.line(x, top - 52, x + cw - 16, top - 52)
            rec(g, x, top - 51, x + cw - 16, top - 39)
        g.y = top - h - 11


def p_budget(g):
    g.bg(); g.frame()
    g.header(C.BUDGET["title"])
    rows = C.BUDGET["sections"] + [C.BUDGET["total"]]
    g.table(C.BUDGET["cols"], C.BUDGET["widths"], rows, row_h=32, max_h=46)


def p_needs_wants(g):
    g.bg(); g.frame()
    g.header(C.NEEDS_WANTS["title"])
    g.y -= 4
    tw = g.W - 2 * g.M
    bw = (tw - 14) / 2
    top = g.y
    h = g.space(reserve=170)
    for i, (t, ex) in enumerate([(C.NEEDS_WANTS["needs_title"],
                                  C.NEEDS_WANTS["needs_examples"]),
                                 (C.NEEDS_WANTS["wants_title"],
                                  C.NEEDS_WANTS["wants_examples"])]):
        x = g.M + i * (bw + 14)
        g.panel(t, h, x, bw, top)
        yy = top - 36
        for e in ex:
            g.c.setFont("Sans", 9)
            g.c.setFillColor(FAINT)
            g.c.drawString(x + 14, yy, e)
            yy -= 15
        yy -= 6
        g.c.setStrokeColor(LINE)
        g.c.setLineWidth(0.7)
        while yy > top - h + 14:
            g.c.line(x + 12, yy, x + bw - 12, yy)
            rec(g, x + 12, yy + 1, x + bw - 12, yy + 22)
            yy -= 26
    g.y = top - h - 18
    g.para(C.NEEDS_WANTS["prompt"], "Serif-It", 11.5, BROWN, tw - 0.4 * IN, 17)
    g.y -= 8
    g.rules(4, 28)


def p_bills(g):
    g.bg(); g.frame()
    g.header(C.BILLS["title"])
    g.table(C.BILLS["cols"], C.BILLS["widths"], C.BILLS["rows"], row_h=26,
            reserve=30)
    g.foot(C.BILLS["note"])


def p_subs(g):
    g.bg(); g.frame()
    g.header(C.SUBS["title"])
    g.table(C.SUBS["cols"], C.SUBS["widths"], C.SUBS["rows"], row_h=26,
            reserve=150)
    g.y -= 2
    for p in C.SUBS["prompts"]:
        g.para(p, "Serif-It", 11, BROWN, g.W - 2 * g.M, 16)
        g.y -= 4
        g.rules(2, 26)


def p_savings_goals(g):
    g.bg(); g.frame()
    g.header(C.SAVINGS_GOALS["title"])
    g.y -= 4
    for i in range(C.SAVINGS_GOALS["count"]):
        top = g.y
        h = 128
        g.panel(f"GOAL {i + 1}", h)
        yy = top - 40
        for f in C.SAVINGS_GOALS["fields"]:
            g.c.setFont("Sans-Bold", 9.4)
            g.c.setFillColor(BROWN)
            g.c.drawString(g.M + 14, yy, f)
            x = g.M + 14 + pdfmetrics.stringWidth(f, "Sans-Bold", 9.4) + 8
            g.c.setStrokeColor(LINE)
            g.c.setLineWidth(0.7)
            g.c.line(x, yy - 2, g.W - g.M - 16, yy - 2)
            rec(g, x, yy - 1, g.W - g.M - 16, yy + 10)
            yy -= 21
        g.c.setFont("Sans", 8.6)
        g.c.setFillColor(GREY)
        g.c.drawString(g.M + 14, yy - 2, "PROGRESS")
        g.progress_bar(g.M + 78, yy - 6, g.W - 2 * g.M - 96, 13)
        g.y = top - h - 12
    g.panel_lines(C.SAVINGS_GOALS["notes"], 3, gap=26)


def p_challenge(g):
    g.bg(); g.frame()
    g.header(C.CHALLENGE["title"])
    g.field(C.CHALLENGE["target"], gap=30)
    g.y -= 2
    tw = g.W - 2 * g.M
    cw = (tw - 16) / 2
    top = g.y
    rh = min(34.0, max(24.0, (top - 19 - g.M * 1.05) / 15))
    for col in range(2):
        x = g.M + col * (cw + 16)
        yy = top
        g.c.setFillColor(SAGE)
        g.c.rect(x, yy - 19, cw, 19, fill=1, stroke=0)
        g.c.setFillColor(HexColor("#FFFFFF"))
        g.c.setFont("Sans-Bold", 8.2)
        g.c.drawCentredString(x + cw * 0.12, yy - 13, C.CHALLENGE["cols"][0])
        g.c.drawCentredString(x + cw * 0.45, yy - 13, C.CHALLENGE["cols"][1])
        g.c.drawCentredString(x + cw * 0.80, yy - 13, C.CHALLENGE["cols"][2])
        yy -= 19
        for r in range(15):
            day = col * 15 + r + 1
            if r % 2 == 1:
                g.c.setFillColor(PANEL)
                g.c.rect(x, yy - rh, cw, rh, fill=1, stroke=0)
            g.c.setFont("Sans", 9)
            g.c.setFillColor(BROWN)
            g.c.drawCentredString(x + cw * 0.12, yy - rh + 7, str(day))
            rec(g, x + cw * 0.24 + 2, yy - rh + 2, x + cw * 0.66 - 2, yy - 2)
            rec(g, x + cw * 0.66 + 2, yy - rh + 2, x + cw - 2, yy - 2)
            yy -= rh
        g.c.setStrokeColor(LINE)
        g.c.setLineWidth(0.6)
        yy2 = top - 19
        for _ in range(16):
            g.c.line(x, yy2, x + cw, yy2)
            yy2 -= rh
        for fx in (0.0, 0.24, 0.66, 1.0):
            g.c.line(x + cw * fx, top, x + cw * fx, top - 19 - 15 * rh)
        g.c.setStrokeColor(BEIGE)
        g.c.setLineWidth(0.9)
        g.c.rect(x, top - 19 - 15 * rh, cw, 19 + 15 * rh, fill=0, stroke=1)
    g.y = top - 19 - 15 * rh - 16


def p_emergency(g):
    g.bg(); g.frame()
    g.header(C.EMERGENCY["title"])
    g.y -= 6
    for p in C.EMERGENCY["prompts"]:
        g.field(p, gap=46)
    g.y -= 18
    # thermometer: 10 stacked segments
    top = g.y
    h = g.space(reserve=76)
    bw = 1.7 * IN
    x = g.cx - bw / 2
    g.c.setFillColor(PANEL2)
    g.c.roundRect(x, top - h, bw, h, 8, fill=1, stroke=0)
    g.c.setStrokeColor(BEIGE)
    g.c.setLineWidth(0.9)
    g.c.roundRect(x, top - h, bw, h, 8, fill=0, stroke=1)
    seg = h / 10
    g.c.setStrokeColor(HexColor("#FFFFFF"))
    g.c.setLineWidth(1.0)
    for i in range(1, 10):
        g.c.line(x, top - seg * i, x + bw, top - seg * i)
    g.c.setFont("Sans", 8.4)
    g.c.setFillColor(GREY)
    for i in range(11):
        g.c.drawRightString(x - 8, top - seg * i - 3, f"{100 - i * 10}%")
    g.y = top - h - 18
    g.para("Fill in one segment each time you reach another 10% of your target.",
           "Sans", 10, GREY, g.W - 2 * g.M, 15)
    g.foot(C.EMERGENCY["quote"])


def p_debt(g):
    g.bg(); g.frame()
    g.header(C.DEBT["title"])
    g.table(C.DEBT["cols"], C.DEBT["widths"], C.DEBT["rows"], row_h=27,
            reserve=58)
    g.y -= 2
    tw = g.W - 2 * g.M
    bw = (tw - 14) / 2
    top = g.y
    for i, t in enumerate(C.DEBT["totals"]):
        x = g.M + i * (bw + 14)
        g.panel(None, 40, x, bw, top, fill=PANEL2)
        g.c.setFont("Sans-Bold", 9.6)
        g.c.setFillColor(BROWN)
        g.c.drawString(x + 12, top - 16, t)
        g.c.setStrokeColor(LINE)
        g.c.line(x + 12, top - 31, x + bw - 12, top - 31)
        rec(g, x + 12, top - 30, x + bw - 12, top - 17)
    g.y = top - 40 - 12


def p_debt_plan(g):
    g.bg(); g.frame()
    g.header(C.DEBT_PLAN["title"])
    g.y -= 4
    for s in C.DEBT_PLAN["sections"]:
        top = g.y
        h = 4 * 30 + 36
        g.panel(s, h)
        yy = top - 46
        for f in C.DEBT_PLAN["fields"]:
            g.c.setFont("Sans-Bold", 9.8)
            g.c.setFillColor(BROWN)
            g.c.drawString(g.M + 14, yy, f)
            x = g.M + 14 + pdfmetrics.stringWidth(f, "Sans-Bold", 9.8) + 8
            g.c.setStrokeColor(LINE)
            g.c.setLineWidth(0.7)
            g.c.line(x, yy - 2, g.W - g.M - 14, yy - 2)
            rec(g, x, yy - 1, g.W - g.M - 14, yy + 11)
            yy -= 30
        g.y = top - h - 14
    g.foot(C.DEBT_PLAN["quote"])


def p_weekly(g, idx):
    g.bg(); g.frame()
    g.header(C.WEEKLY["titles"][idx])
    g.table(C.WEEKLY["cols"], C.WEEKLY["widths"], C.WEEKLY["rows"], row_h=25,
            max_h=32)


def p_no_spend(g):
    g.bg(); g.frame()
    g.header(C.NO_SPEND["title"])
    tw = g.W - 2 * g.M
    cw = (tw - 16) / 2
    top = g.y
    rh = min(30.0, max(23.0, (top - 19 - 130 - g.M * 1.05) / 15))
    for col in range(2):
        x = g.M + col * (cw + 16)
        yy = top
        g.c.setFillColor(SAGE)
        g.c.rect(x, yy - 19, cw, 19, fill=1, stroke=0)
        g.c.setFillColor(HexColor("#FFFFFF"))
        g.c.setFont("Sans-Bold", 7.6)
        g.c.drawCentredString(x + cw * 0.09, yy - 13, "DAY")
        g.c.drawCentredString(x + cw * 0.26, yy - 13, "NO-SPEND")
        g.c.drawCentredString(x + cw * 0.58, yy - 13, "WHAT I DID INSTEAD")
        g.c.drawCentredString(x + cw * 0.88, yy - 13, "KEPT")
        yy -= 19
        for r in range(15):
            day = col * 15 + r + 1
            if r % 2 == 1:
                g.c.setFillColor(PANEL)
                g.c.rect(x, yy - rh, cw, rh, fill=1, stroke=0)
            g.c.setFont("Sans", 8.8)
            g.c.setFillColor(BROWN)
            g.c.drawCentredString(x + cw * 0.09, yy - rh + 7, str(day))
            g.checkbox(x + cw * 0.26 - 5, yy - rh + 6, 10)
            rec(g, x + cw * 0.34 + 2, yy - rh + 2, x + cw * 0.78 - 2, yy - 2)
            rec(g, x + cw * 0.78 + 2, yy - rh + 2, x + cw - 2, yy - 2)
            yy -= rh
        g.c.setStrokeColor(LINE)
        g.c.setLineWidth(0.6)
        yy2 = top - 19
        for _ in range(16):
            g.c.line(x, yy2, x + cw, yy2)
            yy2 -= rh
        for fx in (0.0, 0.18, 0.34, 0.78, 1.0):
            g.c.line(x + cw * fx, top, x + cw * fx, top - 19 - 15 * rh)
        g.c.setStrokeColor(BEIGE)
        g.c.setLineWidth(0.9)
        g.c.rect(x, top - 19 - 15 * rh, cw, 19 + 15 * rh, fill=0, stroke=1)
    g.y = top - 19 - 15 * rh - 18
    g.para(C.NO_SPEND["reflection"], "Serif-It", 11.5, BROWN, tw - 0.4 * IN, 17)
    g.y -= 6
    g.rules(3, 26)


def p_grocery(g):
    g.bg(); g.frame()
    g.header(C.GROCERY["title"])
    tw = g.W - 2 * g.M
    bw = (tw - 20) / 3
    top = g.y
    for i, t in enumerate(C.GROCERY["top"]):
        x = g.M + i * (bw + 10)
        g.panel(None, 52, x, bw, top, fill=PANEL2)
        g.c.setFont("Sans-Bold", 8.6)
        g.c.setFillColor(SAGE_D)
        g.c.drawCentredString(x + bw / 2, top - 17, t)
        g.c.setStrokeColor(LINE)
        g.c.line(x + 14, top - 38, x + bw - 14, top - 38)
        rec(g, x + 14, top - 37, x + bw - 14, top - 24)
    g.y = top - 52 - 16
    left_w = tw * 0.56
    right_w = tw - left_w - 14
    ytop = g.y
    day_gap = max(30.0, (ytop - g.M * 1.25) / 7)
    yy = ytop
    for d in C.GROCERY["days"]:
        g.c.setFont("Sans-Bold", 9.2)
        g.c.setFillColor(SAGE_D)
        g.c.drawString(g.M, yy, d)
        g.c.setStrokeColor(LINE)
        g.c.setLineWidth(0.7)
        g.c.line(g.M + 68, yy - 2, g.M + left_w - 8, yy - 2)
        rec(g, g.M + 68, yy - 1, g.M + left_w - 8, yy + 12)
        yy -= day_gap
    gx = g.M + left_w + 14
    gh = ytop - yy + 10
    g.panel(C.GROCERY["list_title"], gh, gx, right_w, ytop + 12)
    ly = ytop - 14
    g.c.setStrokeColor(LINE)
    g.c.setLineWidth(0.7)
    while ly > ytop + 12 - gh + 14:
        g.c.line(gx + 12, ly, gx + right_w - 12, ly)
        rec(g, gx + 12, ly + 1, gx + right_w - 12, ly + 20)
        ly -= 24
    g.y = yy - 6


def p_shopping(g):
    g.bg(); g.frame()
    g.header(C.SHOPPING["title"])
    g.table(C.SHOPPING["cols"], C.SHOPPING["widths"], C.SHOPPING["rows"], row_h=26,
            reserve=34)
    g.foot(C.SHOPPING["prompt"])


def p_triggers(g):
    g.bg(); g.frame()
    g.header(C.TRIGGERS["title"])
    g.y -= 6
    for p in C.TRIGGERS["prompts"]:
        g.prompt(p, 3)


def p_habits(g):
    g.bg(); g.frame()
    g.header(C.HABITS["title"])
    g.y -= 4
    tw = g.W - 2 * g.M
    bw = (tw - 14) / 2
    top = g.y
    h = g.space(reserve=140)
    for i, t in enumerate([C.HABITS["keep"], C.HABITS["change"]]):
        x = g.M + i * (bw + 14)
        g.panel(t, h, x, bw, top)
        yy = top - 40
        g.c.setStrokeColor(LINE)
        g.c.setLineWidth(0.7)
        while yy > top - h + 12:
            g.c.line(x + 12, yy, x + bw - 12, yy)
            rec(g, x + 12, yy + 1, x + bw - 12, yy + 22)
            yy -= 26
    g.y = top - h - 16
    g.panel_lines(C.HABITS["new"], 3, gap=28)


def p_checkin(g):
    g.bg(); g.frame()
    g.header(C.CHECKIN["title"])
    g.y -= 4
    hh = g.spread(4, gap=12, lo=100, hi=170)
    for name, q in C.CHECKIN["sections"]:
        top = g.y
        h = hh
        g.panel(None, h)
        g.c.setFont("Serif-Semi", 13)
        g.c.setFillColor(SAGE_D)
        g.c.drawString(g.M + 14, top - 22, name)
        g.c.setFont("Sans-It", 9.6)
        g.c.setFillColor(GREY)
        g.c.drawString(g.M + 14 + 74, top - 22, q)
        yy = top - 44
        g.c.setStrokeColor(LINE)
        g.c.setLineWidth(0.7)
        while yy > top - h + 12:
            g.c.line(g.M + 14, yy, g.W - g.M - 14, yy)
            rec(g, g.M + 14, yy + 1, g.W - g.M - 14, yy + 20)
            yy -= 24
        g.y = top - h - 12


def p_review(g):
    g.bg(); g.frame()
    g.header(C.REVIEW["title"])
    g.table(C.REVIEW["cols"], C.REVIEW["widths"], C.REVIEW["rows"], row_h=30,
            reserve=64)
    g.y -= 2
    tw = g.W - 2 * g.M
    bw = (tw - 20) / 3
    top = g.y
    for i, t in enumerate(C.REVIEW["totals"]):
        x = g.M + i * (bw + 10)
        g.panel(None, 50, x, bw, top, fill=PANEL2)
        g.c.setFont("Sans-Bold", 8.6)
        g.c.setFillColor(SAGE_D)
        g.c.drawCentredString(x + bw / 2, top - 17, t)
        g.c.setStrokeColor(LINE)
        g.c.line(x + 14, top - 37, x + bw - 14, top - 37)
        rec(g, x + 14, top - 36, x + bw - 14, top - 23)
    g.y = top - 50 - 12


def p_where(g):
    g.bg(); g.frame()
    g.header(C.WHERE["title"],
             "Write your amount and percentage, then shade each bar to compare.")
    g.y -= 2
    tw = g.W - 2 * g.M
    for cat in C.WHERE["categories"]:
        top = g.y
        g.c.setFont("Sans-Bold", 10)
        g.c.setFillColor(BROWN)
        g.c.drawString(g.M, top, cat)
        g.c.setFont("Sans", 8.4)
        g.c.setFillColor(GREY)
        g.c.drawString(g.M + tw * 0.52, top, "AMOUNT")
        g.c.setStrokeColor(LINE)
        g.c.setLineWidth(0.7)
        g.c.line(g.M + tw * 0.62, top - 2, g.M + tw * 0.80, top - 2)
        rec(g, g.M + tw * 0.62, top - 1, g.M + tw * 0.80, top + 11)
        g.c.setFillColor(GREY)
        g.c.drawString(g.M + tw * 0.84, top, "%")
        g.c.line(g.M + tw * 0.88, top - 2, g.M + tw, top - 2)
        rec(g, g.M + tw * 0.88, top - 1, g.M + tw, top + 11)
        g.progress_bar(g.M, top - 26, tw, 13, segs=10)
        g.y = top - 52


def p_savings_review(g):
    g.bg(); g.frame()
    g.header(C.SAVINGS_REVIEW["title"])
    g.y -= 6
    for p in C.SAVINGS_REVIEW["prompts"]:
        g.prompt(p, 3)


def p_wins(g):
    g.bg(); g.frame()
    g.header(C.WINS["title"], size=21)
    g.y -= 8
    hh = g.spread(5, gap=12, lo=80, hi=140)
    for p in C.WINS["prompts"]:
        top = g.y
        h = hh
        g.panel(None, h)
        g.c.setFillColor(ROSE)
        g.c.circle(g.M + 22, top - 20, 3.0, fill=1, stroke=0)
        g.c.setFont("Sans-Bold", 10.2)
        g.c.setFillColor(BROWN)
        g.c.drawString(g.M + 34, top - 24, p)
        yy = top - 46
        g.c.setStrokeColor(LINE)
        g.c.setLineWidth(0.7)
        while yy > top - h + 10:
            g.c.line(g.M + 14, yy, g.W - g.M - 14, yy)
            rec(g, g.M + 14, yy + 1, g.W - g.M - 14, yy + 20)
            yy -= 24
        g.y = top - h - 12


def p_reflection(g):
    g.bg(); g.frame()
    g.header(C.REFLECTION["title"])
    g.y -= 4
    for p in C.REFLECTION["prompts"]:
        g.prompt(p, 2)


def p_next(g):
    g.bg(); g.frame()
    g.header(C.NEXT_MONTH["title"])
    g.y -= 4
    hh = g.spread(6, gap=12, lo=76, hi=130)
    ngap = (hh - 34) / 2
    for s in C.NEXT_MONTH["sections"]:
        g.panel_lines(s, 2, gap=ngap)
        g.y += 12 - 12


def p_dashboard(g):
    g.bg(); g.frame()
    g.header(C.DASHBOARD["title"])
    g.y -= 6
    tw = g.W - 2 * g.M
    bw = (tw - 14) / 2
    top = g.y
    th = max(70.0, (g.space(reserve=200) - 2 * 12) / 3)
    for i, t in enumerate(C.DASHBOARD["tiles"]):
        r, c_ = divmod(i, 2)
        x = g.M + c_ * (bw + 14)
        y = top - r * (th + 12)
        g.panel(None, th, x, bw, y, fill=PANEL)
        g.c.setFont("Sans-Bold", 8.8)
        g.c.setFillColor(SAGE_D)
        g.c.drawString(x + 14, y - 18, t)
        g.c.setStrokeColor(LINE)
        g.c.setLineWidth(0.8)
        g.c.line(x + 14, y - th + 18, x + bw - 14, y - th + 18)
        rec(g, x + 14, y - th + 19, x + bw - 14, y - 22)
    g.y = top - 3 * (th + 12) - 2
    wh = g.spread(2, gap=12, lo=76, hi=150)
    for t in C.DASHBOARD["wide"]:
        g.panel_lines(t, 2, gap=(wh - 34) / 2)


def p_master(g):
    g.bg(); g.frame()
    g.header(C.MASTER["title"])
    g.table(C.MASTER["cols"], C.MASTER["widths"], C.MASTER["rows"], row_h=32,
            max_h=44)


def p_reset(g):
    g.bg(); g.frame()
    g.header(C.RESET["title"])
    g.y -= 10
    hh = g.spread(10, reserve=46, gap=9, lo=40, hi=62)
    for it in C.RESET["items"]:
        top = g.y
        h = hh
        g.panel(None, h)
        g.checkbox(g.M + 16, top - 26, 13)
        g.c.setFont("Sans", 11)
        g.c.setFillColor(BROWN)
        g.c.drawString(g.M + 42, top - 24, it)
        g.y = top - h - 9
    g.foot(C.RESET["quote"])


def p_final(g):
    c = g.c
    g.art_full("final.png")
    steps = 200
    band = (g.H - g.H * 0.40) / steps
    for i in range(steps):
        yy = g.H - (i + 1) * band
        a = 0.93 * (1 - i / steps) ** 1.4
        c.setFillColor(Color(0.992, 0.984, 0.965, alpha=a))
        c.rect(0, yy, g.W, band + 1, fill=1, stroke=0)
    m = 0.46 * IN
    c.setStrokeColor(HexColor("#C3B49A"))
    c.setLineWidth(1.1)
    c.rect(m, m, g.W - 2 * m, g.H - 2 * m, fill=0, stroke=1)

    card_top = g.H - 1.05 * IN
    card_h = 4.5 * IN
    c.setFillColor(Color(1, 1, 1, alpha=0.90))
    c.roundRect(g.M - 6, card_top - card_h, g.W - 2 * (g.M - 6), card_h,
                10, fill=1, stroke=0)
    c.setStrokeColor(BEIGE)
    c.setLineWidth(0.7)
    c.roundRect(g.M - 6, card_top - card_h, g.W - 2 * (g.M - 6), card_h,
                10, fill=0, stroke=1)

    g.y = g.H - 1.55 * IN
    w = g.W - 2 * g.M - 0.3 * IN
    for ln in g.wrap(C.FINAL["statement"], "Serif-Semi", 26, w):
        g.cstr(ln, "Serif-Semi", 26, CHAR)
        g.y -= 34
    g.y -= 4
    c.setStrokeColor(ROSE)
    c.setLineWidth(1.1)
    c.line(g.cx - 1.1 * IN, g.y, g.cx + 1.1 * IN, g.y)
    g.y -= 26
    g.para(C.FINAL["body"], "Sans", 10.8, BROWN, w - 0.35 * IN, 17)
    g.y -= 16
    for p in C.FINAL["prompts"]:
        c.setFont("Sans-Bold", 9.8)
        c.setFillColor(BROWN)
        c.drawString(g.M + 8, g.y, p)
        g.y -= 16
        c.setStrokeColor(LINE)
        c.setLineWidth(0.7)
        c.line(g.M + 8, g.y, g.W - g.M - 8, g.y)
        rec(g, g.M + 8, g.y + 1, g.W - g.M - 8, g.y + 20)
        g.y -= 26


# =============================================================== build
def fitted(mk, draw, foot):
    best = 24.0
    for gap in [24 + i * 0.5 for i in range(40)]:
        g = mk(dry=True)
        g.gap = float(gap)
        draw(g)
        if g.y < foot:
            break
        best = float(gap)
    g = mk(dry=False)
    g.gap = best
    draw(g)


PAGES = []


def build(path, W, H):
    M = 0.72 * IN
    c = rl_canvas.Canvas(path, pagesize=(W, H))
    c.setTitle("Monthly Budget Planner \u2014 A Simple & Beautiful Way "
               "to Organize Your Money")
    c.setAuthor("Cedric Errol Cajelo")
    c.setSubject("A printable monthly budget planner")

    def mk(dry=False):
        return P(c, W, H, M, dry)

    foot = M * 1.05
    plan = [
        ("Cover", p_cover, False),
        ("This Planner Belongs To", p_belongs, False),
        ("Welcome", p_welcome, False),
        ("How to Use Your Planner", p_howto, False),
        ("My Financial Vision", p_vision, True),
        ("My Financial Goals", p_goals, False),
        ("My Year at a Glance", p_year, False),
        ("Monthly Overview", p_month_overview, False),
        ("Income Tracker", p_income, False),
        ("Fixed Expenses", p_fixed, False),
        ("Variable Expenses", p_variable, False),
        ("My Monthly Budget", p_budget, False),
        ("Needs vs. Wants", p_needs_wants, False),
        ("Bill Payment Tracker", p_bills, False),
        ("Subscription Checkup", p_subs, False),
        ("My Savings Goals", p_savings_goals, False),
        ("My Savings Challenge", p_challenge, False),
        ("Emergency Fund", p_emergency, False),
        ("Debt Tracker", p_debt, False),
        ("My Debt Payment Plan", p_debt_plan, False),
        ("Week 1 \u2014 Spending Tracker", lambda g: p_weekly(g, 0), False),
        ("Week 2 \u2014 Spending Tracker", lambda g: p_weekly(g, 1), False),
        ("Week 3 \u2014 Spending Tracker", lambda g: p_weekly(g, 2), False),
        ("Week 4 \u2014 Spending Tracker", lambda g: p_weekly(g, 3), False),
        ("No-Spend Challenge", p_no_spend, False),
        ("Grocery & Meal Budget", p_grocery, False),
        ("Shopping Planner", p_shopping, False),
        ("Understanding My Spending", p_triggers, True),
        ("My Money Habits", p_habits, False),
        ("Weekly Money Check-In", p_checkin, False),
        ("Month-End Budget Review", p_review, False),
        ("Where Did My Money Go?", p_where, False),
        ("My Savings Review", p_savings_review, True),
        ("Celebrate Your Financial Wins", p_wins, False),
        ("Monthly Money Reflection", p_reflection, True),
        ("Next Month\u2019s Money Plan", p_next, False),
        ("My Financial Dashboard", p_dashboard, False),
        ("My Money Goals", p_master, False),
        ("My Financial Reset", p_reset, False),
        ("My Money Has a Plan", p_final, False),
    ]
    global PAGES
    PAGES = [(n, i) for i, (n, _f, _a) in enumerate(plan)]
    for pi, (_name, fn, auto) in enumerate(plan):
        _PAGE[0] = pi
        if auto:
            fitted(mk, fn, foot)
        else:
            fn(mk())
        c.showPage()
    c.save()
    return path


def dump_fields(path):
    import json
    with open(path, "w") as fh:
        json.dump(FIELDS, fh)
    return len(FIELDS)


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
        "/Title": "Monthly Budget Planner \u2014 A Simple & Beautiful Way "
                  "to Organize Your Money",
        "/Author": "Cedric Errol Cajelo",
        "/Subject": "A printable monthly budget planner",
        "/Keywords": "budget, planner, finance, money, savings, expenses, "
                     "printable, debt, tracker",
    })
    with open(path, "wb") as fh:
        w.write(fh)


def main():
    os.makedirs(OUT, exist_ok=True)
    register_fonts()
    FIELDS.clear()
    a = build(os.path.join(OUT, "budget_planner_US_Letter.pdf"), 8.5 * IN, 11 * IN)
    n = dump_fields(os.path.join(OUT, "fields_letter.json"))
    print(f"  recorded {n} writing areas (US Letter)")
    strip_helvetica(a)
    FIELDS.clear()
    b = build(os.path.join(OUT, "budget_planner_A4.pdf"),
              210 / 25.4 * IN, 297 / 25.4 * IN)
    dump_fields(os.path.join(OUT, "fields_a4.json"))
    strip_helvetica(b)
    from pypdf import PdfReader
    for f in (a, b):
        r = PdfReader(f)
        p0 = r.pages[0]
        print(f"{os.path.basename(f)}: {len(r.pages)} pages  "
              f"{float(p0.mediabox.width)/72:.2f} x {float(p0.mediabox.height)/72:.2f} in  "
              f"{os.path.getsize(f)/1e6:.1f} MB")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Build the fillable-PDF edition of the MONTHLY BUDGET PLANNER.

Takes the printable PDF plus the writing areas recorded during layout and
turns each one into a real AcroForm field, so the planner can be typed into
in any free PDF reader, saved, and reused. Bookmarks are added so all forty
pages are one click away.
"""
import json
import os

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")

TEXT_RGB = (0.16, 0.14, 0.12)
TITLE = ("Monthly Budget Planner \u2014 A Simple & Beautiful Way "
         "to Organize Your Money")

BOOKMARKS = [
    "Cover", "This Planner Belongs To", "Welcome",
    "How to Use Your Planner", "My Financial Vision", "My Financial Goals",
    "My Year at a Glance", "Monthly Overview", "Income Tracker",
    "Fixed Expenses", "Variable Expenses", "My Monthly Budget",
    "Needs vs. Wants", "Bill Payment Tracker", "Subscription Checkup",
    "My Savings Goals", "My Savings Challenge", "Emergency Fund",
    "Debt Tracker", "My Debt Payment Plan",
    "Week 1 \u2014 Spending Tracker", "Week 2 \u2014 Spending Tracker",
    "Week 3 \u2014 Spending Tracker", "Week 4 \u2014 Spending Tracker",
    "No-Spend Challenge", "Grocery & Meal Budget", "Shopping Planner",
    "Understanding My Spending", "My Money Habits", "Weekly Money Check-In",
    "Month-End Budget Review", "Where Did My Money Go?", "My Savings Review",
    "Celebrate Your Financial Wins", "Monthly Money Reflection",
    "Next Month\u2019s Money Plan", "My Financial Dashboard", "My Money Goals",
    "My Financial Reset", "My Money Has a Plan",
]

GROUPS = [
    ("Plan", 1, 7), ("Track", 8, 19), ("Spend", 20, 27),
    ("Reflect", 27, 35), ("Review", 36, 39),
]


def build(src, fields_json, dst):
    doc = pymupdf.open(src)
    fields = json.load(open(fields_json))

    per_page = {}
    for f in fields:
        per_page.setdefault(f["page"], []).append(f)

    n = 0
    for pno, items in sorted(per_page.items()):
        page = doc[pno]
        ph = page.rect.height
        # sort top-to-bottom, left-to-right for sane tab order
        items.sort(key=lambda f: (round(ph - f["y1"], 1), round(f["x0"], 1)))
        for i, f in enumerate(items):
            # PDF origin is bottom-left; pymupdf widgets use top-left
            rect = pymupdf.Rect(f["x0"], ph - f["y1"], f["x1"], ph - f["y0"])
            if rect.width < 8 or rect.height < 6:
                continue
            w = pymupdf.Widget()
            w.rect = rect
            w.field_name = f"p{pno + 1}_{i:03d}"
            w.field_label = f.get("name") or ""
            w.text_color = TEXT_RGB
            w.border_width = 0
            w.fill_color = None
            if f["kind"] == "check":
                w.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
                w.field_value = False
            else:
                w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
                w.text_font = "Helv"
                # a consistent, handwriting-sized type on every field
                w.text_fontsize = 9.5 if rect.height >= 15 else 8
                w.field_value = ""
                if rect.height > 40:
                    w.field_flags = pymupdf.PDF_TX_FIELD_IS_MULTILINE
                    w.text_fontsize = 9.5
            page.add_widget(w)
            n += 1

    # bookmarks
    toc = []
    used = set()
    for name, s, e in GROUPS:
        toc.append([1, name, s + 1])
        for p in range(s, min(e + 1, len(BOOKMARKS))):
            toc.append([2, BOOKMARKS[p], p + 1])
            used.add(p)
    for p in range(len(BOOKMARKS)):
        if p not in used:
            toc.append([1, BOOKMARKS[p], p + 1])
    toc.sort(key=lambda t: (t[2], t[0]))
    doc.set_toc(toc)

    doc.set_metadata({
        "title": TITLE + " (Fillable Edition)",
        "author": "Cedric Errol Cajelo",
        "subject": "A fillable monthly budget planner",
        "keywords": "budget, planner, fillable, finance, savings, expenses",
    })
    doc.save(dst, garbage=3, deflate=True)
    doc.close()
    return n


def main():
    total = build(os.path.join(OUT, "budget_planner_US_Letter.pdf"),
                  os.path.join(OUT, "fields_letter.json"),
                  os.path.join(OUT, "budget_planner_FILLABLE.pdf"))
    print(f"budget_planner_FILLABLE.pdf: {total} fields")
    t2 = build(os.path.join(OUT, "budget_planner_A4.pdf"),
               os.path.join(OUT, "fields_a4.json"),
               os.path.join(OUT, "budget_planner_FILLABLE_A4.pdf"))
    print(f"budget_planner_FILLABLE_A4.pdf: {t2} fields")


if __name__ == "__main__":
    main()

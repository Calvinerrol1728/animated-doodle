#!/usr/bin/env python3
"""
Turn the print PDFs into proper ebook editions.

A printable and an ebook are not the same product. Someone reading on a phone,
tablet or Kindle app needs to jump to Day 17 without scrolling through forty
pages, so this adds:

  * a full clickable bookmark outline (every page, all 30 days)
  * ebook metadata: title, author, subject, keywords
  * "fit page" open behaviour so it opens as a whole page, not zoomed in
  * a linked contents page is NOT injected -- the outline panel does the job
    and keeps the page count at a clean 40

Outputs into ./out:
  selfcare_journal_EBOOK.pdf         from the US Letter edition
  selfcare_journal_EBOOK_A4.pdf      from the A4 edition
"""
import os
import sys

from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, DictionaryObject, NameObject, BooleanObject

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content as C  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")

TITLE = "30 Days of Self-Care \u2014 A Gentle Journey Back to Yourself"
AUTHOR = "Cedric Errol Cajelo"
SUBJECT = "A 30-Day Journal for Rest, Reflection & Self-Love"
KEYWORDS = ("self-care, journal, wellness, mindfulness, self-love, mental health, "
            "reflection, gratitude, printable, workbook, prompts")


def outline_plan():
    """(page_index, label, is_child) for the whole book."""
    plan = [
        (0, "Cover", False),
        (1, "This Journal Belongs To", False),
        (2, "Welcome", False),
        (3, "A Gentle Guide", False),
        (4, "My Promise to Myself", False),
    ]
    # 30 day pages start at index 5
    for i, (day, title, _blocks, _motif) in enumerate(C.DAYS):
        plan.append((5 + i, f"Day {day} \u2014 {title.title()}", True))
    # bonus pages
    plan += [
        (35, "My Self-Care Toolkit", False),
        (36, "My Self-Care Menu", False),
        (37, "Things I Want to Remember", False),
        (38, "Looking Back", False),
        (39, "You Made Space for Yourself", False),
    ]
    return plan


def build(src, dst):
    reader = PdfReader(src)
    writer = PdfWriter()
    for pg in reader.pages:
        writer.add_page(pg)

    writer.add_metadata({
        "/Title": TITLE,
        "/Author": AUTHOR,
        "/Subject": SUBJECT,
        "/Keywords": KEYWORDS,
        "/Creator": "30 Days of Self-Care",
        "/Producer": "30 Days of Self-Care",
    })

    # bookmarks -- the 30 days nest under one parent so the panel stays tidy
    days_parent = None
    for idx, label, is_day in outline_plan():
        if idx >= len(writer.pages):
            continue
        if is_day:
            if days_parent is None:
                days_parent = writer.add_outline_item(
                    "The 30 Days", idx, bold=True)
            writer.add_outline_item(label, idx, parent=days_parent)
        else:
            writer.add_outline_item(label, idx, bold=True)

    # open with the bookmark panel visible, pages fitted to the window
    writer._root_object.update({
        NameObject("/PageMode"): NameObject("/UseOutlines"),
        NameObject("/PageLayout"): NameObject("/SinglePage"),
    })
    vp = DictionaryObject()
    vp[NameObject("/DisplayDocTitle")] = BooleanObject(True)
    writer._root_object[NameObject("/ViewerPreferences")] = writer._add_object(vp)
    # /Fit destination on open
    try:
        first = writer.pages[0].indirect_reference
        writer._root_object[NameObject("/OpenAction")] = ArrayObject(
            [first, NameObject("/Fit")]
        )
    except Exception:
        pass

    with open(dst, "wb") as fh:
        writer.write(fh)
    return dst


def main():
    jobs = [
        ("selfcare_journal_US_Letter.pdf", "selfcare_journal_EBOOK.pdf"),
        ("selfcare_journal_A4.pdf", "selfcare_journal_EBOOK_A4.pdf"),
    ]
    for src, dst in jobs:
        s = os.path.join(OUT, src)
        if not os.path.exists(s):
            print("missing", s)
            continue
        d = build(s, os.path.join(OUT, dst))
        r = PdfReader(d)
        print(f"{dst}: {len(r.pages)} pages  "
              f"{os.path.getsize(d)/1e6:.1f} MB  "
              f"title={r.metadata.get('/Title')[:40]!r}")


if __name__ == "__main__":
    main()

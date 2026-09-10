#!/usr/bin/env python3
"""Bootstrap a study deck from raw course notes.

Reads whatever you pasted from the course (slide text, PDF-extracted text, your own summary)
and emits a data/deck.json skeleton: sections from headings, one flashcard per definition-looking
line, and a starter bank of recall prompts you turn into real questions.

  python3 tools/md2deck.py notes.md -o data/deck.json
  python3 tools/validate.py --stats          # then check it

This deliberately does NOT invent answer keys for your assessment. It organises YOUR material so
you can test yourself on it.
"""
from __future__ import annotations
import argparse
import json
import os
import re
import sys

HEAD = re.compile(r"^(#{1,4})\s+(.*)$")
BULLET = re.compile(r"^\s*[-*•]\s+(.*)$")
TERM = re.compile(r"^\s*(?:[-*•]\s*)?\**([A-Z][\w /&'\-]{2,48}?)\**\s*(?:[:—–-]|\bis\b|\bare\b|\bmeans\b|\brefers to\b)\s+(.+)$")
# label prefixes that are metadata, not the term itself — "Term: Loss — ..." must not card as "Term"
LEAD_NOISE = re.compile(r"^(?:key\s+)?(?:term|definition|definition of|glossary|entry|word|meaning|concept)\s*$", re.I)
KEYTERM = re.compile(r"^\s*\**((?:key )?term:?|definition:?|glossary:?)\**\s*(.*)$", re.I)


def title_of(path: str, text: str) -> str:
    for line in text.splitlines():
        m = HEAD.match(line.strip())
        if m:
            return m.group(2).strip()
    return os.path.splitext(os.path.basename(path))[0].replace("_", " ").replace("-", " ").strip() or "Course notes"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("src", nargs="?", default="-", help="notes file, or - for stdin")
    ap.add_argument("-o", "--out", default="data/deck.json")
    ap.add_argument("--max-cards", type=int, default=80)
    args = ap.parse_args()

    text = sys.stdin.read() if args.src == "-" else open(args.src, encoding="utf-8", errors="replace").read()
    if len(text.strip()) < 40:
        print("That input is too short to build anything from — paste the actual course text.", file=sys.stderr)
        return 1

    title = title_of(args.src if args.src != "-" else "notes", text)
    deck = {
        "title": title,
        "subtitle": "auto-imported from notes — review before you study",
        "pass_mark": 70,
        "suggested_time_minutes": 20,
        "sections": [],
        "flashcards": [],
        "questions": [],
    }

    cur = None
    seen_cards: set[str] = set()
    lines = text.replace("\r", "").split("\n")
    for raw in lines:
        line = raw.rstrip()
        s = line.strip()
        if not s:
            continue
        m = HEAD.match(s)
        if m:
            cur = {"title": m.group(2).strip(), "body": "", "points": []}
            deck["sections"].append(cur)
            continue
        if cur is None:
            cur = {"title": "Notes", "body": "", "points": []}
            deck["sections"].append(cur)
        b = BULLET.match(s)
        if b:
            cur["points"].append({"point": b.group(1).strip(), "why": ""})
        else:
            cur["body"] = (cur["body"] + "\n" if cur["body"] else "") + s
        # definition-shaped lines make good cards
        d = TERM.match(s)
        if d and len(deck["flashcards"]) < args.max_cards:
            term, meaning = d.group(1).strip("* ").strip(), d.group(2).strip().rstrip(".")
            if LEAD_NOISE.match(term):
                m2 = TERM.match(meaning)
                if m2:
                    term, meaning = m2.group(1).strip("* ").strip(), m2.group(2).strip().rstrip(".")
                else:
                    term = ""
            k = term.lower()
            if not k or k in seen_cards or len(meaning) < 12:
                continue
            seen_cards.add(k)
            deck["flashcards"].append({"front": f"Define: {term}", "back": meaning, "section": cur["title"]})

    # drop sections that ended up with no usable content
    deck["sections"] = [s for s in deck["sections"] if s["body"].strip() or s["points"]]
    for s in deck["sections"]:
        pts = [p for p in s["points"] if p["point"]]
        if pts:
            s["points"] = pts
            s["body"] = ""
        else:
            s.pop("points", None)

    # starter self-test prompts: turn each note section's first points into question scaffolding
    for s in deck["sections"][:14]:
        for p in (s.get("points") or [])[:3]:
            deck["questions"].append({
                "type": "single",
                "stem": f"[TODO write the question] Recall: {p['point'][:110]}",
                "options": ["correct option — fill in", "plausible distractor", "half-true distractor", "opposite-of-true distractor"],
                "answer": 0,
                "rationale": "",
                "why_wrong": "",
                "section": s["title"],
            })
        if not s.get("points"):
            words = re.findall(r"[A-Za-z][\w\-']{3,}", s["body"])
            if words:
                deck["questions"].append({
                    "type": "fillin",
                    "stem": f"[TODO] From this section, define: {words[0].title()}",
                    "answer": ["<paste the key wording>"],
                    "rationale": "",
                    "section": s["title"],
                })

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    json.dump(deck, open(args.out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"wrote {args.out}")
    print(f"  {len(deck['sections'])} sections · {len(deck['flashcards'])} cards auto-built · {len(deck['questions'])} question stubs (marked [TODO])")
    if not deck["flashcards"]:
        print("  no definition-shaped lines found — write the cards by hand, it is better practice anyway")
    print("next: python3 tools/validate.py --stats  → then edit the stubs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

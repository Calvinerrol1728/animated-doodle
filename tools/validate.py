#!/usr/bin/env python3
"""Deck tooling for the study app.

Usage:
  python3 tools/validate.py                      # validate data/deck.json (or the example deck)
  python3 tools/validate.py --stats              # counts + coverage report
  python3 tools/validate.py --fix-dupes          # drop duplicate stems in place
  python3 tools/md2deck.py notes.md -o data/deck.json   # bootstrap a deck from your raw notes
"""
from __future__ import annotations
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECK = os.path.join(ROOT, "data", "deck.json")
EXAMPLE = os.path.join(ROOT, "data", "deck.json.js")


def load_example() -> dict:
    raw = open(EXAMPLE, encoding="utf-8").read()
    body = raw.split("=", 1)[1].strip().rstrip(";")
    return json.loads(body)


def load_deck() -> tuple[dict, str]:
    if os.path.exists(DECK):
        return json.load(open(DECK, encoding="utf-8")), "data/deck.json"
    return load_example(), "data/deck.json.js (EXAMPLE — placeholder content, not your course)"


def stem_key(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def validate(deck: dict, strict: bool = False) -> tuple[list[str], list[str]]:
    errs: list[str] = []
    warns: list[str] = []
    if not isinstance(deck, dict):
        return ["deck must be a JSON object"], []
    for k in ("sections", "flashcards", "questions"):
        if k in deck and not isinstance(deck[k], list):
            errs.append(f"`{k}` must be an array")
    if not any(len(deck.get(k) or []) for k in ("sections", "flashcards", "questions")):
        errs.append("deck is empty: add sections, flashcards or questions")

    seen_stem: dict[str, int] = {}
    for i, q in enumerate(deck.get("questions") or []):
        at = f"questions[{i}]"
        stem = (q.get("stem") or "").strip()
        if not stem:
            errs.append(f"{at}: missing `stem`")
        else:
            k = stem_key(stem)
            if k in seen_stem:
                warns.append(f"{at}: duplicate of questions[{seen_stem[k]}] — same stem twice")
            else:
                seen_stem[k] = i
        t = (q.get("type") or "single").lower()
        if t not in ("single", "multiple", "multi", "truefalse", "boolean", "fillin"):
            errs.append(f"{at}: unknown type {t!r} (single|multiple|truefalse|fillin)")
            continue
        if t in ("single", "multiple", "multi"):
            opts = q.get("options") or []
            if len(opts) < 2:
                errs.append(f"{at}: needs at least 2 `options`")
                continue
            ans = q.get("answer")
            idxs = ans if isinstance(ans, list) else ([] if ans is None else [ans])
            idxs = [a for a in idxs]
            if not idxs:
                errs.append(f"{at}: `answer` missing")
            for a in idxs:
                if not isinstance(a, int) or not (0 <= a < len(opts)):
                    errs.append(f"{at}: answer index {a!r} out of range (0..{len(opts) - 1})")
            if t == "single" and len(idxs) > 1:
                warns.append(f"{at}: multiple answers but type=single — switch to `multiple`")
            if t in ("multiple", "multi") and len(idxs) < 2:
                warns.append(f"{at}: type=multiple but only one answer selected — is it really 'select all that apply'?")
            if any(not str(o).strip() for o in opts):
                errs.append(f"{at}: blank option text")
        elif t == "truefalse":
            if q.get("answer") is None:
                errs.append(f"{at}: truefalse needs `answer`: true|false")
        elif t == "fillin":
            a = q.get("answer")
            acc = a if isinstance(a, list) else [a]
            if not [x for x in acc if x]:
                errs.append(f"{at}: fillin needs a non-empty `answer` string")
        if not q.get("rationale"):
            warns.append(f"{at}: no `rationale` — the explanation is where the learning happens")
        if not q.get("section"):
            warns.append(f"{at}: no `section` — weak-spot grouping works better with one")

    for i, c in enumerate(deck.get("flashcards") or []):
        at = f"flashcards[{i}]"
        if not (c.get("front") or "").strip():
            errs.append(f"{at}: missing `front`")
        if not (c.get("back") or "").strip():
            errs.append(f"{at}: missing `back`")
        if len(str(c.get("back") or "")) > 600:
            warns.append(f"{at}: back is {len(str(c['back']))} chars — a card should hold one idea, move the rest to notes")

    for i, s in enumerate(deck.get("sections") or []):
        at = f"sections[{i}]"
        if not (s.get("title") or "").strip():
            errs.append(f"{at}: missing `title`")
        if not (s.get("body") or "").strip() and not s.get("points"):
            warns.append(f"{at}: has neither `body` nor `points`")

    if not (deck.get("title") or "").strip():
        warns.append("`title` is empty — the header will read 'Untitled course'")

    # coverage: does every question map to a note/card section?
    note_secs = {s.get("title") for s in deck.get("sections") or []}
    card_secs = {c.get("section") for c in deck.get("flashcards") or [] if c.get("section")}
    q_secs = {q.get("section") for q in deck.get("questions") or [] if q.get("section")}
    for orphan in sorted(q_secs - note_secs - card_secs):
        warns.append(f"questions reference section {orphan!r} but no notes/cards do")
    for dead in sorted((note_secs | card_secs) - q_secs):
        if strict:
            warns.append(f"section {dead!r} has no questions — you cannot self-test it")

    return errs, warns


def stats(deck: dict) -> None:
    print(f"title:      {deck.get('title')}")
    print(f"pass mark:  {deck.get('pass_mark', '(unset → app assumes 70%)')}")
    print(f"time limit: {deck.get('suggested_time_minutes', '(unset)')} min")
    types: dict[str, int] = {}
    for q in deck.get("questions") or []:
        t = (q.get("type") or "single").lower()
        types[t] = types.get(t, 0) + 1
    with_rat = sum(1 for q in deck.get("questions") or [] if q.get("rationale"))
    with_trap = sum(1 for q in deck.get("questions") or [] if q.get("why_wrong") or q.get("whyWrong"))
    print(f"sections:   {len(deck.get('sections') or [])}")
    print(f"flashcards: {len(deck.get('flashcards') or [])}")
    print(f"questions:  {len(deck.get('questions') or [])}  {types or ''}")
    print(f"  with rationale: {with_rat}   with 'why the trap fails': {with_trap}")
    by: dict[str, int] = {}
    for q in deck.get("questions") or []:
        by[q.get("section") or "(none)"] = by.get(q.get("section") or "(none)", 0) + 1
    for k, v in sorted(by.items(), key=lambda kv: -kv[1]):
        print(f"    {v:>3}  {k}")


def main() -> int:
    args = sys.argv[1:]
    deck, src = load_deck()
    print(f"source: {src}\n")
    if "--stats" in args:
        stats(deck)
        return 0
    if "--fix-dupes" in args:
        seen: set[str] = set()
        kept = []
        for q in deck.get("questions") or []:
            k = stem_key(q.get("stem") or "")
            if k and k in seen:
                print(f"dropping duplicate: {(q.get('stem') or '')[:70]}")
                continue
            seen.add(k)
            kept.append(q)
        deck["questions"] = kept
        json.dump(deck, open(DECK, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"wrote {len(kept)} questions to data/deck.json")
        return 0
    errs, warns = validate(deck, strict="--strict" in args)
    for e in errs:
        print(f"ERROR  {e}")
    for w in warns:
        print(f"warn   {w}")
    if not errs and not warns:
        print("deck is valid and consistent ✓")
    stats(deck)
    return 1 if errs else 0


if __name__ == "__main__":
    raise SystemExit(main())

# Study Deck — course-prep app

A self-contained study app for working through a training course: notes, self-rated flashcards,
instant-feedback practice, a timed mock exam, and a weak-spot drill queue built from your own misses.

No build step, no dependencies, no network calls. Everything (your notes, your scores) stays in
`localStorage` in your browser.

## Run it

```bash
./serve.sh                 # http://0.0.0.0:8000
# or: python3 -m http.server 8000 --bind 0.0.0.0
```

Then open the preview. On first load you get a **placeholder example deck** so every mode is
clickable — it is flagged `EXAMPLE DATA` in the header. Replace it with your own material:

```bash
cp data/TEMPLATE.json data/deck.json    # then edit
python3 tools/validate.py --stats       # check it
```

…or click **Paste / import material** in the app and drop in JSON, markdown, or a `.json` file.

## Modes

| Tab | What it does | When to use it |
| --- | --- | --- |
| **Notes** | Your section notes, each ending with "exam trap" notes on why near-miss answers fail, plus reveal-a-card recall prompts | First pass — understand before you memorise |
| **Flashcards** | 3D flip, self-rated *Again / Hard / Good / Easy* | Daily reps; `Space` flips, `1-4` rate, `←/→` move |
| **Practice** | Tutor mode: answer, get the rationale immediately, misses are logged | Learning the material |
| **Mock exam** | Timed, answers held until submit, scored against your `pass_mark`, full review after | Rehearsing the real thing |
| **Weak spots** | Only questions you have missed more than you have nailed | The last 20 minutes before you sit it |

Practice and mock both **randomise order by default** — if you can only answer the questions in the
order the deck lists them, you have memorised positions, not content.

## Deck format

```jsonc
{
  "title": "Course name",
  "pass_mark": 75,                   // used for the mock-exam banner only
  "suggested_time_minutes": 20,
  "sections": [
    { "title": "Scope", "points": [ { "point": "the rule", "why": "why the trap answer fails" } ] },
    { "title": "Scope", "body": "or free-form prose: **bold**, `code`, '- ' bullets" }
  ],
  "flashcards": [ { "front": "prompt", "back": "answer", "section": "Scope" } ],
  "questions": [
    { "type": "single",     "stem": "…", "options": ["…","…"], "answer": 1, "rationale": "…", "why_wrong": "…", "section": "Scope" },
    { "type": "multiple",   "stem": "…", "options": ["…","…","…"], "answer": [0,2] },
    { "type": "truefalse",  "stem": "…", "answer": false },
    { "type": "fillin",     "stem": "…", "answer": ["30 days", "thirty days"] }
  ]
}
```

Prefer writing markdown? `## Section`, `### Card` with `**Front:**` / `**Back:**`, and
`### Q:` with `A)` `B)` … then `Correct: B`, `Rationale:`, `Why-wrong:`. Paste it in the import box
and it is parsed for you (see `data/TEMPLATE.md`).

Fill-in answers are matched loosely: case/punctuation-insensitive, comma-separated parts all
accepted, and "30 days" matches "thirty (30) days".

## Testing

```bash
npm i --no-save jsdom && node .test/smoke.mjs   # 56 headless assertions across all five modes
DBG=1 node .test/smoke.mjs                       # dumps the view DOM at each step
```

The test boots `index.html` in jsdom and drives the real UI: flip/rate a card, answer a full
practice run, sit a timed mock, interrupt a drill and come back to it, import JSON and markdown,
and check that a bad deck is rejected without losing the good one. In the browser,
`window.__studydeck` exposes `{ state, parseMarkdown, applyDeck }` if you want to poke at it.

## Tools

```bash
python3 tools/validate.py             # structural errors + warnings (dupes, missing rationales, orphan sections)
python3 tools/validate.py --stats     # counts by type and by section
python3 tools/validate.py --strict    # also flags sections you cannot self-test
python3 tools/validate.py --fix-dupes # drop duplicate question stems in place
python3 tools/md2deck.py notes.md -o data/deck.json   # bootstrap a deck from raw pasted course text
```

`md2deck.py` reads `## headings` into sections, `- ` bullets into note points, and
definition-shaped lines (`Indemnity — the principle that…`) into flashcards, then leaves `[TODO]`
question stubs for you to finish. It organises **your** material; it does not write answers for
you and will not invent plausible-sounding rules to fill gaps.

## A note on scope

This is a study aid. It does not, and will not, complete or auto-answer an employer's or vendor's
assessment: no answer-key lookups against a live course, no auto-completion of training progress,
no tampering with LMS state. If you are preparing for a mandatory compliance course, the honest
shortcut is understanding it — which is also the version that survives an audit, a manager asking
"so what would you have done?", and the actual job.

## Files

```
index.html          app shell
styles.css          all styling (dark, print-friendly spacing)
app.js              deck store, markdown/JSON import, five renderers, scoring
data/deck.json.js   example placeholder deck (loaded via script tag so file:// also works)
data/TEMPLATE.json  copy → data/deck.json and fill in
data/TEMPLATE.md    markdown import example
tools/              validator + notes→deck bootstrap
serve.sh            http server bound to 0.0.0.0
```

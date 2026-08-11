# Princess Elara and the Secret Garden of Stars

*A Little Story About Kindness, Courage, and Wonder*

An original illustrated children's picture book for ages 3–7.

**📖 Read it: [`princess_elara_and_the_secret_garden_of_stars.pdf`](princess_elara_and_the_secret_garden_of_stars.pdf)**

---

## The book

| | |
|---|---|
| **Pages** | 15 (cover + 13 story pages + ending page) |
| **Trim size** | 8.5 × 11 in portrait |
| **Resolution** | 300 DPI (2550 × 3300 px per page) |
| **Reading age** | 3–7 |
| **Style** | Hand-painted watercolor & soft gouache |

### Story

Elara loves the night sky — until one autumn the stars begin to go out. When a small
star with a bent point falls into her roses, she sets off past the thorn hedge to find
the garden where stars are grown. Along the way she stops to mend a moth's torn wing,
even though stopping costs her time. At the hilltop she finds a golden gate with no
handle and no key, carved with three words: *Kindness opens me.* She cannot open it —
but the moth she saved can.

The kindness she gave away is the very thing that saves her.

---

## Design system

Every page follows one consistent template:

- **Top ~22%** — a large cream/ivory narration bubble with soft, slightly irregular
  hand-painted edges and a decorative border that shifts with the scene
  (honeybees, crescent moons, roses, thorny vines, river reeds, gold filigree).
- **Lower ~78%** — the illustration.
- **Bottom** — a subtle repeating border of tiny flowers, leaves and gold stars.

**Visual hierarchy:** narration always sits in the large cream bubble; character
dialogue sits in smaller pastel bubbles (yellow for the star, sage for the gardener,
pink for Elara) pointing toward the speaker, never covering a face.

**Exceptions by design:** the cover uses a decorative fairytale title panel instead of
a narration bubble, and the ending page uses a smaller cloud bubble ringed with golden
stars, with **THE END** beneath it.

**Character continuity:** Elara is drawn identically throughout — warm light-brown
skin, big dark-brown eyes, long wavy dark-brown hair, a small gold star tiara, and a
lavender-and-soft-pink gown with tiny gold star embroidery.

---

## Repository layout

```
├── princess_elara_and_the_secret_garden_of_stars.pdf   # the finished book
├── STORY.md                                            # manuscript (source of truth)
├── build_book.py                                       # assembles pages → PDF
└── pages/                                              # page art, in reading order
    ├── 00_cover.png
    ├── 03_p01.png … 15_p13.png
    └── 99_ending.png
```

Pages are assembled in filename sort order, so the numeric prefixes control the
sequence. To insert a page between two existing ones, pick an unused prefix.

## Rebuilding the PDF

```bash
pip install pillow
python3 build_book.py
```

Options: `--pages <dir>` to point at a different art directory, `--out <file>` to
change the output path. Each image is scaled to cover the 8.5 × 11 page and
center-cropped, so source art should already be close to a 1:1.294 ratio.

---

## Notes on publishing

The interior meets the 300 DPI requirement of Amazon KDP and IngramSpark. Before
selling, you would still need:

- a full-bleed interior export (add ~0.125 in bleed on all sides) and a separate
  wrap-around cover file sized to the printer's spine calculator for your page count;
- a copyright page and, optionally, an ISBN;
- **AI disclosure** — KDP and most retailers require you to declare AI-generated
  content at upload. It does not prevent publication, but it must be disclosed.

Illustrations were generated with AI and each page's text was proofread against
`STORY.md` word for word.

---

## Print-ready files

`print/interior_print_bleed.pdf` (24pp, 8.75 × 11.25 in with 0.125 in bleed) and
`print/cover_wrap_print.pdf` (full wrap, 17.3663 × 11.25 in) are ready for Amazon KDP
and IngramSpark. Build them with `python3 build_print.py`.

**Edit `AUTHOR`, `PUBLISHER`, `YEAR`, `ISBN` and `DEDICATION` at the top of
`build_print.py` before uploading** — the files currently print `[YOUR NAME]`.

See [`PUBLISHING.md`](PUBLISHING.md) for verified specs, page order, and upload steps.

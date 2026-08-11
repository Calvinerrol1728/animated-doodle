# Publishing Guide

Print-ready files for **Princess Elara and the Secret Garden of Stars**.

| File | What it is |
|---|---|
| `print/interior_print_bleed.pdf` | 24-page interior, 8.75 × 11.25 in (8.5 × 11 trim + 0.125 in bleed) |
| `print/cover_wrap_print.pdf` | Full wrap cover (back + spine + front), 17.3663 × 11.25 in |
| `princess_elara_and_the_secret_garden_of_stars.pdf` | Screen/reading copy, 8.5 × 11, no bleed |

Regenerate both print files with `python3 build_print.py`.

---

## ⚠️ Before you upload — put your name in the book

Open **`book_details.txt`**, replace the placeholders, save, then run:

```bash
python3 build_print.py
```

That's it — both PDFs rebuild in about 15 seconds with your details on the title page,
copyright page, and dedication page.

The file looks like this:

```
author = [YOUR NAME]
publisher = [YOUR IMPRINT]
year = 2026
isbn =
dedication = For every child who stops to help\nsomething small.
```

Notes:

- Only change the text **after** the `=` sign.
- `publisher` can be any name you like ("Moonpath Books") or left empty.
- Leave `isbn` empty if you're using Amazon's free ISBN.
- In `dedication`, `\n` starts a new line.
- Lines starting with `#` are notes and are ignored.

If you forget, the build prints a loud warning and the PDFs will literally say
`[YOUR NAME]` — so you can't ship it by accident.

---

## Verified specs

Both files were checked programmatically and pass:

- ✅ **Trim + bleed** — interior 8.75 × 11.25 in (0.125 in bleed on all four edges); art
  bleeds to the edge via edge-pixel extension, so trimming can never leave a white sliver
- ✅ **300 DPI** — every embedded image measured at exactly 300 DPI
- ✅ **24 pages** — meets the KDP paperback minimum (a 15-page book cannot be published)
- ✅ **Uniform page size** across all 24 pages
- ✅ **All fonts embedded** — the unused `/Helvetica` entry reportlab adds by default is
  stripped, since it trips preflight
- ✅ **Safe area** — no text within 0.5 in of any trim edge
- ✅ **Barcode zone clear** — 2 × 1.2 in at 0.25 in from the lower-right trim of the back
  cover, left blank
- ✅ **File size** — 35 MB interior, 7 MB cover (limit is 650 MB)

### Spine

```
spine = pages × 0.002347 (color interior) + 0.06 = 24 × 0.002347 + 0.06 = 0.1163 in
```

The spine is intentionally **blank**. KDP allows spine text only above 0.0625 in, but in
practice needs ~79+ pages before anything is legible. At 0.116 in, no type fits.

**If your page count changes, the spine width changes and the cover must be rebuilt.**
`build_print.py` derives the spine from the actual interior page count automatically.

---

## Interior page order

| Page | Content |
|---|---|
| 1 | Half title |
| 2 | Blank |
| 3 | Title page |
| 4 | Copyright + AI disclosure |
| 5 | Dedication |
| 6–18 | Story pages 1–13 |
| 19 | Ending page — *"Even the smallest act of kindness…"* + THE END |
| 20 | "Sweet dreams, little one." |
| 21 | "Let's Talk About It" — 5 discussion questions |
| 22 | About This Story |
| 23–24 | Blank |

Pages 23–24 are blanks padding to the 24-page minimum. If you add content later, keep the
total at a multiple of 2 (printers work in leaves) and rebuild the cover.

---

## Uploading to KDP

1. **Paperback → Print options:** select **8.5 × 11 in** trim, **Premium Color** interior,
   **white paper**, **Bleed: Yes**, **Glossy** or matte cover.
2. Upload `print/interior_print_bleed.pdf` as the manuscript.
3. Upload `print/cover_wrap_print.pdf` under "Upload a cover you already have".
4. **AI disclosure** — KDP asks during setup whether your book contains AI-generated
   content. Answer **yes** for images. This does not block publication. The copyright page
   already carries a matching disclosure.
5. Run KDP's **Print Previewer** and check every page before approving. It flags anything
   the automated checks here cannot see.

### IngramSpark

Same interior file works. IngramSpark uses slightly thicker paper stock, so the spine will
differ — pull their exact template and rebuild the cover to match before uploading.

### Colour profile

Both files are RGB, which KDP accepts and converts. For the closest colour match on press,
convert to CMYK (US Web Coated SWOP v2) and export as PDF/X-1a:2001 in Acrobat or Affinity
Publisher. Expect the deep violet night skies to shift slightly duller in CMYK — that is
normal and unavoidable in four-colour printing.

---

## Ebook

For a Kindle ebook you need a front-cover JPG at **1600 × 2560 px** (1.6:1). The current
cover is 8.5 × 11 (1.29:1), so it needs re-cropping or extending — do not simply stretch it.

---

## Legal note

This is general production guidance, not legal advice. Copyright registration, ISBN
purchase, and trade-dress questions are worth a professional's time if you plan to sell at
volume.

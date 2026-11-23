---
name: visual-decks
description: Make presentations, decks, slides and PDF guides that teach with a diagram first and spoken words second, using the fixed deck-engine renderer and component bank.
when_to_use: Any request to make a presentation, deck, slides, pitch, one-pager series or PDF guide, or to fix or redesign one.
---

# Visual decks

Build every deck with this repo's fixed engine. A deck is ONE slides file that puts together pages from the component bank. The PDF is the product; review the PDF, never the HTML.

## Procedure

1. **Write the spec first.** Copy `spec-template.md`. Fill in the job, the reader, when they read it, the purpose, the promise, what the reader wants and their dream outcome, the outcomes list, the vocabulary, and the reader's questions in the order they'll ask them. Ask for anything you can't fill in.
2. **Plan each page before designing it.** For every page, write three lines as a comment in the slides file:
   - `Q:` the one question the reader has at that moment
   - `A:` the one-sentence answer
   - `Outcome:` which outcome from the spec it serves
   If you can't write all three, cut the page.
3. **Pick a component from the bank** (`components/README.md`, `components/gallery.png`) that shows the answer as a picture. Pass in only words and data.
4. **Build:** `python3 slides.py build/` then `node engine/render.js build/`.
5. **Check:** `python3 engine/check.py build/`. It must say PASS.
6. **Look at every image in `build/pages/`, full size.** Fix the slides file and re-run until nothing overlaps, overflows or is cut off, and every page passes the rules below.
7. **Deliver** `deck.pdf` and a short list of gaps (facts you couldn't source).

## Page rules

- **One page, one question.** Each page makes one point, in the order the reader asks.
- **The razor:** if an element doesn't support that page's answer, cut it.
- **At most 3 components per page, each with a meaning:**
  1. a visual (the diagram that teaches),
  2. the spoken text (lead line + supporting line),
  3. optional: a trust element, e.g. a testimonial with the person's photo. Use each quote once.
  The header (wordmark, step strip) doesn't count.
- **Attention path:** visual top-left first (the `.vis` box, 776px wide). Spoken column on the right (~290px). Quote card bottom-right, the last thing the eye reaches. Only the cover may be text-first.
- **The diagram teaches.** Prefer flowcharts, if/else trees, comparisons, bars, timelines and sample documents over paragraphs.
- **Cut redundant labels:** no header crumbs, no labels that repeat the headline, no "what's next" lines, no "Step N done" ticks.
- **No footers and no page numbers.** All sources go on one last "Sources, by page" page.
- **No checkboxes.** Nobody can tick a PDF. Use dots or icons.

## Word rules

- Write only what a person would **say out loud** to the reader, sitting across from them, at about a 9th-grade reading level. Show everything else in the visual.
- **Fixed vocabulary.** Pick one word per idea and use it every time. Explain any other term in plain words where it appears. Reserve "Step" for the deck's steps only.
- **No idioms, gestures, invented labels, or AI-sounding lines** ("Let's be honest", "Here's the thing", "unlock", "game-changer", "You made it").
- **Better text, never smaller text.** Lead line 30px, supporting line 21px. If it doesn't fit, cut or simplify the words.
- One accent phrase per lead line: `kit.ac("...")`.
- **No unsourced claims.** Every fact traces to a source. Don't generalize ("most teams", "often") from thin evidence. If a fact is missing, research it and cite it, or leave it out and list it as a gap.
- **No anti-proof.** Never show what you don't have, can't do or haven't sourced. Leave the topic out instead.
- No placeholder brackets on a page, unless the deck config allows that exact one.

## Persuasion lens (optional): Power, Trust, Likeness

Use it when the deck has to win someone over. Every component should express one of the three.
- **Power** = we have what you want. Show it, don't tell it: numbers, names, results that answer a question the reader is actually asking.
- **Trust** = concrete, doable, step-by-step directions that get the reader a good result if they follow them, even when that means pointing them elsewhere.
- **Likeness** = people like the reader, in their own words, so the reader thinks "this is for me".

## Engine rules

- **Never rewrite the renderer** (`engine/kit.py`, `render.js`, `check.py`) for a deck. Never fork or patch the kit inside a deck.
- **Build from the bank.** A new component only when nothing in the bank fits the page's question. Write it in the slides file, then add it back to the bank: a function in `engine/components.py`, a page in `components/build_gallery.py`, a thumbnail, and a row in `components/README.md`.
- **Brand lives in a theme** (`themes/*.json`): colors, fonts, wordmark, step names. Never hard-code brand colors in a slides file; use `kit.C[...]`.
- **Zero-blur stacked shadows only** (`kit.SHADOW`). A blurred CSS shadow becomes an `/SMask` image that some PDF viewers draw as a gray box.
- **Static TTF fonts only** (no variable fonts, no web-font CDN), so the PDF never gets Type 3 fonts.
- **Images:** photos as JPEG with no transparency; everything else as SVG or CSS. People without a photo get initials in a circle (`photo: None`). Never use a photo of someone who isn't the person quoted.
- Deck-specific banned words and allowed placeholders go in `deck.json` next to the slides file.

## Self-check before delivering

1. `check.py` says PASS, and you looked at every page image.
2. On every page, the visual is seen first and the spoken line is something a person would say.
3. Every page answers exactly one reader question, in spec order, and every element supports that answer.
4. Every fact traces to a source on the sources page. No anti-proof, no unsourced generalizations.
5. Only fixed-vocabulary words. No idioms or AI-sounding lines. No text under 13px except labels and attributions.

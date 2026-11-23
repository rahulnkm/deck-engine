# Deck spec: [deck name]

Fill in every section before you design a page. Delete the guidance lines in italics when you're done.
The generator writes the slides file from this spec, the source files in section 9, and the component bank.

## 1. Job
- **Sender:** _who is speaking, and how they refer to themselves ("we", "I")._
- **Reader:** _one specific person: role, situation, what they know and don't know._
- **When they read it:** _before a call? after a demo? on their own, cold? What have they already done?_
- **Purpose:** _what the reader can do or decide after reading that they couldn't before._
- **Call to action:** _the one thing you want them to do next. If they've already done it (e.g. booked a call), don't ask again._

## 2. The promise
What the reader has by the end, in their words:
- _..._
- _..._

## 3. What the reader wants
**In their words:** _"I want ..., but I don't know how to get it."_
1. _..._
2. _..._
3. _..._

**Dream outcome:** _one sentence: the result they'd pay for, in their words._

## 4. Outcomes
Every element on every page must move the reader toward one of these. If it doesn't, cut it.
- _save time_
- _save money_
- _a smart, informed decision_
- _..._

## 5. Persuasion lens (optional)
- **Power** (we have what you want, shown not told): _evidence that answers a question the reader is actually asking._
- **Trust** (concrete, doable step-by-step directions): _the instructions this deck gives._
- **Likeness** (people like the reader, in their own words): _which quotes, from whom._

## 6. Words
- **Reading level:** about 9th grade. Only what a person would say out loud.
- **Fixed vocabulary** (one word per idea, used every time):
  | Word | Means | Never say instead |
  |---|---|---|
  | _tool_ | _the software being chosen_ | _platform, solution, app_ |
  | | | |
- **"Step" means only:** _Step 1 ..., Step 2 ..., Step 3 ..._ (or "no steps in this deck")
- **Banned words and phrases** (also put them in `deck.json` → `"banned"`): _..._
- **Allowed placeholders** (also in `deck.json` → `"allowed_placeholders"`): _none_

## 7. Structure: the reader's questions, in order
One page per question. For each, the generator writes Q / A / Outcome in the slides file before designing it.

| # | Reader's question | One-sentence answer | Outcome | Component |
|---|---|---|---|---|
| 1 | What is this, and is it for me? | | | `cover` |
| 2 | What will this take me through? | | | `step_map` |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |
| 6 | | | | |
| 7 | | | | |
| last | Where does each fact come from? | | honesty | `sources_page` |

Pages to leave out on purpose: _..._

## 8. Visual system
- **Theme:** `themes/[name].json` (colors, fonts, wordmark, step names).
- **Page:** 1280x720. Visual top-left in the 776px box; spoken column right (~290px); quote card bottom-right.
- **Components:** from `components/README.md`. New ones go back into the bank.
- **Photos:** _folder of JPEGs (no transparency) for quoted people, or "none: initials"._

## 9. Sources (the only allowed facts)
| Source | What it backs | Link or file | Date pulled |
|---|---|---|---|
| | | | |

**Gaps** (facts you need but couldn't source; leave them off the pages):
- _..._

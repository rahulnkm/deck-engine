# Principles

The longer version of the rules in `SKILL.md`, with good and bad examples. The examples use made-up topics.

---

## 1. Start from the reader's questions, not your outline

A deck works when each page answers the question the reader has at that moment. Your outline ("About us, Features, Pricing, Team") follows what *you* want to say. The reader's questions follow what *they* need to decide.

**Bad structure:** Overview → Features → Benefits → Pricing → Contact
**Good structure:**
1. What is this, and is it for me?
2. What will this take me through?
3. Do I need this yet?
4. Which parts apply to me?
5. How do I judge my options?
6. What will it cost?
7. How do I do it?
8. Where does each fact come from?

Write the questions in the spec before you design anything.

## 2. Plan each page in three lines

Before you build a page, write:

```
# Q: Do we need a tool yet?
# A: Yes, when your team loses track of work more than once a month.
# Outcome: save money (don't buy too early)
```

If you can't write the answer in one sentence, the page is trying to do two things. Split it or cut it. If the answer serves none of the outcomes in the spec, cut the page.

## 3. The razor

For every element on a page, ask: does it support this page's answer? Is it a distraction? Does it build trust, show likeness or show power? If not, cut it.

Things that almost always fail the razor:
- A label that repeats the headline ("Pricing" above a big price).
- Column headers like "What you want" / "Our answer" when the layout already says it.
- "Next up: ..." lines. The step strip already shows where the reader is.
- "Step 2 done" ticks. Same reason.
- Decorative icons that don't mean anything.
- Footers and page numbers. Sources go on one last page.

## 4. Three components, each with a meaning

A page has at most three components:

1. **A visual** that teaches the answer.
2. **The spoken text:** a lead line and an optional supporting line.
3. **Optional, a trust element:** a quote from a real person with their photo, or a short testimonial.

**Bad:** a chart, a paragraph, three bullet points, a quote, a callout box and a button.
**Good:** a flowchart (top-left), "You need a tool when your team *loses track* of work." (right column), one quote card (bottom-right).

## 5. The attention path

People look at the picture first, then read. Put things where the eye goes:

```
+------------------------------------------+----------------+
| VISUAL (776px wide)                      | Lead line 30px |
| the diagram that teaches                 | Support 21px   |
| eye lands here first                     |                |
|                                          |                |
|                                          | [quote card]   |
+------------------------------------------+----------------+
```

The cover may lead with text. Every other page leads with the visual.

## 6. The diagram teaches

People learn more from a good diagram than from the same words in a paragraph. Before writing any sentence, ask: what picture would make this obvious?

| If the answer is... | Show it as... | Bank component |
|---|---|---|
| "It depends on X" | an if/else tree or a yes/no fork | `converge_decide`, `yes_adds_flow` |
| "A is better for some people, B for others" | a two-path comparison with "Pick A if..." | `two_path_compare` |
| "This is bigger than that" | bars | `bar_chart` |
| "First this, then that" | a process row or a step map | `process_doc`, `step_map` |
| "It changes over time" | stage cards or a timeline | `stage_cards`, `bar_chart(timeline=...)` |
| "You'll end up with this document" | a sample of the document | `process_doc` |
| "Here are your options" | an icon grid | `module_grid`, `feature_cards` |
| "Check these things" | a table: ask / how to check / good sign | `check_table` |
| "It costs this much" | one big number + what drives it | `number_hero` |

**Bad:** "Our plan includes boards for visual planning, sprints for time-boxed work, guest access for client visibility, and time tracking for billing."
**Good:** four cards, each with a chip (Boards, Sprints, Guest access, Time tracking), one line on what it does, and one concrete example.

## 7. Words a person would say out loud

Read every line out loud as if you were sitting across from the reader. If you'd never say it that way, rewrite it.

| Bad | Good |
|---|---|
| "Leverage a unified platform to streamline cross-functional workflows." | "Everyone sees the same list of tasks." |
| "Here's the number you've been waiting for." | "A year costs $1,152 for 12 people." |
| "Let's be honest: most tools fail." | "Pick a tool your team will still use in six months." |
| "Unlock seamless collaboration." | "Clients can see their project without emailing you." |
| "The whole road, start to finish." | "Three steps, from 'do we need this?' to a tool your team uses." |

Aim for a 9th-grade reading level: short sentences, common words, one idea per sentence.

## 8. Fixed vocabulary

Pick one word per idea and use it every time. If page 3 says "tool", page 6 can't say "platform" and page 8 "solution". Readers assume a new word means a new thing.

- List your words in the spec (`Words` section).
- Explain any word outside the list in plain words, right where it appears: "SSO (one login for all your apps)".
- Reserve "Step" for the deck's own steps. Don't use it for anything else.

## 9. Better text, never smaller text

The lead line is 30px and the supporting line is 21px. Always. When a line doesn't fit, the problem is the words.

**Bad:** shrink the supporting line to 15px to fit three sentences.
**Good:** cut to one sentence that says the one thing the reader needs.

Labels (11px caps) and attributions (12-13px) are the only small text.

## 10. No unsourced claims

Every fact on a page traces to a source listed on the sources page. Don't generalize from thin evidence.

| Bad | Good |
|---|---|
| "Most teams abandon their first tool." | (leave it out, or cite a study that says so) |
| "Trusted by thousands." | "1,200 teams use it (company report, March 2026)." |
| "Often cheaper than the alternatives." | "$8 per person per month (pricing page, June 2026)." |

If a fact you need is missing, research it with trustworthy sources and add it, with citations, to a source file before using it. If you can't find it, leave the topic out and list it as a gap in your delivery note.

## 11. No anti-proof

Never show something you don't have, can't do or haven't sourced. It plants the doubt you're trying to remove.

| Bad | Good |
|---|---|
| "We don't publish our uptime yet." | (leave uptime out) |
| "No customer reviews so far." | (leave reviews out) |
| "Claims process: coming soon." | "Ask us about it on the call." |

## 12. Trust elements: real people, real words

- Use real quotes from real people, with their permission and their photo.
- Use each quote once per deck.
- Never use a photo of someone who isn't the person quoted. With no photo, the engine draws initials in a circle.
- A quote earns its place when it says something the reader has lived ("We found out a task was late when the client asked about it."), not when it's generic praise ("Great product!").

## 13. No checkboxes

A deck is read, not filled in. A checkbox invites an action the reader can't take. Use dots, icons or numbers.

## 14. Sources on the last page

No footers, no page numbers, no tiny source lines under charts. One last page, "Sources, by page", lists each page number and the source of every fact on it. Add any disclaimer as one line under it.

## 15. Power, Trust, Likeness (optional persuasion lens)

When a deck must win someone over, check that every component expresses one of these:

- **Power: we have what you want.** Make the gap the reader feels as large as is honest. Show it, don't tell it. Evidence must answer a question the reader is actually asking; never use a number just because it looks impressive.
  *Bad:* "We're the best." *Good:* "Quote in 10 minutes" next to a timeline that shows it.
- **Trust: concrete, doable directions.** Step-by-step instructions the reader can follow and get a good result, even when that means sending them to someone else.
  *Bad:* "Do your research." *Good:* "Invite one teammate. Watch them add a task. Good sign: under 5 minutes, with no help."
- **Likeness: people like the reader, in their own words.** Trigger self-recognition: "this is for me", "that happened to me".
  *Bad:* "Teams everywhere love us." *Good:* a quote from someone with the reader's job, describing the reader's exact problem.

## 16. Review the PDF, not the HTML

The browser preview lies: fonts can differ, shadows can turn into gray boxes, text can overflow at print size. `check.py` rasterizes the PDF itself into `pages/`. Look at every image at full size before you deliver. Fix the slides file and re-run until:

- nothing overlaps, overflows or is cut off,
- no text is under 13px except labels and attributions,
- the visual is the first thing you see on each page.

## 17. Why the engine is fixed

Every deck that rewrites its own renderer re-learns the same bugs: blurred shadows that print as gray boxes, variable fonts that become Type 3, images with alpha channels. The engine solves them once. Decks change words and data only. When a deck needs something new, it goes back into the bank so the next deck gets it for free.

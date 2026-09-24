---
name: pitch-deck-writer
description: Builds an investor or lender pitch deck as a PowerPoint (.pptx) file from the business's feasibility study. It follows the proven narrative (problem, solution, why now, market, competition, business model, traction, financials, team, the ask), puts one idea per slide with the takeaway as the headline, fills every financial figure from Foundation's calculation engine through the bundled renderer, and runs visual QA on every slide. Use when someone asks for "a pitch deck", "investor presentation", "slides for my bank meeting", "turn my business plan into a deck", or a ".pptx". Works with a connected Foundation MCP server (engine-computed financial slides) or standalone (no financial result slides).
---

# Pitch Deck Writer

A seed investor spends about **3–4 minutes** on a deck. Many aren't read to the end, and the
first slide gets far more attention than any other. So the deck has to make its case in the
headlines alone. YC's rules are **legibility, simplicity and obviousness**: one idea per slide,
large type, and no decoration that doesn't carry meaning. Sequoia's structure is the default
narrative, and it expects a bottom-up market size.

## How numbers work

Same rule as the business-plan-writer skill:

- Computed figures appear in the spec only as `{{path|format}}` tokens, filled from a facts
  file holding the engine's own output.
- The projection chart (`"from": "results.projection"`), the scenarios table and the
  competitor grid are generated from the facts directly.
- Never type a computed figure. A path that doesn't exist stops the build.

## Step 0: Mode and inputs

Look for the Foundation MCP tools (a client may add a prefix).

- **Connected:** confirm the project. Save `facts.json` with `currency`, `project`
  (`get_project`), `results` (`compute_feasibility`) and `scenarios` (`compute_scenarios`),
  pasted in verbatim. Run the market-research skill first if there's no
  `competitorBenchmark` or market sizing yet.
- **Standalone:** no engine figures. Build the story slides; for the financial slide, show
  the investment inputs and the pricing and say projections come from Foundation. Don't
  invent profit, IRR or payback figures.

Ask in one round for anything you still need: the audience (angel, VC, bank or grant body),
the amount and instrument, the team bios, any traction (customers, pre-orders, letters of
intent, revenue so far), and a one-line tagline.

## Step 1: Storyline (write the headlines first)

Write every slide's **headline as its takeaway, as a full sentence**. For example, "No one on
the route combines specialty coffee, food and a 7am opening", not "Competition". Read the
headlines in sequence. If they don't tell the whole story alone, fix them before designing
anything.

Default sequence (10–13 slides):

| # | Slide | Type |
|---|---|---|
| 1 | Company + one-line tagline | `title` |
| 2 | Problem: specific, quantified, from the customer's point of view | `statement` (+ `points`) |
| 3 | Solution / product | `statement` or `bullets` |
| 4 | Why now | `statement` |
| 5 | Market: bottom-up TAM/SAM/SOM with sources | `market` |
| 6 | Competition: the benchmark grid, your row highlighted | `benchmark` |
| 7 | Business model: pricing and unit economics (inputs, or `saasMetrics` tokens) | `kpis` or `table` |
| 8 | Traction / validation (skip it rather than fake it) | `kpis` or `bullets` |
| 9 | Financials: headline figures | `kpis` with engine tokens |
| 10 | Projection | `chart` from `results.projection` |
| 11 | Downside: Worst / Base / Best | `scenarios` |
| 12 | Team | `team` |
| 13 | The ask + use of funds + milestones | `ask` |
| 14 | Close / contact | `closing` |

- **Bank or lender audience:** move the downside and repayment capacity forward, and play
  down "why now" and exit.
- **Grant body:** add impact, such as jobs (`project.overview.employment`) and local benefit.

## Step 2: Write the spec

Format: `references/spec-format.md`.

- At most about 25 words of body text per slide, and 3–4 points maximum. Put detail in the
  speaker notes (`notes`).
- Headlines: 1–2 lines. The renderer warns when text probably overflows its box.
- Every slide already carries a visual element: a big number, a chart, a grid, bars, or an
  accent rule. Don't add clip-art.
- Use-of-funds percentages must add up to 100 (the renderer checks this).
- Consistency: the same numbers as the business plan and the project. Same ask, same dates,
  same team.

## Step 3: Render and QA

```
python scripts/build_pptx.py deck.json pitch-deck.pptx --facts facts.json --png qa/
```

This needs `python-pptx` and `matplotlib` (preinstalled in Claude's sandbox), plus LibreOffice
and PyMuPDF for the PNG step when available.

- Exit code 2: a token path is wrong. Fix the path.
- **Look at every slide PNG.** Treat QA as a bug hunt, not a formality. Check for overflow,
  collisions, a headline that wraps to three lines, an unreadable chart, an empty-looking
  slide, or a number that contradicts another slide. Fix, re-render and look again.
- If LibreOffice isn't available, say that visual QA wasn't possible, and still fix every
  renderer WARNING.

## Step 4: Deliver

The `.pptx`, plus a one-paragraph note: the storyline in headline form, which slides rely on
`[estimate]` inputs, and what would strengthen the deck most (usually traction evidence).

## Guardrails

- No fabricated traction, logos, testimonials or team credentials.
- The market numbers are the market-research skill's sourced figures, with sources on the
  slide.
- Competitor claims in the grid must be verifiable (public sources).

## Sources

DocSend/Papermark deck-reading data (average review time about 3.7 minutes; first slide read
most; only about 58% read to the end), YC seed deck guidance (legibility, simplicity,
obviousness) and Sequoia's template: [DocSend](https://www.docsend.com/pitch-deck-metrics/),
[Papermark](https://www.papermark.com/pitch-deck-metrics),
[YC library](https://www.ycombinator.com/library/search?query=pitch+decks),
[Sequoia format](https://pitchbuilder.io/blogs/news/what-is-the-sequoia-pitch-deck-model).
Slide QA approach inspired by Anthropic's public `pptx` skill (referenced, not copied; that
skill is source-available, not open source).

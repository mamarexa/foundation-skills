# Writing style: no AI tells

<!-- Shared by every Foundation skill that writes prose. All copies must stay identical:
     skills/tests/test_scripts.py checks it. -->

Everything these skills write (plans, decks, memos, reports, emails) goes to lenders,
investors and customers. Text that reads as machine-written costs the founder credibility
before anyone looks at the numbers. So every skill that writes follows this guide, and runs a
dedicated pass for it before delivering.

## Where the rules come from

- Wikipedia's editors keep a field guide to recognisable machine-written text, maintained by
  WikiProject AI Cleanup: [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).
  Background: [Artificial intelligence in Wikimedia projects](https://en.wikipedia.org/wiki/Artificial_intelligence_in_Wikimedia_projects).
  The checklist below paraphrases it.
- **If a public "humanizer" skill built on that guide is installed, run it as the final pass
  over the prose.** For example [blader/humanizer](https://github.com/blader/humanizer)
  (MIT, works with Claude Code, Codex and other agents via `npx skills add blader/humanizer`).
  If none is installed, apply the checklist below yourself.
- Whatever tool does the pass, it may change **wording only**. It must never change or add a
  number, name, date, source or `{{token}}`. Re-check any sentence that contains one.

## Hard rules

1. **No em dashes (—)**, and no spaced en dashes ( – ) used as dashes. Use a comma, a colon,
   parentheses, or two sentences. (En dashes in ranges such as "28–35%" are fine.)
2. **No hype or sales language:** revolutionary, game-changing, seamless, cutting-edge,
   unlock, unleash, elevate, empower, world-class, best-in-class (unless it quotes a cited
   benchmark).
3. **No chatbot leftovers:** "I hope this helps", "Let me know if…", "Certainly!", "Great
   question", "As an AI…".
4. **No unnamed authorities:** "experts say" or "studies show" without naming the source.
   Name it, or cut the claim.

## Checklist for the review pass

**Staging instead of stating**
- "Not X, but Y" or "It's not just about X" contrasts that add drama rather than facts.
  State Y.
- Short one-line closers that restate the paragraph ("That's the real opportunity.").
  Delete them.
- Run-ups ("Here's the thing:", "Let's dive in"). Start with the point.
- Arguing with objections nobody raised.

**Rhythm by rule**
- Lists of exactly three by habit. Use as many items as there really are.
- Several sentences in a row that start the same way.
- Stacked hedges ("could potentially"). Pick one, or state it plainly.

**Inflation**
- Overused words: delve, tapestry, testament, pivotal, crucial, robust, landscape, realm,
  foster, underscore, showcase, vibrant, meticulous, intricate, interplay, leverage,
  synergy, holistic. Use the plain word.
- Ordinary facts called "a pivotal moment" or "a key milestone". Keep the fact, drop the
  significance claim.
- Vague "-ing" add-ons ("…, highlighting its commitment to quality"). Cut them, or make
  the claim concrete.
- "Serves as" / "stands as" / "boasts" where "is" / "has" works.

**Formatting by rule**
- Bold used as decoration. Bold only what a skimming reader must not miss.
- Title Case Headings. Use sentence case ("Market analysis", not "Market Analysis").
- Emoji, decorative dividers and needless headings in short sections.

**Leftovers**
- Guessing to fill a gap ("likely", "presumably") without a source. Say what's unknown.
- A section's first sentence repeating its heading.
- Talking about earlier drafts ("updated to reflect…").

## What good looks like here

Short declarative sentences. A number with its source beats an adjective. Name the customer,
the place, the price and the competitor. Say what could go wrong, plainly. Write as a careful
analyst would for a bank credit committee.

## Automatic check

The business-plan and pitch-deck renderers run `scripts/writing_lint.py` on the spec and warn
on em dashes, the overused words above, chatbot leftovers and stock constructions. A warning
must be fixed or consciously kept (for example a quoted source's own words). The script only
catches the mechanical tells, so the review pass above is still required.

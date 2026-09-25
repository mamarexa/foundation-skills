---
name: market-research
description: Market sizing (TAM, SAM, SOM) and competitor benchmarking for a new venture, built from sourced, checkable data. It counts customers bottom-up and cross-checks with a top-down estimate, profiles the competitors from their public pricing, features and reviews, fills a competitors × features benchmark grid, and checks whether the business's revenue plan is realistic against the market it can actually reach. Use when someone asks "how big is my market", "TAM SAM SOM", "who are my competitors", "competitor analysis", "benchmark my competitors", "what do competitors charge", "market research for my business plan or pitch deck", or "is my revenue forecast realistic". When prices or terms aren't public, it prepares an outreach kit for the founder: a table of competitors' public contact details, honest email and call templates, and the rules for using them. The agent never contacts anyone itself. Works with a connected Foundation MCP server (writes the market size and the competitor benchmark into the project) or standalone.
---

# Market Research

You act as a market analyst preparing the market chapter of a feasibility study or pitch.
Investors and lenders discount two things immediately:

- a TAM quoted from a headline industry report with "we only need 1%";
- a competitor slide that says "no real competition".

Your job is to replace both with numbers and facts the founder can defend line by line.

## Step 0: Mode

Look for the Foundation MCP tools (`get_project`, `update_market_sizing`,
`update_competitor_benchmark`; a client may
add a prefix).

- **Connected:** `list_projects`, confirm the project, then `get_project`. It gives the business
  description, overview, revenue rows and any existing `competitorBenchmark`. Build on the
  existing grid instead of replacing it blindly.
- **Standalone:** work from what the founder tells you.

In both modes you need **web search / browsing**. If you have none, say so. Then produce the
method, the formulas and a research checklist for the founder to fill in, and don't invent
figures.

## Step 1: Define the market precisely

Before any number, agree with the founder on the following (ask once, in one batch):

- **Customer unit:** who buys, as a countable thing. Households, cafés, logistics firms with
  20–200 trucks, dental practices, commuters passing a location per day.
- **Geography** the business can actually serve now, and later.
- **The job** the product does, and the **alternatives** customers use today. The alternatives
  include doing nothing and doing it themselves.
- **Price per customer per year**, from the project's revenue rows if connected.

A market definition that's too broad (all of "food", all of "SMB software") is the most common
error. Narrow it until each customer unit is countable.

## Step 2: Size it: bottom-up first, top-down as a cross-check

**Bottom-up (primary):**

- **TAM** = all customer units that have the need × annual spend per customer. Spend is this
  product's price, or the current spend on the alternatives.
- **SAM** = the part of TAM this business model can reach: its geography, segment,
  channel, language and regulation.
- **SOM** = what this business can realistically win in 3–5 years, **built from its own
  go-to-market capacity**. Examples: sales reps × deals per rep per year; store footfall ×
  conversion; marketing budget ÷ acquisition cost per customer (CAC); seats × table turns ×
  days. SOM is not "x% of SAM".

**Top-down (cross-check):** start from an industry report, a government statistic or a
listed competitor's revenue, and narrow it to the SAM definition. If the top-down and
bottom-up SAM differ by more than about 50%, find out why before reporting either one.

**Sources, in order of preference:** government statistics (census, business registers,
trade statistics), industry association data, listed companies' annual reports, reputable
research firms' published figures, then press. Cite each number with its source, year and URL.
Label every derived figure with its formula, for example
`12,400 cafés [ONS 2025] × £3,100/yr [our price] = £38.4M`.

**Sanity rules:**

- A new entrant's Year-1 share rarely exceeds 1–2% of SAM. More needs a specific reason, such as
  signed contracts or a captive channel.
- Physical local businesses (a café, a shop, a clinic) have a *catchment area*, not a national
  market. Size them from footfall, population within a radius and visit frequency.
- Keep **market value** (money spent) separate from **market volume** (units, customers).

**Save it.**

- Connected: call `update_market_sizing` with `customerUnit`, `geography`, and for each of
  `tam`, `sam` and `som` an annual `value` (in the project's currency), a `basis` (the formula
  in words) and a `source`. The app's Market Size step shows it and flags levels that don't nest.
- Standalone: put the same object in `marketSizing` in `foundation-project.json`.

## Step 3: Competitors

1. **Identify** 5–10 competitors across three rings: direct (same offer, same customers),
   indirect (a different offer for the same job) and substitutes (doing nothing, doing it
   themselves, spreadsheets). Search the way a customer would, for example
   "<product> near <city>", "<problem> software", marketplace listings and review sites.
2. **Profile each one from public sources only:**
   - website, published price list or menu, plans and tiers;
   - features and service levels;
   - locations, opening hours and delivery area;
   - review scores and **recurring complaints**, which point to gaps;
   - funding and size signals, such as headcount or number of locations.

   Record the source URL and date for every fact.
3. **Features to compare:** pick 6–12 features **customers actually choose on**. Use review
   language and buyer guides, not the founder's own feature list. Include price-related ones
   such as "free tier", "no setup fee" and "delivery included".
4. **Benchmark grid:** competitors are rows, features are columns, and a check means the
   competitor verifiably offers the feature. Include the founder's own planned offer as the
   first row (for example "Us (planned)"), so the gaps are visible.
   - Connected: `update_competitor_benchmark` with the full grid. Keep the ids of existing rows
     and columns, and send everything you want kept, because it replaces the whole grid.
   - Standalone: put it in `competitorBenchmark` in `foundation-project.json` (format: the
     feasibility-analyst skill's `references/handoff-format.md`).
5. **Price reference table** (in the report): each competitor's comparable price point,
   normalized to the same unit (per month, per cover, per kg), with source and date. The
   pricing-optimizer skill uses this table.
6. **Gaps the public sources can't fill** (prices not published, service terms, lead times):
   prepare the **founder's outreach kit** (Step 3b). Don't guess.

## Step 3b: Founder's outreach kit (the founder makes the contact, never you)

When important facts aren't public, give the founder what they need to find them out
themselves, following `references/outreach-kit.md`:

1. **Contact table:** for each competitor, the **business's** public contact channels only:
   website contact page, general or sales email, main phone number, booking or quote form,
   opening hours. Include the source URL. No personal emails or phone numbers of individual
   employees, and nothing scraped from behind a login.
2. **What to find out:** per competitor, the specific open questions (for example "price for
   20 seats, annual billing" or "minimum order and delivery charge").
3. **Drafts:** short, honest email templates and call scripts for the approaches in the
   reference file (a genuine enquiry, open market research, or a supplier/partner enquiry),
   with the questions filled in. Mark the parts the founder must adapt to be true for them.
4. **The rules**, in plain words: keep contacts short, don't place fake orders or book fake
   demos, don't sign anything under a false identity, don't ask for confidential information,
   and check call-recording consent rules before recording.

Put the kit in a separate file (`outreach-kit.md`) so it's easy to use. Once the founder
brings answers back, add them to the benchmark and price table with the source
"founder enquiry, <date>".

## Step 4: Reality-check the plan (connected)

Call `compute_feasibility` and read the projection's revenue by year. Compare the engine's
Year-1 and final-year revenue with the SOM and the SAM, as a share of each. If the plan needs
more than the SOM, or an implausible share of SAM, say so plainly. Point to the revenue rows
(volumes, customer counts) that should come down. Also check the reverse: a plan that's tiny
relative to a reachable SOM may be underselling the opportunity.

## Step 5: Deliver

Write `market-research.md` (or the format the founder wants) with these sections:

1. **Market definition:** the customer unit, geography, the job and the alternatives.
2. **Market size:** TAM, SAM and SOM with formulas, sources and the top-down cross-check,
   plus a one-sentence verdict.
3. **Competitive landscape:** the three rings, the grid (or a pointer to it in Foundation),
   the price reference table and 3–5 insights. Insights are gaps and weak points competitors
   leave open, *not* "we're better at everything".
4. **Implications for the plan:** from Step 4, and which positioning the evidence supports.
5. **Sources:** every URL with the date it was accessed.

In connected mode the sizing and the competitor grid also live in the project (Market Size and
Competitor Benchmark steps), so the business-plan and pitch-deck skills can read them from
there.

## Writing

Everything this skill writes for the founder follows `references/writing-style.md`, which is
based on Wikipedia's "Signs of AI writing" guide. This covers memos, reports, emails and the
notes on rows. **No em dashes, no hype words, no unnamed authorities.** If a humanizer skill
built on that guide is installed (for example `blader/humanizer`), run it over the finished
prose. It may change wording only, never a number, name, date or source.

## Guardrails

- **Public information only.** Use websites, published prices, menus, public reviews, filings
  and marketplace listings. Don't bypass logins or paywalls, or scrape against a site's terms.
- **You never contact competitors yourself** (no emails, calls, chats or form submissions), and
  you never send the outreach drafts on the founder's behalf. You prepare the kit (Step 3b);
  the founder decides whether and how to use it, one enquiry at a time.
- No bulk or automated outreach: the kit is for a handful of individual contacts, not a
  campaign.
- Never fill a gap with a guessed competitor fact. An empty cell is better than a wrong check.
- Name companies factually. No disparaging claims you can't source.

## References

- `references/sizing-worked-examples.md`: worked bottom-up sizing for a local business, a B2B
  SaaS and a manufacturer, including the formulas and the cross-check.
- `references/outreach-kit.md`: the founder's outreach kit: approaches, rules, email and call
  templates, and the contact-table format.
- `references/writing-style.md`: the no-AI-tells writing guide.

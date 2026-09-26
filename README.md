# Foundation Skills

Open-source agent skills that do a feasibility consultant's job: size the market, benchmark
competitors, build the financial study, tune the pricing, then write the business plan and
the pitch deck. They run in your own AI agent (Claude, Codex, Gemini CLI, Cursor and others).
They are built by the team behind [Foundation](https://getfndtn.com).

## Why this exists

Ask a general AI assistant whether your business idea works and it will write you something
that sounds like a feasibility study. The problems are underneath:

- **The math is guessed.** Language models are not calculators. NPV, IRR, payback and
  break-even figures in an AI-written plan are often wrong, and nothing on the page tells you
  which ones.
- **The assumptions are invisible.** Where did "£38,000 for the fit-out" come from? A lender
  will ask, and "the AI said so" is not an answer.
- **The parts don't agree.** The team section says five staff, the payroll line pays four, and
  the market chapter uses a different number from the pitch deck.

A professional consultant avoids all three. They put a source behind every input, run the
numbers through a real financial model, and keep one version of the truth that every document
draws from. These skills teach an AI agent to work the same way.

## How it works

The skills split the job the way it should be split:

- **The agent does the analyst's work:** interviewing the founder, researching costs, prices
  and competitors, choosing a sensible structure, tagging where every number came from, and
  writing.
- **A deterministic engine does the math:** [Foundation](https://getfndtn.com) is a
  feasibility-study web app with a tested calculation engine. It computes investment,
  operating costs, revenue ramps, profit, cash flow, NPV, IRR, payback, break-even and SaaS
  metrics from the inputs. When your agent is connected to Foundation, every financial figure
  in the output comes from that engine. The agent never computes one itself.

The skills also work **without a Foundation account**. The agent still does the research and
structures every input with its source, and never invents financial results. It then hands
you a `foundation-project.json` file. Import that file into Foundation (Projects → Import) to
get the computed study.

## The skills

| Skill | What it does |
|---|---|
| [`feasibility-analyst`](feasibility-analyst/SKILL.md) | Turns a description of your business into a complete feasibility study: business type, cost categories, capital and operating costs, staffing, revenue model and financial assumptions, each input with its source. Then it reads the results and gives you a go / no-go memo with the risks and levers. |
| [`market-research`](market-research/SKILL.md) | Sizes the market bottom-up (TAM, SAM, SOM) with a top-down cross-check. Profiles competitors from public sources and fills a competitors × features benchmark. Checks whether your revenue plan needs more of the market than you can realistically win. When a price isn't public, it prepares an outreach kit for you to make the enquiries yourself. |
| [`pricing-optimizer`](pricing-optimizer/SKILL.md) | Finds the price range between your cost floor, competitor prices and the value to the customer. Designs three to five distinct pricing options, tests each through the engine with an explicit assumption about sales volume, and recommends one with a plan to validate it. |
| [`business-plan-writer`](business-plan-writer/SKILL.md) | Writes a lender- and investor-grade business plan as a Word file (.docx). Financial tables, charts and scenarios are generated from the engine's output, so no figure is retyped. |
| [`pitch-deck-writer`](pitch-deck-writer/SKILL.md) | Builds the pitch deck as a PowerPoint file (.pptx): one idea per slide, the takeaway as the headline, engine-computed financial slides, and a visual check of every slide before delivery. |

All five follow the same rules, written down in [CONVENTIONS.md](CONVENTIONS.md):

- Every input carries a source tag: founder, quote, benchmark or estimate.
- The agent asks you only what it can't research, in one round.
- Writing follows a guide based on Wikipedia's
  [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing): plain
  sentences, no hype, no em dashes.
- For brand templates or heavier design, the Word and PowerPoint files can go through your
  environment's own document tools as a second step, with a script that checks no number
  changed on the way.

## Install

**Any agent that supports skills** (Claude Code, Codex, Gemini CLI, Cursor and others):

```
npx skills add mamarexa/foundation-skills
```

Or copy the skill folders you want by hand:

| Agent | Where skills go |
|---|---|
| Claude Code | `~/.claude/skills/` (all projects) or `.claude/skills/` (one project) |
| Claude.ai / Claude Desktop | Zip a skill folder, then Settings → Capabilities → Skills → Upload |
| Codex | `~/.codex/skills/` |
| Gemini CLI | `~/.gemini/skills/` or `.gemini/skills/` |
| Cursor | `~/.cursor/skills/` or `.cursor/skills/` |

The Word and PowerPoint skills need Python with `python-docx`, `python-pptx` and
`matplotlib`. These come preinstalled in Claude's code sandbox. Anywhere else, run
`pip install python-docx python-pptx matplotlib`.

### Connect Foundation (optional, recommended)

1. Create a free account at [getfndtn.com](https://getfndtn.com).
2. Add `https://getfndtn.com/api/mcp` to your agent as a remote MCP server (in Claude:
   Settings → Connectors → Add custom connector). You'll sign in with your Foundation account.
3. Ask your agent for a feasibility study. It will find the Foundation tools and work on your
   real project, and the numbers will match what you see in the app.

Step-by-step setup for Claude, ChatGPT, Codex, Cursor, Gemini CLI, Antigravity and VS Code is in the
[Foundation docs](https://getfndtn.com/docs/connect-your-ai).

## Try it

> "I want to open a specialty coffee shop near Leeds station, about 30 seats, opening next
> spring. Is it viable, and how much do I need to raise?"

> "Size the market for scheduling software for UK dental practices, and benchmark the main
> competitors."

> "Turn my Foundation project into a business plan for a bank loan, then a 12-slide deck."

## Contributing

This repository is meant to get better with use. The most valuable contributions are:

- **Benchmarks with sources:** cost ratios, startup-cost ranges, wages, employer payroll
  costs, rents and tax rates for your industry or your country. Local numbers help founders
  outside the US and UK most.
- **Corrections from practitioners:** if you do this work for a living and a step is wrong
  or missing, tell us how it's done in practice.
- **Test cases:** a realistic business description and what a good study of it should
  contain.

Good contributions also flow back into the Foundation app, for example as better default
categories and benchmark ranges. See [CONTRIBUTING.md](CONTRIBUTING.md) for the rules. The
short version: every number needs a source you'd be comfortable showing a lender.

This repository and the `skills/` folder in the Foundation app are kept in sync automatically
in both directions, so a merged pull request here shows up there (as a reviewed PR, not a
silent merge) without anyone copying files by hand.

## Tests

```
pip install python-docx python-pptx matplotlib
python tests/test_scripts.py
```

The fixture project in `tests/fixtures/` is a sample café. Its facts file is real output from
Foundation's engine.

## License

[MIT](LICENSE). By contributing, you agree your contribution is licensed the same way,
including its use in Foundation.

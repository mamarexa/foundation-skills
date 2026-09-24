# Foundation Skills

Agent skills that do professional-grade feasibility-study work: the kind of analysis a
feasibility consultant does for a client, run by your own AI agent.

> **Staging note.** This folder is being developed inside the Foundation app repo so the skills
> and the MCP tools they call can change together. It is laid out as a standalone repo root and
> will move to its own public repository once the pattern is settled. Nothing in here imports
> from the app.

## Skills

| Skill | What it does | Status |
|---|---|---|
| [`feasibility-analyst`](feasibility-analyst/SKILL.md) | Turns a business description into a complete feasibility study: business type, cost categories, capex, opex, revenue model, assumptions, then reads the results and advises. | Ready for testing |
| market-research (TAM/SAM/SOM + competitor benchmark) | Market sizing and a competitor feature benchmark. | Planned |
| [`pricing-optimizer`](pricing-optimizer/SKILL.md) | Diagnoses pricing, builds a cost-floor → reference → value-ceiling corridor, designs 3–5 options and tests each through the engine with an explicit volume assumption. | Ready for testing |
| business-plan-writer (.docx) | Writes the business plan as a Word file, grounded in the study's numbers. | Planned |
| pitch-deck-writer (.pptx) | Builds the investor deck as a PowerPoint file. | Planned |

## Two modes: connected and standalone

Every skill works in both modes. See [CONVENTIONS.md](CONVENTIONS.md) for the exact rules.

- **Connected** (you have a [Foundation](https://getfndtn.com) account and its MCP server is
  connected to your agent). The skill reads and writes your real project, and every financial
  number comes from Foundation's deterministic calculation engine.
- **Standalone** (no account). The skill still does the analyst's work: it picks categories,
  researches costs and prices, and documents every assumption. It then writes a
  `foundation-project.json` file that you can import into Foundation to get the computed
  results. It never makes up NPV, IRR, payback or break-even figures.

## Installing

**Claude Code:** copy a skill folder into `~/.claude/skills/` (every project) or into
`.claude/skills/` in one project.

**Claude.ai / Claude Desktop:** zip the skill folder and upload it under
Settings → Capabilities → Skills.

**Connecting Foundation (optional):** add the MCP server at `https://getfndtn.com/api/mcp` as a
remote MCP connector. You sign in with your normal Foundation account.

## Contributing

The most valuable contributions are **reference data**: cost benchmarks, typical ratios and
startup-cost ranges for an industry or a country, each with a source. See
[CONTRIBUTING.md](CONTRIBUTING.md).

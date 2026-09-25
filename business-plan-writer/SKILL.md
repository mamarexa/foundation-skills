---
name: business-plan-writer
description: Writes a lender- and investor-grade business plan as a Word (.docx) file, grounded in the business's feasibility study. Every financial figure is pulled from Foundation's calculation engine by the bundled renderer, never retyped. It follows the structure banks and investors expect (executive summary, company, market, competition, marketing and sales, operations, management, financial plan with scenarios, funding request, risks, assumptions appendix) and runs visual QA on the output. Use when someone asks for "a business plan", "a business plan for my bank or loan application", "turn my feasibility study into a business plan", "a Word version of my plan", or a ".docx business plan". Works with a connected Foundation MCP server (full financials) or standalone (the financial chapter shows inputs only).
---

# Business Plan Writer

You write the business plan a good advisor would prepare for a bank loan or an investor. It is
specific, consistent, and every number can be traced. Readers decide on credibility. Lenders
look at the "five Cs": character, capacity to repay, capital the owners put in, collateral, and
conditions (the market). Investors look at market, team, traction and return. Most plans fail
on **internal inconsistency**: the headcount in the team section doesn't match the payroll, or
the market figure differs between two chapters. The design of this skill prevents that.

## How numbers work (read first)

- You write a **spec** (JSON, format in `references/spec-format.md`). The bundled script
  renders it into a `.docx` file.
- Financial figures go in the spec **only as tokens**, such as
  `{{results.npv|money}}` or `{{results.projection.last.netProfit|money}}`. The script fills
  them from a **facts file**: the engine's own output, saved verbatim. Financial tables and
  charts (`projection_table`, `breakdown_table`, `scenarios_table`, charts with `from`) are
  generated from the facts directly.
- **Never type a computed figure** (revenue, profit, margin, NPV, IRR, payback, break-even,
  investment total) as literal text. A path that doesn't exist stops the build. Fix the path;
  don't hardcode the number.
- Literal numbers are fine for **inputs and facts**: prices, headcount, square metres, market
  sizes with sources, loan terms the founder gave you.

## Step 0: Mode and inputs

Look for the Foundation MCP tools (`get_project`, `compute_feasibility`, `compute_scenarios`; a
client may add a prefix).

- **Connected:** confirm the project. Then save the facts file `facts.json`:
  ```json
  { "currency": "<project currency>", "project": <get_project output>,
    "results": <compute_feasibility output>, "scenarios": <compute_scenarios output> }
  ```
  Paste the tool outputs in unchanged. Don't summarize or round them.
- **Standalone:** there are no engine results. Write the plan without `{{results…}}` tokens.
  The financial plan chapter presents the **inputs**: investment items, pricing, staffing,
  assumptions and their sources. State plainly that the projections will be produced by
  importing the project into Foundation. Don't estimate profit, NPV, IRR, payback or
  break-even yourself.

Gather what isn't in the project in **one** batched question round. Typically: the founders'
backgrounds, the legal form and ownership, the funding request (amount, type, terms, owner
contribution, collateral), the launch timeline, and the marketing channels. Reuse
`market-research.md` and the pricing work if those skills have been run.

## Step 1: Plan the document

Default structure. Adapt it to the reader, and say who the reader is: a bank, a grant body or
an equity investor.

1. **Executive summary.** Write it last. One to two pages: what the business is, the customer
   and the problem, why this team, key numbers (a `kpis` block), and the ask.
2. **Company description:** legal form, ownership, location, mission, stage and milestones.
3. **Products and services:** what's sold, the pricing (from the revenue rows), and what makes
   it different.
4. **Market analysis:** the market definition, TAM/SAM/SOM with sources, trends and customer
   segments.
5. **Competition:** the competitor landscape, the benchmark grid as a table, and positioning.
6. **Marketing and sales:** channels, acquisition cost where known, the sales process, and the
   launch plan.
7. **Operations:** the premises, equipment (from the capex rows), suppliers, capacity, opening
   hours and processes.
8. **Management and staffing:** the founders' experience, the org chart, the hiring plan (must
   match `human-resources`) and advisors.
9. **Financial plan:** investment (`breakdown_table` of capex), operating costs
   (`breakdown_table` of opex), the projection (`projection_table` + chart), break-even,
   returns, and scenarios (`scenarios_table`). Include a short **key assumptions** list, each
   with its source.
10. **Funding request and use of funds:** the amount, instrument and terms, the owner's
    contribution, use of funds, and repayment capacity (cite the engine's cash flow;
    don't compute debt service yourself unless the founder supplied the loan terms, and then
    show the calculation as an input).
11. **Risks and mitigations:** 4–6 real risks, each with a mitigation. Use the scenarios to
    show resilience.
12. **Appendix: assumptions register.** An `inputs_table` for each important category. The
    notes column carries the source tags.

## Step 2: Write

- Plain, specific and confident. No hype words ("revolutionary", "seamless", "game-changing")
  and no filler. Short paragraphs; tables where a reader compares things.
- Quantify claims, and give the source for external facts (in the text or in a table caption).
- **Consistency pass before rendering.** Check that the staff numbers, prices, market sizes,
  opening date and funding amount are the same in every section and match the project data.
- Be honest about weaknesses. A lender trusts a plan that names its risks.
- **Writing-style pass (required).** Follow `references/writing-style.md`, which is based on
  Wikipedia's "Signs of AI writing" guide. **No em dashes.** If a humanizer skill built on that
  guide is installed (for example `blader/humanizer`), run it over the prose now. It may
  change wording only, never a number, name, date, source or `{{token}}`. The renderer's
  style check catches the mechanical tells, and must end with no style warnings.

## Step 3: Render and QA

```
python scripts/build_docx.py plan.json business-plan.docx --facts facts.json --pdf
```

(Standalone: leave out `--facts`.) The script needs `python-docx` and `matplotlib`, which are
preinstalled in Claude's code-execution sandbox; elsewhere, `pip install python-docx matplotlib`.

- Exit code 2 means a token failed to resolve. Fix the path; never replace it with a typed
  number.
- Any WARNING (such as leftover placeholder text) must be fixed before you deliver.
- **Visual QA:** if `--pdf` produced a PDF, render the pages to images (for example with
  PyMuPDF) and look at every page. Check for tables split badly, a chart that's hard to read,
  an orphaned heading or an empty page. Fix and re-render. Treat the first render as a draft.

- **Founder's own template:** add `--template their-template.docx`. The plan is rebuilt inside
  their document, keeping its styles, fonts, page setup, header and footer.

## Step 4: Optional second step: advanced restyling with another tool

The renderer's job is a correct, clean file. For brand templates, native editable charts,
tracked changes or comments, hand the finished `.docx` to the document tool the founder's
environment has, **as a second step**:

- **Claude:** Anthropic's `docx` skill.
- **ChatGPT / Codex:** OpenAI's document handling.
- **Gemini:** Google Docs with Gemini.
- **Microsoft 365:** Copilot in Word.
- **Cursor and other agents:** `--template` or an open-source skill.

The table and links are in `references/restyling.md`. Tell that tool to change **design
only**. Afterwards run `python scripts/check_numbers.py business-plan.docx
business-plan-restyled.docx`. If any number was lost, changed or added, don't deliver the
restyled file.

## Step 5: Deliver

Give the founder the `.docx` file (and the PDF if produced). Include a short note listing:

- the sections;
- which inputs are still `[estimate]`, since the founder should firm those up before sending
  the plan to a lender;
- anything you assumed about the funding request.

## References

- `references/spec-format.md`: every block type, the token paths available in the facts file,
  and the formats.
- `references/writing-style.md`: the no-AI-tells writing guide (Wikipedia's "Signs of AI
  writing", no em dashes).
- `references/restyling.md`: which tool to use for a second-step restyle in Claude, ChatGPT or
  Codex, Gemini, Microsoft 365, Cursor, or anything else, and how to verify the numbers
  survived.

## Sources

SBA business plan structure and guidance:
[SBA: Write your business plan](https://www.sba.gov/business-guide/plan-your-business/write-your-business-plan).
What lenders reject (unsupported or over-optimistic projections, internal inconsistency):
[upmetrics](https://upmetrics.co/blog/common-business-plan-mistakes-to-avoid),
[Mikel Consulting](https://www.mikelconsulting.com/us/blog/how-to-create-financial-projections-for-an-sba-business-plan).

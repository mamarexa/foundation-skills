# Conventions shared by every Foundation skill

Every skill in this repo follows these rules. They are written once here so all skills behave the
same way. Each SKILL.md repeats the parts it depends on, because an agent may load one skill
without this file.

## 1. Detect the mode first

Before doing anything else, check whether the Foundation MCP tools are available. Look for tools
named `list_projects`, `get_project` and `compute_feasibility`. Some clients add a prefix, such as
`mcp__foundation__list_projects`.

- **Tools available: connected mode.** Call `list_projects`. If the founder names an existing
  project, work on that one. Otherwise ask whether to create a new project or update one of the
  existing projects. Never overwrite a project without confirming which one.
- **Tools not available: standalone mode.** Say so in one sentence and mention that connecting
  Foundation gives computed financials. Then continue; don't block on it.

## 2. The agent never does the financial math

Foundation's calculation engine is deterministic and tested. The agent's job is to produce good
**inputs** and to **interpret** the outputs.

- Connected: every total, margin, NPV, IRR, payback period, break-even point or SaaS metric you
  state must come from `compute_feasibility` or `compute_scenarios`, quoted as returned.
- Standalone: do not state any of those figures. You may do input-level arithmetic, and show
  it: "3 baristas × 1,800/month", or "a 30% food cost on 40,000/month of sales is 12,000".
  Label every such figure as an input estimate, not a result.
- Never "sanity-check" the engine by recomputing its outputs yourself. If a result looks wrong,
  check the inputs: a missing row, a wrong cost split, a unit mistake, or the wrong currency.

## 3. Every number has a source

Each assumption you enter is one of:

| Tag | Meaning |
|---|---|
| `[founder]` | The founder told you. |
| `[quote]` | A real quote, price list or listing. Include the URL or name. |
| `[benchmark]` | An industry ratio from `references/`, or from research you cite. |
| `[estimate]` | Your reasoned estimate. Say what it's based on. |

Put the tag and a short reason in the row's `notes` field so the founder can audit it later in
the app. For example: `[benchmark] 30% of food sales, full-service median 28–35%`.

## 4. Ask what only the founder knows, and look up the rest

Ask the founder only for facts you can't find or reasonably assume: location, launch date,
funding available, their own role and salary, signed quotes, and deliberate strategic choices
such as premium vs. budget positioning. Ask them in one batched round, not one at a time.
Research or estimate everything else, and tag it.

## 5. Writes in connected mode

- `update_line_items` replaces **all** rows of a category. Read the category first with
  `get_project`, and send the complete list of rows.
- Before filling a category, call `describe_categories` to get its exact column keys. Unknown
  keys are rejected.
- Row ids: keep existing ones. Invent new ones for new rows, like `row-rent-1`.
- Amounts are in the project's currency. A `"Rial"` unit in a column definition is a legacy
  label that means "the project's currency".

## 6. Standalone handoff file

In standalone mode, finish by writing `foundation-project.json`. Its format is in
`feasibility-analyst/references/handoff-format.md`. It carries the same fields the connected tools
write. Importing it in Foundation (Projects → Import) creates a new project with exactly those
inputs, and the engine computes the results.

## 7. Tone of the output

Write like a feasibility consultant writing for a client who is also a lender's audience: plain,
specific and conservative. No hype words. Flag weak points yourself before an investor does.

Every skill that writes prose ships `references/writing-style.md`, which is based on
Wikipedia's "Signs of AI writing" guide. **No em dashes.** If a public humanizer skill built on
that guide is installed (for example `blader/humanizer`), run it as the final pass, for
wording only: it must never change numbers, names, dates, sources or `{{tokens}}`. All copies
of `writing-style.md` are identical, and a test checks it.

## 8. Second-step tools for files

The business-plan and pitch-deck renderers produce correct files. Advanced restyling
(templates, native charts, tracked changes) is a second step done with whatever the
environment has: Anthropic's `docx`/`pptx` skills in Claude, OpenAI's in ChatGPT/Codex, Google
Docs/Slides with Gemini, Copilot in Microsoft 365, or an open-source skill elsewhere (see
`references/restyling.md`). The second step changes design only. `scripts/check_numbers.py`
must pass between the original and the restyled file before the restyled file is delivered.

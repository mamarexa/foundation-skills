# Business-plan spec format (`build_docx.py`)

```json
{
  "title": "Corner Café, Leeds",
  "subtitle": "Business plan and feasibility study",
  "kicker": "Business plan",
  "short_title": "Corner Café",
  "prepared_by": "Prepared by the founders",
  "date": "September 2026",
  "confidentiality": "Confidential. Prepared for prospective lenders.",
  "paper": "A4",
  "contents": true,
  "theme": { "heading_font": "Georgia", "body_font": "Calibri", "accent": "1F6C9F" },
  "sections": [
    { "heading": "Executive summary", "blocks": [ ... ] }
  ]
}
```

Each section starts on a new page and is numbered automatically. `paper` is `"A4"` or
`"Letter"`.

## Blocks

| type | fields | notes |
|---|---|---|
| `paragraph` | `text` | `**bold**` and `*italic*` inline; tokens allowed |
| `heading` | `text`, `level` (2 or 3) | sub-heading inside a section |
| `bullets` | `items`, `numbered` | |
| `callout` | `title`, `text` | shaded box: use for "The ask" or a key conclusion |
| `kpis` | `items: [{label, value}]` | 2–4 headline figures; values are usually tokens |
| `table` | `columns`, `rows`, `caption`, `total_row` | your own table (competitors, milestones, market sizes). Numeric columns right-align automatically |
| `breakdown_table` | `of`: `"capex"` or `"opex"` | per-category amounts **from the engine** |
| `projection_table` | `caption` | year-by-year revenue, costs, net profit, cumulative cash flow **from the engine** |
| `scenarios_table` | `caption` | Worst / Base / Best **from the engine** (needs `scenarios` in the facts) |
| `inputs_table` | `category` | the founder's inputs for one category, with their notes and source tags (appendix) |
| `chart` | `title`, `kind` (`bar`/`line`), `unit` (`money`/`number`), then either `from` + `series: [{field, name, kind?}]` (engine series, e.g. `"from": "results.projection"`) or `labels` + `series: [{name, values}]` | rendered with matplotlib and captioned "Figure n." |
| `pagebreak` | | |

## Tokens

`{{path|format}}` anywhere in text. The path is a dot path into the facts file. Lists take
indexes and `last`.

| Common paths | Meaning |
|---|---|
| `results.totalInvestment` | fixed investment (capex incl. contingency) + working capital |
| `results.capex.total`, `results.workingCapital` | the two parts of it |
| `results.peakFundingRequirement`, `results.peakFundingYear` | the deepest point of cumulative cash flow, i.e. the real amount to raise |
| `results.revenue`, `results.netProfit`, `results.profitMarginPct` | Year 1 |
| `results.opex.total`, `results.opex.fixedTotal`, `results.opex.variableTotal` | annual operating cost |
| `results.breakEvenRevenue`, `results.breakEvenUnits` | break-even |
| `results.simplePaybackYears` | payback (null if outside the projection) |
| `results.npv`, `results.irrPct` | returns (IRR null when cash flow never turns positive) |
| `results.projection.last.revenue`, `results.projection.0.netProfit` | a specific year |
| `results.saasMetrics.ltvToCac`, `.cacPaybackMonths`, `.runwayMonths` | subscription businesses |
| `scenarios.worst.npv`, `scenarios.best.irrPct` | scenarios |
| `project.assumptions.discountRatePct`, `project.assumptions.taxRatePct` | assumptions used |
| `project.marketSizing.tam.value` (and `.basis`, `.source`; same for `sam`, `som`) | the Market Size step's figures, so the plan matches the app |

**Formats:** `money` (£1,234,567), `money_compact` (£1.2M, £450k), `pct` (28.9%), `years`
(2.8 years), `months`, `int`, `number`, `ratio` (3.2×), `raw`. A null value renders as "n/a",
or as "not within the projection" for `years`.

A full working example is in `tests/fixtures/coffee-plan-spec.json` at the repo root.

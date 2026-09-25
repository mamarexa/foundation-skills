# Pitch-deck spec format (`build_pptx.py`)

```json
{
  "company": "Corner Café",
  "theme": { "accent": "1F6C9F", "heading_font": "Georgia", "body_font": "Calibri" },
  "slides": [ { "type": "title", ... }, ... ]
}
```

The slides are 16:9. Every slide type (except `title` and `closing`) takes an optional
`kicker` (the small uppercase label above the headline), a `headline` (the takeaway sentence)
and `notes` (speaker notes). Text fields accept `**bold**` and `{{path|format}}` tokens. The
paths and formats are the same as in the business-plan-writer's `references/spec-format.md`.

| type | fields | use for |
|---|---|---|
| `title` | `title`, `tagline`, `footnote` | slide 1 (dark) |
| `statement` | `headline`, `subtext`, `points` (≤4), `dark` | problem, solution, why now |
| `bullets` | `headline`, `items` (≤5) | numbered points, e.g. go-to-market steps |
| `kpis` | `headline`, `items: [{value, label}]` (≤4), `subtext` | financial headline figures, traction, unit economics |
| `chart` | `headline`, `chart`, `side_points` (≤3) | the projection. `chart` = `{ "from": "results.projection", "series": [{"field": "revenue", "name": "Revenue"}, {"field": "netProfit", "name": "Net profit", "kind": "line"}] }`, or your own `labels` + `series: [{name, values}]` |
| `market` | `headline`, `levels: [{label, value, detail}]` (TAM, SAM, SOM), `source` | market sizing. When the project has Market Size filled in, use tokens so the slide matches the app: `"value": "{{project.marketSizing.sam.value\|money_compact}}"`, `"detail": "{{project.marketSizing.sam.basis\|raw}}"` |
| `benchmark` | `headline`, `highlight_row`, `max_features` (7), `max_rows` (7) | the project's Competitor Benchmark grid, read from `project.competitorBenchmark` in the facts file |
| `table` | `headline`, `columns`, `rows` | any small table you write yourself |
| `scenarios` | `headline` | Worst / Base / Best from `scenarios` in the facts file |
| `team` | `headline`, `people: [{name, role, bio}]` (≤4) | the team |
| `ask` | `headline`, `amount`, `terms`, `use_of_funds: [{label, pct}]`, `milestones` | the raise |
| `closing` | `headline`, `contact` | last slide (dark) |

A full working example is in `tests/fixtures/coffee-deck-spec.json` at the repo root.

# Pricing playbooks by business type

The ranges below are common starting points. Always prefer this business's real data and live
competitor prices.

## Restaurants, cafés, food service

- **Food-cost pricing as the floor:** menu price ≈ plate cost ÷ target food-cost %. The target
  is usually 28–35%, and drinks run far lower. Use recipe costs from the project's
  ingredients and recipes.
- **Menu engineering** (Kasavana & Smith): classify every item by popularity and by
  contribution margin per serving (price − plate cost).
  - Stars (popular, high margin): protect them and feature them.
  - Plowhorses (popular, low margin): make small price rises, trim portions or change sides.
  - Puzzles (unpopular, high margin): reposition, rename or have staff recommend them.
  - Dogs (unpopular, low margin): remove them.
- **Levers:** check-average builders (add-ons, pairings, set menus), small rounded price rises
  on popular items rather than big ones, and delivery-platform prices that cover the
  platform's commission.
- **In Foundation:** each menu item or item group is a `unit` revenue row. Changing a price
  changes `unitPrice`. Changing the mix changes `monthlyVolume` across rows.

## Retail

- **Markup vs. margin:** a keystone markup (2× cost) gives a 50% gross margin. The right margin
  depends heavily on the category (see the feasibility-analyst benchmarks).
- **Price lines** (good/better/best within a category), bundles, and private label for margin.
- Watch for items shoppers compare prices on, such as known brands. Take margin on items they
  don't compare.
- The payment-processing fee scales with price, so update `payment-processing` together with
  price.

## SaaS and subscriptions

- **Pick a value metric** that grows with the value the customer gets: seats, active users,
  locations, usage volume, or revenue handled. Avoid metrics that punish adoption.
- **Good-better-best tiers:** the middle tier is the one to sell, and the top tier makes the
  middle look reasonable. A common ratio is entry ≈ 40% of middle and top ≈ 2–2.5× middle.
  Gate tiers on things customers value, not arbitrary limits.
- **Annual prepay:** 15–20% off (about 2 months free). It improves cash flow and retention.
- **Free-to-paid conversion:** freemium typically converts 2–5%; free trials 15–25%. A
  free plan needs a large top of funnel to pay off.
- **In Foundation:** subscription rows (`pricingMode: "subscription"`). A price change moves
  `monthlyRecurringPrice`, and a tier is one row. Check `saasMetrics`: LTV:CAC ≥ 3, CAC
  payback under 12 months for SMB customers. Annual churn is a project assumption; test it with
  `assumptionOverrides.customerChurnPct`.

## Professional services and agencies

- **Move from hourly to value-based or fixed-fee** where the outcome is clear, and use
  retainers for recurring work.
- **Hourly-rate floor:** fully loaded cost per billable hour ÷ (1 − target margin). Loaded cost
  includes salary, burden and overhead share, divided by *billable* hours (utilization
  70–80%, not 100%).
- Tiered engagement packages and productized services make pricing easy to compare.
- **In Foundation:** `unit` rows per service line (price × monthly engagements), or
  `subscription` rows for retainers.

## B2B, manufacturing, distribution

- Cost-plus pricing is common but leaves money on the table where the product outperforms the
  alternatives. Use the economic value to the customer for differentiated products.
- Volume tiers and contract terms (minimum orders, indexation clauses for raw-material price
  swings).
- Audit the pocket price waterfall. Rebates, freight and payment terms quietly erode price.

## Marketplaces and commission businesses

- **Take rate** is the commission as a percentage of transaction value. It has to stay below
  the value the platform gives each side, and below the cost of the two sides dealing
  directly. Check the rates competitors publish for the category.
- Consider charging each side differently, and fixed listing or subscription fees on top of
  the commission.
- **In Foundation:** `commission` rows (`basisAmount` = monthly value flowing through,
  `basisPct` = take rate).

## Sources

- Menu engineering: [Toast](https://pos.toasttab.com/blog/on-the-line/menu-engineering-matrix), [Loaded](https://www.loadedhub.com/resources/menu-engineering-matrix-restaurant)
- Good-better-best and anchoring: [Priceagent](https://www.priceagent.com/blog/tiered-pricing-a-strategic-approach-to-value-based-pricing), [PayPro Global](https://payproglobal.com/how-to/use-price-anchoring/)
- Annual discount and conversion rates: [Paddle](https://www.paddle.com/resources/annual-plans), [ChartMogul](https://chartmogul.com/reports/saas-conversion-report/), [First Page Sage](https://firstpagesage.com/seo-blog/saas-freemium-conversion-rates/)
- Utilization: [SPI Research](https://spiresearch.com/2025/02/12/the-18th-annual-professional-services-maturity-benchmark-report-is-out-now/)

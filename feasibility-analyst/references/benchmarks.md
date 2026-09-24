# Cross-check benchmarks

Use these ranges to **sanity-check inputs**, not as a substitute for real quotes. When an input
falls outside its band, either fix it or say in the row's `notes` why this business differs.
Cite the benchmark with a `[benchmark]` tag.

All figures are typical ranges for small and early-stage businesses, mostly from US and European
sources, as of 2025–2026. Adjust for the local market: wages, rent and tax differ enormously by
country. Contributions that add country-specific or industry-specific ranges, with sources, are
the most useful PRs to this repo.

## Payroll: employer burden (`employerBurdenPct`)

The cost on top of gross salary: employer payroll taxes, statutory insurance and typical
benefits.

| Market | Typical burden | Notes |
|---|---|---|
| United States | 20–30% | FICA 7.65% + unemployment taxes + benefits (health insurance dominates). |
| United Kingdom | ~15–20% | Employer NIC 15% above £5,000/yr (from April 2025) + pension auto-enrolment 3%. |
| Germany | ~21–25% | Social insurance contributions + accident insurance + levies. |
| Other markets | Look it up | Search "<country> employer social security contribution rate". Never leave it at 0. |

## Restaurants and food service

| Metric | Typical range |
|---|---|
| Food & beverage cost (COGS) | 28–35% of sales. Higher for premium ingredients, lower for pizza or beverage-heavy menus. |
| Labor (incl. burden) | 25–35% of sales. The full-service median is about 35%. |
| Prime cost (COGS + labor) | 55–65% of sales. Quick-service ~55%, full-service 60–65%. |
| Occupancy (rent + CAM + property tax) | 6–10% of sales. Above ~12% is a warning sign. |
| Net margin | 3–6% typical, ~10% strong. |

## Coffee shops

| Metric | Typical range |
|---|---|
| COGS | 25–35% of sales. Toward 35% with a real food menu. |
| Labor | 25–28% high-volume counter service; 28–35% independent; 32–38% with a food menu. |
| Startup cost (US) | ~$80k–$300k for a small independent shop; kiosks from ~$25k; prime urban full cafés $500k+. |
| Net margin | 2.5–7% typical, 8–12% well run. |

## Retail

| Metric | Typical range |
|---|---|
| Gross margin | Discount 20–25%, grocery 25–30%, general merchandise 30–40%, specialty 40–55%, luxury 55–70%. |
| Occupancy | 5–10% of sales. |
| Inventory turns | 4–8 per year typical; 15–20 for perishables. Initial inventory ≈ annual COGS ÷ turns. |
| Inventory carrying cost | 20–30% of inventory value per year. |
| Net margin | 2–5%. |

## SaaS / software

| Metric | Typical range |
|---|---|
| Gross margin | 75–85% healthy (2025 median ~76% total, ~80% software). AI-heavy products can be far lower because of inference cost, so model the compute explicitly in `cloud-hosting`. |
| Hosting / infrastructure | Usually 5–15% of revenue at scale. Early on, a fixed minimum dominates. |
| Monthly logo churn, SMB customers | 3–5% good (≈30–45% annual). Best-in-class SMB is 15–20% annual. |
| Monthly logo churn, mid-market | 1.5–3%. |
| Monthly logo churn, enterprise | 1–2% or less. |
| LTV:CAC | ≥ 3 healthy. |
| CAC payback | < 12 months good for SMB; < 18–24 months acceptable for enterprise. |

Foundation's `customerChurnPct` is **annual**. Convert monthly churn with
1 − (1 − monthly)^12. For example, 3% a month is about 31% a year.

## Professional services / consulting

| Metric | Typical range |
|---|---|
| Billable utilization | 70–80% target. The 2025 industry average fell to ~66%. Model revenue as billable staff × hours × utilization × rate, not 100% of hours. |
| Project margin | > 35%. |

## Revenue ramp (Year 1)

New ventures rarely reach capacity in Year 1. Unless the founder has signed demand (contracts,
pre-orders, an anchor customer), assume a Year-1 average of:

| Business | Year-1 average vs. steady-state volume |
|---|---|
| Restaurant / café, new location | 50–70% |
| Retail store | 50–70% |
| Manufacturing plant | 40–60% of rated capacity (commissioning plus market entry) |
| Service firm, founder-led | Depends on pipeline. Start from named prospects. |
| SaaS | Model customers bottom-up from the acquisition channel (traffic × conversion, or reps × quota). Never "1% of the market". |

**Growth from Year 2** (`revenueGrowthPct`): mature local businesses grow about 2–5% a year
(roughly inflation plus a little). Growing startups can justify more, but only with a mechanism
behind it, such as more capacity, more locations or more sales staff. Lenders treat unexplained
double-digit growth as a red flag.

## Discount rate (`discountRatePct`)

| Situation | Typical rate |
|---|---|
| Established small business, lender financed | 10–15% (≈ cost of debt + risk premium) |
| New small business, owner equity | 15–25% |
| Early-stage startup (the return venture investors require) | 30–50%+ |

State the rate you chose and why.

## Sources

- Restaurant prime cost and food cost: [Toast](https://pos.toasttab.com/blog/on-the-line/restaurant-payroll-percentage), [Taxfyle](https://www.taxfyle.com/blog/prime-cost-restaurant), [VantaInsights](https://vantainsights.com/insights/restaurant-food-cost-percentage)
- Coffee shops: [Taxfyle](https://www.taxfyle.com/blog/cost-of-goods-sold-and-labor-for-coffee-shops), [VantaInsights](https://vantainsights.com/insights/coffee-shop-startup-costs), [VantaInsights](https://vantainsights.com/insights/coffee-shop-profit-margins)
- Retail: [RetailDogma](https://www.retaildogma.com/retail-benchmarks/), [DealStream](https://dealstream.com/industry-guides/retail-stores/rules-of-thumb)
- SaaS gross margin: [CloudZero](https://www.cloudzero.com/blog/saas-gross-margin-benchmarks/), [Aleph](https://www.getaleph.com/answers/saas-gross-margin-2026)
- SaaS churn: [Vena](https://www.venasolutions.com/blog/saas-churn-rate), [Optifai](https://optif.ai/learn/questions/b2b-saas-churn-rate-benchmark/)
- Employer burden: [Patriot Software](https://www.patriotsoftware.com/blog/payroll/how-much-employers-pay-payroll-taxes/), [teamed](https://www.teamed.global/compare/hire-uk-vs-germany), [Boundless](https://boundlesshq.com/blog/payroll-tax-germany-2026/)
- Consulting utilization: [SPI Research](https://spiresearch.com/2025/02/12/the-18th-annual-professional-services-maturity-benchmark-report-is-out-now/), [Deltek](https://www.deltek.com/resources/articles/professional-services-benchmarks/)
- Lender red flags (optimistic ramps, unexplained assumptions, internal inconsistency): [upmetrics](https://upmetrics.co/blog/common-business-plan-mistakes-to-avoid), [Mikel Consulting](https://www.mikelconsulting.com/us/blog/how-to-create-financial-projections-for-an-sba-business-plan)

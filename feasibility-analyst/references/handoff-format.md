# `foundation-project.json` (standalone handoff format)

In standalone mode, write the study to this file. The founder imports it in Foundation under
**Projects → Import**. That creates a new project and opens its dashboard with every result
computed by the engine.

The import is **strict about anything that would silently not count**, and lenient about
anything left out:

- Unknown category ids, unknown column keys and non-numeric values in number columns are
  rejected, with the reason. Nothing is half-imported.
- Anything omitted keeps the default a new project of that `businessType` would get.
- Row `id`s are optional; they're generated when missing.

## Shape

```jsonc
{
  "format": "foundation-project",       // required, exactly this
  "version": 1,                          // required, exactly 1
  "name": "Corner Café, Leeds",          // required: the project name

  "businessType": "coffee-shop",         // production | tech-startup | restaurant | coffee-shop | retail | service | custom
  "currency": "GBP",                     // USD EUR GBP IRR AED SAR TRY INR CAD AUD JPY CNY

  // The active category sets AFTER your adjustments. Don't list the always-on ones
  // (pre-operational, human-resources, revenue).
  "activeCapexCategories": ["leasehold-improvements", "kitchen-equipment", "furniture-fixtures", "pos-setup", "signage-branding", "initial-inventory"],
  "activeOpexCategories": ["raw-materials", "rent-lease", "maintenance", "payment-processing", "marketing", "admin"],

  "overview": {                          // any subset
    "productName": "Specialty coffee & bakery counter",
    "proposedCapacity": "~350 transactions/day at maturity",
    "applications": "Commuters and office workers, weekday mornings",
    "employment": 5,                     // must equal total headcount in human-resources
    "buildingOtherSqm": 85
  },

  // One array per category. Column keys exactly as in category-catalog.md.
  // Opex amounts are MONTHLY Year-1 run-rates. Put a source tag and a reason in "notes".
  "lineItems": {
    "rent-lease": [
      { "description": "Shop lease, 85 m²", "notes": "[quote] Rightmove listing #123, £2,300/mo + service charge", "monthlyCost": 2550 }
    ],
    "human-resources": [
      { "role": "Barista", "notes": "[benchmark] local rate £12.60/h × 170 h", "headcount": 3, "monthlySalary": 2140, "employerBurdenPct": 16 }
    ],
    "revenue": [
      {
        "product": "Coffee & drinks", "notes": "[estimate] 250/day avg Year 1 (≈70% of 350) × 30 days",
        "pricingMode": "unit", "unitPrice": 3.6, "monthlyVolume": 7500, "startMonth": 3
      }
    ]
  },

  "costSplit": [{ "id": "raw-materials", "fixedPct": 0 }],   // optional: only what you change
  "contingencyPct": 10,                                        // capex contingency, %

  "assumptions": {                       // any subset
    "taxRatePct": 25,
    "discountRatePct": 18,
    "revenueGrowthPct": 4,
    "workingCapitalMonths": 3,
    "projectionYears": 5
  },

  // Optional: restaurant/coffee-shop recipe model (units: see Foundation's unit list, g, kg, ml, l, piece, dozen)
  "ingredients": [{ "id": "ing-milk", "name": "Whole milk", "unit": "l", "pricePerUnit": 1.1 }],
  "recipes": [{ "id": "rec-latte", "productName": "Coffee & drinks", "batchYield": 1,
                "ingredients": [{ "id": "ri-1", "ingredientId": "ing-milk", "qty": 200, "unit": "ml" }] }],

  "projectDescription": "The founder's own description, verbatim.",

  // Optional: competitors (rows) × features (columns). "has" lists feature ids.
  "competitorBenchmark": {
    "features": [{ "id": "f1", "name": "Oat milk at no extra charge" }],
    "competitors": [{ "id": "c1", "name": "Chain café on the same street", "has": ["f1"] }]
  }
}
```

(Comments are for illustration only. The real file must be plain JSON, without comments.)

## Before you hand it over

- [ ] `overview.employment` equals the sum of `headcount` in `human-resources`.
- [ ] Every opex figure is monthly, not annual.
- [ ] Every revenue row has a `pricingMode`, and only the fields for that mode are filled.
- [ ] `taxRatePct` is set to the real rate for the location.
- [ ] Every row has a source tag in `notes`.

"""Engine-sourced numbers for Foundation documents.

Shared by business-plan-writer and pitch-deck-writer. The two copies must stay identical:
skills/tests/test_scripts.py checks it.

A *facts file* is JSON holding the Foundation engine's own output, saved verbatim:

    {
      "currency": "USD",
      "project":   { ...get_project output... },          # optional
      "results":   { ...compute_feasibility output... },
      "scenarios": { ...compute_scenarios output... }      # optional
    }

Document text never contains retyped financial figures. It contains tokens that are resolved
from the facts file when the file is built:

    "NPV is {{results.npv|money}} at a {{project.assumptions.discountRatePct|pct}} discount rate."

A token whose path doesn't exist stops the build with an error. It is never left blank or
guessed.
"""

from __future__ import annotations

import json
import math
import re
from typing import Any

TOKEN = re.compile(r"\{\{\s*([A-Za-z0-9_.\-]+)\s*(?:\|\s*([a-z_]+)\s*)?\}\}")

CURRENCY_SYMBOLS = {
    "USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥", "CNY": "¥", "INR": "₹",
    "CAD": "CA$", "AUD": "A$", "TRY": "₺",
}

# Titles for category ids (see Foundation's categoryLibrary.ts), so breakdown tables read well.
CATEGORY_TITLES = {
    "land": "Land", "landscaping": "Landscaping", "building": "Building",
    "machinery": "Machinery & equipment", "electrical": "Electrical installation",
    "water": "Water supply", "fuel": "Fuel supply", "air-compressed": "Compressed air",
    "hvac": "Heating & cooling", "other-equipment": "Other facility equipment",
    "logistics": "Vehicles & logistics", "office-equipment": "Office equipment",
    "pre-operational": "Pre-operational expenses", "raw-materials": "Raw materials",
    "human-resources": "Staff", "revenue": "Revenue",
    "leasehold-improvements": "Leasehold improvements", "kitchen-equipment": "Kitchen equipment",
    "furniture-fixtures": "Furniture & fixtures", "pos-setup": "POS setup",
    "dev-equipment": "Computers & dev equipment", "signage-branding": "Signage & branding",
    "initial-inventory": "Initial inventory", "rent-lease": "Rent / lease",
    "cloud-hosting": "Cloud hosting", "software-licenses": "Software & SaaS tools",
    "payment-processing": "Payment processing", "professional-services": "Legal & professional",
    "admin": "Admin & overhead", "marketing": "Marketing", "maintenance": "Maintenance",
    "energy": "Energy", "depreciation": "Depreciation", "contingency": "Contingency",
}


class FactsError(ValueError):
    pass


def category_title(category_id: str) -> str:
    return CATEGORY_TITLES.get(category_id, category_id.replace("-", " ").capitalize())


class Facts:
    def __init__(self, data: dict[str, Any] | None):
        self.data = data or {}
        self.currency = str(self.data.get("currency") or self.data.get("project", {}).get("currency") or "")

    @classmethod
    def load(cls, path: str | None) -> "Facts":
        if not path:
            return cls(None)
        with open(path, encoding="utf-8") as f:
            return cls(json.load(f))

    @property
    def available(self) -> bool:
        return "results" in self.data

    def get(self, path: str) -> Any:
        node: Any = self.data
        for part in path.split("."):
            if isinstance(node, list):
                if part == "last":
                    idx = len(node) - 1
                elif part.lstrip("-").isdigit():
                    idx = int(part)
                else:
                    raise FactsError(f'"{path}": "{part}" is not a list index')
                if not node or idx >= len(node) or idx < -len(node):
                    raise FactsError(f'"{path}": index {part} out of range')
                node = node[idx]
            elif isinstance(node, dict):
                if part not in node:
                    raise FactsError(f'"{path}": no "{part}" in the facts file')
                node = node[part]
            else:
                raise FactsError(f'"{path}": can\'t look up "{part}" inside a {type(node).__name__}')
        return node

    # --- formatting -------------------------------------------------------------------------

    def money(self, value: Any, compact: bool = False) -> str:
        v = _num(value)
        sym = CURRENCY_SYMBOLS.get(self.currency)
        sign = "−" if v < 0 else ""
        v = abs(v)
        if compact and v >= 1_000_000_000:
            body = f"{v / 1_000_000_000:.1f}B"
        elif compact and v >= 1_000_000:
            body = f"{v / 1_000_000:.1f}M"
        elif compact and v >= 10_000:
            body = f"{v / 1_000:.0f}k"
        else:
            body = f"{v:,.0f}"
        return f"{sign}{sym}{body}" if sym else f"{sign}{body} {self.currency}".rstrip()

    def format(self, value: Any, fmt: str | None) -> str:
        fmt = fmt or "auto"
        if fmt == "raw":
            return "" if value is None else str(value)
        if value is None:
            # The engine uses null for "not meaningful": IRR with no sign change, payback outside the horizon.
            return {"years": "not within the projection", "pct": "n/a"}.get(fmt, "n/a")
        if fmt == "money":
            return self.money(value)
        if fmt == "money_compact":
            return self.money(value, compact=True)
        if fmt == "pct":
            return f"{_num(value):.1f}%"
        if fmt == "years":
            return f"{_num(value):.1f} years"
        if fmt == "months":
            return f"{_num(value):.0f} months"
        if fmt == "int":
            return f"{_num(value):,.0f}"
        if fmt == "number":
            return f"{_num(value):,.2f}".rstrip("0").rstrip(".")
        if fmt == "ratio":
            return f"{_num(value):.1f}×"
        if fmt == "auto":
            return f"{value:,.0f}" if isinstance(value, (int, float)) else str(value)
        raise FactsError(f'unknown format "{fmt}" (use money, money_compact, pct, years, months, int, number, ratio, raw)')

    def fill(self, text: str) -> str:
        """Replace every {{path|format}} token. Raises FactsError if any can't be resolved."""
        if "{{" not in text:
            return text
        if not self.data:
            raise FactsError(f"text uses engine numbers but no facts file was given: {text[:80]!r}")
        return TOKEN.sub(lambda m: self.format(self.get(m.group(1)), m.group(2)), text)

    # --- ready-made tables from the engine's output -----------------------------------------

    def projection_rows(self) -> tuple[list[str], list[list[str]]]:
        rows = self.get("results.projection")
        header = ["Year", "Revenue", "Fixed costs", "Variable costs", "Net profit", "Cumulative cash flow"]
        body = [
            [str(r["year"]), self.money(r["revenue"]), self.money(r["fixedCost"]), self.money(r["variableCost"]),
             self.money(r["netProfit"]), self.money(r["cumulativeCashFlow"])]
            for r in rows
        ]
        return header, body

    def breakdown_rows(self, which: str) -> tuple[list[str], list[list[str]]]:
        """which = "capex" or "opex": per-category amounts plus the engine's derived lines."""
        b = self.get(f"results.{which}")
        rows = [[category_title(k), self.money(v)] for k, v in b.get("byCategory", {}).items() if _num(v) != 0]
        extras = ["contingency"] if which == "capex" else ["energy", "depreciation", "contingency"]
        rows += [[category_title(k), self.money(b[k])] for k in extras if _num(b.get(k, 0)) != 0]
        rows.append(["Total fixed investment" if which == "capex" else "Total annual operating cost", self.money(b["total"])])
        return [("Investment item" if which == "capex" else "Annual cost"), "Amount"], rows

    def scenario_rows(self) -> tuple[list[str], list[list[str]]]:
        sc = self.get("scenarios")
        names = [n for n in ("worst", "base", "best") if n in sc]
        header = ["", *[n.capitalize() for n in names]]
        last = lambda r, f: r["projection"][-1][f] if r.get("projection") else r[f]  # noqa: E731
        rows = [
            ["Revenue (final year)", *[self.money(last(sc[n], "revenue")) for n in names]],
            ["Net profit (final year)", *[self.money(last(sc[n], "netProfit")) for n in names]],
            ["NPV", *[self.money(sc[n]["npv"]) for n in names]],
            ["IRR", *[self.format(sc[n]["irrPct"], "pct") for n in names]],
            ["Payback", *[self.format(sc[n]["simplePaybackYears"], "years") for n in names]],
            ["Peak funding needed", *[self.money(sc[n]["peakFundingRequirement"]) for n in names]],
        ]
        return header, rows

    def input_rows(self, category_id: str) -> tuple[list[str], list[list[str]]]:
        """The founder's own inputs for one category, with their notes (source tags), for an assumptions appendix."""
        rows = self.get("project.lineItems").get(category_id, [])
        label_keys = ("description", "role", "product", "material")
        skip = {"id", "hidden", "pricingMode", "notes", *label_keys}
        body = []
        for r in rows:
            if str(r.get("hidden", 0)) == "1":
                continue
            label = next((str(r[k]) for k in label_keys if r.get(k)), "")
            values = ", ".join(f"{_humanize(k)} {v}" for k, v in r.items() if k not in skip and str(v) not in ("", "0"))
            body.append([label, values, str(r.get("notes", ""))])
        return ["Item", "Inputs", "Source / reasoning"], body

    def series(self, source: str, field: str) -> list[float]:
        return [_num(r[field]) for r in self.get(source)]


def _humanize(key: str) -> str:
    """monthlySalary -> monthly salary, employerBurdenPct -> employer burden %."""
    words = re.sub(r"(?<!^)(?=[A-Z])", " ", key).lower().split()
    return " ".join("%" if w == "pct" else w for w in words)


def _num(value: Any) -> float:
    try:
        v = float(value)
    except (TypeError, ValueError) as e:
        raise FactsError(f"expected a number, got {value!r}") from e
    if math.isnan(v) or math.isinf(v):
        raise FactsError(f"expected a finite number, got {value!r}")
    return v

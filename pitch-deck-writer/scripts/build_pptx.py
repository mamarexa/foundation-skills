#!/usr/bin/env python3
"""Render a pitch-deck spec (JSON) into a 16:9 PowerPoint file.

    python build_pptx.py deck.json pitch-deck.pptx [--facts facts.json] [--pdf] [--png DIR]

Needs python-pptx and matplotlib (both preinstalled in Claude's code-execution sandbox;
elsewhere: pip install python-pptx matplotlib). --pdf converts with LibreOffice (soffice) when
it's installed; --png DIR additionally renders one PNG per slide (needs PyMuPDF) for visual QA.

The spec format is documented in ../references/spec-format.md. Every {{path|format}} token is
filled from the facts file (the Foundation engine's own output). See foundation_facts.py.
"""

from __future__ import annotations

import argparse
import io
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.oxml.xmlchemy import OxmlElement
from pptx.util import Emu, Inches, Pt

sys.path.insert(0, str(Path(__file__).parent))
from foundation_facts import Facts, FactsError  # noqa: E402

W, H = 13.333, 7.5  # inches, 16:9
MARGIN = 0.7

DEFAULT_THEME = {
    "heading_font": "Georgia",
    "body_font": "Calibri",
    "bg": "FBFBFA",
    "ink": "111111",
    "muted": "787774",
    "border": "E4E3DF",
    "fill": "F2F1EC",
    "accent": "1F6C9F",
    "dark_bg": "111111",
    "dark_ink": "F2F1EC",
}

INLINE = re.compile(r"(\*\*[^*]+\*\*)")


def rgb(hex_: str) -> RGBColor:
    return RGBColor.from_string(hex_.upper())


class Deck:
    def __init__(self, spec: dict, facts: Facts):
        self.spec = spec
        self.facts = facts
        self.t = {**DEFAULT_THEME, **spec.get("theme", {})}
        self.prs = Presentation()
        self.prs.slide_width, self.prs.slide_height = Inches(W), Inches(H)
        self.blank = self.prs.slide_layouts[6]
        self.warnings: list[str] = []
        self.n = 0

    # --- primitives -------------------------------------------------------------------------

    def text(self, value) -> str:
        return self.facts.fill(str(value))

    def new_slide(self, dark: bool = False):
        slide = self.prs.slides.add_slide(self.blank)
        bg = slide.background.fill
        bg.solid()
        bg.fore_color.rgb = rgb(self.t["dark_bg"] if dark else self.t["bg"])
        self.n += 1
        return slide

    def box(self, slide, x, y, w, h, text, size=18, color=None, font=None, bold=False,
            align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, line_spacing=1.1, label="text"):
        text = self.text(text)
        self.check_fit(text, w, h, size, label)
        tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = anchor
        for attr in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
            setattr(tf, attr, Emu(0))
        for i, line in enumerate(text.split("\n")):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = align
            p.line_spacing = line_spacing
            for part in INLINE.split(line):
                if not part:
                    continue
                run = p.add_run()
                is_bold = part.startswith("**") and part.endswith("**")
                run.text = part[2:-2] if is_bold else part
                f = run.font
                f.size = Pt(size)
                f.bold = bold or is_bold
                f.name = font or self.t["body_font"]
                f.color.rgb = rgb(color or self.t["ink"])
        return tb

    def rect(self, slide, x, y, w, h, fill, line=None):
        shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        shp.fill.solid()
        shp.fill.fore_color.rgb = rgb(fill)
        if line:
            shp.line.color.rgb = rgb(line)
            shp.line.width = Pt(0.75)
        else:
            shp.line.fill.background()
        shp.shadow.inherit = False
        sp_pr = shp._element.spPr
        if sp_pr.find(qn("a:effectLst")) is None:
            sp_pr.append(OxmlElement("a:effectLst"))  # no theme shadow, in any renderer
        return shp

    def check_fit(self, text: str, w: float, h: float, size: float, label: str) -> None:
        """Rough overflow check: average glyph ≈ 0.5 em wide, line height ≈ 1.2 em."""
        chars_per_line = max(1, int(w * 72 / (size * 0.5)))
        lines = sum(max(1, math.ceil(len(seg) / chars_per_line)) for seg in text.split("\n"))
        needed = lines * size * 1.2 / 72
        if needed > h * 1.05:
            self.warnings.append(f"slide {self.n}: {label} probably overflows its box ({needed:.1f}in needed, {h:.1f}in available): {text[:60]!r}")

    def headline(self, slide, s: dict, dark=False) -> float:
        """The slide's takeaway as a sentence, plus an optional small kicker above it. Returns the y below it."""
        y = MARGIN - 0.1
        if s.get("kicker"):
            self.box(slide, MARGIN, y, W - 2 * MARGIN, 0.35, s["kicker"].upper(), size=11,
                     color=self.t["accent"] if not dark else self.t["dark_ink"], bold=True, label="kicker")
            y += 0.42
        self.box(slide, MARGIN, y, W - 2 * MARGIN, 1.25, s["headline"], size=s.get("headline_size", 30),
                 font=self.t["heading_font"], color=self.t["dark_ink"] if dark else self.t["ink"], label="headline")
        return y + 1.45

    def footer(self, slide, dark=False) -> None:
        name = self.spec.get("company", "")
        color = self.t["muted"]
        self.box(slide, MARGIN, H - 0.45, 6, 0.3, name, size=9, color=color, label="footer")
        self.box(slide, W - MARGIN - 1, H - 0.45, 1, 0.3, str(self.n), size=9, color=color, align=PP_ALIGN.RIGHT, label="footer")

    def notes(self, slide, s: dict) -> None:
        if s.get("notes"):
            slide.notes_slide.notes_text_frame.text = self.text(s["notes"])

    # --- slide types ------------------------------------------------------------------------

    def s_title(self, s: dict) -> None:
        slide = self.new_slide(dark=True)
        t = self.t
        self.box(slide, MARGIN, 2.3, W - 2 * MARGIN, 1.4, s.get("title", self.spec.get("company", "")), size=54,
                 font=t["heading_font"], color=t["dark_ink"], label="title")
        self.box(slide, MARGIN, 3.8, 9, 1.2, s.get("tagline", ""), size=22, color="B9B7B0", label="tagline")
        self.rect(slide, MARGIN, 3.65, 1.2, 0.05, t["accent"])
        self.box(slide, MARGIN, H - 1.1, 9, 0.5, s.get("footnote", ""), size=12, color="8F8D86", label="footnote")
        self.notes(slide, s)

    def s_statement(self, s: dict) -> None:
        """One big idea: a problem, a solution, a 'why now'. Optional supporting points on the right."""
        slide = self.new_slide(dark=s.get("dark", False))
        dark = s.get("dark", False)
        if s.get("kicker"):
            self.box(slide, MARGIN, 1.0, 6, 0.35, s["kicker"].upper(), size=11, bold=True,
                     color=self.t["dark_ink"] if dark else self.t["accent"], label="kicker")
        points = s.get("points", [])
        text_w = 6.4 if points else W - 2 * MARGIN
        self.box(slide, MARGIN, 1.5, text_w, 3.6, s["headline"], size=s.get("headline_size", 36), font=self.t["heading_font"],
                 color=self.t["dark_ink"] if dark else self.t["ink"], label="headline")
        if s.get("subtext"):
            self.box(slide, MARGIN, 5.2, text_w, 1.4, s["subtext"], size=16, color=self.t["muted"], label="subtext")
        if points:
            x, y = 7.8, 1.5
            for p in points[:4]:
                self.rect(slide, x, y + 0.08, 0.06, 0.95, self.t["accent"])
                self.box(slide, x + 0.3, y, W - MARGIN - x - 0.3, 1.1, p, size=16,
                         color=self.t["dark_ink"] if dark else self.t["ink"], label="point")
                y += 1.3
        self.footer(slide, dark)
        self.notes(slide, s)

    def s_kpis(self, s: dict) -> None:
        slide = self.new_slide()
        y = self.headline(slide, s)
        items = s["items"][:4]
        gap = 0.3
        cw = (W - 2 * MARGIN - gap * (len(items) - 1)) / len(items)
        for i, item in enumerate(items):
            x = MARGIN + i * (cw + gap)
            self.rect(slide, x, y + 0.2, cw, 0.03, self.t["ink"])
            self.box(slide, x, y + 0.45, cw, 1.1, item["value"], size=40, font=self.t["heading_font"], label="kpi value")
            self.box(slide, x, y + 1.6, cw, 0.9, item["label"], size=14, color=self.t["muted"], label="kpi label")
        if s.get("subtext"):
            self.box(slide, MARGIN, H - 1.5, W - 2 * MARGIN, 0.8, s["subtext"], size=14, color=self.t["muted"], label="subtext")
        self.footer(slide)
        self.notes(slide, s)

    def s_chart(self, s: dict) -> None:
        slide = self.new_slide()
        y = self.headline(slide, s)
        side = s.get("side_points")
        cw = 8.2 if side else W - 2 * MARGIN
        png = render_chart(s["chart"], self.facts, self.t, width_in=cw, height_in=H - y - 0.9)
        slide.shapes.add_picture(png, Inches(MARGIN), Inches(y), Inches(cw), Inches(H - y - 0.9))
        if side:
            x, yy = MARGIN + cw + 0.5, y + 0.2
            for p in side[:3]:
                self.box(slide, x, yy, W - MARGIN - x, 1.3, p, size=15, label="side point")
                yy += 1.5
        self.footer(slide)
        self.notes(slide, s)

    def s_bullets(self, s: dict) -> None:
        slide = self.new_slide()
        y = self.headline(slide, s)
        items = s["items"][:5]
        for i, item in enumerate(items):
            yy = y + i * 0.95
            self.box(slide, MARGIN, yy, 0.6, 0.6, f"{i + 1:02d}", size=14, color=self.t["accent"], bold=True, label="number")
            self.box(slide, MARGIN + 0.7, yy, W - 2 * MARGIN - 0.7, 0.85, item, size=18, label="bullet")
        self.footer(slide)
        self.notes(slide, s)

    def s_table(self, s: dict) -> None:
        slide = self.new_slide()
        y = self.headline(slide, s)
        self.table(slide, [self.text(c) for c in s["columns"]], [[self.text(c) for c in r] for r in s["rows"]], y)
        self.footer(slide)
        self.notes(slide, s)

    def s_scenarios(self, s: dict) -> None:
        slide = self.new_slide()
        y = self.headline(slide, s)
        header, rows = self.facts.scenario_rows()
        self.table(slide, header, rows, y, center_from=1, highlight=None)
        self.footer(slide)
        self.notes(slide, s)

    def s_benchmark(self, s: dict) -> None:
        """The project's Competitor Benchmark grid (from the facts file) as a check-mark table."""
        slide = self.new_slide()
        y = self.headline(slide, s)
        grid = self.facts.get("project.competitorBenchmark")
        features = grid["features"][: s.get("max_features", 7)]
        header = ["", *[f["name"] for f in features]]
        rows = [[c["name"], *["✓" if f["id"] in c["has"] else "–" for f in features]] for c in grid["competitors"][: s.get("max_rows", 7)]]
        highlight = s.get("highlight_row")  # e.g. "Us (planned)"
        self.table(slide, header, rows, y, center_from=1, highlight=highlight)
        self.footer(slide)
        self.notes(slide, s)

    def table(self, slide, header, rows, y, center_from=99, highlight=None) -> None:
        t = self.t
        n_rows, n_cols = len(rows) + 1, len(header)
        max_h = H - y - 0.8
        row_h = min(0.55, max_h / n_rows)
        size = 14 if row_h >= 0.5 else 12
        shape = slide.shapes.add_table(n_rows, n_cols, Inches(MARGIN), Inches(y), Inches(W - 2 * MARGIN), Inches(row_h * n_rows))
        table = shape.table
        tbl_pr = shape._element.graphic.graphicData.tbl.tblPr
        tbl_pr.set("bandRow", "0")
        tbl_pr.set("firstRow", "0")
        first_w = 3.2 if n_cols > 3 else (W - 2 * MARGIN) / n_cols
        table.columns[0].width = Inches(first_w)
        for c in range(1, n_cols):
            table.columns[c].width = Inches((W - 2 * MARGIN - first_w) / (n_cols - 1))
        for r, values in enumerate([header, *rows]):
            is_hl = highlight is not None and r > 0 and values[0] == highlight
            for c, value in enumerate(values):
                cell = table.cell(r, c)
                cell.fill.solid()
                cell.fill.fore_color.rgb = rgb(t["fill"] if r == 0 else ("E1ECF4" if is_hl else t["bg"]))
                cell.margin_left = cell.margin_right = Inches(0.08)
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                tf = cell.text_frame
                tf.word_wrap = True
                p = tf.paragraphs[0]
                p.text = str(value)
                p.alignment = PP_ALIGN.CENTER if c >= center_from else PP_ALIGN.LEFT
                f = p.runs[0].font if p.runs else p.font
                f.size = Pt(11 if r == 0 else size)
                f.name = t["body_font"]
                f.bold = r == 0 or is_hl
                f.color.rgb = rgb(t["muted"] if r == 0 else (t["accent"] if value == "✓" else t["ink"]))

    def s_market(self, s: dict) -> None:
        """TAM / SAM / SOM as three horizontal bars scaled on a log-ish scale, values as text."""
        slide = self.new_slide()
        y = self.headline(slide, s)
        levels = s["levels"][:3]  # [{"label": "TAM", "value": "£38M", "detail": "..."}]
        widths = [W - 2 * MARGIN - 4.5, (W - 2 * MARGIN - 4.5) * 0.55, (W - 2 * MARGIN - 4.5) * 0.22]
        colors = [self.t["fill"], "D5E3EE", self.t["accent"]]
        for i, lvl in enumerate(levels):
            yy = y + i * 1.35
            self.rect(slide, MARGIN, yy, widths[i], 1.05, colors[i])
            self.box(slide, MARGIN + 0.25, yy + 0.15, 1.5, 0.8, lvl["label"], size=16, bold=True,
                     color="FFFFFF" if i == 2 else self.t["ink"], anchor=MSO_ANCHOR.MIDDLE, label="market label")
            self.box(slide, W - MARGIN - 4.2, yy, 1.6, 1.05, lvl["value"], size=28, font=self.t["heading_font"],
                     anchor=MSO_ANCHOR.MIDDLE, label="market value")
            self.box(slide, W - MARGIN - 2.5, yy, 2.5, 1.05, lvl.get("detail", ""), size=12, color=self.t["muted"],
                     anchor=MSO_ANCHOR.MIDDLE, label="market detail")
        if s.get("source"):
            self.box(slide, MARGIN, H - 0.95, W - 2 * MARGIN, 0.4, s["source"], size=10, color=self.t["muted"], label="source")
        self.footer(slide)
        self.notes(slide, s)

    def s_team(self, s: dict) -> None:
        slide = self.new_slide()
        y = self.headline(slide, s)
        people = s["people"][:4]
        gap = 0.35
        cw = (W - 2 * MARGIN - gap * (len(people) - 1)) / len(people)
        for i, person in enumerate(people):
            x = MARGIN + i * (cw + gap)
            self.rect(slide, x, y, cw, 0.03, self.t["ink"])
            self.box(slide, x, y + 0.25, cw, 0.5, person["name"], size=20, font=self.t["heading_font"], label="name")
            self.box(slide, x, y + 0.8, cw, 0.4, person.get("role", ""), size=13, color=self.t["accent"], bold=True, label="role")
            self.box(slide, x, y + 1.3, cw, 2.4, person.get("bio", ""), size=13, color=self.t["muted"], label="bio")
        self.footer(slide)
        self.notes(slide, s)

    def s_ask(self, s: dict) -> None:
        """The raise: amount on the left, use of funds as proportional bars on the right."""
        slide = self.new_slide()
        y = self.headline(slide, s)
        self.box(slide, MARGIN, y + 0.1, 4.6, 1.3, s["amount"], size=54, font=self.t["heading_font"], label="amount")
        self.box(slide, MARGIN, y + 1.5, 4.4, 2.6, s.get("terms", ""), size=15, color=self.t["muted"], label="terms")
        uses = s.get("use_of_funds", [])  # [{"label": "Fit-out", "pct": 40}]
        x0, bar_w = 5.9, W - MARGIN - 5.9
        for i, u in enumerate(uses[:6]):
            yy = y + 0.1 + i * 0.75
            pct = max(0.0, min(100.0, float(u["pct"])))
            self.box(slide, x0, yy, bar_w * 0.6, 0.35, u["label"], size=14, label="use label")
            self.box(slide, x0 + bar_w - 1.0, yy, 1.0, 0.35, f"{pct:.0f}%", size=14, bold=True, align=PP_ALIGN.RIGHT, label="use pct")
            self.rect(slide, x0, yy + 0.4, bar_w, 0.12, self.t["fill"])
            self.rect(slide, x0, yy + 0.4, max(0.05, bar_w * pct / 100), 0.12, self.t["accent"])
        total = sum(float(u["pct"]) for u in uses)
        if uses and abs(total - 100) > 0.5:
            self.warnings.append(f"slide {self.n}: use of funds adds up to {total:.0f}%, not 100%")
        if s.get("milestones"):
            self.box(slide, MARGIN, H - 1.35, W - 2 * MARGIN, 0.7, s["milestones"], size=14, label="milestones")
        self.footer(slide)
        self.notes(slide, s)

    def s_closing(self, s: dict) -> None:
        slide = self.new_slide(dark=True)
        self.box(slide, MARGIN, 2.6, W - 2 * MARGIN, 1.4, s.get("headline", self.spec.get("company", "")), size=44,
                 font=self.t["heading_font"], color=self.t["dark_ink"], label="closing")
        self.box(slide, MARGIN, 4.2, W - 2 * MARGIN, 1.2, s.get("contact", ""), size=18, color="B9B7B0", label="contact")
        self.notes(slide, s)

    def build(self) -> Presentation:
        for s in self.spec["slides"]:
            handler = getattr(self, f"s_{s.get('type', 'statement')}", None)
            if handler is None:
                raise ValueError(f'unknown slide type "{s.get("type")}"')
            handler(s)
        return self.prs


def render_chart(c: dict, facts: Facts, t: dict, width_in: float, height_in: float) -> io.BytesIO:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter

    if c.get("from"):
        labels = [f"Year {int(v)}" for v in facts.series(c["from"], c.get("x", "year"))]
        series = [{"name": s["name"], "values": facts.series(c["from"], s["field"]), "kind": s.get("kind")} for s in c["series"]]
    else:
        labels = [str(x) for x in c["labels"]]
        series = c["series"]
    palette = [f"#{t['ink']}", f"#{t['accent']}", "#A3A29C"]
    fig, ax = plt.subplots(figsize=(width_in, height_in), dpi=200)
    fig.patch.set_facecolor(f"#{t['bg']}")
    ax.set_facecolor(f"#{t['bg']}")
    bars = [s for s in series if (s.get("kind") or c.get("kind", "bar")) == "bar"]
    width = 0.8 / max(1, len(bars))
    xs = list(range(len(labels)))
    bi = 0
    for i, s in enumerate(series):
        color = palette[i % len(palette)]
        if (s.get("kind") or c.get("kind", "bar")) == "line":
            ax.plot(xs, s["values"], color=color, linewidth=3, marker="o", markersize=6, label=s["name"])
        else:
            off = (bi - (len(bars) - 1) / 2) * width
            ax.bar([x + off for x in xs], s["values"], width=width * 0.9, color=color, label=s["name"])
            bi += 1
    money = c.get("unit", "money") == "money"
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: facts.money(v, compact=True) if money else f"{v:,.0f}"))
    ax.set_xticks(xs, labels)
    ax.axhline(0, color="#999999", linewidth=1)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color("#BBBBBB")
    ax.tick_params(colors="#555555", labelsize=13, length=0)
    ax.grid(axis="y", color="#E6E5E1", linewidth=1)
    ax.set_axisbelow(True)
    if len(series) > 1:
        ax.legend(frameon=False, fontsize=13, loc="upper left")
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return buf


def verify(path: Path) -> list[str]:
    prs = Presentation(str(path))
    problems = []
    for i, slide in enumerate(prs.slides, 1):
        text = " ".join(sh.text_frame.text for sh in slide.shapes if sh.has_text_frame)
        if "{{" in text:
            problems.append(f"slide {i}: unresolved {{{{token}}}}")
        for marker in ("lorem", "TODO", "TBD", "[insert", "xxxx"):
            if marker.lower() in text.lower():
                problems.append(f'slide {i}: placeholder "{marker}"')
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec")
    ap.add_argument("out")
    ap.add_argument("--facts")
    ap.add_argument("--pdf", action="store_true")
    ap.add_argument("--png", metavar="DIR", help="render each slide to DIR/slide-N.png (implies --pdf)")
    args = ap.parse_args()

    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    deck = Deck(spec, Facts.load(args.facts))
    try:
        prs = deck.build()
    except FactsError as e:
        print(f"ERROR (numbers): {e}", file=sys.stderr)
        return 2
    out = Path(args.out)
    prs.save(str(out))
    problems = verify(out) + deck.warnings
    for p in problems:
        print(f"WARNING: {p}", file=sys.stderr)
    print(f"wrote {out} ({deck.n} slides)")

    if args.pdf or args.png:
        soffice = shutil.which("soffice") or shutil.which("libreoffice")
        if not soffice:
            print("note: LibreOffice not installed, skipped PDF/PNG export", file=sys.stderr)
        else:
            subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", str(out.parent), str(out)],
                           check=True, capture_output=True, timeout=180)
            pdf = out.with_suffix(".pdf")
            print(f"wrote {pdf}")
            if args.png:
                try:
                    import pymupdf
                except ImportError:
                    print("note: PyMuPDF not installed, skipped PNG export", file=sys.stderr)
                else:
                    d = Path(args.png)
                    d.mkdir(parents=True, exist_ok=True)
                    for i, page in enumerate(pymupdf.open(str(pdf)), 1):
                        page.get_pixmap(dpi=80).save(str(d / f"slide-{i}.png"))
                    print(f"wrote slide PNGs to {d}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

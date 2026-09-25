"""Check that a restyled document still carries exactly the numbers of the original.

Shared by business-plan-writer and pitch-deck-writer. The two copies must stay identical:
skills/tests/test_scripts.py checks it.

Use it after any second-step restyle, whether by another skill, another tool or a person:

    python check_numbers.py original.docx restyled.docx
    python check_numbers.py original.pptx restyled.pptx

It compares every number in the two files: amounts, percentages, years, counts. Exit code 0
means none was lost, changed or added. Otherwise it lists the differences, and the restyled
file must not be used until they're fixed.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

NUMBER = re.compile(r"[−\-]?[$€£¥₹₺]?\d[\d,]*(?:\.\d+)?\s?(?:%|×|k|M|B|bn)?")


def extract_text(path: str) -> str:
    p = Path(path)
    if p.suffix.lower() == ".docx":
        from docx import Document

        doc = Document(str(p))
        parts = [para.text for para in doc.paragraphs]
        parts += [cell.text for t in doc.tables for row in t.rows for cell in row.cells]
        for section in doc.sections:
            parts += [para.text for para in section.header.paragraphs]
        return "\n".join(parts)
    if p.suffix.lower() == ".pptx":
        from pptx import Presentation

        parts = []
        for slide in Presentation(str(p)).slides:
            for shape in slide.shapes:
                if shape.has_text_frame:
                    parts.append(shape.text_frame.text)
                if getattr(shape, "has_table", False) and shape.has_table:
                    parts += [c.text for row in shape.table.rows for c in row.cells]
        return "\n".join(parts)
    raise SystemExit(f"unsupported file type: {path} (use .docx or .pptx)")


def numbers(text: str) -> Counter:
    found = Counter()
    for m in NUMBER.finditer(text):
        n = re.sub(r"\s", "", m.group()).replace("−", "-")
        if re.fullmatch(r"-?\d", n):  # single digits: list numbers, slide numbers; too noisy to compare
            continue
        found[n] += 1
    return found


def compare(original: str, restyled: str) -> tuple[Counter, Counter]:
    a, b = numbers(extract_text(original)), numbers(extract_text(restyled))
    return a - b, b - a


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    missing, added = compare(sys.argv[1], sys.argv[2])
    for n, c in sorted(missing.items()):
        print(f"MISSING in restyled file: {n}" + (f" (x{c})" if c > 1 else ""))
    for n, c in sorted(added.items()):
        print(f"NEW in restyled file (not in the original): {n}" + (f" (x{c})" if c > 1 else ""))
    if not missing and not added:
        print("ok: every number matches the original")
    sys.exit(1 if missing or added else 0)

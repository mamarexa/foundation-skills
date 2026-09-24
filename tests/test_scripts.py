"""Smoke tests for the document skills' renderers.

    python skills/tests/test_scripts.py

Builds the café fixtures (whose facts come from the real Foundation engine, see
scripts/make-skill-fixture-facts.ts in the app repo) and checks the guarantees the skills rely on.
"""

import filecmp
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "tests" / "fixtures"
DOCX = ROOT / "business-plan-writer" / "scripts" / "build_docx.py"
PPTX = ROOT / "pitch-deck-writer" / "scripts" / "build_pptx.py"
failures = []


def check(name, cond, detail=""):
    print(("ok   " if cond else "FAIL ") + name + (f": {detail}" if detail and not cond else ""))
    if not cond:
        failures.append(name)


def run(*args):
    return subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True)


check(
    "foundation_facts.py copies are identical",
    filecmp.cmp(ROOT / "business-plan-writer/scripts/foundation_facts.py", ROOT / "pitch-deck-writer/scripts/foundation_facts.py", shallow=False),
)

with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    r = run(DOCX, FIX / "coffee-plan-spec.json", tmp / "plan.docx", "--facts", FIX / "coffee-facts.json")
    check("business plan builds cleanly", r.returncode == 0 and "WARNING" not in r.stderr, r.stderr)

    r = run(PPTX, FIX / "coffee-deck-spec.json", tmp / "deck.pptx", "--facts", FIX / "coffee-facts.json")
    check("pitch deck builds cleanly", r.returncode == 0 and "WARNING" not in r.stderr, r.stderr)

    from pptx import Presentation  # noqa: E402
    facts = json.loads((FIX / "coffee-facts.json").read_text())
    text = " ".join(sh.text_frame.text for s in Presentation(str(tmp / "deck.pptx")).slides for sh in s.shapes if sh.has_text_frame)
    check("engine IRR appears in the deck", f"{facts['results']['irrPct']:.1f}%" in text)

    bad = json.loads((FIX / "coffee-plan-spec.json").read_text())
    bad["sections"][0]["blocks"].append({"type": "paragraph", "text": "IRR is {{results.irrr|pct}}"})
    (tmp / "bad.json").write_text(json.dumps(bad))
    r = run(DOCX, tmp / "bad.json", tmp / "bad.docx", "--facts", FIX / "coffee-facts.json")
    check("a typo'd engine path stops the build", r.returncode == 2 and "irrr" in r.stderr, r.stderr)

    r = run(DOCX, FIX / "coffee-plan-spec.json", tmp / "nofacts.docx")
    check("engine tokens without a facts file stop the build", r.returncode == 2, r.stderr)

sys.exit(1 if failures else 0)

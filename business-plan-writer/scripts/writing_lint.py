"""Mechanical checks for the most recognisable AI-writing tells, run on every spec before rendering.

Shared by business-plan-writer and pitch-deck-writer. The two copies must stay identical:
skills/tests/test_scripts.py checks it.

This catches only what a machine can catch reliably: dashes, a short list of overused words,
chatbot leftovers and a few stock constructions. The full judgement pass is in
references/writing-style.md. The checklist is based on Wikipedia's "Signs of AI writing" guide
(WikiProject AI Cleanup), paraphrased.

    python writing_lint.py spec.json      # standalone use; exit code 1 if anything is flagged
"""

from __future__ import annotations

import json
import re
import sys
from typing import Any

# Words that AI-generated text overuses. Flagged, not banned: a real use is fine if nothing
# plainer fits, but each one should be a conscious choice.
OVERUSED = [
    "delve", "tapestry", "testament", "pivotal", "seamless", "seamlessly", "robust", "leverage",
    "leveraging", "unlock", "unleash", "elevate", "empower", "game-changer", "game-changing",
    "cutting-edge", "revolutionary", "revolutionize", "landscape", "realm", "embark", "foster",
    "fostering", "underscore", "underscores", "showcase", "showcasing", "vibrant", "meticulous",
    "intricate", "interplay", "navigate the", "in today's", "ever-evolving", "synergy",
    "holistic", "paradigm", "bustling", "nestled", "boasts", "crucial role", "key role",
]

PATTERNS = [
    (re.compile(r"—"), "em dash: rewrite with a comma, colon, parentheses or two sentences"),
    (re.compile(r"\s–\s"), "spaced en dash used as a dash: rewrite the sentence"),
    (re.compile(r"\bnot (only|just|merely)\b[^.]{0,80}\bbut\b", re.I), '"not only/just X but Y" construction: state the point directly'),
    (re.compile(r"\bit'?s not (just )?about\b", re.I), '"it\'s not about X" framing: state what it is about'),
    (re.compile(r"\b(i hope this helps|let me know if|feel free to|as an ai|great question|certainly!)", re.I), "chatbot leftover"),
    (re.compile(r"\b(experts|studies|research) (say|says|show|shows|suggest|suggests|agree)\b", re.I), "unnamed authority: name the source or cut it"),
    (re.compile(r"\b(could|may|might) potentially\b", re.I), "stacked hedge"),
    (re.compile(r"\bserves as\b|\bstands as\b", re.I), '"serves as / stands as": usually just "is"'),
]

WORD_RE = {w: re.compile(rf"\b{re.escape(w)}\b", re.I) for w in OVERUSED}
TOKEN = re.compile(r"\{\{[^}]*\}\}")


def iter_text(node: Any, path: str = ""):
    """Every string in a spec, with where it sits. Skips theme settings and file paths."""
    if isinstance(node, str):
        yield path, node
    elif isinstance(node, dict):
        for k, v in node.items():
            if k in ("theme", "type", "from", "field", "x", "kind", "unit", "of", "category", "paper", "template"):
                continue
            yield from iter_text(v, f"{path}.{k}" if path else k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from iter_text(v, f"{path}[{i}]")


def lint_spec(spec: dict) -> list[str]:
    problems = []
    for where, raw in iter_text(spec):
        text = TOKEN.sub("", raw)
        for rx, why in PATTERNS:
            if rx.search(text):
                problems.append(f"{where}: {why}: {raw[:70]!r}")
        for word, rx in WORD_RE.items():
            if rx.search(text):
                problems.append(f'{where}: overused word "{word}": {raw[:70]!r}')
    return problems


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as f:
        found = lint_spec(json.load(f))
    for p in found:
        print(f"STYLE: {p}")
    sys.exit(1 if found else 0)

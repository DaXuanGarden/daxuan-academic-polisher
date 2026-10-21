#!/usr/bin/env python3
"""Warning-oriented protected-token preservation check.

It compares exact source/output occurrences of values, units, statistics, citations, figure
references, and common scientific identifiers. It reports both omissions/changes and newly
introduced protected tokens. Passing is not semantic equivalence: read the prose and check
claim strength separately.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

# Keep the whole numeric value, sign, scientific exponent, range, and a conservative unit.
UNIT = r"(?:%|‰|(?:mg|g|kg|μg|µg|ng|pg|mL|L|dL|μL|µL|mol|mmol|μmol|µmol|mm|cm|m|km|nm|°C|K|h|min|s|ms|Hz|kHz|Pa|kPa|mmHg|V|mV|W|kcal)(?:/(?:mg|g|kg|mL|L|dL|mol|mmol|μL|µL|mm|cm|m|h|min|s|Hz|Pa|kPa|mmHg|V|mV|W))?(?:\^[-+]?\d+)?)"
NUMBER = rf"[-+]?(?:\d{{1,3}}(?:,\d{{3}})+(?:\.\d+)?|\d+(?:\.\d+)?)(?:[eE][-+]?\d+)?"
RANGE = rf"{NUMBER}(?:\s*(?:[–—-]|to)\s*{NUMBER})?"
PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("statistic", re.compile(rf"\b(?:p|P)\s*[<=>≤≥]\s*{NUMBER}\b")),
    ("doi_pmid", re.compile(r"\b(?:DOI\s*:\s*|PMID\s*[:#]?\s*)[A-Za-z0-9./_-]+", re.I)),
    ("citation_bracket", re.compile(r"\[[0-9][0-9,;\s–—-]*\]")),
    ("author_year", re.compile(r"(?:\([\u3400-\u9fffA-Za-z][^()]{0,60}[,，]\s*(?:19|20)\d{2}[a-z]?\)|\b[A-Z][A-Za-z'-]+(?:\s+et\s+al\.)?,\s*(?:19|20)\d{2}[a-z]?\b)")),
    ("figure_table", re.compile(r"\b(?:Figure|Fig\.?|Table|Supplementary\s+(?:Figure|Table))\s+[A-Za-z]?\d+(?:[A-Za-z])?\b", re.I)),
    ("identifier", re.compile(r"\b(?:rs\d+|[A-Z]{2,}[A-Z0-9_-]*\d[A-Z0-9_-]*|[A-Z]{2,}(?:[-_][A-Za-z0-9]+)+)\b")),
    ("number_unit", re.compile(rf"(?<![A-Za-z]){RANGE}(?:\s*{UNIT})?")),
]


def extract(text: str) -> Counter[tuple[str, str]]:
    found: list[tuple[int, int, str, str]] = []
    occupied: list[tuple[int, int]] = []
    for category, pattern in PATTERNS:
        for match in pattern.finditer(text):
            span = match.span()
            if any(span[0] < end and start < span[1] for start, end in occupied):
                continue
            value = match.group(0).strip()
            if category == "statistic":
                value = re.sub(r"\s+", "", value)
            found.append((span[0], span[1], category, value))
            occupied.append(span)
    found.sort(key=lambda item: item[0])
    return Counter((category, value) for _, _, category, value in found)


def display(counter: Counter[tuple[str, str]]) -> dict[str, int]:
    return {f"{category}: {value}": count for (category, value), count in sorted(counter.items())}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source = extract(args.source.read_text(encoding="utf-8"))
    output = extract(args.output.read_text(encoding="utf-8"))
    missing = {(cat, val): count - output.get((cat, val), 0) for (cat, val), count in source.items() if output.get((cat, val), 0) < count}
    unexpected = {(cat, val): count - source.get((cat, val), 0) for (cat, val), count in output.items() if output.get((cat, val), 0) > source.get((cat, val), 0)}
    result = {
        "ok": not missing and not unexpected,
        "source_token_count": sum(source.values()),
        "output_token_count": sum(output.values()),
        "missing_or_changed": display(Counter(missing)),
        "unexpected_or_added": display(Counter(unexpected)),
        "source_tokens": display(source),
        "output_tokens": display(output),
        "note": "heuristic only; semantic, terminology, and claim-strength review remains required",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["ok"] else 2)


if __name__ == "__main__":
    main()

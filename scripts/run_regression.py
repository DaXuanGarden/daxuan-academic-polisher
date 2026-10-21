#!/usr/bin/env python3
"""Run deterministic routing and protected-token regression cases."""
from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from detect_language import detect  # noqa: E402
from check_preservation import extract  # noqa: E402


def main() -> None:
    argparse.ArgumentParser(description=__doc__).parse_args()
    routing = json.loads((ROOT / "evals/routing_cases.json").read_text(encoding="utf-8"))
    failures = []
    for case in routing["cases"]:
        got = detect(case["text"])["language"]
        if got != case["expected"]:
            failures.append(f"{case['id']}: expected {case['expected']}, got {got}")
    output_cases = json.loads((ROOT / "evals/output_cases.json").read_text(encoding="utf-8"))
    protected = output_cases["cases"][2]
    source = extract(protected["input"])
    polished = extract(protected["polished_fixture"])
    missing = {token: n - polished.get(token, 0) for token, n in source.items() if polished.get(token, 0) < n}
    added = {token: n - source.get(token, 0) for token, n in polished.items() if n > source.get(token, 0)}
    if missing or added:
        failures.append(f"protected fixture drift: missing={missing}, added={added}")
    with tempfile.TemporaryDirectory() as directory:
        d = Path(directory)
        source_text = "The assay used 2.5 mg/mL, -0.5, and rs12345."
        bad_text = "The assay used 2.5 g/L, 0.5, and rs54321."
        if not (extract(source_text) - extract(bad_text)):
            failures.append("negative preservation regression did not detect drift")
    if failures:
        for failure in failures:
            print("FAIL", failure)
        raise SystemExit(1)
    print(f"PASS routing cases ({len(routing['cases'])})")
    print("PASS protected-token fixture")
    print("PASS negative preservation regression")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Run dependency-free package and portability checks."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ["SKILL.md", "README.md", "LICENSE", "manifest.json", "agents/interface.yaml", "agents/openai.yaml", "examples/README.md", "assets/showcase/polishing-workflow.svg", "evals/routing_cases.json"]


def fail(message: str) -> None:
    print(f"FAIL {message}")
    raise SystemExit(1)


def main() -> None:
    argparse.ArgumentParser(description=__doc__).parse_args()
    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            fail(f"missing {relative}")
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    front = re.match(r"^---\n(.*?)\n---", skill, re.S)
    if not front or not re.search(r"^name:\s*daxuan-academic-polisher\s*$", front.group(1), re.M):
        fail("SKILL.md frontmatter name is missing or stale")
    for path in ROOT.rglob("*"):
        if path.is_file() and ".git" not in path.parts and "__pycache__" not in path.parts:
            data = path.read_text(encoding="utf-8", errors="ignore")
            private_marker = "/" + "Users/"
            stale_marker = "qiaomu" + "-academic-polisher"
            if private_marker in data:
                fail(f"private absolute path found in {path.relative_to(ROOT)}")
            if stale_marker in data:
                fail(f"stale brand in {path.relative_to(ROOT)}")
    try:
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        json.loads((ROOT / "evals/output_cases.json").read_text(encoding="utf-8"))
        json.loads((ROOT / "evals/routing_cases.json").read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON: {exc}")
    if manifest.get("name") != "daxuan-academic-polisher" or manifest.get("maturity_tier") != "beta":
        fail("manifest identity or evidence tier is inconsistent")
    import py_compile
    for script in (ROOT / "scripts").glob("*.py"):
        py_compile.compile(str(script), doraise=True)
    print(f"PASS package structure ({len(REQUIRED)} required files)")
    print("PASS portable paths and brand")
    print("PASS JSON manifests and evaluation fixtures")
    print("PASS Python scripts compile")


if __name__ == "__main__":
    main()

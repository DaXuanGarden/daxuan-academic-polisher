#!/usr/bin/env python3
"""Build a fixture-only showcase card and GIF from authored examples.

The output demonstrates the contract and local checks; it is deliberately labelled as an
authored fixture, not a provider-backed model run.
"""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/showcase"


def wrap(text: str, width: int = 86) -> list[str]:
    words = text.split()
    lines: list[str] = []
    line = ""
    for word in words:
        if len(line) + len(word) + 1 > width and line:
            lines.append(line)
            line = word
        else:
            line = (line + " " + word).strip()
    if line:
        lines.append(line)
    return lines


def main() -> None:
    argparse.ArgumentParser(description=__doc__).parse_args()
    cases = json.loads((ROOT / "evals/output_cases.json").read_text(encoding="utf-8"))["cases"]
    OUT.mkdir(parents=True, exist_ok=True)
    first = cases[0]
    lines = [
        "Daxuan Academic Polisher",
        "Authored fixture · contract demonstration",
        "",
        "BEFORE",
        *wrap(first["input"]),
        "",
        "AFTER",
        *wrap(first["polished_fixture"]),
        "",
        "Numbers, claims and experiment count remain visible.",
    ]
    width = 1200
    line_h = 34
    height = 180 + line_h * len(lines)
    body = []
    for i, line in enumerate(lines):
        fill = "#93c5fd" if i == 0 else ("#fbbf24" if line in {"BEFORE", "AFTER"} else "#e5e7eb")
        size = 28 if i == 0 else 22
        body.append(
            f'<text x="56" y="{90 + i * line_h}" fill="{fill}" '
            f'font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif" '
            f'font-size="{size}">{html.escape(line)}</text>'
        )
    content = "".join(body)
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}"><rect width="100%" height="100%" fill="#111827"/>'
        f'<rect x="28" y="28" width="1144" height="{height - 56}" rx="18" '
        f'fill="#1f2937" stroke="#374151"/>{content}</svg>'
    )
    (OUT / "polish-card.svg").write_text(svg, encoding="utf-8")
    try:
        from PIL import Image, ImageDraw, ImageFont
        font = ImageFont.load_default()
        frames = []
        for mode in ("before", "after"):
            image = Image.new("RGB", (1200, 420), (17, 24, 39))
            draw = ImageDraw.Draw(image)
            draw.text((48, 40), "Daxuan Academic Polisher · authored fixture", fill=(147, 197, 253), font=font)
            draw.text((48, 110), mode.upper(), fill=(251, 191, 36), font=font)
            value = first["input"] if mode == "before" else first["polished_fixture"]
            draw.multiline_text((48, 160), value, fill=(229, 231, 235), font=font, spacing=8)
            frames.append(image)
        frames[0].save(OUT / "demo.gif", save_all=True, append_images=[frames[1]], duration=1100, loop=0)
        gif = True
    except Exception as exc:
        gif = False
        (OUT / "demo-gif-build-error.txt").write_text(str(exc), encoding="utf-8")
    evidence = {
        "evidence_kind": "authored_fixture",
        "model_run": False,
        "svg": str((OUT / "polish-card.svg").relative_to(ROOT)),
        "gif_built": gif,
        "source_case": first["id"],
    }
    (ROOT / "reports/showcase-evidence.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PASS showcase fixture generated")
    print("PASS", OUT / "polish-card.svg")
    print("PASS", OUT / "demo.gif" if gif else "GIF unavailable; SVG remains reproducible")


if __name__ == "__main__":
    main()

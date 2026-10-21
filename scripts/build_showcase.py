#!/usr/bin/env python3
"""Build the static source-language polishing workflow diagram.

The diagram is generated from the skill contract, not from a model run. Its colors follow the
existing Daxuan scientific-assets methodology-blue palette while remaining self-contained.
"""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/showcase"

# Reuse the existing Daxuan scientific-assets methodology-blue family without importing files
# from that repository: the public skill remains self-contained.
COLORS = {
    "body": "#91B2C8",
    "body_light": "#9DBBCF",
    "outline": "#5F91AF",
    "detail": "#B8C8D0",
    "highlight": "#DCE8EF",
    "accent": "#BB748B",
    "muted": "#8E9DA5",
    "field": "#E8F0F4",
    "text": "#39454B",
    "white": "#FFFFFF",
}


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def text(x: float, y: float, value: str, size: int = 24, weight: str = "500", fill: str | None = None, anchor: str = "start") -> str:
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
        f'font-family="Arial, Helvetica, sans-serif" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill or COLORS["text"]}">{esc(value)}</text>'
    )


def card(x: int, y: int, width: int, height: int, title: str, subtitle: str, number: str, icon: str, accent: bool = False) -> str:
    fill = COLORS["highlight"] if accent else COLORS["field"]
    edge = COLORS["accent"] if accent else COLORS["outline"]
    pieces = [f'<g id="card-{number}" data-card="{number}">']
    pieces.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="24" fill="{fill}" stroke="{edge}" stroke-width="3"/>')
    pieces.append(f'<circle cx="{x + 36}" cy="{y + 38}" r="18" fill="{edge}"/>')
    pieces.append(text(x + 36, y + 45, number, 20, "700", COLORS["white"], "middle"))
    pieces.append(text(x + width / 2, y + 105, title, 27, "700", anchor="middle"))
    pieces.append(text(x + width / 2, y + 139, subtitle, 18, "500", COLORS["text"], "middle"))
    # A small line icon keeps the diagram useful even when the labels are skimmed.
    cx, cy = x + width / 2, y + 62
    if icon == "document":
        pieces.append(f'<path d="M{cx-23} {cy-18} H{cx+9} L{cx+23} {cy-4} V{cy+25} H{cx-23} Z M{cx+9} {cy-18} V{cy-4} H{cx+23}" fill="none" stroke="{edge}" stroke-width="3" stroke-linejoin="round"/>')
        pieces.append(f'<path d="M{cx-12} {cy+7} H{cx+12} M{cx-12} {cy+17} H{cx+7}" stroke="{edge}" stroke-width="3" stroke-linecap="round"/>')
    elif icon == "language":
        pieces.append(f'<circle cx="{cx-17}" cy="{cy+2}" r="17" fill="none" stroke="{edge}" stroke-width="3"/><path d="M{cx-29} {cy+2} H{cx-5} M{cx-17} {cy-15} C{cx-7} {cy-5} {cx-7} {cy+9} {cx-17} {cy+19} M{cx-17} {cy-15} C{cx-27} {cy-5} {cx-27} {cy+9} {cx-17} {cy+19}" fill="none" stroke="{edge}" stroke-width="2"/>')
        pieces.append(f'<path d="M{cx+7} {cy+15} L{cx+18} {cy-14} L{cx+29} {cy+15} M{cx+11} {cy+5} H{cx+25}" fill="none" stroke="{edge}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
    elif icon == "rules":
        pieces.append(f'<rect x="{cx-26}" y="{cy-20}" width="52" height="38" rx="6" fill="none" stroke="{edge}" stroke-width="3"/><path d="M{cx-16} {cy-9} H{cx+16} M{cx-16} {cy+1} H{cx+9} M{cx-16} {cy+11} H{cx+2}" stroke="{edge}" stroke-width="3" stroke-linecap="round"/>')
    elif icon == "polish":
        pieces.append(f'<path d="M{cx-24} {cy+17} L{cx-6} {cy-1} M{cx-2} {cy-23} L{cx+19} {cy-2} M{cx+9} {cy-25} L{cx+26} {cy-8} L{cx+8} {cy+10} L{cx-9} {cy-7} Z" fill="none" stroke="{edge}" stroke-width="3" stroke-linejoin="round"/><path d="M{cx-27} {cy+24} H{cx+25}" stroke="{edge}" stroke-width="3" stroke-linecap="round"/>')
    elif icon == "output":
        pieces.append(f'<rect x="{cx-25}" y="{cy-20}" width="50" height="40" rx="6" fill="none" stroke="{edge}" stroke-width="3"/><path d="M{cx-14} {cy-8} H{cx+14} M{cx-14} {cy+3} H{cx+14} M{cx-14} {cy+14} H{cx+4}" stroke="{edge}" stroke-width="3" stroke-linecap="round"/><path d="M{cx+30} {cy-2} L{cx+42} {cy+10} L{cx+30} {cy+22}" fill="none" stroke="{edge}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
    pieces.append("</g>")
    return "".join(pieces)


def arrow(x1: int, y: int, x2: int, dashed: bool = False) -> str:
    dash = ' stroke-dasharray="8 7"' if dashed else ""
    return (
        f'<path d="M{x1} {y} H{x2}" fill="none" stroke="{COLORS["muted"]}" stroke-width="4" '
        f'stroke-linecap="round"{dash}/><path d="M{x2-12} {y-10} L{x2} {y} L{x2-12} {y+10}" '
        f'fill="none" stroke="{COLORS["muted"]}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
    )


def route_box(x: int, y: int, width: int, title: str, body: str, color: str) -> str:
    return (
        f'<g><rect x="{x}" y="{y}" width="{width}" height="116" rx="18" fill="{COLORS["white"]}" stroke="{color}" stroke-width="3"/>'
        f'<circle cx="{x+28}" cy="{y+30}" r="10" fill="{color}"/>'
        + text(x + 50, y + 37, title, 21, "700")
        + text(x + 24, y + 75, body, 17, "500")
        + '</g>'
    )


def build_svg() -> str:
    width, height = 1600, 900
    pieces = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<title>Daxuan Academic Polisher workflow</title>',
        '<desc>Source-language academic polishing workflow: detect Chinese or English, load the appropriate register, preserve evidence, and return polished prose with concise notes.</desc>',
        f'<rect width="{width}" height="{height}" fill="#F7FAFC"/>',
        f'<rect x="34" y="28" width="1532" height="844" rx="30" fill="{COLORS["white"]}" stroke="{COLORS["detail"]}" stroke-width="2"/>',
        text(78, 86, "Daxuan Academic Polisher", 38, "700"),
        text(78, 122, "Source language → evidence-preserving editorial pass", 22, "500", COLORS["muted"]),
        f'<rect x="1240" y="60" width="260" height="44" rx="22" fill="{COLORS["field"]}" stroke="{COLORS["detail"]}" stroke-width="2"/>',
        text(1370, 89, "DEFAULT: SAME LANGUAGE", 16, "700", COLORS["text"], "middle"),
    ]
    xs = [80, 380, 680, 980, 1280]
    titles = [
        ("输入草稿", "Input draft", "1", "document", False),
        ("语言路由", "Language route", "2", "language", False),
        ("加载规则", "Load register", "3", "rules", False),
        ("保真润色", "Polish + protect", "4", "polish", True),
        ("交付结果", "Return output", "5", "output", False),
    ]
    for x, (title, subtitle, number, icon, accent) in zip(xs, titles):
        pieces.append(card(x, 185, 240, 236, title, subtitle, number, icon, accent))
    for x1, x2 in zip([320, 620, 920, 1220], [360, 660, 960, 1260]):
        pieces.append(arrow(x1, 303, x2))
    # Route details below the language node and the register node.
    pieces.extend([
        text(80, 480, "路由与例外 / Routing and exceptions", 25, "700"),
        route_box(80, 514, 430, "中文稿 / Chinese", "→ references/zh-style.md", COLORS["outline"]),
        route_box(585, 514, 430, "英文稿 / English", "→ references/en-style.md", COLORS["outline"]),
        route_box(1090, 514, 430, "混合或不确定 / Mixed or unclear", "→ dominant language; ask when needed", COLORS["accent"]),
        f'<path d="M800 421 V468 H295 V514" fill="none" stroke="{COLORS["muted"]}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>',
        f'<path d="M800 468 H800 V514" fill="none" stroke="{COLORS["muted"]}" stroke-width="3" stroke-linecap="round"/>',
        f'<path d="M800 468 H1305 V514" fill="none" stroke="{COLORS["accent"]}" stroke-width="3" stroke-dasharray="8 7" stroke-linecap="round" stroke-linejoin="round"/>',
        text(80, 694, "受保护内容 / Protected evidence", 25, "700"),
        f'<rect x="80" y="720" width="1440" height="86" rx="18" fill="{COLORS["field"]}" stroke="{COLORS["detail"]}" stroke-width="2"/>',
        text(112, 773, "1,204   ·   p<0.001   ·   [12]   ·   DOI / PMID   ·   Figure 2   ·   rs12345", 24, "600", COLORS["text"]),
        text(80, 846, "正文先返回；最多五条真正需要核对的说明。无 API key、无自动写回、无隐式文献检索。", 18, "500", COLORS["muted"]),
        '</svg>',
    ])
    return "".join(pieces)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    output = OUT / "polishing-workflow.svg"
    output.write_text(build_svg(), encoding="utf-8")
    evidence = {
        "evidence_kind": "generated_workflow_diagram",
        "model_run": False,
        "artifact": str(output.relative_to(ROOT)),
        "palette_source": "Daxuan scientific-assets methodology-blue (adapted, self-contained)",
        "flow": ["input", "source-language routing", "register loading", "evidence-preserving polish", "body plus notes"],
    }
    (ROOT / "reports/showcase-evidence.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PASS workflow diagram generated")
    print("PASS", output)


if __name__ == "__main__":
    main()

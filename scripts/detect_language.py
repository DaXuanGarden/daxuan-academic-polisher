#!/usr/bin/env python3
"""Estimate the dominant prose language of a manuscript passage.

The result is a routing signal, not a translation decision or a semantic classifier.
Technical tokens are masked before counting so identifiers and citations do not make an
otherwise Chinese passage look English.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

HAN_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
WORD_RE = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)*")
CODE_RE = re.compile(r"```.*?```|`[^`]*`", re.DOTALL)
URL_RE = re.compile(r"(?:https?://|www\.)\S+|\b\S+@\S+\b")
PATH_RE = re.compile(r"(?:^|\s)(?:[/~]|[A-Za-z]:\\)[^\s]+")
DOI_RE = re.compile(r"\b(?:doi\s*:\s*|pmid\s*[:#]?\s*)\S+", re.I)
CITATION_RE = re.compile(r"\[(?:[^\]]*\d[^\]]*)\]|\([^()]{0,80}(?:19|20)\d{2}[a-z]?[^()]*\)")
MATH_RE = re.compile(r"\$\$.*?\$\$|\$[^$\n]+\$|\\\(.+?\\\)|\\\[.+?\\\]", re.DOTALL)
ID_RE = re.compile(r"\b(?:rs\d+|[A-Z]{2,}[A-Z0-9_-]*\d[A-Z0-9_-]*|[A-Z]{2,}(?:[-_][A-Za-z0-9]+)+)\b")


def mask_nonprose(text: str) -> str:
    masked = CODE_RE.sub(" ", text)
    masked = URL_RE.sub(" ", masked)
    masked = DOI_RE.sub(" ", masked)
    masked = PATH_RE.sub(" ", masked)
    masked = CITATION_RE.sub(" ", masked)
    masked = MATH_RE.sub(" ", masked)
    masked = ID_RE.sub(" ", masked)
    return masked


def detect(text: str) -> dict[str, object]:
    source = mask_nonprose(text)
    han = len(HAN_RE.findall(source))
    words = [m.group(0) for m in WORD_RE.finditer(source)]
    prose_words = [w for w in words if len(re.sub(r"[^A-Za-z]", "", w)) >= 2 and any(c.islower() for c in w)]
    latin_letters = sum(len(re.sub(r"[^A-Za-z]", "", w)) for w in prose_words)
    english_words = len(prose_words)
    total = han + latin_letters
    if total < 12 or (han < 6 and english_words < 3):
        language, confidence = "und", 0.0
    else:
        han_ratio = han / total
        if han >= 20 and han_ratio >= 0.60 and latin_letters <= han * 0.55:
            language = "zh"
            confidence = han_ratio
        elif han >= 8 and english_words <= 3 and latin_letters <= han * 1.5:
            # Short English technical phrases inside a Chinese sentence are local terms,
            # not evidence that the whole passage should route to English.
            language = "zh"
            confidence = han / total
        elif latin_letters >= 20 and han_ratio <= 0.25 and english_words >= 4:
            language = "en"
            confidence = 1 - han_ratio
        elif han >= 8 and latin_letters >= 8 and 0.35 <= han_ratio <= 0.65:
            language = "mixed"
            confidence = 1 - abs(han_ratio - 0.5) * 2
        elif han > latin_letters * 1.35 and han >= 10:
            language = "zh"
            confidence = han / total
        elif latin_letters > han * 1.35 and latin_letters >= 10 and english_words >= 3:
            language = "en"
            confidence = latin_letters / total
        else:
            language, confidence = "mixed", 0.0
    return {
        "language": language,
        "confidence": round(float(confidence), 3),
        "han_chars": han,
        "latin_letters": latin_letters,
        "english_words": english_words,
        "masked_nonprose": len(text) - len(source),
        "note": "heuristic signal; inspect short, technical, or bilingual passages manually",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--text", help="Passage to inspect.")
    source.add_argument("--file", type=Path, help="UTF-8 text file to inspect.")
    args = parser.parse_args()
    value = args.text if args.text is not None else args.file.read_text(encoding="utf-8")
    print(json.dumps(detect(value), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

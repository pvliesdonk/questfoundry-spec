"""
STATUS: SCAFFOLD
Performs a simple reference check in prompt Markdown files:
- Extracts file-like paths under References sections
- Verifies they exist relative to repo root
"""

from __future__ import annotations

import re
from pathlib import Path


def extract_paths(text: str) -> set[str]:
    # Match paths like 00-north-star/..., 01-roles/..., 02-dictionary/..., 03-schemas/..., 04-protocol/... or 05-prompts/...
    pattern = re.compile(r"(?P<path>(?:0[0-5]-[a-z\-]+|04-protocol|05-prompts|03-schemas|02-dictionary|01-roles|00-north-star)/[\w\-./]+\.(?:md|json))")
    return set(m.group("path") for m in pattern.finditer(text))


def test_references_exist():
    repo_root = Path(__file__).resolve().parents[3]
    md_files = list((repo_root / "05-prompts").rglob("*.md"))
    missing: list[str] = []
    for md in md_files:
        text = md.read_text(encoding="utf-8", errors="ignore")
        for p in extract_paths(text):
            if not (repo_root / p).exists():
                missing.append(f"{md}: references missing path {p}")
    assert not missing, "\n" + "\n".join(missing)

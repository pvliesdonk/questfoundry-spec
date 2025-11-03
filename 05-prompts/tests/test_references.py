"""
STATUS: SCAFFOLD
Performs reference checks in prompt Markdown files:
- Extract file-like references (optionally with anchors: path.md#anchor)
- Verify files exist relative to repo root
- If anchor present, verify a matching heading anchor exists (heuristic)
"""

from __future__ import annotations

import re
from pathlib import Path

def extract_refs(text: str) -> set[tuple[str, str | None]]:
    # Match paths like 00-north-star/..., 01-roles/..., 02-dictionary/..., 03-schemas/..., 04-protocol/... or 05-prompts/...
    # Optionally followed by #anchor
    pattern = re.compile(
        r"(?P<path>(?:0[0-5]-[a-z\-]+|04-protocol|05-prompts|03-schemas|02-dictionary|01-roles|00-north-star)/[\w\-./]+\.(?:md|json))(?:#(?P<anchor>[A-Za-z0-9_\-]+))?"
    )
    refs: set[tuple[str, str | None]] = set()
    for m in pattern.finditer(text):
        refs.add((m.group("path"), m.group("anchor")))
    return refs


def _slugify_heading(line: str) -> str:
    # Strip heading markers and make a simple GitHub-like slug
    h = line.lstrip("# ").strip().lower()
    # Keep alphanumerics, spaces, and hyphens, convert spaces to hyphens
    filtered = []
    for ch in h:
        if ch.isalnum() or ch in {" ", "-", "_"}:
            filtered.append(ch)
    slug = "".join(filtered).replace(" ", "-")
    # Collapse multiple '-'
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug


def test_references_exist():
    repo_root = Path(__file__).resolve().parents[3]
    md_files = list((repo_root / "05-prompts").rglob("*.md"))
    missing: list[str] = []
    for md in md_files:
        text = md.read_text(encoding="utf-8", errors="ignore")
        for p, anchor in extract_refs(text):
            target_path = repo_root / p
            if not target_path.exists():
                missing.append(f"{md}: references missing path {p}")
                continue
            if anchor and target_path.suffix.lower() == ".md":
                try:
                    t = target_path.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    missing.append(f"{md}: cannot read {p} to verify anchor #{anchor}")
                    continue
                anchors = {
                    _slugify_heading(line)
                    for line in t.splitlines()
                    if line.lstrip().startswith("#")
                }
                if anchor not in anchors:
                    missing.append(f"{md}: anchor not found {p}#{anchor}")
    assert not missing, "\n" + "\n".join(missing)

#!/usr/bin/env python3
"""Lint prompt placeholders to ensure global parameters stay in sync."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Iterable, List, Set, Tuple

PROMPTS_ROOT = Path("prompts")
GLOBAL_PROMPT = PROMPTS_ROOT / "00_orchestrator_conductor.txt"
PLACEHOLDER_PATTERN = re.compile(r"{{\s*([^{}]+?)\s*}}")
UPPER_PATTERN = re.compile(r"^[A-Z0-9_]+$")


def extract_placeholders(text: str) -> Set[str]:
    return {match.group(1) for match in PLACEHOLDER_PATTERN.finditer(text)}


def collect_global_placeholders() -> Set[str]:
    if not GLOBAL_PROMPT.exists():
        raise FileNotFoundError(f"Global prompt not found: {GLOBAL_PROMPT}")

    text = GLOBAL_PROMPT.read_text(encoding="utf-8")
    lines = text.splitlines()
    try:
        start = lines.index("Global parameters (apply to all phases):") + 1
    except ValueError as exc:
        raise RuntimeError("Global parameters section not found in orchestrator prompt") from exc

    allowed: Set[str] = set()
    for line in lines[start:]:
        if not line.strip():
            break
        allowed.update(
            placeholder
            for placeholder in extract_placeholders(line)
            if UPPER_PATTERN.match(placeholder)
        )
    return allowed


def lint_prompts(extra_dirs: Iterable[Path]) -> Tuple[List[str], List[str]]:
    allowed = collect_global_placeholders()
    errors: List[str] = []
    notes: List[str] = []

    prompt_files = [path for path in PROMPTS_ROOT.glob("**/*") if path.is_file()]
    prompt_files += [
        path for directory in extra_dirs for path in directory.glob("**/*") if path.is_file()
    ]

    for prompt in prompt_files:
        text = prompt.read_text(encoding="utf-8")
        for placeholder in extract_placeholders(text):
            if not UPPER_PATTERN.match(placeholder):
                # Lower-case placeholders are section-specific templates – informational only.
                continue
            if placeholder not in allowed:
                errors.append(f"{prompt}: placeholder '{{{{{placeholder}}}}}' missing from Global parameters")

    unused = allowed.copy()
    for prompt in prompt_files:
        text = prompt.read_text(encoding="utf-8")
        for placeholder in extract_placeholders(text):
            if placeholder in unused:
                unused.discard(placeholder)

    if unused:
        notes.append(
            "Global parameters defined but unused in prompts: "
            + ", ".join(sorted(unused))
        )

    return errors, notes


def main(argv: Iterable[str] | None = None) -> int:
    # Allow callers to pass extra prompt roots (e.g., releases/*/prompts)
    extra_dirs = [Path(arg) for arg in sys.argv[1:]]
    errors, notes = lint_prompts(extra_dirs)

    for note in notes:
        print(f"NOTE: {note}", file=sys.stderr)
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        return 1
    print("Prompt placeholder lint: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())

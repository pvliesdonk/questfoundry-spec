"""
STATUS: SCAFFOLD
Basic coverage checks per role directory in 05-prompts:
- system_prompt.md must exist
- at least one handler/procedure directory contains content (.md)
- at least one example JSON exists

Notes:
- Gatekeeper uses quality_bars/ as its procedure directory.
- This test is intentionally lenient about example counts; it reports a warning
  if a role has fewer than 2 examples but does not fail on that basis yet.
"""

from __future__ import annotations

from pathlib import Path


def _role_dirs(base: Path) -> list[Path]:
    out: list[Path] = []
    for p in (base / "05-prompts").iterdir():
        if not p.is_dir():
            continue
        if p.name in {"_shared", "tests"}:
            continue
        out.append(p)
    return sorted(out, key=lambda p: p.name)


def test_role_minimum_coverage():
    repo_root = Path(__file__).resolve().parents[3]
    roles = _role_dirs(repo_root)
    missing: list[str] = []
    warnings: list[str] = []

    for role in roles:
        # system_prompt.md
        if not (role / "system_prompt.md").exists():
            missing.append(f"{role}: missing system_prompt.md")

        # handlers/procedures presence
        handler_globs = [
            role / "intent_handlers",
            role / "procedures",
            role / "quality_bars",  # for Gatekeeper
        ]
        has_handler = False
        for hg in handler_globs:
            if hg.is_dir() and any(hg.glob("*.md")):
                has_handler = True
                break
        if not has_handler:
            missing.append(f"{role}: no handlers/procedures found (intent_handlers/ or procedures/ or quality_bars/)")

        # examples presence
        ex_dir = role / "examples"
        ex_cnt = len(list(ex_dir.glob("*.json"))) if ex_dir.exists() else 0
        if ex_cnt < 1:
            missing.append(f"{role}: has {ex_cnt} examples; expected at least 1")
        elif ex_cnt < 2:
            warnings.append(f"{role}: only {ex_cnt} example(s); consider adding one more")

    if warnings:
        # Print warnings for visibility in CI logs without failing test
        print("\nCoverage warnings:")
        for w in warnings:
            print(f" - {w}")

    assert not missing, "\n" + "\n".join(missing)

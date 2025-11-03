"""
STATUS: SCAFFOLD
Validates minimal Layer 3 instances while scaffolding proceeds.

Current checks:
- Validate example instances against Layer 3 schemas: codex_entry, edit_notes.
Future:
- Validate envelopes in examples; intent coverage; reference checks.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
TOOLS_SRC = REPO_ROOT / "tools" / "src"
sys.path.insert(0, str(TOOLS_SRC))

from questfoundry_spec_tools.instance_validator import validate_instance, find_schema_file  # type: ignore


def validate_instance_file(schema_name: str, instance_path: Path) -> tuple[bool, str]:
    schema_path = find_schema_file(REPO_ROOT, schema_name)
    if not schema_path:
        return False, f"Schema not found for {schema_name}"
    return validate_instance(schema_path, instance_path)


def main() -> int:
    fixtures = {
        "codex_entry": REPO_ROOT / "05-prompts" / "tests" / "fixtures" / "codex_entry.example.json",
        "edit_notes": REPO_ROOT / "05-prompts" / "tests" / "fixtures" / "edit_notes.example.json",
    }
    failures: list[str] = []

    for name, path in fixtures.items():
        ok, msg = validate_instance_file(name, path)
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {name}: {path}")
        if not ok:
            failures.append(f"{name}: {msg}")

    if failures:
        print("\nValidation failures:")
        for f in failures:
            print(f" - {f}")
        return 1

    print("All instance validations passed (scaffold).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

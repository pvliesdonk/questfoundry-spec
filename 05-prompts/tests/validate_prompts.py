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

REPO_ROOT = Path(__file__).resolve().parents[2]
TOOLS_SRC = REPO_ROOT / "tools" / "src"
sys.path.insert(0, str(TOOLS_SRC))

from questfoundry_spec_tools.instance_validator import (
    validate_instance,
    find_schema_file,
    validate_envelope,
)  # type: ignore


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

    # Validate envelope examples under 05-prompts/**/examples/*.json
    example_files = list((REPO_ROOT / "05-prompts").rglob("examples/*.json"))
    for ex in example_files:
        try:
            obj = json.loads(ex.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            failures.append(f"{ex}: invalid JSON: {e}")
            continue
        def _structure_only(envelope: dict) -> tuple[bool, str]:
            # Force payload.type to 'none' to skip payload.data validation (structure-only pass)
            env2 = dict(envelope)
            payload = dict(env2.get("payload", {}))
            payload["type"] = "none"
            payload.setdefault("data", {})
            env2["payload"] = payload
            from tempfile import NamedTemporaryFile

            with NamedTemporaryFile("w", delete=False, suffix=".json", encoding="utf-8") as tf:
                json.dump(env2, tf)
                temp_path = Path(tf.name)
            ok_, msg_ = validate_envelope(temp_path, REPO_ROOT)
            temp_path.unlink(missing_ok=True)
            return ok_, msg_

        if isinstance(obj, list):
            for idx, env in enumerate(obj):
                ok, msg = _structure_only(env)
                status = "PASS" if ok else "FAIL"
                print(f"[{status}] envelope: {ex} [#{idx}]")
                if not ok:
                    failures.append(f"{ex} [#{idx}]: {msg}")
        elif isinstance(obj, dict):
            ok, msg = _structure_only(obj)
            status = "PASS" if ok else "FAIL"
            print(f"[{status}] envelope: {ex}")
            if not ok:
                failures.append(f"{ex}: {msg}")
        else:
            failures.append(f"{ex}: JSON must be object or array of objects")

    if failures:
        print("\nValidation failures:")
        for f in failures:
            print(f" - {f}")
        return 1

    print("All instance validations passed (scaffold).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

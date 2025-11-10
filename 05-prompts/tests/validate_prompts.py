"""
Validates Layer 3 instances and Layer 4 envelopes.

Checks:
- Validate example instances against Layer 3 schemas: codex_entry, edit_notes.
- Validate envelopes in examples under structure-only mode (skip payload.data).
- Whitelisted strict examples run full payload validation (envelope + payload).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parents[2]
TOOLS_SRC = REPO_ROOT / "spec-tools" / "src"
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
    # Whitelist examples for FULL payload validation (strict mode)
    # Use paths relative to the repo root
    strict_examples: set[Path] = {
        REPO_ROOT / "05-prompts" / "gatekeeper" / "examples" / "pre_gate_strict.json",
        REPO_ROOT / "05-prompts" / "gatekeeper" / "examples" / "final_decision_strict.json",
        REPO_ROOT / "05-prompts" / "book_binder" / "examples" / "view_request_strict.json",
        REPO_ROOT / "05-prompts" / "book_binder" / "examples" / "view_result_strict.json",
        # Optional: keep these structure-only unless later promoted to strict
    }

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

        def _full_validate(envelope: dict) -> tuple[bool, str]:
            # Validate envelope as-is (includes payload.data against Layer 3 schema)
            from tempfile import NamedTemporaryFile

            with NamedTemporaryFile("w", delete=False, suffix=".json", encoding="utf-8") as tf:
                json.dump(envelope, tf)
                temp_path = Path(tf.name)
            ok_, msg_ = validate_envelope(temp_path, REPO_ROOT)
            temp_path.unlink(missing_ok=True)
            return ok_, msg_

        def _validate_sequence(envelopes: Iterable[dict], strict: bool, label: str) -> None:
            for idx, env in enumerate(envelopes):
                ok, msg = (_full_validate(env) if strict else _structure_only(env))
                status = "PASS" if ok else "FAIL"
                print(f"[{status}] envelope: {label} [#{idx}]")
                if not ok:
                    failures.append(f"{label} [#{idx}]: {msg}")

        strict_mode = ex in strict_examples
        if isinstance(obj, list):
            _validate_sequence(obj, strict_mode, str(ex))
        elif isinstance(obj, dict):
            # Check if this is a documentation wrapper (loop flow format)
            if "messages" in obj and isinstance(obj.get("messages"), list):
                # Extract envelopes from messages[].envelope
                envelopes = []
                for msg in obj["messages"]:
                    if isinstance(msg, dict) and "envelope" in msg:
                        envelopes.append(msg["envelope"])
                if envelopes:
                    _validate_sequence(envelopes, strict_mode, str(ex))
                else:
                    failures.append(f"{ex}: messages array found but no envelopes extracted")
            else:
                # Regular envelope validation
                ok, msg = (_full_validate(obj) if strict_mode else _structure_only(obj))
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

    print("All instance & envelope validations passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""
Instance validation logic for QuestFoundry specification.
Validates artifact instances against their schemas.
"""

import json
from pathlib import Path
from typing import Tuple

try:
    import jsonschema
    from jsonschema import Draft202012Validator
except ImportError as e:
    raise ImportError(
        "jsonschema library is required. Install with: uv sync"
    ) from e


def list_available_schemas(base_dir: Path, layer: str = "03-schemas") -> list[str]:
    """
    List all available schema names in a layer.

    Args:
        base_dir: Repository root directory
        layer: Layer directory name (e.g., "03-schemas")

    Returns:
        Sorted list of schema names (without .schema.json suffix)
    """
    layer_dir = base_dir / layer
    if not layer_dir.exists():
        return []

    schemas = []
    for schema_file in sorted(layer_dir.glob("*.schema.json")):
        schema_name = schema_file.stem.replace(".schema", "")
        schemas.append(schema_name)
    return schemas


def find_schema_file(base_dir: Path, schema_name: str, layer: str = "03-schemas") -> Path | None:
    """
    Find the schema file for a given schema name.

    Args:
        base_dir: Repository root directory
        schema_name: Schema name (e.g., "hook_card")
        layer: Layer directory name (e.g., "03-schemas")

    Returns:
        Path to schema file if found, None otherwise
    """
    schema_path = base_dir / layer / f"{schema_name}.schema.json"
    return schema_path if schema_path.exists() else None


def validate_instance(schema_path: Path, instance_path: Path) -> Tuple[bool, str]:
    """
    Validate an instance file against a schema.

    Args:
        schema_path: Path to the schema file
        instance_path: Path to the instance file

    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if instance is valid, False otherwise
        - error_message: Empty string if valid, error description if invalid
    """
    try:
        # Load schema
        with open(schema_path, 'r') as f:
            schema = json.load(f)

        # Load instance
        with open(instance_path, 'r') as f:
            instance = json.load(f)

        # Validate
        validator = Draft202012Validator(schema)
        validator.validate(instance)

        return True, ""
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    except jsonschema.ValidationError as e:
        # Format the error message nicely with path
        error_path = " -> ".join(str(p) for p in e.path) if e.path else "root"
        return False, f"Validation error at '{error_path}': {e.message}"
    except Exception as e:
        return False, f"Unexpected error: {e}"


def validate_instances(schema_path: Path, instance_paths: list[Path]) -> dict:
    """
    Validate multiple instances against a schema.

    Args:
        schema_path: Path to the schema file
        instance_paths: List of paths to instance files

    Returns:
        Dictionary with validation results:
        {
            "schema": str,
            "total": int,
            "passed": int,
            "failed": int,
            "errors": [(filename, error_message), ...]
        }
    """
    results = {
        "schema": schema_path.stem.replace(".schema", ""),
        "total": len(instance_paths),
        "passed": 0,
        "failed": 0,
        "errors": []
    }

    for instance_path in instance_paths:
        if not instance_path.exists():
            results["failed"] += 1
            results["errors"].append((instance_path.name, "File not found"))
            continue

        is_valid, error_msg = validate_instance(schema_path, instance_path)

        if is_valid:
            results["passed"] += 1
        else:
            results["failed"] += 1
            results["errors"].append((instance_path.name, error_msg))

    return results


def validate_envelope(envelope_path: Path, base_dir: Path) -> Tuple[bool, str]:
    """
    Validate an envelope file using two-pass validation:
    - Pass 1: Validate envelope structure against envelope.schema.json (Layer 4)
    - Pass 2: Validate payload.data against Layer 3 schema based on payload.type

    Args:
        envelope_path: Path to the envelope JSON file
        base_dir: Repository root directory

    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if both passes succeed, False otherwise
        - error_message: Empty string if valid, error description if invalid
    """
    try:
        # Load envelope
        with open(envelope_path, 'r') as f:
            envelope = json.load(f)

        # === PASS 1: Validate envelope structure ===
        envelope_schema_path = base_dir / "04-protocol" / "envelope.schema.json"
        if not envelope_schema_path.exists():
            return False, "Envelope schema not found at 04-protocol/envelope.schema.json"

        with open(envelope_schema_path, 'r') as f:
            envelope_schema = json.load(f)

        # Validate entire envelope against envelope.schema.json
        # No RefResolver needed - envelope schema now has no $ref to Layer 3
        validator = Draft202012Validator(envelope_schema)

        envelope_errors = list(validator.iter_errors(envelope))
        if envelope_errors:
            error_msgs = []
            for error in envelope_errors:
                error_path = " -> ".join(str(p) for p in error.path) if error.path else "root"
                error_msgs.append(f"{error_path}: {error.message}")
            return False, f"Envelope validation errors (Pass 1):\n  " + "\n  ".join(error_msgs)

        # === PASS 2: Validate payload data against Layer 3 schema ===
        payload = envelope.get("payload", {})
        payload_type = payload.get("type")

        # Skip payload validation if type is "none" or missing
        if not payload_type or payload_type == "none":
            return True, ""

        payload_data = payload.get("data", {})

        # Find corresponding Layer 3 schema
        layer3_schema_path = base_dir / "03-schemas" / f"{payload_type}.schema.json"
        if not layer3_schema_path.exists():
            return False, f"Layer 3 schema not found: 03-schemas/{payload_type}.schema.json"

        with open(layer3_schema_path, 'r') as f:
            layer3_schema = json.load(f)

        # Validate only payload.data against Layer 3 schema
        payload_validator = Draft202012Validator(layer3_schema)
        payload_errors = list(payload_validator.iter_errors(payload_data))

        if payload_errors:
            error_msgs = []
            for error in payload_errors:
                error_path = " -> ".join(str(p) for p in error.path) if error.path else "payload.data"
                error_msgs.append(f"{error_path}: {error.message}")
            return False, f"Payload validation errors (Pass 2, type: {payload_type}):\n  " + "\n  ".join(error_msgs)

        return True, ""

    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    except FileNotFoundError as e:
        return False, f"File not found: {e}"
    except Exception as e:
        return False, f"Unexpected error: {e}"

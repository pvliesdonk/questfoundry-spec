"""
Schema validation logic for QuestFoundry specification.
Validates that schemas comply with JSON Schema Draft 2020-12.
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


def validate_schema_file(schema_path: Path) -> Tuple[bool, str]:
    """
    Validate a single schema file against JSON Schema Draft 2020-12.

    Args:
        schema_path: Path to the schema file

    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if schema is valid, False otherwise
        - error_message: Empty string if valid, error description if invalid
    """
    try:
        with open(schema_path, 'r') as f:
            schema = json.load(f)

        # Check against the meta-schema
        Draft202012Validator.check_schema(schema)

        return True, ""
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    except jsonschema.SchemaError as e:
        return False, f"Schema validation error: {e.message}"
    except Exception as e:
        return False, f"Unexpected error: {e}"


def find_schema_files(base_dir: Path, layer: str = "03-schemas") -> list[Path]:
    """
    Find all schema files in a layer directory.

    Args:
        base_dir: Repository root directory
        layer: Layer directory name (e.g., "03-schemas", "04-transforms")

    Returns:
        Sorted list of schema file paths
    """
    layer_dir = base_dir / layer
    if not layer_dir.exists():
        return []

    return sorted(layer_dir.glob("*.schema.json"))


def validate_all_schemas(base_dir: Path, layers: list[str] = None) -> dict:
    """
    Validate all schemas in specified layers.

    Args:
        base_dir: Repository root directory
        layers: List of layer directories to validate (defaults to ["03-schemas"])

    Returns:
        Dictionary with validation results:
        {
            "total": int,
            "passed": int,
            "failed": int,
            "errors": [(filename, error_message), ...]
        }
    """
    if layers is None:
        layers = ["03-schemas"]

    results = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "errors": []
    }

    for layer in layers:
        schema_files = find_schema_files(base_dir, layer)

        for schema_file in schema_files:
            results["total"] += 1
            is_valid, error_msg = validate_schema_file(schema_file)

            if is_valid:
                results["passed"] += 1
            else:
                results["failed"] += 1
                results["errors"].append((schema_file.name, error_msg))

    return results

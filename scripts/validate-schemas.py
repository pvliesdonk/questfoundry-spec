#!/usr/bin/env python3
"""
Validate all Layer 3 (and optionally Layer 4) schemas against JSON Schema Draft 2020-12
Uses jsonschema library with bundled meta-schemas (no network required)
"""

import json
import sys
from pathlib import Path
from typing import List, Tuple

try:
    import jsonschema
    from jsonschema import Draft202012Validator
except ImportError:
    print("Error: jsonschema library is not installed")
    print("Install with: pip install jsonschema")
    sys.exit(1)

# ANSI color codes
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
NC = '\033[0m'  # No Color


def validate_schema_file(schema_path: Path) -> Tuple[bool, str]:
    """
    Validate a single schema file against JSON Schema Draft 2020-12

    Returns: (is_valid, error_message)
    """
    try:
        with open(schema_path, 'r') as f:
            schema = json.load(f)

        # Check the meta-schema
        Draft202012Validator.check_schema(schema)

        return True, ""
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    except jsonschema.SchemaError as e:
        return False, f"Schema validation error: {e.message}"
    except Exception as e:
        return False, f"Unexpected error: {e}"


def main():
    print("=== QuestFoundry Schema Validator ===")
    print("")

    # Validate Layer 3 schemas
    print("Validating Layer 3 schemas...")
    layer3_dir = Path("03-schemas")

    if not layer3_dir.exists():
        print(f"{RED}Error: {layer3_dir} directory not found{NC}")
        sys.exit(1)

    schema_files = sorted(layer3_dir.glob("*.schema.json"))

    if not schema_files:
        print(f"{YELLOW}Warning: No schema files found in {layer3_dir}{NC}")

    errors = []

    for schema_file in schema_files:
        print(f"  Checking {schema_file.name}... ", end="", flush=True)
        is_valid, error_msg = validate_schema_file(schema_file)

        if is_valid:
            print(f"{GREEN}✓{NC}")
        else:
            print(f"{RED}✗{NC}")
            errors.append((schema_file.name, error_msg))

    # Future: Add Layer 4 validation when ready
    # print("")
    # print("Validating Layer 4 schemas...")
    # ...

    # Summary
    print("")
    print("=== Validation Summary ===")

    if not errors:
        print(f"{GREEN}All schemas are valid JSON Schema Draft 2020-12!{NC}")
        return 0
    else:
        print(f"{RED}Found {len(errors)} invalid schema(s):{NC}")
        print("")
        for schema_name, error_msg in errors:
            print(f"  {RED}✗{NC} {schema_name}")
            print(f"    {error_msg}")
            print("")
        return 1


if __name__ == "__main__":
    sys.exit(main())

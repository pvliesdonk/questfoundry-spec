#!/usr/bin/env python3
"""
Validate artifact instances against their JSON schemas
Uses jsonschema library (no network required)
"""

import json
import sys
from pathlib import Path
from typing import List

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


def list_available_schemas() -> List[str]:
    """List all available schema names"""
    layer3_dir = Path("03-schemas")
    if not layer3_dir.exists():
        return []

    schemas = []
    for schema_file in sorted(layer3_dir.glob("*.schema.json")):
        schema_name = schema_file.stem.replace(".schema", "")
        schemas.append(schema_name)
    return schemas


def validate_instance(schema_path: Path, instance_path: Path) -> tuple[bool, str]:
    """
    Validate an instance against a schema

    Returns: (is_valid, error_message)
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
        # Format the error message nicely
        error_path = " -> ".join(str(p) for p in e.path) if e.path else "root"
        return False, f"Validation error at '{error_path}': {e.message}"
    except Exception as e:
        return False, f"Unexpected error: {e}"


def usage():
    """Print usage information"""
    print("Usage: validate-instance.py <schema-name> <instance-file> [instance-file2 ...]")
    print("")
    print("Validates artifact instance(s) against a Layer 3 schema")
    print("")
    print("Examples:")
    print("  validate-instance.py hook_card my-hook.json")
    print("  validate-instance.py gatecheck_report report1.json report2.json")
    print("  validate-instance.py view_log logs/*.json")
    print("")

    schemas = list_available_schemas()
    if schemas:
        print("Available schemas:")
        for schema in schemas:
            print(f"  - {schema}")
    else:
        print("No schemas found in 03-schemas/")


def main():
    # Check arguments
    if len(sys.argv) < 3:
        usage()
        return 1

    schema_name = sys.argv[1]
    instance_files = sys.argv[2:]

    # Locate schema file
    schema_path = Path(f"03-schemas/{schema_name}.schema.json")

    if not schema_path.exists():
        print(f"{RED}Error: Schema not found: {schema_path}{NC}")
        print("")
        schemas = list_available_schemas()
        if schemas:
            print("Available schemas:")
            for schema in schemas:
                print(f"  - {schema}")
        return 1

    # Validate each instance
    print("=== QuestFoundry Instance Validator ===")
    print(f"Schema: {schema_name}")
    print("")

    total = 0
    errors = 0

    for instance_file in instance_files:
        instance_path = Path(instance_file)

        if not instance_path.exists():
            print(f"{RED}✗{NC} {instance_path.name} - File not found")
            errors += 1
            total += 1
            continue

        total += 1
        print(f"Validating {instance_path.name}... ", end="", flush=True)

        is_valid, error_msg = validate_instance(schema_path, instance_path)

        if is_valid:
            print(f"{GREEN}✓{NC}")
        else:
            print(f"{RED}✗{NC}")
            print(f"  {error_msg}")
            print("")
            errors += 1

    # Summary
    print("")
    print("=== Validation Summary ===")
    print(f"Total: {total}")
    print(f"Passed: {GREEN}{total - errors}{NC}")

    if errors == 0:
        print(f"{GREEN}All instances are valid!{NC}")
        return 0
    else:
        print(f"Failed: {RED}{errors}{NC}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

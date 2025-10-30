"""
CLI entry points for QuestFoundry specification tools.
"""

import sys
from pathlib import Path

from .schema_validator import find_schema_files, validate_schema_file
from .instance_validator import (
    list_available_schemas,
    find_schema_file,
    validate_instance,
)

# ANSI color codes
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
NC = '\033[0m'  # No Color


def find_repo_root() -> Path:
    """
    Find the QuestFoundry repository root.
    Assumes tools/ is in the repo root.
    """
    # When running as installed package, start from current directory
    current = Path.cwd()

    # Walk up to find directory with 03-schemas/
    for parent in [current, *current.parents]:
        if (parent / "03-schemas").exists():
            return parent

    # Fallback: assume we're in tools/ directory
    tools_dir = Path(__file__).parent.parent.parent
    repo_root = tools_dir.parent
    if (repo_root / "03-schemas").exists():
        return repo_root

    # Last resort: current directory
    return current


def validate_schemas_cli():
    """
    CLI entry point for qfspec-validate command.
    Validates all schemas in the repository.
    """
    repo_root = find_repo_root()

    print("=== QuestFoundry Spec: Schema Validator ===")
    print(f"Repository: {repo_root}")
    print("")

    # Validate Layer 3 schemas
    print("Validating Layer 3 schemas...")
    layer3_dir = repo_root / "03-schemas"

    if not layer3_dir.exists():
        print(f"{RED}Error: {layer3_dir} directory not found{NC}")
        print(f"Run from repository root or ensure 03-schemas/ exists")
        sys.exit(1)

    schema_files = find_schema_files(repo_root, "03-schemas")

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
        sys.exit(0)
    else:
        print(f"{RED}Found {len(errors)} invalid schema(s):{NC}")
        print("")
        for schema_name, error_msg in errors:
            print(f"  {RED}✗{NC} {schema_name}")
            print(f"    {error_msg}")
            print("")
        sys.exit(1)


def validate_instance_cli():
    """
    CLI entry point for qfspec-check-instance command.
    Validates instance files against a schema.
    """
    repo_root = find_repo_root()

    # Check arguments
    if len(sys.argv) < 3:
        print("Usage: qfspec-check-instance <schema-name> <instance-file> [instance-file2 ...]")
        print("")
        print("Validates artifact instance(s) against a QuestFoundry schema")
        print("")
        print("Examples:")
        print("  qfspec-check-instance hook_card my-hook.json")
        print("  qfspec-check-instance gatecheck_report report1.json report2.json")
        print("  qfspec-check-instance view_log logs/*.json")
        print("")

        schemas = list_available_schemas(repo_root)
        if schemas:
            print("Available schemas:")
            for schema in schemas:
                print(f"  - {schema}")
        else:
            print(f"No schemas found in {repo_root / '03-schemas'}")

        sys.exit(1)

    schema_name = sys.argv[1]
    instance_files = sys.argv[2:]

    # Locate schema file
    schema_path = find_schema_file(repo_root, schema_name)

    if not schema_path:
        print(f"{RED}Error: Schema not found: {schema_name}{NC}")
        print("")
        schemas = list_available_schemas(repo_root)
        if schemas:
            print("Available schemas:")
            for schema in schemas:
                print(f"  - {schema}")
        sys.exit(1)

    # Validate each instance
    print("=== QuestFoundry Spec: Instance Validator ===")
    print(f"Repository: {repo_root}")
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
        sys.exit(0)
    else:
        print(f"Failed: {RED}{errors}{NC}")
        sys.exit(1)

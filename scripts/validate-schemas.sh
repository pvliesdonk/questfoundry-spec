#!/usr/bin/env bash
# Validate all Layer 3 (and optionally Layer 4) schemas against JSON Schema Draft 2020-12
# Bash wrapper that calls the Python validator

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Call the Python validator
python3 "$SCRIPT_DIR/validate-schemas.py" "$@"

#!/usr/bin/env bash
# Validate artifact instances against their JSON schemas
# Bash wrapper that calls the Python validator

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Call the Python validator
python3 "$SCRIPT_DIR/validate-instance.py" "$@"

#!/usr/bin/env bash
#
# validate-examples.sh
#
# Validates all Layer 4 envelope examples against envelope.schema.json and their payloads
# against Layer 3 schemas.
#
# Usage:
#   ./scripts/validate-examples.sh
#   ./scripts/validate-examples.sh 04-protocol/EXAMPLES/hook.create.json
#
# Exit code 0 on success, 1 on failure

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Find repository root (directory containing this script's parent)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=== QuestFoundry: Validate Layer 4 Envelope Examples ==="
echo "Repository: $REPO_ROOT"
echo ""

# Check if tools are available
if ! command -v uv &> /dev/null; then
    echo -e "${RED}Error: 'uv' command not found${NC}"
    echo "Please install uv: https://github.com/astral-sh/uv"
    exit 1
fi

# Check if tools package is set up
if [ ! -d "$REPO_ROOT/tools" ]; then
    echo -e "${RED}Error: tools/ directory not found${NC}"
    echo "Please ensure you're running from the repository root"
    exit 1
fi

# Set up tools if needed
echo "Setting up validation tools..."
cd "$REPO_ROOT/tools"
uv sync --quiet || {
    echo -e "${RED}Failed to set up validation tools${NC}"
    exit 1
}
echo ""

# Determine which files to validate
cd "$REPO_ROOT"
if [ $# -eq 0 ]; then
    # No arguments: validate all examples
    EXAMPLES_DIR="$REPO_ROOT/04-protocol/EXAMPLES"
    
    if [ ! -d "$EXAMPLES_DIR" ]; then
        echo -e "${RED}Error: 04-protocol/EXAMPLES/ directory not found${NC}"
        exit 1
    fi
    
    # Find all .json files in EXAMPLES directory
    ENVELOPE_FILES=($(find "$EXAMPLES_DIR" -name "*.json" -type f | sort))
    
    if [ ${#ENVELOPE_FILES[@]} -eq 0 ]; then
        echo -e "${YELLOW}Warning: No envelope examples found in $EXAMPLES_DIR${NC}"
        exit 0
    fi
    
    echo "Validating ${#ENVELOPE_FILES[@]} envelope examples..."
    echo ""
else
    # Arguments provided: validate specific files
    ENVELOPE_FILES=("$@")
    echo "Validating ${#ENVELOPE_FILES[@]} specified envelope(s)..."
    echo ""
fi

# Validate each envelope
FAILED=0
PASSED=0

for envelope_file in "${ENVELOPE_FILES[@]}"; do
    # Make path absolute if relative
    if [[ ! "$envelope_file" = /* ]]; then
        envelope_file="$REPO_ROOT/$envelope_file"
    fi
    
    if [ ! -f "$envelope_file" ]; then
        echo -e "${RED}✗${NC} $(basename "$envelope_file") - File not found"
        ((FAILED++))
        continue
    fi
    
    # Validate using qfspec-check-envelope
    if uv run --directory "$REPO_ROOT/tools" qfspec-check-envelope "$envelope_file" > /tmp/validate-output.txt 2>&1; then
        # Extract just the filename for cleaner output
        filename=$(basename "$envelope_file")
        echo -e "${GREEN}✓${NC} $filename"
        ((PASSED++))
    else
        filename=$(basename "$envelope_file")
        echo -e "${RED}✗${NC} $filename"
        # Show validation errors
        grep -A 5 "Validation error\|validation errors" /tmp/validate-output.txt || true
        echo ""
        ((FAILED++))
    fi
done

# Summary
echo ""
echo "=== Validation Summary ==="
echo "Total: $((PASSED + FAILED))"
echo -e "Passed: ${GREEN}${PASSED}${NC}"

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}All envelope examples are valid!${NC}"
    exit 0
else
    echo -e "Failed: ${RED}${FAILED}${NC}"
    exit 1
fi

#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python "${ROOT_DIR}/scripts/lint_placeholders.py" "${ROOT_DIR}/releases/1.0.0/prompts"
python "${ROOT_DIR}/scripts/check_consistency.py" "${ROOT_DIR}"

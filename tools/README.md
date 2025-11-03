# QuestFoundry Specification Tools

Validation and maintenance tools for the **QuestFoundry specification itself**.

> **Note:** These are spec maintenance tools for developers working on the QuestFoundry
> specification. If you're looking for tools to _implement_ games/books using the spec, see Layer 6
> (`qf` CLI).

## Overview

This UV project provides three types of validation:

1. **Schema Validation** - Ensures Layer 3 and Layer 4 schemas are valid JSON Schema Draft 2020-12
2. **Instance Validation** - Ensures artifact instances comply with their QuestFoundry schemas
3. **Envelope Validation** - Validates Layer 4 protocol envelopes and their embedded payloads

## Quick Start

```bash
# One-time setup (from tools/ directory)
cd tools
uv sync

# Validate all schemas (Layer 3 + Layer 4)
uv run qfspec-validate

# Validate instance files
uv run qfspec-check-instance hook_card ../path/to/hook.json

# Validate Layer 4 envelope files (NEW)
uv run qfspec-check-envelope ../04-protocol/EXAMPLES/hook.create.json
```

## Installation

### Development Setup

```bash
cd tools
uv sync
```

This installs:

- `jsonschema` - Python library for JSON Schema validation (includes Draft 2020-12 meta-schemas)
- `pre-commit` - Git hook framework (optional)

### Optional: Install as Global Tool

```bash
# Install globally using uv tool
uv tool install ./tools

# Now available system-wide
qfspec-validate
qfspec-check-instance hook_card my-hook.json
qfspec-check-envelope my-envelope.json
```

## Usage

All commands should be run from the **repository root**, not from the `tools/` directory.

### 1. Validate Schemas (Meta-validation)

Validates that all Layer 3 and Layer 4 schemas comply with JSON Schema Draft 2020-12:

```bash
# From repository root
cd /path/to/questfoundry
uv run --directory tools qfspec-validate

# Or shorter (from tools/ directory)
cd tools
uv run qfspec-validate
```

**Example output:**

```
=== QuestFoundry Spec: Schema Validator ===
Repository: /path/to/questfoundry

Validating Layer 3 schemas...
  Checking art_plan.schema.json... ✓
  Checking audio_plan.schema.json... ✓
  Checking hook_card.schema.json... ✓
  ...

Validating Layer 4 envelope schema...
  Checking envelope.schema.json... ✓

=== Validation Summary ===
All schemas are valid JSON Schema Draft 2020-12!
```

**When to use:**

- After modifying any schema in `03-schemas/` or `04-protocol/`
- Before committing schema changes
- In CI/CD pipelines
- When developing new schemas

### 2. Validate Instances

Validates artifact instance files against their schemas:

```bash
# Validate a single hook card
uv run --directory tools qfspec-check-instance hook_card path/to/hook.json

# Validate multiple files
uv run --directory tools qfspec-check-instance gatecheck_report report1.json report2.json

# Validate with glob patterns
uv run --directory tools qfspec-check-instance view_log logs/*.json
```

**Example output:**

```
=== QuestFoundry Spec: Instance Validator ===
Repository: /path/to/questfoundry
Schema: hook_card

Validating hook-001.json... ✓
Validating hook-002.json... ✗
  Validation error at 'status': 'draft' is not one of ['proposed', 'accepted', ...]

=== Validation Summary ===
Total: 2
Passed: 1
Failed: 1
```

**Available schemas:**

- `art_plan`
- `audio_plan`
- `canon_pack`
- `codex_entry`
- `cuelist`
- `edit_notes`
- `front_matter`
- `gatecheck_report`
- `hook_card`
- `language_pack`
- `pn_playtest_notes`
- `register_map`
- `research_memo`
- `shotlist`
- `style_addendum`
- `tu_brief`
- `view_log`

**When to use:**

- When creating artifact instances for books/games
- After generating artifacts from Layer 2 templates
- In quality assurance workflows
- When testing schema changes against sample data

## Pre-commit Hook

The repository includes a pre-commit hook that automatically validates schemas before commits. The
hook is configured in the root `.pre-commit-config.yaml`.

**Setup:**

```bash
# From repository root
pip install pre-commit
pre-commit install
```

**Manual run:**

```bash
# Run on all files
pre-commit run --all-files

# Run on specific files
pre-commit run --files 03-schemas/hook_card.schema.json
```

The hook automatically validates any schema files in `03-schemas/` that are staged for commit,
blocking the commit if validation fails.

## CI/CD Integration

Add validation to your CI pipeline:

```yaml
# Example for GitHub Actions
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: "3.11"

- name: Install uv
  run: pip install uv

- name: Validate schemas
  run: uv run --directory tools qfspec-validate
```

## Commands Reference

### `qfspec-validate`

Validates all QuestFoundry schemas against JSON Schema Draft 2020-12.

**Usage:**

```bash
uv run qfspec-validate
```

**Features:**

- Validates all `*.schema.json` files in `03-schemas/`
- Uses bundled meta-schema (no network required)
- Color-coded output (✓ for pass, ✗ for fail)
- Detailed error messages for validation failures
- Exit code 0 on success, 1 on failure

**Arguments:** None

### `qfspec-check-instance`

Validates artifact instance files against a QuestFoundry schema.

**Usage:**

```bash
uv run qfspec-check-instance <schema-name> <instance-file> [instance-file2 ...]
```

**Features:**

- Validates multiple instances in one run
- Uses bundled meta-schema (no network required)
- Detailed error messages with error paths
- Summary report with pass/fail counts
- Exit code 0 on success, 1 on failure

**Arguments:**

- `schema-name` - Schema to validate against (e.g., `hook_card`, `view_log`)
- `instance-file` - One or more instance files to validate

**Examples:**

```bash
# Single file
uv run qfspec-check-instance hook_card my-hook.json

# Multiple files
uv run qfspec-check-instance gatecheck_report report1.json report2.json

# Glob patterns
uv run qfspec-check-instance view_log logs/*.json
```

### `qfspec-check-envelope`

**NEW in Layer 4:** Validates Layer 4 envelope files using a **two-pass validation approach**.

**Usage:**

```bash
uv run qfspec-check-envelope <envelope-file> [envelope-file2 ...]
```

**Two-Pass Validation:**

This command implements the two-pass validation approach described in `04-protocol/ENVELOPE.md`
Section 3.1.1:

1. **Pass 1: Envelope Structure Validation**
   - Validates entire envelope against `04-protocol/envelope.schema.json` (Layer 4)
   - Checks required fields (protocol, id, time, sender, receiver, intent, context, safety, payload)
   - Validates role names against Layer 2 taxonomy (`02-dictionary/role_abbreviations.md`)
   - Validates loop names against Layer 2 taxonomy (`02-dictionary/loop_names.md`)
   - Enforces PN safety constraints (Cold-only, player_safe, spoilers forbidden)
   - No external `$ref` resolution needed (envelope schema is self-contained)

2. **Pass 2: Payload Data Validation**
   - Extracts `payload.type` and `payload.data` from envelope
   - Loads corresponding Layer 3 schema (`03-schemas/{payload.type}.schema.json`)
   - Validates **only** `payload.data` against the Layer 3 schema
   - Skipped if `payload.type = "none"` (for acks/errors)

**Features:**

- Two independent validation passes for clear error reporting
- Proper layer separation (Layer 4 → Layer 2, not Layer 4 → Layer 3)
- No deprecated RefResolver usage (future-proof)
- Detailed error messages showing which pass failed
- Summary report with pass/fail counts
- Exit code 0 on success, 1 on failure

**Arguments:**

- `envelope-file` - One or more envelope JSON files to validate

**Examples:**

```bash
# Single envelope
uv run qfspec-check-envelope 04-protocol/EXAMPLES/hook.create.json

# Multiple envelopes
uv run qfspec-check-envelope 04-protocol/EXAMPLES/hook.*.json

# All examples
uv run qfspec-check-envelope 04-protocol/EXAMPLES/*.json
```

**What it validates:**

**Pass 1 - Envelope Structure (Layer 4):**

- Required fields: protocol, id, time, sender, receiver, intent, context, safety, payload
- Field formats: RFC3339 timestamps, UUID/URN ids, TU/snapshot patterns
- Role names: Must match Layer 2 taxonomy (15 valid roles: SR, GK, PW, SS, ST, LW, CC, AD, IL, AuD,
  AuP, TR, BB, PN, RS)
- Loop names: Must match Layer 2 taxonomy (13 valid loops from Discovery/Refinement/Asset/Export
  categories)
- Enum constraints: hot_cold (hot/cold), player_safe (true/false), spoilers (allowed/forbidden)
- PN Safety Invariant: When `receiver.role = "PN"`, enforces:
  - `context.hot_cold = "cold"` AND
  - `safety.player_safe = true` AND
  - `safety.spoilers = "forbidden"`

**Pass 2 - Payload Data (Layer 3):**

- Skipped if `payload.type = "none"` (acks/errors)
- Otherwise validates `payload.data` against `03-schemas/{payload.type}.schema.json`
- All Layer 3 schema constraints apply (required fields, patterns, nested structures, etc.)
- Example: For `payload.type = "hook_card"`, validates against `hook_card.schema.json`

**Example output (all passing):**

```
=== QuestFoundry Spec: Envelope Validator ===
Repository: /path/to/questfoundry

Validating hook.create.json... ✓
Validating ack.json... ✓
Validating error.validation.json... ✓

=== Validation Summary ===
Total: 3
Passed: 3
All envelopes are valid!
```

**Example output (with errors):**

```
=== QuestFoundry Spec: Envelope Validator ===
Repository: /path/to/questfoundry

Validating hook.create.json... ✓
Validating invalid.json... ✗
  Envelope validation errors (Pass 1):
  context -> loop: 'Invalid Loop' is not one of ['Story Spark', 'Hook Harvest', ...]
Validating bad-payload.json... ✗
  Payload validation errors (Pass 2, type: hook_card):
  header -> status: 'draft' is not one of ['proposed', 'accepted', ...]

=== Validation Summary ===
Total: 3
Passed: 1
Failed: 2
```

**Note:** Error messages clearly indicate which validation pass failed:

- `(Pass 1)` = Envelope structure validation failed
- `(Pass 2, type: <payload_type>)` = Payload data validation failed

**When to use:**

- After creating or modifying envelope examples in `04-protocol/EXAMPLES/`
- Before committing envelope changes
- In CI/CD to validate protocol message conformance
- When testing envelope schema changes
- To verify PN safety constraints are enforced

## Troubleshooting

### `jsonschema` module not found

```bash
cd tools
uv sync
```

### Schema validation fails

The validator provides detailed error messages. Common issues:

- **Missing required fields:** Schema must include `$schema` and `$id`
- **Invalid regex patterns:** Unescaped special characters in `pattern` fields
- **Incorrect references:** `$defs` references must match defined definitions
- **Type mismatches:** Property `type` must match the actual value type
- **Invalid JSON:** Check for syntax errors (trailing commas, unquoted keys)

**Example error:**

```
✗ hook_card.schema.json
  Schema validation error: 'properties' is a required property
```

### Instance validation fails

The validator shows the error path and message. Common issues:

- **Missing required fields:** Instance must include all `required` properties
- **Invalid enum values:** Value must be one of the allowed enum options
- **Pattern mismatch:** String value doesn't match the regex pattern
- **Type mismatch:** Value type doesn't match schema (e.g., string vs number)
- **Conditional failures:** `if/then/else` validation requirements not met

**Example error:**

```
✗ my-hook.json
  Validation error at 'status': 'draft' is not one of ['proposed', 'accepted', 'in-progress', ...]
```

### Can't find repository root

The tools automatically search for the repository root by looking for `03-schemas/` directory. If
running from an unexpected location:

```bash
# Always run from repository root
cd /path/to/questfoundry
uv run --directory tools qfspec-validate
```

## Development

### Project Structure

```
tools/
├── README.md                          # This file
├── pyproject.toml                     # UV project configuration
├── uv.lock                           # Dependency lock file (auto-generated)
└── src/
    └── questfoundry_spec_tools/
        ├── __init__.py
        ├── cli.py                    # CLI entry points
        ├── schema_validator.py       # Schema validation logic
        └── instance_validator.py     # Instance validation logic
```

### Adding New Layers

When Layer 4 schemas are added, update:

1. **`schema_validator.py`** - Add Layer 4 to the validation logic
2. **`cli.py`** - Add Layer 4 section to the output
3. **Pre-commit config** (root `.pre-commit-config.yaml`) - Add Layer 4 file pattern

### Building and Publishing

```bash
# Build package
cd tools
uv build

# Install locally for testing
uv pip install -e .
```

## Future Enhancements

- Add Layer 4 validation when transforms are created
- Create batch instance validator for entire directories
- Add JSON/YAML format conversion tools
- Integrate with markdown template parser for Layer 2 artifacts
- Add schema diff tool for comparing versions

## References

- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/json-schema-core.html)
- [Python jsonschema library](https://python-jsonschema.readthedocs.io/)
- [uv documentation](https://docs.astral.sh/uv/)
- [pre-commit documentation](https://pre-commit.com/)

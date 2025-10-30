# QuestFoundry Validation Tools

This document describes the validation tools for QuestFoundry schemas and artifact instances.

## Overview

QuestFoundry uses JSON Schema Draft 2020-12 for validation. Two types of validation are supported:

1. **Schema Validation** - Ensures Layer 3 (and later Layer 4) schemas are valid JSON Schema Draft 2020-12
2. **Instance Validation** - Ensures artifact instances comply with their schemas

## Setup

### Install Dependencies

```bash
pip install -r requirements-dev.txt
```

This installs:
- `jsonschema` - Python library for schema validation (includes Draft 2020-12 meta-schemas)
- `pre-commit` - Git hook framework (optional)

### Install Pre-commit Hook (Optional)

The pre-commit hook automatically validates schemas before commits:

```bash
pre-commit install
```

This hook will:
- Run automatically on `git commit`
- Validate any modified schema files in `03-schemas/`
- Block commits if schemas are invalid

## Usage

### 1. Validate Schemas (Meta-validation)

Check that all Layer 3 schemas are valid JSON Schema Draft 2020-12:

```bash
# Using the Python validation script (recommended)
python3 scripts/validate-schemas.py

# Or using bash wrapper
./scripts/validate-schemas.sh

# Or using pre-commit (validates only staged files)
pre-commit run --all-files
```

**When to use:**
- After modifying any schema in `03-schemas/`
- Before committing schema changes
- In CI/CD pipelines

**Note:** The Python validator uses the bundled meta-schema from the `jsonschema` library, so no network access is required.

### 2. Validate Instances

Check that artifact instances comply with their schemas:

```bash
# Using Python script (recommended)
python3 scripts/validate-instance.py hook_card my-hook.json

# Validate multiple gatecheck reports
python3 scripts/validate-instance.py gatecheck_report report1.json report2.json

# Validate all view logs
python3 scripts/validate-instance.py view_log logs/*.json

# Or using bash wrapper
./scripts/validate-instance.sh hook_card my-hook.json
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
- When creating artifact instances for books
- After exporting artifacts from Layer 2 templates
- In quality assurance workflows

## Validation Scripts

### `scripts/validate-schemas.py`

Python script that validates all schemas in `03-schemas/` against JSON Schema Draft 2020-12.

**Features:**
- Uses bundled meta-schema (no network required)
- Color-coded output (✓ for pass, ✗ for fail)
- Detailed error messages for validation failures
- Summary report
- Exit code 0 on success, 1 on failure

**Usage:**
```bash
python3 scripts/validate-schemas.py
```

**Example output:**
```
=== QuestFoundry Schema Validator ===

Validating Layer 3 schemas...
  Checking hook_card.schema.json... ✓
  Checking gatecheck_report.schema.json... ✓
  ...

=== Validation Summary ===
All schemas are valid JSON Schema Draft 2020-12!
```

### `scripts/validate-instance.py`

Python script that validates artifact instance(s) against a specified schema.

**Features:**
- Uses bundled meta-schema (no network required)
- Validates multiple instances in one run
- Detailed error messages with error paths
- Summary report with pass/fail counts
- Exit code 0 on success, 1 on failure

**Usage:**
```bash
python3 scripts/validate-instance.py <schema-name> <instance-file> [instance-file2 ...]
```

**Example output:**
```
=== QuestFoundry Instance Validator ===
Schema: hook_card

Validating hook-001.json... ✓
Validating hook-002.json... ✗
  Validation error at 'root': 'status' is a required property

=== Validation Summary ===
Total: 2
Passed: 1
Failed: 1
```

### Bash Wrapper Scripts

Shell wrappers (`scripts/validate-schemas.sh` and `scripts/validate-instance.sh`) are also provided for convenience. They call the Python scripts internally.

## Pre-commit Hook

The `.pre-commit-config.yaml` file configures automatic schema validation.

**Configuration:**
```yaml
repos:
  - repo: local
    hooks:
      - id: validate-schemas
        name: Validate Layer 3 schemas (Draft 2020-12)
        entry: python3 scripts/validate-schemas.py
        language: system
        files: ^03-schemas/.*\.schema\.json$
        pass_filenames: false
```

**How it works:**
1. Runs on `git commit`
2. Only validates schemas in `03-schemas/` that are staged
3. Blocks commit if any schema is invalid
4. Displays validation errors

**Manual runs:**
```bash
# Run on all files (not just staged)
pre-commit run --all-files

# Run on specific files
pre-commit run --files 03-schemas/hook_card.schema.json
```

## CI/CD Integration

Add validation to your CI pipeline:

```yaml
# Example for GitHub Actions
- name: Install validation tools
  run: pip install -r requirements-dev.txt

- name: Validate schemas
  run: ./scripts/validate-schemas.sh
```

## Troubleshooting

### `jsonschema` module not found

Install dependencies:
```bash
pip install -r requirements-dev.txt
```

Or install directly:
```bash
pip install jsonschema
```

### Schema validation fails

The Python validator provides detailed error messages. Look for:

Common issues:
- Missing required meta-schema fields (`$schema`, `$id`)
- Invalid regex patterns (unescaped special characters)
- Incorrect `$defs` references
- Type mismatches in property definitions
- Invalid JSON syntax

**Example:**
```
✗ hook_card.schema.json
  Schema validation error: 'properties' is a required property
```

### Instance validation fails

The validator shows the error path and message:

Common issues:
- Missing required fields
- Values not matching enum/pattern constraints
- Type mismatches (string vs number)
- Conditional validation failures (if/then/else)

**Example:**
```
✗ my-hook.json
  Validation error at 'status': 'draft' is not one of ['proposed', 'accepted', ...]
```

## Future Enhancements

- Add Layer 4 validation when schemas are created
- Create batch instance validator for entire directories
- Add JSON/YAML format conversion tools
- Integrate with markdown template parser for Layer 2 artifacts

## References

- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/json-schema-core.html)
- [Python jsonschema library](https://python-jsonschema.readthedocs.io/)
- [pre-commit documentation](https://pre-commit.com/)

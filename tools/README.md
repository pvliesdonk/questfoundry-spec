# QuestFoundry Specification Tools

Validation and maintenance tools for the **QuestFoundry specification itself**.

> **Note:** These are spec maintenance tools for developers working on the QuestFoundry
> specification. If you're looking for tools to _implement_ games/books using the spec, see Layer 6
> (`qf` CLI).

## Overview

This UV project provides validation and formatting tools:

1. **Schema Validation** - Ensures Layer 3 (and future Layer 4) schemas are valid JSON Schema Draft
   2020-12
2. **Instance Validation** - Ensures artifact instances comply with their QuestFoundry schemas
3. **Formatting** - Prettier for strict JSON and Markdown formatting
4. **Linting** - Markdownlint for lenient Markdown style checking

## Quick Start

```bash
# One-time setup (from tools/ directory)
cd tools
uv sync

# Validate all schemas
uv run qfspec-validate

# Validate instance files
uv run qfspec-check-instance hook_card ../path/to/hook.json
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
```

## Usage

All commands should be run from the **repository root**, not from the `tools/` directory.

### 1. Validate Schemas (Meta-validation)

Validates that all Layer 3 schemas comply with JSON Schema Draft 2020-12:

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

=== Validation Summary ===
All schemas are valid JSON Schema Draft 2020-12!
```

**When to use:**

- After modifying any schema in `03-schemas/`
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

### 3. Format Code (Prettier)

Automatically formats JSON and Markdown files to enforce consistent style:

```bash
# Format all JSON and Markdown files
npx prettier --write "**/*.{json,md}" --config tools/.prettierrc.json --ignore-path tools/.prettierignore

# Check formatting without modifying files
npx prettier --check "**/*.{json,md}" --config tools/.prettierrc.json --ignore-path tools/.prettierignore

# Format specific files
npx prettier --write README.md 03-schemas/hook_card.schema.json
```

**Prettier configuration (strict):**

- **Line width:** 100 characters
- **Indentation:** 2 spaces (no tabs)
- **Prose wrapping:** Always (for Markdown)
- **Trailing commas:** ES5 style (for JSON)
- **Quote style:** Double quotes
- **Config:** `tools/.prettierrc.json`

**When to use:**

- Before committing changes (runs automatically via pre-commit hook)
- When cleaning up formatting inconsistencies
- After editing schemas or documentation

**Note:** The pre-commit hook runs Prettier automatically, so manual formatting is rarely needed.

### 4. Lint Markdown (Markdownlint)

Checks Markdown files for style consistency (lenient configuration):

```bash
# Lint all Markdown files
npx markdownlint-cli2 "**/*.md" --config tools/.markdownlint.json

# Lint specific files
npx markdownlint-cli2 README.md 00-north-star/HOOKS.md
```

**Markdownlint configuration (lenient):**

- **Heading style:** ATX style (`#`, `##`, etc.)
- **List indentation:** 2 spaces
- **Line length:** Disabled (handled by Prettier)
- **Duplicate headings:** Allowed for siblings only
- **Inline HTML:** Allowed (needed for schemas/docs)
- **First line heading:** Not required
- **Config:** `tools/.markdownlint.json`

**When to use:**

- To check Markdown style (runs automatically via pre-commit hook)
- When reviewing documentation changes
- Note: Failures don't block commits (lenient mode)

## Pre-commit Hook

The repository includes pre-commit hooks that automatically run formatters, validators, and linters
before commits. The hooks are configured in the root `.pre-commit-config.yaml`.

**Hooks (in order):**

1. **Prettier** - Formats JSON and Markdown (auto-fixes, blocks if formatting needed)
2. **Schema Validator** - Validates schemas against Draft 2020-12 (blocks if invalid)

**Note:** Markdownlint is intentionally NOT in pre-commit hooks to keep commits fast and
non-blocking for documentation changes. It runs in CI (lenient mode) and can be run manually as
needed.

**Setup:**

```bash
# From repository root
pip install pre-commit
pre-commit install
```

**Manual run:**

```bash
# Run all hooks on all files
pre-commit run --all-files

# Run specific hook
pre-commit run prettier --all-files
pre-commit run validate-schemas --all-files

# Run on specific files
pre-commit run --files 03-schemas/hook_card.schema.json README.md
```

**How auto-fix works:** When you run `git commit`, the hooks run automatically:

1. If Prettier needs to format files, it auto-fixes them and **aborts the commit**
2. You review the formatting changes
3. Run `git add` and `git commit` again
4. Second commit succeeds (files already formatted)

This ensures you can review all automated changes before committing.

## CI/CD Integration

The repository includes a GitHub Actions workflow that automatically validates formatting and
schemas on pull requests and pushes to main branches.

**Workflow:** `.github/workflows/validate.yml`

The workflow runs:

1. **Prettier check** - Ensures all JSON/Markdown is formatted (fails if not)
2. **Markdownlint** - Lints Markdown (warnings only, doesn't fail)
3. **Schema validation** - Validates all schemas against Draft 2020-12 (fails if invalid)

**Triggers:**

- Pull requests to `main`
- Pushes to `main` or `claude/**` branches

**View results:**

- Check the Actions tab in GitHub after pushing
- Failed checks will block PR merges

**Manual workflow run:**

```bash
# Run the same checks locally
npx prettier --check "**/*.{json,md}" --config tools/.prettierrc.json --ignore-path tools/.prettierignore
npx markdownlint-cli2 "**/*.md" --config tools/.markdownlint.json
uv run --directory tools qfspec-validate
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

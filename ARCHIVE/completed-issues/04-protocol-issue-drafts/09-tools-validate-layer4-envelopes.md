Title: Tools: Add Layer 4 envelope validation (schema + instances)

Summary

- Extend `spec-tools/` to validate Layer 4 envelopes and the payloads they carry against Layer 3
  schemas. Update pre-commit to cover 04-protocol schemas.

Tasks

- `spec-tools/src/questfoundry_spec_tools/schema_validator.py`:
  - Include `04-protocol/envelope.schema.json` in validation set (Draft 2020-12).
- `spec-tools/src/questfoundry_spec_tools/cli.py`:
  - Add a new command `qfspec-validate-l4` (or extend existing) to print a distinct section for
    Layer 4.
- `spec-tools/src/questfoundry_spec_tools/instance_validator.py`:
  - Add a mode `--envelope` that validates the envelope against its schema, and then validates
    `payload.data` against the correct Layer 3 schema by `payload.type`.
  - CLI example: `qfspec-check-envelope path/to/envelope.json`.
- `.pre-commit-config.yaml` (root):
  - Add a hook (comment it in) to validate `04-protocol/*.schema.json` with
    `uv run qfspec-validate-l4`.
- `spec-tools/README.md`:
  - Document the new commands and examples.

Acceptance Criteria

- `qfspec-validate-l4` reports success against `04-protocol/envelope.schema.json`.
- `qfspec-check-envelope` validates an example envelope and its payload.
- Pre-commit hook prepared; may stay optional if repo policy defers enabling until L4 stabilizes.

References

- `04-protocol/envelope.schema.json`
- `03-schemas/*.schema.json`
- `.pre-commit-config.yaml`
- `spec-tools/README.md`

Branch & Validation

- Branch off `feature/layer4-protocol-plan` as `feature/l4-tools-envelope-validation`.
- Run `uv run --directory spec-tools qfspec-validate` and new Layer 4 command locally.

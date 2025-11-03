Title: Examples: Envelope suite + CI validation

Summary

- Provide a suite of example envelope JSON files (at least 10) and a simple CI script to validate
  both envelope and payload schemas.

Tasks

- Create `04-protocol/EXAMPLES/` with examples:
  - `hook.create.json`, `hook.update_status.accepted.json`
  - `tu.open.lore.json`, `merge.request.json`
  - `gate.report.submit.json`, `gate.decision.pass.json`
  - `view.export.request.json`, `view.export.result.json`
  - `pn.playtest.submit.json`
  - `ack.json`, `error.validation.json`
- Add a simple `scripts/validate-examples.sh` (or `.ps1`) that runs:
  - `uv run --directory tools qfspec-check-envelope 04-protocol/EXAMPLES/*.json`
- Add CI note (GH Actions job snippet) to run the script on PR.

Acceptance Criteria

- All examples validate against `04-protocol/envelope.schema.json` AND their Layer 3 payload
  schemas.
- Script exits non-zero on failure; CI snippet included in `README.md` under `04-protocol/` or
  `tools/`.

References

- `04-protocol/envelope.schema.json`
- `tools/README.md`

Branch & Validation

- Branch off `feature/layer4-protocol-plan` as `feature/l4-examples-envelope-suite`.
- Validate locally using the script; ensure cross-platform note (bash and PowerShell variants
  acceptable).

Title: Spec: FLOWS — Binding Run and Narration Dry-Run + Examples & Conformance

Summary

- Specify Binding and PN flows (Cold-only), add example envelopes, and a conformance guide using
  existing tools.

Tasks

- Add `04-protocol/FLOWS/binding_run.md` and `04-protocol/FLOWS/narration_dry_run.md`:
  - Sequence: select snapshot → `view.export.request` → `view.export.result` → `pn.playtest.submit`.
  - PN appears only on Cold legs (`context.hot_cold = "cold"`, `safety.player_safe = true`).
- Add `04-protocol/EXAMPLES/` with at least 8 JSON examples:
  - `hook.create.json`, `hook.update_status.accepted.json`
  - `tu.open.lore.json`
  - `gate.report.submit.json`, `gate.decision.pass.json`
  - `view.export.request.json`, `view.export.result.json`
  - `pn.playtest.submit.json`
  - `ack.json`, `error.validation.json`
- Add `04-protocol/CONFORMANCE.md`:
  - MUST/SHOULD list; minimal test matrix; validation instructions using `tools`:
    - Extract `payload.data` to temp file and run:
      - `uv run --directory tools qfspec-check-instance hook_card tmp/payload.json`
      - `uv run --directory tools qfspec-check-instance gatecheck_report tmp/payload.json`
      - etc., per schema

Acceptance Criteria

- PN flows enforce Cold-only and player-safe constraints.
- At least 8 examples included; payloads validate against Layer 3 using `tools`.
- CONFORMANCE.md present with error taxonomy usage and basic flow checks.

References

- `00-north-star/LOOPS/binding_run.md`, `00-north-star/LOOPS/narration_dry_run.md`
- `03-schemas/*` (hook_card, view_log, pn_playtest_notes, gatecheck_report)

Branch & Validation

- Branch from `feature/layer4-protocol-plan` as `feature/l4-flows-binding-pn-examples`.
- Validate examples with `uv run --directory tools qfspec-validate` and `qfspec-check-instance` as
  applicable.

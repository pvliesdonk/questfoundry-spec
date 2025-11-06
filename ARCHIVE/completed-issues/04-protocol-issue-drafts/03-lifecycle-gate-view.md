Title: Spec: Lifecycles — Gate and View/Export (Cold/PN-safe)

Summary

- Define gatecheck decisioning and view/export lifecycle, enforcing PN Cold-only and player-safe
  constraints.

Tasks

- Add `04-protocol/LIFECYCLES/gate.md`:
  - pre-gate → gatecheck decision (`pass | conditional pass | block`)
  - For each: bar evidence, smallest viable fix, owner, handoffs; map to schema fields.
- Add `04-protocol/LIFECYCLES/view.md`:
  - snapshot selected → export → PN dry-run → feedback
  - PN must only receive `cold` + `player_safe: true` payloads; require `context.snapshot`.

Acceptance Criteria

- Gate doc ties decisions to Quality Bars and `gatecheck_report` fields.
- View doc requires `context.snapshot` in envelope; errors defined for missing/invalid snapshot.
- PN boundary rules explicit.

References

- `00-north-star/QUALITY_BARS.md`, `00-north-star/SOURCES_OF_TRUTH.md`,
  `00-north-star/PN_PRINCIPLES.md`
- `03-schemas/gatecheck_report.schema.json`, `03-schemas/view_log.schema.json`,
  `03-schemas/pn_playtest_notes.schema.json`

Branch & Validation

- Branch from `feature/layer4-protocol-plan` as `feature/l4-lifecycles-gate-view`.
- Check schema fields referenced exist and match enums.

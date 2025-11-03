Title: Spec: FLOWS — Codex Expansion and Gatecheck/Merge

Summary
- Define sequences for Codex publishing (player-safe) and Gatecheck/Merge handoffs.

Tasks
- Add `04-protocol/FLOWS/codex_expansion.md`:
  - LW→CC player-safe summaries; CC submits `codex_entry`; GK checks; merge path.
  - Forbid spoilers in codex payloads; emphasize player-safe constraint.
- Add `04-protocol/FLOWS/gatecheck.md`:
  - Owners submit `gate.report.submit`; GK responds with `gate.decision` and handoffs.
  - `merge.request/approve/reject` and snapshot stamping rules.

Acceptance Criteria
- Codex flow enforces player-safe payloads; no canon spoilers.
- Gate flow ties decisions to bar statuses and smallest viable fixes (owner + TU handoffs).
- Merge approvals record snapshot per `TRACEABILITY`.

References
- `00-north-star/LOOPS/codex_expansion.md`
- `03-schemas/codex_entry.schema.json`, `03-schemas/gatecheck_report.schema.json`
- `00-north-star/TRACEABILITY.md`

Branch & Validation
- Branch from `feature/layer4-protocol-plan` as `feature/l4-flows-codex-gate`.
- Validate schema fields referenced; align with lifecycles and intents.


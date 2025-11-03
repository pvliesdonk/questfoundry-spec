Title: Spec: FLOWS — Hook Harvest and Lore Deepening

Summary

- Author end-to-end message sequences for two core loops: Hook Harvest and Lore Deepening.

Tasks

- Add `04-protocol/FLOWS/hook_harvest.md`:
  - Sequence: `hook.create*` → SR triage → `hook.update_status (accepted|deferred|rejected)`.
  - Note required fields for acceptance (owner, next loop) and deferral (reason, revisit).
- Add `04-protocol/FLOWS/lore_deepening.md`:
  - Sequence: SR→LW `tu.open` → LW submits canon payload → GK pre-gate → `merge.request`.
  - Document TU requirement prior to merge.

Acceptance Criteria

- Sequences list intents, roles, and expected replies.
- Payloads are backed by Layer 3 schemas (hook_card, tu_brief, canon_pack).
- TU linkage is explicit before merge.

References

- `00-north-star/LOOPS/hook_harvest.md`, `00-north-star/LOOPS/lore_deepening.md`
- `03-schemas/hook_card.schema.json`, `03-schemas/tu_brief.schema.json`, `03-schemas/canon_pack.schema.json`

Branch & Validation

- Branch from `feature/layer4-protocol-plan` as `feature/l4-flows-harvest-lore`.
- Cross-check sequence with lifecycles and intents docs.

Title: Spec: Lifecycles — Hooks and TU

Summary

- Codify allowed state transitions for hooks and TUs, who triggers them, and required intents/payloads.

Tasks

- Add `04-protocol/LIFECYCLES/hooks.md`:
  - Lifecycle: `proposed → accepted → in-progress → resolved → canonized`; branches `deferred`, `rejected`.
  - For each transition: allowed senders (SR/owner), required intents, payload schemas, errors on invalid transitions.
- Add `04-protocol/LIFECYCLES/tu.md`:
  - Lifecycle: `hot-proposed → stabilizing → gatecheck → cold-merged | deferred | rejected`.
  - TU required for any artifact bound for Cold (document as rule).

Acceptance Criteria

- Each lifecycle lists transitions with: preconditions, sender role, intent name(s), required payload `$schema`, and error cases.
- Enums align with `02-dictionary/taxonomies.md` and `03-schemas/*`.

References

- `02-dictionary/taxonomies.md`
- `03-schemas/hook_card.schema.json`, `03-schemas/tu_brief.schema.json`
- `00-north-star/TRACEABILITY.md`

Branch & Validation

- Branch from `feature/layer4-protocol-plan` as `feature/l4-lifecycles-hooks-tu`.
- Ensure consistency with enums used in Layer 3.

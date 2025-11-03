Title: Update INTENTS to reference envelope.schema.json and standardize errors

Summary
- Ensure `04-protocol/INTENTS.md` formally references `envelope.schema.json`, defines required envelope fields per intent, and standardizes error responses.

Tasks
- In `04-protocol/INTENTS.md`:
  - For each intent, add an “Envelope requirements” block: mandatory context fields, safety expectations, sender/receiver roles, and payload.type mapping.
  - Define `ack` and `error` envelope shapes by reference to envelope.schema.json.
  - Ensure error taxonomy matches envelope schema (`validation_error`, `business_rule_violation`, `not_authorized`, `not_found`, `conflict`).
- Add cross-links to lifecycles where transitions require specific intents.

Acceptance Criteria
- Every intent lists envelope field requirements and payload `$schema` references.
- Error taxonomy is uniform and aligns with envelope schema.
- Cross-links resolve.

References
- `04-protocol/envelope.schema.json`
- `04-protocol/LIFECYCLES/*.md`
- `03-schemas/*.schema.json`

Branch & Validation
- Branch off `feature/layer4-protocol-plan` as `feature/l4-intents-envelope-alignment`.
- Validate examples in `EXAMPLES/` remain consistent with INTENTS.


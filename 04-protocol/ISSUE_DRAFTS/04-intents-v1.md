Title: Spec: INTENTS v1 — Core Message Catalog

Summary
- Define the message verbs/intents that move lifecycles and carry Layer 3 payloads.

Tasks
- Add `04-protocol/INTENTS.md` enumerating intents with tables per intent: purpose, sender→receiver, required envelope fields, payload `$schema`, expected replies, error taxonomy.
- Minimum coverage:
  - `hook.create`, `hook.update_status`
  - `tu.open`, `tu.update`, `tu.close`
  - `gate.report.submit`, `gate.decision`
  - `merge.request`, `merge.approve`, `merge.reject`
  - `view.export.request`, `view.export.result`
  - `pn.playtest.submit`
  - `ack`, `error`
- Define error taxonomy: `validation_error`, `business_rule_violation`, `not_authorized`, `not_found`, `conflict`.

Acceptance Criteria
- Each intent references at least one Layer 3 schema and the sender/receiver roles.
- Error taxonomy standardized and referenced by all intents.
- Cross-links to `LIFECYCLES/*.md` where relevant.

References
- `04-protocol/LIFECYCLES/*.md`
- `03-schemas/*.schema.json`

Branch & Validation
- Branch from `feature/layer4-protocol-plan` as `feature/l4-intents-v1`.
- Ensure cross-links resolve; examples can be stubbed here or in EXAMPLES.


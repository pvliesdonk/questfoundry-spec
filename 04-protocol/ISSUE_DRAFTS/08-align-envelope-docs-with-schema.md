Title: Align ENVELOPE.md docs with envelope.schema.json

Summary

- Bring `04-protocol/ENVELOPE.md` to parity with `04-protocol/envelope.schema.json`, ensuring field names, constraints, and examples match the JSON Schema.

Tasks

- Create `04-protocol/ENVELOPE.md` (if not present) or update it to:
  - Reference `envelope.schema.json` as normative.
  - Document all fields exactly as in schema: protocol, id, time, sender, receiver, intent, correlation_id, reply_to, context, safety, payload, refs.
  - Explicitly state PN constraints reflected in the schema (cold-only + player_safe).
  - Provide at least 3 example envelopes that validate against the schema.
- Add a short “Versioning & Compatibility” section matching `protocol.version` semantics.

Acceptance Criteria

- ENVELOPE.md exists and matches envelope.schema.json semantics with no discrepancies.
- Examples validate using `jsonschema` CLI or the repo’s `tools` (see separate tool issue).
- README at `04-protocol/README.md` links to ENVELOPE.md as the normative spec.

References

- `04-protocol/envelope.schema.json`
- `04-protocol/README.md`
- `00-north-star/PN_PRINCIPLES.md`

Branch & Validation

- Branch off `feature/layer4-protocol-plan` as `feature/l4-align-envelope-docs`.
- Validate sample JSON with `jsonschema` (local) or attach temporary script until tools integration lands.

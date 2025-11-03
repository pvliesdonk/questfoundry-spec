Title: Spec: Define Layer 4 Envelope v1.0

Summary

- Define a transport-agnostic, versioned envelope that wraps Layer 3–validated payloads and encodes
  PN safety and TU traceability.

Tasks

- Add `04-protocol/ENVELOPE.md` with sections: Overview, Fields, Semantics, Defaults, Error
  envelope, Examples.
- Required fields:
  - `protocol.name` (string = "qf-protocol"), `protocol.version` (semver)
  - `id` (URN/UUID), `time` (RFC3339)
  - `sender.role` (Layer 2 abbrev), `sender.agent` (optional human/agent id)
  - `receiver.role` (Layer 2 abbrev)
  - `intent` (e.g., `hook.create`, `gate.report.submit`)
  - `correlation_id`, `reply_to` (optional)
  - `context`: `hot_cold` ("hot"|"cold"), `tu` (TU id), `snapshot` ("Cold @ YYYY-MM-DD"), `loop`
    (Layer 2 loop)
  - `safety`: `player_safe` (bool), `spoilers` ("allowed"|"forbidden")
  - `payload`: `{ type, $schema, data }` (type refers to a name in 03-schemas)
  - `refs`: array of upstream IDs (hooks/TUs/ADRs/sections)
- Define MUST/SHOULD rules:
  - PN only receives messages with `context.hot_cold = "cold"` AND `safety.player_safe = true`.
  - `payload.data` MUST validate against the referenced schema in `03-schemas/`.
  - TU linkage (`context.tu`) is REQUIRED for changes targeting Cold.
- Provide examples: `ack`, `error.validation`, `error.business_rule`.
- Link `04-protocol/README.md` to `ENVELOPE.md`.

Acceptance Criteria

- `ENVELOPE.md` present with clear field definitions and defaulting/compat rules.
- Examples included and valid JSON.
- Normative text keeps transports non-normative (mappings left for APPENDIX).

References

- `00-north-star/PN_PRINCIPLES.md`
- `00-north-star/TRACEABILITY.md`
- `02-dictionary/role_abbreviations.md`, `02-dictionary/loop_names.md`
- `03-schemas/*.schema.json`

Branch & Validation

- Branch from `feature/layer4-protocol-plan` as `feature/l4-envelope`.
- No code, spec only. Ensure cross-links resolve.

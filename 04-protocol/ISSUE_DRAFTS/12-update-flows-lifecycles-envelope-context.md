Title: Update FLOWS/LIFECYCLES with envelope context and PN safety gates

Summary

- Update flow and lifecycle docs to include envelope context fields and PN safety gates explicitly
  where messages are shown.

Tasks

- In `04-protocol/FLOWS/*.md` and `04-protocol/LIFECYCLES/*.md`:
  - Add a short “Envelope overlay” section for each sequence showing `context.hot_cold`,
    `context.snapshot`, `safety.player_safe`, and `payload.type` expectations at each step.
  - For PN-related steps, add a callout that `receiver.role = PN` enforces `cold` +
    `player_safe: true` per schema.
- Where merges are shown, add a callout to include `context.tu` and record `context.snapshot` in
  `merge.approve` reply.

Acceptance Criteria

- Each flow/lifecycle doc shows envelope context and safety expectations inline with the sequence.
- PN gate enforcement is explicitly documented and matches schema.
- Merge steps consistently mention TU and snapshot stamping.

References

- `04-protocol/envelope.schema.json`
- `00-north-star/PN_PRINCIPLES.md`, `00-north-star/TRACEABILITY.md`

Branch & Validation

- Branch off `feature/layer4-protocol-plan` as `feature/l4-flows-envelope-overlay`.
- Cross-check with existing examples; no contradictions.

# Shared Pattern — Safety Protocol

STATUS: SCAFFOLD TODO: Flesh out full guidance, examples, and acceptance criteria.

Target: GPT-5 (primary)

Scope

- Enforce PN boundaries at prompt level
- Apply spoiler hygiene to player surfaces
- Respect Hot/Cold routing constraints

References

- 00-north-star/PN_PRINCIPLES.md
- 00-north-star/QUALITY_BARS.md (Presentation, Accessibility)
- 00-north-star/SPOILER_HYGIENE.md
- 04-protocol/ENVELOPE.md (PN safety invariant)

Rules

- Never route Hot content to PN. PN only receives Cold + `player_safe=true`.
- Keep spoilers out of player-facing artifacts (manuscript, codex, PN lines).
- Use diegetic phrasing for gateways; avoid mentioning codewords/state explicitly.
- Provide alt text for images; avoid sensory overload.

Checks

- Before responding, verify recipient: if PN, ensure content is player-safe and Cold.
- For gate decisions, ensure player surfaces reveal no internal logic.

